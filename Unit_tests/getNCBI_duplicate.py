import requests
import bs4
import re
import os
import codecs
#tests to see if and where code stops 
print("1")

## Base URL Of NCBI common to all URLS
	temporaryURL = 'https://www.ncbi.nlm.nih.gov'
        # a good soup with /assmebly hrefs
    lemonrice = codecs.open("soup.html", 'r')
    # a gross soup with no /assembly(s)
    peasoup = ""
# # a soup that will make (me) sick invalid html
    chowder = ""


## Function that finds first href that contain part of the urlPiece in the url. 
def find_url(urlPiece, S):
    theURL = ''
    
    try:
    for a in soup.find_all('a', href=True):
        if('/assembly' in a['href']):
            theURL = theURL + a['href']
            break
    print(theURL)
    
    catch:
    print("invalid assembly")



## Gets the URL for the Assembly link from NCBI's refseq accession 
	temporaryURL2 = temporaryURL + find_url('/assembly', soup)
	new_request = requests.get(temporaryURL2)
	new_soup = bs4.BeautifulSoup(new_request.text)

## Finds the div element with a rprt class  
	items = new_soup.find("div", class_="rprt")

## Get's the assembly URL and gets the assembly url HTML file.
	temporaryURL2 = temporaryURL + find_url('/assembly', items)

	new_request = requests.get(temporaryURL2)
	#features is the default html parser
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
	downloadUrl = url + "/" + lastPieceOfUrl + "_genomic.fna.gz"
	os.system("wget " + downloadUrl)

#Test to see if and where code stops
print('2')
## Test code to verify it works
get_accession_data('NC_003888.3')
get_accession_data()
get_accession_data()
get_accession_data()
#Test to see if and when code stops
print('3')
