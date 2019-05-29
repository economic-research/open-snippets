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
terms = pd.read_csv(keyword_search_input.csv',
                    dtype=str, sep=',')

# Import data of interest
rootdir     = '<my-rootdir>'
filename    = '<filename>'
df          = pd.read_csv(rootdir + filename,
        dtype=str, sep=',')
df.rename_axis('My Cool Index', inplace=True)

runfile('source/keyword_search/keyword_search.py')

# Generate bag of words model
start_time = time.time()
df_bow = keyword_search(df=df, column='transcripcion', terms=terms, 
                        sprocessing=10000, mprocessing=True)
elapsed_time = time.time() - start_time

print(elapsed_time)
