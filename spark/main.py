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


if __name__ == "__main__":
    def myFunc(s):
        words = s.split(" ")
        filestream = open('test.txt', 'w')
        filestream.write("hello world")
        filestream.close()
        return len(words)

    currentDir = os.getcwd()
    countResultsDir = "/sparkResults"
    claimDataLocation = currentDir + "/transformed/Example.csv"
    sc = SparkContext("local", "Healthcare Hidden Markov Models")
    executeMe = sc.textFile(claimDataLocation).map(myFunc)

    def printMe(r):
        print r
    executeMe.foreach(printMe)






















