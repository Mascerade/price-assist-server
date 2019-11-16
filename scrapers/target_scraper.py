import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper

class TargetScraper(Scraper):
    def __init__(self, product_model):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        }
        super().__init__(name="Target",
                    search_address='https://www.target.com/s?searchTerm={}'.format(product_model),
                    product_model=product_model,
                    user_agent=self.headers,
                    data="")
                    
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        chrome_path = r"C:\Users\Ultim\Documents\PriceCheccer-Python-Minified\target_scraper\chromedriver.exe"
        self.driver = selenium.webdriver.Chrome(chrome_path, options=options, service_log_path="NUL")
        self.driver.get(self.search_address)

    def retrieve_product_price(self):
        try:
            product_address_attrs = {"class": "h-display-block h-text-bold h-text-bs "
                                              "flex-grow-one styles__StyledTitleLink-ytfmhe-5 "
                                              "hDEDqu Link-sc-1m0vfdz-0 biVtQF",
                                     "data-test": "product-title"}

            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            self.price = soup.find("span", attrs={"data-test": "product-price"}).text
            self.product_address = "https://www.target.com" + soup.find("a", attrs=product_address_attrs)["href"]
            self.driver.close()

        except AttributeError or TypeError:
            self.price = "Could Not Find Price"
            self.driver.close()
