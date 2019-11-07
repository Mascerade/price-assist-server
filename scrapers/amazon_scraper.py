from bs4 import BeautifulSoup
import requests
import random
import os
import sys

sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class AmazonProduct(Scraper):
    def __init__(self, address):
        try:
            with open(os.path.join(os.getcwd(), 'user_agents', 'amazon_agents_refined.txt'), "r") as scrapers:
                user_agent = {"User-Agent": random.choice(scrapers.read().splitlines())}
            super().__init__(name="Amazon", search_address=address, product_model=None, user_agent=user_agent, data="")
            self.entry_list = []
            self.data = requests.get(self.search_address, headers=self.user_agent).text
            self.soup = BeautifulSoup(self.data, Scraper.parser)
            self.error = ""
            self.title = ""

        except Exception as e:
            print(e)

    def retrieve_item_model(self):
        try:
            self.title = self.soup.find(id="productTitle").text.strip()
            for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                for row in self.soup.find_all(id='productDetails_techSpec_section_' + str(number)):
                    for tr in row.find_all('tr'):
                        self.entry_list.append(tr.text.strip())

            for row in self.soup.find_all(id='productDetails_detailBullets_sections1'):
                for tr in row.find_all('tr'):
                    self.entry_list.append(tr.text.strip())

            for x in self.entry_list:
                if "Item model number" in x:
                    self.product_model = x[17:].strip()

        except AttributeError as e:
            self.error = e
            self.product_model = None

        except TypeError as e:
            self.error = e
            self.product_model = None

        except requests.HTTPError as e:
            self.error = e
            print("From Amazon", e)

        except Exception as e:
            self.error = e
            self.product_model = None

    def retrieve_item_price(self):
        try:
            self.price = self.soup.find("span", id='priceblock_ourprice').text.strip()
        except AttributeError or TypeError:
            try:
                self.price = self.soup.find(id='priceblock_dealprice').text.strip()
            except AttributeError or TypeError:
                self.price = "Price Not Available"

        except Exception:
            self.price = "Price Not Available"

        return


class Amazon(Scraper):
    def __init__(self, product_model):
        with open(os.path.join(os.getcwd(), 'user_agents', 'amazon_agents_refined.txt'), "r") as scrapers:
            header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(name="Amazon",
                         search_address='https://www.amazon.com/s?k={}&i=electronics&ref=nb_sb_noss'.format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         data="")
        try:
            data = requests.get(self.search_address, headers=self.user_agent).text
            self.soup = BeautifulSoup(data, Scraper.parser)

        except Exception as e:
            self.price = "Could not find price"
            self.product_address = "None"

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("span", attrs={"class": "a-offscreen"})[0].text

        except AttributeError as e:
            self.price = "Could not find price"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.amazon.com" + \
                                   self.soup.find_all("a", attrs={"class": "a-link-normal a-text-normal"})[0]['href']

        except AttributeError as e:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"
