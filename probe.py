#
# This is just various functions that explore the azure blob database
#

import sys
from azure.storage.blob.baseblobservice import BaseBlobService as bsb

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


def printBlobs(container, blob_svc):
    for blob in blob_svc.list_blobs(container):
        print blob.name


def printContainers(blob_svc):
    for blob in blob_svc.list_containers():
        print blob.name


def main(category, cont_name="bra", account_num=0):
    (name, key) = getAccount(account_num)
    bs = bsb(account_name=name, account_key=key)
    if category.upper == "B":
        print "All blobs in account %s, container %s:" % (name, cont_name)
        printBlobs(cont_name, bs)
    elif category.upper == "C":
        print "All containers in account %s:" % name
        printContainers(bs)
    else:
        print "Invalid category input. Enter B or C to list blobs or \
        categories, respectively. If listing blobs, also enter name of blob"


main(sys.argv[1:])
