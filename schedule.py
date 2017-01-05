# import libraries
import urllib.request
import json
import csv
import traceback
import string

import auth

def setUrl_schedule(origin, destination, month, day):
	date = '2017-' + month + '-' + day
	url = 'https://api.lufthansa.com/v1/operations/schedules/' + origin + '/' + destination + '/' + date + '?directFlights=true'
	return url

try:
	count = 0
	token = auth.get_token()

	exportcsv = 'directFlightPairs.csv'
	importcsv = 'EUplus.csv'

	# # Write csv headers
	# f = csv.writer(open(exportcsv, "w"))
	# f.writerow(['origin', 'des', 'httpcode'])

	with open(importcsv) as csvfile:
		reader = csv.DictReader(csvfile)
		lst = list()
		for row in reader:
			lst.append(row['airportCode'])

	# Create two lists
	originList = lst
	desList = lst

	# Choose alphabets range, if needed
	startChar = 'I'
	endChar = 'M'
	charString = string.ascii_uppercase[:]

	startIdx = charString.index(startChar)
	endIdx = charString.index(endChar)

	rangeChar = charString[startIdx : int(endIdx) + 1]
	rangeList = list(rangeChar)
	print (rangeList)

	# Make requests for all possible pairs of European airports
	for o_item in originList:
		origin = o_item

		for char in rangeList:
			if not origin.startswith(char):
				continue

			for d_item in desList:
				destination = d_item

				code = auth.getCode(setUrl_schedule(origin, destination, '01', '20'), token);

				f = csv.writer(open(exportcsv, "a"))
				f.writerow([o_item, d_item, code])

			print ('Export for flights from ' + origin + ' complete')

	print ('***Export done')

except:
	print("Request failed")
	print(traceback.print_exc())
