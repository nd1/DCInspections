"""Command line interface to the Yelp Search API."""

import json
import oauth2
import optparse
import urllib
import urllib2
import csv

dPath = "/users/graham3333/desktop/DC_Rest/"
hPath = "/users/graham3333/desktop/DC_Rest/Yelp/"

# Required options
consumer_key = "rL63BiMOzvpkVHIR62Mftg"
consumer_secret = "qyqILC2U7b14mnWpzjZEUdbQkOk"
token = "Ui-7VXos4bIZckrHWK2dfnLIz6-Rm3R5"
token_secret = "O64Wzo0r_HaxWZ7lCvj_Mo4Gw74"
host = "api.yelp.com"
bk = 0

def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
	"""Returns response for API request."""
	# Unsigned URL
	encoded_params = ''
	if url_params:
		encoded_params = urllib.urlencode(url_params)
	url = 'http://%s%s?%s' % (host, path, encoded_params)
	
	# Sign the URL
	consumer = oauth2.Consumer(consumer_key, consumer_secret)
	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
						'oauth_timestamp': oauth2.generate_timestamp(),
						'oauth_token': token,
						'oauth_consumer_key': consumer_key})
	
	token = oauth2.Token(token, token_secret)
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
	signed_url = oauth_request.to_url()
	
	# Connect
	try:
		conn = urllib2.urlopen(signed_url, None)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()
	except urllib2.HTTPError, error:
		response = json.loads(error.read())
	
	return response


def checkAgain(c, rName, pID, response):
	global w
	if "businesses" not in response:
		print "Exceeded maximum daily requests. Try again tomorrow."
		f2.close()

		f = open(hPath + 'permit_to_yelp_temp.csv', 'rU')
		r = csv.reader(f)
		f3 = open(hPath + 'permit_to_yelp_store.csv', 'wb')
		w = csv.writer(f3)
		for row in r:
			w.writerow(row)
		f3.close()
		global bk
		bk = 1
	elif len(response["businesses"]) == 0:
		print "No Matching Businesses. Marking Blank and moving to next..."
		w.writerow([pID,''])
	elif len(response["businesses"]) <= c:
		check = raw_input("No Other Matches Left. Mark blank (m) or restart (r)?")
		if check == "m":
			w.writerow([pID,''])
		elif check == "r":
			c = 0
			checkAgain(c, rName, pID, response)
		else:
			checkAgain(c, rName, pID, response)
	else:
		print "Name to Match: " + rName
		print "Potential Match: " + response["businesses"][c]["name"]
		print "Geo_Accuracy: " + str(response["businesses"][c]["location"]["geo_accuracy"])
		print "Geo Accuracy Scale: 0 [worst] to 9 [best]"
		print "Responses: y=Yes, n=No, a=abort and no match, r=restart at 1st record"
		check = raw_input("Is this correct?")
		if check != "y" and check != "n":
			if check == "a":
				print "No Match"
				w.writerow([pID,''])
			elif check == "r":
				c = 0
				checkAgain(c, rName, pID, response)
			else:
				checkAgain(c, rName, pID, response)
		elif check == "y":
			print "ID is " + response["businesses"][c]["id"]
			w.writerow([pID,str(response["businesses"][c]["id"].encode("latin1"))])
			c = 0
		else:
			c += 1
			checkAgain(c, rName, pID, response)
  
f = open(dPath + 'restaurants_finalgeo.csv', 'rU')
r = csv.reader(f)
data = []
for row in r:
	data.append([row[0],row[1],row[2]])
	
fDone = open(hPath + 'permit_to_yelp_store.csv', 'rU')
r2 = csv.reader(fDone)
dDone = 0
dA = []
for row in r2:
	dDone += 1
	dA.append([row[0],row[1]])

f.close()
fDone.close()

f2 = open(hPath + 'permit_to_yelp_temp.csv', 'wb')
w = csv.writer(f2)
for i in range(dDone):
	w.writerow(dA[i])

for i in range(dDone, len(data)):
	
	# Setup URL params from options
	url_params = {}
	url_params['term'] = data[i][1]
	#url_params['ll'] = "38.90440268,-77.03446626"
	url_params['location'] = data[i][2]
	url_params['category_filter'] = "restaurants"
	url_params['sort'] = "0"

	response = request(host, '/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
	#print json.dumps(response, sort_keys=True, indent=2)
	
	check = checkAgain(0, url_params['term'], data[i][0], response)
	
	if bk == 1:
		break

f2.close()

f = open(hPath + 'permit_to_yelp_temp.csv', 'rU')
r = csv.reader(f)
f3 = open(hPath + 'permit_to_yelp_store.csv', 'wb')
w = csv.writer(f3)
for row in r:
	w.writerow(row)
f3.close()
