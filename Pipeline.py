import abc
import Bias

class GeneralPipeline(abc.ABC):
    def __init__(self, members):
        self.members = members

    ### Concrete method that should take fasta input files of the list of genes. We can code and test this now.
    def get_bias(self, fasta):
	print("get_bias has been called")
        index = CodonUsageTable(fasta)
	index.generate_rcsu_table()
	index.generate_nrcsu_table()
	index.generate_hegfb_table()
	data = [index.rcsu_index, index.nrcsu_index, index.hegfb_index]
	return data

    @abc.abstractmethod
    ### This will vary. So far we have NCBI and a genome.
    def get_data(self):
        pass

    @abc.abstractmethod
    def gethegs(self):
        pass

    ## Concrete method that should be the same for all pipelines.
    def output(self):
        print("output has been called")


class NcbiPipe(GeneralPipeline):
    def get_data(self):
        print("ncbi get_data has been called")

    ## Use Biopython to lookup the fasta file for a RefSeqID number. Input validation should be here as well. Make sure it is a fasta file.
    def get_data_ncbi(self, accession):
        print(accession)

    def gethegs(self):
        print("ncbi gethegs has been called")


class GenomePipe(GeneralPipeline):


class Facade:

    def uploaded_genome(self, file):    
        print("The genome was successfully uploaded")   

    def ncbi(self, accession):
        print(accession)


## Let's first make the web page redirector. Worry about the other stuff later.....

### When we press a button the code should execute the facade call.
### It seems the code here takes care of sessions dynamically.


def hello:


