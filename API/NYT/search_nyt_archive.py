#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:47:03 2019

@author: jose_jurado_vadillo@brown.edu

Input:
    - A top directory
    - Search terms
Output:
    - A dataframe that is the subset of all files in top directory that 
    meet the search criteria
"""

import pandas as pd
import datetime, os, sys

params = pd.read_csv('{route-of-file-with-parameters}')

# Read user input
name_of_query   = params.loc[0,'name_of_query']

if int(params.loc[0,'to_lower']) == 1:
    to_lower = True
else:
    to_lower = False

data_route  = params.loc[0,'data_route']
write_route = params.loc[0,'write_route']

### Leave empty to ignore criteria. Give argument as list object.
lead_paragraph_contains_all = list(params['lead_paragraph_contains_all'].dropna())
lead_paragraph_contains_any = list(params['lead_paragraph_contains_any'].dropna())
snippet_contains_all        = list(params['snippet_contains_all'].dropna())
snippet_contains_any        = list(params['snippet_contains_any'].dropna())
source_is                   = list(params['source_is'].dropna())
source_is_any               = list(params['source_is_any'].dropna())
news_desk_is                = list(params['news_desk_is'].dropna())
news_desk_any               = list(params['news_desk_any'].dropna())
section_name_is             = list(params['section_name_is'].dropna())
section_name_is_any         = list(params['section_name_is_any'].dropna())
type_of_material_is         = list(params['type_of_material_is'].dropna())
type_of_material_any        = list(params['type_of_material_any'].dropna())
main_contains_all           = list(params['main_contains_all'].dropna())
main_contains_any           = list(params['main_contains_any'].dropna())

# Count nr of files
path, dirs, files   = next(os.walk(data_route))
file_count          = len(files)
del path, dirs, files, params

# Returns the name of a column from a NYT archive dataframe
def return_colname(varname):
    new_string      = varname.replace('_contains_all', '')
    new_string      = new_string.replace('_contains_any', '')
    new_string      = new_string.replace('_is_any', '')
    new_string      = new_string.replace('_is', '')
    return(new_string)

# Returns True if an option is in use, false otherwise
def option_selected_indicator(listname):
    length_ind = False
    for category in listname:
       if len(eval(category)) > 0:
           length_ind = True
    return(length_ind)

# Search criteria
list_criteria_contains_all = ['lead_paragraph_contains_all', 
                              'snippet_contains_all', 'source_is', 'news_desk_is', 
                              'section_name_is','type_of_material_is', 'main_contains_all']

list_criteria_contains_any      = ['lead_paragraph_contains_any',
                                   'snippet_contains_all', 'source_is_any',
                                   'news_desk_any',
                                   'section_name_is_any', 'type_of_material_any',
                                   'main_contains_any']

uses_all        = option_selected_indicator(list_criteria_contains_all)
uses_any        = option_selected_indicator(list_criteria_contains_any)

all_categories  = list_criteria_contains_all + list_criteria_contains_any

# Store results across many files
main_columns = ['lead_paragraph', 'snippet', 'source', 'document_type', 
                'news_desk', 'pub_date', 'section_name',
                'type_of_material', 'word_count', '_id', 
                'web_url', 'main', 'kicker']

date_now                    =   datetime.datetime.now()
archive_clean               = pd.DataFrame(columns=main_columns) # stores results across all files
file_counter                = 0

# Checks
    ## Check that user provided at least 1 input
if uses_all == False and uses_any == False:
    sys.exit('You need to provide at least 1 search parameter.')
    ## Check that user provided at least 1 file as input
if file_count == 0:
    sys.exit('You need to provide at least 1 file as input')

for file in os.listdir(data_route):
    results_index_all         = [] # Stores ALL index number of interest for given document
    results_index_any         = []
    ## Load data
    df              = pd.read_csv(data_route + file)
    ## Data cleaning
    df              = df.drop(columns=['Unnamed: 0', 'section_name.1']) # Due to bug, in build_archive.py column was duplicated
        
    ## Drop rows  with missing values in search criteria
    for category in all_categories:
        if len(eval(category)) > 0:
            colname     = return_colname(category)
            df          = df.dropna(subset=[colname])
            df[colname] = df[colname].astype(str)
            if to_lower:
                df[colname] = df[colname].astype(str).str.lower()
    
    ### Selects indexes that meet condition
        ## For ALL conditions
    j           = 1
    index_all   = {}
    index_any   = {}
    
    if uses_all:
        for category in list_criteria_contains_all:
            colname         = return_colname(category) # Map to NYT column name
            # Check that conditions isn't empty
            if len(eval(category)) > 0:
                # Iterate through criteria in category
                for criteria in eval(category):
                    # Find subset of DF that meets condition
                    df_temp         = df[df[colname].str.contains(criteria)] 
                    # Store index in index_all dict
                    index_all['cond{0}'.format(j)] = df_temp.index.tolist()
                    j   += 1
           
    j = 1
    
        ## For ANY condition
    if uses_any:
        for category in list_criteria_contains_any:
            colname         = return_colname(category) # Map to NYT column name
            # Check that conditions isn't empty
            if len(eval(category)) > 0:
                # Iterate through criteria in category
                for criteria in eval(category):
                    # Find subset of DF that meets condition
                    df_temp         = df[df[colname].str.contains(criteria)] 
                    # Store index in index_any dict
                    index_any['cond{0}'.format(j)] = df_temp.index.tolist()
                    j   += 1
         
    # Calculate intersections and unions of subsets -----------------------------------------
        ## ALL conditions must be met
    if uses_all:
                ### Case I: Exactly 1 condition
        if len(index_all) == 1:
            set_base    = set(index_all['cond1'])
                ### Case II: More than 1 condition
        elif len(index_all) > 1:
            for i in range(1,len(index_all)+1):
                if i == 1:
                    set_base  = set(index_all['cond1'])
                element_name    = 'cond' + str(i)
                set_base        =        set_base.intersection(set(index_all[element_name]))
        
                ### Store results in index
        results_index_all       = set_base
        del set_base
                   
        ## ANY conditions may be met
    if uses_any:
                ### Case I: Exactly 1 condition
        if len(index_any) == 1:
            set_base    = set(index_any['cond1'])
                ### Case II: More than 1 condition
        elif len(index_any) > 1:
            for i in range(1,len(index_any)+1):
                if i == 1:
                    set_base  = set(index_any['cond1'])
                element_name    = 'cond' + str(i)
                set_base        =        set_base.union(set(index_any[element_name]))
                
               ### Store results in index 
        results_index_any       = set_base
        del set_base
        
        ## Calculate the intersection of every ALL and ANY conditions
        if uses_all == True and uses_any == False:
            results_index = list(results_index_all)
        elif uses_all == True and uses_any == True:
            results_index = list(results_index_any.
                                 intersection(results_index_all))
        else:
            results_index = list(results_index_any)
    
    # Create DF subset
    df_final                    = df[df.index.isin(list(set(results_index)))]
    # END--Calculate intersections and unions of subsets ------------------------------------
        
    archive_clean  = archive_clean.append(df_final, sort=False)
    # Cleaning 
    del (category, colname, criteria, df, df_final, df_temp, file, 
         index_all, index_any, j, results_index, results_index_all,
         results_index_any)
    
    file_counter += 1
    print('Progress: ', file_counter/file_count*100, '%')

# Delete variables and temporary objects
del (all_categories, data_route, element_name, file_count, file_counter, 
     i, list_criteria_contains_all, list_criteria_contains_any, 
     main_columns, to_lower, uses_all, uses_any)

# Delete search criteria (user input)
del (lead_paragraph_contains_all,lead_paragraph_contains_any,
     snippet_contains_all, snippet_contains_any, source_is,
     source_is_any, news_desk_is, news_desk_any, section_name_is,
     section_name_is_any, type_of_material_is, type_of_material_any,
     main_contains_all, main_contains_any)

# Fix index of archive before saving to disk
archive_clean = archive_clean.reset_index(drop=True)

archive_clean.to_csv(write_route + 'query_' + name_of_query +
                     str(date_now) + '.csv')

# Final clean up
del (date_now, name_of_query, write_route)
