import time
from sys import platform
import requests
from bs4 import BeautifulSoup

class Scraper:
    """
    The "Master" scraper
    Creates unified class for all other scrapers to inherit from
    Keeps properties of objects the same across all scrapers
    * Have to create a variable that stores the amazon title across all of the scraper classes
    * Will make it simpler to keep track of it
    """

    # For linux OS
    REQUIRED_PACKAGES_INSTALLED = True

    # Parameter for if we want to use the proxy
    USING_PROXY = False

    parser = ""
    if platform == "win32" or REQUIRED_PACKAGES_INSTALLED:
        parser = "lxml"


    else:
        parser = "html5lib"

    def __init__(self, name, search_address, product_model, user_agent, data):
        self.time = time.time()
        self.name = name
        self.price = ""
        self.search_address = search_address
        self.product_address = ""
        self.product_model = product_model
        self.user_agent = user_agent
        self.title = None
        self.data = data

        if Scraper.USING_PROXY:        
            payload = {'api_key': '71ed1c68ca01210f236f353690f74549', 'url':self.search_address}
            self.data = requests.get("http://api.scraperapi.com", params=payload, headers=self.user_agent, timeout=5).text

        else:
            self.data = requests.get(self.search_address, headers=self.user_agent, timeout=5).text

        self.soup = BeautifulSoup(self.data, Scraper.parser)

    def retrieve_product_address(self):
        pass

    def retrieve_product_price(self):
        pass

    def get_elapsed_time(self):
        print(str(self.name) + " " + str(time.time() - self.time))

    def test(self):
        self.retrieve_product_address()
        self.retrieve_product_price()
        print(self.price, self.product_address)

    def retrieve_all_information(self):
        scraper_info = []
        self.retrieve_product_address()
        self.retrieve_product_price()
        scraper_info.append(self.name)
        scraper_info.append(self.price)
        scraper_info.append(self.product_address)
        self.get_elapsed_time()
        return scraper_info
