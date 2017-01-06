# This script reads through processed a provided directory of enriched tweets,
# gets location and time data for each user, and then uses that data to store
# movements from admin2 to admin2 over time. Note that any individual's
# movements are NOT stored permanently. A redis server is used to persistently
# store the hashed user IDs and their most recent movement and time of
# movement. All data sent to redis must be secured properly to protect user
# privacy.


import json
import os
import sys
from itertools import islice
import redis
# import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)
# m = redis.StrictRedis(host='localhost', port=6379, db=0)
m = dict()


def readList(lst):
    for line in lst:
        j = json.loads(line)
        d = getData(j)
        if d:
            (user_ID, admin_2, timestamp) = d
            key = "user:" + user_ID
            if r.hvals(key) and isRecent(r.hget(key, "timestamp"), timestamp):
                updateMatrix(r.hget(key, "admin_2"), admin_2, timestamp)
            r.hmset(key, {"admin_2": admin_2, "timestamp": timestamp})


def readFile(inpath):
    # print "Reading from " + inpath
    # start = time.time()
    num_chunks = 1
    chunk_size = 1024*1024
    with open(inpath, "r") as inFile:
        next_n_lines = list(islice(inFile, chunk_size))
        while next_n_lines:
            readList(next_n_lines)
            next_n_lines = list(islice(inFile, chunk_size))
            num_chunks += 1
    # print "Processed %d chunks in %s seconds" % \
    # (num_chunks, str(start - time.time()))
    return


def readDirectory(inpath):
    for file in os.listdir(inpath)[7:-1]:
        if os.path.isfile(inpath+file):
            readFile(inpath+file)


def updateMatrix(orig, dest, value):
    # if not mtx[(orig, dest)]:
    #     mtx[(orig, dest)] = []
    # mtx[(orig, dest)].append(value)
    key = str(orig) + ":" + str(dest)
    if key not in m:
        m[key] = []
    m[key].append(value)


def getData(tweet):
    if tweet["admin_info"] and int(tweet["admin_info"]["admin_level"]) > 1:
        user_ID = tweet["user"]["screen_name"]
        admin_2 = tweet["admin_info"]["ID_2"]
        timestamp = int(tweet["utc_time"])
        p = (user_ID, admin_2, timestamp)
        return p
    return None


def isRecent(then, now):
    DAY = 86400  # 1 day in POSIX time
    days = 3
    return (int(now) - int(then) < DAY*days)
    # Possibly look into catching "out of order" tweets from the same user.
    # I.e. if an earlier tweet from a user happens to be read by the program
    # before a later one. The tweets are mostly in order by time but k-sorted.


def main(inpath):
    try:
        # readFile(inpath)
        readDirectory(inpath)
        print m
        r.flushdb()
        return m
    except:
        print m
        r.flushdb()
        raise


main(sys.argv[1])
