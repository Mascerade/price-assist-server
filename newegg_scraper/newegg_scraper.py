from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class NeweggProduct(Scraper):
    def __init__(self, product_model):
        self.price = ""
        self.product_address = ""
        with open(os.getcwd() + "\\user_agents\\newegg_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(search_address='https://www.newegg.com/Product/ProductList.aspx?' +\
                                      'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}'\
                                .format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        self.data = requests.get(self.search_address, headers=self.user_agent)
        self.data = self.data.text
        self.soup = BeautifulSoup(self.data, 'html.parser')

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find("a", attrs={"class": "item-title", "title": "View Details"})['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_price(self):
        try:
            self.price = "$"
            stop = False
            for x in self.soup.find("li", "price-current").text:
                if not stop:
                    if x.isdigit():
                        self.price += x

                    elif x == "(":
                        stop = True

                    elif x == "." or x == ",":
                        self.price += x

            if self.price.strip(" ") == "$":
                self.price = "Price Shown In Cart"

            else:
                self.price = self.price.strip(" ")

        except AttributeError as e:
            self.price = "Could Not Find Price"

        except TypeError as e:
            self.price = "Could Not Find Price"

        except Exception as e:
            self.price = "Could Not Find Price"

