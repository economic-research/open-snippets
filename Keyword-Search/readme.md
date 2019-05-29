# keyword_search: a module to perform very efficient keyword searches in Python
Efficiently implements keyword searches in python

Note: Please check **keyword_search_example.py** first.

keyword_search.py takes 5 arguments:
1. a dataframe with text (called **DF** for simplicity)
2. a column of the dataframe DF (called **COL** for simplicity)
3. a dataframe with two columns as keyword search inputs called **TERMS** (more of that in a bit)/1
4. optionally, an argument called **sprocessing** that specifies how the program breaks down a large dataframe into smaller ones for processing. This might affect performance, but does not affect the final result. Default is *sprocessing=10,000*.
5. If **mprocessing** is set to true the script will use multiprocessing to substitute words when specified. In certain circumstances this might actually hurt performance. Note that regardless of the value of this variable keyword_search.py will use multiprocessing to perform keyword searches whenever the length of **DF** is larger than **sprocessing**. Default is *mprocessing=False*.

Returns:

A new dataframe which is the join of **DF** with additional columns which are the list of terms for the keyword search as specified by **TERMS**. Lets call this dataframe **DF_OUT**. Let *a_ij* be the value of row *i* and column *j* from **DF_OUT**.  *a_ij* will be the number of times the term refered to in column *j* of DF_OUT appears in the *i'th* row of the dataframe **DF** and column **COL**: *DF[COL]*.

/1 The dataframe **TERMS** has 2 columns:
1. colssearch: single words in lowercase
2. newname: optionally, if one wants to search for "n-grams" (concepts with more than 1 word), the script is able to substitute the original word for the new word before doing the keyword search.
