from bs4 import BeautifulSoup
import requests


class AmazonProduct:
    def __init__(self, address):
        self.price = ""
        self.model_number = ""
        self.address = address
        self.entry_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/41.0.2228.0 Safari/537.36',
        }

    def retrieve_item_model(self):
        try:
            data = requests.get(self.address, headers=self.headers)
            soup = BeautifulSoup(data.text, "html.parser")
            for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                for row in soup.find_all(id='productDetails_techSpec_section_' + str(number)):
                    for tr in row.find_all('tr'):
                        self.entry_list.append(tr.text.strip())

            for row in soup.find_all(id='productDetails_detailBullets_sections1'):
                for tr in row.find_all('tr'):
                    self.entry_list.append(tr.text.strip())

            for x in self.entry_list:
                if "Item model number" in x:
                    self.model_number = x[17:].strip()

        except AttributeError:
            self.model_number = None

    def retrieve_item_price(self):
        if self.model_number is None:
            return
        data = requests.get(self.address, headers=self.headers)
        soup = BeautifulSoup(data.text, "html.parser")
        self.price = soup.find(id='priceblock_ourprice').text.strip()
