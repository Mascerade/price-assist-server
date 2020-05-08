import requests
import random
import sqlite3
import datetime

NUM_RETAILERS = 13

min_price_value = int(input("What is the min price you would like? "))
max_price_value = int(input("What is the max price you would like? "))

num_values = input("How many values would you like? ")
num_values = int(num_values)

conn = sqlite3.connect("databases/fake_data.db")
cursor = conn.cursor()
item_models = requests.get('http://localhost:5003/item_model_data').json()

for item_model, _ in item_models.items():
    create_table = (''' CREATE TABLE IF NOT EXISTS "{}"(
        date DATE,
        amazon float,
        bestbuy float,
        newegg float,
        walmart float,
        bandh float,
        ebay float,
        tigerdirect float,
        microcenter float,
        jet float,
        outlet float,
        superbiiz float,
        target float,
        rakuten float);'''.format(item_model))

    cursor.execute(create_table)

    count = 0
    for x in range(num_values):
        random_prices = [datetime.date.today() + datetime.timedelta(days=count)] + random.sample(range(min_price_value, max_price_value), NUM_RETAILERS)
        insert_format = ''' INSERT INTO "''' + item_model + '''" (date, amazon, bestbuy, newegg, walmart, bandh, 
            ebay, tigerdirect, microcenter, jet, outlet, superbiiz, target, rakuten) VALUES(''' + "?, " * (NUM_RETAILERS) + '''?)'''
        cursor.execute(insert_format, tuple(random_prices))
        conn.commit()
        count += 1

conn.close()
