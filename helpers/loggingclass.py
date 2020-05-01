import os
import sys
import logging
sys.path.append(os.getcwd())
from master_scraper.master_scraper import Scraper

class WriteLog():
    def __init__(self, name, log_path):
        self.name = name
        self.log_path = log_path
        logging.basicConfig(filename=log_path, level=logging.DEBUG)

    
    def access_error(self, function_name, tor_user_agent, tor_username, soup):
        for word in Scraper.SCRAPER_ERROR_WORDS:
            if (word in soup.lower()):
                logging.error('Could not access ' + self.name + '. User Agent: ' + tor_user_agent + ' Tor Username: ' + tor_username + ". From " + function_name)
                break

    def unhandled_error(self, error, function_name):
        logging.error('Unhandled type of error: ' + error + '. ' + function_name)
