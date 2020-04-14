from bs4 import BeautifulSoup
import random
import os
import sys
import requests
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class SuperBiiz(Scraper):
    def __init__(self, product_model, test_header = None, tor_username = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'user_agents', 'scrapers_master.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}

        if tor_username is None:
            with open("settings.json") as json_file:
                settings = json.load(json_file)

                if settings["location"] == "desktop":
                    with open(os.path.join(os.getcwd(), 'desktop_tor_ips', 'superbiiz_tor_ips.txt')) as superbiiz_tor_ips:
                        tor_username = int(random.choice(superbiiz_tor_ips.read().splitlines()).strip())
                    
                elif settings["location"] == "server":
                    pass

        super().__init__(name="SuperBiiz",
                         search_address='https://www.superbiiz.com/query.php?s={}'.format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         tor_username=tor_username,
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

        except Exception as e:
            self.price = None
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.superbiiz.com/" + self.soup.find_all("tr")[45].find("a")["href"]

        except Exception:
            self.product_address = None

if __name__ == "__main__":
    superbiiz = SuperBiiz("BX80684I99900K")
    superbiiz.test()
