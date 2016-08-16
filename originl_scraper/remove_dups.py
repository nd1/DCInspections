# remove duplicate Permit IDs from Restaurant DB

import csv

f = open('/users/graham3333/desktop/DC_Rest/restaurants_update.csv', 'rU')
rows = csv.reader(f)
ffinal = open('/users/graham3333/desktop/DC_Rest/restaurants_final.csv', 'wb')
writeout = csv.writer(ffinal)
pastIDs = []
total = 0
duplicate = 0

for row in rows:
	check = 0
	for index in pastIDs:
		if index == row[0]:
			check = 1
			duplicate += 1
			
	if check == 0:
		writeout.writerow(row)
		pastIDs.append(row[0])
		
	total += 1
	
f.close()
ffinal.close()
print str(total) + ' records processed.'
print str(duplicate) + ' duplicate Permit IDs removed.'