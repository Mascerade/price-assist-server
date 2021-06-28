from bs4 import BeautifulSoup
import requests
import os
import sys
import random
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class Walmart(NetworkScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Walmart",
                         search_address=f'https://www.walmart.com/search/?query={product_model}',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)

    def retrieve_product_address(self):
        # TODO: Fix address
        try:
            self.product_address = "https://www.walmart.com" + \
                                   self.soup.find('a', {'data-type': 'itemTitles'})['href']

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find("span", attrs={"class": "price-group"}).text

            except (AttributeError, IndexError, TypeError) as e:
                # AttributeError most likely means that it was not able to find the span
                # resulting in a NoneType error
                self.access_error(function_name="retrieve_product_price()")
                self.price = None

            except Exception as e:
                self.unhandled_error(error=e, function_name="retrieve_product_price()")
                self.price = None

        else:
            self.price = None


if __name__ == "__main__":
    walmart = Walmart("Ryzen 9 3900X")
    walmart.test()
