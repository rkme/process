"""
This script will serve to calculate home admins for given users. Using the methodology described in %article we can attempt
to relate patterns of geolocated tweet locations for individual users with home locations for various admins
 """

import sys
import os
import json
import redis
import time
import datetime.datetime as dt
import scipy.sparse as sp
from itertools import islice
h = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

def getData(tweet):
	if tweet["admin_info"] and int(tweet["admin_info"]["admin_level"]) > 1:
		user

def readList(lst):
	for line in lst:
		j = json.loads(line)
		d = getData(j)

def readFile(inpath):
	print "Reading from " + inpath
	start = time.time()
	num_chunks = 1
	chunk_size = 1024
	with open(inpath, "r") as inFile:
		next_n_lines = list(islice(inFile, chunk_size))
		while next_n_lines:
			readList(next_n_lines)
			next_n_lines = list(islice(inFile, chunk_size))
			num_chunk += 1

def readDirectory(inpath):
	for file in os.listdir(inpath):
		if os.path.isfile(file):
			readFile(file)

def main(inpath):
	readDirectory(inpath)

