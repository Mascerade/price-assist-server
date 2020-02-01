from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Walmart(Scraper):
    def __init__(self, product_model, test_header = None, tor_username = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'tor_agents', 'walmart_tor.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}
        
        else:
            header = {"User-Agent": test_header}

        super().__init__(name="Walmart",
                         search_address='https://www.walmart.com/search/?query={}'.format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         tor_username=tor_username,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.walmart.com" + \
                                   self.soup.find('a', 'product-title-link line-clamp line-clamp-2')['href']

        except Exception:
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not "None":
            try:
                self.price = self.soup.find("span", attrs={"class": "price-group"}).text

            except Exception:
                self.price = None

        else:
            self.price = None


if __name__ == "__main__":
    walmart = Walmart("Ryzen 9 3900X")
    walmart.test()
