from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class OutletPC(Scraper):
    def __init__(self, product_model, test_header = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'user_agents', 'walmart_agents.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}
        
        super().__init__(name="OutletPC",
                         search_address='https://sitesearch.outletpc.com/search/display_type-Grid--keywords-{}'
                         .format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find('a', 'prod-name')['href']

        except Exception:
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find("div", attrs={"id": "nxt-prod-price"}).text

            except Exception as e:
                self.price = None

        else:
            self.price = None

if __name__ == "__main__":
    outlet = OutletPC("BX80684I99900K")
    outlet.test()
