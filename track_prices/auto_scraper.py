from flask import Flask, request
import json
import flask
import time
import requests

if __name__ == "__main__":
    import sys
    import os    
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from amazon_scraper.amazon_scraper import Amazon


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
        """ Create new price history in database OR update existing one with new date and price """
        pass    

if __name__ == "__main__":
    app.run("localhost", port=5003, threaded=True)