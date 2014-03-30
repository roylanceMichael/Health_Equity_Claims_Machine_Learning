import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# sys variables
	claimsDetailsOrderedMemberIDDateFile = sys.argv[1]
	trainTransitionsOutputFileName = "data/trainTransitions.csv"
	testTransitionsOutputFileName = "data/testTransitions.csv"
	emissionsOutputFileName = "data/emissions.csv"
	goldStandardFileName = "data/goldStandard.json"
	transitionColumnNames = ["From_CPT", "To_CPT", "Probability"]
	emissionColumnNames = ["CPT", "Total_Amount", "Probability"]

	# get the build
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile)

	# get the hmm dictionaries
	dictionaryTuples = builder.build()

	# save to file
	utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionColumnNames, emissionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionColumnNames, trainTransitionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[2], transitionColumnNames, testTransitionsOutputFileName)
	utils.createGoldStandardFile(dictionaryTuples[3], goldStandardFileName)

if __name__ == '__main__':
        main()