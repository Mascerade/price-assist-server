from bs4 import BeautifulSoup
import requests
import random
import os
import sys
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper

class Amazon(Scraper):
    """
    We now have 4 scrapers that are essentially gaurenteed to work
    """
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="Amazon",
                         search_address='https://www.amazon.com/s?k={}&i=electronics&ref=nb_sb_noss'.format(product_model),
                         product_model=product_model,
                         test_tor_username=test_tor_username,
                         test_user_agent = test_user_agent,
                         data="")
        
        print(self.soup.prettify())

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("span", attrs={"class": "a-offscreen"})[0].text

        except AttributeError as e:
            print(e)
            self.price = None

        except Exception as e:
            print(e)
            self.product_address = None

    def retrieve_product_address(self):
        # TODO: Fix this
        try:
            self.product_address = "https://www.amazon.com" + \
                                   self.soup.find_all("a", attrs={"data-selenium": "miniProductPageProductNameLink"})[0]['href']
        
        except AttributeError as e:
            print(e)
            self.product_address = None

        except Exception as e:
            print(e)
            self.product_address = None

if __name__ == "__main__":
    amazon = Amazon("asus vivobook")
    amazon.test()
