from bs4 import BeautifulSoup
import urllib.request


class TigerDirect:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_search_address = 'http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'.format(product_model)
        self.product_address = "None"
        self.headers = {
            'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'
        }

        data = urllib.request.Request(self.product_search_address, headers=self.headers)
        data = urllib.request.urlopen(data).read()
        self.soup = BeautifulSoup(data, "html.parser")

    def retrieve_price(self):
        try:
            self.price = self.soup.find('div', 'salePrice').text

        except AttributeError:
            self.price = "Could not find price"

        except TypeError:
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "http://www.tigerdirect.com" + self.soup.find('a', {'class': 'itemImage'})['href']

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"
