import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper

class TargetScraper(Scraper):
    def __init__(self, product_model, test_header = None, tor_username = None):
        super().__init__(name="Target",
                    search_address='https://www.target.com/s?searchTerm={}'.format(product_model),
                    product_model=product_model,
                    use_selenium=True,
                    data="")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find("span", attrs={"data-test": "product-price"}).text
            
        except AttributeError or TypeError:
            self.price = None

    def retrieve_product_address(self):
        try:
            product_address_attrs = {"class": "Link-sc-1khjl8b-0 styles__StyledTitleLink-e5kry1-5 cPukFm h-display-block h-text-bold h-text-bs flex-grow-one",
                            "data-test": "product-title"}

            self.product_address = "https://www.target.com" + self.soup.find("a", attrs=product_address_attrs)["href"]

        except Exception:
            self.product_address = None

if __name__ == "__main__":
    target = TargetScraper("lg oled tv")
    target.test()
