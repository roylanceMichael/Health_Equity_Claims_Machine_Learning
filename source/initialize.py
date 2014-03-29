import json
import utils
import pymssql

def main():
	# static strings
	master = "master"
	initializeSqlFile = "sqlScripts/1_initialize.sql"
	databaseExistsSql = "select 1 from sys.databases where name = %s"
	createDatabaseSql = "create database [%s]"

	# if the database exists, do not continue
	configFile = utils.readConfigFile()
	database = configFile["database"]

	conn = pymssql.connect(host=configFile["host"], user=configFile["user"], password=configFile["password"], database=master)
	cur = conn.cursor()
	cur.execute(databaseExistsSql, database)
	row = cur.fetchone()
	conn.close()

	if not row:
		conn = pymssql.connect(host=configFile["host"], user=configFile["user"], password=configFile["password"], database=master)
		cur = conn.cursor()
		cur.execute(createDatabaseSql, database)
		conn.commit()

		# read in the initializeSql
		f = open(initializeSqlFile, 'r')
		initializeSql = f.read()
		cur.execute(initializeSql)
		conn.commit()

if __name__ == '__main__':
        main()