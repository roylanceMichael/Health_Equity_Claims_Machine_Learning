import sys
import csv
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	trainTransitions = {}
	emissions = {}
	goldFiles = {}

	outputFile = "results/predict.csv"
	outputFileGranular = "results/granular.csv"
	outputFileTrans = "results/trans.csv"

	filteringType = utils.ageGender

	# for filteringType in utils.filteringTypes:
	print "reading train, emission, and gold path from %s" % (filteringType)
	# file names
	trainTransitionsOutputFileName = "buildResults/%sTrainTransitions.csv" % (filteringType)
	testTransitionsOutputFileName = "buildResults/%sTestTransitions.csv" % (filteringType)
	emissionsOutputFileName = "buildResults/%sEmissions.csv" % (filteringType)
	goldFilePath = "buildResults/%sGoldStandard.json" % (filteringType)
	
	# convert to dictionaries
	trainTransitions[filteringType] = utils.createMarkovDictFromCsv(trainTransitionsOutputFileName)
	emissions[filteringType] = utils.createMarkovDictFromCsv(emissionsOutputFileName)
	goldFiles[filteringType] = utils.createGoldStandardDict(goldFilePath)

	fileStream = csv.writer(open(outputFile, "wb"))
	fileStream.writerow(["Path", "GoldAmount", "ExpectedAmount", "TrainAmount", "TrainLowest", "TrainHighest"])

	granularFileStream = csv.writer(open(outputFileGranular, "wb"))
	granularFileStream.writerow(["Previous", "Current", "HighestNext", "GoldAmount", "ExpectedAmount", "HighestProbAmount", "HighestAmount", "LowestAmount", "IsSame"])

	transFileStream = csv.writer(open(outputFileTrans, "wb"))
	transFileStream.writerow(["Previous", "Current", "HighestNext", "CurrentProb", "HighestProb", "IsSame"])

	goldFileDict = goldFiles[filteringType]
	
	for key in goldFileDict:
		print "processing key %s" % (key)
		for output in predictCpt.goldFileCheck(goldFileDict[key], trainTransitions[filteringType], emissions[filteringType], filteringType):
			fileStream.writerow(output)

		for output in predictCpt.predictNextState(goldFileDict[key], trainTransitions[filteringType], emissions[filteringType], filteringType):
			granularFileStream.writerow(output)

		for output in predictCpt.predictTrans(goldFileDict[key], trainTransitions[filteringType], emissions[filteringType], filteringType):
			transFileStream.writerow(output)
	
if __name__ == '__main__':
        main()