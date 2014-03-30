import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	# file names - hard coded for now
	trainTransitionsOutputFileName = "transformed/trainTransitions.csv"
	testTransitionsOutputFileName = "transformed/testTransitions.csv"
	emissionsOutputFileName = "transformed/emissions.csv"
	goldFilePath = "transformed/goldStandard.json"

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