# Count new restaurants, inspections, and violations

import csv
import datetime

now = datetime.datetime.now()
date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
counts = {"r":0,"i":0,"v":0}

path = "/users/graham3333/desktop/dc_rest/"
aPath = "/users/graham3333/desktop/dc_rest/archive/"

f = open(path + "inspection_update.csv", "rU")
f2 = open(path + "violations_update.csv", "rU")
f3 = open(path + "restaurants_finalgeo.csv", "rU")
r = csv.reader(f)
r2 = csv.reader(f2)
r3 = csv.reader(f3)

f4 = open(aPath + "inspection_" + date + ".csv", "rU")
f5 = open(aPath + "violations_" + date + ".csv", "rU")
f6 = open(aPath + "restaurants_" + date + ".csv", "rU")
r4 = csv.reader(f4)
r5 = csv.reader(f5)
r6 = csv.reader(f6)

count = 0
for row in r:
	count += 1

countMatch = 0
for row in r4:
	countMatch += 1
	
counts["i"] = count - countMatch

count = 0
for row in r2:
	count += 1

countMatch = 0
for row in r5:
	countMatch += 1
	
counts["v"] = count - countMatch

count = 0
for row in r3:
	count += 1

countMatch = 0
for row in r6:
	countMatch += 1
	
counts["r"] = count - countMatch

print "(monthly update) " + str(counts["r"]) + " new restaurants, " + str(counts["i"]) + " new inspections, and " + str(counts["v"]) + " new violations. grahamimac.com/inspectionmapper"

f.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
