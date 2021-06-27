from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup

from .base_scraper import Scraper

class NetworkScraper(Scraper):
    '''
    A NetworkScraper is the simpler scraper. It only uses Requests to get the data
    needed to scrape the website. There is no web driver or heavy application used.
    '''
    def __init__(self,
                 name: str,
                 product_model: str,
                 search_address: str,
                 using_tor: bool,
                 test_user_agent: Optional[Dict[str, str]] = None,
                 test_tor_username: Optional[int] = None,
                ):
        super().__init__(
            name = name,
            product_model=product_model,
            search_address=search_address,
            using_tor=using_tor,
            test_user_agent=test_user_agent,
            test_tor_username=test_tor_username
        )


    def retrieve_soup(self):
        '''
        For a network scraper, go to the search address using Requests and create the soup
        '''
        
        try:
            self.data = requests.get(self.search_address, headers=self.user_agent, timeout=5).text

        except Exception as e:
            print(e)
            self.unhandled_error(e, 'Making request in base_scraper.py')
            self.price = None
            self.product_address = None

        self.soup = BeautifulSoup(self.data, Scraper.PARSER)