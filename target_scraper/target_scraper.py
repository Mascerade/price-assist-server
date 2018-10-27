import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class TargetScraper:
    def __init__(self, product_model):
        self.price = ""
        self.product_model = product_model
        self.product_address = 'https://www.target.com/s?searchTerm={}'.format(product_model, product_model)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }
        options = Options()
        options.add_argument('--headless')
        self.driver = selenium.webdriver.Chrome(options=options)
        self.data = self.driver.get(self.product_address)

    def retrieve_product_price(self):
        try:
            print(self.data.page_source)
            soup = BeautifulSoup(self.data.page_source, "lxml")
            print(soup)

        except AttributeError:
            self.price = "Could Not Find Price"


target = TargetScraper("xbox")
target.retrieve_product_price()
