# First fill first DB with names, Permit IDs, Address, UniqueID (Mine) and a second DB with UniqueID and URLs
# Some code from https://scraperwiki.com/scrapers/dc_restaurant_inspections/edit/
import requests
from bs4 import BeautifulSoup
import csv
import urllib2
from unidecode import unidecode
import datetime

now = datetime.datetime.now()
date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)

headers  = {"a":"Inspections",
"inputEstabName":"",
"inputPermitType":10, # restaurants
"inputInspType":"ANY",
"inputWard":"ANY",
"inputQuad":"ANY",
"btnSearch":"Search"}
URL = 'http://washington.dc.gegov.com/webadmin/dhd_431/web/index.cfm'
Nom = 'http://nominatim.openstreetmap.org/search?format=xml&q='

read = open('/users/graham3333/desktop/DC_Rest/Archive/restaurants_' + date + '.csv', 'rU')
re = csv.reader(read)
storeDB = []

f = open('/users/graham3333/desktop/DC_Rest/restaurants_update.csv', 'wb')
restall = csv.writer(f)

for row in re:	
	if row[3] == "ERROR":
		row[3] = ""
	if row[4] == "ERROR":
		row[4] = ""
	restall.writerow(row)
	storeDB.append(str(row[0]))
		
businesses = requests.post(URL, data = headers)

soup = BeautifulSoup(businesses.text)
results = soup.find(id="divInspectionSearchResults").ul
loop = results.find_all('li')

for rest in loop:
	# Get Permit ID, if the li has no h3 attribute, it's an inspection and not a restaurant name
	try: 
		href = rest.h3.a['href']
		hlen = len(href.split('='))
		pID = href.split('=')[hlen-1]
	
		checkTest = 0
		for i in storeDB:
			if pID == i:
				checkTest = 1
		
		if checkTest == 0:
		
			# Get Restaurant Name
			rName = rest.h3.a.string.rstrip().lstrip()
		
			# Get Name
			address = rest.prettify().split('</h3>')[1].split('<br/>')[0].rstrip().lstrip()
		
			# Geocode Address in Nominatim
			a = address.replace(' ','+')
			NomResults = urllib2.urlopen(Nom + a).read()		
		
			try: 
				lon = NomResults.split('lon="')[1].split('"')[0]
			except IndexError:
				try: 
					lon = NomResults.split("lon='")[1].split("'")[0]
				except IndexError:
					lon = ''
			try: 
				lat = NomResults.split('lat="')[1].split('"')[0]
			except IndexError:
				try:
					lat = NomResults.split("lat='")[1].split("'")[0]
				except IndexError:
					lat = ''
			
			# Write to CSV
			rName = unidecode(rName) # Remove any accented/non-standard letters
			address = unidecode(address)
			restall.writerow([pID, rName, address, lat, lon])
			
			print rName
		
	except AttributeError:
		pass

f.close() 