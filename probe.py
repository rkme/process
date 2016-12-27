"""
This is just various functions that explore the azure blob database
"""

import sys
import os
from azure.storage.blob.baseblobservice import BaseBlobService as bsb

bs = bsb(account_name = ACCOUNT_NAME, account_key = ACCOUNT_KEY)

def printBlobs(container, blob_service = bs):
	for blob in blob_service.list_blobs(container):
		print blob.name

def printContainers(j = 5):
	for blob in bs.list_containers():
		print blob.name

def main(arg):
	printBlobs(arg)

main(sys.argv[1])
