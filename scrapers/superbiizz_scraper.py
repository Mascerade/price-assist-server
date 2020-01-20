from bs4 import BeautifulSoup
import random
import os
import sys
import requests
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class SuperBiiz(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'scrapers_master.txt'), "r") as scrapers:
            header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="SuperBiiz",
                         search_address='https://www.superbiiz.com/query.php?s={}'.format(product_model),
                         product_model=product_model,
                         user_agent=header,
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

        except AttributeError as e:
            self.price = "Could not find price"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.superbiiz.com/" + self.soup.find_all("tr")[45].find("a")["href"]

        except AttributeError as e:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

if __name__ == "__main__":
    superbiiz = SuperBiiz("BX80684I99900K")
    superbiiz.test()
