import time
import json
from sys import platform
import sys
import os
import requests
import random
from bs4 import BeautifulSoup
import time
import subprocess
import logging
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from common.common_path import CommonPaths


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

    # This is going to be a dictionary of all the settings loaded from settings.json
    SETTINGS = {}

    SCRAPER_ERROR_WORDS = ["404", "automated", "access", "captcha"]

    if os.path.exists("settings.json"):
        # Location (from settings.json)
        with open("settings.json") as json_file:
            settings = json.load(json_file)
            SETTINGS = settings

    parser = ""
    if platform == "win32" or REQUIRED_PACKAGES_INSTALLED:
        parser = "lxml"

    else:
        parser = "html5lib"
    
    def __init__(self, name, search_address, product_model, data, test_user_agent = None, test_tor_username = None, use_selenium = False):
        self.time = time.time()
        self.name = name
        self.price = ""
        self.search_address = search_address
        self.product_address = ""
        self.product_model = product_model
        self.user_agent = test_user_agent
        self.title = None
        self.data = data
        self.tor_username = test_tor_username
        self.use_selenium = use_selenium
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('logging/' + name.lower() + '.log')
        self.logger.addHandler(fh)

        # For testing, we pass in a user agent, so if there is no testing, then find a user agent from CommonPaths
        if test_user_agent is None:
            self.user_agent = {"User-Agent": random.choice(CommonPaths.SCRAPER_USER_AGENTS[self.name.lower()]), "referer": "https://www.google.com/"}

        # Only if testing
        else:
            self.user_agent = {"User-Agent": test_user_agent}

        # Again, if we're not testing, use the username from CommonPaths
        if test_tor_username is None:
            if CommonPaths.SCRAPER_TOR_IPS[name.lower()] is None:
                self.tor_username = random.randint(1, 10000)

            else:
                self.tor_username = int(random.choice(CommonPaths.SCRAPER_TOR_IPS[self.name.lower()]).replace(" ", ""))

        # Only if testing
        else: 
            self.tor_username = test_tor_username

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
                self.data = requests.get(self.search_address, headers=self.user_agent, timeout=5).text

            except Exception as e:
                self.unhandled_error(e, 'Making request in master_scraper.py')
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

    def access_error(self, function_name):
        error_found = False
        for word in Scraper.SCRAPER_ERROR_WORDS:
            if (word in str(self.soup).lower()):
                self.logger.error(time.ctime(time.time()) + ': Could not access ' + self.name + '. User Agent: ' + self.user_agent['User-Agent'] + ' Tor Username: ' + str(self.tor_username) + ". From " + function_name)
                error_found = True
                break
        
        if not error_found:
            self.logger.warning(time.ctime(time.time()) + ': Did not find the product ' + self.product_model)

    def unhandled_error(self, error, function_name):
        self.logger.error(time.ctime(time.time()) + ': Unhandled type of error: ' + str(error) + '. ' + function_name)
