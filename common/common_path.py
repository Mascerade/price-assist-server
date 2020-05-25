import os
import sys
import json
import random
sys.path.append(os.getcwd())

class CommonPaths():
    print('here')
    RETAILER_LIST = ["Amazon", "B&H", "BestBuy", "Ebay", "Jet", "Microcenter", "Newegg", "OutletPC", "Rakuten", "Superbiiz", "Target"]

    # This is going to be a dictionary of all the settings loaded from settings.json
    SETTINGS = {}

    # For when there is no auto-generated user agents to use from settings
    DEFAULT_USER_AGENTS_DIR = "user_agents/default_user_agents"

    # Dictionary for the scrapers Tor usernames
    SCRAPER_TOR_IPS = {}

    # Dictionary for the scrapers Tor user agents
    SCRAPER_USER_AGENTS = {}

    SCRAPER_ERROR_WORDS = ["404", "automated", "access", "captcha"]

    # Whether we are using the caching server or not
    CACHE = True

    if os.path.exists("settings.json"):
        # Location (from settings.json)
        with open("settings.json") as json_file:
            settings = json.load(json_file)
            SETTINGS = settings

    # Essentially, get all the names of the scrapers
    all_scrapers = [f.split("_")[0] for f in os.listdir(os.path.join(os.getcwd(), 'scrapers/')) if os.path.isfile(os.path.join(os.getcwd(), 'scrapers/', f)) and f != "__init__.py"]
    for index, scraper in enumerate(all_scrapers):
        if scraper == "bandh":
            all_scrapers[index] = "b&h"

    for scraper in all_scrapers:
        # Assigns a list of tor usernames to each scraper
        try:
            with open(os.path.join(os.getcwd(), SETTINGS['tor_ips_dir'], scraper + '_tor_ips.txt')) as f:
                SCRAPER_TOR_IPS[scraper] = f.read().splitlines()

        except FileNotFoundError:
            SCRAPER_TOR_IPS[scraper] = None
        
        # Assigns a user agent to each scraper
        try:
            with open(os.path.join(os.getcwd(), SETTINGS['tor_user_agents_dir'], scraper + '_tor.txt')) as f:
                SCRAPER_USER_AGENTS[scraper] = f.read().splitlines()
            
        except FileNotFoundError:
            with open(os.path.join(os.getcwd(), DEFAULT_USER_AGENTS_DIR, 'scrapers_master.txt')) as f:
                SCRAPER_USER_AGENTS[scraper] = f.read().splitlines()
