from bs4 import BeautifulSoup
import requests
import os
import sys
import random
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Jet(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="Jet",
                         search_address='https://jet.com/search?term={}'.format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.jet.com" + self.soup.findAll("a", attrs={"class":
                "base__BaseStyledComponent-sc-1l64hnd-0 base__Link-sc-1l64hnd-2 " +
                "BaseProductTile__ItemLink-sc-1h29u1u-0 cBMJRO"})[0]["href"]

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        try:
            self.price = self.soup.findAll("span", attrs={"class":"base__BaseStyledComponent-sc-1l64hnd-0 " +
            "typography__Text-sc-1lwzhqv-0 hIuNJJ"})[0].text

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    jet = Jet("BX80684I99900K")
    jet.test()