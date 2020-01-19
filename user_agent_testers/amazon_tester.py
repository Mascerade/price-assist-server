import sys, os
import time
sys.path.insert(0, os.getcwd())
from scrapers.amazon_scraper import Amazon

product_address = "https://www.amazon.com/Intel-BX80684I99900KF-i9-9900KF-Processor-Unlocked/dp/B07MGBZWDZ/ref=sr_1_1?keywords=bx80684i99900kf&qid=1578097145&sr=8-1"
price = "$478.89"

file_name = input("What would you like to call the refined user agent file? ")
directory = input("What directory do you want to put the file in? ")

try:
    os.mkdir(os.getcwd() + "/" + directory)

except: 
    pass

with open("user_agents/scrapers_master.txt", "r") as master, open(directory + "/" + file_name + ".txt", "a+") as refined_file:
    for user_agent in master:
        print(user_agent + " ___________________________________")
        count = 0
        while count < 5:
            amazon = Amazon("bx80684i99900kf", user_agent.strip())
            try:
                amazon.retrieve_product_address()
                amazon.retrieve_product_price()

            except Exception as e:
                pass

            if amazon.price != "None" or amazon.price is not None:
                if amazon.product_address is None or amazon.product_address == "None":
                    break
                
                else:
                    print("YES", amazon.price, amazon.product_address)
                    if count == 4:
                        refined_file.write(user_agent)

            else:
                break
            
            count += 1
            time.sleep(5)
