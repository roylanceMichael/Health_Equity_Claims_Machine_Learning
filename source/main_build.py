import sys
import utils
import orderedClaimsHmmBuilder
import cptToCcs

def main():
	# sys variables
	transformedDir = "transformed"
	claimsDetailsOrderedMemberIDDateZipFile = "transformed/ClaimDetailDependent.zip"
	claimsDetailsOrderedMemberIDDateFile = "transformed/ClaimDetailDependent.csv"
	trainTransitionsOutputFileName = "buildResults/%strainTransitions.csv"
	testTransitionsOutputFileName = "buildResults/%stestTransitions.csv"
	emissionsOutputFileName = "buildResults/%sEmissions.csv"
	goldStandardFileName = "buildResults/%sGoldStandard.json"
	transitionColumnNames = ["From_CPT", "To_CPT", "Probability"]
	emissionColumnNames = ["CPT", "Total_Amount", "Probability"]

	# extract data, if it doesn't exist
	print "extracting claims data - if it doesn't exist already"
	utils.extractFileIfNotExists(claimsDetailsOrderedMemberIDDateZipFile, claimsDetailsOrderedMemberIDDateFile, transformedDir)

	# ensure cptToCss file exists
	print "buildint cptToCss dictionary - if needed"
	cptDict = cptToCcs.createCptToCcsDictionary()

	# get the build
	# utils.loadClaimData(claimsDetailsOrderedMemberIDDateFile, cptDict)
	utils.saveClaimDetailDependent()

	return
	builder = orderedClaimsHmmBuilder.OrderedClaimsHmmBuilder(claimsDetailsOrderedMemberIDDateFile, cptDict)

	# get the hmm dictionaries
	# for filteringType in utils.filteringTypes:
	filteringType = utils.ageGender

	print "building the models and gold standard test file with %s" % (filteringType)
	dictionaryTuples = builder.build(filteringType)

	# save to file
	print "saving the models and gold standard test file to buildResults/"
	utils.createCsvFromMarkovDict(dictionaryTuples[0], emissionColumnNames, (emissionsOutputFileName % (filteringType)))
	utils.createCsvFromMarkovDict(dictionaryTuples[1], transitionColumnNames, (trainTransitionsOutputFileName % (filteringType)))
	utils.createGoldStandardFile(dictionaryTuples[3], (goldStandardFileName % (filteringType)))

if __name__ == '__main__':
        main()