import sys
import os
import random
<<<<<<< HEAD
import requests
import bs4
=======
from bs4 import BeautifulSoup
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
>>>>>>> 210dd2610e3930a693a041cf090d78ac14331042
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Rakuten(Scraper):
    """
    Scrapes Rakuten to get required information
    """

    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\walmart_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}
        super().__init__(search_address="https://www.rakuten.com/search/" + product_model.replace(" ", "%20"),
                         product_model=product_model,
                         user_agent=headers,
                         data="")
<<<<<<< HEAD
=======

        options = Options()
        options.add_argument("user-agent=" + self.user_agent["User-Agent"])
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        chrome_path = r"C:\Users\Ultim\Documents\Price-Assist---Server\target_scraper\chromedriver.exe"
        self.driver = selenium.webdriver.Chrome(chrome_path, options=options, service_log_path="NUL")
        self.data = self.driver.get(self.search_address)
        self.soup = BeautifulSoup(self.driver.page_source, "html.parser")

    def retrieve_product_address(self):
        try:
            self.product_address = self.soup.findAll("a", attrs={"itemprop":"url"})[0]["href"]

        except AttributeError as e:
            print(e)
            self.product_address = "None"

        except TypeError as e:
            print(e)
            self.product_address = "None"

        except Exception as e:
            print(e)
            self.product_address = "None"

    def retrieve_product_price(self):
        try:
            self.price = self.soup.findAll("span", attrs={"class":"r-product__price-text"})[0].text

        except AttributeError as e:
            self.price = "Could Not Find Price"

        except TypeError as e:
            self.price = "Could Not Find Price"

        except Exception as e:
            self.price = "Could Not Find Price"

        finally:
            self.done()

    def done(self):
        self.driver.close()


rakuten = Rakuten("gtx 1080")
rakuten.retrieve_product_address()
rakuten.retrieve_product_price()
print(rakuten.product_address, rakuten.price)
>>>>>>> 210dd2610e3930a693a041cf090d78ac14331042
