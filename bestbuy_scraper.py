from bs4 import BeautifulSoup
import urllib


class BestBuy:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.bestbuy.com/site/searchpage.jsp?st={}&_' \
                                      'dyncharset=UTF-8&id=pcat17071&' \
                                      'type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&' \
                                      'ks=960&keys=keys'.format(product_model)
        self.product_address = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_product_address(self):
        try:
            data = urllib.request.urlopen(self.product_search_address)
            data = data.read()
            soup = BeautifulSoup(data, "html.parser")
            sku_header = soup.find('h4', 'sku-header')
            self.product_address = sku_header.find('a')['href']

        except AttributeError:
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            data = urllib.request.urlopen(self.product_address)
            data = data.read()
            soup = BeautifulSoup(data, "html.parser")
            self.price = soup.find('div', 'priceView-hero-price priceView-purchase-price').text

        else:
            self.price = "Could Not Find Price"
