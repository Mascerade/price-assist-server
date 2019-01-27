class Scraper():
    def __init__(self, search_address, product_model, user_agent, data):
        self.price = ""
        self.search_address = search_address
        self.product_address = ""
        self.product_model = product_model
        self.user_agent = user_agent
        self.data = data


class SubScraper(Scraper):
    def __init__(self, product_model):
        super().__init__("search_address", product_model, "user_agent", "data")

