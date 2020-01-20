from bs4 import BeautifulSoup
import requests
import os
import random
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Microcenter(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'microcenter_agents.txt'), "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(name="Microcenter",
                         search_address='https://www.microcenter.com/search/search_results.aspx?Ntt={}'
                         .format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', {"itemprop": "price"}).text

        except AttributeError:
            self.price = "Could not find price"

        except Exception as e:
            self.price = "Could not find price"

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.microcenter.com" + self.soup.find("a", attrs={"id": "hypProductH2_0"})["href"]

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.price = "Could not find price"

if __name__ == "__main__":
    micro = Microcenter("BX80684I99900K")
    micro.test()
    