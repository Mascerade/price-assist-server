from bs4 import BeautifulSoup
import requests
import os
import random
import sys
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Microcenter(Scraper):
    def __init__(self, product_model, test_header = None, tor_username = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'user_agents', 'microcenter_agents.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}

        if tor_username is None:
            with open("settings.json") as json_file:
                settings = json.load(json_file)

                if settings["location"] == "desktop":
                    with open(os.path.join(os.getcwd(), 'desktop_tor_ips', 'microcenter_tor_ips.txt')) as microcenter_tor_ips:
                        tor_username = int(random.choice(microcenter_tor_ips.read().splitlines()).strip())
                    
                elif settings["location"] == "server":
                    pass

        super().__init__(name="Microcenter",
                         search_address='https://www.microcenter.com/search/search_results.aspx?Ntt={}'
                         .format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         tor_username=tor_username,
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
    