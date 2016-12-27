#This is a lazy way of making a histogram with hourly buckets for tweets
#based upon a SINGLE source file.
#
#Functions as a test process, NOT a final script

import matplotlib.pyplot as plt
import numpy as np
import os
import json
import time
from datetime import datetime
from itertools import islice
from pprint import pprint
import sys

SOURCE_PATH = "../process/data2/"

# LAZY_TIME_LIST = [0]*24

def getHour(epoch_seconds):
	return datetime.fromtimestamp(float(epoch_seconds)).hour

def loopFiles(inpath, outpath="data"):
        indir = os.listdir(inpath)
#        outdir = os.listdir(outpath)
	hist_bins = 24
	LAZY_CALENDAR = [[0]*hist_bins]*len(indir)
	d = 0
        for file in indir:
#                if file not in outdir:
                LAZY_CALENDAR[d] = readFile(inpath+file, outpath)
#                else:
#                    print file + " already exists in output directory."
        	d += 1
	return LAZY_CALENDAR

def joinLists(first, second):
	return [x + y for x,y in zip(first, second)]

def readFile(inpath, outpath="data"):
	start = time.time()
	chunk_size = 1024
	hist = [0]*24
	with open(inpath, "r") as inFile:
		next_n_lines = list(islice(inFile, chunk_size))
		num_lines = 0
		while next_n_lines:
			hist = joinLists(hist, countHours(next_n_lines))
			num_lines += len(next_n_lines)
			next_n_lines = list(islice(inFile, chunk_size))
	return hist

def countHours(lst):
	hours = [0]*24
	for t in lst:
		j = json.loads(t)
		hours[getHour(j["local_time"])] += 1
	return hours

def main(inpath = SOURCE_PATH):
	histogram = loopFiles(inpath)
	return histogram

print main()
