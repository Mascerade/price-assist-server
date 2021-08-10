from typing import Optional
from selenium.webdriver.common.by import By
from common.network_scraper import NetworkScraper
from common.stm_scraper import STMScraper

class TigerDirect(STMScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="TigerDirect",
                         search_address=f'http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={product_model}',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         indicator_element=[By.CLASS_NAME, 'sku-display'])

    def retrieve_product_price(self):
        try:
            count = 0
            self.price = self.soup.find('p', attrs={'class': 'price'}).text
            if self.price is None:
                self.price = self.soup.find('p', attrs={'class': 'salePrice'}).text
            if self.price.count("$") > 1:
                for index, x in enumerate(self.price):
                    if x == "$" and count > 0:
                        self.price = self.price[index:]
                        break
                    if x == "$":
                        count += 1

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

    def retrieve_product_address(self):
        try:
            self.product_address = "http://www.tigerdirect.com" + self.soup.find('a', {'class': 'itemImage'})['href']

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    tiger = TigerDirect("ryzen 7")
    tiger.test()
