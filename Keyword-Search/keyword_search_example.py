#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:17:30 2019

@author: jose_jurado_vadillo@brown.edu

keyword search example
"""
import pandas as pd
import time

# Import keywords (parameters to parse)
terms = pd.read_csv('./source/Keyword-search/keyword_search_input.csv',
                    dtype=str, sep=',')

# Import data of interest
rootdir     = '<my-data-directory>'
df = pd.read_csv(rootdir + 'data.csv',
        dtype=str, sep=',')

df.reset_index(inplace=True)
df.drop(['index'], axis=1, inplace=True)

runfile('source/Keyword-Search/full_keyword_searches.py')

# Generate bag of words model
start_time = time.time()
df_bow = keyword_search(df=df, column='snippet', terms=terms, size_processing=10000)
elapsed_time = time.time() - start_time

print(elapsed_time)

# Drop indexes before joining data

# Join data
df_final = pd.concat([df, df_bow], axis=1, ignore_index=False, sort=False)
