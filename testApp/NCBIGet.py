import requests
import bs4
import re
import os
import subprocess
import glob


## Base URL Of NCBI common to all URLS
the_request = None
temporaryURL = 'https://www.ncbi.nlm.nih.gov'
soup = None
viewer_nucleotide = None
viewer_soup = None

## Function that finds first href that contain part of the urlPiece in the url. First the NCBI
## sidebar is parsed to find an assembly link. If an assembly link is not present then the 
## program will attempt to find the assembly link in the viewer. If however, the organsim is not a bacteria, then the program will raise an error. Similiary if there is no assembly link the program will also throw an error.

def find_url(urlPiece, soup, viewer_soup):
    try:
        theURL = ''
        if 'Bacteria' not in str(viewer_soup):
            raise ValueError("The Nucleotide accession specified is not a Bacteria!")
        for a in soup.find_all('a', href=True):
            if('/assembly' in a['href']):
                theURL = temporaryURL + a['href']
                break
        if theURL:
            return theURL
        else:
            for a in viewer_soup.find_all('a', href=True):
                if('/assembly' in a['href']):
                    theURL = a['href']
                    break
            if theURL:
                return theURL
            else: 
                raise ValueError("Invalid accession, no assembly URL")
    except ValueError as e:
        print(e)

def initialRequest(accession):
        global the_request
        the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
        global soup
        soup = bs4.BeautifulSoup(the_request.text)
        global viewer_nucleotide
        viewerNucleotide = requests.get("https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id="+accession+"&db=nuccore&extrafeat=0&fmt_mask=0&retmod=html&withmarkup=on&tool=portal&log")
        global viewer_soup
        viewer_soup = bs4.BeautifulSoup(viewerNucleotide.text)

## Gets the HTML file for the NCBI accession number of interest.
def get_accession_data(accession):
    initialRequest(accession)

## Gets the URL for the Assembly link from NCBI's refseq accession
    temporaryURL2 = find_url('/assembly', soup, viewer_soup)
    new_request = requests.get(temporaryURL2)
    new_soup = bs4.BeautifulSoup(new_request.text)
    

## Finds the div element with a rprt class
    if not new_soup.find_all('a', attrs={'href': re.compile("^ftp://ftp.ncbi.nlm.nih.gov/genomes/all")}):
        items = new_soup.find("div", class_="rprt")

## Get's the assembly URL and gets the assembly url HTML file.
        temporaryURL2 = find_url('/assembly', items, viewer_soup)
        new_request = requests.get(temporaryURL2)
        new_soup = bs4.BeautifulSoup(new_request.text)

## Searches for the FTP File folder in the assembly HTML webpage.
    url = ''
    items = new_soup.find_all('a', href=True)
    for a in items:
        if "ftp://" in a['href']:
            url = a['href']
            break

## Constructs the download URL and gets the information onto the system
    lastPieceOfUrl = re.findall('[^\/]+$', url)[0]
    downloadUrl = url + "/" + lastPieceOfUrl + "_cds_from_genomic.fna.gz"
    subprocess.call(["wget", downloadUrl])
    subprocess.Popen(["gunzip"] + glob.glob("*.gz"))
    return lastPieceOfUrl + "_cds_from_genomic.fna"

def get_assembly_data(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/assembly/" + accession)
    soup = bs4.BeautifulSoup(the_request.text)
    url = ''
    items = soup.find_all('a', href=True)
    for a in items:
        if "ftp://" in a['href']:
            url = a['href']
            break

    lastPieceOfUrl = re.findall('[^\/]+$', url)[0]
    downloadUrl = url + "/" + lastPieceOfUrl + "_cds_from_genomic.fna.gz"
    subprocess.call(["wget", downloadUrl])
    subprocess.Popen(["gunzip"] + glob.glob("*.gz"))
    return lastPieceOfUrl + "_cds_from_genomic.fna"


def get_assembly_accession(accession):
    initialRequest(accession)
    temporaryURL2 = find_url('/assembly', soup, viewer_soup)
    new_request = requests.get(temporaryURL2)
    new_soup = bs4.BeautifulSoup(new_request.text)
    if not new_soup.find_all('a', attrs={'href': re.compile("^ftp://ftp.ncbi.nlm.nih.gov/genomes/all")}):
        items = new_soup.find("div", class_="rprt")
        temporaryURL2 = find_url('/assembly', items, viewer_soup)
        new_request = requests.get(temporaryURL2)
        new_soup = bs4.BeautifulSoup(new_request.text)
    assemblyID = temporaryURL2.rsplit('/', 1)[-1]
    if not assemblyID:
        raise ValueError("An error has occured at get_assembly_accession")
    return assemblyID
    
  


    
   



