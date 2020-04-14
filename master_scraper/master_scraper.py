import time
from sys import platform
import os
import requests
import random
from bs4 import BeautifulSoup
import time
import subprocess
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Scraper:
    # TODO: Make the user agent thing universal so I can put it here
    # TODO: Test user agents for each scraper
    
    """
    The "Master" scraper
    Creates unified class for all other scrapers to inherit from
    Keeps properties of objects the same across all scrapers
    * Have to create a variable that stores the amazon title across all of the scraper classes
    * Will make it simpler to keep track of it
    """

    # For linux OS
    REQUIRED_PACKAGES_INSTALLED = True

    # Parameter for if we want to use selenium
    USING_SELENIUM = True

    # Parameter to control type of webdriver
    USING_CHROME = True

    parser = ""
    if platform == "win32" or REQUIRED_PACKAGES_INSTALLED:
        parser = "lxml"

    else:
        parser = "html5lib"
    
    def __init__(self, name, search_address, product_model, user_agent, data, tor_username = None, use_selenium = False):
        self.time = time.time()
        self.name = name
        self.price = ""
        self.search_address = search_address
        self.product_address = ""
        self.product_model = product_model
        self.user_agent = user_agent
        self.title = None
        self.data = data
        self.tor_username = tor_username
        if self.tor_username is None:
            self.tor_username = random.randint(1, 100000)
        self.use_selenium = use_selenium

        if Scraper.USING_SELENIUM and self.use_selenium:
            proxies = {
                "http": "socks5h://" + str(self.tor_username) + ":idk@localhost:9050",
                "https": "socks5h://" + str(self.tor_username) + ":idk@localhost:9050"
                }

            try:
                if Scraper.USING_CHROME:
                    display = Display(visible=0, size=(800, 600))
                    display.start()
                    caps = DesiredCapabilities().CHROME
                    caps["pageLoadStrategy"] = "normal"
                    options = Options()
                    options.add_argument('--no-sandbox')
                    # options.add_argument('--window-size=1420,1080')
                    # options.add_argument('--headless')
                    options.add_argument('--disable-gpu')
                    driver = webdriver.Chrome(options=options, desired_capabilities=caps, executable_path="/usr/local/share/chromedriver")
                    driver.get(self.search_address)

                else:
                    binary = FirefoxBinary("/usr/lib/firefox/firefox")
                    caps = DesiredCapabilities().FIREFOX
                    caps["pageLoadStrategy"] = "normal"
                    options = webdriver.firefox.options.Options()
                    options.add_argument("--headless")
                    proxy = "socks5h://" + str(self.tor_username) + ":idk@localhost:9050"
                    options.add_argument("--proxy-server=" + proxy)
                    options.add_argument("--id=" + str(self.tor_username))
                    driver = webdriver.Firefox(options=options, firefox_binary=binary, desired_capabilities=caps, executable_path=os.path.join(os.getcwd(), "gecko_driver/geckodriver"))
                    driver.get(self.search_address)
                if (self.name == "Rakuten" or self.name == "Target"):
                    time.sleep(3)
                self.data = driver.page_source

            except Exception as e:
                print(str(e))
                self.price = "None"
                self.product_address = "None"

            finally:
                #driver.close()
                #display.stop()
                pass

        else:        
            proxies = {
                "http": "socks5h://" + str(self.tor_username) + ":idk@localhost:9050",
                "https": "socks5h://" + str(self.tor_username) + ":idk@localhost:9050"
                }

            try:
                self.data = requests.get(self.search_address, proxies=proxies, headers=self.user_agent, timeout=5).text

            except Exception as e:
                self.price = "None"
                self.product_address = "None"

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
