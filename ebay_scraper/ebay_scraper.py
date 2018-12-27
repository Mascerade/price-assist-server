from bs4 import BeautifulSoup
import urllib.request
import random
import os


class Ebay:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_address = 'https://www.ebay.com/sch/i.html?_odkw={}&_osacat=0&_from=R40&_' \
                               'trksid=p2045573.m570.l1313.TR1.TRC0.A0.H0.TRS1&_nkw={}&_' \
                               'sacat=0'.format(product_model, product_model)
        with open(os.getcwd() + "\scrapers.txt", "r") as scrapers:
            self.user_agent = {"User-Agent": random.choice(scrapers.read().splitlines())}

    def retrieve_product_price(self):
        try:
            data = urllib.request.urlopen(self.product_address)
            data = data.read()
            soup = BeautifulSoup(data, "lxml")
            price = soup.find_all('span', 's-item__price')[0].text
            self.price = price

        except AttributeError:
            self.price = "Could Not Find Price"

        except TypeError:
            self.price = "Could Not Find Price"

        except Exception as e:
            self.price = "Could Not Find Price"
