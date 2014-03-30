import utils

def goldFileCheck(goldFileDict, transitionDictionary, emissionDictionary, maxToTake=100):
	totalErrors = 0
	total = 0
	for key in goldFileDict:
		previous = utils.startState
		current = ""

		goldAmount = 0
		path = previous
		trainAmount = 0
		total = total + 1

		for tup in goldFileDict[key]:
			current = tup[0]
			path = path + " " + current
			amount = float(tup[1])

			if (transitionDictionary.has_key(previous) and 
				transitionDictionary[previous].has_key(current)):

				emissionKey = previous + "_" + current

				if emissionDictionary.has_key(emissionKey):
					goldAmount = goldAmount + amount
					trainAmount = trainAmount + float(getHighestProb(emissionDictionary, emissionKey))

					previous = current
					continue

			totalErrors = totalErrors + 1
			yield "could not find a transition from %s to %s" % (previous, current)
			yield ""
			break

		yield "path: " + path
		yield "gold: " + str(goldAmount)
		yield "train: " + str(trainAmount)
		yield ""

	yield "total errors: " + str(totalErrors) + "/" + str(total)

def getHighestProb(markovDict, key):
	highestSubkey = ""
	highestProb = -1

	for subkey in markovDict[key]:
		if markovDict[key][subkey] > highestProb:
			highestSubkey = subkey
			highestProb = markovDict[key][subkey]

	return highestSubkey