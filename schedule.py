# import libraries
import urllib.request
import json
import csv
import traceback

import auth

def setUrl_schedule(month, day):
	date = '2016-' + str(month) + '-' + str(day)
	url = 'https://api.lufthansa.com/v1/operations/schedules/FRA/ZRH/' + date
	return url

try:
	count = 0
	token = auth.get_token()

	for day in range(24,32):
		rep = auth.getResponse(setUrl_schedule(12,day), token)
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

		print('Finished export for day ' + str(day))

except:
	print("Request failed")
	print(traceback.print_exc())
