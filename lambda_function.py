from amazon_scraper import AmazonProduct
from newegg_scraper import NeweggProduct
from bestbuy_scraper import BestBuy
from walmart_scraper import Walmart
from flask import Flask, request


def lambda_handler(url):
    amazon = AmazonProduct(url)
    amazon.retrieve_item_model()
    amazon.retrieve_item_price()
    item_model = amazon.model_number
    item_price = amazon.price

    if item_model is not None:
        newegg = NeweggProduct(item_model)
        newegg.retrieve_product_address()
        newegg.retrieve_product_price()
        newegg_price = newegg.price

        bestbuy = BestBuy(item_model)
        bestbuy.retrieve_product_address()
        bestbuy.retrieve_product_price()
        bestbuy_price = bestbuy.price

        walmart = Walmart(item_model)
        walmart.retrieve_product_address()
        walmart.retrieve_product_price()
        walmart_price = walmart.price

        prices = {"amazon_price": item_price,
                  "newegg_price": newegg_price,
                  "bestbuy_price": bestbuy_price,
                  "walmart_price": walmart_price}

        return str(prices)

    else:
        return {"Error": "Amazon link invalid; Could not retrieve prices"}


# Create the Flask app
app = Flask(__name__)


@app.route('/query')
def query_example():
    link = request.args.get('link')
    return lambda_handler(link)


# Run app using ip 102.168.0.177 debug mode on port 5000
if __name__ == '__main__':
    app.run(host='192.168.0.177', port=5000)
