#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 16:21:02 2019

@author: jose_jurado_vadillo@brown.edu

Builds archive with news from NYT Archive API.
"""

import json, os, datetime
import pandas as pd

dirlist_0   = '{my-data-directory}' # route where nyt_archive.py stores code
data_route  = '{my-store-route}'

main_columns = ['lead_paragraph', 'snippet', 'source', 'document_type', 
                'news_desk', 'pub_date', 'section_name',
                'type_of_material', 'word_count', '_id', 
                'section_name', 'web_url']

date_now            =   datetime.datetime.now()

archive             = pd.DataFrame(columns=main_columns)
archive['main']     = []
archive['kicker']   = []

year_count          = 1
counter             = 0
file_counter        = 0

for file in os.listdir(dirlist_0):
    
    filename    = dirlist_0 + file
    f           = open(filename, 'r')
    r           = json.loads(f.read())

    num_articles= r['response']['meta']['hits']
    
    for artnum in range(0,len(r['response']['docs'])+1):
        for col in main_columns:
            try:
                archive.loc[counter,[col]]  = r['response']['docs'][artnum][col]
            except:
                pass
        try:
            archive.loc[counter,['main']]   = (r['response']['docs']
                                    [artnum]['headline']['main'])
        except:
            pass
        try:
            archive.loc[counter,['kicker']] = (r['response']['docs']
                                    [artnum]['headline']['kicker'])
        except:
            pass
        counter += 1
        
    print('Completed: ', year_count/(12*12)*100, '%')
    year_count += 1
    
    archive.to_csv(data_route + 
                   str(file_counter) + 
                   '_' + str(date_now) + '.csv')
    del archive
    archive             = pd.DataFrame(columns=main_columns)
    archive['main']     = []
    archive['kicker']   = []
    counter             = 0
    file_counter        += 1
