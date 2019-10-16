# FEATURES NEEDED TO BE ADDED
# pivotSort: New logic for product item name and generic item name matching
# pivotSort: Some items not detected
# Implement proper prices/units handling, some of it is not correct
# Implement automation of API JSON parsing, currently done manually
# Parse more than 20 items for each store
# Organic flags in JSON are repetitive; implement code that will handle organic and non-organic without organic flag in JSON file

# Packages
from flask import Flask, render_template
import requests
import urllib.request
import time
import json

app = Flask(__name__)

# JSON data file
json_data = 'jsondata.json'

# Initialize data structures for json data
responses = []
storenames = []
itemAccessKeys = []
priceAccessKeys = []
unitAccessKeys = []
storeZipCodes = []
items_generic = []
organic_arr = []
index = 0

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

# Generic item list from JSON
for genstore in data_dict['genericItems']:
    items_generic.append(genstore['name'])
    organic_arr.append(genstore['organic'])

# Initialize items and prices lists
items = []
prices = []
stores = []
units = []

# Append zipcode to storename
def appendZipCodeToStoreName(storenames, storeZipCodes):
    for index, zipcode in enumerate(storeZipCodes):
        storenames[index] = storenames[index]+"("+str(zipcode)+")"
    return storenames

# Header row for pivot table on website
headerRow = ['Item', 'Organic?']
headerRow.extend(appendZipCodeToStoreName(storenames, storeZipCodes))

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

# Generic Item Name Check, return boolean
#def isGeneric(itemArr, itemGenArr):
#    for words in itemArr:
        
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
for itemcount in range(20):
    for storeindex in range(3):
        itemToAppend = getKeys(responses[storeindex].json(), itemAccessKeys[storeindex], itemcount)
        unitsToAppend = getKeys(responses[storeindex].json(), unitAccessKeys[storeindex], itemcount)
        priceToAppend = getKeys(responses[storeindex].json(), priceAccessKeys[storeindex], itemcount)
        items.append(itemToAppend)
        prices.append(convertPricePerUnits(priceToAppend, unitsToAppend, 1)) # Fix
        units.append(convertUnits(unitsToAppend))
        stores.append(storenames[storeindex])

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

groceriesTable = pivotSort(items_generic, items, prices, stores, storenames, units, itemcount)

# Debugging
# print(groceriesTable)
# print(items_generic)
# print(organic_arr)

# Home page routing
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', groceries=groceriesTable, headerRow=headerRow)

# Unsorted table
@app.route("/unsorted")
def unsorted():
    return render_template('unsorted.html', groceries=zip(items, prices, stores, units))

# Enable debugging when running
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='9001', debug=True)
