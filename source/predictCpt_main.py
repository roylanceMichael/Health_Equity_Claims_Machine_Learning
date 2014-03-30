import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	# file names - hard coded for now
	trainTransitionsOutputFileName = "data/trainTransitions.csv"
	testTransitionsOutputFileName = "data/testTransitions.csv"
	emissionsOutputFileName = "data/emissions.csv"
	goldFilePath = "data/goldStandard.json"

	# convert to dictionaries
	trainTransitionDictionary = utils.createMarkovDictFromCsv(trainTransitionsOutputFileName)
	testTransitionDictionary = utils.createMarkovDictFromCsv(testTransitionsOutputFileName)
	emissionDictionary = utils.createMarkovDictFromCsv(emissionsOutputFileName)
	goldFileDict = utils.createGoldStandardDict(goldFilePath)

	# determine if transitions match up
	for stdout in predictCpt.goldFileCheck(goldFileDict, trainTransitionDictionary, emissionDictionary):
		print stdout
	
if __name__ == '__main__':
        main()