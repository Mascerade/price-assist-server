""""
Developed by Jason Acheampong of Timeless Apps
"""

""" LOCAL IMPORTS """
from amazon_scraper.amazon_scraper import AmazonProduct
from helpers.scraper_functions import ScraperHelpers
from helpers.gui_generator import gui_generator


""" OUTSIDE IMPORTS """
from flask import Flask, request
import threading
import time

iframe = """
<div id="iframe-wrapper" style="visibility: visible; width: 100%; display: flex; justify-content: center; align-items: center; transform: translateZ(0px); overflow: hidden; background-color: transparent; z-index: 100000000; border: none;">
    <iframe id="iframe" class="scrollbar scrollbar-primary" style="height: 500px; width: 300px; border: none;">
    </iframe>
</div>
"""

heading = """
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <link href="https://fonts.googleapis.com/css?family=Raleway:400,500" rel="stylesheet"> 
    <link rel="stylesheet" href="https://raw.githack.com/BinaryWiz/Price-Assist/master/css/retailers-popup.css"> 
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.2.1/lux/bootstrap.min.css">
"""


def lambda_handler(url, price, item_model):
    scrapers = ScraperHelpers()
    start_time = time.time()
    searcher = item_model
    print(searcher)

    retailer_functions = {
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

    if searcher is not None:
        thread_list = []
        for function in retailer_functions.values():
            thread_list.append(threading.Thread(target=function, args=(searcher,)))

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        prices = {
            "amazon_data": price,
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
        scrapers.all_scrapers.insert(0, ["Amazon", price, "#"])
        print("Total Elapsed Time: " + str(time.time()-start_time))
        return str({"iframe": iframe, "head": heading, "body": gui_generator(scrapers.all_scrapers)})
        # return str(prices)

    else:
        return str({"Error": "Amazon link invalid; Could not retrieve prices"})


# Create the Flask app
application = Flask(__name__)


@application.route('/api/query')
def query():
    link = request.args.get('link')
    amazon_price = request.args.get('amazon_price')
    item_model = request.args.get('item_model')
    try:
        return lambda_handler(link, amazon_price, item_model)

    except TypeError as e:
        print(e)


# Run app using localhost on port 5000
if __name__ == '__main__':
    application.run(host='0.0.0.0', threaded=True, debug=True)
