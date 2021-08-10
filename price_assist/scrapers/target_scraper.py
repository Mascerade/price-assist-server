from typing import Optional
from selenium.webdriver.common.by import By
from common.process_scraper import ProcessScraper
from common.stm_scraper import STMScraper

class Target(STMScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="Target",
                         search_address=f'https://www.target.com/s?searchTerm={product_model}',
                         using_tor=using_tor,
                         product_model=product_model,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         indicator_element=[By.XPATH, "//div[@data-test='product-list-container']"])

    def retrieve_product_address(self):
        try:
            product_address_attrs = {"data-test": "product-title"}
            self.product_address = "https://www.target.com" + self.soup.find("a", attrs=product_address_attrs)["href"]

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find("div", attrs={"data-test": "current-price"}).text
            
        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None

if __name__ == "__main__":
    target = Target("lg oled tv")
    target.test()
