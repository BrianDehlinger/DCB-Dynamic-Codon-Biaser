import unittest


#test for empty href
#test for no assembly
class TestCalc(unitttest.Testcase):

	def test_find_url(self):
		result = find_url(self)
		self.assertEqual( result, real_URL)
		
if __name__ == '__main__':
	unittest.main()
#test htmls 
		
# python -m unittest get_test.py