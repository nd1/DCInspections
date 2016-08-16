# Output files with headers for data download

import csv

# Copy restaurant, inspection, and violation files to Archive folder
f = open('/users/graham3333/desktop/DC_Rest/restaurants_finalgeo.csv', 'rU')
f2 = open('/users/graham3333/desktop/DC_Rest/violations_update.csv', 'rU')
f3 = open('/users/graham3333/desktop/DC_Rest/inspection_update.csv', 'rU')
f4 = open('/users/graham3333/desktop/DC_Rest/num_to_cat.csv', 'rU')
f5 = open('/users/graham3333/desktop/DC_Rest/Yelp/permit_to_yelp_store.csv', 'rU')
f6 = open('/users/graham3333/desktop/DC_Rest/Open_Table/opentable.csv', 'rU')
fr = csv.reader(f)
fr2 = csv.reader(f2)
fr3 = csv.reader(f3)
fr4 = csv.reader(f4)
fr5 = csv.reader(f5)
fr6 = csv.reader(f6)

w = open('/users/graham3333/desktop/inspectionmapper/data/restaurants.csv', 'wb')
w2 = open('/users/graham3333/desktop/inspectionmapper/data/violations.csv', 'wb')
w3 = open('/users/graham3333/desktop/inspectionmapper/data/inspections.csv', 'wb')
w4 = open('/users/graham3333/desktop/inspectionmapper/data/violations_key.csv', 'wb')
w5 = open('/users/graham3333/desktop/inspectionmapper/data/yelp_crosswalk.csv', 'wb')
w6 = open('/users/graham3333/desktop/inspectionmapper/data/opentable_crosswalk.csv', 'wb')
ww = csv.writer(w)
ww2 = csv.writer(w2)
ww3 = csv.writer(w3)
ww4 = csv.writer(w4)
ww5 = csv.writer(w5)
ww6 = csv.writer(w6)

ww.writerow(["Permit ID","Name","Address","Lattitude","Longitude"])
for row in fr:
	ww.writerow(row)

print 'Restaurant data ready.'

ww2.writerow(["Inspection ID","Violation Number","Violation Text"])
for row in fr2:
	ww2.writerow(row)

print 'Violations data ready.'

ww3.writerow(["Inspection ID","Permit ID","Date","Time","Inspection Type","Critical Violations","Non Critical Violations","Critical Violations Corrected On Site","Critical Violations To Be Resolved","Non Critical Violations Corrected On Site","Non Critical Violations To Be Resolved"])
for row in fr3:
	ww3.writerow(row)

print 'Inspections data ready.'

ww4.writerow(["Violation Number","Violation Description","Violation Category"])
for row in fr4:
	ww4.writerow(row)

print 'Violations Key data ready.'

ww5.writerow(["PermitID","YelpID"])
for row in fr5:
	ww5.writerow(row)

print 'Yelp Crosswalk data ready.'

ww6.writerow(["PermitID","OpenTableID"])
for row in fr6:
	ww6.writerow(row)

print 'OpenTable Crosswalk data ready.'

f.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
w.close()
w2.close()
w3.close()
w4.close()
w5.close()
w6.close()