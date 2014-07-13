import utils
import operator
import math

def predictTrans(goldFileList, transitionDictionary, emissionDictionary, filterOption):
	previous = ""

	for tup in goldFileList:
		if previous == "":
			previous = tup[0]
			continue

		current = tup[0]
		
		# get most frequent from previous
		if transitionDictionary.has_key(previous) and transitionDictionary[previous].has_key(current):
			highestProbNext = getHighestProb(transitionDictionary, previous, 1)[0][0]
			yield [previous, current, highestProbNext, transitionDictionary[previous][current], transitionDictionary[previous][highestProbNext], (current == highestProbNext)]
			previous = current
		else:
			break
			yield [previous, current, "error", "error", "error", "error"]

def predictNextState(goldFileList, transitionDictionary, emissionDictionary, filterOption):
	previous = ""

	for tup in goldFileList:
		if previous == "":
			previous = tup[0]
			continue

		current = tup[0]
		
		# get most frequent from previous
		if transitionDictionary.has_key(previous):
			highestProbNext = getHighestProb(transitionDictionary, previous, 1)[0][0]

			emissionKey = previous + "_" + highestProbNext
			if emissionDictionary.has_key(emissionKey):
				frequentAmount = getHighestProb(emissionDictionary, emissionKey, 1)[0][0]
				randomAmount = getRandomAmount(emissionDictionary, emissionKey)
				highestAmount = getHighestAmount(emissionDictionary, emissionKey)
				lowestAmount = getLowestAmount(emissionDictionary, emissionKey)
				yield [previous, current, highestProbNext, float(tup[1]), randomAmount, frequentAmount, highestAmount, lowestAmount, (current == highestProbNext)]
			else:
				yield [previous, current, highestProbNext, float(tup[1]), 0, 0, 0, 0, (current == highestProbNext)]
			
			previous = current
		else:
			yield ["error " + previous, current, "error", "error", "error", "error", "error", "error", "error"]

def goldFileCheck(goldFileList, transitionDictionary, emissionDictionary, filterOption, maxToTake=100):
	totalErrors = 0
	total = 0
	previous = ""
	current = ""

	goldAmount = 0
	path = previous
	trainAmount = 0
	trainHighest = 0
	trainLowest = 0
	randomAmount = 0
	total = total + 1
	foundError = False

	for tup in goldFileList:
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
				trainAmount = trainAmount + float(getHighestProb(emissionDictionary, emissionKey, 1)[0][0])
				trainHighest = trainHighest + getHighestAmount(emissionDictionary, emissionKey)
				trainLowest = trainLowest + getLowestAmount(emissionDictionary, emissionKey)
				randomAmount = randomAmount + getRandomAmount(emissionDictionary, emissionKey)
				previous = current
				continue

		totalErrors = totalErrors + 1
		foundError = True
		# yield ["%s %s" % (previous, current), "Error", "Error", "Error", "Error", "Error"]
		break

	# don't report if there was an error...
	if foundError == True:
		return

	if len(path) > 7500:
		yield [path[0:7500], goldAmount, randomAmount, trainAmount, trainLowest, trainHighest]
	else:
		yield [path, goldAmount, randomAmount, trainAmount, trainLowest, trainHighest]

def getHighestProb(markovDict, key, n):
	sorted_n = sorted(markovDict[key].iteritems(), key=operator.itemgetter(1))
	sorted_n.reverse()
	return sorted_n[:n]

def getRandomAmount(markovDict, key):
	totalAmount = 0

	for subkey in markovDict[key]:
		castedSubkey = float(subkey)
		prob = markovDict[key][subkey]
		totalAmount = totalAmount + (castedSubkey * prob)

	return totalAmount

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