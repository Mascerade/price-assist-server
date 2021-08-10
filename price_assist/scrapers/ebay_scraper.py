from typing import Optional
from selenium.webdriver.common.by import By
from common.network_scraper import NetworkScraper
from common.stm_scraper import STMScraper

class Ebay(STMScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Ebay",
                         search_address=(f'https://www.ebay.com/sch/i.html?_odkw={product_model}&_nkw={product_model}&_sacat=0'),
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         indicator_element=[By.ID, 'srp-river-results'])

        self.product_address = self.search_address
    
    def retrieve_product_price(self):
        try:
            self.price = self.soup.find_all('span', attrs={'class': 's-item__price'})[0].text

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    ebay = Ebay("BX80684I99900K")
    ebay.test()
