import os
from sklearn import metrics
from pyspark import SparkContext

sc = SparkContext("local", "Healthcare Hidden Markov Models")
currentDir = os.getcwd()

claimDataLocation = currentDir + "/transformed/ClaimDetailDependent.csv"

print 'expecting the data to exist in HDFS here: %s' % claimDataLocation

claimData = sc.textFile(claimDataLocation)

print 'size of claim data is %s' % (claimData.count())

# memberId, dependentId, cptCode, patientAmount are the fields we care about

