"""
This method will download all tweets from the specified country that we have in blob storage to the specified directory.

Usage is: anaconda2/python2 download.py country_code outpath

where country_code is the ISO-Alpha 3 code for the country you're looking for and outpath is the directory you want to save to
 """

import sys
import os
from azure.storage.blob import baseblobservice as bsb

#This method will download the blobs from the specified country to the specified directory.
def downloadBlobs(blob_service, country, path):
	for blob in list(blob_service.list_blobs(country)):
		fp = path+blob.name
		if blob.name not in os.listdir(path):
			blob_service.get_blob_to_path(container, blob.name, fp)
	return

def main(country, outpath="./"):

	bs = bsb.BaseBlobService(account_name = ACCOUNT_NAME, account_key = ACCOUNT_KEY)
	path = "./" + outpath + "/"
	downloadBlobs(bs, path)
	return os.listdir(path)

main(*sys.argv[1:])
