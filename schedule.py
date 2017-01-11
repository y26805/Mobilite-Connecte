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

# Choose alphabets range, if needed. Range is inclusive of starChar and endChar
def setRange(startChar, endChar):
	charString = string.ascii_uppercase[:]

	startIdx = charString.index(startChar)
	endIdx = charString.index(endChar)

	rangeChar = charString[startIdx : int(endIdx) + 1]
	rangeList = list(rangeChar)

	return rangeList

def setInputDate():
	month = input('Enter month')
	date = input('Enter date')

	return month, date

def setInputRange():
	startChar = input('Enter starting alphabet')
	endChar = input('Enter finishing alphabet')

	print('Programme will run from ' + startChar + ' to ' + endChar)

	return startChar, endChar

try:
	token = auth.get_token()

	month, date = setInputDate()
	startChar, endChar = setInputRange()

	exportcsv = 'directFlightPairs_' + month + '_' + date + '.csv'
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


	# Make requests for all possible pairs of European airports
	for o_item in originList:
		origin = o_item

		for char in setRange(startChar, endChar):
			if not origin.startswith(char):
				continue

			for d_item in desList:
				destination = d_item

				code = auth.getCode(setUrl_schedule(origin, destination, month, date), token);

				f = csv.writer(open(exportcsv, "a"))
				f.writerow([o_item, d_item, code])

			print ('Export for flights from ' + origin + ' complete')

	print ('***Export done')

except:
	print("Request failed")
	print(traceback.print_exc())
