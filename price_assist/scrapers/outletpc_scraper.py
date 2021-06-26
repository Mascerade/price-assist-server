from bs4 import BeautifulSoup
import requests
import os
import sys
import random
import json
from common.base_scraper import Scraper


class OutletPC(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="OutletPC",
                         search_address='https://sitesearch.outletpc.com/search/display_type-Grid--keywords-{}'
                         .format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find('a', 'prod-name')['href']

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find("div", attrs={"id": "nxt-prod-price"}).text

            except (AttributeError, IndexError, TypeError) as e:
                # AttributeError most likely means that it was not able to find the span
                # resulting in a NoneType error
                self.access_error(function_name="retrieve_product_price()")
                self.price = None

            except Exception:
                self.unhandled_error(error=e, function_name="retrieve_product_price()")
                self.price = None

        else:
            self.price = None

if __name__ == "__main__":
    outlet = OutletPC("BX80684I99900K")
    outlet.test()
