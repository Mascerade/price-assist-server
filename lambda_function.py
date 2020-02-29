""""
Developed by Jason Acheampong of Timeless Apps
"""

""" LOCAL IMPORTS """
from helpers.scraper_functions import ScraperHelpers
from scrapers.amazon_scraper import AmazonProduct
from helpers.gui_generator import gui_generator
from master_scraper.master_scraper import Scraper

""" OUTSIDE IMPORTS """
from flask import Flask, request
import json
import flask
import threading
import time
import requests
import traceback

CACHE = True

def network_scrapers(retailer, price, item_model, title, return_type):
    USING_SOURCE_RETAILER = True
    scrapers = ScraperHelpers()
    start_time = time.time()
    searcher = item_model

    if retailer == "None":
        USING_SOURCE_RETAILER = False

    print(retailer)

    # Runs each scraper and it makes it easier to know which scraper function
    # Is for which retailer
    retailer_functions = {
        "amazon_data": scrapers.retrieve_amazon_data,
        "walmart_data": scrapers.retrieve_walmart_data,
        "newegg_data": scrapers.retrieve_newegg_data,
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

    try:
        cache_check = False
        if searcher is not None:
            # Make GET request
            
            if CACHE:
                # Make a request to the caching server
                cached_server_data = requests.get("http://localhost:5001?item_model=" + item_model).json()

                # If stored data was in the cache and it is valid [Name, Price, Product Address]
                # Then return those values
                if cached_server_data["success"]:
                    for _, value in cached_server_data.items():
                        if type(value) == list and len(value) >= 3:
                            scrapers.all_scrapers.append(value)

                    if return_type == "json":
                        return json.dumps(cached_server_data)
                    
                    elif return_type == "gui":
                        scrapers.remove_extraneous()
                        scrapers.sort_all_scrapers()
                        return str({"iframe": ScraperHelpers.iframe, "head": ScraperHelpers.heading, "body": gui_generator(scrapers.all_scrapers, True)})

                else:
                    cache_check = True
        
            if USING_SOURCE_RETAILER:
                retailer_functions[retailer.strip().lower() + "_data"] = price
                scrapers.all_scrapers.append([retailer, price, "#"])
                
            if not CACHE or cache_check:
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
                # Created dictionary that contains all the generated data for retailer
                # [Name, Price, Product Address]
                prices = {
                    "identifier": searcher,
                    "amazon_data": scrapers.amazon_data,
                    "walmart_data": scrapers.walmart_data,
                    "newegg_data": scrapers.newegg_data,
                    "bandh_data": scrapers.bandh_data,
                    "ebay_data": scrapers.ebay_data,
                    "tigerdirect_data": scrapers.tiger_direct_data,
                    "microcenter_data": scrapers.microcenter_data,
                    "jet_data": scrapers.jet_data,
                    "outletpc_data": scrapers.outletpc_data,
                    "superbiiz_data": scrapers.biiz_data
                }
                    
                if USING_SOURCE_RETAILER:
                    # If we're using the source retailer, then get the title from the url
                    prices["title"] = title

                    # Only put the item model and title into the database if it is from a source retailer
                    requests.put("http://localhost:5003/item_model_data", json={"item_model": item_model, "title": prices["title"]})

                    prices[retailer.strip().lower() + "_data"] = [retailer, price, "#"]


                print("Total Elapsed Time: " + str(time.time()-start_time))

                # Removes all the scrapers that didn't give valid information
                scrapers.remove_extraneous()

                # Sort the scrapers by price (low --> high)
                scrapers.sort_all_scrapers()

                # Send the item model to the item model database
                
                # Send the price data to the track prices database
                # requests.put("http://localhost:5003/", json={"item_model": item_model, "data": prices})

                if CACHE:
                    requests.put("http://localhost:5001/", json={"data": json.loads(json.dumps(prices)), "cache_flag": False})

                if return_type == "json":
                    # Jsonify the data to return it
                    load = flask.jsonify(prices)
                    return json.dumps(load.json)
                
                elif return_type == "gui":
                    return str({"iframe": ScraperHelpers.iframe, "head": ScraperHelpers.heading, "body": gui_generator(scrapers.get_all_scrapers(), True)})

        else:
            return str({"Error": "Item model not found"})
    
    except Exception as e:
        print(str(e), "from lambda_function")
        print(traceback.format_exc())
        return flask.jsonify({"success": False}), 500

def process_based_scraper(retailer, price, item_model, return_type):
    USING_SOURCE_RETAILER = True
    scrapers = ScraperHelpers()
    start_time = time.time()
    searcher = item_model

    if retailer == "None":
        USING_SOURCE_RETAILER = False


    if searcher is not None:
        # Make GET request
        if CACHE:
            # Make a request to the caching server
            cached_server_data = requests.get("http://localhost:5001?item_model=" + item_model + "_process").json()

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
                    return str({"iframe": ScraperHelpers.iframe, "head": ScraperHelpers.heading, "body": gui_generator(scrapers.all_scrapers, False)})

    # Runs each scraper and it makes it easier to know which scraper function
    # Is for which retailer
    retailer_functions = {
        "bestbuy_data": scrapers.retrieve_bestbuy_data,
        "rakuten_data": scrapers.retrieve_rakuten_data,
        "target_data": scrapers.retrieve_target_data
    }

    # Set the retailer that the info is coming from in the retailer_function
    # dictionary to the price. This is so that the program does not try
    # To run a thread for it unnecessarily

    if USING_SOURCE_RETAILER:
        retailer_functions[retailer.strip().lower() + "_data"] = price

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
    
    prices = {
        "identifier": searcher,
        "bestbuy_data": scrapers.bestbuy_data,
        "rakuten_data": scrapers.rakuten_data,
        "target_data": scrapers.target_data
    }

    if CACHE:
        requests.put("http://localhost:5001/", json={"data": json.loads(json.dumps(prices)), "cache_flag": True})
    
    if return_type == "json":
        # Jsonify the data to return it
        load = flask.jsonify(prices)        
        return json.dumps(load.json)

    elif return_type == "gui":
        # Removes all the scrapers that didn't give valid information
        scrapers.remove_extraneous()

        # Sort the scrapers by price (low --> high)
        scrapers.sort_all_scrapers()

        return str({"iframe": ScraperHelpers.iframe, "head": ScraperHelpers.heading, "body": gui_generator(scrapers.get_all_scrapers(), False)})

    print(time.time() - start_time)

# Create the Flask app
application = Flask(__name__)


@application.route('/price-assist/api/network-scrapers')
def query():
    # Get all the required information from the parameters in the URL
    retailer = request.args.get('retailer')
    price = request.args.get('price')
    item_model = request.args.get('item_model')
    title = request.args.get('title')
    return_type = request.args.get('return_type')
    
    try:
        return network_scrapers(retailer, price, item_model, title, return_type)

    except TypeError:
        return flask.abort(500)

@application.route('/price-assist/api/process-scrapers')
def proces_based_scraper_response():
    retailer = request.args.get('retailer')
    price = request.args.get('price')
    item_model = request.args.get('item_model')
    return_type = request.args.get('return_type')

    try:
        return process_based_scraper(retailer, price, item_model, return_type)

    except TypeError:
        return flask.abort(500)


# Run app using localhost
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
