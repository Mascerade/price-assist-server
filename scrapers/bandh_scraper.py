from bs4 import BeautifulSoup
import random
import os
import sys
import requests
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class BandH(Scraper):
    def __init__(self, product_model, test_header = None):
        if test_header is None:
            with open(os.path.join(os.getcwd(), 'user_agents', 'bandh_agents.txt'), "r") as scrapers:
                header = {"User-Agent": random.choice(scrapers.read().splitlines())}

        else:
            header = {"User-Agent": test_header}

        super().__init__(name="B&H",
                         search_address='https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model),
                         product_model=product_model,
                         user_agent=header,
                         data="")

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', 'itc-you-pay-price bold').text.strip()

        except Exception:
            self.price = None
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.find("a", attrs={'class': 'c5', 'data-selenium': 'itemHeadingLink', 'itemprop': 'url'})['href']

        except Exception:
            self.product_address = None

if __name__ == "__main__":
    bandh = BandH("BX80684I99900K")
    bandh.test()
