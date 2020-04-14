import random
import sqlite3

min_price_value = int(input("What is the min price you would like? "))
max_price_value = int(input("What is the max price you would like? "))

num_values = input("How many values would you like? ")
num_values = int(num_values)

table_name = input("What would you like the table name to be? ")

conn = sqlite3.connect("track_prices/fake_data.db")
cursor = conn.cursor()
cursor.execute(''' CREATE TABLE IF NOT EXISTS {} (xval INTEGER, price INTEGER)'''.format(table_name))

for x in range(num_values):
    random_number = random.randint(min_price_value, max_price_value)
    insert_text = " INSERT INTO " + table_name + " (xval, price) VALUES(?, ?)"
    cursor.execute(insert_text, (x,  random_number))
    conn.commit()

conn.close()
