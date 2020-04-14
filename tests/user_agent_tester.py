import sys, os
import time
sys.path.insert(0, os.getcwd())
from scrapers.amazon_scraper import Amazon
from scrapers.newegg_scraper import NeweggProduct
from scrapers.walmart_scraper import Walmart
from scrapers.jet_scraper import Jet
from scrapers.ebay_scraper import Ebay
from scrapers.microcenter_scraper import Microcenter
from scrapers.outletpc_scraper import OutletPC
from scrapers.superbiizz_scraper import SuperBiiz
from scrapers.tigerdirect_scraper import TigerDirect

scraper_classes = {
    "amazon": Amazon,
    "newegg": NeweggProduct,
    "walmart": Walmart,
    "jet": Jet,
    "ebay": Ebay,
    "microcenter": Microcenter,
    "outletpc": OutletPC,
    "superbiiz": SuperBiiz,
    "tigerdirect": TigerDirect
}

# Gets parameters from the terminal and sets the variables
scraper_name = sys.argv[1].lower()
file_name = sys.argv[2]
directory = sys.argv[3]
test_item_model = sys.argv[4]

# file_name = input("What would you like to call the refined user agent file? ")
# directory = input("What directory do you want to put the file in? ")

try:
    os.mkdir(os.getcwd() + "/" + directory)

except: 
    pass

user_agent_number = 0

# Scraper master is the file that has 700+ user agents in it
# Opens that along with a new file in *directory/file_name*
with open("user_agents/scrapers_master.txt", "r") as master, open(directory + "/" + file_name + ".txt", "a+") as refined_file:
    for user_agent in master:
        user_agent_number += 1 # Just to keep track of where we are in scraper master
        print(user_agent_number, user_agent + " ___________________________________")
        
        # Must get 5 results in a row for one user agent for it to be added to the file
        count = 0
        while count < 5:
            # Based on the scraper name given by the user, create the instance
            scraper = scraper_classes[scraper_name](test_item_model, user_agent.strip())

            try:
                scraper.retrieve_product_address()
                scraper.retrieve_product_price()

            except Exception as e:
                pass
            
            # If the price and product model aren't none, the continue testing the user agent
            # Otherwise, break from this user agent
            if scraper.price != "None" or scraper.price is not None:
                if scraper.product_address is None or scraper.product_address == "None":
                    break
                
                else:
                    # If it worked 5 times, add it to the new file
                    print("YES", scraper.price, scraper.product_address)
                    if count == 4:
                        refined_file.write(user_agent)

            else:
                break
            
            count += 1
            time.sleep(5)
