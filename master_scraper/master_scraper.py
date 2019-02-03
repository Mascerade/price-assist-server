import os
import json


class Scraper:
    file = open(os.getcwd() + "/adjs.json", "r")
    adjectives = json.load(file)
    file.close()

    def __init__(self, search_address, product_model, user_agent, data):
        self.price = ""
        self.search_address = search_address
        self.product_address = ""
        self.product_model = product_model
        self.user_agent = user_agent
        self.title = None
        self.data = data
