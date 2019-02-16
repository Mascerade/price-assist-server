from bs4 import BeautifulSoup
import urllib.request
import requests
import random
import os
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Ebay(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\ebay_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="Ebay",
                         search_address='https://www.ebay.com/sch/i.html?_odkw={}&_osacat=0&_from=R40&_' \
                               'trksid=p2045573.m570.l1313.TR1.TRC0.A0.H0.TRS1&_nkw={}&_' \
                               'sacat=0'.format(product_model, product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        self.product_address = self.search_address
        self.data = requests.get(self.search_address, headers=self.user_agent).text
        self.soup = BeautifulSoup(self.data, "lxml")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all('span', 's-item__price')[0].text

        except AttributeError:
            self.price = "Could Not Find Price"

        except TypeError:
            self.price = "Could Not Find Price"

        except Exception as e:
            self.price = "Could Not Find Price"
