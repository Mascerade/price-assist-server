from bs4 import BeautifulSoup
import requests
import os
import random
import sys
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class TigerDirect(NetworkScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool =False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="TigerDirect",
                         search_address=f'http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={product_model}',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)

    def retrieve_product_price(self):
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

        except Exception as e:
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
