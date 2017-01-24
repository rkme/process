# Flow

## Python

I use the Anaconda distribution of python 2 to run all of this. Extra
dependencies outside of that are listed in the readme.

## Data

### accounts.txt


First we need to download the blobs fom Azure. I store the account name and
account key in the text file accounts.txt. The file stores each account-key
pair as a two line pair. The first line is the account, the next line is the
key. Currently (1/6/17) there is information for two Azure accounts stored in
that file, so we have four lines. If you want to add another one, you just add
the two more lines.

**Tl;dr**: Put the account name and key for the Azure account you want to read from
in accounts.txt

### download.py

This program actually does the downloading from Azure. You give it the country
that you want to download from, the account you want from accounts.txt, and the
path to the directory you want the files saved to. The country name has to be
the name of the container in the account you're looking for. In the case of
tweets, you need the ISO-alpha 3 code (bra for Brazil, mex for Mexico, etc.).
In accounts.txt, the first account is 0, the second is 1, and so on. The default
used account is "tweets" which is account 0. The default save location is the
current directory you're in.

**Tl;dr**: python download.py country_code account_number target_path  
Saves all blobs from the country blob in the account to the target path.
Big files.

### process.py

This program enriches the tweets in the target directory and saves the enriched
versions in a different target directory. This adds fields for admin2, local
time, preferred location, and other useful metrics. **Note that this file does
not need to be run on the tweets that have been enriched in real time.** This
program is most useful if the blobs you have are straight from twitter, or
legacy data that never got enriched. Note that the field names and information
that this produces is not that same as the one Qusai's live code does. I will
try to match mine to his so that they conform. **Also note that this program
will essentially duplicate the data, preserving the old files. It does not
write in place.** The new files will have an identical name, so if you make the
target directory the same as the source directory, this will break itself.
Don't do that. This will be fixed in the new version I guess.

**Tl;dr**: python process.py source_dir target_dir  
The above command takes every blob in the source directory and writes an
enriched version to the target directory.

## Analysis

### mobility.py

This program reads through a directory containing tweets and constructs a redis
database matching "recent" movements from admin to admin by individual users.
Recent means that we only see movement if a user shows up more than once within
3 days, so that would have to be a fairly active user. The redis server needs
to be running in order for this to actually work properly, so make sure that's
going. Once the database has been constructed, it returns to you a dictionary
with admin-to-admin travel paths as the keys (adm_from:admin_to) and a list of
the timestamps in which the movement occurred (when the user showed at their
destination). I was flushing the user-movement database, but I had to keep
running my program over and over to get my mobility data so I keep it in order
to establish "home" location for each user. To retain privacy, I plan to hash
each user's ID so it does not match back to any individual. 

**Tl;dr**: python mobility.py source_dir  
The above command will create a redis database of usernames matched to a list
of location-timestamp pairs and a DOK sparse matrix of admin movement over
time.

Notes: Add structure: Adding keywords and actual commands as well as adding actual sources to methods and reasoning.
Bullet points: use steps and create a road map for usage.
