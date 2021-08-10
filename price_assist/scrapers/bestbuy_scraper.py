from typing import Optional
from selenium.webdriver.common.by import By
from common.process_scraper import ProcessScraper
from common.stm_scraper import STMScraper


class BestBuy(STMScraper):
    def __init__(self,
                 product_model: str,
                 using_tor: bool = False,
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        super().__init__(name="BestBuy",
                         search_address=f'https://www.bestbuy.com/site/searchpage.jsp?st={product_model}',
                         product_model=product_model,
                         using_tor=using_tor,
                         test_user_agent=test_user_agent,
                         test_tor_username=test_tor_username,
                         indicator_element=[By.ID, 'main-results'])

    def retrieve_product_address(self):
        try:
            sku_header = self.soup.find('h4', attrs={'class': 'sku-header'})
            self.product_address = "https://www.bestbuy.com" + sku_header.find('a')['href']

        except (AttributeError, IndexError, TypeError) as e:
            self.access_error(function_name="retrieve_product_address()")
            self.product_address = None 

        except Exception as e:
            self.unhandled_error(error=e, function_name="retrieve_product_address()")
            self.product_address = None

    def retrieve_product_price(self):
        if self.product_address is not None:
            try:
                self.price = self.soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'}).find("span").text

            except (AttributeError, IndexError, TypeError) as e:
                self.access_error(function_name="retrieve_product_price()")
                self.price = None

            except Exception as e:
                self.unhandled_error(error=e, function_name="retrieve_product_price()")

        else:
            self.price = None

if __name__ == "__main__":
    best = BestBuy("BX80684I99900K")
    best.test()
