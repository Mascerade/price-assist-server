import sys, os
import time
sys.path.insert(0, os.getcwd())
from scrapers.walmart_scraper import Walmart

file_name = input("What would you like to call the refined user agent file? ")
directory = input("What directory do you want to put the file in? ")

try:
    os.mkdir(os.getcwd() + "/" + directory)

except: 
    pass

user_agent_number = 0
with open("user_agents/scrapers_master.txt", "r") as master, open(directory + "/" + file_name + ".txt", "a+") as refined_file:
    for user_agent in master:
        user_agent_number += 1
        print(user_agent_number, user_agent + " ___________________________________")
        count = 0
        while count < 5:
            walmart = Walmart("bx80684i99900kf", user_agent.strip())
            try:
                walmart.retrieve_product_address()
                walmart.retrieve_product_price()

            except Exception as e:
                pass

            if walmart.price != "None" or walmart.price is not None or walmart.price != "Could Not Find Price":
                if walmart.product_address is None or walmart.product_address == "None":
                    break
                
                else:
                    print("YES", walmart.price, walmart.product_address)
                    if count == 4:
                        refined_file.write(user_agent)

            else:
                break
            
            count += 1
            time.sleep(5)
