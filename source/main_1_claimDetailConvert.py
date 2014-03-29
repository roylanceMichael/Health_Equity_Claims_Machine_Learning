import sys
import utils
import csv as csv

def main():
	# take input parameters of claims and claimdetails
	claimFile = sys.argv[1]
	claimDetailsFile = sys.argv[2]

	# cycle through each to pick up necessary information
	# IE "join"
	csv_file_object = csv.reader(open(claimFile, 'rb'))
	header = csv_file_object.next()

	claimData = {}

	for row in csv_file_object:
		claimId = row[0]
		memberId = row[1]
		dependentId = row[2]
		serviceStart = row[3]
		serviceEnd = row[4]



if __name__ == '__main__':
        main()