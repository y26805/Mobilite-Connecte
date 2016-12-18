# import libraries
# documentation for urllib: https://docs.python.org/3.5/library/urllib.request.html
import urllib.request
import json
import csv
import traceback

token_url = 'https://api.lufthansa.com/v1/oauth/token'
client_id = 'qdjw9vsn48t9brhqhghvj724'
client_secret = 'db4uNT4NEb'
csvname = 'airport_dir_v2.csv'

# define data
data = urllib.parse.urlencode({
	'client_id': client_id,
	'client_secret': client_secret,
	'grant_type':'client_credentials'
	})
# encode text data into UTF8
bdata = data.encode('utf8')

try:
	rep = urllib.request.urlopen(url=token_url, data=bdata)
	
	# Convert bytes to string type and string type to dict
	string = rep.read().decode('utf8')
	token_json = json.loads(string)

	print("Token is: ", token_json['access_token'])

# if rep.getcode() != 200
except:
	print("Token acquisition failed")
	print(traceback.print_exc())

try:
	# create offset variable because max. number of records is 100
	offset = 0
	count = 0;

	for offset in range(0, 1300, 100):	

		# set request url
		# url1: flights from CDG to HKG scheduled on 31 dec 2016
		# url2: list directory of airports
		url1 = 'https://api.lufthansa.com/v1/operations/schedules/CDG/HKG/2016-12-31'
		url2 = 'https://api.lufthansa.com/v1/references/airports?lang=EN&limit=100&offset=' + str(offset)
	
		# create request with url2
		req = urllib.request.Request(url2)

		# set header
		req.add_header('Authorization','Bearer '+ token_json['access_token'])
		# choose to receive in JSON
		req.add_header('Accept','application/json')

		rep = urllib.request.urlopen(req).read().decode('utf8')
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

