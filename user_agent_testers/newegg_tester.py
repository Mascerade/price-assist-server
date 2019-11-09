import sys, os
sys.path.append(os.getcwd())
from scrapers.newegg_scraper import NeweggProduct
import time

product_address = "https://www.newegg.com/amd-ryzen-7-2700x/p/N82E16819113499?Description=Ryzen%207&cm_re=Ryzen_7-_-19-113-499-_-Product"
price = "$479.99"
with open("scrapers_master2.txt", "r") as s, open("user_agents/newegg_agents2.txt", "a") as a:
    for x in s:
        time.sleep(2)        
        z = 1
        while z < 2:
            newegg = NeweggProduct("BX80684I99900K", x.strip())
            try:
                newegg.retrieve_product_address()
                newegg.retrieve_product_price()

            except Exception as e:
                pass

            if newegg.price == price:
                if newegg.product_address is None or newegg.product_address == "None":
                    print("No", newegg.price, newegg.product_address)
                
                else:
                    print("YES", newegg.product_address)
                    a.write(x)

            else:
                print("NO", newegg.price, newegg.product_address)
                
            z += 1
