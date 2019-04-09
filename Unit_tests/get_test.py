import unittest


#test for empty href
#test for no assembly
class TestCalc(unitttest.Testcase):

	def test_find_url(self):
		result = find_url('/assembly', lemonrice)
		real_URL = ""
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