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
    utilModuleFile = currentDir + "source/utils.py"
    claimsDetailsOrderedMemberIDDateZipFile = transformedDir + "/ClaimDetailDependent.zip"
    claimsDetailsOrderedMemberIDDateFile = transformedDir + "/ClaimDetailDependent.csv"
    claimDataLocation = currentDir + claimsDetailsOrderedMemberIDDateFile

    # extract zip if it doesn't exist already
    utils.extractFileIfNotExists(claimsDetailsOrderedMemberIDDateZipFile, claimsDetailsOrderedMemberIDDateFile, transformedDir)

    # 0, 1, 2, 3, 4, 5, 6, 7, 11
    # memberId, dependentId, cptCode, ccsCode, patientAmount, totalAmount, Year, Gender are the fields we care about

    def buildTransitionWrapper(gender, year, state):
        return utils.buildTransition(utils.ageGender, gender, year, "", "") + state

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

        return ((memberId, dependentId), (memberId, dependentId, ccsCode, patientAmount, year, gender, serviceDate))

    def mapSequences(rows):
        for row in rows:
            personRecords = row[1]
            sorted(row[1], key=lambda x: (x[6], x[2]))
            startState = "START"
            previous = startState

            for item in personRecords:
                current = buildTransitionWrapper(item[5], item[4], item[2])
                yield ((previous, current), 1)
                previous = current

    def sumConditionalTotals(rows):
        for row in rows:
            total = len(row[1])
            yield (row[0][0], (row[0][1], total))

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

    executeMe = sc.textFile(claimDataLocation)
    executeMe = executeMe.map(mapTransition).groupByKey()
    executeMe = executeMe.mapPartitions(mapSequences).groupByKey()
    executeMe = executeMe.mapPartitions(sumConditionalTotals).groupByKey()
    executeMe = executeMe.mapPartitions(createProbabilities).groupByKey()
    executeMe = executeMe.flatMapValues(lambda row: row)
    executeMe.saveAsTextFile(resultsDir + "transitionDictionary")

if __name__ == '__main__':
        main()