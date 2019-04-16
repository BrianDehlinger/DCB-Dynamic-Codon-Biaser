import unittest 

# python -m unittest get_test.py
class Test(unittest.Testcase):
	
	def test_get_bias(self):
        test1 = [0,0,0]
		self.assertequal(test1, get_bias(fasta))
        test2 = [1,1,1]
        self.assertequal(test2, get_bias(fasta))
	
	def test_clean_hegs(self):
		result = "40"
		self.assertequal(result, clean_hegs(f))
	
#makes the running test easier
if __name__ == '__main__':
	unittest.main()
