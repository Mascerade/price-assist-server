import sys
import os
import random
import requests
import bs4
from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Rakuten(Scraper):
    """
    Scrapes Rakuten to get required information
    """

    def __init__(self, product_model):
        with open(os.getcwd() + "/user_agents/walmart_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="Rakuten",
                         search_address="https://www.rakuten.com/search/" + product_model.replace(" ", "%20"),
                         product_model=product_model,
                         user_agent=headers,
                         use_selenium=True,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.findAll("div", attrs={"class":"r-product__name r-product__section"})[0].find("a")["href"]

        except Exception as e:
            print(e)
            self.product_address = None

    def retrieve_product_price(self):
        try:
            self.price = self.soup.findAll("span", attrs={"class":"r-product__price-text"})[0].text

        except Exception:
            self.price = None

if __name__ == "__main__":
    rakuten = Rakuten("BX80684I99900K")
    rakuten.test()
