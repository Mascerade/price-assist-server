from bs4 import BeautifulSoup
import requests
import os
import random
import sys
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class Microcenter(NetworkScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[Dict[str, str]] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Microcenter",
                         search_address=f'https://www.microcenter.com/search/search_results.aspx?Ntt={product_model}',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', {"itemprop": "price"}).text

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
            self.product_address = "https://www.microcenter.com" + self.soup.find("a", attrs={"id": "hypProductH2_0"})["href"]


        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    micro = Microcenter("BX80684I99900K")
    micro.test()
    