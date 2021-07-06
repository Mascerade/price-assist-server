import time
import json
from sys import platform
import sys
import os
import requests
import random
from bs4 import BeautifulSoup
import time
import logging
from typing import Optional, Dict, List
from common.common_path import CommonPaths


class Scraper:
    # TODO: Make the user agent thing universal so I can put it here
    # TODO: Test user agents for each scraper
    
    """
    The scraper
    Creates unified class for all other scrapers to inherit from
    Keeps properties of objects the same across all scrapers
    * Have to create a variable that stores the amazon title across all of the scraper classes
    * Will make it simpler to keep track of it
    """

    # Set the parser to use for BeautifulSoup
    PARSER: str = "lxml"
    
    def __init__(self,
                 name: str,
                 product_model: str,
                 search_address: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        self.time = time.time()
        self.name = name
        self.product_model = product_model
        self.search_address = search_address
        self.using_tor = using_tor
        self.user_agent: Dict[str, str] = {}
        self.tor_username: Optional[int] = None
        
        self.data: str = ""
        self.price: Optional[str] = None
        self.product_address: Optional[str] = None
        self.title: Optional[str] = None
        self.request_data: str = ""
        self.soup: Optional[BeautifulSoup] = None
        
        # Logger is based on the name of the scraper (easy to find)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # The file is based on the name as well
        fh = logging.FileHandler(f'logging/{name}.log')
        self.logger.addHandler(fh)

        # For testing, we pass in a user agent, so if there is no testing, then find a user agent from CommonPaths
        if test_user_agent is None:
            self.user_agent = {"User-Agent": random.choice(CommonPaths.SCRAPER_USER_AGENTS[self.name.lower()]), "referer": "https://www.google.com/"}

        # Only if testing
        else:
            self.user_agent = {"User-Agent": test_user_agent}

        # Again, if we're not testing, use the username from CommonPaths
        if test_tor_username is None and self.using_tor:
            scraper_tor_ips: Optional[List[str]] = CommonPaths.SCRAPER_TOR_IPS[self.name.lower()]
            if scraper_tor_ips is None:
                self.tor_username = random.randint(1, 10000)

            else:
                self.tor_username = int(random.choice(scraper_tor_ips).replace(" ", ""))

        # Only if testing
        else: 
            self.tor_username = test_tor_username
    
    def retrieve_soup(self) -> None:
        pass

    def retrieve_product_address(self) -> None:
        pass

    def retrieve_product_price(self) -> None:
        pass

    def get_elapsed_time(self):
        print(str(self.name) + " " + str(time.time() - self.time))

    def test(self):
        self.retrieve_product_address()
        self.retrieve_product_price()
        print(self.price, self.product_address)

    def retrieve_all_information(self):
        # scraper_info = []
        self.retrieve_soup()
        self.retrieve_product_address()
        self.retrieve_product_price()
        # scraper_info.append(self.name)
        # scraper_info.append(self.price)
        # scraper_info.append(self.product_address)
        self.get_elapsed_time()
        # return scraper_info

    def access_error(self, function_name):
        error_found = False
        for word in CommonPaths.SCRAPER_ERROR_WORDS:
            if (word in str(self.soup).lower()):
                self.logger.error(time.ctime(time.time()))

        if not error_found:
            self.logger.warning(time.ctime(time.time()) + ': Did not find the product ' + self.product_model)

    def unhandled_error(self, error, function_name):
        self.logger.error(time.ctime(time.time()) + ': Unhandled type of error: ' + str(error) + '. ' + function_name)

    def as_dict(self) -> Dict[str, Optional[str]]:
        return {
            'retailer': self.name.lower(),
            'price': self.price,
            'product_address': self.product_address
        }
