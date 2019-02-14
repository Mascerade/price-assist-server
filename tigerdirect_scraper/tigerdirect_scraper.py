from bs4 import BeautifulSoup
import requests
import os
import random
import sys
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class TigerDirect(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\tigerdirect_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="TigerDirect",
                         search_address='http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'
                         .format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        try:
            self.data = requests.get(self.search_address, headers=self.user_agent).text
            self.soup = BeautifulSoup(self.data, "lxml")

        except Exception as e:
            print(e)
            self.price = "Could not find price"

    def retrieve_product_price(self):
        try:
            count = 0
            self.price = self.soup.find('div', 'salePrice').text
            if self.price.count("$") > 1:
                for index, x in enumerate(self.price):
                    if x == "$" and count > 0:
                        self.price = self.price[index:]
                        break
                    if x == "$":
                        count += 1

        except AttributeError:
            self.price = "Could not find price"

        except TypeError:
            self.product_address = "None"
            self.price = "Could not find price"

        except Exception as e:
            self.product_address = "None"
            self.price = "Could not find price"

    def retrieve_product_address(self):
        try:
            self.product_address = "http://www.tigerdirect.com" + self.soup.find('a', {'class': 'itemImage'})['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"


tiger = TigerDirect("core i7")
tiger.retrieve_product_address()
tiger.retrieve_product_price()
print(tiger.product_address, tiger.price)
