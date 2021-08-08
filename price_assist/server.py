""""
Developed by Jason Acheampong of Timeless Apps
"""

""" OUTSIDE IMPORTS """
from flask import Flask, request
from flask_cors import cross_origin
from typing import Tuple, Optional
import json
import flask
import time
import requests
import logging
import os

""" LOCAL IMPORTS """
from scrapers.amazon_scraper import Amazon
from scrapers.bandh_scraper import BandH
from scrapers.bestbuy_scraper import BestBuy
from scrapers.ebay_scraper import Ebay
from scrapers.microcenter_scraper import Microcenter
from scrapers.newegg_scraper import Newegg
from scrapers.target_scraper import Target
from scrapers.tigerdirect_scraper import TigerDirect
from scrapers.walmart_scraper import Walmart
from common.common_path import CommonPaths
from common.scraper_manager import ScraperManager
from common.scraper_tab_manager import ScraperTabManager
from common.stm_scraper import STMScraper

# manager = ScraperTabManager('Amazon', '500', 'https://www.google.com')
# print(manager)
# test = STMScraper('Amazon', 'x', 'https://www.google.com/', using_tor=False, indicator_element=[], test_user_agent=None, test_tor_username=None)

# Create logging folder
if not os.path.exists('logging'):
    os.mkdir('logging')

# Sets up the logger for when exceptions happen in the server
logger = logging.getLogger('lambda_function')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logging/lambda_function.log')
logger.addHandler(fh)

def get_caching_data(label) -> Optional[str]:
    try:
        cached_server_data = requests.get(f"http://{CommonPaths.CACHE_IP}:5001?item_model=" + label).json()

        # If stored data was in the cache and it is valid [Name, Price, Product Address]
        # Then return those values
        if cached_server_data["success"]:
            return json.dumps(cached_server_data)
        else:
            return None
    
    except requests.exceptions.ConnectionError:
        logger.warning('Caching server not running right now')
        return None

def network_scrapers(retailer: Optional[str],
                     price: Optional[str],
                     item_model: Optional[str],
                     title: Optional[str],
                     image: Optional[str]) -> Tuple[str, int]:
    start_time = time.time()
    if item_model is not None:
        item_model = item_model.lower()
        identifier: str = item_model

    print(retailer)

    # Set the retailer that the info is coming from in the retailer_function
    # dictionary to the price. This is so that the program does not try
    # To run a thread for it unnecessarily

    try:
        if identifier is not None:
            # This block is only run if the caching server is online
            # Otherwise, go through with scraping the websites
            if CommonPaths.CACHE:
                cache = get_caching_data(item_model)
                if cache is not None:
                    return cache, 200
            
            # Add the network scrapers to scraper manager and run them
            scraper_manager: ScraperManager = ScraperManager(retailer, price, identifier)
            scraper_manager.add(Amazon(identifier))
            scraper_manager.add(Ebay(identifier))
            scraper_manager.add(Microcenter(identifier))
            scraper_manager.add(Newegg(identifier))
            scraper_manager.add(TigerDirect(identifier))
            scraper_manager.add(Walmart(identifier))
            scraper_manager.run_scrapers()

            if retailer != None and title != None:
                # Only put the item model and title into the database if it is from a source retailer
                try:
                    requests.put(f"http://{CommonPaths.TRACK_PRICES_IP}:5003/item_model_data", json={"item_model": identifier, "title": title})
                    requests.put(f"http://{CommonPaths.TRACK_PRICES_IP}:5003/image_data", json={"item_model": identifier, "image": image})

                except requests.exceptions.ConnectionError:
                    logger.warning('Track Prices server not running right now')

            # Send the price data to the track prices database
            if CommonPaths.CACHE:
                try:
                    requests.put(f"http://{CommonPaths.CACHE_IP}:5001/", json={"data": scraper_manager.as_dict(),
                                                                               "cache_flag": False})

                except requests.exceptions.ConnectionError:
                    logger.warning('Caching server not running right now')

            print(time.time() - start_time)

            return json.dumps(scraper_manager.as_dict()), 200

        else:
            return json.dumps({"success": False, "message": "Item model not found"}), 404
    
    except Exception as e:
        logger.error('Unexpected error from lambda function: ' + str(e))
        return json.dumps({"success": False}), 500

def process_based_scraper(retailer: Optional[str],
                          price: Optional[str],
                          item_model: Optional[str]) -> Tuple[str, int]:
    start_time = time.time()
    if item_model is not None:
        item_model = item_model.lower()
        identifier: str = item_model

    print(retailer)

    try:
        if identifier is not None:
            # Make GET request to the cache
            if CommonPaths.CACHE:
                cache = get_caching_data(identifier + '_process')
                if cache is not None:
                    return cache, 200

            # Add the process scrapers to scraper manager and run them
            scraper_manager: ScraperManager = ScraperManager(retailer, price, identifier)
            scraper_manager.add(BestBuy(identifier))
            scraper_manager.add(BandH(identifier))
            scraper_manager.add(Target(identifier))
            scraper_manager.run_scrapers()

        # Add to cache if necessary
        if CommonPaths.CACHE:
            try:
                requests.put("http://" + CommonPaths.CACHE_IP + ":5001/", json={"data": json.loads(json.dumps(scraper_manager.as_dict())),
                                                                                "cache_flag": True})

            except requests.exceptions.ConnectionError:
                logger.warning('Caching server not running right now')

        print(time.time() - start_time)

        return json.dumps(scraper_manager.as_dict()), 200

    except Exception as e:
        logger.error('Unexpected error from lambda function: ' + str(e))
        return json.dumps({"success": False}), 500

def single_retailer(retailer: Optional[str], item_model: Optional[str]) -> Tuple[str, int]:
    if retailer is not None and item_model is not None:
        try:
            retailer = retailer.lower()
            item_model = item_model.lower()
            if CommonPaths.CACHE:
                network_scrapers = get_caching_data(item_model)
                if network_scrapers is not None:
                    try:
                        network_scrapers_dict = json.loads(network_scrapers)
                        return json.dumps({retailer: network_scrapers_dict[retailer]}), 200

                    except KeyError:
                        process_scrapers = get_caching_data(f'{item_model}_process')
                        if process_scrapers is not None:
                            process_scrapers_dict = json.loads(process_scrapers)
                            return json.dumps({retailer: process_scrapers_dict[retailer]}), 200

            scraper_manager = ScraperManager(None, None, None)
            scraper_manager.add(Amazon(item_model))
            scraper_manager.add(Ebay(item_model))
            scraper_manager.add(Microcenter(item_model))
            scraper_manager.add(Newegg(item_model))
            scraper_manager.add(TigerDirect(item_model))
            scraper_manager.add(Walmart(item_model))
            scraper_manager.add(BestBuy(item_model))
            scraper_manager.add(BandH(item_model))
            scraper_manager.add(Target(item_model))
            if retailer is not None:
                return json.dumps(scraper_manager.run_single_scraper(retailer)), 200
            else:
                return json.dumps({"success": False, "message": "Could not find the retailer"}), 404
        
        except Exception as e:
            logger.error(f'Unexpected error from single_retailer: {e}')
            return json.dumps({"success": False}), 500
    else:
        return json.dumps({"success": False, "message": "Insufficient valid information"}), 404

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
