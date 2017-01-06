# This method enriches all of the raw tweets files stored in a source directory
# and stores the enriched copies in a target directory. This just adds the
# fields for "most specific" location, the local time, and admin_info, from
# Mike's API.
#
# Usage is: anaconda2/python2 process.py source_directory target_directory
#
# Note that this will take 20-30s to load up before running through because the
# tzwhere module is not friendly. Once it loads, it should run fine. The
# enrichment may cause duplication of information if the tweets have been
# enriched partially before being stored on blob-storage, but I'm keeping it
# that way until we finalize where and when we enrich the tweets.

import os
import json
import sys
import pytz
from datetime import datetime
from tzwhere import tzwhere
from itertools import islice, chain
import time
import requests


def readFile(inpath, outpath):
    print "Reading from: " + inpath
    start = time.time()
    with open(inpath, "rt") as inFile:
        next_n_lines = list(islice(inFile, 1024*128))
        num_lines = 0
        prefix_len = inFile.name.rfind("/") + 1
        outfile = pathify(outpath) + inFile.name[prefix_len:]
        while next_n_lines:
            readListToFile(next_n_lines, outfile)
            num_lines += len(next_n_lines)
            next_n_lines = list(islice(inFile, 1024*128))
    print "Processed %d lines in: %s seconds" % \
          (num_lines, str(time.time() - start))
    return


#####
# Shamelessly stolen from SE:
# https://stackoverflow.com/questions/1335392/iteration-over-list-slices
#

###
# Yields items from an iterator in iterable chunks.
#


def ichunked(seq, chunksize):
    it = iter(seq)
    while True:
        yield chain([it.next()], islice(it, chunksize-1))


###
# Yields items from an iterator in list chunks
#


def chunked(seq, chunksize):
    for chunk in ichunked(seq, chunksize):
        yield list(chunk)


#
# /stolen
######

###
# Evaluates whether or not the coordinates provided in the tweet are specific
# enough to meet the requirements for what we're analyzing. In this case we are
# looking to see if we can find admin2 from the coordinates, so if the bounding
# box is too large, we don't have a reliable answer and must throw it out.
#


def specificEnough(tweet):
    acceptable = ["exact", "pnt", "neighborhood", "city"]
    return tweet["coords_level"] in acceptable


def readListToFile(lst, outpath):
    with open(outpath, "a") as outFile:
        for group in chunked(lst, 128):
            tweets = []
            coordinates = []
            s = ""
            for tweet in group:
                try:
                    j = json.loads(tweet)
                    t = processTweet(j)
                    if specificEnough(t):
                        coordinates.append(t["coords"])
                        tweets.append(t)
                    else:
                        t["admin_info"] = None
                        outFile.write(json.dumps(t) + "\n")
                except ValueError as e:
                    if tweet == '\n':
                        print "Newline character found."
                        continue
                    else:
                        raise e
            s += ",".join((",".join(str(y) for y in x) for x in coordinates))
            g = httpGet(API_URL+s)
            ##########
            for x in xrange(len(g)):
                if g[x]:
                    tweets[x]["admin_info"] = g[x]
                else:
                    tweets[x]["admin_info"] = None
                outFile.write(str(json.dumps(tweets[x])) + "\n")
    return


def httpGet(url):
    try:
        # s = requests.Session()  # Relic. Possibly still useful
        # a = requests.adapters.HTTPAdapter(max_retries=10)
        # s.mount("http://", a)
        return requests.get(url).json()
    except requests.exceptions.ConnectionError as e:
        print url
        raise
    except ValueError as e:
        print e
        print url
        return []


def processTweet(tweet):
    c = getCoordinates(tweet)  # Returns tuple with three elements or None
    date = getDate(tweet)
    date_str = str(date)
    local_time, local_time_str, utc_offset = None, None, None
    if c:
        (tweet["coords"], tweet["coords_type"], tweet["coords_level"]) = c
        utc_offset = utcOffset(tweet["coords"], date)
        ld = getLocalDate(date, utc_offset)
        # if not ld:
        # print "c: %s, date: %s, utc_offset: %s, local_date: %s" % (str(c),\
        # date_str, str(utc_offset), str(ld))
        local_time = datetime.strftime(ld, "%s")
        local_time_str = str(local_time)
    tweet["utc_time"] = datetime.strftime(date, "%s")
    tweet["utc_time_str"] = date_str
    tweet["local_time"] = local_time
    tweet["local_time_str"] = local_time_str
    tweet["tz_offset"] = utc_offset     # called this because tweets already
    return tweet                        # have a field called utc_offset


###
# Lazy function to close open files. Won't stop due to keyboard interruption.


def cleanup(files):
    for key in files:
        try:
            files[key].close()
        except KeyboardInterrupt:
            print "Cleaning up!"
            files[key].close()
        except Exception as e:
            print e
            continue
    return


###
# Returns the most accurate possible coordinate location of the tweet along
# with the type of coordinate that it grabbed in ([lat, lon], type) format.
# Returns None if the location cannot be determined


def getCoordinates(tweet):
    if tweet["geo"]:
        return (tweet["geo"]["coordinates"], "Point", "exact")
    elif tweet["place"]:
        return (centroid(tweet["place"]["bounding_box"]["coordinates"][0]),
                "Centroid", tweet["place"]["place_type"])
    else:
        return None


def centroid(bounding_box):
    lat1 = bounding_box[0][1]
    lon1 = bounding_box[0][0]
    lat2 = bounding_box[3][1]
    lon2 = bounding_box[3][0]
    lat = float(lat1 + lat2)/2.0
    lon = float(lon1 + lon2)/2.0
    return [lat, lon]


###
# If passed correct non-None coordinates and the utc date as a
# datetime.datetime object. This will return the correct utc offset for the
# given coords at the time of year in seconds, if the tzwhere module can find
# the timezone. Otherwise, this will return None.
#


def utcOffset(coordinates, date):
    if coordinates:
        [lat, lon] = coordinates
        tz_name = tz.tzNameAt(lat, lon, forceTZ=True)
        if tz_name:
            zone = pytz.timezone(tz_name)
#           zone = pytz.timezone(tz.tzNameAt(lat, lon))
            l = (float(zone.localize(date).strftime("%z"))/100.) * 60 * 60
#           if l ==  0.0:
#           print "zone: %s, coordinates: %s, date: $s, localize: %s" % \
#           (str(x) for x in (zone, coordinates, date, zone.localize(date))
            return l
    return None


###
# Returns the local time as a datetime object if passed the utc_time (as a
# datetime object) and the utc_offset in seconds. If the utc_offset passed to
# it is None, will return None


def getLocalDate(utc_time, utc_offset):
    if utc_offset is not None:
        epoch_seconds = float(datetime.strftime(utc_time, "%s"))
        epoch_seconds += utc_offset
        return datetime.fromtimestamp(epoch_seconds)
    else:
        return None


def getDate(tweet):
    time_str = tweet["created_at"]
    format = "%a %b %d %H:%M:%S +0000 %Y"
    dt = datetime.strptime(time_str, format)
    return dt


def loopFiles(inpath, outpath):
    indir = os.listdir(inpath)
    outdir = os.listdir(outpath)
    for file in indir:
        if ".txt" in file and file not in outdir:
            readFile(inpath+file, outpath)
        else:
            print file + " already exists in output directory."
    return


def pathify(path):
    return "./" + path + "/"


def main(inpath, outpath):
    inpath = pathify(inpath)
    outpath = pathify(outpath)
    loopFiles(inpath, outpath)


API_URL = "http://40.114.15.133:8080/api/coords/"
tz = tzwhere.tzwhere(shapely=True, forceTZ=True)
# tz = tzwhere.tzwhere() #Faster, less accurate. Will have to change forceTZ to
# False from the tz.tzNameAt() call in utcOffset().
main(*sys.argv[1:])
