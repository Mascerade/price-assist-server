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


def lambda_handler(url):
    scrapers = ScraperHelpers()
    start_time = time.time()
    amazon = AmazonProduct(url)
    amazon.retrieve_item_model()
    print("Amazon: " + str(time.time() - start_time))
    item_model = amazon.product_model
    searcher = item_model

    if searcher is not None:
        t = threading.Thread(target=amazon.retrieve_item_price)
        t2 = threading.Thread(target=scrapers.retrieve_newegg_data, args=(searcher,))
        t3 = threading.Thread(target=scrapers.retrieve_walmart_data, args=(searcher,))
        t4 = threading.Thread(target=scrapers.retrieve_bandh_data, args=(searcher,))
        t5 = threading.Thread(target=scrapers.retrieve_ebay_data, args=(searcher,))
        t6 = threading.Thread(target=scrapers.retrieve_tiger_direct_data, args=(searcher,))
        t7 = threading.Thread(target=scrapers.retrieve_microcenter_price, args=(searcher,))
        t8 = threading.Thread(target=scrapers.retrieve_jet_price, args=(item_model,))
        t9 = threading.Thread(target=scrapers.retrieve_bestbuy_data, args=(item_model,))
        t10 = threading.Thread(target=scrapers.retrieve_outletpc_price, args=(item_model,))

        t.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()

        t.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()

        prices = {
            "amazon_data": amazon.price,
            "bestbuy_data": scrapers.bestbuy_data,
            "newegg_data": scrapers.newegg_data,
            "walmart_data": scrapers.walmart_data,
            "bandh_data": scrapers.bandh_data,
            "ebay_data": scrapers.ebay_data,
            "tigerdirect_data": scrapers.tiger_direct_data,
            "microcenter_data": scrapers.microcenter_data,
            "jet_data": scrapers.jet_data,
            "outletpc_data": scrapers.outletpc_data
        }

        print("Total Elapsed Time: " + str(time.time()-start_time))
        return str(prices)

    else:
        return str({"Error": "Amazon link invalid; Could not retrieve prices"})


# Create the Flask app
app = Flask(__name__)


@app.route('/query')
def query_example():
    link = request.args.get('link')
    try:
        return lambda_handler(link)

    except TypeError as e:
        print(e)


# Run app using localhost on port 5000
if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
