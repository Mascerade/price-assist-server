from bs4 import BeautifulSoup
import urllib.request
import os
import random
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper

class Microcenter(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\microcenter_agents.txt", "r") as scrapers:
            headers = ['User-Agent', random.choice(scrapers.read().splitlines())]
        super().__init__(search_address='https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        try:
            data = urllib.request.Request(self.search_address)
            data.add_header(self.user_agent[0], self.user_agent[1])
            data = urllib.request.urlopen(data)
            data = data.read()
            self.soup = BeautifulSoup(data, "lxml")

        except Exception as e:
            self.price = "Could not find price"

    def retrieve_price(self):
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

