from bs4 import BeautifulSoup
import requests
import os
import sys
import random
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class NeweggProduct(NetworkScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Newegg",
                         search_address=('https://www.newegg.com/Product/ProductList.aspx?'
                                         f'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={product_model}')
                                .format(product_model),
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)
        
    def retrieve_product_address(self):
        try:
            self.title = self.soup.find("a", attrs={"class": "item-title", "title": "View Details"}).text
            self.title = self.title.replace('"', '\\\"')
            self.product_address = self.soup.find("a", attrs={"class": "item-title", "title": "View Details"})['href']


        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None
            self.title = "Unavailable"

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None
            self.title = "Unavailable"

    def retrieve_product_price(self):
        try:
            self.price = "$"
            stop = False
            for x in self.soup.find("li", "price-current").text:
                if not stop:
                    if x.isdigit():
                        self.price += x

                    elif x == "(":
                        stop = True

                    elif x == "." or x == ",":
                        self.price += x

            if self.price.strip(" ") == "$":
                self.price = "Price Shown In Cart"

            else:
                self.price = self.price.strip(" ")

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    newegg = NeweggProduct("P2719H")
    newegg.test()
