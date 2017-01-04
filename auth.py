import urllib.request
import urllib.error
import json
import traceback
import time

import hidden

def get_token():
    token_url = 'https://api.lufthansa.com/v1/oauth/token'
    secrets = hidden.oauth()
    client_id = secrets['client_id']
    client_secret = secrets['client_secret']

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

@RateLimited(5)  # 5 per second at most
def getResponse(url, token):
	req = urllib.request.Request(url)
	# set header
	req.add_header('Authorization','Bearer ' + token)
	# choose to receive in JSON
	req.add_header('Accept','application/json')

	rep = urllib.request.urlopen(req).read().decode('utf8')

	return rep

def getCode(url, token):
    req = urllib.request.Request(url)
    # set header
    req.add_header('Authorization','Bearer ' + token)
    # choose to receive in JSON
    req.add_header('Accept','application/json')

    try:
        http_code = urllib.request.urlopen(req).getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return e.code
    else:
        return http_code
