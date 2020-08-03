import requests
import bs4
import re
import glob
import gzip
import io


## Base URL Of NCBI common to all URLS
NCBIBASEURL = 'https://www.ncbi.nlm.nih.gov'


## Function that finds first href that contain part of the urlPiece in the url. First the NCBI
## sidebar is parsed to find an assembly link. If an assembly link is not present then the 
## program will attempt to find the assembly link in the viewer. If however, the organsim is not a bacteria, then the program will raise an error. Similiary if there is no assembly link the program will also throw an error.

def _find_url(urlPiece, soup, viewer_soup):
    try:
        the_url = ''
        if 'Bacteria' not in str(viewer_soup):
            raise ValueError("The Nucleotide accession specified is not a Bacteria!")
        for a in soup.find_all('a', href=True):
            if('/assembly' in a['href']):
                the_url = NCBIBASEURL + a['href']
                break
        if the_url:
            return the_url
        else:
            for a in viewer_soup.find_all('a', href=True):
                if('/assembly' in a['href']):
                    the_url = a['href']
                    break
            if the_url:
                return the_url
            else: 
                raise ValueError("Invalid accession, no assembly URL")
    except ValueError as e:
        print(e)

def _get_soup_nuccore(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
    return bs4.BeautifulSoup(the_request.text)
		
def _get_viewer_soup_nuccore(accession):
    viewerNucleotide = requests.get("https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id="+accession+"&db=nuccore&extrafeat=0&fmt_mask=0&retmod=html&withmarkup=on&tool=portal&log")
    return bs4.BeautifulSoup(viewerNucleotide.text)

def _get_soup_assembly(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/assembly/" + accession)
    return bs4.BeautifulSoup(the_request.text)

## Gets the HTML file for the NCBI accession number of interest. Utilizes commands instead of global variables to reduce semantic coupling!
def get_accession_data(accession):
    soup = _get_soup_nuccore(accession)
    viewer_soup = _get_viewer_soup_nuccore(accession)

## Gets the URL for the Assembly link from NCBI's refseq accession
    temporary_url_two = _find_url('/assembly', soup, viewer_soup)
    new_request = requests.get(temporary_url_two)
    new_soup = bs4.BeautifulSoup(new_request.text)
    

## Finds the div element with a rprt class
    if not new_soup.find_all('a', attrs={'href': re.compile("^ftp://ftp.ncbi.nlm.nih.gov/genomes/all")}):
        items = new_soup.find("div", class_="rprt")

## Get's the assembly URL and gets the assembly url HTML file.
        temporary_url_two = _find_url('/assembly', items, viewer_soup)
        new_request = requests.get(temporary_url_two)
        new_soup = bs4.BeautifulSoup(new_request.text)

## Searches for the FTP File folder in the assembly HTML webpage.
    url = ''
    item = new_soup.find('a', href=True, text='FTP directory for RefSeq assembly')
    url = item['href']


## Constructs the download URL and gets the information onto the system
    last_piece_of_url = re.findall('[^\/]+$', url)[0]
    downloadUrl = url + "/" + last_piece_of_url + "_cds_from_genomic.fna.gz"

    decompressed_data = gzip.decompress(requests.get(download_url).content)
    return {"filename": last_piece_of_url + "_cds_from_genomic.fna",
            "data": decompressed_data}

def get_assembly_data(accession):
    soup = _get_soup_assembly(accession)
    item = soup.find('a', href=True, text='FTP directory for RefSeq assembly')
    url = item['href']

    last_piece_of_url = re.findall('[^\/]+$', url)[0]
    download_url = url + "/" + last_piece_of_url + "_cds_from_genomic.fna.gz"
    decompressed_data = gzip.decompress(requests.get(download_url).content)
    #return last_piece_of_url + "_cds_from_genomic.fna"
    return {"filename": last_piece_of_url + "_cds_from_genomic.fna",
            "data": decompressed_data}




