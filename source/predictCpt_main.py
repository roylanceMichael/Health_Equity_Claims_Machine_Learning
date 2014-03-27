import sys
import utils
import orderedClaimsHmmBuilder

def main():
	# file names - hard coded for now
	cptStart = sys.argv[1]
	transitionsOutputFileName = "data/transitions.csv"
	emissionsOutputFileName = "data/emissions.csv"

	# convert to dictionaries
	transitionDictionary = utils.createMarkovDictFromCsv(transitionsOutputFileName)
	emissionDictionary = utils.createMarkovDictFromCsv(emissionsOutputFileName)

	# find most likely path
	mostTaken = 10
	taken = 0
	pathTaken = []
	currentPath = cptStart

	while currentPath != None and taken < mostTaken:
		if transitionDictionary.has_key(currentPath):
			pathTaken.append(currentPath)

			bestPath = ""
			bestProb = -1

			for subkey in transitionDictionary[currentPath]:
				if bestProb < transitionDictionary[currentPath][subkey]:
					bestProb = transitionDictionary[currentPath][subkey]
					bestPath = subkey

			currentPath = bestPath
		else:
			currentPath = None

		taken = taken + 1

	print "best path:"
	for path in pathTaken:
		print path

if __name__ == '__main__':
        main()