import csv as csv
import re
import os
import random
import utils

class OrderedClaimsHmmBuilder:
	def __init__(self, fileName, cptDict, useCpt=False, setSplit=0.98):
		self.fileName = fileName
		self.cptDict = cptDict
		self.setSplit = setSplit
		self.useCpt = useCpt

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

	def createRxState(self, previousState, currentState):
		# are we Rx?
		isPreviousStateRx = previousState.find(utils.rxCode) != -1
		isCurrentStateRx = currentState == utils.rxCode
		
		if isCurrentStateRx:
			if isPreviousStateRx:
				return previousState
			return previousState + currentState
		return currentState

	def createCurrentState(self, previousState, currentState, row, buildType):
		rxState = self.createRxState(previousState, currentState)

		if rxState != currentState:
			return rxState

		return utils.buildTransition(buildType, row[7], row[6], '', '') + currentState

	

	def build(self, buildType):
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
			rawCode = row[3]

			currentCptCode = self.createCurrentState(previousCptCode, rawCode, row, buildType)
			unfilteredCptCode = self.createRxState(previousCptCode, rawCode)

			patientAmount = float(row[4])
			totalAmount = str(patientAmount)

			if rowMemberId != currentMemberId or dependentId != currentDependentId:
				# set final state
				self.setDict(transitions, previousCptCode, utils.endState)
				self.setDict(emissions, previousCptCode + "_" + utils.endState, totalAmount)
				
				(transitions, isTest) = self.determineDictionary(testTransitions, trainTransitions)

				# set start state
				startState = utils.startState
				self.setDict(transitions, startState, currentCptCode)
				self.setDict(emissions, startState + "_" + currentCptCode, totalAmount)

				if isTest:
					goldStandard[rowMemberId + dependentId] = [(startState, 0)]
					goldStandard[rowMemberId + dependentId].append((unfilteredCptCode, totalAmount, row[6], row[7], '', ''))
				
				currentMemberId = rowMemberId
				currentDependentId = dependentId
				previousCptCode = currentCptCode
				continue

			self.setDict(transitions, previousCptCode, currentCptCode)
			self.setDict(emissions, previousCptCode + "_" + currentCptCode, totalAmount)
			
			if isTest:
				goldStandard[rowMemberId + dependentId].append((unfilteredCptCode, totalAmount, row[6], row[7], '', ''))

			previousCptCode = currentCptCode

		# create probabilities out of these now
		emissionsProb = self.buildDict(emissions)
		trainTransitionsProb = self.buildDict(trainTransitions)
		testTransitionsProb = self.buildDict(testTransitions)

		return (emissionsProb, trainTransitionsProb, testTransitionsProb, goldStandard)