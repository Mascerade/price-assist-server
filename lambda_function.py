from amazon_scraper import AmazonProduct
from newegg_scraper import NeweggProduct
from bestbuy_scraper import BestBuy
from walmart_scraper import Walmart


def lambda_function(event, context):
    amazon = AmazonProduct(event["q"])
    amazon.retrieve_item_model()
    amazon.retrieve_item_price()
    item_model = amazon.model_number
    item_price = amazon.price

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

    message = {
        'amazon_price': item_price,
        'newegg_price': newegg_price,
        'bestbuy_price': bestbuy_price,
        'walmart_price': walmart_price
    }
