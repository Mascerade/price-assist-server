from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Walmart(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'walmart_agents.txt'), "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(name="Walmart",
                         search_address='https://www.walmart.com/search/?query={}'.format(product_model, product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.walmart.com" + \
                                   self.soup.find('a', 'product-title-link line-clamp line-clamp-2')['href']
        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_address is not "None":
            try:
                self.price = self.soup.find("span", attrs={"class": "price-group"}).text

            except AttributeError:
                self.price = "Could Not Find Price"

            except TypeError:
                self.price = "Could Not Find Price"

            except Exception as e:
                self.price = "Could Not Find Price"

        else:
            self.price = "Could Not Find Price"


if __name__ == "__main__":
    walmart = Walmart("Ryzen 9 3900X")
    walmart.test()
