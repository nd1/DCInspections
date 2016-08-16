# Cleans up geocoded addresses with Google, Yahoo, etc

from geopy import geocoders
import csv

f = open('/users/graham3333/desktop/DC_Rest/restaurants_final.csv', 'rU')
rows = csv.reader(f)
ffinal = open('/users/graham3333/desktop/DC_Rest/restaurants_finalgeo.csv', 'wb')
writeout = csv.writer(ffinal)
total = 0
geofixed = 0
notfixed = 0

for row in rows:
	if row[3] == '':
		g = geocoders.GoogleV3(api_key="AIzaSyANf7d_cZOhzhN0X2PPTkH8fP525ajdjSE")
		us = geocoders.GeocoderDotUS()  
		try:
			place, (lat,lon) = g.geocode(row[2])
			writeout.writerow([row[0],row[1],row[2],lat,lon])
			print row[2] + ',' + str(lat) + ',' + str(lon)
			geofixed += 1
		except:
			try:
				place, (lat,lon) = us.geocode(row[2])
				writeout.writerow([row[0],row[1],row[2],lat,lon])
				print row[2] + ',' + str(lat) + ',' + str(lon)
				geofixed += 1
			except:
				writeout.writerow([row[0],row[1],row[2],"",""])
				notfixed += 1

	else:
		writeout.writerow(row)

	total += 1

f.close()
ffinal.close()
print str(total) + ' rows processed.'
print str(geofixed) + ' errors geocoded.'
print str(notfixed) + ' still not found.'
	