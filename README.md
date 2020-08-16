# DCB-Dynamic-Codon-Bias
A web application for dynamically calculating the codon usage bias in bacterial genomes.

1) Get Prodigal to run on Lambda
2) Get Diamond to run on lambda
3) allow for the use of temporary file directories on lambda.
4) Define UI without flask using JS 
5) API gateway 
6) Lambda function that dispatches to bundled code instead of routes.py.
7) Then the code produces a zip file and sends to user

# Dependenices:

Here is a list of required dependencies

* A Linux OS
* Python version 3 with:
* Biopython https://biopython.org/
* BeautifulSoup4 https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
* Pandas https://pandas.pydata.org/
* NumPy https://www.numpy.org/
* flask http://flask.pocoo.org/
* requests module installable via pip3 install requests
* flask-bootstrap installable via pip3 install flask-bootstrap
* Prodigal: https://github.com/hyattpd/Prodigal/wiki/installation


# Setup and Installation

Ensure all dependencies are installed before these steps*

```
Clone this repository onto the local machine using git clone. The folder you clone it into will be the parent directory for the repository
Manually go into folder parent-directory-here/Dynamic-Codon-Bias/testApp/app/__init__.py
Configure the UPLOAD_FOLDER name to wherever the cloned repo is. For example r"/home/bdehlinger/DCB-Dynamic-Codon-Bias/testApp". You must include the folder up until testApp for the configuration to work properly.
Configure the MAX_CONTENT_LENGTH to desired max upload size. 16MB is 16 * 1024 *1024. Whereas 18MB is 18 * 1024 * 1024.
```

# Running the Web Application:

```
Go to a terminal and change  your view to the testApp subfolder
Enter the command: $ python3 -m flask run
Local web server will be up. This is NOT concurrent and it is highly discouraged to use the flask run command in production.
```

You may choose any number of methods for deployment! Flask is not meant for production use cases.

# References

1) Athey J, Alexaki A, Osipova E, et al. A new and updated resource for codon usage tables. BMC Bioinformatics. 2017;18(1):391. Published 2017 Sep 2. doi:10.1186/s12859-017-1793-7
2)  Puigbo P, Bravo IG and Garcia-Vallve S. (2008) CAIcal: a combined set of tools to assess codon usage adaptation. Biology Direct, 3:38.
3) - Puigbo P., Romeu A. and Garcia-Vallve S. 2008. HEG-DB: a datase of predict highly expressed genes in prokaryotic complete genomes under translational selection. Nucleic Acids Research, 36:D524-7.
4) Hilterbrand A, Saelens J, Putonti C. CBDB: the codon bias database. BMC Bioinformatics. 2012;13:62. Published 2012 Apr 26. doi:10.1186/1471-2105-13-62
5) Sharp PM, Bailes E, Grocock RJ, Peden JF, Sockett RE. Variation in the strength of selected codon usage bias among bacteria. Nucleic Acids Res. 2005;33(4):1141–1153. Published 2005 Feb 23. doi:10.1093/nar/gki242
6) Hyatt D, Chen GL, Locascio PF, Land ML, Larimer FW, Hauser LJ. Prodigal: prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics. 2010;11:119. Published 2010 Mar 8. doi:10.1186/1471-2105-11-119
7) Buchfink, Benjamin, Chao Xie, and Daniel H Huson. "Fast and Sensitive Protein Alignment Using DIAMOND." Nature Methods 12.1 (2015): 59-60. Web.
8) Chapman B, Chang J: Biopython: Python tools for computational biology. ACM SIGBIO Newslett. 2000, 20: 15-19. 10.1145/360262.360268.
9) http://flask.pocoo.org/
10) https://www.crummy.com/software/BeautifulSoup/
11) Sharp PM, Li WH. The codon Adaptation Index--a measure of directional synonymous codon usage bias, and its potential applications. Nucleic Acids Res. 1987;15(3):1281–1295.
12) Gouy M, Gautier C. Codon usage in bacteria: correlation with gene expressivity. Nucleic Acids Res. 1982;10(22):7055–7074.
13) https://gunicorn.org/
  


### Note:

Program runs in about 8.14 seconds on an averaged sized bacterial genome. 
