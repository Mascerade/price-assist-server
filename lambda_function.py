""""
Developed by Jason Acheampong of Timeless Apps
"""

""" LOCAL IMPORTS """
from helpers.scraper_functions import ScraperHelpers
from helpers.gui_generator import gui_generator
from master_scraper.master_scraper import Scraper
from common.common_path import CommonPaths

""" OUTSIDE IMPORTS """
from flask import Flask, request
from flask_cors import cross_origin
import json
import flask
import threading
import time
import requests
import traceback
import logging

# Sets up the logger for when exceptions happen in the server
logger = logging.getLogger('lambda_function')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logging/lambda_function.log')
logger.addHandler(fh)

def get_caching_data(label):
    try:
        cached_server_data = requests.get("http://" + CommonPaths.CACHE_IP + ":5001?item_model=" + label).json()

        # If stored data was in the cache and it is valid [Name, Price, Product Address]
        # Then return those values
        if cached_server_data["success"]:
            return json.dumps(cached_server_data)
    
    except requests.exceptions.ConnectionError:
        logger.warning('Caching server not running right now')

def network_scrapers(retailer, price, item_model, title, image):
    USING_SOURCE_RETAILER = True
    scrapers = ScraperHelpers()
    start_time = time.time()
    item_model = item_model.lower()
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
        "ebay_data": scrapers.retrieve_ebay_data,
        "tigerdirect_data": scrapers.retrieve_tiger_direct_data,
        "microcenter_data": scrapers.retrieve_microcenter_price,
    }

    # Set the retailer that the info is coming from in the retailer_function
    # dictionary to the price. This is so that the program does not try
    # To run a thread for it unnecessarily

    try:
        if searcher is not None:
            # This block is only run if the caching server is online
            # Otherwise, go through with scraping the websites
            if CommonPaths.CACHE:
                cache = get_caching_data(item_model)
                if cache is not None:
                    return cache

            # This makes it so that if we already have the retailer's data, we don't run the scraper
            if USING_SOURCE_RETAILER:
                print(retailer, price)
                retailer_functions[retailer.strip().lower() + "_data"] = price
                scrapers.all_scrapers.append([retailer, price, "#"])
                
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
                "ebay_data": scrapers.ebay_data,
                "tigerdirect_data": scrapers.tiger_direct_data,
                "microcenter_data": scrapers.microcenter_data,
            }
                
            if USING_SOURCE_RETAILER:
                # If we're using the source retailer, then get the title from the url
                prices["title"] = title
                prices[retailer.strip().lower() + "_data"] = [retailer, price, "#"]

                # Only put the item model and title into the database if it is from a source retailer
                try:
                    requests.put("http://" + CommonPaths.TRACK_PRICES_IP + ":5003/item_model_data", json={"item_model": item_model, "title": prices["title"]})
                    requests.put("http://" + CommonPaths.TRACK_PRICES_IP + ":5003/image_data", json={"item_model": item_model, "image": image})

                except requests.exceptions.ConnectionError:
                    logger.warning('Track Prices server not running right now')

            print("Total Elapsed Time: " + str(time.time()-start_time))

            # Removes all the scrapers that didn't give valid information
            scrapers.remove_extraneous()

            # Sort the scrapers by price (low --> high)
            scrapers.sort_all_scrapers()
            
            # Send the price data to the track prices database
            if CommonPaths.CACHE:
                try:
                    requests.put("http://" + CommonPaths.CACHE_IP + ":5001/", json={"data": json.loads(json.dumps(prices)), "cache_flag": False})

                except requests.exceptions.ConnectionError:
                    logger.warning('Caching server not running right now')

            # Jsonify the data to return it
            load = flask.jsonify(prices)
            return json.dumps(load.json)

        else:
            return str({"Error": "Item model not found"})
    
    except Exception as e:
        logger.error('Unexpected error from lambda function: ' + str(e))
        return flask.jsonify({"success": False}), 500

def process_based_scraper(retailer, price, item_model):
    USING_SOURCE_RETAILER = True
    scrapers = ScraperHelpers()
    start_time = time.time()
    item_model = item_model.lower()
    searcher = item_model

    if retailer == "None":
        USING_SOURCE_RETAILER = False

    if searcher is not None:
        # Make GET request to the cache
        if CommonPaths.CACHE:
            cache = get_caching_data(item_model + '_process')
            if cache is not None:
                return cache

    # Runs each scraper and it makes it easier to know which scraper function
    # Is for which retailer
    retailer_functions = {
        "bestbuy_data": scrapers.retrieve_bestbuy_data,
        "rakuten_data": scrapers.retrieve_rakuten_data,
        "bandh_data": scrapers.retrieve_bandh_data,
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
        "bandh_data": scrapers.bandh_data,
        "target_data": scrapers.target_data
    }

    if CommonPaths.CACHE:
        try:
            requests.put("http://" + CommonPaths.CACHE_IP + ":5001/", json={"data": json.loads(json.dumps(prices)), "cache_flag": True})

        except requests.exceptions.ConnectionError:
            logger.warning('Caching server not running right now')

    print(time.time() - start_time)

    # Jsonify the data to return it
    load = flask.jsonify(prices)        
    return json.dumps(load.json)


def single_retailer(retailer, item_model):
    retailer = retailer.lower()
    item_model = item_model.lower()
    if CommonPaths.CACHE:
        network_scrapers = get_caching_data(item_model)
        if network_scrapers is not None:
            try:
                network_scrapers = json.loads(network_scrapers)
                return json.dumps(network_scrapers[retailer + '_data'])

            except KeyError:
                process_scrapers = json.loads(get_caching_data(item_model + '_process'))
                return json.dumps(process_scrapers[retailer + '_data'])

    scrapers = ScraperHelpers()
    retailer_functions = {
        "amazon_data": scrapers.retrieve_amazon_data,
        "walmart_data": scrapers.retrieve_walmart_data,
        "newegg_data": scrapers.retrieve_newegg_data,
        "bandh_data": scrapers.retrieve_bandh_data,
        "ebay_data": scrapers.retrieve_ebay_data,
        "tigerdirect_data": scrapers.retrieve_tiger_direct_data,
        "microcenter_data": scrapers.retrieve_microcenter_price,
        "bestbuy_data": scrapers.retrieve_bestbuy_data,
        "rakuten_data": scrapers.retrieve_rakuten_data,
        "target_data": scrapers.retrieve_target_data
    }

    retailer_functions[retailer.lower() + '_data'](item_model)
    prices = {
        "amazon_data": scrapers.amazon_data,
        "walmart_data": scrapers.walmart_data,
        "newegg_data": scrapers.newegg_data,
        "bandh_data": scrapers.bandh_data,
        "ebay_data": scrapers.ebay_data,
        "tigerdirect_data": scrapers.tiger_direct_data,
        "microcenter_data": scrapers.microcenter_data,
        "bestbuy_data": scrapers.bestbuy_data,
        "rakuten_data": scrapers.rakuten_data,
        "target_data": scrapers.target_data
    }
    
    return json.dumps(prices[retailer.lower() + '_data'])

# Create the Flask app
application = Flask(__name__)


@application.route('/price-assist/api/network-scrapers')
@cross_origin()
def network_scraper():
    # Get all the required information from the parameters in the URL
    retailer = request.args.get('retailer')
    price = request.args.get('price')
    item_model = request.args.get('item_model')
    title = request.args.get('title')
    image = request.args.get('image')
    
    try:
        return network_scrapers(retailer, price, item_model, title, image)

    except Exception as e:
        logger.error('Unexpected error from network scrapers: {}'.format(str(e)))
        return flask.abort(500)

@application.route('/price-assist/api/process-scrapers')
@cross_origin()
def process_based_scraper_response():
    retailer = request.args.get('retailer')
    price = request.args.get('price')
    item_model = request.args.get('item_model')

    try:
        return process_based_scraper(retailer, price, item_model)

    except Exception as e:
        logger.error('Unexpected error from process scrapers: {}'.format(str(e)))
        return flask.abort(500)

@application.route('/price-assist/api/current-price')
@cross_origin()
def current_price():
    retailer = request.args.get('retailer')
    item_model = request.args.get('item_model')

    try:
        return single_retailer(retailer, item_model)

    except TypeError as e:
        print(str(e))
        return flask.abort(500)

# Run app using localhost
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
