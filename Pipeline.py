from Bias import *

class Pipeline():

    def codon_bias(file_name):
        index = CodonAdaptationIndex(file_name)
        index.generate_rscu_index()
        index.generate_nrscu_index()
        index.print_rscu_index()
        print()
        index.print_nrscu_index()
        return index.rscu_index, index.nrscu_index
