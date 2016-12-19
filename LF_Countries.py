import urllib.request
import json
import csv
import traceback

token_url='https://api.lufthansa.com/v1/oauth/token'
client_id='qdjw9vsn48t9brhqhghvj724'
client_secret = 'db4uNT4NEb'

# define data
data = urllib.parse.urlencode({'client_id': client_id,'client_secret': client_secret,'grant_type':'client_credentials'})
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

	count = 0;
	for offset in range(0, 1300, 100):	

		# set request url
		# url2: list directory of airports
		url2 = 'https://api.lufthansa.com/v1/references/countries/?lang=EN'
	
		# create request with url2
		req = urllib.request.Request(url2)

		# set header
		req.add_header('Authorization','Bearer '+ token_json['access_token'])
		# choose to receive in JSON
		req.add_header('Accept','application/json')

		rep = urllib.request.urlopen(req).read().decode('utf8')
		rep_json = json.loads(rep)

		for country in rep_json['CountryResource']['Countries']['Country']:
			count = count + 1
			d = country['Names']['Name']
			print([country['CountryCode'],country['ZoneCode'],d['@LanguageCode'],d['$']])

            
			print(country['CountryCode'])


	# export as CSV 
	# if start of export
		f = csv.writer(open("countries.csv", "w"))
		# write CSV headers
		f.writerow(['CountryCode', 'ZoneCode', 'Language', 'Country'])

		print("Created file")

except:
	print("Request failed")
	print(traceback.print_exc())

for rows in rep_json['CountryResource']['Countries']['Country']:
	d = rows['Names']['Name']
	f.writerow([rows['CountryCode'],rows['ZoneCode'],d['@LanguageCode'], d['$']])

print('Export Successful')

