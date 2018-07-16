from bs4 import BeautifulSoup
import requests


class Walmart:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.walmart.com/search/?query={}&cat_id=3944&typeahead={}' \
                                        .format(product_model, product_model)
        self.product_address = None
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_product_address(self):
        data = requests.get(self.product_search_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        self.product_address = "https://www.walmart.com"+soup.find('a', 'product-title-link line-clamp line-clamp-2')['href']

    def retrieve_product_price(self):
        count = 0
        data = requests.get(self.product_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
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


product = Walmart("X322BV-SR")
product.retrieve_product_address()
product.retrieve_product_price()
print(product.price)
