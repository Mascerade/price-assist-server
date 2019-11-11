from bs4 import BeautifulSoup
import random
import requests
import os
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class BestBuy(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'bestbuy_agents.txt'), "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(name="BestBuy",
                         search_address='https://www.bestbuy.com/site/searchpage.jsp?st={}'.format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")

    def retrieve_product_address(self):
        try:
            sku_header = self.soup.find('h4', 'sku-header')
            self.product_address = "https://www.bestbuy.com" + sku_header.find('a')['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find('div', 'priceView-hero-price priceView-customer-price').find("span").text

            except Exception:
                self.price = "Could Not Find Price"

        else:
            self.price = "Could Not Find Price"
