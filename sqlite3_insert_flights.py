import csv
import sqlite3

# Create database in RAM
conn = sqlite3.connect("mobility.db")
# Create cursor
cur = conn.cursor()

def createTable(tablename, arg):
	# check if exists
	cur.execute("CREATE TABLE if not exists " + arg)
	# clear table data
	cur.execute("DELETE FROM " + tablename)

def insertData(tablename, filename,):
	with open(filename, "rt", encoding='utf8') as file:
		dr = csv.DictReader(file)
		if (tablename == "airports"):
			to_db = [(row['airport_code'],
			row['airport_name'],
			row['city_code'],
			row['country_code'],
			row['latitude'],
			row['longitude']) for row in dr]
			# insert each row
			cur.executemany("INSERT INTO " + tablename + " VALUES (?, ?, ?, ?, ?, ?);", to_db)
		if (tablename == "cities"):
			to_db = [(row['cityCode'],
			row['countryCode'],
			row['name'],
			row['lat'],
			row['lon']) for row in dr]
			# insert each row
			cur.executemany("INSERT INTO " + tablename + " VALUES (?, ?, ?, ?, ?);", to_db)
		if (tablename == "countries"):
			to_db = [(
			row['countryCode'],
			row['zoneCode'],
			row['name']) for row in dr]
			# insert each row
			cur.executemany("INSERT INTO " + tablename + " VALUES (?, ?, ?);", to_db)

# # Create table for airports
# createTable("airports", "airports (airportCode, airportName, cityCode, countryCode, lat, lon);")
# insertData("airports", "airport_clean.csv")
#
# # # Create table for cities
# createTable("cities", "cities (cityCode, countryCode, cityName, lat, lon);")
# insertData("cities", "cities.csv")
#
# # Create table for countries
# createTable("countries", "countries (countryCode, zoneCode, name);")
# insertData("countries", "countries.csv")

# # Print
# for row in cur.execute("SELECT airportName FROM airports WHERE countryCode='DE'"):
# 	print(row)

filename = 'directFlightPairs_01_24.csv'
tablename = 'flights'

with open(filename, "rt", encoding='utf8') as file:
	dr = csv.DictReader(file)
	to_db = [(row['origin'],
	row['des'],
	row['httpcode']) for row in dr]
	# insert each row
	cur.executemany("INSERT INTO " + tablename + " VALUES (?, ?, ?, '2017-01-24');", to_db)

conn.commit()
conn.close()
