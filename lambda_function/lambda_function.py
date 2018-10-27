from amazon_scraper import AmazonProduct
from newegg_scraper import NeweggProduct
from bestbuy_scraper import BestBuy
from walmart_scraper import Walmart
from bandh_scraper import BandH
from ebay_scraper import Ebay
from tigerdirect_scraper import TigerDirect
from microcenter_scraper import Microcenter
from flask import Flask, request
import threading
import urllib.request
import time

newegg_price = None
bestbuy_price = None
walmart_price = None
bandh_price = None
ebay_price = None
tiger_direct_price = None
microcenter_price = None


def retrieve_newegg_data(item_model):
    newegg = NeweggProduct(item_model)
    newegg.retrieve_product_address()
    newegg.retrieve_product_price()
    global newegg_price
    newegg_price = newegg.price
    return


def retrieve_bestbuy_data(item_model):
    bestbuy = BestBuy(item_model)
    bestbuy.retrieve_product_address()
    bestbuy.retrieve_product_price()
    global bestbuy_price
    bestbuy_price = bestbuy.price
    return


def retrieve_walmart_data(item_model):
    walmart = Walmart(item_model)
    walmart.retrieve_product_address()
    walmart.retrieve_product_price()
    global walmart_price
    walmart_price = walmart.price
    return


def retrieve_bandh_data(item_model):
    bandh = BandH(item_model)
    bandh.retrieve_price()
    global bandh_price
    bandh_price = bandh.price
    return


def retrieve_ebay_data(item_model):
    ebay = Ebay(item_model)
    ebay.retrieve_product_price()
    global ebay_price
    ebay_price = ebay.price
    return


def retrieve_tiger_direct_data(item_model):
    tiger = TigerDirect(item_model)
    tiger.retrieve_price()
    global tiger_direct_price
    tiger_direct_price = tiger.price
    return


def retrieve_microcenter_price(item_model):
    micro = Microcenter(item_model)
    micro.retrieve_price()
    global microcenter_price
    microcenter_price = micro.price
    return


def lambda_handler(url):
    start_time = time.time()
    amazon = AmazonProduct(url)
    amazon.retrieve_item_model()
    item_model = amazon.model_number
    print(time.time() - start_time)

    t = threading.Thread(target=amazon.retrieve_item_price)
    t2 = threading.Thread(target=retrieve_newegg_data, args=(item_model,))
    t3 = threading.Thread(target=retrieve_walmart_data, args=(item_model,))
    t4 = threading.Thread(target=retrieve_bandh_data, args=(item_model,))
    t5 = threading.Thread(target=retrieve_ebay_data, args=(item_model,))
    t6 = threading.Thread(target=retrieve_tiger_direct_data, args=(item_model,))
    t7 = threading.Thread(target=retrieve_microcenter_price, args=(item_model,))

    t.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()

    t.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()

    global newegg_price
    global bestbuy_price
    global walmart_price
    global bandh_price
    global ebay_price
    global tiger_direct_price
    global microcenter_price

    if item_model is not None:
        prices = {
            "amazon_price": amazon.price,
            "newegg_price": newegg_price,
            "walmart_price": walmart_price,
            "bandh_price": bandh_price,
            "ebay_price": ebay_price,
            "tigerdirect_price": tiger_direct_price,
            "microcenter_price": microcenter_price
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
