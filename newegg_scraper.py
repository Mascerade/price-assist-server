from bs4 import BeautifulSoup
import requests


class NeweggProduct:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.newegg.com/Product/ProductList.aspx?' +\
                            'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}&N=-1&isNodeId=1'\
                                .format(self.product_model)
        self.product_address = None
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/41.0.2228.0 Safari/537.36',
        }

    def retrieve_product_address(self):
        data = requests.get(self.product_search_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, 'html.parser')
        for product in soup.find_all('div', 'item-container'):
            self.product_address = product.find('a').text

    def retrieve_product_price(self):
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        data = requests.get(self.product_search_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, 'html.parser')
        counter = 0
        for price in soup.find_all('li', 'price-current'):
            for x in price.text.strip():
                if counter == 2:
                    self.price += x
                    counter += 1
                    return
                elif counter == 1:
                    self.price += x
                    counter += 1
                elif x == ".":
                    counter += 1
                    self.price += x
                elif x in numbers or x == "$":
                    self.price += x
