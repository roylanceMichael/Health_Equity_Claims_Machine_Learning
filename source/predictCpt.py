import utils

def predictPaths(cpts, transitionDictionary, maxToTake=100):
 	# find most likely path
	taken = 0
	pathTaken = []
	modifiedCpts = utils.startState + cpts

	for i in range(1, len(modifiedCpts)):
		previousCpt = modifiedCpts[i-1]
		currentCpt = modifiedCpts[i]

		if (transitionDictionary.has_key(previousCpt) and 
			transitionDictionary[previousCpt].has_key(currentCpt)):
			


	currentPath = cpts

	while currentPath != None and taken < maxToTake:
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

	return pathTaken

