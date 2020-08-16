from Bias import *
from Bio import SeqIO
import pandas
from NCBIGet import get_accession_data, get_assembly_data
import os
import csv
import io
import subprocess
import tempfile
import shutil


class GeneralPipeline():
    def __init__(self):
        self.file = ''

    def calculate_bias(self, raw_fasta):
        tmpdir = tempfile.mkdtemp()
        fasta = os.path.join(tmpdir, 'fasta_input_to_bio_python')
        with open(fasta, 'w') as f:
            f.write(raw_fasta['hegs'])
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
        shutil.rmtree(tmpdir)
        return index, matrix

    def write_bias(self, filename, index, matrix):
        output_buffer = io.StringIO()
        error_output = None
        writer = csv.writer(output_buffer)
        if index.codon_exception != []:
            error_buffer = io.StringIO()
            error_writer = csv.writer(error_buffer)
            for error in index.codon_exception:
                error_writer.writerow([error])
            error_buffer.seek(0)
            error_output = error_buffer.read()
        writer.writerow(["Codon", "RCSU", "NRCSU", "HEG FB"])
        for entry in matrix:
            writer.writerow(entry)
        output_buffer.seek(0)
        output = output_buffer.read()
        output_buffer.close()
        error_buffer.close()
        return {"filename": filename, "output": output, "errors": error_output}

    # Reads in the matches from diamond. This function then cleans up and standarizes the output so that there are at most 40 highly expressed
    # Genes in an output file called temporary.fasta. Elongation factor EF-2 is replaced with elongation factor G because they are actually
    # the same protein. File is outputed as HEGS.fasta.
    def _get_hegs_to_forty_items(self, diamond_output, tmpdir, temp_cds_file):
        input_buffer = io.StringIO(diamond_output)
        df = None
        with input_buffer:
            df = pandas.read_table(
                input_buffer,
                names=[
                    "Subject",
                    "Bit",
                    "SeqID"],
                skipinitialspace=True)
        df = df.replace(r'\[.*\]', '', regex=True)
        df["Subject"] = df["Subject"].str.strip()
        df["Subject"] = df["Subject"].apply(
            lambda x: ' '.join(x.split(' ')[1:]))
        df["Subject"] = df["Subject"].str.lower()
        df = df.replace("elongation factor ef-2", "elongation factor g")
        df2 = df.sort_values(["Subject", "Bit"], ascending=[True, False])
        df2 = df2.loc[df2.groupby(
            'Subject')["Bit"].idxmax()].reset_index(drop=True)
        items = df2.SeqID.unique()
        newSeqs = []
        for seq_record in SeqIO.parse(temp_cds_file, "fasta"):
            if (seq_record.id in items):
                newSeqs.append(seq_record)
        if len(newSeqs) < 38:
            print("WARNING there are less than 38 sequences.")
        temp_file = os.path.join(tmpdir, 'hegs')
        with open(temp_file, "w") as handle:
            SeqIO.write(newSeqs, handle, "fasta")
        hegs = None
        with open(temp_file, 'r') as handle:
            hegs = handle.read()
        os.remove(temp_file)
        return hegs

    # Uses DIAMOND on the database called testDB that contains a database assembled from the identical protein groups NCBI database of the
    # 40 highly expressed genes in bacteria. Outputs a file called matches with the sequence title, bitscore, and query sequence id. K is specified to avoid redundancy and get
    # the top hit for each query. Diamond has a binary in the parent working
    # directory in this application. Diamond could be installed to avoid this
    # change in directory.
    def get_hegs(self, filename):
        hegs = None
        try:
            tmpdir = tempfile.mkdtemp()
            temp_diamond_output_file = os.path.join(tmpdir, filename)
            temp_cds_file = os.path.join(tmpdir, 'input_to_diamond')
            with open(temp_cds_file, 'w') as file:
                file.write(self.cds_data)
            subprocess.call(["./diamond",
                             "blastx",
                             "-d",
                             "testDB",
                             "-q",
                             temp_cds_file,
                             "-o",
                             temp_diamond_output_file,
                             "-f",
                             "6",
                             "stitle",
                             "bitscore",
                             "qseqid",
                             "-k",
                             "1"])
            with open(temp_diamond_output_file, 'r') as file:
                diamond_output = file.read()
                hegs = self._get_hegs_to_forty_items(
                    diamond_output, tmpdir, temp_cds_file)
        finally:
            shutil.rmtree(tmpdir)
        return {"filename": filename, "hegs": hegs}


class NcbiPipe(GeneralPipeline):

    # This function downloads the genome from a refseq nucleotide accession number. It delegates work to the get_accession_data method from the NCBIGet module.
    # Self.file is the file name of the downloaded fasta file.
    def _get_data(self, accession):
        assembly_data = get_accession_data(accession)
        self.cds_data = assembly_data['data'].decode("utf-8")
        self.file_name = assembly_data['filename']


class NcbiAssemblyPipe(GeneralPipeline):
    # This function downloads the genome from a refseq assembly accession number. It delegates work to the get_assembly_data method from the NCBIGet module.
    # Self.file is the file name of the downloaded fasta file.
    def _get_data(self, accession):
        assembly_data = get_assembly_data(accession)
        self.cds_data = assembly_data['data']
        self.file_name = assembly_data['filename']


class GenomePipe(GeneralPipeline):

    # Prodigal is run on the temporaryFile(which is what the uploaded genome
    # is called). the -d flag specifies to output a file containing all of the
    # found protein coding sequences found.
    def _get_data(self, file_name, genome_data):
        try:
            tmpdir = tempfile.mkdtemp()
            temp_input_file_to_prodigal = os.path.join(tmpdir, file_name)
            temp_output_file = os.path.join(tmpdir, 'prodigal_output')
            with open(temp_input_file_to_prodigal, 'w') as file:
                file.write(genome_data)
            subprocess.call(["/tmp/prodigal",
                             "-i",
                             temp_input_file_to_prodigal,
                             "-o",
                             os.path.join(tmpdir,
                                          "tempGenes"),
                             "-f",
                             "gff",
                             "-d",
                             temp_output_file])
            with open(temp_output_file, 'r') as file:
                self.file_name = file_name
                self.cds_data = file.read()
        finally:
            shutil.rmtree(tmpdir)

# This class is to simplify access in the actual flask application. It
# abstracts complexity away. Both of the methods utilize a directory for
# the get_hegs method(diamond). This could be avoided completely by
# installing diamond and modifying the code instead of using the binary.


class Facade:

    # This function is called when a user decides to upload a genome. First any temporary folder is removed. A new temporary folder is made. The
    # temporaryFile that was uploaded is moved to this temporary folder. A Genome Pipeline is created. Prodigal is run on the data. The file name is set with get_data.
    # Diamond is run with get_hegs. get_hegs_to_forty_items standardizes the output such that only forty genes remain. Get_bias returns a csv file into the temporary directoy. Self.file is changed in order to allow flask to actually
    # return the csv.
    def uploaded_genome(self, file_name, genome_data):
        genomepipe = GenomePipe()
        genomepipe._get_data(file_name, genome_data)
        hegs_fasta = genomepipe.get_hegs(file_name)["hegs"]
        index, matrix = genomepipe.calculate_bias(hegs_fasta)
        parseable_result = genomepipe.write_bias(file_name, index, matrix)
        csv_output, errors = parseable_result['output'], parseable_result['errors']
        return {
            "hegs": hegs_fasta['hegs'],
            "file_name": file_name,
            "csv_data": csv_output,
            "errors": errors}

    # This function is called when a user enters a RefSeq accession. Prodigal is first called on the uploaded genome. Then the file name is set with get_data.
    # get_hegs outputs the matches from running a query against a local database. Clean_hegs is called to output only 40 HEGs as there are some duplicates and
    # inconsistencies in the output from diamond. get_bias actually returns the csv containing the bias statistics. The file name for facade is set to the
    # bias csv file.
    def ncbi(self, accession):
        ncbipipe = NcbiPipe()
        ncbipipe._get_data(accession)
        hegs_fasta = ncbipipe.get_hegs(accession)
        index, matrix = ncbipipe.calculate_bias(hegs_fasta)
        parseable_result = ncbipipe.write_bias(accession, index, matrix)
        csv_output, errors = parseable_result['output'], parseable_result['errors']
        return {
            "hegs": hegs_fasta['hegs'],
            "file_name": accession,
            "csv_data": csv_output,
            "errors": errors}

  # This function is called when a user enters a RefSeq Assembly accession.
  # Prodigal is first called on the uploaded genome. Then the file name is
  # set with get_data. get_hegs outputs the matches from running a query
  # against a local database. Clean_hegs is called to output only 40 HEGs as
  # there are some duplicates and inconsistencies in the output from
  # diamond. get_bias actually returns the csv containing the bias
  # statistics. The file name for facade is set to the bias csv file.
    def ncbiassembly(self, accession):
        ncbipipe = NcbiAssemblyPipe()
        ncbipipe._get_data(accession)
        hegs_fasta = ncbipipe.get_hegs(accession)
        index, matrix = ncbipipe.calculate_bias(hegs_fasta)
        parseable_result = ncbipipe.write_bias(accession, index, matrix)
        csv_output, errors = parseable_result['output'], parseable_result['errors']
        return {
            "hegs": hegs_fasta['hegs'],
            "file_name": accession,
            "csv_data": csv_output,
            "errors": errors}
