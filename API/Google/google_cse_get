#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produces number of hits for a given Google query for the list of US counties.
Uses Google CSE API.

Run in Ubuntu Linux 18.04 with kernel 4.15

Before running:
1. Create a Google CSE and copy its ID (CX)
2. Create a Google Cloud Account and obtain your API key.
3. Put your CSE ID and API key from steps 1 and 2 into separate CSV files.

@author: jose_jurado_vadillo@brown.edu
"""
import requests, csv, datetime, time
import pandas as pd

# ---------------------- User input --------------------------------
query_list         = '{my-query-list}'
# ---------------------- User input --------------------------------

#Import CSE keys
reader      = csv.reader(open('{my-key-csv}', 'r'))
cse_dict    = {}

for row in reader:
   k, v = row
   cse_dict[k] = v

#Import Google CSE ID's
reader          = csv.reader(open('{my-cse-list-csv}',
                                  'r'))
cse_id_dict     = {}

for row in reader:
   k, v = row
   cse_id_dict[k] = v

# Import data
counties_dat        = pd.read_csv('{my-list-of-counties-names}')
counties_list       = counties_dat['Geographic Name']

# ---------------- Parameters (immutable) ---------------------------------
cx                  = cse_id_dict['{my-prefered-cse-engine}']
key                 = cse_dict['{my-prefered-key}']                  # Google cloud API key
base_url            = 'https://www.googleapis.com/customsearch/v1'
date_now            = datetime.datetime.now()
# ---------------- Parameters (immutable) ---------------------------------

results = pd.DataFrame(columns=['num. results', 'URL', 'county', 'year'])

if len(query_list) > 0:
    for term in query_list:

        # file name
        my_title = ''
        for word in term.split():
            my_title = my_title + '_' + word

        my_title = my_title[1:]

        counter = 0

        for county in counties_list:
            for year in range(2015,2017):

                # Build query
                query_term      = county + ' ' + term
                sort_val        = 'date:r:' + str(year)   + '0101:' + str(year) + '1231'
                PARAMS          = {'q': query_term, 'cx': cx, 'key': key,
                                   'sort': sort_val}
                r               = requests.get(url = base_url, params = PARAMS)
                # Fill out parameters to table
                results.loc[counter,['URL']]            = r.url
                results.loc[counter,['county']]         = county
                results.loc[counter,['year']]           = year

                try:
                    data        = r.json()
                    nr_matches  = data['queries']['request'][0]['totalResults']

                    results.loc[counter,['num. results']]   = nr_matches
                except:
                    print('error for: ', county)
                    results.loc[counter,['num. results']]   = 99999999

                counter += 1
                print('Completed: ', counter/len(counties_list)*100/2,
                      '% for ', term)
                time.sleep(1)

        results.to_csv('{my-filename}' +
                       my_title + str(date_now) + '.csv')

else:
    counter = 0
    for county in counties_list:
        for year in range(2015,2017):
            # Build query
            sort_val        = 'date:r:' + str(year)   + '0101:' + str(year) + '1231'
            PARAMS          = {'q': county, 'cx': cx, 'key': key,
                               'sort':sort_val}

            r           = requests.get(url = base_url, params = PARAMS)
            # Fill out parameters to table
            results.loc[counter,['URL']]            = r.url
            results.loc[counter,['county']]         = county
            results.loc[counter,['year']]           = year
            try:

                data        = r.json()
                nr_matches  = data['queries']['request'][0]['totalResults']

                results.loc[counter,['num. results']]   = nr_matches
            except:
                print('error for: ', county)
                results.loc[counter,['num. results']]   = 99999999


            counter += 1
            print('Completed: ', counter/len(counties_list)*100/2)
            time.sleep(1)

    results.to_csv('{my-filename}' +
                   str(date_now) + '.csv')
