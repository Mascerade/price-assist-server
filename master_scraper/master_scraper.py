import time
from sys import platform


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

    def retrieve_product_address(self):
        pass

    def retrieve_product_price(self):
        pass

    def get_elapsed_time(self):
        print(str(self.name) + " " + str(time.time() - self.time))
