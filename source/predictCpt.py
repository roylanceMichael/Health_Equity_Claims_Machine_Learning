import utils

def goldFileCheck(goldFileDict, transitionDictionary, emissionDictionary, maxToTake=100):
	totalErrors = 0
	total = 0
	for key in goldFileDict:
		previous = ""
		current = ""

		goldAmount = 0
		path = previous
		trainAmount = 0
		trainHighest = 0
		trainLowest = 0
		total = total + 1
		foundError = False

		for tup in goldFileDict[key]:
			# handle start state
			if previous == "":
				previous = tup[0]
				path = path + " " + previous
				continue

			current = tup[0]
			path = path + " " + current
			amount = float(tup[1])

			if (transitionDictionary.has_key(previous) and 
				transitionDictionary[previous].has_key(current)):

				emissionKey = previous + "_" + current

				if emissionDictionary.has_key(emissionKey):
					goldAmount = goldAmount + amount
					trainAmount = trainAmount + float(getHighestProb(emissionDictionary, emissionKey))
					trainHighest = trainHighest + getHighestAmount(emissionDictionary, emissionKey)
					trainLowest = trainLowest + getLowestAmount(emissionDictionary, emissionKey)
					previous = current
					continue

			totalErrors = totalErrors + 1
			foundError = True
			yield "could not find a transition from %s to %s" % (previous, current)
			yield "\n"
			break

		# don't report if there was an error...
		if foundError == True:
			continue

		yield "path: " + path
		yield "gold: " + str(goldAmount)
		yield "trainMostFrequent: " + str(trainAmount)
		yield "trainLowest: " + str(trainLowest)
		yield "trainHighest: " + str(trainHighest)
		yield "\n"

	yield "total errors: " + str(totalErrors) + "/" + str(total)
	yield "\n"

def getHighestProb(markovDict, key):
	highestSubkey = ""
	highestProb = -1

	for subkey in markovDict[key]:
		if markovDict[key][subkey] > highestProb:
			highestSubkey = subkey
			highestProb = markovDict[key][subkey]

	return highestSubkey

def getLowestAmount(markovDict, key):
	lowestSubkey = 9999

	for subkey in markovDict[key]:
		castedSubkey = float(subkey)
		if lowestSubkey > castedSubkey:
			lowestSubkey = castedSubkey

	return lowestSubkey

def getHighestAmount(markovDict, key):
	highestSubkey = -9999

	for subkey in markovDict[key]:
		castedSubkey = float(subkey)
		if highestSubkey < castedSubkey:
			highestSubkey = castedSubkey

	return highestSubkey