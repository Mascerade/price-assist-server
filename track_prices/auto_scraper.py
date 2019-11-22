from flask import Flask, request
import json
import flask
import time
import requests
import sys
import os
import sqlite3


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
            amazon text,
            bestbuy text,
            newegg text,
            walmart text,
            bandh text,
            ebay text,
            tigerdirect text,
            microcenter text,
            jet text,
            outlet text,
            superbiiz text) '''.format(item_model))

        all_items = []
        with open("track_prices/all_items.txt", "r") as file:
            all_items = file.readlines()

        with open("track_prices/all_items.txt", "a+") as file:
            found = False
            for line in all_items:
                if line.strip().lower() == item_model:
                    found = True

            if not found:
                file.write(item_model + "\n")


        return json.dumps({"success": True}), 204

if __name__ == "__main__":
    app.run("localhost", port=5003, threaded=True)