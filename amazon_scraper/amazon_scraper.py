from bs4 import BeautifulSoup
import requests
import urllib.request
import random


class AmazonProduct:
    def __init__(self, address):
        self.price = ""
        self.model_number = ""
        self.address = address
        self.entry_list = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Silk/44.1.54 like Chrome/44.0.2403.63 Safari/537.36'}

        self.data = urllib.request.Request(self.address, headers=self.headers)
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

        except requests.HTTPError as e:
            print("From Amazon", e)

    def retrieve_item_price(self):
        if self.model_number is None:
            return
        soup = BeautifulSoup(self.data, "lxml")
        try:
            self.price = soup.find("span", id='priceblock_ourprice').text.strip()
        except AttributeError:
            try:
                self.price = soup.find(id='priceblock_dealprice').text.strip()
            except AttributeError:
                self.price = "Price Not Available"
        return
