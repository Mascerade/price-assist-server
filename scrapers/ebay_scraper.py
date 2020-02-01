from bs4 import BeautifulSoup
import urllib.request
import requests
import random
import os
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Ebay(Scraper):
    def __init__(self, product_model, test_header = None, tor_username = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'user_agents', 'ebay_agents.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}

        super().__init__(name="Ebay",
                         search_address='https://www.ebay.com/sch/i.html?_odkw={}&_osacat=0&_from=R40&_' \
                               'trksid=p2045573.m570.l1313.TR1.TRC0.A0.H0.TRS1&_nkw={}&_' \
                               'sacat=0'.format(product_model, product_model),
                         product_model=product_model,
                         user_agent=header,
                         tor_username=tor_username,
                         data="")

        self.product_address = self.search_address
    
    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all('span', 's-item__price')[0].text

        except Exception:
            self.price = None

if __name__ == "__main__":
    ebay = Ebay("BX80684I99900K")
    ebay.test()
