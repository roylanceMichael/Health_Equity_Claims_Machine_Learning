import sys
import utils
import orderedClaimsHmmBuilder
import predictCpt

def main():
	# file names - hard coded for now
	cptStart = sys.argv[1]
	transitionsOutputFileName = "data/transitions.csv"
	emissionsOutputFileName = "data/emissions.csv"

	# convert to dictionaries
	transitionDictionary = utils.createMarkovDictFromCsv(transitionsOutputFileName)
	emissionDictionary = utils.createMarkovDictFromCsv(emissionsOutputFileName)

	# find most likely path
	pathTaken = predictCpt.predictPaths(cptStart, transitionDictionary)

	print "best path:"
	for path in pathTaken:
		print path

if __name__ == '__main__':
        main()