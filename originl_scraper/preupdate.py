# Organizes files pre-update

import os
import datetime
import csv

# Remove unnecessary files
os.remove('/users/graham3333/desktop/DC_Rest/restaurants_final.csv')
os.remove('/users/graham3333/desktop/DC_Rest/restaurants_update.csv')

# Copy restaurant, inspection, and violation files to Archive folder
f = open('/users/graham3333/desktop/DC_Rest/restaurants_finalgeo.csv', 'rU')
f2 = open('/users/graham3333/desktop/DC_Rest/violations_update.csv', 'rU')
f3 = open('/users/graham3333/desktop/DC_Rest/inspection_update.csv', 'rU')
fr = csv.reader(f)
fr2 = csv.reader(f2)
fr3 = csv.reader(f3)

now = datetime.datetime.now()
date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)

w = open('/users/graham3333/desktop/DC_Rest/Archive/restaurants_' + date + '.csv', 'wb')
w2 = open('/users/graham3333/desktop/DC_Rest/Archive/violations_' + date + '.csv', 'wb')
w3 = open('/users/graham3333/desktop/DC_Rest/Archive/inspection_' + date + '.csv', 'wb')
ww = csv.writer(w)
ww2 = csv.writer(w2)
ww3 = csv.writer(w3)

for row in fr:
	if row[3] == "ERROR":
		row[3] = ""
	if row[4] == "ERROR":
		row[4] = ""
	ww.writerow(row)

print 'Restaurant file backed up.'

for row in fr2:
	ww2.writerow(row)

print 'Violations file backed up.'

for row in fr3:
	ww3.writerow(row)

print 'Inspection file backed up.'

f.close()
f2.close()
f3.close()
w.close()
w2.close()
w3.close()

# Delete files in main folder to allow for new files
os.remove('/users/graham3333/desktop/DC_Rest/restaurants_finalgeo.csv')
os.remove('/users/graham3333/desktop/DC_Rest/violations_update.csv')
os.remove('/users/graham3333/desktop/DC_Rest/inspection_update.csv')