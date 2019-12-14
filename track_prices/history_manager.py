from flask import Flask, request
import json
import flask
from flask_cors import cross_origin
import time
import requests
import sys
import os
import sqlite3
import datetime
import plyvel

""" 
This is the auto-price checker
Essentially, have SQL database where each table name is the product's
model and each is a different date with the price on that date

FOR THE DATABASE
* For now, we will use a locally stored database (sqlite3)

FOR AUTO UPDATING
* Going to have to set up some kind of thread pool because
  we can only have so many products updating at the same time

* It will send a request to this server to get information from the
  scrapers using a specific product address (probably going to have
  to fix the problem where I will have to use totally new members
  to do this)
    - This can be a seperate route (/update or something with a
    dictionary of all the product addresses along with the retailer name)
"""

# What is used to create the dict of each entry
RETAILER_ORDER = ["date", "amazon", "bestbuy", "newegg", "walmart", "banh", "ebay", "tigerdirect", "microcenter", "jet", "outletpc", "superbiiz"]

app = Flask(__name__)

@app.route("/fake_data", methods=["GET"])
@cross_origin()
def get_fake_data():
    """ Used to test the graph of the GUI """

    # Opens a connection to the fake data database
    conn = sqlite3.connect("fake_data.db")
    cursor = conn.cursor()

    # Get all the data from the table "fake_data1"
    get_info = "SELECT * from fake_data1"
    cursor.execute(get_info)

    # Data to be returned
    return_data = []

    # Zips the entries with "date" and "amazon" because that is what the GUI uses
    for entry in cursor.fetchall():
        return_data.append(dict(zip(['date', 'amazon'], entry)))

    # Return the data with error code 200
    return json.dumps(return_data), 200

@app.route("/", methods=["GET"])
@cross_origin()
def get_data():
    """ Retrieve all the data from the SQL Database """
    item_model = request.args.get("item_model")
    
    ply_db = plyvel.DB('item_model_db/', create_if_missing = False)
    for key, value in ply_db:
        print(key, value)

    ply_db.close()

    with sqlite3.connect("prices.db") as conn:
        get_info = '''SELECT * from {}'''.format(item_model)
        # The cursor is what actaully gets data from the database
        cur = conn.cursor()

        try: 
            # Execute the selection of data
            cur.execute(get_info)
        
        except sqlite3.OperationalError as e:
            return json.dumps({'success': False, 'msg': str(e)}), 500

        # Get the data
        sql_data = cur.fetchall()

        # List of dictionaries to return
        return_data = []

        # Zip the retailer_order with each entry to get a dict of each retailer's prices
        for entry in sql_data:
            return_data.append(dict(zip(RETAILER_ORDER, entry)))
        
        # return the data with a 200 success error code
        return json.dumps(return_data), 200

@app.route("/", methods=["PUT"])
def put_data():
    if request.method == "PUT":
        """
        Create new price history in database OR update existing one with new date and price
        Data should be in the form of a JSON:
        {'item_model': some_item_model, 'prices': another_json_of_prices} 
        """

        data = request.json
        item_model = data['item_model'].lower()

        conn = sqlite3.connect("prices.db")

        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS {} (
        date DATE,
        amazon float,
        bestbuy float,
        newegg float,
        walmart float,
        bandh float,
        ebay float,
        tigerdirect float,
        microcenter float,
        jet float,
        outlet float,
        superbiiz float); '''.format(item_model))

        # List used to insert the date and prices into the database
        insert_prices = [datetime.date.today()]

        # Get only the actual information about each retailer from the data dict
        # Note: We're treating 0's as invalid information
        for _, value in data["data"].items():
            try:
                # The item model is part of the data, so don't include that
                if type(value) == str:
                    continue

                # If there was just blank price information, don't include it
                elif value[1] == '':
                    insert_prices.append("0")
                    continue
                                
                # Convert the price to a float to make sure it's actual price information
                # Convert it back to a string to add to the database
                insert_prices.append(str(float(value[1][1:])))
            
            except:
                insert_prices.append("0")

        insert_prices = tuple(insert_prices)
        insert_data = ''' INSERT INTO ''' + item_model + ''' (date, amazon, bestbuy, newegg, walmart, bandh, 
        ebay, tigerdirect, microcenter, jet, outlet, superbiiz) VALUES(''' + "?, " * (len(RETAILER_ORDER) - 1) + '''?)'''

        # Just to check that everything is working
        print(insert_data)

        # Add the data to the databse
        cursor.execute(insert_data, insert_prices)
        conn.commit()

        # Close the connections
        cursor.close()
        conn.close()

        ply_db = plyvel.DB('item_model_db/', create_if_missing = True)

        ply_db.put(bytes(item_model, encoding='utf-8'), bytes(True))
        
        ply_db.close()

        return json.dumps({"success": True}), 204

@app.route("/", methods=["DELETE"])
def delete_data():
    item_model = request.json['item_model'].lower().strip()
    ply_db = plyvel.DB('item_model_db/', create_if_missing = False)

    # We check if "check" is equal to None (meaning the item model is not in the database)
    check = ply_db.get(bytes(item_model, encoding='utf-8'))
    
    # As long as there is something in "check" the item_model exists
    if check is not None:
        # Establish the connection to the prices database
        conn = sqlite3.connect("prices.db")
        cursor = conn.cursor()

        # DROP TABLE essentially will delete the table
        delete_str = "DROP TABLE " + item_model

        # Execute the deletion of the table and close the connection
        cursor.execute(delete_str)
        conn.commit()
        conn.close()

        # Delete the item_model in the plyvel database as well
        ply_db.delete(bytes(item_model, encoding='utf-8'))
    
        return json.dumps({'success': True}), 202

    return json.dumps({'success': False, "msg":"Item model not found"}), 400

if __name__ == "__main__":
    app.run("localhost", port=5003, threaded=True)
