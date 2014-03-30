import utils

def goldFileCheck(goldFileDict, transitionDictionary, emissionDictionary, maxToTake=100):
	
	for key in goldFileDict:
		previous = utils.startState
		current = ""

		goldAmount = 0
		path = previous
		trainAmount = 0
		for tup in goldFileDict[key]:
			current = tup[0]
			path = path + " " + current
			amount = float(tup[1])

			if (transitionDictionary.has_key(previous) and 
				transitionDictionary[previous].has_key(current)):

				if emissionDictionary.has_key(current):
					goldAmount = goldAmount + amount
					trainAmount = trainAmount + float(getHighestProb(emissionDictionary, current))

					previous = current
					continue

			yield 'could not find a transition from %s to %s' % (previous, current)
			break

		yield "path: " + path
		yield "gold: " + str(goldAmount)
		yield "train: " + str(trainAmount)
		yield ""

def getHighestProb(markovDict, key):
	highestSubkey = ""
	highestProb = -1

	for subkey in markovDict[key]:
		if markovDict[key][subkey] > highestProb:
			highestSubkey = subkey
			highestProb = markovDict[key][subkey]

	return highestSubkey