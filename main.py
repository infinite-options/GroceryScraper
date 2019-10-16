# Enter password for MySQL RDS as first command line argument

'''
from flask import Flask, render_template
'''
from datetime import datetime

import sys
import requests
import urllib.request
import time
import json
import pymysql

'''
app = Flask(__name__)
'''

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
storenames = []
itemAccessKeys = []
priceAccessKeys = []
unitAccessKeys = []
storeZipCodes = []
index = 0
numberOfStores = 5
numberOfItemsPerStore = 20

'''
items_generic = []
organic_arr = []
'''

# Load JSON containing URLs of APIs of grocery stores
with open(json_data, 'r') as data_f:
    data_dict = json.load(data_f)

# Organize API URLs
for apiurl in data_dict['apiURL']:
    responses.append('')
    responses[index] = requests.get(apiurl['url'])
    responses[index].raise_for_status()
    storenames.append(apiurl['name'])
    itemAccessKeys.append(apiurl['itemAccessKeys'])
    priceAccessKeys.append(apiurl['priceAccessKeys'])
    unitAccessKeys.append(apiurl['unitAccessKeys'])
    storeZipCodes.append(apiurl['zipCode'])
    index += 1

# Deprecated generic item word array
'''
# Generic item list from JSON
for genstore in data_dict['genericItems']:
    items_generic.append(genstore['name'])
    organic_arr.append(genstore['organic'])
'''

# Deprecated arrays for printing to web endpoint
'''
# Initialize items and prices lists
items = []
prices = []
stores = []
units = []
'''

# Get current date and time
def getCurrentDateAndTime():
    now = datetime.now()
    # dd/mm/YY HH:MM:SS
    return now.strftime("%m/%d/%Y %H:%M:%S")

'''
# Append zipcode to storename
def appendZipCodeToStoreName(storenames, storeZipCodes):
    for index, zipcode in enumerate(storeZipCodes):
        storenames[index] = storenames[index]+"("+str(zipcode)+")"
    return storenames

# Header row for pivot table on website
headerRow = ['Item', 'Organic?']
headerRow.extend(storenames)
# headerRow.extend(appendZipCodeToStoreName(storenames, storeZipCodes))

# Convert to price per pound
def convertPricePerUnits(basePrice, baseUnit, numberOfUnits):
    retPrice = float(basePrice)
    if baseUnit == "OUNCE":
        retPrice *= 16
    return retPrice/numberOfUnits

# Convert units
def convertUnits(baseUnits):
    retUnits = baseUnits
    if baseUnits == "OUNCE":
        retUnits = "POUND"
    if baseUnits == "LB":
        retUnits = "POUND"
    return retUnits

# Return quantity of units
def unitQuantity(productName, baseUnits):
    wordsArray = productName.lower().split()
    if baseUnits in wordsArray[1:]:
        return wordsArray[wordsArray.index(baseUnits)-1]

# Return boolean, organic check, argument takes binary value, returns string
def isOrganicReturnString(value):
    if value == 1:
        return "yes"
    elif value == 0:
        return "no"
    else:
        return "error: n/a"

# Return boolean, organic check, argument takes an array of words, returns binary
def isOrganic(productNameArr):
    if "organic" in productNameArr:
        return 1
    else:
        return 0
'''


# Old pivot sort (runs in O(n^3) :/)
'''
# EXACT WORD CHECK (does not yet check tomato vs tomatoes)
# Solves in inefficient time
# NEED COLUMN FOR UNITS
def pivotSort(items_generic, items, prices, stores, storenames, units, itemcount):
    retTable = []
    genericItemIndex = 0
    for item in items_generic:
        itemGenArr = item.lower().split()
        tableRow = [item, isOrganicReturnString(organic_arr[genericItemIndex])]
        for store in storenames:
            itemFound = 0
            for count in range(itemcount):
                itemArr = items[count].lower().split()
                if all(word in itemArr for word in itemGenArr) and (stores[count] == store) and (isOrganic(itemArr) == organic_arr[genericItemIndex]) and (itemFound == 0):
                    tableRow.append(prices[count])
                    # Debugging
                    #print(items[count]," is ",prices[count]," at ",stores[count])
                    itemFound = 1
            if itemFound == 0:
                tableRow.append("none")
                # Debugging
                #print(item," not found at ",store)
        retTable.append(tableRow)
        genericItemIndex += 1
    return retTable
'''

'''
# Generic Item Name Check, return boolean
#def isGeneric(itemArr, itemGenArr):
#    for words in itemArr:
'''

# Get access keys for a JSON
def getKeys(data, keys, apiItemIndex):
    # Temporary fix for APIs missing data (i.e. Target units), fix ASAP
    if keys[0] == "N/A":
        return keys[1]
    for key in keys:
        if key == "apiItemIndex":
            key = apiItemIndex
        data = data[key]
#       print(key)
    return data

# Add items and prices
# Fixed: NEEDS SIGNIFICANT CLEANUP - CURRENTLY MANUALLY PARSING APIS
# Fixed: WRITE FUNCTION THAT AUTOMATES
# Fixed: INCLUDE DIRECTORY OF KEYS TO PARSE FROM IN THE JSON ITSELF
#def insertGroceriesToTableQuery(itemcount, numberOfStores):
mysql_insert_groceries_query = """INSERT INTO groceries (item, price, unit, store, zipcode, price_date)
                        VALUES (%s, %s, %s, %s, %s, %s) """

for itemcount in range(numberOfItemsPerStore):
    for storeindex in range(numberOfStores):
        itemToAppend = getKeys(responses[storeindex].json(), itemAccessKeys[storeindex], itemcount)
        unitsToAppend = getKeys(responses[storeindex].json(), unitAccessKeys[storeindex], itemcount)
        priceToAppend = getKeys(responses[storeindex].json(), priceAccessKeys[storeindex], itemcount)
        insertTuple = (itemToAppend, priceToAppend, unitsToAppend, storenames[storeindex], storeZipCodes[storeindex], getCurrentDateAndTime())
        cur.execute(mysql_insert_groceries_query, insertTuple)
'''        items.append(itemToAppend)
        prices.append(priceToAppend)
        units.append(unitsToAppend)
        stores.append(storenames[storeindex])
'''
conn.commit()

'''
#   prices.append(convertPricePerUnits(responses[0].json()['list'][itemcount]['store']['price'],responses[0].json()['list'][itemcount]['store']['retail_unit'],1))
#   stores.append('Whole Foods')
#   units.append(convertUnits(responses[0].json()['list'][itemcount]['store']['retail_unit']))
#   items.append(responses[1].json()['search_response']['items']['Item'][itemcount]['title'])
#   prices.append(convertPricePerUnits(responses[1].json()['search_response']['items']['Item'][itemcount]['price']['current_retail'],'POUND',1)) # POUND IS NOT CORRECT, REPLACE WITH A FUNCTION THAT CAN READ/DETECT UNIT FROM ITEM DESCRIPTION (temporarily using pound to keep this functional)
#   stores.append('Target')
#   units.append('n/a')
#   items.append(responses[2].json()['productsinfo'][itemcount]['description'])
#   prices.append(convertPricePerUnits(responses[2].json()['productsinfo'][itemcount]['pricePer'],responses[2].json()['productsinfo'][itemcount]['unitOfMeasure'],1))
#   stores.append('Safeway')
#   units.append(convertUnits(responses[2].json()['productsinfo'][itemcount]['unitOfMeasure']))

#cur.execute("INSERT INTO groceries (item, price, unit, store, price_date) VALUES ('Sample banana', 1.99, 'POUND', 'Sample store', '10:40:00 10/26/2019')")
#conn.commit()

#insertGroceriesToTableQuery()
'''

cur.close()

'''
groceriesTable = pivotSort(items_generic, items, prices, stores, storenames, units, itemcount)
'''

'''
# Debugging
# print(groceriesTable)
# print(items_generic)
# print(organic_arr)
'''

conn.close()

'''
# Home page routing
@app.route("/")
@app.route("/home")
def unsorted():
    return render_template('home.html', groceries=zip(items, prices, stores, units))

@app.route("/pivot")
def home():
    return render_template('pivot.html', groceries=groceriesTable, headerRow=headerRow)
# Enable debugging when running
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='9001', debug=True)
'''

print("Script complete")
