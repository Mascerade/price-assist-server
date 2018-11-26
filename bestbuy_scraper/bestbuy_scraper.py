from bs4 import BeautifulSoup
import urllib.request


class BestBuy:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'https://www.bestbuy.com/site/searchpage.jsp?st={}'.format(product_model)
        self.product_address = "None"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36',
        }
        data = urllib.request.Request(self.product_search_address, headers=self.headers)
        data = urllib.request.urlopen(data).read()
        self.soup = BeautifulSoup(data, "html.parser")

    def retrieve_product_address(self):
        try:
            sku_header = self.soup.find('h4', 'sku-header')
            self.product_address = sku_header.find('a')['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

    def retrieve_product_price(self):
        if self.product_search_address is not None:
            self.price = self.soup.find('div', 'priceView-hero-price priceView-purchase-price').text

        else:
            self.price = "Could Not Find Price"
