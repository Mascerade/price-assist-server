from bs4 import BeautifulSoup
import urllib.request
import requests
import random
import os
import sys
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class Ebay(NetworkScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[Dict[str, str]] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Ebay",
                         search_address=(f'https://www.ebay.com/sch/i.html?_odkw={product_model}&_osacat=0&_from=R40&_'
                                          f'trksid=p2045573.m570.l1313.TR1.TRC0.A0.H0.TRS1&_nkw={product_model}&_sacat=0'),
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username
                         )

        self.product_address = self.search_address
    
    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all('span', 's-item__price')[0].text

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    ebay = Ebay("BX80684I99900K")
    ebay.test()
