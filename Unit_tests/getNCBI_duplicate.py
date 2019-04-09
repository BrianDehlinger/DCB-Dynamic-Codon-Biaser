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

def get_accession_data(accession):
    the_request = requests.get("https://www.ncbi.nlm.nih.gov/nuccore/" + accession)
    global soup 
    soup = bs4.BeautifulSoup(the_request.text)
    print("2")
    

get_accession_data("NC_003888.3")
print('3')
def find_url(p, soup):
	theURL = ""
	for a in soup.find_all("a", href=True):
		if('/assembly' in a['href']):
			theURL = theURL + a['href']
		break
	print(theURL)                 
	
	#except:
		#print("invalid assembly")
                             


find_url('/assembly', soup)

