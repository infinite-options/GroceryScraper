# Enter password for MySQL RDS as first command line argument

from datetime import datetime
from decimal import *

import sys
import requests
import urllib.request
import time
import json
import pymysql
import pandas as pd

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

mysql_insert_price_compare_query = """INSERT INTO price_competitive_join 
(item_id, item_name, farm_price, farm_unit, market_name, market_item_name, market_item_id, market_price, market_unit, market_zipcode, market_price_date, is_item_same, is_competitive)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """


def doPriceComparison(farm_unit, farm_price, market_unit, market_price):
    # get base conversion from sf.conversion_units of farm_unit and farm_price
    # if base unit is same then only price is compared
    print("IN DO COMPARISON")
    if type(farm_unit) is str and type(market_unit) is str:
        query = """SELECT recipe_unit, conversion_ratio, common_unit FROM conversion_units WHERE recipe_unit = %s;"""
        cur_sf.execute(query, farm_unit.lower())
        farm_base_unit = cur_sf.fetchone()
        # print('farm_base_unit: ', farm_base_unit)
        cur_sf.execute(query, market_unit.lower())
        market_base_unit = cur_sf.fetchone()
        # print('market_base_unit: ', market_base_unit)

        if farm_base_unit[2] == market_base_unit[2]:
            if farm_price/farm_base_unit[1] < market_price/market_base_unit[1]:
                return "YES"
            return "NO"
        else:
            print("BASE CONVERSION UNIT DOES NOT MATCH!!!")
            return "NO"
    else:
        print("FARM UNIT NONE DETECTED")
        return "NO"


try:
    query_groceries = """SELECT * from groceries;"""
    groceries_df = pd.read_sql(query_groceries, conn_pricing)
    # print(groceries_df)
    query_items = """select * from items;"""
    items_df = pd.read_sql(query_items, conn_sf)
    # print(items_df)

    # perform LEFT JOIN on both the dataframes
    result_df = pd.merge(items_df, groceries_df,
                         left_on='item_name', right_on='abb_item_name', how='left')
    # print('-------------------------------------------------------------------------------------')
    # print(result_df)
    # html = result_df.to_html()
    # text_file = open("index.html", "w")
    # text_file.write(html)
    # text_file.close()
    for index, row in result_df.iterrows():
        print(row.itm_business_id)
        print('row: ', row)
        farm_price = row.item_price
        print('farm_price: ', farm_price)
        farm_unit = row.item_unit
        print('farm_unit: ', type(farm_unit))
        market_price = row.price
        print('market_price: ', market_price)
        market_unit = row.unit
        print('market_unit: ', type(market_unit))
        # print('item_name: ', row.item)
        is_competitve = doPriceComparison(
            farm_unit, Decimal(farm_price), market_unit, Decimal(market_price))
        insertTuple = (str(row.item_id_x), str(row.item_name_x),
                       str(row.item_price), str(row.item_unit), str(row.store), str(row.item_name_y), str(row.item_id_y), str(row.price), str(row.unit), str(row.zipcode), str(row.price_date), "YES", is_competitve)
        cur_pricing.execute(mysql_insert_price_compare_query, insertTuple)
    conn_pricing.commit()
except:
    print("Exception thrown!!!!!!!!!")

cur_pricing.close()
cur_sf.close()
print("Cursor closed.")

conn_pricing.close()
conn_sf.close()
print("Connection to RDS closed.")

print("Script complete")
