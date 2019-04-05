Recommended (uses the NYT Archive API):

-* nyt_archive.py: uses the NYT Archive API to search for the metadata of all articles of the NYT and stores it in JSON format
-* build_archive.py: uses as input the JSON files from nyt_archive.py to create tables with the NYT entire archive 
-* search_nyt_archive.py: provided a list of words to be searched, as well as a list of excluded terms, it provides a table with
	the list of NYT articles of interest. It uses the collection of articles collected from the NYT Archive API by build_archive.py
	so in that sense it includes all NYT articles of interest. 

Deprecated (uses NYT Archive API):

-* nyt_article_search.py: for given parameters finds articles of interest from the NYT. It uses the NYT Search API,
	INSTEAD OF the Archive API.

See: https://developer.nytimes.com/apis
