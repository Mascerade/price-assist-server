from bs4 import BeautifulSoup
import urllib.request
import requests


class NeweggProduct:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.newegg.com/Product/ProductList.aspx?' +\
                                      'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}'\
                                .format(self.product_model)
        self.product_address = ""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.102 Safari/537.36'
        }

    def retrieve_product_address(self):
        try:
            data = urllib.request.urlopen(self.product_search_address)
            data = data.read()
            soup = BeautifulSoup(data, 'lxml')
            self.product_address = soup.find("a", attrs={"class": "item-title", "title": "View Details"})['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                data = requests.get(self.product_search_address, headers=self.headers)
                data = data.text
                soup = BeautifulSoup(data, 'html.parser')
                self.price = "$"
                stop = False
                for x in soup.find("li", "price-current").text:
                    if not stop:
                        if x.isdigit():
                            self.price += x

                        elif x == "(":
                            stop = True

                        elif x == "." or x == ",":
                            self.price += x

                self.price = self.price.strip(" ")

            except AttributeError as e:
                self.price = "Could Not Find Price"

            except TypeError as e:
                self.price = "Could Not Find Price"

        else:
            self.price = "Could Not Find Price"

