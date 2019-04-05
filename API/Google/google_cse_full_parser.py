#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:21:45 2019

@author: jose_jurado_vadillo@brown.edu

Makes queries using Google CSE and stores results in json.
Makes queries across time windows.
"""

import requests, csv, datetime, json, time, os

#Import CSE keys
reader      = csv.reader(open('keys.csv', 'r'))
key_list    = {}

for row in reader:
   k, v         = row
   key_list[k]  = v

#Import Google CSE ID's
reader          = csv.reader(open('CSE_engines.csv', 'r'))
cse_id_dict     = {}

for row in reader:
   k, v = row
   cse_id_dict[k] = v

# ---------------- User Input ---------------------------------------------
searchkeylist       = ['dogs', 'cats','ferrets']
newspaper           = 'national-geographic'
startdate           = datetime.datetime(2000,1,1,0,0,0)
enddate             = datetime.datetime(2017,10,15,0,0,0)
deltatime           = 30 # nr of dates considered
maxnrpages          = 10 # maximum nr pages to query for date x term x newspaper
# ---------------- User Input ---------------------------------------------

# ---------------- Parameters (immutable) ---------------------------------
key                 = key_list['my-preferred-key']                  # Google cloud API key
base_url            = 'https://www.googleapis.com/customsearch/v1'
numval              = 10
cx                  = cse_id_dict[newspaper]
storedir            = ('./queries/'
                       + newspaper)
date_now            = str(datetime.datetime.now())
wait_time           = 1.2
# ---------------- Parameters (immutable) ---------------------------------

def leadzero(value):
    if value < 10:
        newstring = '0' + str(value)
    else:
        newstring = str(value)
    return newstring

# Generate a directory to store results
if not os.path.exists(storedir):
    os.makedirs(storedir)

# ---------------------------------------------------------
# Count nr. of search combinations required
total_counts = 1

for word in searchkeylist:
    # Starting values of loop
    startdateval    = startdate
    enddateval      = startdateval + datetime.timedelta(days=deltatime)  
    while enddateval <= enddate:
        total_counts += 1
        startdateval    = enddateval + datetime.timedelta(days=1)
        enddateval      = enddateval +  datetime.timedelta(days=deltatime +1)
    
max_total_api_calls = total_counts * maxnrpages
print('Parsing: ', newspaper)
print('Maximum nr. of API calls: ', max_total_api_calls)
print('Maximum time to run: ', max_total_api_calls*wait_time/60,
      ' minutes')
print('Minimum nr. of API calls: ', total_counts)
print('Minimum time to run: ', total_counts*wait_time/60, ' minutes')
# ---------------------------------------------------------

# Make queries
counter         = 1
queries_count   = 0
errors_count    = 0

for term in searchkeylist:
    # Reset starting values of loop
    startdateval    = startdate
    enddateval      = startdateval + datetime.timedelta(days=deltatime)
    update_window   = False  
    
    while enddateval <= enddate:
        # Updates the query window (except the first time it runs)
        if update_window:
            startdateval = enddateval + datetime.timedelta(days=1)
            enddateval   = enddateval + datetime.timedelta(days=deltatime)
        else:
            update_window = True
        
        # Construct date restriction
        startdatestr    = (str(startdateval.year)+ 
                                leadzero(startdateval.month) + leadzero(startdateval.day))
        
        enddatestr      =  (str(enddateval.year)+ 
                                leadzero(enddateval.month) + leadzero(enddateval.day))
    
        
        sortkey     = 'date:r:' + startdatestr + ':' + enddatestr
        
        # Print progress
        print(queries_count/max_total_api_calls*100, '% of max.', 
              ' | ', queries_count/total_counts*100, '% of min.',
              ' | term: ',
              term, ' | start: ', startdatestr)
        counter += 1
        
        for numpage in range(0,maxnrpages):
            startval= numpage*10 + 1
            
            PARAMS  = {'q': term, 'cx': cx, 'key': key,
                           'num': numval, 'sort': sortkey, 'start':
                               startval}
            
            r               = requests.get(url = base_url, params = PARAMS)
            time.sleep(wait_time) # guarantees < 100 queries every 100 seconds
            queries_count   += 1
            data            = r.json()            
            
            # Store results
            filename = (storedir + '/' +  term + '_' + 
                        sortkey + '_' + str(numpage) + 
                        '_' + date_now + '.json')
            
            with open(filename, 'w') as fp:
                json.dump(data, fp)
            
            # Skip if there are no more results
            # In rare instances there are "back-end errors". So
            # data['searchInformation']['totalResults'] doesn't exist
            try:
                if data['searchInformation']['totalResults'] == '0':
                    break
            except:
                print('Error for: ', term, ' date ', sortkey,
                      ' page ', numpage)
                errors_count += 1
                break # If error skip to next date parsed
    
print('Queries used: ', queries_count, ' | Total errors: ',
      errors_count)
