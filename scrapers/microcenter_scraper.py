from bs4 import BeautifulSoup
import requests
import os
import random
import sys
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Microcenter(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="Microcenter",
                         search_address='https://www.microcenter.com/search/search_results.aspx?Ntt={}'
                         .format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', {"itemprop": "price"}).text

        except Exception:
            self.price = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.microcenter.com" + self.soup.find("a", attrs={"id": "hypProductH2_0"})["href"]

        except Exception:
            self.product_address = None
            self.price = None

if __name__ == "__main__":
    micro = Microcenter("BX80684I99900K")
    micro.test()
    