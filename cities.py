# import libraries
import urllib.request
import json
import csv
import traceback
import time

import auth

def setUrl(offset):
	url = 'https://api.lufthansa.com/v1/references/cities?limit=100&offset=' + str(offset) + "&lang=EN"
	return url

try:
	count = 0
	token = auth.get_token()

	for offset in range(0, 8400, 100):
		rep = auth.getResponse(setUrl(offset), token)
		rep_json = json.loads(rep)

		# export as CSV
		# if start of export
		if offset == 0:
			f = csv.writer(open("cities.csv", "w"))
			# write CSV headers
			f.writerow(['cityCode', 'countryCode', 'name', 'lat','lon'])
		else:
			f = csv.writer(open("cities.csv", "a"))

		for city in rep_json['CityResource']['Cities']['City']:
				count = count + 1
				if 'Position' not in city:
					f.writerow([
							city['CityCode'],
							city['CountryCode'],
							city['Names']['Name']['$'],
							None,
							None
							])
				else:
					f.writerow([
							city['CityCode'],
							city['CountryCode'],
							city['Names']['Name']['$'],
							city['Position']['Coordinate']['Latitude'],
							city['Position']['Coordinate']['Longitude']
							])

		print('Finished export for ' + str(count) + 'th cities')

except:
	print("Request failed")
	print(traceback.print_exc())
