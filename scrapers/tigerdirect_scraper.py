from bs4 import BeautifulSoup
import requests
import os
import random
import sys
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class TigerDirect(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="TigerDirect",
                         search_address='http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'
                         .format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_price(self):
        print(self.soup)
        try:
            count = 0
            self.price = self.soup.find('div', 'salePrice').text
            if self.price.count("$") > 1:
                for index, x in enumerate(self.price):
                    if x == "$" and count > 0:
                        self.price = self.price[index:]
                        break
                    if x == "$":
                        count += 1

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

    def retrieve_product_address(self):
        try:
            self.product_address = "http://www.tigerdirect.com" + self.soup.find('a', {'class': 'itemImage'})['href']

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    tiger = TigerDirect("ryzen 7")
    tiger.test()
