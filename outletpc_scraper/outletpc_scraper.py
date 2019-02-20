from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class OutletPC(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\walmart_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(name="OutletPC",
                         search_address='https://sitesearch.outletpc.com/search/display_type-Grid--keywords-{}'
                         .format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        self.data = requests.get(self.search_address, headers=self.user_agent, timeout=5).text
        self.soup = BeautifulSoup(self.data, "lxml")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find('a', 'prod-name')['href']
        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_address is not "None":
            try:
                self.price = self.soup.find("div", attrs={"id": "nxt-prod-price"}).text
            except AttributeError:
                self.price = "Could Not Find Price"

            except TypeError:
                self.price = "Could Not Find Price"

            except Exception as e:
                self.price = "Could Not Find Price"

        else:
            self.price = "Could Not Find Price"
