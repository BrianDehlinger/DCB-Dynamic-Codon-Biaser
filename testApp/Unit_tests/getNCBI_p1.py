import requests
import bs4
import re
import os
import codecs
#tests to see if and where code stops 
#print("1")


#This is the first test portion that makes the first request 


## Base URL Of NCBI common to all URLS
temporaryURL = 'https://www.ncbi.nlm.nih.gov'
#soup = ""
#can I call a function within a function when testing??
def get_accession_data(accession):
	the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
	soup = bs4.BeautifulSoup(the_request.text)
    
	try:
		def find_url(soup):
			theURL = ""
			for a in soup.find_all("a", href=True):
				if('/assembly' in a['href']):
					theURL = theURL + a['href']
					break
			temp1 = 'https://www.ncbi.nlm.nih.gov' + theURL
			return(temp1)
		find_url(soup)
	except:
		print("invalid")



get_accession_data('NC_003888.3')


