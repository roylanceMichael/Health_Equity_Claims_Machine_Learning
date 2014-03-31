import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# sys variables
	transformedDir = "transformed"
	claimsDetailsOrderedMemberIDDateZipFile = "transformed/ClaimDetailDependent.zip"
	claimsDetailsOrderedMemberIDDateFile = "transformed/ClaimDetailDependent.csv"
	trainTransitionsOutputFileName = "transformed/%strainTransitions.csv"
	testTransitionsOutputFileName = "transformed/%stestTransitions.csv"
	emissionsOutputFileName = "transformed/%sEmissions.csv"
	goldStandardFileName = "transformed/%sGoldStandard.json"
	transitionColumnNames = ["From_CPT", "To_CPT", "Probability"]
	emissionColumnNames = ["CPT", "Total_Amount", "Probability"]

	# extract data, if it doesn't exist
	print "extracting claims data - if it doesn't exist already"
	utils.extractFileIfNotExists(claimsDetailsOrderedMemberIDDateZipFile, claimsDetailsOrderedMemberIDDateFile, transformedDir)

	# get the build
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile)

	# get the hmm dictionaries
	for filteringType in utils.filteringTypes:
		print "building the models and gold standard test file with %s" % (filteringType)
		dictionaryTuples = builder.build(filteringType)

		# save to file
		print "saving the models and gold standard test file to transformed/"
		utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionColumnNames, (emissionsOutputFileName % (filteringType)))
		utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionColumnNames, (trainTransitionsOutputFileName % (filteringType)))
		utils.createCsvFromMarkovDict(dictionaryTuples[2], transitionColumnNames, (testTransitionsOutputFileName % (filteringType)))
		utils.createGoldStandardFile(dictionaryTuples[3], (goldStandardFileName % (filteringType)))

if __name__ == '__main__':
        main()