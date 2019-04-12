import requests
import bs4
import re
import os
import codecs
#tests to see if and where code stops 
print("1")

## Base URL Of NCBI common to all URLS
temporaryURL = 'https://www.ncbi.nlm.nih.gov'
#soup = ""
#can I call a function within a function when testing??
try:
	def get_accession_data(accession):
		the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
		soup = bs4.BeautifulSoup(the_request.text)
    
		def find_url(soup):
			theURL = ""
			for a in soup.find_all("a", href=True):
				if('/assembly' in a['href']):
					theURL = theURL + a['href']
					break
			temp1 = 'https://www.ncbi.nlm.nih.gov' + theURL
			print(temp1)
		find_url(soup)
except:
	print("invalid")
	
	
    temporaryURL2 = temporaryURL + find_url('/assembly', soup)
    new_request = requests.get(temporaryURL2)
    new_soup = bs4.BeautifulSoup(new_request.text)
    items = new_soup.find("div", class_="rprt")

## Get's the assembly URL and gets the assembly url HTML file.
    temporaryURL2 = temporaryURL + find_url('/assembly', items)

    new_request = requests.get(temporaryURL2)
    new_soup = bs4.BeautifulSoup(new_request.text)

## Searches for the FTP File folder in the assembly HTML webpage.
    url = ''
    items = new_soup.find_all('a', href=True)
    for a in items:
        if "ftp://" in a['href']:
            url = a['href']
            break


get_accession_data('NC_003888.3')


