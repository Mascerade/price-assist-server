from bs4 import BeautifulSoup
import urllib.request
import os
import random

class TigerDirect:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'.format(product_model)
        self.product_address = "None"
        with open(os.getcwd() + "\\user_agents\\tigerdirect_agents.txt", "r") as scrapers:
            self.headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        try:
            data = urllib.request.Request(self.product_search_address, headers=self.headers)
            data = urllib.request.urlopen(data).read()
            self.soup = BeautifulSoup(data, "html.parser")

        except Exception as e:
            self.price = "Could not find price"

    def retrieve_price(self):
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
