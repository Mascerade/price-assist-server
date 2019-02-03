from bs4 import BeautifulSoup
import requests
import os
import sys
import random
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class NeweggProduct(Scraper):
    def __init__(self, product_model, amazon_title):
        with open(os.getcwd() + "\\user_agents\\newegg_agents.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        # Initializes the Scraper class with the NeweggProduct
        super().__init__(search_address='https://www.newegg.com/Product/ProductList.aspx?' +\
                                      'Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}'\
                                .format(product_model),
                         product_model=product_model,
                         title=None,
                         user_agent=headers,
                         data="",
                         amazon_title=amazon_title)
        self.prices = []
        self.titles_links = None
        self.data = requests.get(self.search_address, headers=self.user_agent)
        self.data = self.data.text
        self.soup = BeautifulSoup(self.data, 'html.parser')

    def retrieve_product_information(self):
        try:
            # Includes info about link AND actual title
            full_titles = self.soup.find_all("a", attrs={"class": "item-title", "title": "View Details"})[:6]
            titles = []
            links = []

            for index, title in enumerate(full_titles):
                titles.append(title.text)  # Appends the actual title of the product
                links.append(title['href'])  # Appends just the link to the product page of the product

                self.prices.append(self.check_price(self.soup.findAll("li", attrs={"class": "price-current"})[index].text))

            self.titles_links = dict(zip(titles, links))  # Makes the title name the key and the link the value in a dict

        except AttributeError:
            self.product_address = "None"

        except TypeError:
            self.product_address = "None"

        except Exception as e:
            self.product_address = "None"

    def get_best_product(self):
        """

        """

    def check_price(self, price):
        try:
            self.adjusted_price = ""
            stop = False
            for x in price:
                if not stop:
                    if x.isdigit():
                        self.adjusted_price += x

                    elif x == "(":
                        stop = True

                    elif x == ".":
                        self.adjusted_price += x

            if self.adjusted_price.strip(" ") == "":
                self.adjusted_price = None

            else:
                self.adjusted_price = self.adjusted_price.strip(" ")
                return self.adjusted_price

        except AttributeError as e:
            self.adjusted_price = None

        except TypeError as e:
            self.adjusted_price = None

        except Exception as e:
            self.adjusted_price = None

    def print_titles_links(self, dict):
        for key, value in dict.items():
            print(key, ": ", value)


newegg = NeweggProduct("789564-0010",
                       'Bose QuietComfort 35 (Series II) Wireless Headphones, Noise Cancelling, with Alexa voice control - Black')
newegg.retrieve_product_information()
newegg.get_best_product()

