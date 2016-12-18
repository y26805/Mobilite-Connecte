# import libraries
# documentation for urllib: https://docs.python.org/3.5/library/urllib.request.html
import urllib.request
import json
import csv
import traceback

# Define functions
def get_token():
	token_url = 'https://api.lufthansa.com/v1/oauth/token'
	client_id = 'qdjw9vsn48t9brhqhghvj724'
	client_secret = 'db4uNT4NEb'

	# Define data
	data = urllib.parse.urlencode({'client_id': client_id,'client_secret': client_secret,'grant_type':'client_credentials'})
	# Encode text data into UTF8
	bdata = data.encode('utf8')

	try:
		rep = urllib.request.urlopen(url=token_url, data=bdata)

		# Convert bytes to string type and string type to dict
		string = rep.read().decode('utf8')
		token_json = json.loads(string)
		token = token_json['access_token']

		print("Token is: ", token)

		return token

	except:
		print("Token acquisition failed")
		print(traceback.print_exc())


def getResponse(url, token):
	req = urllib.request.Request(url)
	# set header
	req.add_header('Authorization','Bearer ' + token)
	# choose to receive in JSON
	req.add_header('Accept','application/json')

	rep = urllib.request.urlopen(req).read().decode('utf8')

	return rep

def setUrl_schedule(month, day):
	date = '2016-' + str(month) + '-' + str(day)
	url = 'https://api.lufthansa.com/v1/operations/schedules/FRA/ZRH/' + date
	return url

try:
	count = 0
	token = get_token()

	for day in range(24,31):
		rep = getResponse(setUrl_schedule(12,day), token)
		rep_json = json.loads(rep)

		# export as CSV
		# if start of export
		if day == 24:
			f = csv.writer(open("schedule_dir_v3.csv", "w"))
			# write CSV headers
			f.writerow(['count', 'dep1', 'arr1', 'dep2','arr2'])
		else:
			f = csv.writer(open("schedule_dir_v3.csv", "a"))

		for flight in rep_json['ScheduleResource']['Schedule']:
				count = count + 1
				if len(flight['Flight']) != 2:
					f.writerow([count,
						flight['Flight']['Departure']['AirportCode'],
						flight['Flight']['Arrival']['AirportCode']])
				else:
					f.writerow([count,
						flight['Flight'][0]['Departure']['AirportCode'],
						flight['Flight'][0]['Arrival']['AirportCode'],
						flight['Flight'][1]['Departure']['AirportCode'],
						flight['Flight'][1]['Arrival']['AirportCode']])

		print('Finished export for day' + str(day))

except:
	print("Request failed")
	print(traceback.print_exc())
