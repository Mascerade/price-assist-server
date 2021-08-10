from typing import Optional
from selenium.webdriver import chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from stm.manager import ChromeTabManager
from common.stm_scraper import STMScraper
from common.scraper_manager import ScraperManager

class ScraperTabManager(ScraperManager, ChromeTabManager):
    def __init__(self,
                 cr: Optional[str],
                 cr_price: Optional[str],
                 cr_product_address: Optional[str],
                 *args,
                 **kwargs):
        
        # Don't need to wait for whole page to load
        caps = DesiredCapabilities().CHROME
        caps['pageLoadStrategy'] = 'none'

        # Add Chrome options to change the user agent and get rid of the "Chrome is being automated" message.
        opts = chrome.options.Options()
        opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
        opts.add_experimental_option('excludeSwitches', ['enable-automation'])

        ScraperManager.__init__(self,
                                cr,
                                cr_price,
                                cr_product_address)
        ChromeTabManager.__init__(self,
                                  [],
                                  desired_capabilities=caps,
                                  options=opts,
                                  *args,
                                  **kwargs)

    def add(self, scraper: STMScraper) -> None: # type: ignore[override]
        '''
        Both add the scraper to the ScraperManager and to the TabManager
        '''
        self.scrapers.append(scraper)
        self.add_new_tab(scraper)
    
    def run_scrapers(self) -> None:
        '''
        Run the scrapers through the ChromeTabManager
        '''
        self.open_tabs()
        self.execute_all_on_indicated()
