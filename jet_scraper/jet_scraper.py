from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Jet(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\scrapers_master.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(name="Jet",
                         search_address='https://jet.com/search?term={}'.format(product_model),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        self.data = requests.get(self.search_address, headers=self.user_agent, timeout=5).text
        self.soup = BeautifulSoup(self.data, "lxml")

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.jet.com" + self.soup.findAll("a", attrs={"class":
                "base__BaseStyledComponent-djfk5g-0 "
                "base__Link-djfk5g-2 BaseProductTile__ItemLink-mors47-0 kIPima"})[0]["href"]

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_price(self):
        try:
            self.price = self.soup.findAll("span", attrs={"class":"core__Box-avlav9-0 typography__"
                                                                  "Text-sc-13794y4-0 jOrchV"})[0].text

        except AttributeError:
            self.price = "Could Not Find Price"

        except TypeError:
            self.price = "Could Not Find Price"

        except Exception as e:
            self.price = "Could Not Find Price"
