import unittest
from getNCBI_duplicate import get_accession_data
import codecs

class TestCalc(unittest.TestCase):

	def test_find_url(self):
		result = get_accession_data('NC_003888.3')
		real_URL = "https://www.ncbi.nlm.nih.gov/assembly?LinkName=nuccore_assembly&from_uid=32141095"
		self.assertEqual(result, real_URL)
        self.assertEqual(find_url('NC_00388'), "invalid" )


if __name__ == '__main__':
	unittest.main()


#test htmls
#SOUP contains a good URL 
#

#this would be how to call it without the main method		
#python -m unittest get_test.py
