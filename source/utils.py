import zipfile
import csv as csv
import os.path
import json

configFile = "config.json"
startState = "START_STATE"
endState = "END_STATE"
rxCode = "Rx"

def readConfigFile():
	with open(configFile) as configFileStream:
		return json.load(configFileStream)

def extractFileIfNotExists(zipFileName, fileName, zipDir):
	if not os.path.isfile(fileName) and os.path.isfile(zipFileName):
		zfile = zipfile.ZipFile(zipFileName)

		for name in zfile.namelist():
			zfile.extract(name, zipDir)

def createCsvFromMarkovDict(markovDict, columnNames, fileName):
	open_file_object = csv.writer(open(fileName, "wb"))

	open_file_object.writerow(columnNames)

	for key in markovDict:
		for subkey in markovDict[key]:
			open_file_object.writerow([key, subkey, markovDict[key][subkey]])

def createGoldStandardFile(goldStandardDict, fileName):
	with open(fileName, 'w') as outfile:
	  json.dump(goldStandardDict, outfile, indent=4)

def createGoldStandardDict(fileName):
	with open(fileName) as inFile:
		return json.load(inFile)

def createMarkovDictFromCsv(fileName):
	csv_file_object = csv.reader(open(fileName, 'rb'))
	header = csv_file_object.next()

	markovDict = {}

	for row in csv_file_object:
		key = row[0]
		subkey = row[1]
		probability = float(row[2])

		if markovDict.has_key(key):
			markovDict[key][subkey] = probability
		else:
			markovDict[key] = { subkey: probability }

	return markovDict