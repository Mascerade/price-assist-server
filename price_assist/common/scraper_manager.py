from typing import List, Dict, Union, Optional
from threading import Thread
from common.base_scraper import Scraper

class ScraperManager():
    def __init__(self,
                 cr: Optional[str],
                 cr_price: Optional[str],
                 cr_product_address: Optional[str]):
        self.cr = cr
        self.cr_price = cr_price
        self.cr_product_address = cr_product_address
        self.scrapers: List[Scraper] = []

    def add(self, scraper: Scraper) -> None:
        self.scrapers.append(scraper)
    
    def run_scrapers(self) -> None:
        '''
        Run the scrapers in parallel
        '''
        
        thread_list: List[Thread] = []
        for scraper in self.scrapers:
            # If the scraper is the current retailer, don't run the functions
            if scraper.name.lower() == self.cr:
                scraper.price = self.cr_price
                scraper.product_address = self.cr_product_address
                continue

            thread_list.append(Thread(target=scraper.retrieve_all_information))
            
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    def run_single_scraper(self, scraper_name: str) -> Optional[Dict[str, Optional[str]]]:
        '''
        Run single scraper
        '''
        for scraper in self.scrapers:
            if scraper.name.lower() == scraper_name:
                scraper.retrieve_all_information()
                return {scraper.name.lower(): scraper.as_dict()}
        return None
    
    def as_dict(self) -> Dict[str, Union[Dict[str, Optional[str]], List[str]]]:
        '''
        Return the information in the scrapers.
        {
            retailer1: {name1, price1, product_address1}
            retailer2: {name2, price2, product_address2}
            .
            .
            .
            scraper_names: [name1, name2, name3 . . .]
        }
        '''

        ret: Dict[str, Union[Dict[str, Optional[str]], List[str]]] = {}
        scraper_names: List[str] = []
        for scraper in self.scrapers:
            ret[scraper.name.lower()] = scraper.as_dict()
            scraper_names.append(scraper.name.lower())
        ret['scraper_names'] = scraper_names
        return ret