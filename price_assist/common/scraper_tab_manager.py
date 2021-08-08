from typing import List, Dict, Union, Optional
from threading import Thread
from stm.manager import ChromeTabManager
from common.base_scraper import Scraper
from common.stm_scraper import STMScraper
from common.scraper_manager import ScraperManager

class ScraperTabManager(ScraperManager, ChromeTabManager):
    def __init__(self,
                 cr: Optional[str],
                 cr_price: Optional[str],
                 cr_product_address: Optional[str],
                 *args,
                 **kwargs):
        ScraperManager.__init__(self,
                                cr,
                                cr_price,
                                cr_product_address)
        ChromeTabManager.__init__(self, [], *args, **kwargs)

    def add(self, scraper: STMScraper) -> None:
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
