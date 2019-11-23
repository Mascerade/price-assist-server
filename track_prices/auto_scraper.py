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


app = Flask(__name__)

@app.route("/", methods=["GET", "PUT"])
def main():
    if request.method == "GET":
        """ Retrieve all the data from the SQL Database """
        pass

    if request.method == "PUT":
        """
        Create new price history in database OR update existing one with new date and price
        Data should be in the form of a JSON:
        {'item_model': some_item_model, 'prices': another_json_of_prices} 
        """

        data = request.json
        item_model = data['item_model'].lower()

        with sqlite3.connect("track_prices/prices.db") as c:
            c.execute(''' CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY,
            date text,
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


        # TODO: Parse the request data and put it in the database
        insert_prices = [datetime.now().strftime("%m-%Y-%d")]

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
                
                print(value)
                
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