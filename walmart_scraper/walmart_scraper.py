from bs4 import BeautifulSoup
import requests
import os
import random


class Walmart:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.walmart.com/search/?query={}'.format(product_model, product_model)
        self.product_address = "None"
        with open(os.getcwd() + "\\user_agents\\walmart_agents.txt", "r") as scrapers:
            self.headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

    def retrieve_product_address(self):
        try:
            data = requests.get(self.product_search_address, headers=self.headers)
            data = data.text
            soup = BeautifulSoup(data, "lxml")
            self.product_address = "https://www.walmart.com" + \
                                   soup.find('a', 'product-title-link line-clamp line-clamp-2')['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_address is not "None":
            try:
                count = 0
                data = requests.get(self.product_address, headers=self.headers)
                data = data.text
                soup = BeautifulSoup(data, "lxml")
                price = soup.find('div', 'prod-PriceHero').text
                for letter in price:
                    if letter == "$":
                        count += 1
                        if count == 2:
                            return
                        else:
                            self.price += letter
                    else:
                        self.price += letter

            except AttributeError:
                self.price = "Could Not Find Price"

            except TypeError:
                self.price = "Could Not Find Price"

            except Exception as e:
                self.price = "Could Not Find Price"

        else:
            self.price = "Could Not Find Price"
