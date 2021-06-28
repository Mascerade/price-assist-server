import os
import sys
import json
import random
from typing import Dict, List, Optional


class CommonPaths():
    # Whether we are using the caching server or not
    CACHE: bool = True
    
    # Load the settings
    if os.path.exists("settings.json"):
        with open("settings.json") as json_file:
            SETTINGS: Dict[str, str] = json.load(json_file)

    # For when there is no auto-generated user agents to use from settings
    DEFAULT_USER_AGENTS_DIR: str = "user_agents/default_user_agents"

    # Dictionary for the scrapers Tor usernames
    SCRAPER_TOR_IPS: Dict[str, Optional[List[str]]] = {}

    # Dictionary for the scrapers Tor user agents
    SCRAPER_USER_AGENTS: Dict[str, List[str]] = {}

    SCRAPER_ERROR_WORDS = ["404", "automated", "access", "captcha"]

    # The IP address for the caching server
    CACHE_IP = "localhost"

    # The IP for Track Prices
    TRACK_PRICES_IP = 'localhost'


    # Essentially, get all the names of the scrapers
    all_scrapers = [f.split("_")[0] for f in os.listdir('scrapers/') if os.path.isfile(os.path.join('scrapers/', f)) and f != "__init__.py"]

    for scraper in all_scrapers:
        # Assigns a list of tor usernames to each scraper
        try:
            with open(os.path.join(SETTINGS['tor_ips_dir'], f'{scraper}_tor_ips.txt')) as f:
                SCRAPER_TOR_IPS[scraper] = f.read().splitlines()

        except FileNotFoundError:
            SCRAPER_TOR_IPS[scraper] = None
        
        # Assigns a user agent to each scraper
        try:
            with open(os.path.join(SETTINGS['tor_user_agents_dir'], f'{scraper}_tor.txt')) as f:
                SCRAPER_USER_AGENTS[scraper] = f.read().splitlines()
            
        except FileNotFoundError:
            with open(os.path.join(DEFAULT_USER_AGENTS_DIR, 'scrapers_master.txt')) as f:
                SCRAPER_USER_AGENTS[scraper] = f.read().splitlines()
