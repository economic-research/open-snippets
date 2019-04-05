#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:00:20 2019

@author: jose_jurado_vadillo@brown.edu

Imports json objects from google_cse_full_parser.py and appends them
"""

import json, os
import pandas as pd

rootdir     = './queries/'
data_folder = os.path.abspath(rootdir)

colnames = ['displayLink', 'formattedUrl', 'htmlFormattedUrl', 'htmlSnippet',
       'htmlTitle', 'kind', 'link', 'pagemap', 'snippet', 'title',
       'filename']

dupscols = ['formattedUrl', 'htmlFormattedUrl', 'snippet',
            'title', 'window']

df_full    = pd.DataFrame(columns=colnames)
df_matches = pd.DataFrame(columns=['outlet', 'matches', 'page9'])
j = -1
original_rows = 0 

for subdir in next(os.walk(data_folder))[1]:
    print('Parsing outlet ', subdir)
    
    j += 1
    isnine = 999999
    
    df          = pd.DataFrame(columns=colnames)
    subfolder   = data_folder + '/' + str(subdir)
    
    for file in os.listdir(subfolder):
        filename = subfolder + '/' + file
                    
        with open(filename) as f:
            data  = json.load(f)
        
        # In rare ocassions Google returns a back-end error
        try:
            if int(data['searchInformation']['totalResults']) > 0:
                df_temp                 = pd.DataFrame(data['items'])
                df_temp['filename']     = filename
                df                      = df.append(df_temp, sort=False)
        except:
            pass
    
    if len(df) > 0:
        df[['term','window','page','today']] = (df['filename'].
                          str.split('_',expand=True))
        df['outlet']    = subdir
        df['term']      = (df['term'].
              replace(regex=True,to_replace=subfolder + '/',value=''))
        df['window']    = (df['window'].
              replace(regex=True,to_replace='date:r:',value=''))
        
        df.sort_values(by=['window'],axis=0, inplace=True)
        df.to_csv(rootdir + subdir + '.csv')
        original_rows += len(df)
        
        df_nodups = df.drop_duplicates(subset=dupscols, keep='first')
        df_nodups.reset_index(drop=True, inplace=True)
        df_nodups.to_csv(rootdir + subdir + '_nodups.csv')
        
        df_full = df_full.append(df_nodups, sort=False)
        isnine  = len(df_nodups[df_nodups['page'].astype(int) == 9])
    else:
        df_nodups = df
        isnine    = 0
    df_matches.loc[j]  = [subdir, len(df_nodups), 
                  isnine]

df_matches = df_matches.sort_values(by=['outlet'], axis=0)
df_matches.reset_index(drop=True, inplace=True)
df_matches.to_csv(rootdir + 'matches_dir.csv')

df_full.reset_index(drop=True, inplace=True)
df_full.to_csv(rootdir + 'articles_cse.csv')

print(df_matches)
print('Total matches ', df_matches['matches'].sum())
print('Duplicates: ', 1 - len(df_full)/original_rows, '%')
