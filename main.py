# Enter password for MySQL RDS as first command line argument

from datetime import datetime

import sys
import requests
import urllib.request
import time
import json
import pymysql

# RDS
RDS_HOST = 'pm-mysqldb.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
RDS_PORT = 3306
RDS_USER = 'admin'
RDS_DB = 'pricing'

# RDS PASSWORD
if len(sys.argv) == 2:
    RDS_PW = str(sys.argv[1])
else:
    print("Usage: Enter password for MySQL server as first command line argument")
    sys.exit(1)

# RDS connection
conn = pymysql.connect( RDS_HOST,
                        user=RDS_USER,
                        port=RDS_PORT,
                        passwd=RDS_PW,
                        db=RDS_DB)
cur = conn.cursor()

# JSON data file
json_data = 'jsondata.json'

# Initialize data structures for json data
responses = []
responseIndex = 0
numberOfItemsPerStore = 20

# Hashmaps of access keys and store info
accessKeyDict = {'itemAccessKeys': [], 'priceAccessKeys': [], 'unitAccessKeys': [], 'isOnSaleAccessKeys': [], 'salePriceAccessKeys': []}
storeInfo = {'storeNames': [], 'storeZipCodes': []}

# Load JSON containing URLs of APIs of grocery stores
with open(json_data, 'r') as data_f:
    data_dict = json.load(data_f)

# Organize API URLs
for apiurl in data_dict['apiURL']:
    responses.append('')
    responses[responseIndex] = requests.get(apiurl['url'])
    responses[responseIndex].raise_for_status()
    responseIndex += 1
    storeInfo['storeNames'].append(apiurl['name'])
    storeInfo['storeZipCodes'].append(apiurl['zipCode'])
    accessKeyDict['itemAccessKeys'].append(apiurl['itemAccessKeys'])
    accessKeyDict['priceAccessKeys'].append(apiurl['priceAccessKeys'])
    accessKeyDict['unitAccessKeys'].append(apiurl['unitAccessKeys'])
    if apiurl['saleAccessKeysExist']:
        accessKeyDict['isOnSaleAccessKeys'].append(apiurl['saleAccessKeysExist']['isOnSaleAccessKeys'])
        accessKeyDict['salePriceAccessKeys'].append(apiurl['saleAccessKeysExist']['salePriceAccessKeys'])
    else:
        accessKeyDict['isOnSaleAccessKeys'].append(None)
        accessKeyDict['salePriceAccessKeys'].append(None)

# Set number of stores
numberOfStores = responseIndex

# Get current date and time
def getCurrentDateAndTime():
    now = datetime.now()
    # dd/mm/YY HH:MM:SS
    return now.strftime("%m/%d/%Y %H:%M:%S")

# Get access keys for a JSON
def getKeys(data, keys, apiItemIndex):
    
    '''
    # Temporary fix for APIs missing data (i.e. Target units), fix ASAP
    if keys[0] == "N/A":
        return keys[1]
    '''
    
    for key in keys:
        if key == "apiItemIndex":
            key = apiItemIndex
        data = data[key]
#       print(key)
    return data

# Not working as of 11/17/19
def checkItemSale(accessKeyDict, storeindex, itemcount):
    if accessKeyDict['isOnSaleAccessKeys'] is not None:
        if getKeys(responses[storeindex].json(), accessKeyDict['isOnSaleAccessKeys'][storeindex], itemcount) is not None:
            return getKeys(responses[storeindex].json(), accessKeyDict['salePriceAccessKeys'][storeindex], itemcount)
    return getKeys(responses[storeindex].json(), accessKeyDict['priceAccessKeys'][storeindex], itemcount)

# Add items and prices
mysql_insert_groceries_query = """INSERT INTO groceries (item, price, unit, store, zipcode, price_date)
                        VALUES (%s, %s, %s, %s, %s, %s) """

for itemcount in range(numberOfItemsPerStore):
    for storeindex in range(numberOfStores):
        itemToAppend = getKeys(responses[storeindex].json(), accessKeyDict['itemAccessKeys'][storeindex], itemcount)
        unitsToAppend = getKeys(responses[storeindex].json(), accessKeyDict['unitAccessKeys'][storeindex], itemcount)
#        priceToAppend = checkItemSale(accessKeyDict, storeindex, itemcount)
        priceToAppend = getKeys(responses[storeindex].json(), accessKeyDict['priceAccessKeys'][storeindex], itemcount)
        storeToAppend = storeInfo['storeZipCodes'][storeindex]
        insertTuple = (itemToAppend, priceToAppend, unitsToAppend, storeInfo['storeNames'][storeindex], storeToAppend, getCurrentDateAndTime())
        cur.execute(mysql_insert_groceries_query, insertTuple)

conn.commit()

cur.close()

conn.close()

print("Script complete")
