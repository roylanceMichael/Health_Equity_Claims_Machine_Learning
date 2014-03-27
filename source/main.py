import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# sys variables
	claimsDetailsOrderedMemberIDDateFile = sys.argv[1]
	transitionsOutputFileName = "data/transitions.csv"
	emissionsOutputFileName = "data/emissions.csv"
	transitionColumnNames = ["From_CPT", "To_CPT", "Probability"]
	emissionColumnNames = ["CPT", "Total_Amount", "Probability"]

	# get the build
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile, True)

	# get the hmm dictionaries
	dictionaryTuples = builder.build()

	# save to file
	utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionColumnNames, emissionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionColumnNames, transitionsOutputFileName)

if __name__ == '__main__':
        main()