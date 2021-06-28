import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys
import os
from typing import Optional, Dict
from common.process_scraper import ProcessScraper

class TargetScraper(ProcessScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Target",
                         search_address=f'https://www.target.com/s?searchTerm={product_model}',
                         using_tor=False,
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username)

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find("span", attrs={"data-test": "product-price"}).text
            
        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

    def retrieve_product_address(self):
        # TODO: Returns None for address
        try:
            product_address_attrs = {"class": "Link-sc-1khjl8b-0 styles__StyledTitleLink-e5kry1-5 cPukFm h-display-block h-text-bold h-text-bs flex-grow-one",
                            "data-test": "product-title"}

            self.product_address = "https://www.target.com" + self.soup.find("a", attrs=product_address_attrs)["href"]

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    target = TargetScraper("lg oled tv")
    target.test()
