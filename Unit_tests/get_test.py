import unittest
from getNCBI_duplicate import find_url
import codecs
#test for empty href
#test for no assembly
lemonrice = codecs.open("soup.html", 'r')
peasoup = codecs.open("psoup.html", 'r')
chowder = codecs.open("csoup.html", 'r')
class TestCalc(unittest.TestCase):

	def test_find_url(self):
		result = find_url('/assembly', lemonrice)
		real_URL = "https://www.ncbi.nlm.nih.gov/nuccore/NC_003888.3"
		self.assertEqual(result, real_URL)
		self.assertEqual(find_url('/assembly', peasoup), "invalid assembly" )
		self.assertEqual(find_url('/assembly', chowder), "invalid assembly")


if __name__ == '__main__':
	unittest.main()


#test htmls
#SOUP contains a good URL 
#

#this would be how to call it without the main method		
#python -m unittest get_test.py
