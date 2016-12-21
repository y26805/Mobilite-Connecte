# import libraries
import urllib.request
import json
import csv
import traceback
import time

import auth

# Define functions

def setUrl(offset):
	url = 'https://api.lufthansa.com/v1/references/countries/?limit=100&offset=' + str(offset) + "&lang=EN"
	return url

try:
    count = 0
    token = auth.get_token()

    for offset in range(0, 300, 100):
        rep = auth.getResponse(setUrl(offset), token)
        rep_json = json.loads(rep)

        # export as CSV
        # if start of export
        if offset == 0:
            f = csv.writer(open("countries.csv", "w"))
            # write CSV headers
            f.writerow(['countryCode', 'zoneCode', 'name'])
        else:
            f = csv.writer(open("countries.csv", "a"))

        for country in rep_json['CountryResource']['Countries']['Country']:

            count = count + 1
            if 'ZoneCode' not in country:
                f.writerow([
                country['CountryCode'],
                None,
                country['Names']['Name']['$'],
                ])
            else:
                f.writerow([
                country['CountryCode'],
                country['ZoneCode'],
                country['Names']['Name']['$'],
                ])

        print('Finished export for ' + str(count) + 'th countries')

except:
    print("Request failed")
    print(traceback.print_exc())
