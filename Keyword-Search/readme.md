keyword_search.py
Efficiently implements keyword searches in python

Note:
Please check keyword_search_example.py first.

keyword_search.py takes 4 arguments:
1. a dataframe with text (called DF for simplicity)
2. a column of the dataframe DF (called COL for simplicity)
3. a dataframe with two columns as keyword search inputs (more of that in a bit)***
4. optionally, an argument called size_processing that specifies how the program breaks down large dataframe into smaller ones for processing.
   Might affect performance, but does not affect the final result.

Returns:
A dataframe with as many columns as rows in the input dataframe (see step 3). Lets call this dataframe DF_OUT. This dataframe has the same number of rows as DF. 
Let a_ij be the value of row i and column j from DF_OUT.  a_ij will be the number of times the term refered to in column j of DF_OUT
appears in the i'th row of the dataframe of step 1 and column specified in step 2: DF[COL].

***The dataframe provided in this step has 2 columns:
1. colssearch: single words in lowercase
2. newname: optionally, if one wants to search for "n-grams" (concepts with more than 1 word), the script is able to substitute the original word for the new word
before doing the keyword search. For example, suppose that the 4th row of this dataframe looks like this:

colssearch	newname
...		...
bright day	brightday

The scrip will first replace all instances of "bright day" with "brightday" and then perform a keyword search using the term brightday.
