"""Scrape and clean data from http://dc.healthinspections.us
This script will loop through all alpha numeric search pages on the site and create a cleaned CSV file with the following information:

Permit ID
Business Name
Address
Business Type
Permit url
Google Map url

A copy of the raw data is written to CSV for verification purposes.
The final CSV contains all business types subject to DC health inspection, regardless of category or business permit location.

Potential items to add in the future:
-Ward and Quadrant are avaiable on the site, but parsing them leads to inconsistent results. See if there is a way to reliably pull this data.
-Sending the dataframe directly to the clean_df function was causing some errors so the csv is being read back in for cleaning. Look into figuring out why and see if the intermidiary read can be skipped.
-Address info is not always uniform, look into options to separate into street, city, state, zip.

Notes: after using this script, I noted some blocking issues with the inspections site. Links could be browsed to, but not pulled.

Nicole Donnelly 20160607
with inital code from Kate Rabinowitz
"""

import re
import string
import urllib
import pandas as pd

from bs4 import BeautifulSoup
from time import sleep
from random import randint

def parse_names(name_soup):
    #parse the name, permit, and map data from the soup element
    i = 0
    names=[]
    permits=[]
    maps=[]

    while i < len(name_soup):
        names.append(name_soup[i].contents[1].get_text().encode('utf8'))
        permits.append(name_soup[i].contents[1].get('href'))
        maps.append(name_soup[i].contents[3].get('href'))
        i += 1
    return names, permits, maps

def parse_location(location_soup):
    #parse the location, ward, and category data from the soup element
    location=[]
    #wards=[]
    category=[]

    for element in location_soup:
        location.append(element.find_all(text=re.compile(r'\b ?, DC\b|\b ?, VA\b|\b ?, MD\b|ASTORIA RD NW|\b ?, FL\b')))
        #wards.append(element.find_all(text=re.compile(r'Ward: \b')))
        category.append(element.find_all(text=re.compile(r'Type: \b')))

    #remove blank entries
    location = filter(None, location)
    #wards = filter(None, wards)
    category = filter(None, category)
    return location, category

def raw_df(business, permits, maps, location, category):
    #creates a dataframe with the raw_data

    raw = pd.DataFrame({'Names': business, 'Permit': permits, 'Map': maps, 'Location': location, 'Category': category})
    return raw

def scrape_business(base_url, end_point):

    #the loop will create each url available in the search and scrape each page and return a dataframe

    #create an empty dataframe
    bus_list = pd.DataFrame()

    for x in end_point:
        #items started to error out during testing, adding a sleep timer
        seconds = 5 + (random.random() * 5)
        time.sleep(seconds)
        print "Starting to scrape url ", x

        Bus_Name=[]

        #create the url and read the page with BeautifulSoup
        url = base_url + x
        print url
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')

        #section is the soup item everything is parsed from
        section = soup.find('div', id='divInspectionSearchResults')

        #verify there is data on the page to scrape
        Bus_Name=section.find_next('ul').find_all('h3')
        if len(Bus_Name) == 0:
            print "There are no items to scrape at: %s" % url
        else:
            #get the name, permit, and map data
            Business_Name, Permit_url, Map_url = parse_names(Bus_Name)

            #get the location, ward, and category
            #ward contains quadrant which will be pulled during cleaning
            Location, Category = parse_location(section.find_next('ul').find_all('li'))

            print "Appending %d records to the data frame." % len(Business_Name)
            bus_list = bus_list.append(raw_df(Business_Name, Permit_url, Map_url, Location, Category))
            print "Current total records: %d \n" % len(bus_list)


    return bus_list

def clean_df(df):
    #clean the raw dataframe generated by the scrape

    #remove unwanted characters
    df.replace(regex=True, to_replace=r'( \\r\\n)?\\r\\n\\t\\t\\t\\t|(\[u\')|(\'\])|Type: ', value=r'', inplace=True)

    #parse permit id number and make permit a full url
    for index, row in df.iterrows():
        permit_string = df.Permit.ix[index]
        permit_value = (permit_string.partition('permitID=')[2])
        df.set_value(index, 'Permit_id', permit_value)
        df.set_value(index, 'Permit', ('http://dc.healthinspections.us/webadmin/dhd_431/web/index.cfm' + df.Permit.ix[index]))

    #change the column names
    df.columns = ['category', 'address', 'map_url', 'name', 'permit_url', 'permit_id']

    #drop duplicates. all permit ids are unique but some get listed multiple times in the search pagers
    df.drop_duplicates(subset=['permit_id'], inplace=True)

    #rearrange the dataframe
    new_order = ['permit_id', 'name', 'address', 'category', 'permit_url', 'map_url']
    cleaned = df[new_order]
    return cleaned

def buisness_list():
    #the main function to create the data

    #define the base url and end point to append
    baseurl = 'http://dc.healthinspections.us/webadmin/dhd_431/web/index.cfm?a=inspections&alpha='
    endpoint = list(string.ascii_lowercase) + list (string.digits)
    #endpoint=['a', 'b', 'c', 'd']
    raw = scrape_business(baseurl, endpoint)
    raw.to_csv('business_list_raw.csv', index=False)
    print 'Raw data saved to CSV.'

    #read the raw data csv in and clean it
    df_to_clean = pd.read_csv('business_list_raw.csv')
    clean = clean_df(df_to_clean)
    clean.to_csv('business_list.csv', index=False)
    print 'Data cleaned and save to CSV'

if __name__ == "__main__":
    buisness_list()