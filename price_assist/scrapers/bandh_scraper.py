from bs4 import BeautifulSoup
import random
import os
import sys
import requests
import json
from typing import Optional, Dict
from common.process_scraper import ProcessScraper


class BandH(ProcessScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[Dict[str, str]] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="BandH",
                         search_address='https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}&N=0&InitialSearch=yes' \
                                      '&sts=ma&Top+Nav-Search='.format(product_model),
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', attrs={'data-selenium': 'uppedDecimalPriceFirst'}).text.strip() + "." + \
                self.soup.find('sup', attrs={'data-selenium': 'uppedDecimalPriceSecond'}).text.strip()

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://bhphotovideo.com" + self.soup.find("a", attrs={'data-selenium': 'miniProductPageProductNameLink'})['href']

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    bandh = BandH("BX80684I99900K")
    bandh.test()
