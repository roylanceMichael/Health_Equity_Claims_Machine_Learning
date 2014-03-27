import unittest
import orderedClaimsHmmBuilder

class OrderedClaimsHmmBuilder(unittest.TestCase):
	def test_buildProducesOutput(self):
		# arrange
		claimDetailsFile = '../data/ClaimDetailsOrderByMemberIDDate.csv'
		builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimDetailsFile)

		# act
		resultTuple = builder.build()

		# assert
		self.assertTrue(resultTuple != None)
		self.assertTrue(len(resultTuple) == 2)
		self.assertTrue(len(resultTuple[0]) > 0)
		self.assertTrue(len(resultTuple[1]) > 0)

def main():
    unittest.main()

if __name__ == '__main__':
        main()