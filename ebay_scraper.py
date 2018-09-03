from bs4 import BeautifulSoup
import requests


class Ebay:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_address = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311.R1' \
                                      '.TR2.TRC1.A0.H0.{}.' \
                                      'TRS0&_nkw=49s405&_sacat=0'.format(product_model, product_model)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_product_price(self):
        try:
            data = requests.get(self.product_address, headers=self.headers)
            data = data.text
            soup = BeautifulSoup(data, "html.parser")
            price = soup.find('span', 's-item__price').text
            self.price = price

        except AttributeError:
            self.price = "Could Not Find Price"
