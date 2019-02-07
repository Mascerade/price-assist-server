import sys
import os
import random
import bs4
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper


class Rakuten(Scraper):
    def __init__(self, product_model):
        with open(os.getcwd() + "\\user_agents\\scraper.txt", "r") as scrapers:
            headers = {"User-Agent": random.choice(scrapers.read().splitlines())}

        super().__init__(search_address="",
                         product_model=product_model,
                         user_agent=headers,
                         data="")
        