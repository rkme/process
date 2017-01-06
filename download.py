#
# This method will download all tweets from the specified country that we have
# in blob storage to the specified directory.
#
# Usage is: anaconda2/python2 download.py country_code outpath
#
# where country_code is the ISO-Alpha 3 code for the country you're looking for
# and outpath is the directory you want to save to
#

import sys
import os
from azure.storage.blob import baseblobservice as bsb

#
# This method will download the blobs from the specified country to the
# specified directory.
#


def downloadBlobs(blob_service, country, path):
    for blob in list(blob_service.list_blobs(country)):
        fp = path + blob.name
        if blob.name not in os.listdir(path):
            blob_service.get_blob_to_path(country, blob.name, fp)
    return os.listdir(path)

#
# This function gets account name and key from an external file.
# account_num is the ordered number of the account, starting from 0
#


def getAccount(account_num):
    account_path = "./accounts.txt"  # same directory as this program
    account_attr = 2  # This is how many lines are used for each account
    start = account_num * account_attr
    end = start + account_attr
    with open(account_path) as inFile:
        [name, key] = inFile.readlines()[start:end]  # readlines() is fine here
    return (name, key)


def main(country, account_num=0, outpath="./"):
    (name, key) = getAccount(account_num)
    bs = bsb.BaseBlobService(account_name=name, account_key=key)
    path = "./" + outpath + "/"
    d = downloadBlobs(bs, path)
    return d


main(*sys.argv[1:])
