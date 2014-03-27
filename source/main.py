import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# sys variables
	claimsDetailsOrderedMemberIDDateFile = sys.argv[1]
	transitionsOutputFileName = "data/transitions.csv"
	emissionsOutputFileName = "data/emissions.csv"

	# get the build
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile)

	# get the hmm dictionaries
	dictionaryTuples = builder.build()

	# save to file
	utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionsOutputFileName)
	utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionsOutputFileName)

if __name__ == '__main__':
        main()