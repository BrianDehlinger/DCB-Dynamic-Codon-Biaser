import abc
from Bias import *
from Bio import SeqIO
import pandas
from NCBIGet import get_accession_data
import os
import csv
from timeit import default_timer as timer

class GeneralPipeline(abc.ABC):
    def __init__(self):
        self.file = ''
        self.error_string = ""

    ### Takes a fasta file as input.  Outputs a CSV file of the biases for each codon.
    def get_bias(self, fasta):
        index = CodonUsageTable(fasta)
        index.generate_rcsu_table()
        index.generate_nrcsu_table()
        index.generate_hegfb_table()
        matrix = [[0 for x in range(4)] for y in range(64)]
        i = 0
        for item in sorted(index.rcsu_index):
            matrix[i][0] = item
            matrix[i][1] = index.rcsu_index[item]
            i += 1
        i = 0
        for item in sorted(index.nrcsu_index):
            matrix[i][2] = index.nrcsu_index[item]
            i += 1
        i = 0
        for item in sorted(index.hegfb_index):
            matrix[i][3] = index.hegfb_index[item]
            i += 1
        with open(self.file + ".bias.txt", 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Codon", "RCSU", "NRCSU", "HEG FB"])
            for entry in matrix:
                writer.writerow(entry)
        outcsv.close()
        if index.codon_exception == True:
            self.error_string = "Illegal Codon in File; data may be inaccurate."


    def clean_hegs(self):
        df = pandas.read_table("temp/matches", names=["Subject", "Bit", "SeqID"], skipinitialspace=True)
        df = df.replace('\[.*\]', '', regex=True)
        df["Subject"] = df["Subject"].str.strip()
        df["Subject"] = df["Subject"].apply(lambda x: ' '.join(x.split(' ')[1:]))
        df = df.replace("elongation factor EF-2", "elongation factor G")
        df2 = df.sort_values(["Subject", "Bit"], ascending=[True,False])
        df2 = df2.loc[df2.groupby('Subject')["Bit"].idxmax()].reset_index(drop=True)
        items = df2.SeqID.unique()
        newSeqs = []
        for seq_record in SeqIO.parse(self.file, "fasta"):
            if (seq_record.id in items):
                print(seq_record)
                newSeqs.append(seq_record)
        print(len(newSeqs))
        

        with open("temp/temporary.fasta", "w") as handle:
            SeqIO.write(newSeqs, handle, "fasta")

    def get_hegs(self):
        os.system("./diamond blastx -d testDB -q " + self.file + " -o temp/matches -f 6 stitle bitscore qseqid -k 1")

    ## Concrete method that should be the same for all pipelines.
    def output(self):
        print("output has been called")


class NcbiPipe(GeneralPipeline):
    
    ## This function downloads the genome from a refseq accession number
    def get_data(self, accession):
        self.file = "temp/" + get_accession_data(accession)
        print(self.file)

class GenomePipe(GeneralPipeline):
    
    def prodigal_it(self):
        os.system("prodigal -i temp/temporaryFile -o temp/tempGenes -f gff -d temp/theCDS")
    
    def get_data(self):
        self.file = ("temp/theCDS")
    

class Facade:

    def uploaded_genome(self):
        os.system("rm -rf temp")
        os.system("mkdir temp")
        os.system("mv temporaryFile temp") 
        genomepipe = GenomePipe()
        genomepipe.prodigal_it()
        genomepipe.get_data()
        genomepipe.get_hegs()
        genomepipe.clean_hegs()
        genomepipe.get_bias('temp/temporary.fasta')
        self.file = os.getcwd() + "/" +  genomepipe.file + ".bias.txt"

    def ncbi(self, accession):
        os.system("rm -rf temp")
        os.system("mkdir temp")
        ncbipipe = NcbiPipe()
        ncbipipe.get_data(accession)
        ncbipipe.get_hegs()
        ncbipipe.clean_hegs()
        ncbipipe.get_bias('temp/temporary.fasta')
        self.file = os.getcwd() + "/" +  ncbipipe.file + ".bias.txt"
'''
facade = Facade()
start = timer()
facade.ncbi('ABAW00000000')
end = timer()
print(end - start)
'''

