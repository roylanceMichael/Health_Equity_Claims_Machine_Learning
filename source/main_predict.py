import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	trainTransitions = {}
	emissions = {}
	goldFiles = {}

	outputFile = "predict.result"

	for filteringType in utils.filteringTypes:
		print "reading train, emission, and gold path from %s" % (filteringType)
		# file names
		trainTransitionsOutputFileName = "transformed/%sTrainTransitions.csv" % (filteringType)
		testTransitionsOutputFileName = "transformed/%sTestTransitions.csv" % (filteringType)
		emissionsOutputFileName = "transformed/%sEmissions.csv" % (filteringType)
		goldFilePath = "transformed/%sGoldStandard.json" % (filteringType)
		

		# convert to dictionaries
		trainTransitions[filteringType] = utils.createMarkovDictFromCsv(trainTransitionsOutputFileName)
		emissions[filteringType] = utils.createMarkovDictFromCsv(emissionsOutputFileName)
		goldFiles[filteringType] = utils.createGoldStandardDict(goldFilePath)

	fileStream = open(outputFile,"w")

	goldFileDict = goldFiles[utils.noFiltering]

	for key in goldFileDict:
		for filteringType in utils.filteringTypes:
			for output in predictCpt.goldFileCheck(goldFileDict[key], trainTransitions[filteringType], emissions[filteringType], filteringType):
				fileStream.write(output + "\n")

	fileStream.close()
	
if __name__ == '__main__':
        main()