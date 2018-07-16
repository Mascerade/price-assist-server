from bs4 import BeautifulSoup
import requests


class BestBuy:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.bestbuy.com/site/searchpage.jsp?st={}&_dyncharset=UTF-8&id=pcat17071&' \
                                      'type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&' \
                                      'ks=960&keys=keys'.format(product_model)
        self.product_address = None
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }

    def retrieve_product_address(self):
        data = requests.get(self.product_search_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        skuTitle = soup.find('div', 'sku-title')
        self.product_address = "https://www.bestbuy.com" + skuTitle.find('a')['href']

    def retrieve_product_price(self):
        data = requests.get(self.product_address, headers=self.headers)
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        print(soup.find('div', 'priceView-hero-price priceView-purchase-price').text)

product = BestBuy("XBR65X900F")
product.retrieve_product_address()
product.retrieve_product_price()
