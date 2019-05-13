# DCB-Dynamic-Codon-Bias Database
A web application for dynamically calculating the codon usage bias in bacterial genomes.

**This web application will utilize a database to store the results of the entirety of all bacteria that have complete RefSeq Assemblies on NCBI as of 5/11/2019**

Design:


SQL Query language will be utilized to access a local database such as PostgreSQL
OR
Kibana and Elastic Search a will be utilzied to enable ultrafast search and visualization.

Data will be stored on a local server running Linux and queries will be possible through a web application.
Ideally visualization will be done live.

Requirements:

-Website should be concurrent, so code must be written to prevent concurrency issues.
-Website should allow for reasonable extension of functions. For example different kinds of queries to the coding sequences might be added later and highly expressed genes should be stored for every genome- This will be a fraction of the data from NCBI(16.3GB compressed).
-Website should provide reasonable information on errors during annotation process.
-Queries should return results immediately(should not take longer than a few seconds to query the entire database.(So if SQL doesn't work can we ADD elasticsearch?)
-Data integrity needs to be ensured with checksum from NCBI. 

First all files must be downloaded(DONE)
Second: a database must be created that can be populated with data from the program. The database should have a primary key being the assembly accession. Other info will be the organism, taxonomic information, codon usage statistics, and file containing 40 highly expressed genes(name). 
Third: Data must be indexed properly to ensure fast retrieval, aggregation and queries. (Elastic Search)
3.5 Database queries connected to web application.
    Robustness, Security, Integrity of database. 
Foruth: Visualization and summary statistic layer can be added on top into web application after local testing. Flask or Django?
Fifth: Deployment options









# Dependenices:

Here is a list of required dependencies

- A Linux OS
- Python version 3 with:
    1) Biopython https://biopython.org/
    2) BeautifulSoup4 https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
    3) Pandas https://pandas.pydata.org/
    4) NumPy https://www.numpy.org/
    5) flask http://flask.pocoo.org/
    6) requests module installable via pip3 install requests
    6) flask-bootstrap installable via pip3 install flask-bootstrap
    7) flask-sqlalchemy
    8) flask-migrate

- Postgresql
- Prodigal: https://github.com/hyattpd/Prodigal/wiki/installation


# Setup and Installation

*Ensure all dependencies are installed before these steps*

1) Clone this repository onto the local machine using git clone. The folder you clone it into will be the parent directory for the repository
2) Manually go into folder parent-directory-here/Dynamic-Codon-Bias/testApp/app/__init__.py
    a) Configure the UPLOAD_FOLDER name to wherever the cloned repo is. For example r"/home/bdehlinger/DCB-Dynamic-Codon-Bias/testApp". You must include the folder up until testApp for the configuration to work properly.
    b) Configure the MAX_CONTENT_LENGTH to desired max upload size. 16MB is 16 * 1024 *1024. Whereas 18MB is 18 * 1024 * 1024.


# Running the Web Application:

1) Go to a terminal and change  your view to the testApp subfolder
2) Enter the command:
    $ python3 -m flask run
3) Local web server will be up. This is NOT concurrent and it is highly discouraged to use the flask run command in production.

You may choose any number of methods for deployment!

Gunicorn is our choice.

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
  


Note:

Program runs in about 8.14 seconds on an averaged sized bacterial genome. 
