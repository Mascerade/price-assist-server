from bs4 import BeautifulSoup
import requests
import random
import os
import sys
import json
from master_scraper.master_scraper import Scraper


class Amazon(Scraper):
    """
    We now have 4 scrapers that are essentially gaurenteed to work
    """
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="Amazon",
                         search_address='https://www.amazon.com/s?k={}&i=electronics'.format(product_model),
                         product_model=product_model,
                         test_tor_username=test_tor_username,
                         test_user_agent = test_user_agent,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.amazon.com" + \
                                   self.soup.find_all("a", attrs={"class": "a-link-normal a-text-normal"})[0]['href']
        
        except (AttributeError, IndexError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("span", attrs={"class": "a-offscreen"})[0].text

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price")
            # I don't think it is necessary to do this
            # self.product_address = None


if __name__ == "__main__":
    amazon = Amazon("asus vivobook")
    amazon.test()
