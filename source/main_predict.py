import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	for filteringType in utils.filteringTypes:
		# file names
		trainTransitionsOutputFileName = "transformed/%sTrainTransitions.csv" % (filteringType)
		testTransitionsOutputFileName = "transformed/%sTestTransitions.csv" % (filteringType)
		emissionsOutputFileName = "transformed/%sEmissions.csv" % (filteringType)
		goldFilePath = "transformed/%sGoldStandard.json" % (filteringType)
		outputFile = "%sPredict.result" % (filteringType)

		# convert to dictionaries
		trainTransitionDictionary = utils.createMarkovDictFromCsv(trainTransitionsOutputFileName)
		testTransitionDictionary = utils.createMarkovDictFromCsv(testTransitionsOutputFileName)
		emissionDictionary = utils.createMarkovDictFromCsv(emissionsOutputFileName)
		goldFileDict = utils.createGoldStandardDict(goldFilePath)

		fileStream = open(outputFile,"w")

		print "comparing predictions from train against %s" % (goldFilePath)
		
		for output in predictCpt.goldFileCheck(goldFileDict, trainTransitionDictionary, emissionDictionary):
			fileStream.write(output + "\n")

		fileStream.close()
	
if __name__ == '__main__':
        main()