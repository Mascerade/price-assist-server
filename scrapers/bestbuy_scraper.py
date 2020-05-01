from bs4 import BeautifulSoup
import random
import requests
import os
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class BestBuy(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="BestBuy",
                         search_address='https://www.bestbuy.com/site/searchpage.jsp?st={}'.format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="",
                         use_selenium=True)

    def retrieve_product_address(self):
        try:
            sku_header = self.soup.find('h4', 'sku-header')
            self.product_address = "https://www.bestbuy.com" + sku_header.find('a')['href']

        except AttributeError:
            self.product_address = None 

        except TypeError:
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find('div', 'priceView-hero-price priceView-customer-price').find("span").text

            except Exception:
                self.price = None

        else:
            self.price = None

if __name__ == "__main__":
    best = BestBuy("BX80684I99900K")
    best.test()
