from bs4 import BeautifulSoup
import urllib.request


class BandH:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model)
        self.product_address = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_price(self):
        data = urllib.request.urlopen(self.product_search_address)
        data = data.read()
        soup = BeautifulSoup(data, "html.parser")
        self.price = soup.find('span', 'price bold sixteen c7').text.strip()


product = BandH("xbr65x900f")
product.retrieve_price()
