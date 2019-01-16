#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:06:09 2019

@author: jose_jurado_vadillo@brown.edu

This script downloads ALL articles for a given set of terms.
"""

import requests, math, json, datetime, time

# -------------------------- Define values ------------------
base_url        =   'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
search_term     =   '{my-search-term}'
myAPI_key       =   '{my-api-key}'
date_now        =   datetime.datetime.now()
# -------------------------- Define values ------------------

title = ''
for word in search_term.split():
    title = title + '_' + word

title = title[1:]

# Goods (examples)
# Headlines
# data['response']['docs'][1]['headline']['main'] 

# Display total nr. of hits
PARAMS          = {'api-key':myAPI_key,'q':search_term,
                       'begin_date':'20110101', 'end_date':'20171231'}
r               = requests.get(url = base_url, params=PARAMS)
data            = r.json()
hits            = data['response']['meta']['hits']
print('Total nr. of hits: ', hits)
time.sleep(6)

for year in range(2011,2018):
    print('Year: ', year)
    # Count number of hits
    start_val       = str(year) + '0101'
    end_val         = str(year) + '1231'
    PARAMS          = {'api-key':myAPI_key,'q':search_term,
                       'begin_date':start_val, 'end_date':end_val}
    r               = requests.get(url = base_url, params=PARAMS)
    data            = r.json()
    
    hits            = data['response']['meta']['hits']
    
    if hits > 2000:
        print('Too many hits for year: ', year)
        
    for page in range(1,math.ceil(hits/10)+1):
        PARAMS          = {'api-key':myAPI_key,'q':search_term,
                       'begin_date':start_val, 'end_date':end_val,
                       'page':page}
        r               = requests.get(url = base_url, params=PARAMS)
        data            = r.json()
        
        file_name       = ('{my-file-name}' +
                          title + '/year?' + str(year) + '_page?' + str(page) 
                           + '_sdate?' + str(date_now)+ '.json')
                           
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
        #time.sleep(6)   # As recommended by the NYT
        time.sleep(22) # To remain below 4,000 queries/day
