from Bias import *
from Bio import SeqIO
import pandas
from NCBIGet import get_accession_data, get_assembly_data
import os
import csv
import subprocess


class GeneralPipeline():
    def __init__(self):
        self.file = ''

    ### Takes a fasta file as input.  Outputs a CSV file of the biases for each codon.
    def _calculate_bias(self, fasta, filename):
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
        with open(filename + ".bias.csv", 'w') as outcsv:
            writer = csv.writer(outcsv)
            if index.codon_exception != []:
                with open(filename + "errors.txt", 'w') as error_file:
                    error_writer = csv.writer(error_file)
                    for error in index.codon_exception:
                        error_writer.writerow([error])
            writer.writerow(["Codon", "RCSU", "NRCSU", "HEG FB"])
            for entry in matrix:
                writer.writerow(entry)
        outcsv.close()

    ## Reads in the matches from diamond. This function then cleans up and standarizes the output so that there are at most 40 highly expressed 
    ## Genes in an output file called temporary.fasta. Elongation factor EF-2 is replaced with elongation factor G because they are actually
    ## the same protein. File is outputed as HEGS.fasta.
    def _get_hegs_to_forty_items(self, filename):
        df = pandas.read_table("matches", names=["Subject", "Bit", "SeqID"], skipinitialspace=True)
        df = df.replace('\[.*\]', '', regex=True)
        df["Subject"] = df["Subject"].str.strip()
        df["Subject"] = df["Subject"].apply(lambda x: ' '.join(x.split(' ')[1:]))
        df["Subject"] = df["Subject"].str.lower()
        df = df.replace("elongation factor ef-2", "elongation factor g")
        df2 = df.sort_values(["Subject", "Bit"], ascending=[True,False])
        df2 = df2.loc[df2.groupby('Subject')["Bit"].idxmax()].reset_index(drop=True)
        items = df2.SeqID.unique()
        newSeqs = []
        for seq_record in SeqIO.parse(self.file, "fasta"):
            if (seq_record.id in items):

                newSeqs.append(seq_record)
        if len(newSeqs) <38:
            print("WARNING there are less than 38 sequences.")
        with open("HEGS.fasta", "w") as handle:
            SeqIO.write(newSeqs, handle, "fasta")
        return len(newSeqs)
    ## Uses DIAMOND on the database called testDB that contains a database assembled from the identical protein groups NCBI database of the
    ## 40 highly expressed genes in bacteria. Outputs a file called matches with the sequence title, bitscore, and query sequence id. K is specified to avoid redundancy and get 
    ## the top hit for each query. Diamond has a binary in the parent working directory in this application. Diamond could be installed to avoid this change in directory.
    def _get_hegs(self, filename, directory):
        os.chdir("..")
        subprocess.call(["./diamond", "blastx", "-d", "testDB", "-q", directory + "/" + self.file, "-o", directory + "/matches", "-f", "6", "stitle", "bitscore", "qseqid", "-k", "1"])
        os.chdir(directory)


class NcbiPipe(GeneralPipeline):
    
    ## This function downloads the genome from a refseq nucleotide accession number. It delegates work to the get_accession_data method from the NCBIGet module.
    ## Self.file is the file name of the downloaded fasta file. 
    def _get_data(self, accession):
        self.file = get_accession_data(accession)
        

class NcbiAssemblyPipe(GeneralPipeline):
    
    ## This function downloads the genome from a refseq assembly accession number. It delegates work to the get_assembly_data method from the NCBIGet module.
    ## Self.file is the file name of the downloaded fasta file. 
    def _get_data(self, accession):
        self.file = get_assembly_data(accession)
        

class GenomePipe(GeneralPipeline):
    
    ## Prodigal is run on the temporaryFile(which is what the uploaded genome is called). the -d flag specifies to output a file containing all of the found protein coding sequences found. 
    def _prodigal_it(self, filename):
        subprocess.call(["prodigal", "-i", filename, "-o", "tempGenes", "-f", "gff", "-d", filename + "CDS"])
        
   ## The list of protein coding sequences is called theCDS in this case. Diamond will use this as a query sequence. 
    def _get_data(self, filename):
        self.file = (filename + "CDS")

    
## This class is to simplify access in the actual flask application. It abstracts complexity away. Both of the methods utilize a directory for the get_hegs method(diamond). This could be avoided completely by installing diamond and modifying the code instead of using the binary.
class Facade:
    
    ## This function is called when a user decides to upload a genome. First any temporary folder is removed. A new temporary folder is made. The 
    ## temporaryFile that was uploaded is moved to this temporary folder. A Genome Pipeline is created. Prodigal is run on the data. The file name is set with get_data. 
    ## Diamond is run with get_hegs. get_hegs_to_forty_items standardizes the output such that only forty genes remain. Get_bias returns a csv file into the temporary directoy. Self.file is changed in order to allow flask to actually
    ## return the csv. 
    def uploaded_genome(self, filename, directory):
        genomepipe = GenomePipe()
        genomepipe._prodigal_it(filename)
        genomepipe._get_data(filename)
        genomepipe._get_hegs(filename, directory)
        genomepipe._get_hegs_to_forty_items(filename)
        genomepipe._calculate_bias("HEGS.fasta", filename)
        self.file = filename + ".bias.csv"

    ### This function is called when a user enters a RefSeq accession. 
    ### Prodigal is first called on the uploaded genome. Then the file 
    ### name is set with get_data. get_hegs outputs the matches from running 
    ### a query against a local database. Clean_hegs is called to output only 40 
    ### HEGs as there are some duplicates and inconsistencies in the output from diamond. 
    ### get_bias actually returns the csv containing the bias statistics. The file name for facade is set to the bias csv file. 
    def ncbi(self, accession, directory):
        ncbipipe = NcbiPipe()
        ncbipipe._get_data(accession)
        ncbipipe._get_hegs(accession, directory)
        ncbipipe._get_hegs_to_forty_items(accession)
        ncbipipe._calculate_bias("HEGS.fasta", accession)
        self.file = accession + ".bias.csv"

  ### This function is called when a user enters a RefSeq Assembly accession. Prodigal is first called on the uploaded genome. Then the file name is set with get_data. get_hegs outputs the matches from running a query against a local database. Clean_hegs is called to output only 40 HEGs as there are some duplicates and inconsistencies in the output from diamond. get_bias actually returns the csv containing the bias statistics. The file name for facade is set to the bias csv file. 
    def ncbiassembly(self, accession, directory):
        ncbipipe = NcbiAssemblyPipe()
        ncbipipe._get_data(accession)
        ncbipipe._get_hegs(accession, directory)
        ncbipipe._get_hegs_to_forty_items(accession)
        ncbipipe._calculate_bias("HEGS.fasta", accession)
        self.file = accession + ".bias.csv"

