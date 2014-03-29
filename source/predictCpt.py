def predictPaths(cptStart, transitionDictionary, maxToTake=100):
 	# find most likely path
	taken = 0
	pathTaken = []
	currentPath = cptStart

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