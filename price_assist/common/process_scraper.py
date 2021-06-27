import time
from typing import Optional, Tuple, Dict
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from .base_scraper import Scraper

class ProcessScraper(Scraper):
    '''
    The ProcessScraper is the more complex scraper. This is used when websites either
    issue a block when JavaScript is not rendered or need JavaScript to be rendered
    in order to get the necessary information.
    For this, Selenium is used.
    '''
    def __init__(self,
                 name: str,
                 product_model: str,
                 search_address: str,
                 using_tor: bool,
                 test_user_agent: Optional[Dict[str, str]] = None,
                 test_tor_username: Optional[int] = None,
                 webdriver_type: str = 'firefox'):
        super().__init__(
            name = name,
            product_model=product_model,
            search_address=search_address,
            using_tor=using_tor,
            test_user_agent=test_user_agent,
            test_tor_username=test_tor_username
        )

        self.webdriver_type = webdriver_type
        assert self.webdriver_type == 'chrome' or self.webdriver_type == 'firefox', \
               f"Invalid webdriver type passed {self.webdriver_type}. Expect either 'chrome' or 'firefox'."

    def chrome_driver(self) -> Tuple[webdriver.Chrome, Display]:
        '''
        Returns the Python Display that the Chrome driver uses as well
        as the Chrome driver itself. Use the driver to get the page_source
        for BeautifulSoup.
        '''
        
        display: Display = Display(visible=0, size=(800, 600))
        display.start()
        caps: Dict[str, str] = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        options = Options()
        options.add_argument('--no-sandbox')
        # options.add_argument('--window-size=1420,1080')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options,
                                  desired_capabilities=caps,
                                  executable_path=f"executables/chromedriver")
        
        return driver, display

    def firefox_driver(self) -> webdriver.Firefox:
        '''
        Return a Firefox webdriver to get the page_source. Use the driver
        to get the page_source for BeautifulSoup. 
        '''

        binary = FirefoxBinary("/usr/lib/firefox/firefox")
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "normal"
        options = webdriver.firefox.options.Options()
        options.add_argument("--headless")

        # Add the proxy options if Tor is being used
        if self.using_tor:
            proxy = f"socks5h://{self.tor_username}:idk@localhost:9050"
            options.add_argument(f"--proxy-server={proxy}")
            options.add_argument(f"--id={self.tor_username}")
        driver = webdriver.Firefox(options=options,
                                   firefox_binary=binary,
                                   desired_capabilities=caps,
                                   executable_path=f"executables/geckodriver")
        
        return driver

    def retrieve_soup(self):
        '''
        For a network scraper, go to the search address using Requests and create the soup
        '''
        
        try:
            if self.webdriver_type == 'chrome':
                driver, display = self.chrome_driver()
            
            elif self.webdriver_type == 'firefox':
                driver = self.firefox_driver()
            
            driver.get(self.search_address)
            if (self.name == "Rakuten" or self.name == "Target"):
                time.sleep(3)
            
            self.data = driver.page_source
            self.soup: BeautifulSoup = BeautifulSoup(self.data, Scraper.PARSER)

        except Exception as e:
            print(str(e))
            self.price = None
            self.product_address = None

        finally:
            driver.close()
            
            if self.webdriver_type == 'chrome':
                display.stop()
