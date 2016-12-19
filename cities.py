# import libraries
import urllib.request
import json
import csv
import traceback
import time

# Define functions

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

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

@RateLimited(5)  # 5 per second at most
def getResponse(url, token):
	req = urllib.request.Request(url)
	# set header
	req.add_header('Authorization','Bearer ' + token)
	# choose to receive in JSON
	req.add_header('Accept','application/json')

	rep = urllib.request.urlopen(req).read().decode('utf8')

	return rep

def setUrl(offset):
	url = 'https://api.lufthansa.com/v1/references/cities?limit=100&offset=' + str(offset) + "&lang=EN"
	return url

try:
	count = 0
	token = get_token()

	for offset in range(0, 5000, 100):
		rep = getResponse(setUrl(offset), token)
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
