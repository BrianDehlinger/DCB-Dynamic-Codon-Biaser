import requests
import bs4
import re
import os

## Gets the HTML file for the NCBI accession number of interest.
def get_accession_data(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
    soup = bs4.BeautifulSoup(the_request.text)
    marker = False

## Base URL Of NCBI common to all URLS
    temporaryURL = 'https://www.ncbi.nlm.nih.gov'

## Function that finds first href that contain part of the urlPiece in the url. 
    def find_url(urlPiece, soup):
        theURL = ''
        for a in soup.find_all('a', href=True):
            if('/assembly' in a['href']):
                theURL = temporaryURL + a['href']
                break
        if theURL:
            return theURL
        else:
            new_request = requests.get("https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id="+accession+"&db=nuccore&extrafeat=0&fmt_mask=0&retmod=html&withmarkup=on&tool=portal&log")
            soup = bs4.BeautifulSoup(new_request.text)
            for a in soup.find_all('a', href=True):
                if('/assembly' in a['href']):
                    theURL = a['href']
                    marker = True
                    break
        return theURL

## Gets the URL for the Assembly link from NCBI's refseq accession
    temporaryURL2 = find_url('/assembly', soup)
    print(temporaryURL2)
    new_request = requests.get(temporaryURL2)
    new_soup = bs4.BeautifulSoup(new_request.text)

## Finds the div element with a rprt class
    if not new_soup.find_all('a', attrs={'href': re.compile("^ftp://ftp.ncbi.nlm.nih.gov/genomes/all")}):
        items = new_soup.find("div", class_="rprt")

## Get's the assembly URL and gets the assembly url HTML file.
        temporaryURL2 = find_url('/assembly', items)

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
    os.chdir("temp")
    os.system("wget " + downloadUrl)
    os.system("gunzip -f  *.gz")
    os.chdir("..")
    return lastPieceOfUrl + "_cds_from_genomic.fna"


