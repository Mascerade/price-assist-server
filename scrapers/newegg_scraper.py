from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class NeweggProduct(Scraper):
    def __init__(self, product_model, test_header = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'tor_agents', 'newegg_tor.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}   
        
        super().__init__(name="Newegg",
                         search_address='https://www.newegg.com/Product/ProductList.aspx?' +\
                                      'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}'\
                                .format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         data="")
        
    def retrieve_product_address(self):
        try:
            self.title = self.soup.find("a", attrs={"class": "item-title", "title": "View Details"}).text
            self.product_address = self.soup.find("a", attrs={"class": "item-title", "title": "View Details"})['href']

        except AttributeError as e:
            self.title = "Unavailable"
            self.product_address = None

        except TypeError as e:
            self.title = "Unavailable"
            self.product_address = None

        except Exception as e:
            self.title = "Unavailable"
            self.product_address = None

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
            self.price = None

        except TypeError as e:
            self.price = None

        except Exception as e:
            self.price = None

if __name__ == "__main__":
    newegg = NeweggProduct("BX80684I99900K")
    newegg.test()
