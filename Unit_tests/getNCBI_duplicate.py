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

def get_accession_data(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
    soup = bs4.BeautifulSoup(the_request.text)
    
    def find_url(p, soup):
    	theURL = ""
    	for a in soup.find_all("a", href=True):
    		if('assembly' in a['href']):
    			theURL = theURL + a['href']
    			break
    	print(theURL)
    	temp1 = 'https://www.ncbi.nlm.nih.gov' +  find_url('/assembly', soup)
    	print('2')
    	print(temp1)
    	find_url('/assembly', soup)
		
get_accession_data('NC_003888.3')


