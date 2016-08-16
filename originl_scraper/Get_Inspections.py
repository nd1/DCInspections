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
pre = 'http://washington.dc.gegov.com/webadmin/dhd_431/'

f = open('/users/graham3333/desktop/DC_Rest/inspection_update.csv', 'wb')
f2 = open('/users/graham3333/desktop/DC_Rest/violations_update.csv', 'wb')
restall = csv.writer(f)
viol = csv.writer(f2)

read = open('/users/graham3333/desktop/DC_Rest/Archive/inspection_' + date + '.csv', 'rU')
read2 = open('/users/graham3333/desktop/DC_Rest/Archive/violations_' + date + '.csv', 'rU')
re = csv.reader(read)
re2 = csv.reader(read2)
inspList = []
violList = []

# Read all entries from old tables into a list and write them into new table
for row in re:
	inspList.append(str(row[0]) + str(row[1]))
	restall.writerow(row)
		
for row in re2:
	viol.writerow(row)
		
read.close()
read2.close()

businesses = requests.post(URL, data = headers)

soup = BeautifulSoup(businesses.text)
results = soup.find(id="divInspectionSearchResults").ul
loop = results.find_all('li')

for rest in loop:
	# Get Permit ID, if the li has no h3 attribute, it's an inspection and not a restaurant name
	if rest.h3:
		href = rest.h3.a['href']
		hlen = len(href.split('='))
		pID = href.split('=')[hlen-1]	
		print pID	
		
		insp = rest.find(id="divInspectionSearchResultsListing").find_all('li')
		for i in insp:
			check = i.prettify().split('</a>')[1].split('</li>')[0].rstrip().lstrip()
			if check != '(PDF)':
				# Get iID
				iID = i.a['href'].split('inspectionID=')[1].split('&')[0]
				
				exist = iID + pID
				existTest = 0
				for test in inspList:
					if exist == test:
						existTest = 1
						
				if existTest == 0:

					# Get all other stats
					followURL = pre + i.a['href'].replace('../','')
					r = urllib2.urlopen(followURL).read()
					
					# Get Date, Time, and Type
					s = BeautifulSoup(r).find("table", class_="times").tr.td.table.find_all('tr')
					nums = s[3].find_all('div')
					Date = nums[3].string.rstrip().lstrip() + '-' + nums[1].string.rstrip().lstrip() + '-' + nums[2].string.rstrip().lstrip()
					# If there is an AM or PM listed
					if s[3].sup:
						if s[3].sup.string:
							dayCheck = s[3].sup.string.rstrip().lstrip()
							if dayCheck == 'AM':
								if nums[4].string.rstrip().lstrip() == "":
									firstTime = "00"
								else:
									firstTime = nums[4].string.rstrip().lstrip()
							else:
								if nums[4].string.rstrip().lstrip() == "":
									firstTime = "00"
								else:
									firstTime = str(int(float(nums[4].string.rstrip().lstrip())) + 12)
							if nums[5].string.rstrip().lstrip() == "":
								lastTime = "00"
							else:
								lastTime = nums[5].string.rstrip().lstrip()
							Time =  firstTime + ':' + lastTime
					# If there is no AM or PM listed
					else:
						Time = "00:00"						
					Type = s[5].find_all('div')[7].string.rstrip().lstrip()
					
					# Get Violations Summary Information
					s = BeautifulSoup(r).find("table", class_="times").tr.find("table", class_="times").find_all('tr')
					crit = s[1].find_all('td')
					ncrit = s[2].find_all('td')
					CritViol = crit[1].string.rstrip().lstrip()
					CV_COS = crit[3].string.rstrip().lstrip()
					CV_R = crit[5].string.rstrip().lstrip()			
					NCritViol = ncrit[1].string.rstrip().lstrip()
					NCV_COS = ncrit[3].string.rstrip().lstrip()
					NCV_R = ncrit[5].string.rstrip().lstrip()
					if CritViol == '':
						CritViol = '0'
					if CV_COS == '':
						CV_COS = '0'
					if CV_R == '':
						CV_R = '0'
					if NCritViol == '':
						NCritViol = '0'
					if NCV_COS == '':
						NCV_COS = '0'
					if NCV_R == '':
						NCV_R = '0'
						
					# Write to CSV and print values
					print '    ' + iID + ', ' + pID + ', ' + Date + ', ' + Time + ', ' + Type + ', ' + CritViol + ', ' + NCritViol + ', ' + CV_COS + ', ' + CV_R + ', ' + NCV_COS + ', ' + NCV_R
					restall.writerow([iID,pID,Date,Time,Type,CritViol,NCritViol,CV_COS,CV_R,NCV_COS,NCV_R])
					
					# Get Violations Details, write to CSV and print values
					s = BeautifulSoup(r).find(class_="times fs_10px").find_all('tr')
					for j in s:
						try:
							c = ' '.join(j.td['class'])
						except:
							c = '_blank'
						if c == 'b t':
							sBlank = s.index(j)
					totalBlank = len(s) - sBlank + 1
					if len(s) == totalBlank:
						numviol = 'None'
						textviol = 'None'
						print '        ' + iID + ', ' + numviol
						viol.writerow([iID,numviol,textviol])
					else:
						for j in range(1, len(s) - totalBlank + 1):
							v = s[j].td.string.rstrip().lstrip()
							try:
								numviol = v.split('.')[0]
							except:
								numviol = 'None'
							try:
								textviol = v.split('. - ')[1].replace('"','')
							except:
								textviol = 'No text provided (by DC Department of Health)'
							textviol = ' '.join(textviol.split())
							print '        ' + iID + ', ' + numviol
							try:
								viol.writerow([iID,numviol,textviol])
							except:
								viol.writerow([iID,numviol,"Character encoding error"])


f.close() 
f2.close()