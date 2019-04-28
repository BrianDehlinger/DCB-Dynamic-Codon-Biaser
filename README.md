# DCB-Dynamic-Codon-Bias
A web application for dynamically calculating the codon usage bias in bacterial genomes.

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



    
    
  


Note:

Program runs in about 8.14 seconds on an averaged sized bacterial genome. 
