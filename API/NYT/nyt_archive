#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 14:38:46 2019

@author: jose_jurado_vadillo@brown.edu

This scripts gathers all metadata for articles from the NYT for 2006-2017
using the Archive API.
"""

import requests, json, datetime, time

base_url        = 'https://api.nytimes.com/svc/archive/v1/'
date_now        =   datetime.datetime.now()

for year in range(2006,2018):
    for month in range(1,13):
        print('Year: ',year,' and month: ', month)
        url = (base_url + str(year) + '/' + str(month) 
            + '.json?api-key={my-api-key}')
        r               = requests.get(url = url)
        data            = r.json()
        
        
        file_name       = ('{my-file-name}'
                          + 'year?' + str(year) + '_month?' + str(month) 
                           + '_sdate?' + str(date_now)+ '.json')
        
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
            
        time.sleep(22)
