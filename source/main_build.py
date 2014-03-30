import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# sys variables
	transformedDir = "transformed"
	claimsDetailsOrderedMemberIDDateZipFile = "transformed/ClaimDetailDependent.zip"
	claimsDetailsOrderedMemberIDDateFile = "transformed/ClaimDetailDependent.csv"
	trainTransitionsOutputFileName = "transformed/trainTransitions.csv"
	testTransitionsOutputFileName = "transformed/testTransitions.csv"
	emissionsOutputFileName = "transformed/emissions.csv"
	goldStandardFileName = "transformed/goldStandard.json"
	transitionColumnNames = ["From_CPT", "To_CPT", "Probability"]
	emissionColumnNames = ["CPT", "Total_Amount", "Probability"]

	# extract data, if it doesn't exist
	print "extracting claims data - if it doesn't exist already"
	utils.extractFileIfNotExists(claimsDetailsOrderedMemberIDDateZipFile, claimsDetailsOrderedMemberIDDateFile, transformedDir)

	# get the build
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile)

	# get the hmm dictionaries
	print "building the models and gold standard test file"
	dictionaryTuples = builder.build()

	# save to file
	print "saving the models and gold standard test file to transformed/"
	utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionColumnNames, emissionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionColumnNames, trainTransitionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[2], transitionColumnNames, testTransitionsOutputFileName)
	utils.createGoldStandardFile(dictionaryTuples[3], goldStandardFileName)

if __name__ == '__main__':
        main()