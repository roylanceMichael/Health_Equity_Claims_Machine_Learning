import numpy as np
import csv as csv
import re
import os

class OrderedClaimsHmmBuilder:
	def __init__(self, fileName):
		self.fileName = fileName

	def setDict(self, tempDict, key, subkey):
		if tempDict.has_key(key):
			if tempDict[key].has_key(subkey):
				tempDict[key][subkey] = tempDict[key][subkey] + 1
			else:
				tempDict[key][subkey] = 1
		else:
			tempDict[key] = { subkey: 1 }

	def build(self):
		csv_file_object = csv.reader(open(self.fileName, 'rb'))
		header = csv_file_object.next()

		# read all of a member's claims in at once
		# NewMemberID, CPTCode
		currentMemberId = 0

		# CPT -> cost
		emissions = {}

		# CPT -> CPT
		transitions = {}

		previousCptCode = ''
		for row in csv_file_object:
			rowMemberId = int(row[0])
			rowCptCode = row[1]

			patientAmount = float(row[2])
			repricedAmount = float(row[3])

			totalAmount = str(patientAmount + repricedAmount)

			# set current cpt code to one in row if a new group
			if previousCptCode == '' or rowMemberId != currentMemberId:
				currentMemberId = rowMemberId
				previousCptCode = rowCptCode
				continue

			self.setDict(emissions, rowCptCode, totalAmount)
			self.setDict(transitions, previousCptCode, rowCptCode)

			previousCptCode = rowCptCode

		# TODO: create probabilities out of these now
		emissionsProb = {}
		transitionsProb = {}

		

		return (emissions, transitions)