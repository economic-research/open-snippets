#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produces number of hits for a given Google query
Uses Google CSE API

Created on Wed Dec 26 15:41:09 2018

@author: jose_jurado_vadillo@brown.edu
"""
import requests, csv

#Import CSE keys
reader      = csv.reader(open('keys.csv', 'r'))
cse_dict    = {}

for row in reader:
   k, v = row
   cse_dict[k] = v

#Import Google CSE ID's
reader          = csv.reader(open('CSE_engines.csv', 'r'))
cse_id_dict     = {}

for row in reader:
   k, v = row
   cse_id_dict[k] = v

# ---------------- User Input ---------------------------------------------
search_query        = 'beautiful dogs'
cx                  = cse_id_dict['my-search-engine']
start_val           = 91
# ---------------- User Input ---------------------------------------------

# ---------------- Parameters (immutable) ---------------------------------
key                 = cse_dict['my-preferred-key']                  # Google cloud API key
base_url            = 'https://www.googleapis.com/customsearch/v1'
numval              = 10
PARAMS              = {'q': search_query, 'cx': cx, 'key': key,
                       'start': start_val, 'num': numval}
# ---------------- Parameters (immutable) ---------------------------------

# Parse information
r       = requests.get(url = base_url, params = PARAMS) 
data    = r.json() 

# Get nr. of matches
nr_matches = data['queries']['request'][0]['totalResults']
print('Nr. of matches is: ', nr_matches)

items = data['items']
