from typing import Optional
from selenium.webdriver.common.by import By
from common.process_scraper import ProcessScraper
from common.stm_scraper import STMScraper


class BandH(STMScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="BandH",
                         search_address='https://www.bhphotovideo.com/c/search?' \
                                      'Ntt={}'.format(product_model),
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         indicator_element=[By.XPATH, "//div[@data-selenium='listingProductDetailSection']"])

    def retrieve_product_price(self):
        try:
            self.price = self.soup.find('span', attrs={'data-selenium': 'uppedDecimalPriceFirst'}).text.strip() + "." + \
                self.soup.find('sup', attrs={'data-selenium': 'uppedDecimalPriceSecond'}).text.strip()

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_price()")
            self.price = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_price()")
            self.price = None
            self.product_address = None

    def retrieve_product_address(self):
        try:
            self.product_address = "https://bhphotovideo.com" + self.soup.find("a", attrs={'data-selenium': 'miniProductPageProductNameLink'})['href']

        except (AttributeError, IndexError, TypeError) as e:
            # AttributeError most likely means that it was not able to find the span
            # resulting in a NoneType error
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

if __name__ == "__main__":
    bandh = BandH("BX80684I99900K")
    bandh.test()
