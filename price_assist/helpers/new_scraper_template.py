from bs4 import BeautifulSoup
import random
import os
import sys
import requests
from common.base_scraper import Scraper


class NewScraper(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="NAME",
                         search_address='SEARCH ADDRESS {}'.format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("")[0].text

        except AttributeError as e:
            self.price = None

        except Exception as e:
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find_all("a")[0]['href']

        except AttributeError as e:
            self.product_address = None

        except Exception as e:
            self.product_address = None
