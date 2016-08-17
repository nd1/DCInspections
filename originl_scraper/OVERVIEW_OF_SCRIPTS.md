### overview of original scraper process

**preupdate.py** 
creates backups of csv files; removes the original files after backup



**restaurants_update.py**
uses requests to create a url using these headers:

headers  = {"a":"Inspections",
"inputEstabName":"",
"inputPermitType":10, # restaurants
"inputInspType":"ANY",
"inputWard":"ANY",
"inputQuad":"ANY",
"btnSearch":"Search"}

The requests call builds this url- http://dc.healthinspections.us/webadmin/dhd_431/web/
which has no inspection data. Perhaps there was an API that is now defunct?

The script would pull the name and address from the returned page and geocode it then write it to restaurants_update.csv


**remove_dups.py**
removes duplicate doh permit id data from restaurants_update.csv


**clean_geo.py**
additional attempts to geoencode data in restaurants_update.csv if it was not successful on the first attempt in restaurants_update.py

**Get_Inspections.py**

Parses inspection data. 


Manually update OpenTable crosswalk -- no further info on this step. Likely will be a future feature. Work on getting yelp info first.

**Yelp/search.py**

Attempts to match business with their yelp ids.


**updatedata.py**

**count_new.py**