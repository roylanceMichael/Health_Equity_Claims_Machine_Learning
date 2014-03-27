import csv as csv

def createCsvFromMarkovDict(markovDict, fileName):
	open_file_object = csv.writer(open(fileName, "wb"))

	for key in markovDict:
		for subkey in markovDict[key]:
			open_file_object.writerow([key, subkey, markovDict[key][subkey]])