from bs4 import BeautifulSoup
import urllib.request


class Microcenter:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_model = self.product_model.replace(" ", "%20")
        self.product_search_address = 'https://www.microcenter.com/search/' \
                                      'search_results.aspx?Ntt={}'.format(product_model)
        self.product_address = "None"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }
        try:
            data = urllib.request.Request(self.product_search_address)
            data.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')
            data = urllib.request.urlopen(data)
            data = data.read()

        except Exception as e:
            self.price = "Could not find price"

        self.soup = BeautifulSoup(data, "lxml")

    def retrieve_price(self):
        try:
            self.price = self.soup.find('span', {"itemprop":"price"}).text

        except AttributeError:
            self.price = "Could not find price"

        except Exception as e:
            self.price = "Could not find price"

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.microcenter.com" + self.soup.find("a", attrs={"id": "hypProductH2_0"})["href"]

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.price = "Could not find price"

