from bs4 import BeautifulSoup
import random
import os
import sys
import requests
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class SuperBiiz(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="SuperBiiz",
                         search_address='https://www.superbiiz.com/query.php?s={}'.format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_price(self):
        try:
            # for index, x in enumerate(self.soup.find_all("tr")):
            #     print(x.text, index)
            self.price = self.soup.find_all("td", attrs={"width": "1%"})[0].find("a").text.strip()
            new_price = ""
            for char in self.price:
                if char == "$" or char == "." or char.isdigit():
                    new_price += char
            self.price = new_price

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.superbiiz.com" + self.soup.find_all("tr")[45].find("a")["href"]

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    superbiiz = SuperBiiz("BX80684I99900K")
    superbiiz.test()
