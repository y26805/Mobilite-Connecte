import csv
import sqlite3

# Create database in RAM
conn = sqlite3.connect("mobility.db")
# Create cursor
cur = conn.cursor()

# Create table for airports
cur.execute("CREATE TABLE airports (airportCode, airportName, cityCode, countryCode, lat, lon);")

# Use clean data
with open("airport_clean.csv", "rt",encoding='utf8') as file:
	dr = csv.DictReader(file)
	to_db = [(row['airport_code'], 
		row['airport_name'], 
		row['city_code'], 
		row['country_code'], 
		row['latitude'], 
		row['longitude']) for row in dr]

# Insert each row into DB
cur.executemany("INSERT INTO airports VALUES (?, ?, ?, ?, ?, ?);", to_db)

# Print 
for row in cur.execute("SELECT * FROM airports WHERE countryCode='DE'"):
	print(row)

conn.commit()
conn.close()

