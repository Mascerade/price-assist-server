from bs4 import BeautifulSoup
import requests
import random
import os
import sys
import json
from typing import Optional, Dict
from common.network_scraper import NetworkScraper


class Amazon(NetworkScraper):
    """
    We now have 4 scrapers that are essentially gaurenteed to work
    """
    def __init__(self,
                 product_model: str,
                 using_tor: bool = True,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name = "Amazon",
                         search_address=f'https://www.amazon.com/s?k={product_model}&i=electronics',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_tor_username=test_tor_username,
                         test_user_agent=test_user_agent)

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.amazon.com{}" \
                                    .format(self.soup.find_all("a", attrs={"class": "a-link-normal a-text-normal"})[0]['href'])
        
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
