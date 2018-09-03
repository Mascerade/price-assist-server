from bs4 import BeautifulSoup
import requests


class AmazonProduct:
    def __init__(self, address):
        self.price = ""
        self.model_number = ""
        self.address = address
        self.entry_list = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; LG-H345 Build/LMY47V) AppleWebKit/537.36 ' +
                          '(KHTML, like Gecko) Chrome/43.0.2357.78 Mobile Safari/537.36 OPR/30.0.1856.93524',
        }

        self.data = requests.get(self.address, headers=self.headers)

    def retrieve_item_model(self):
        try:
            soup = BeautifulSoup(self.data.text, "html.parser")
            for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                for row in soup.find_all(id='productDetails_techSpec_section_' + str(number)):
                    for tr in row.find_all('tr'):
                        self.entry_list.append(tr.text.strip())

            for row in soup.find_all(id='productDetails_detailBullets_sections1'):
                for tr in row.find_all('tr'):
                    self.entry_list.append(tr.text.strip())
            print(self.entry_list)
            for x in self.entry_list:
                if "Item model number" in x:
                    self.model_number = x[17:].strip()

        except AttributeError:
            self.model_number = None

        except requests.HTTPError as e:
            print("From Amazon", e)

    def retrieve_item_price(self):
        soup = BeautifulSoup(self.data.text, "html.parser")
        a = soup.find(id='priceblock_ourprice').text.strip()
        print(a)
