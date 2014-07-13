import sys
import utils

def main():
	utils.prepareCsvForBigDataMarkov("transformed/ClaimDetailDependent.csv", "transformed/ClaimUpdated.csv")	

if __name__ == '__main__':
        main()