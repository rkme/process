"""
This script serves to read through all tweets line by line and extract only those
with the specified country name and write them each to a specific country file.
These tweets should not be considered filly processed, they are simply sequestered
to the correct file to be more fully processed.
"""

import os
import json
import sys
import pytz
from datetime import datetime
from tzwhere import tzwhere
from itertools import islice
from pprint import pprint
import time

def extractFile(inpath, outpath = "brazil"):
	print "Reading from: " + inpath
	start = time.clock()
	with open(inpath, "rt") as inFile:
		next_n_lines = list(islice(inFile, 1024))
		num_chunks=1
		while next_n_lines:
			try:		
				readListToFile(next_n_lines, outpath)					
			except KeyboardInterrupt:
				raise
			next_n_lines = list(islice(inFile, 1024*1024))
			num_chunks += 1
			
	print "Processed %d lines in: %s seconds" % (num_chunks, str(time.clock() - start))

def readListToFile(lst, outpath):
	open_files = dict()
	for line in lst:
		try:
			j = json.loads(line)
			if j['place'] and j['place']['country'] == u'Brazil':
				country = "brazil"				
				date = getDate(j)
				year, month, day = date.year, '%02d' % date.month, '%02d' % date.day
				outFile = outpath + "/%s-%s-%s_%s.txt" % (year, month, day, country)
				if not outFile in open_files.keys():
					f = open(outFile, "a")
					open_files[f.name] = f
				open_files[outFile].write(json.dumps(j) + "\n")							
		except ValueError as e:
			print e
			print line 
			raise
		except KeyboardInterrupt:
			cleanup(open_files)
			raise
	cleanup(open_files)
	return

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
	

#Returns the most accurate possible coordinate location of the tweet along with 
#the type of coordinate that it grabbed in ([lat, long], type) format.
#Returns None if the location cannot be determined
def getCoordinates(tweet):
	if tweet["geo"]:
		return (tweet["geo"]["coordinates"], "Point")
	elif tweet["place"]:
		return (centroid(tweet["place"]["bounding_box"]["coordinates"][0]), "Centroid")
	else:
		return None

def centroid(bounding_box):
	lat = (bounding_box[0][1] + bounding_box[1][1])/2.0
	lon = (bounding_box[0][0] + bounding_box[2][0])/2.0
	return [lat, lon]

#If passed correct non-None coordinates and the date as a datetime.datetime object,
#This will return the correct utc offset for the given coords at the time of year
#in seconds. Otherwise, this will return None.
def utcOffset(coordinates, date):
	if coordinates:
		[lat, lon] = coordinates
		zone = pytz.timezone(tz.tzNameAt(lat, lon, forceTZ=True))
		return zone.localize(date.date()).strftime('%z')
#Apparently the above line causes an error when running the tzwhere module
	else:
		return None

def getLocalTime(utc_time, utc_offset):
	epoch_seconds = datetime.strftime(utc_time, "%s")
	print utc_offset
	epoch_seconds += utc_offset
	return datetime.fromtimestamp(float(epoch_seconds))

def getDate(tweet):
	time_str = tweet["created_at"]
	format = "%a %b %d %H:%M:%S +0000 %Y"
	dt = datetime.strptime(time_str, format)
	return dt

def loopFiles(inpath):
	regions = ['southwest']
	for file in os.listdir(inpath):
		if any(x in file for x in regions):
			extractFile(inpath+file)

def pathify(path):
	return "./" + path + "/"

def main(inpath):
	inpath = pathify(inpath)
	loopFiles(inpath)	

# tz = tzwhere.tzwhere(shapely=True, forceTZ=True)
main(sys.argv[1])
print "done!"

