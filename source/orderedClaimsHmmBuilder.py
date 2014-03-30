import csv as csv
import re
import os
import random
import utils

class OrderedClaimsHmmBuilder:
	def __init__(self, fileName, setSplit=0.98):
		self.fileName = fileName
		self.setSplit = setSplit

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

	def determineDictionary(self, test, train):
		if random.random() > self.setSplit:
			return (test, True)
		return (train, False)

	def createCurrentState(self, previousState, currentState):
		# are we Rx?
		isPreviousStateRx = previousState.find(utils.rxCode) != -1
		isCurrentStateRx = currentState == utils.rxCode
		
		if isCurrentStateRx:
			if isPreviousStateRx:
				return previousState
			return previousState + currentState
		return currentState

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
		testTransitions = {}
		trainTransitions = {}

		# gold standard for testing
		goldStandard = {}

		# initial one will be thrown away
		transitions = {}

		isTest = False

		previousCptCode = utils.startState
		for row in csv_file_object:
			rowMemberId = row[0]
			dependentId = row[1]
			currentCptCode = self.createCurrentState(previousCptCode, row[2])

			patientAmount = float(row[3])
			totalAmount = str(patientAmount)

			self.setDict(emissions, currentCptCode, totalAmount)

			if rowMemberId != currentMemberId or dependentId != currentDependentId:
				# set final state
				self.setDict(transitions, previousCptCode, utils.endState)
				
				(transitions, isTest) = self.determineDictionary(testTransitions, trainTransitions)

				# set start state
				self.setDict(transitions, utils.startState, currentCptCode)

				if isTest:
					goldStandard[rowMemberId + dependentId] = [(currentCptCode, totalAmount)]
				
				currentMemberId = rowMemberId
				currentDependentId = dependentId
				previousCptCode = currentCptCode
				continue

			self.setDict(transitions, previousCptCode, currentCptCode)

			if isTest:
				goldStandard[rowMemberId + dependentId].append((currentCptCode, totalAmount))

			previousCptCode = currentCptCode

		# create probabilities out of these now
		emissionsProb = self.buildDict(emissions)
		trainTransitionsProb = self.buildDict(trainTransitions)
		testTransitionsProb = self.buildDict(testTransitions)

		return (emissionsProb, trainTransitionsProb, testTransitionsProb, goldStandard)