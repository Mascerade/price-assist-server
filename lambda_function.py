""""
Developed by Jason Acheampong of Timeless Apps
"""

""" LOCAL IMPORTS """
from helpers.scraper_functions import ScraperHelpers
from scrapers.amazon_scraper import AmazonProduct
from helpers.gui_generator import gui_generator

""" OUTSIDE IMPORTS """
from flask import Flask, request
import json
import flask
import threading
import time
import requests

iframe = """
<div id="iframe-wrapper" style="visibility: visible; width: 100%; display: flex; justify-content: center; 
align-items: center; transform: translateZ(0px); overflow: hidden; background-color: transparent; 
z-index: 100000000; border: none;">
    <iframe id="iframe" class="scrollbar scrollbar-primary" style="height: 500px; width: 300px; border: none;">
    </iframe>
</div>
"""

heading = """
    <style>
        ::-webkit-scrollbar {
            width: 10;
        }
        
        ::-webkit-scrollbar-track {
            background: #7D7D7D;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #4D4D4D;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link href="https://fonts.googleapis.com/css?family=Raleway:400,500" rel="stylesheet"> 
    <link rel="stylesheet" href="https://raw.githack.com/BinaryWiz/Price-Assist/master/css/retailers-popup.css"> 
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.2.1/lux/bootstrap.min.css">
"""


def lambda_handler(retailer, price, item_model, return_type):
    scrapers = ScraperHelpers()
    start_time = time.time()
    searcher = item_model
    print(retailer)

    # Created dictionary that contains all the generated data for retailer
    # [Name, Price, Product Address]
    retailer_functions = {
        "amazon_data": scrapers.retrieve_amazon_data,
        "bestbuy_data": scrapers.retrieve_bestbuy_data,
        "newegg_data": scrapers.retrieve_newegg_data,
        "walmart_data": scrapers.retrieve_walmart_data,
        "bandh_data": scrapers.retrieve_bandh_data,
        "ebay_data": scrapers.retrieve_ebay_data,
        "tigerdirect_data": scrapers.retrieve_tiger_direct_data,
        "microcenter_data": scrapers.retrieve_microcenter_price,
        "jet_data": scrapers.retrieve_jet_price,
        "outletpc_data": scrapers.retrieve_outletpc_price,
        "superbiiz_data": scrapers.retrieve_super_biiz_price
    }

    # Set the retailer that the info is coming from in the retailer_function
    # dictionary to the price. This is so that the program does not try
    # To run a thread for it unnecessarily
    retailer_functions[retailer.strip().lower() + "_data"] = price
    try:
        CACHE = False
        if searcher is not None:
            # Make GET request
            start = time.time()
            
            if CACHE:
                # Make a request to the caching server
                cached_server_data = requests.get("http://localhost:5001?item_model=" + item_model)
                print(time.time() - start)
                cached_server_data = cached_server_data.json()

                # If stored data was in the cache and it is valid [Name, Price, Product Address]
                # Then return those values
                if cached_server_data["success"]:
                    for _, value in cached_server_data.items():
                        if type(value) == list and len(value) == 3:
                            scrapers.all_scrapers.append(value)

                    if return_type == "json":
                        return json.dumps(cached_server_data)
                    
                    elif return_type == "gui":
                        scrapers.remove_extraneous()
                        scrapers.sort_all_scrapers()
                        return str({"iframe": iframe, "head": heading, "body": gui_generator(scrapers.all_scrapers)})    

            else:
                # Neat way of appending each function to the thread_list
                # And then simultaneously start them
                thread_list = []
                for function in retailer_functions.values():
                    if type(function) == str:
                        continue
                    thread_list.append(threading.Thread(target=function, args=(searcher,)))

                for thread in thread_list:
                    thread.start()

                for thread in thread_list:
                    thread.join()

                # Note: prices is for the json format, while scrapers.all_scrapers is for the gui
                prices = {
                    "identifier": searcher,
                    "amazon_data": scrapers.amazon_data,
                    "bestbuy_data": scrapers.bestbuy_data,
                    "newegg_data": scrapers.newegg_data,
                    "walmart_data": scrapers.walmart_data,
                    "bandh_data": scrapers.bandh_data,
                    "ebay_data": scrapers.ebay_data,
                    "tigerdirect_data": scrapers.tiger_direct_data,
                    "microcenter_data": scrapers.microcenter_data,
                    "jet_data": scrapers.jet_data,
                    "outletpc_data": scrapers.outletpc_data,
                    "superbiiz_data": scrapers.biiz_data
                }

                # Use the actual retailer's name if it had to reformatted to abide by
                # Python variable naming conventions (like B&H --> bandh)
                correct_retailer_name = retailer
                if retailer == "bandh":
                    correct_retailer_name = "B&H"

                # Set the source retailer information to the price given and "#" as it's address
                # To stay on the page its on
                prices[retailer.strip().lower() + "_data"] = [correct_retailer_name, price, "#"]

                # Insert the source scrapers to all_scrapers
                # This is because it didn't enter the scraper functions 
                # Where it gets added to all_scrapers
                scrapers.all_scrapers.insert(0, [correct_retailer_name, price, "#"])
                print("Total Elapsed Time: " + str(time.time()-start_time))

                # Removes all the scrapers that didn't give valid information
                scrapers.remove_extraneous()

                # Sort the scrapers by price (low --> high)
                scrapers.sort_all_scrapers()
                
                if return_type == "json":
                    # Jsonify the data to return it
                    load = flask.jsonify(prices)

                    # If the data was not already in the cache
                    if CACHE:
                        requests.put("http://localhost:5001/", json=json.loads(json.dumps(prices)))
                    return json.dumps(load.json)
                
                elif return_type == "gui":
                    # If the data was not already in the cache                    
                    if CACHE:
                        requests.put("http://localhost:5001/", json=json.loads(json.dumps(prices)))
                    return str({"iframe": iframe, "head": heading, "body": gui_generator(scrapers.all_scrapers)})
        else:
            return str({"Error": "Item model not found"})
    
    except Exception as e:
        print(e)
        return flask.jsonify({"success": False}), 500


# Create the Flask app
application = Flask(__name__)


@application.route('/api/query')
def query():
    # Get all the required information from the parameters in the URL
    retailer = request.args.get('retailer')
    price = request.args.get('price')
    item_model = request.args.get('item_model')
    return_type = request.args.get('return_type')
    try:
        return lambda_handler(retailer, price, item_model, return_type)

    except TypeError as e:
        return flask.abort(500)

# Run app using localhost
if __name__ == '__main__':
    application.run(host='localhost', port=5000, threaded=True, debug=True)
