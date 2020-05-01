from bs4 import BeautifulSoup
import requests
import random
import os
import sys
import json
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper
import logging

logging.basicConfig(filename='logging/amazon.log', level=logging.DEBUG)
class Amazon(Scraper):
    """
    We now have 4 scrapers that are essentially gaurenteed to work
    """
    def __init__(self, product_model, test_user_agent = None, test_tor_username = None):
        super().__init__(name="Amazon",
                         search_address='https://www.amazon.com/s?k={}&i=electronics&ref=nb_sb_noss'.format(product_model),
                         product_model=product_model,
                         test_tor_username=test_tor_username,
                         test_user_agent = test_user_agent,
                         data="")
                         
    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all("span", attrs={"class": "a-offscreen"})[0].text

        except (AttributeError, IndexError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            for word in Scraper.SCRAPER_ERROR_WORDS:
                if (word in str(self.soup).lower()):
                    logging.error('Could not access Amazon. User Agent: ' + str(self.user_agent) + ' Tor Username: ' + str(self.tor_username) + ". From retrieve_product_price()")
                    break
            self.price = None

        except Exception as e:
            logging.error('Unhandled type of error: ' + str(e) + '. From retrieve_product_price()')
            # I don't think it is necessary to do this
            # self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://www.amazon.com" + \
                                   self.soup.find_all("a", attrs={"class": "a-link-normal a-text-normal"})[0]['href']
        
        except (AttributeError, IndexError) as e:
            for word in Scraper.SCRAPER_ERROR_WORDS:
                if (word in str(self.soup).lower()):
                    logging.error('Could not access Amazon. User Agent: ' + str(self.user_agent) + ' Tor Username: ' + str(self.tor_username) + ". From retrieve_product_address()")
                    break
            self.product_address = None

        except Exception as e:
            logging.error('Unhandled type of error: ' + str(e) + '. From retrieve_product_address()')
            self.product_address = None

if __name__ == "__main__":
    amazon = Amazon("asus vivobook")
    amazon.test()
