import os
from sklearn import metrics
from pyspark import SparkContext

currentDir = os.getcwd()
countResultsDir = "/sparkResults"
claimDataLocation = currentDir + "/transformed/Example.csv"

#sc = SparkContext("local", "Healthcare Hidden Markov Models")

print 'expecting the data to exist in HDFS here: %s' % claimDataLocation

#claimData = sc.textFile(claimDataLocation)

# print 'size of claim data is %s' % (claimData.count())

# 0, 1, 2, 3, 
# memberId, dependentId, cptCode, patientAmount are the fields we care about

transitionDictionary = {}
emissionDictionary = {}

# def mapFunc(row):
#   # is this the start state?
#   fileStream.write(str(row))
#   return 1

# fileStream = open("testMe.txt", "w")

# claimData.map(mapFunc)

# fileStream.close()

def mapDict(row):
    transition = row[3] + "_" + row[6] + "_" + row[7]
    
    return (transition, 1)


sc = SparkContext("local", "Healthcare Hidden Markov Models")
executeMe = sc.textFile(claimDataLocation).map(mapDict)

def printMe(r):
    print r
    
executeMe.foreach(printMe)






















