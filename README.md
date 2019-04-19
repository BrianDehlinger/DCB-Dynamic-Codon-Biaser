# DCB-Dynamic-Codon-Bias
A tool for dynamically calculating the codon usage bias in bacterial genomes.

Dependenices:

In order for this code to work properly the following are needed:

Linux OS
Python version 3 with:
    Biopython
    BeautifulSoup4
    Pandas
    NumPy
    flask

Prodigal

In order to configure the program to run properly:
  1) Manually go into your folder DCB-Dynamic-Codon-Bias/testApp/app/__init__.py
  2) Manually configure the UPLOAD_FOLDER name to wherever the cloned repo is.
  3) Configure the MAX_CONTENT_LENGTH to desired max upload size. 16MB is 16 * 1024 *1024. Whereas 18MB is 18 * 1024 * 1024.
  4) Change into the 
  


Note:

Program runs in about 8.14 seconds on an averaged sized bacterial genome. 
