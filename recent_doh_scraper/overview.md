**Data scraping process:**

The DC Department of Health (DOH) scans reports which are then displayed on a [website](http://dc.healthinspections.us/webadmin/dhd_431/web/?a=Main). The platform is hosted by a third party called [Digital Health Department](http://www.garrisonenterprises.com/?referrer=DC). A public API for the data could not be located so scraping was initiated.

First, a script was written to loop through all alpha numeric search pages on the site and create a cleaned CSV file with the following information:

Permit ID
Business Name
Address
Business Type
Permit url
Google Map url

From there, the Permit url page was accessed to build a file of inspection report urls. At this point in the process, the origin ip address began to be blocked and was unable to access the url content for scraping. As a work around, selenium was used to programatically save all health inspection reports locally. 

Subsquent scripts were created to parse and clean the health report data. 

The following list describes the scripts and their products:

* 00_dc_health.py - create a cleaned CSV called business_list.csv with the following information: Permit ID, Business Name, Address, Business Type, Permit url, Google Map url
* 01_insp_list_pages.py: takes business_list.csv, optionally filters on category (Restaurant Total for this project), and pulls the page for the permit_id. This locally saves an html file for each permit that can be scraped for inspection information and inspection report urls. **note**- this script is supposed to have a function to read the html pulled and produce a file called inspections_raw_rtotal.csv. The code to do that has been misplaced and needs to be recreated.
* 02_inspection_clean.py - transforms inspections_raw_rtotal.csv into inpection_list.csv
* 03_rpt_pages.py - uses the data in 
inpection_list.csv to download each inspection report to a local html file.
* 04_rpt_parse.py - reads the locally saved inspection report and creates two cleaned csv files. report_result.csv contains Date of inspection; time in; time out; phone number; inspector name; inspector badge; risk category; report id. violation_list.csv contains the report id, each violation from the report, whether the report was corrected on site, and whether it was a repeat violation as a single line. It was noted for one report that the information included in the table was off. When this is encountered, a report violation value of 3 is listed so the information can be manually verified.
* 05_dc_restaurants.py - Combines scraped health inspection data, original repo Yelp ids, and geocoordinates for business to create a master list, geo_master.csv, of buisness in the "Restaurant Total" category. This will be used to identify Yelp ids for each business. Yelp ids are strings of the business name, so difficult to match up in all cases. Telephone numbers are the most usefull identifiers but not always included on the inspection report.
* 06_insp_compilation - builds on previous output to create a csv with inspection report, permit_id, date, time, inspec type, critical violation count, non-crit violation count, crit violation corrected on site, non-crit violation corrected on site, crit violation to be resolved, non-crit violation to be resolved, critical violation repeat violation, and non-crit violation repeat violation. Create a second csv with inspection report, permit_id, critical violation count, non-crit violation count, lat, lon for mapping purposes.on-crit violation to be resolved
