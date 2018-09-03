from bs4 import BeautifulSoup
import urllib.request


class TigerDirect:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_address = 'http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'.format(product_model)
        self.headers = {
            'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'
        }

    def retrieve_price(self):

        try:
            print(self.product_address)
            data = urllib.request.Request(self.product_address, headers=self.headers)
            data = urllib.request.urlopen(data).read()
            soup = BeautifulSoup(data, "html.parser")
            self.price = soup.find('div', 'salePrice').text
            temp = soup.find('span', 'oldPrice').text
            self.price = self.price.replace(temp, '')

        except AttributeError as e:
            print(e)
            print(self.product_address)
            self.price = "Could not find price"
