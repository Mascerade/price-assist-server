from scrapers.amazon_scraper import Amazon

product_address = "https://www.amazon.com/AMD-Ryzen-Processor-Wraith-Cooler/dp/B07B428M7F/ref=sr_1_1?keywords=YD270XBGAFBOX&qid=1573223191&s=electronics&sr=1-1"
price = "$189.59"
with open("user_agents/amazon_agents_refined2.txt", "r") as s, open("amazon_agents_refined2.txt", "a") as a:
    for x in s:
        z = 1
        while z < 11:
            amazon = Amazon("YD270XBGAFBOX", x.strip())
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