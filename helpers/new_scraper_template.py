from bs4 import BeautifulSoup
import random
import os
import sys
import requests
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class NewScraper(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'scrapers_master.txt'), "r") as scrapers:
            header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="NAME",
                         search_address='SEARCH ADDRESs {}'.format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         data="")
        try:
            data = requests.get(self.search_address, headers=self.user_agent).text
            self.soup = BeautifulSoup(data, Scraper.parser)

        except Exception as e:
            self.price = "Could not find price"
            self.product_address = "None"

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("")[0].text

        except AttributeError as e:
            self.price = "Could not find price"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find_all("a")['href']

        except AttributeError as e:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"
