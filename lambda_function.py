from amazon_scraper.amazon_scraper import AmazonProduct
from newegg_scraper.newegg_scraper import NeweggProduct
from bestbuy_scraper.bestbuy_scraper import BestBuy
from walmart_scraper.walmart_scraper import Walmart
from bandh_scraper.bandh_scraper import BandH
from ebay_scraper.ebay_scraper import Ebay
from tigerdirect_scraper.tigerdirect_scraper import TigerDirect
from microcenter_scraper.microcenter_scraper import Microcenter
from target_scraper.target_scraper import TargetScraper
from flask import Flask, request
import threading
import urllib.request
import time

newegg_data = []
bestbuy_data = []
walmart_data = []
bandh_data = []
ebay_data = []
tiger_direct_data = []
microcenter_data = []
target_data = []


def retrieve_newegg_data(item_model):
    newegg = NeweggProduct(item_model)
    newegg.retrieve_product_address()
    newegg.retrieve_product_price()
    global newegg_data
    newegg_data.append("Newegg")
    newegg_data.append(newegg.price)
    newegg_data.append(newegg.product_address)
    return


def retrieve_bestbuy_data(item_model):
    bestbuy = BestBuy(item_model)
    bestbuy.retrieve_product_address()
    bestbuy.retrieve_product_price()
    global bestbuy_data
    bestbuy_data.append("BestBuy")
    bestbuy_data.append(bestbuy.price)
    bestbuy_data.append(bestbuy.product_address)
    return


def retrieve_walmart_data(item_model):
    walmart = Walmart(item_model)
    walmart.retrieve_product_address()
    walmart.retrieve_product_price()
    global walmart_data
    walmart_data.append("Walmart")
    walmart_data.append(walmart.price)
    walmart_data.append(walmart.product_address)
    return


def retrieve_bandh_data(item_model):
    bandh = BandH(item_model)
    bandh.retrieve_price()
    bandh.retrieve_product_address()
    global bandh_data
    bandh_data.append("B&H")
    bandh_data.append(bandh.price)
    bandh_data.append(bandh.product_address)
    return


def retrieve_ebay_data(item_model):
    ebay = Ebay(item_model)
    ebay.retrieve_product_price()
    global ebay_data
    ebay_data.append("Ebay")
    ebay_data.append(ebay.price)
    ebay_data.append(ebay.product_address)
    return


def retrieve_tiger_direct_data(item_model):
    tiger = TigerDirect(item_model)
    tiger.retrieve_product_address()
    tiger.retrieve_price()
    global tiger_direct_data
    tiger_direct_data.append("Tiger Direct")
    tiger_direct_data.append(tiger.price)
    tiger_direct_data.append(tiger.product_address)
    return


def retrieve_microcenter_price(item_model):
    micro = Microcenter(item_model)
    micro.retrieve_product_address()
    micro.retrieve_price()
    global microcenter_data
    microcenter_data.append("Microcenter")
    microcenter_data.append(micro.price)
    microcenter_data.append(micro.product_address)
    return


def retrieve_target_price(item_model):
    target = TargetScraper(item_model)
    target.retrieve_product_price()
    global target_data
    target_data.append("Target")
    target_data.append(target.price)
    target_data.append(target.product_address)


def reset_retailer_lists():
    global newegg_data
    global bestbuy_data
    global walmart_data
    global bandh_data
    global ebay_data
    global tiger_direct_data
    global microcenter_data
    global target_data

    newegg_data = []
    walmart_data = []
    bandh_data = []
    ebay_data = []
    tiger_direct_data = []
    microcenter_data = []
    target_data = []


def lambda_handler(url):
    start_time = time.time()
    amazon = AmazonProduct(url)
    amazon.retrieve_item_model()
    item_model = amazon.model_number
    print(item_model)

    if item_model is not None:
        t = threading.Thread(target=amazon.retrieve_item_price)
        t2 = threading.Thread(target=retrieve_newegg_data, args=(item_model,))
        t3 = threading.Thread(target=retrieve_walmart_data, args=(item_model,))
        t4 = threading.Thread(target=retrieve_bandh_data, args=(item_model,))
        t5 = threading.Thread(target=retrieve_ebay_data, args=(item_model,))
        t6 = threading.Thread(target=retrieve_tiger_direct_data, args=(item_model,))
        t7 = threading.Thread(target=retrieve_microcenter_price, args=(item_model,))
        # t8 = threading.Thread(target=retrieve_target_price, args=(item_model,))

        t.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        # t8.start()

        t.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        # t8.join()

        global newegg_data
        global bestbuy_data
        global walmart_data
        global bandh_data
        global ebay_data
        global tiger_direct_data
        global microcenter_data
        global target_data

        print("GAUTAM")
        prices = {
            "amazon_data": amazon.price,
            "newegg_data": newegg_data,
            "walmart_data": walmart_data,
            "bandh_data": bandh_data,
            "ebay_data": ebay_data,
            "tigerdirect_data": tiger_direct_data,
            "microcenter_data": microcenter_data,
            # "target_data": target_data
        }

        print(time.time()-start_time)
        return str(prices)

    else:
        return str({"Error": "Amazon link invalid; Could not retrieve prices"})


# Create the Flask app
app = Flask(__name__)


@app.route('/query')
def query_example():
    link = request.args.get('link')
    reset_retailer_lists()
    try:
        return lambda_handler(link)

    except urllib.error.HTTPError as e:
        print(e)
        return str({"Error": "Server error"})

    except TypeError as e:
        print(e)


# Run app using localhost on port 5000
if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
