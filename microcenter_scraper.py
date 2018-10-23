from bs4 import BeautifulSoup
import urllib.request


class Microcenter:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_address = 'https://www.microcenter.com/search/' \
                               'search_results.aspx?Ntt={}'.format(product_model)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_price(self):
        try:
            data = urllib.request.urlopen(self.product_address)
            data = data.read()
            soup = BeautifulSoup(data, "lxml")
            self.price = soup.find('span', {"itemprop":"price"}).text

        except AttributeError:
            self.price = "Could not find price"

