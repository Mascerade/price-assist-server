from flask import Flask, request
import json
import flask
import time
import requests
import sys
import os
import sqlite3
from datetime import datetime

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

@app.route("/", methods=["GET"])
def get_data():
    """ Retrieve all the data from the SQL Database """
    item_model = request.args.get("item_model")
    with sqlite3.connect("track_prices/prices.db") as conn:
        get_info = '''SELECT * from {}'''.format(item_model)
        # The cursor is what actaully gets data from the database
        cur = conn.cursor()

        # Execute the selection of data
        cur.execute(get_info)

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
def put_date():
    if request.method == "PUT":
        """
        Create new price history in database OR update existing one with new date and price
        Data should be in the form of a JSON:
        {'item_model': some_item_model, 'prices': another_json_of_prices} 
        """

        data = request.json
        item_model = data['item_model'].lower()

        with sqlite3.connect("track_prices/prices.db") as c:
            c.execute(''' CREATE TABLE IF NOT EXISTS {} (
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
            superbiiz float) '''.format(item_model))

        # List used to insert the date and prices into the database
        insert_prices = [datetime.now().strftime("%Y-%m-%d")]

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

        insert_data = ''' INSERT INTO {} (date, amazon, bestbuy, newegg, walmart, bandh, ebay, tigerdirect, microcenter, jet, outlet, superbiiz) 
        VALUES({})'''.format(item_model, ','.join(insert_prices))

        print(insert_data)

        # Add the data to the databse
        c.execute(insert_data)
        c.commit()

        # Contains all the items already in the list of item_models
        all_items = []

        # Gets all the items already in the database
        with open("track_prices/all_items.txt", "r") as file:
            all_items = file.readlines()

        # Checks if the item PUT is already in the database
        with open("track_prices/all_items.txt", "a+") as file:
            found = False
            for line in all_items:
                if line.strip().lower() == item_model:
                    found = True

            # Add the item to the text file if it hasn't been tracked yet
            if not found:
                file.write(item_model + "\n")

        # Return the fact that data was successfully added to the database
        return json.dumps({"success": True}), 204

if __name__ == "__main__":
    app.run("localhost", port=5003, threaded=True)