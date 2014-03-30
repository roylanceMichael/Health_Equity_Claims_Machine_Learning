import csv as csv
import re
import os

class OrderedClaimsHmmBuilder:
	def __init__(self, fileName, ignoreRx=False):
		self.fileName = fileName
		self.rxCode = "Rx"
		self.startState = "START_STATE"
		self.endState = "END_STATE"
		self.ignoreRx = ignoreRx

	def setDict(self, tempDict, key, subkey):
		if tempDict.has_key(key):
			if tempDict[key].has_key(subkey):
				tempDict[key][subkey] = tempDict[key][subkey] + 1
			else:
				tempDict[key][subkey] = 1
		else:
			tempDict[key] = { subkey: 1 }

	def buildDict(self, oldDict):
		newDict = {}
		for key in oldDict:
			total = 0

			for subkey in oldDict[key]:
				total = total + oldDict[key][subkey]

			newDict[key] = {}
			for subkey in oldDict[key]:
				newDict[key][subkey] = float(oldDict[key][subkey]) / total

		return newDict

	def build(self):
		csv_file_object = csv.reader(open(self.fileName, 'rb'))
		header = csv_file_object.next()

		# read all of a member's claims in at once
		# NewMemberID, CPTCode
		currentMemberId = ""
		currentDependentId = ""

		# CPT -> cost
		emissions = {}

		# CPT -> CPT
		transitions = {}

		previousCptCode = self.startState
		for row in csv_file_object:
			rowMemberId = row[0]
			dependentId = row[1]
			currentCptCode = row[2]

			if currentCptCode == self.rxCode:
				if self.ignoreRx:
					continue

			patientAmount = float(row[3])

			totalAmount = str(patientAmount)
			self.setDict(emissions, currentCptCode, totalAmount)

			if previousCptCode == self.startState:
				self.setDict(transitions, self.startState, currentCptCode)
				currentMemberId = rowMemberId
				currentDependentId = dependentId
				previousCptCode = currentCptCode
				continue

			if rowMemberId != currentMemberId or dependentId != currentDependentId:
				# set final state
				self.setDict(transitions, previousCptCode, self.endState)
				self.setDict(transitions, self.startState, currentCptCode)
				currentMemberId = rowMemberId
				currentDependentId = dependentId
				previousCptCode = currentCptCode
				continue

			self.setDict(transitions, previousCptCode, currentCptCode)
			previousCptCode = currentCptCode

		# create probabilities out of these now
		emissionsProb = self.buildDict(emissions)
		transitionsProb = self.buildDict(transitions)

		return (emissionsProb, transitionsProb)