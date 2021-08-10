from typing import Any, Optional, Sequence, Union
from bs4 import BeautifulSoup
from stm.tab import Tab
from .base_scraper import Scraper

class STMScraper(Scraper, Tab):
    '''
    The STMScraper uses the stm module to create a tab in Chrome to get information.
    '''
    def __init__(self,
                 name: str,
                 product_model: str,
                 search_address: str,
                 using_tor: bool,
                 indicator_element: Sequence[Union[Any, str]],
                 test_user_agent: Optional[str] = None,
                 test_tor_username: Optional[int] = None):
        Scraper.__init__(
            self,
            name = name,
            product_model=product_model,
            search_address=search_address,
            using_tor=using_tor,
            test_user_agent=test_user_agent,
            test_tor_username=test_tor_username)
        Tab.__init__(
            self,
            name=name,
            url=search_address,
            indicator_element=indicator_element)

    def test(self):
        from common.scraper_tab_manager import ScraperTabManager
        manager = ScraperTabManager(cr=None, cr_price=None, cr_product_address=None, executable_path='./executables/chromedriver')
        manager.add(self)
        manager.open_tabs()
        manager.execute_all_on_indicated()
        manager.quit()
        super().test()

    def retrieve_soup(self):
        '''
        For the STM Scraper, getting the soup should be handled by the manager.
        '''
        pass

    def on_indicator_elem_found(self) -> None:
        '''
        Override the default behavior defined in Tab class
        '''
        if self.manager is not None:
            self.data = self.manager.page_source
            self.soup = BeautifulSoup(self.data, Scraper.PARSER)
        
        else:
            return None
    