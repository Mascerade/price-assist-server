import sys
import os
import random
import requests
import bs4
from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from common.base_scraper import Scraper


class Rakuten(Scraper):
    """
    Scrapes Rakuten to get required information
    """

    def __init__(self, product_model):
        super().__init__(name="Rakuten",
                         search_address="https://www.rakuten.com/search/" + product_model.replace(" ", "%20"),
                         product_model=product_model,
                         use_selenium=True,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.findAll("div", attrs={"class":"r-product__name r-product__section"})[0].find("a")["href"]

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        try:
            self.price = self.soup.findAll("span", attrs={"class":"r-product__price-text"})[0].text

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    rakuten = Rakuten("BX80684I99900K")
    rakuten.test()
