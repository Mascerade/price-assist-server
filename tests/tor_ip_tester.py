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

try:
    os.mkdir(os.getcwd() + "/" + directory)

except: 
    pass

with open(directory + "/" + file_name + ".txt", "a+") as refined_file:
    for user in range(1, 1000):
        count = 0
        print("____________________________________________________________________")
        while count < 5:
            scraper = scraper_classes[scraper_name](test_item_model, tor_username=user)

            try:
                scraper.retrieve_product_price()
                scraper.retrieve_product_address()

            except Exception:
                break

            # If the price and product model aren't none, the continue testing the user agent
            # Otherwise, break from this user agent
            if scraper.price is not None:
                if scraper.product_address is None:
                    break
                
                else:
                    # If it worked 5 times, add it to the new file
                    print("YES", scraper.price, scraper.product_address)
                    if count == 4:
                        refined_file.write(str(user))

            else:
                break
            
            count += 1
            time.sleep(5)
