import csv as csv
import re
import os

alphaNumericRegex = "^([A-Za-z]*)([0-9]+)([A-Za-z]*)$"
cptToCssFileName = "data/CptToCss.csv"
cptToCssDictFileName = "transformed/CptToCssDict.csv"

def createCptToCcsDictionary():
	if not os.path.isfile(cptToCssDictFileName):
		csv_file_object = csv.reader(open(cptToCssFileName, 'rb'))
		cptToCcsDict = {}

		for row in csv_file_object:
			ranges = row[0]
			ccsValue = row[1]

			ranges = ranges.replace("'", "")
			splitRanges = ranges.split("-")

			if len(splitRanges) > 1:
				
				currentVal = splitRanges[0]
				maxValue = splitRanges[1]

				cptToCcsDict[currentVal] = ccsValue

				while not isMax(currentVal, maxValue):
					cptToCcsDict[currentVal] = ccsValue
					currentVal = incrementValue(currentVal)

				cptToCcsDict[currentVal] = ccsValue

		open_file_object = csv.writer(open(cptToCssDictFileName, "wb"))

		for key in cptToCcsDict:
			open_file_object.writerow([key, cptToCcsDict[key]])

		return cptToCcsDict
	else:
		csv_file_object = csv.reader(open(cptToCssDictFileName, 'rb'))

		cptToCcsDict = {}

		for row in csv_file_object:
			cptToCcsDict[row[0]] = row[1]

		return cptToCcsDict

def isMax(currentVal, maxValue):
	currentMatch = re.match(alphaNumericRegex, currentVal)
	maxMatch = re.match(alphaNumericRegex, maxValue)

	if currentMatch == None or maxMatch == None or len(currentMatch.groups()) < 3 or len(maxMatch.groups()) < 3:
		return True

	currentNumber = int(currentMatch.groups()[1])
	maxNumber = int(maxMatch.groups()[1])

	return currentNumber >= maxNumber

def incrementValue(currentVal):
	# all strings have 0-many alpha characters, numeric characters, then 0-many alpha characters
	match = re.match(alphaNumericRegex, currentVal)
	
	if match == None or len(match.groups()) < 3:
		return currentVal

	groups = match.groups()

	prefix = groups[0]
	number = int(groups[1]) + 1
	postfix = groups[2]

	return prefix + str(number) + postfix