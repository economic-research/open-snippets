#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:09:57 2019

@author: jose_jurado_vadillo@brown.edu

Fully implements keyword searches
"""
### I Pre-text clenup
from nltk.tokenize import word_tokenize, sent_tokenize

def clean_text(text, colskeep):
    
    def tokenize_text(text):
        return [w for s in sent_tokenize(text) for w in word_tokenize(s)]
    
    def remove_words(text):
        tokens = [w for w in tokenize_text(text) if w in colskeep]
        return ' '.join(tokens)
        
    text = text.lower() # lowercase
    
    text = remove_words(text)
    return text

### II Tokenize and clean text
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

vectorizer  = CountVectorizer()

### Function that returns BoW model
def get_bow(df, colskeep, name):    
    # Substitute 'nan' with empty spaces in data
    df.fillna(value=' ', inplace=True)
    
    # Clean text: lowercase, keep only search for words 
    df = df.apply(clean_text, args=(colskeep,))
    
    # Tokenize
    features    = vectorizer.fit_transform(df)
    cols        = vectorizer.get_feature_names()
    
    # Dataframe representation of bow
    df_bow      = pd.DataFrame(features.todense(), 
                               columns=cols)            
    df_bow.to_csv(name)

### III Implement steps II (and hence I) for given parameters
import numpy as np
import multiprocessing, os, datetime

def bow_model(df, colskeep, sprocessing):
    date_now  = str(datetime.datetime.now())
    os.makedirs(date_now)
    
    if len(df) <= sprocessing:
        # Perform keyword search
        df_bow_final = get_bow(df, colskeep)
    else:
        '''
        If size of dataframe is too big to perform in one step split 
        dataframe into chunks and perform parallel computation of BOW dataframe.
        Store them temporarily in disk and append them
        '''
        df_array        = np.array_split(df, round(len(df)/sprocessing))
        df_bow_final    = pd.DataFrame()
        
        # Generate tuple with arguments
        myargs = []
        for element in range(0, len(df_array)):
            tuple_temp = (df_array[element], colskeep, date_now + 
                          '/' + str(element) + '.csv')
            myargs.append(tuple_temp)
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()-2) as pool:
            pool.starmap(get_bow, myargs)
            pool.terminate()
        
        for element in range(0, len(df_array)):
            df_temp         = pd.read_csv(date_now + '/' + 
                                          str(element) + '.csv')
            df_bow_final    = df_bow_final.append(df_temp, ignore_index=True, 
                                sort=False)
            os.remove(date_now + '/' + str(element) + '.csv')
        os.rmdir(date_now)
    # Fill nan with zeros
    df_bow_final.fillna(value=0, inplace=True)
    return df_bow_final

### IV substitute strings in dataframe (used when there's terms 
### that consist of 2 or more words, for instance)
from collections import Counter

# Auxiliary function that stores dataframes with string substitution
# Included as top level function to use multiprocessing (avoids pickle error)
def replaces(df, name, old_terms, new_terms):
    df = pd.DataFrame(df)
    df.replace(old_terms, new_terms, inplace=True,
                regex=True)
    df.to_csv(name)

def substitute_words(df, terms, mprocessing, sprocessing, column):
    df_substitute   = terms.dropna()
    
    # If there are terms to substitute df_substitute will have length >= 0
    if len(df_substitute) > 0:
        # Prepare data for string substitutions
        old_terms       = list(df_substitute[df_substitute.columns[0]])
        new_terms       = list(df_substitute[df_substitute.columns[1]])
        
        if not mprocessing:
            # If user didn't specify multiprocessing substitute words on entire df
            df.replace(old_terms, new_terms, inplace=True,
                            regex=True)
        else:
            # Otherwise, split df into chunks and perform parallel substitution
            df_processed    = pd.DataFrame()
            date_now        = str(datetime.datetime.now())
            os.makedirs(date_now)
            
            df_array  = np.array_split(df, round(len(df)/sprocessing))
            
            # Generate tuple with arguments
            myargs = []
            for element in range(0, len(df_array)):
                tuple_temp = (df_array[element], date_now + 
                              '/subs_words_' + str(element) + '.csv',
                              old_terms, new_terms)
                myargs.append(tuple_temp)
            
            with multiprocessing.Pool(processes=multiprocessing.cpu_count()-2) as pool:
                pool.starmap(replaces, myargs)
                pool.terminate()
             
            for element in range(0, len(df_array)):
                df_temp         = pd.read_csv(date_now + '/subs_words_' + 
                                         str(element) + '.csv')
                df_processed    =df_processed.append(df_temp, 
                                    ignore_index=True, sort=False)
                os.remove(date_now + '/subs_words_' + str(element) + '.csv')
            os.rmdir(date_now)
            df = df_processed[column]
    return df
    
### V Generate unique list of terms to search for
def clean_keywords(terms):
    # Make a copy and substitute empty cells with missing values
    terms_copy = terms.copy()
    terms_copy.replace('', np.nan, regex=True, inplace=True)
    
    # Index of columns where no substitution is specified
    no_subs = list(terms_copy[terms_copy.columns[1]].dropna().index)
    # keywords that NEED to be substituted:
    df_nosubs = terms_copy.drop(no_subs) 
    # keywords that DON'T NEED to be substituted:
    df_subs = terms_copy.drop(list(Counter(terms_copy.index) - Counter(no_subs)))
    
    terms_final = df_nosubs[df_nosubs.columns[0]]
    terms_final = terms_final.append(df_subs[df_subs.columns[1]])
    return list(set(terms_final.str.lower()))

### VI Implement steps I through V
def keyword_search(df, column, terms, sprocessing=10000, mprocessing=False):
    # 1. Basic error handling
    terms_copy = terms.copy()
    # Substitute empty value with missing to easily identify them
    terms_copy.replace('', np.nan, regex=True, inplace=True)
    
    if len(df) == 0:
        print('DataFrame has no rows')
        raise SystemExit
    if (len(terms) == 0) | (len(terms.columns) != 2):
        print('Terms dataframe should have one row or more, and 2 columns')
        raise SystemExit
    if not column in df.columns:
        print('Please provide a valid column reference for dataframe')
        raise SystemExit
    if terms[terms_copy.columns[0]].isnull().values.any():
        print('Terms dataframe should not have nan/empty values in the first column')
        raise SystemExit
        
    # 2. Keep copy of original dataframe
    df_original         = df.copy()
    colnames_original   = list(df.columns)
    
    # 3. substitute in df complex terms
    df[column] = substitute_words(df=df[column], terms=terms, 
      mprocessing=mprocessing, sprocessing=sprocessing, column=column)
    
    # 4. Prepare list of keywords to search with.
    # Lowercase search terms when appropriate
    terms[terms.columns[1]] = terms[terms.columns[1]].str.lower()
    colskeep = clean_keywords(terms=terms)
    
    # 5. Perform keyword search
    df_bow = bow_model(df=df[column], colskeep=colskeep, 
                       sprocessing=sprocessing)
    df_bow.set_index(df_original.index, inplace=True)
    
    # 6. Join data to oiginal dataframe
    df_joined = pd.concat([df_original, df_bow], axis=1, 
                          ignore_index=False, sort=False)
        
    # 7. Drop columns that are not necessary
    colsdrop    = list(Counter(df_joined.columns) - 
                       Counter(colskeep + colnames_original))
    df_joined.drop(colsdrop, axis=1, inplace=True)
    return df_joined