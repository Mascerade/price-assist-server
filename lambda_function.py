""""
Developed by Jason Acheampong of Timeless Apps
"""

""" LOCAL IMPORTS """
from amazon_scraper.amazon_scraper import AmazonProduct
from helpers.scraper_functions import ScraperHelpers


""" OUTSIDE IMPORTS """
from flask import Flask, request
import threading
import time


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

        print("Total Elapsed Time: " + str(time.time()-start_time))
        return str(prices)

    else:
        return str({"Error": "Amazon link invalid; Could not retrieve prices"})


# Create the Flask app
app = Flask(__name__)


@app.route('/query')
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
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
