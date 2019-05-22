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
import multiprocessing, os

def bow_model(df, colskeep, size_processing):
    if len(df) <= size_processing:
        # Perform keyword search
        df_bow_final = get_bow(df, colskeep)
    else: # If size of dataframe is too big to perform in one step
        df_array        = np.array_split(df, round(len(df)/size_processing))
        df_bow_final    = pd.DataFrame()
        
        myargs = []
        for element in range(0, len(df_array)):
            tuple_temp = (df_array[element], colskeep, str(element)+'.csv')
            myargs.append(tuple_temp)
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()-2) as pool:
            pool.starmap(get_bow, myargs)
            pool.terminate()
        
        for element in range(0, len(df_array)):
            df_temp     = pd.read_csv(str(element) + '.csv')
            df_bow_final= (df_bow_final.
                           append(df_temp, ignore_index=True,sort=False))
            os.remove(str(element) + '.csv')
    
    # Fill nan with zeros
    df_bow_final.fillna(value=0, inplace=True)
    
    return df_bow_final

### IV substitute strings in dataframe (used when there's terms 
### that consist of 2 or more words, for instance)
from collections import Counter

def substitute_words(df, terms):
    df_substitute   = terms.dropna()
    # Prepare data for string substitutions
    old_terms       = list(df_substitute[df_substitute.columns[0]])
    new_terms       = list(df_substitute[df_substitute.columns[1]])
    
    df.replace(old_terms, new_terms, inplace=True,
                    regex=True)
    return df
    
### V Generate unique list of terms to search for
def clean_keywords(terms):
    # Index of columns where no substitution is specified
    is_nan = list(terms.dropna().index)
    # keywords that don't need to be substituted:
    df_1 = terms.drop(is_nan) 
    # keywords that need to be substituted:
    df_2 = terms.drop(list(Counter(terms.index) - Counter(is_nan)))
    
    terms_final = df_1[df_1.columns[0]]
    terms_final = terms_final.append(df_2[df_2.columns[1]])
    return list(set(terms_final))

### VI Implement steps I through V
def keyword_search(df, column, terms, size_processing=10000):
    # 1. substitute in df complex terms
    df[column] = substitute_words(df=df[column], terms=terms)
    
    # 2. Prepare list of keywords to search with
    colskeep = clean_keywords(terms=terms)
    
    # 3. Perform keyword search
    df_bow = bow_model(df=df[column], colskeep=colskeep, 
                       size_processing=size_processing)
    
    # 4. Drop and reset index
    df_bow.reset_index(inplace=True)
    
    # 5. Drop columns that are not necessary
    colsdrop    = list(Counter(df_bow.columns) - Counter(colskeep))
    df_bow      = df_bow.drop(colsdrop, axis=1)
    return df_bow