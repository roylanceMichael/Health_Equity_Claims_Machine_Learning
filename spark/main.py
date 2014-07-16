import os
import datetime
import time
import utils
from datetime import date
from sklearn import metrics
from pyspark import SparkContext

def main():
    currentYear = int(time.strftime("%Y"))
    currentDir = os.getcwd() + "/"
    resultsDir = "sparkBuildResults/"
    transformedDir = "transformed"
    utilModuleFile = currentDir + "spark/utils.py"
    claimsDetailsOrderedMemberIDDateZipFile = transformedDir + "/ClaimDetailDependent.csv.zip"
    claimsDetailsOrderedMemberIDDateFile = transformedDir + "/ClaimDetailDependent.csv"
    claimDataLocation = currentDir + claimsDetailsOrderedMemberIDDateFile

    transitionType = "transition"
    emissionType = "emission"
    goldType = "gold"

    # extract zip if it doesn't exist already
    utils.extractFileIfNotExists(claimsDetailsOrderedMemberIDDateZipFile, claimsDetailsOrderedMemberIDDateFile, transformedDir)

    # 0, 1, 2, 3, 4, 5, 6, 7, 11
    # memberId, dependentId, cptCode, ccsCode, patientAmount, totalAmount, Year, Gender are the fields we care about

    def buildTransitionWrapper(gender, year, state):
        return utils.buildTransition(utils.ageGender, gender, year, "", "") + state

    #map columns
    def mapTransition(row):
        columns = row.split(',')
        memberId = columns[0]
        dependentId = columns[1]
        ccsCode = columns[3]
        patientAmount = columns[4]
        year = columns[6]
        gender = columns[7]
        serviceDate = date.today()
        serviceDateList = columns[11].split(" ")
        if len(serviceDateList) == 2:
            serviceDate = datetime.datetime.strptime(serviceDateList[0], "%Y-%m-%d")

        #natural key, value
        return ((memberId, dependentId), (memberId, dependentId, ccsCode, patientAmount, year, gender, serviceDate))

    def mapSequences(rows):
        # triage into three separate lists
        # transition, emission, and gold
        goldTests = []
        for row in rows:

            personRecords = row[1]
            sorted(row[1], key=lambda x: (x[6], x[2]))
            startState = "START"
            previous = startState

            keepInModel = not utils.isTest()

            goldStandard = []
            for item in personRecords:
                # handle transition
                current = buildTransitionWrapper(item[5], item[4], item[2])
                

                # handle emission
                emissionKey = previous + "_" + current
                patientAmount = item[3]

                # keep in model? 
                #new dictionaries - yield creates each one
                if (keepInModel):
                    yield ((previous, current, transitionType), 1)
                    yield ((emissionKey, patientAmount, emissionType), 1)
                else:
                    goldStandard.append((previous, current, emissionKey, patientAmount, item[4], item[5]))

                previous = current

            # push gold standard, if it exists
            if not keepInModel:
                yield ((row[0][0], row[0][1], goldType), goldStandard)

    # should only be processing transition and emission
    def sumConditionalTotals(rows):
        for row in rows:
            total = len(row[1])
            yield (row[0][0], (row[0][1], total))

    # should only be processing transition and emission
    def createProbabilities(rows):
        for row in rows:
            total = 0

            # find the total for conditional probability
            for item in row[1]:
                total = total + item[1]

            # yield each new probability
            for item in row[1]:
                yield (row[0], (item[0], float(item[1]) / total))

    sc = SparkContext("local", "Healthcare Hidden Markov Models", pyFiles=[utilModuleFile])

    claimData = sc.textFile(claimDataLocation)
    claimDataMappedByMemberIdDependentId = claimData.map(mapTransition).groupByKey()
    transitionEmissionGoldData = claimDataMappedByMemberIdDependentId.mapPartitions(mapSequences).groupByKey()
    
    # transition
    transitionTotals = transitionEmissionGoldData.filter(lambda row: row[0][2] == transitionType).mapPartitions(sumConditionalTotals).groupByKey()
    transitionProbs = transitionTotals.mapPartitions(createProbabilities).groupByKey()
    transitions = transitionProbs.flatMapValues(lambda row: row)
    transitions.saveAsTextFile(resultsDir + "transitionDictionary")

    # emission
    emissionTotals = transitionEmissionGoldData.filter(lambda row: row[0][2] == emissionType).mapPartitions(sumConditionalTotals).groupByKey()
    emissionProbs = emissionTotals.mapPartitions(createProbabilities).groupByKey()
    emissions = emissionProbs.flatMapValues(lambda row: row)
    emissions.saveAsTextFile(resultsDir + "emissionDictionary")

    # gold test
    goldFiles = transitionEmissionGoldData.filter(lambda row: row[0][2] == goldType).flatMapValues(lambda row: row)
    goldFiles.saveAsTextFile(resultsDir + "goldFiles")

    # TODO: finish prediction 
    def handleGoldFileRow(row):
        print "processing gold files"

        path = row[1]
        actualAmount = 0
        expectedAmount = 0
        predictedAmount = 0

        for transition in path:
            previousTransition = transition[0]
            currentTransition = transition[1]
            emissionKey = transition[2]
            actualAmount = transition[3]

            print transition

    goldFiles.foreach(handleGoldFileRow)

if __name__ == '__main__':
        main()