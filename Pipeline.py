import abc
import Bias
from Bio import SeqIO
import pandas
from NCBIGet import get_accession_data
import os

class GeneralPipeline(abc.ABC):
    def __init__(self):
        self.file = ''

    ### Concrete method that should take fasta input files of the list of genes. We can code and test this now.
    def get_bias(self, fasta):
        index = CodonUsageTable(fasta)
        index.generate_rcsu_table()
        index.generate_nrcsu_table()
        index.generate_hegfb_table()
        data = [index.rcsu_index, index.nrcsu_index, index.hegfb_index]
        return data

    def clean_hegs(self):
        df = pandas.read_table("temp/matches", names=["Subject", "Bit", "SeqID"], skipinitialspace=True)
        df = df.replace('\[.*\]', '', regex=True)
        print(df.head())
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


class GenomePipe(GeneralPipeline):
    
    def prodigal_it(self):
        os.system("prodigal -i temp/temporaryFile -o temp/tempGenes -f gff -d temp/theCDS")
    
    def get_data(self):
        self.file = ("temp/theCDS")
    

class Facade:

    def uploaded_genome(self):
        os.system("mkdir temp")  
        genomepipe = GenomePipe()
        genomepipe.prodigal_it()
        genomepipe.get_data()
        genomepipe.get_hegs()
        genomepipe.clean_hegs()
        genomepipe.output()

    def ncbi(self, accession):
        ncbipipe = NcbiPipe()
        ncbipipe.get_data(accession)
        ncbipipe.get_hegs()
        ncbipipe.clean_hegs()
        ncbipipe.output()


facade = Facade()
facade.ncbi('AE014075.1')
facade.ncbi('AP018036.1')
