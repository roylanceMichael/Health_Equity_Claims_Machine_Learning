import zipfile
import mysql.connector
import csv as csv
import os.path
import json
import re
import time

configFile = "config.json"
startState = "START_STATE"
endState = "END_STATE"
rxCode = "Rx"

noFiltering = "noFiltering"
ageOnly = "ageOnly"
genderOnly = "genderOnly"
ageGender = "ageGender"
ageLocation = "ageLocation"

recordInsertStatement = ("insert into healthequity.claimdetaildependent (MemberId, DependentId, CptCode, CcsCode, PatientAmount, TotalAmount, Year, Gender) "
				"values (%s, %s, %s, %s, %s, %s, %s, %s)")

selectClaimDetailDependent = """
	select
		MemberId,
		DependentId, 
		CptCode,
		CcsCode,
		PatientAmount,
		TotalAmount,
		Year,
		Gender
	from ClaimDetailDependent
	order by MemberId asc, DependentId asc
"""

currentYear = int(time.strftime("%Y"))

filteringTypes = [noFiltering, ageOnly, genderOnly, ageGender, ageLocation]

def buildTransition(filterOption, gender, birthYear, zip, state):
	if filterOption == noFiltering:
		return ""
	elif filterOption == ageLocation:
		return mapBirthYearGroups(birthYear) + "_" + state
	elif filterOption == ageOnly:
		return mapBirthYearGroups(birthYear) + "_"
	elif filterOption == genderOnly:
		return gender + "_"
	else:
		return gender + "_" + mapBirthYearGroups(birthYear) + "_"

def mapBirthYearGroups(birthYear):
	# two groups
	# A (before x) and B (after x)
	try:
		castedBirthYear = int(birthYear)

		age = currentYear - castedBirthYear

		if age < 30:
			return "Under30"

		if age < 60:
			return "Under60"

		return "Over60"
	except:
		return "UnknownAge"

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

def saveClaimDetailDependent():
	cnx = mysql.connector.connect(
								user='admin', 
								password='onetwotree',
								host='192.168.1.5',
								database='healthequity')

	cursor = cnx.cursor(buffered=True)

	cursor.execute(selectClaimDetailDependent)

	open_file_object = csv.writer(open("ClaimDetailDependent.csv", "wb"))

	for row in cursor:
		open_file_object.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

	cnx.close()

def loadClaimData(claimFileName, cptToCssDict):
	# load in the csv file
	csv_file_object = csv.reader(open(claimFileName, 'rb'))

	cnx = mysql.connector.connect(
								user='admin', 
								password='onetwotree',
								host='192.168.1.5',
								database='healthequity')

	cursor = cnx.cursor(buffered=True)

	# don't set autocommit, it'll make us go a lot slower
	cursor.execute('SET autocommit = 0')
	cnx.commit()
	
	curIter = 0
	maxIter = 10000

	values = []

	for row in csv_file_object:
		memberId = re.sub("[^0-9]", "", str.strip(row[0])) 
		dependentId = re.sub("[^0-9]", "", str.strip(row[1])) 
		cptCode = str.strip(row[2])
		ccsCode = cptCode

		if cptToCssDict.has_key(cptCode):
			ccsCode = cptToCssDict[cptCode]

		patientAmount = float(str.strip(row[3]))
		totalAmount = float(str.strip(row[4]))
		gender = str.strip(row[7])

		year = str.strip(row[6])
		try:
			year = int(year)
		except:
			# skipping records that don't have birth year, will throw off data
			continue

		insertTuple = (memberId, dependentId, cptCode, ccsCode, patientAmount, totalAmount, year, gender)
		# print insertTuple
		values.append(insertTuple)
		curIter = curIter + 1

		if curIter > maxIter:
			cursor.executemany(recordInsertStatement, values)
			print 'committed ' + str(curIter)
			cnx.commit()
			curIter = 0
			del values[:]

	cursor.executemany(recordInsertStatement, values)
	del values[:]
	cnx.commit()
	cnx.close()