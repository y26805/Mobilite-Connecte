# import libraries
# documentation for urllib: https://docs.python.org/3.5/library/urllib.request.html
import urllib.request
import json
import csv
import traceback

import auth

token_url = 'https://api.lufthansa.com/v1/oauth/token'
csvname = 'airport_dir_v2.csv'

def setUrl(offset):
	url = 'https://api.lufthansa.com/v1/references/airports?lang=EN&limit=100&offset=' + str(offset)
	return url

try:
	# create offset variable because max. number of records is 100
	offset = 0
	count = 0;

	token = auth.get_token()

	for offset in range(0, 1300, 100):

		rep = auth.getResponse(setUrl(offset), token)
		rep_json = json.loads(rep)

		for airport in rep_json['AirportResource']['Airports']['Airport']:
			count = count + 1

		print("Airport count", count)

		# export as CSV
		# if start of export
		if offset == 0:
			f = csv.writer(open(csvname, "w"))
			# write CSV headers
			f.writerow([
				'airport_code',
				'airport_name',
				'city_code',
				'country_code',
				'latitude',
				'longitude',
				'type'
				])
		else:
			f = csv.writer(open(csvname, "a"))

		for airport in rep_json['AirportResource']['Airports']['Airport']:
			# Check if location is airport (NOT bus and NOT train station)
			if not airport['LocationType'] == 'Airport':
				continue
			# Check if 'Position' element exists
			if 'Position' not in airport:
				f.writerow([
					airport['AirportCode'],
					airport['Names']['Name']['$'],
					airport['CityCode'],
					airport['CountryCode'],
					None,
					None,
					airport['LocationType']
					])
			else:
				f.writerow([
					airport['AirportCode'],
					airport['Names']['Name']['$'],
					airport['CityCode'],
					airport['CountryCode'],
					airport['Position']['Coordinate']['Latitude'],
					airport['Position']['Coordinate']['Longitude'],
					airport['LocationType']
					])


	print('Export successful')

except:
	print("Request failed")
	print(traceback.print_exc())
