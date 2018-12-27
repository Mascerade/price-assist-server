from bs4 import BeautifulSoup
import requests
import urllib.request
import random
import os


class AmazonProduct:
    def __init__(self, address):
        print(os.getcwd())
        with open(os.getcwd() + "\\amazon_agents.txt", "r") as scrapers:
            self.user_agent = {"User-Agent": random.choice(scrapers.read().splitlines())}
            print(self.user_agent)
        self.price = ""
        self.model_number = ""
        self.address = address
        self.entry_list = []
        self.data = urllib.request.Request(self.address, headers=self.user_agent)
        self.data = urllib.request.urlopen(self.data).read()

    def retrieve_item_model(self):
        try:
            soup = BeautifulSoup(self.data, "lxml")
            for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                for row in soup.find_all(id='productDetails_techSpec_section_' + str(number)):
                    for tr in row.find_all('tr'):
                        self.entry_list.append(tr.text.strip())

            for row in soup.find_all(id='productDetails_detailBullets_sections1'):
                for tr in row.find_all('tr'):
                    self.entry_list.append(tr.text.strip())
            for x in self.entry_list:
                if "Item model number" in x:
                    self.model_number = x[17:].strip()

        except AttributeError:
            self.model_number = None

        except TypeError:
            self.model_number = None

        except Exception:
            self.model_number = None

        except requests.HTTPError as e:
            print("From Amazon", e)

    def retrieve_item_price(self):
        if self.model_number is None:
            return
        soup = BeautifulSoup(self.data, "lxml")
        try:
            self.price = soup.find("span", id='priceblock_ourprice').text.strip()
        except AttributeError or TypeError:
            try:
                self.price = soup.find(id='priceblock_dealprice').text.strip()
            except AttributeError or TypeError:
                self.price = "Price Not Available"

        except Exception:
            self.price = "Price Not Available"

        return
