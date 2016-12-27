# What the hell is going on in here?
___


### analyze Folder

Currently contains a test function used to analyze enriched tweet files



### bra Folder

Contains all RAW legacy data (separated by geographical quadrants from each crawler). Read more into how the crawlers obtain 
their data to understand more about what these files contain.


### mex Folder
Contains files


### brazil Folder

Contains files that represent all tweets from brazil in the raw data, separated by their respective UTC date. Each tweet from 
the raw files is processed individually, so it doesn't matter if a tweet from one day happens to be in the raw file for another 
day, it will be written to the proper file. All the quadrants are processed into a single file.

### extract Folder

Contains deprecated extract scripts as well as the most recent functioning version, extractTweets.py. I will make sure to 
distinguish this process from the others well so that it shouldn't be confused. Holding on to the deprecated versions so far 
because IIRC they do some other things that may be useful.

### grepBRA Folder

Contains two files of tweets grepped from the raw data directory (bra/) that contained the sequence '"country": "Brazil"' 
(which should all be tweets that have location data that we can track to brazil). This made it easier to process because grep 
is way faster than my current python scripts. The two files are northwest and southwest based upon which quadrant files they 
were reading from. The southwest file is much larger.

### greppedBra Folder

Contains nothing at the moment. Used to contain cut down versions of the grepped files but that step became unnecessary.

### process Folder

Contains the processing script as well as a directory containing enriched tweets organized by UTC date.

Currently enriched means: Added useful/calculated metrics about location, location type, admin info, local time, etc. (12/7/16)

### Other files:

download.py - script used to download the brazil blobs to our bra directory. Can be edited to download whatever you want from a 
given blob to a directory

extract4.py - Probably a copy of another file. Going to make sure of this before deleting

fields.txt - Parameters for a perl script IIRC. Not super sure about this but don't delete this yet.

probe.py - Simple script to print out blob information from the zika9372 account. Useful because it holds onto the account key 
for us. 

info.md - Super useful informative file. Slightly biased opinion.
