# Enter password for MySQL RDS as first command line argument

from datetime import datetime
from decimal import *

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
RDS_DB_pricing = 'pricing'
RDS_DB_sf = 'sf'

# RDS PASSWORD
if len(sys.argv) == 2:
    RDS_PW = str(sys.argv[1])
else:
    print("Usage: Enter password for MySQL server as first command line argument")
    sys.exit(1)

print("Connecting to RDS...")

# RDS connection
print("Connecting to pricing...")
conn_pricing = pymysql.connect(RDS_HOST,
                               user=RDS_USER,
                               port=RDS_PORT,
                               passwd=RDS_PW,
                               db=RDS_DB_pricing)
print("Connected to RDS successfully.")

cur_pricing = conn_pricing.cursor()
print("Initialized cursor.")

print("Connecting to sf...")
conn_sf = pymysql.connect(RDS_HOST,
                          user=RDS_USER,
                          port=RDS_PORT,
                          passwd=RDS_PW,
                          db=RDS_DB_sf)
print("Connected to RDS successfully.")

cur_sf = conn_sf.cursor()
print("Initialized cursor.")

# Add items and prices
mysql_insert_price_compare_query = """INSERT INTO price_competitive 
(item_id, item_name, farm_price, farm_unit, market_name, market_item_name, market_item_id, market_price, market_unit, market_zipcode, market_price_date, is_item_same, is_competitive)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

print("Inserting to RDS...")

# Function to compare prices
# In future, if quantity is considered, add logic in this function


def doPriceComparison(farm_unit, farm_price, market_unit, market_price):
    # get base conversion from sf.conversion_units of farm_unit and farm_price
    # if base unit is same then only price is compared
    print("IN DO COMPARISON")
    query = """SELECT recipe_unit, conversion_ratio, common_unit FROM conversion_units WHERE recipe_unit = %s;"""
    cur_sf.execute(query, farm_unit.lower())
    farm_base_unit = cur_sf.fetchone()
    print('farm_base_unit: ', farm_base_unit)
    cur_sf.execute(query, market_unit.lower())
    market_base_unit = cur_sf.fetchone()
    print('market_base_unit: ', market_base_unit)

    if farm_base_unit[2] == market_base_unit[2]:
        if farm_price/farm_base_unit[1] < market_price/market_base_unit[1]:
            return "YES"
        return "NO"
    else:
        print("BASE CONVERSION UNIT DOES NOT MATCH!!!")
        return "NO"


try:
    item_id = '310-000030'
    item_name = 'Yellow Onion'
    farm_price = '1.25'
    farm_unit = 'lb'
    farm_quantity = '1'
    #is_organic = ''
    query = """ select * from groceries where item LIKE '%Yellow Onion%' and item NOT LIKE '%Organic%';"""
    print("Running query...")
    cur_pricing.execute(query)
    queriedData = cur_pricing.fetchall()
    # print("Queried data.")
    # print(queriedData)

    for row in queriedData:
        print("row: ", row)
        print("store: ", row[4])
        print("market_price: ", row[2])
        print("market_unit: ", row[3])
        market_unit = row[3]
        market_price = row[2]
        # add unit_conversion logic
        # print("Going in function")
        is_competitive = doPriceComparison(
            farm_unit, Decimal(farm_price), market_unit, Decimal(market_price))
        # print("is_competitive:   ", is_competitive)
        insertTuple = (item_id, item_name, farm_price,
                       farm_unit, row[4], row[0], row[1], row[2], row[3], row[5], row[6], "yes", is_competitive)
        cur_pricing.execute(mysql_insert_price_compare_query, insertTuple)
    conn_pricing.commit()
    print("Committed insertion to RDS.")
except:
    print("Exception thrown!!!!!!!!!")

cur_pricing.close()
cur_sf.close()
print("Cursor closed.")

conn_pricing.close()
conn_sf.close()
print("Connection to RDS closed.")

print("Script complete")
