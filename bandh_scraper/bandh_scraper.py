from bs4 import BeautifulSoup
import urllib.request


class BandH:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model)
        self.product_address = "None"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

        data = urllib.request.urlopen(self.product_search_address)
        data = data.read()
        self.soup = BeautifulSoup(data, "html.parser")

    def retrieve_price(self):
        try:
            self.price = self.soup.find('span', 'itc-you-pay-price bold').text.strip()

        except AttributeError:
            self.price = "Could not find price"

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find("a", attrs={'class': 'c5', 'data-selenium': 'itemHeadingLink', 'itemprop': 'url'})['href']
        except AttributeError:
            self.product_address = "None"
