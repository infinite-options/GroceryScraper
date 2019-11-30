from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_cors import CORS

from werkzeug.exceptions import BadRequest, NotFound

from decimal import Decimal
import decimal
import sys
import json
import pymysql

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

app.config['DEBUG'] = True

api = Api(app)

# RDS PASSWORD
if len(sys.argv) == 2:
    RDS_PW_GLOBAL = str(sys.argv[1])
else:
    RDS_PW_GLOBAL = ""

def getRdsConn():
    RDS_HOST = 'pm-mysqldb.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
    RDS_PORT = 3306
    RDS_USER = 'admin'
    RDS_DB = 'pricing'
    RDS_PW = RDS_PW_GLOBAL
    print("Trying to connect to RDS...")
    try:
        conn = pymysql.connect( RDS_HOST,
                                user=RDS_USER,
                                port=RDS_PORT,
                                passwd=RDS_PW,
                                db=RDS_DB)
        cur = conn.cursor()
        print("Successfully connected to RDS.")
        return [conn, cur]
    except:
        print("Could not connect to RDS.")
        raise Exception("RDS Connection failed.")



class latestPricing(Resource):

    """
    class DecimalEncoder(json.JSONEncoder):
        def default(self, value):
            if isinstance(value, decimal.Decimal):
                return str(value)
            # Let the base class default method raise TypeError
            return json.JSONEncoder.default(self, value)
    """

    def get(self):
        response = {}
        try:
            # Connect to RDS
            rds = getRdsConn()
            conn = rds[0]
            cur = rds[1]

            # Run query
            query = """ SELECT item, price, unit, store, zipcode, max(price_date) as \'latestDate\'
                        FROM groceries
                        GROUP BY item, store, zipcode;"""
            print("Running query...")
            cur.execute(query)
            queriedData = cur.fetchall()
            print("Queried data.")


            # Write queried data to json
            items = []
            print("Initialized items list")
            for row in queriedData:
                rowDict = {}
                print("Initialized row dict to append")
                print("Row:", row)
                rowDictKeys = ('item', 'price', 'unit', 'store', 'zipcode', 'latestDate')
                
                for element in enumerate(row):
                    print(element)
                    keyToAppend = rowDictKeys[element[0]]
                    print(keyToAppend)
                    valueToAppend = element[1]
                    if keyToAppend == 'price':
                        valueToAppend = float(valueToAppend)
                    print(valueToAppend)
                    rowDict[keyToAppend] = valueToAppend
                print(rowDict)

                """
#               formattedRowDict = json.dumps(rowDict, cls=DecimalEncoder)
#               print(formattedRowDict)
#               items.append(formattedRowDict)
                """

                items.append(rowDict)

            response['message'] = 'Request successful.'
            response['result'] = items

            print(response)

            # Close RDS connection
            cur.close()
            conn.close()
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')

api.add_resource(latestPricing, '/api/v1/latestpricing')

if __name__ == '__main__':
    app.run(host='localhost', port='8080')
