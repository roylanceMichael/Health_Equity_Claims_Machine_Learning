import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	# file names - hard coded for now
	cpts = sys.argv[1:]
	trainTransitionsOutputFileName = "data/trainTransitions.csv"
	testTransitionsOutputFileName = "data/testTransitions.csv"
	emissionsOutputFileName = "data/emissions.csv"

	# convert to dictionaries
	trainTransitionDictionary = utils.createMarkovDictFromCsv(trainTransitionsOutputFileName)
	testTransitionDictionary = utils.createMarkovDictFromCsv(testTransitionsOutputFileName)
	emissionDictionary = utils.createMarkovDictFromCsv(emissionsOutputFileName)

	# find most likely path
	pathTaken = predictCpt.predictPaths(cpts, transitionDictionary)

	print "best path:"
	for path in pathTaken:
		print path

if __name__ == '__main__':
        main()