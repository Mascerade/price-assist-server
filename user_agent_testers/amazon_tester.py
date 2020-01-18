import sys, os
sys.path.insert(0, os.getcwd())
from scrapers.amazon_scraper import Amazon

product_address = "https://www.amazon.com/Intel-BX80684I99900KF-i9-9900KF-Processor-Unlocked/dp/B07MGBZWDZ/ref=sr_1_1?keywords=bx80684i99900kf&qid=1578097145&sr=8-1"
price = "$478.89"

user_input = input("What would you like to call the refined user agent file? ")

with open("user_agents/scrapers_master.txt", "r") as s, open("user_agents/" + user_input + ".txt", "a") as a:
    for x in s:
        z = 1
        while z < 11:
            amazon = Amazon("bx80684i99900kf", x.strip())
            try:
                amazon.retrieve_product_address()
                amazon.retrieve_product_price()

            except Exception as e:
                pass

            if amazon.price == price:
                if amazon.product_address is None:
                    print("No", amazon.price, amazon.product_address)
                
                else:
                    print("YES", amazon.product_address)
                    #a.write(x)

            else:
                print("NO", amazon.price, amazon.product_address)
                
            z += 1
