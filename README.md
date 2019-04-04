# DCB-Dynamic-Codon-Bias
A tool for dynamically calculating the codon usage bias in bacterial genomes.


Currently:

We have code to calculate codon bias, we have code to take either NCBI refseq genome data and annotate it. We have code to actually pull the relevant
HEGs from the predicted CDS or actual CDS. We just need to:

1) Assemble the complete pipelines. Transfer current code to dummy code. Make sure everything still works.
2) Bugfix and make code softer.
3) Implement an output function to output codon bias into a nice pandas dataframe on an HTML webpage.
4) Input validation

Then we can focus on improving the design of our code by refactoring, improving user interface, and then more stress testing.

