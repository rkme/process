# What the hell is going on in here?
___

This repo is just versions of code that I've been using to explore the raw data from Twitter.

### process.py

Enriches RAW tweet data stored in local directory. Simply copies the raw data and stores the enriched copies in the target directory.

Currently enriched means: Added useful/calculated metrics about location, location type, admin info, local time, etc. (12/7/16)

download.py - script used to download the brazil blobs to our bra directory. Can be edited to download whatever you want from a 
given blob to a directory

extractTweets.py - Deprecated script used to extract country-specific tweets from quadrant files. Useful, but not used anymore.

probe.py - Simple script to print out blob information from the zika9372 account. Useful because it holds onto the account key 
for us. 

README.md - Super useful informative file. Slightly biased opinion.

### Dependencies

`pytzwhere` - Used in process.py. Allows us to find timezones based upon lat-lon.

`shapely` - Used to speed up tzwhere by a couple orders of magnitude. 

`azure-storage` - This is how we download the tweet files from Azure's Blob Storage. Account name and key required.

`redis-py` - Used in mobility.py as a key-value store and database. 
