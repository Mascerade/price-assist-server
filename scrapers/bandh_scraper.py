from bs4 import BeautifulSoup
import random
import os
import sys
import requests
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class BandH(Scraper):
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="B&H",
                         search_address='https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model),
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         data="")

    def retrieve_product_price(self):
        try:
            
            self.price = self.soup.find('span', attrs={'data-selenium': 'uppedDecimalPriceFirst'}).text.strip() + "." + \
                self.soup.find('sup', attrs={'data-selenium': 'uppedDecimalPriceSecond'}).text.strip()

        except Exception as e:
            self.price = None
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://bhphotovideo.com" + self.soup.find("a", attrs={'data-selenium': 'miniProductPageProductNameLink'})['href']

        except Exception:
            self.product_address = None

if __name__ == "__main__":
    bandh = BandH("BX80684I99900K")
    bandh.test()
