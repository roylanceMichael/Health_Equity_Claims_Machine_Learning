import unittest
import cptToCcs
import orderedClaimsHmmBuilder

class CptToCss(unittest.TestCase):
	def test_correctIncrement(self):
		# arrange
		# act
		result = cptToCcs.incrementValue("H1124")

		# assert
		self.assertTrue(result, "H1125")

	def test_correctIncrement1(self):
		# arrange
		# act
		result = cptToCcs.incrementValue("1124")

		# assert
		self.assertTrue(result, "1125")

	def test_correctIncrement2(self):
		# arrange
		# act
		result = cptToCcs.incrementValue("1124H")

		# assert
		self.assertTrue(result, "1125H")

	def test_correctIncrement3(self):
		# arrange
		# act
		result = cptToCcs.incrementValue("R1124H")

		# assert
		self.assertTrue(result, "R1125H")

def main():
    unittest.main()

if __name__ == '__main__':
        main()