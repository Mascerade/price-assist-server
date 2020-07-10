from flask import Flask, request
import json
import flask
from flask_cors import cross_origin
import time
import requests
import sys
import os
import signal
import sqlite3
import datetime
import plyvel
from helpers.title_similarity import get_similar_titles
from helpers.help_functions import format_item_model

""" 
This is the auto-price tracker
Essentially, have SQL database where each table name is the product's
model and each is a different date with the price on that date

FOR THE DATABASE
* For now, we will use a locally stored database (sqlite3)

FOR AUTO UPDATING
* Going to have to set up some kind of thread pool because
  we can only have so many products updating at the same time

* It will send a request to this server to get information from the
  scrapers using a specific product address (probably going to have
  to fix the problem where I will have to use totally new members
  to do this)
    - This can be a seperate route (/update or something with a
    dictionary of all the product addresses along with the retailer name)

* Run this from the track_prices directory
"""

# Create the databases directory first
if not os.path.exists('databases'):
    os.makedirs('databases')

# What is used to create the dict of each entry
DB_ORDER = ["date", "amazon", "bestbuy", "newegg", "walmart", "banh", "ebay", "tigerdirect", "microcenter", "jet", "outletpc", "superbiiz", "target", "rakuten"]

# ITEM_MODEL_DB stores the item model for a product as the key and the title as a value
# This database is used for when the user of Track Prices needs to search a product
ITEM_MODEL_DB = 'databases/item_model_db/'

# IMAGE_DB stores the item model for a product as the key and a link to an image
# for the product as the value
IMAGE_DB = 'databases/image_db/'

# SQL database of all the prices of products tracks with the item model as the key
PRICES_DB = 'databases/prices.db'

# FAKE_DATA is only used for testing the graphing part of Track Prices
FAKE_DATA = 'databases/fake_data.db'

ply_db = plyvel.DB(ITEM_MODEL_DB, create_if_missing = False)
image_db = plyvel.DB(IMAGE_DB, create_if_missing = False)

app = Flask(__name__)

@app.route("/fake_data", methods=["GET"])
@cross_origin()
def get_fake_data():
    """ Used to test the graph of the GUI """

    # Opens a connection to the fake data database
    conn = sqlite3.connect(FAKE_DATA)
    cursor = conn.cursor()

    # Get all the data from the table "fake_data1"
    get_info = "SELECT * from fake_data1"
    cursor.execute(get_info)

    # Data to be returned
    return_data = []

    # Zips the entries with "date" and "amazon" because that is what the GUI uses
    for entry in cursor.fetchall():
        return_data.append(dict(zip(['date', 'amazon'], entry)))

    # Essentially the title of the eventual graph
    return_data.append("Fake Data")

    # Return the data with error code 200
    return json.dumps(return_data), 200

@app.route("/", methods=["GET"])
@cross_origin()
def get_data():
    """ Retrieve all the data from the SQL Database """
    item_model = request.args.get("item_model").lower()

    # This is because the item_model is stored differently in the sql database
    try:
        print(item_model)
        title = ply_db.get(bytes(item_model, encoding='utf-8')).decode('utf-8')
        image = image_db.get(bytes(item_model, encoding='utf-8')).decode('utf-8')

    except AttributeError as e:
        return json.dumps({'success': False, 'msg': str(e)}), 404

    with sqlite3.connect(FAKE_DATA) as conn:
        # Have to change the item model to the version that is formatted for the SQL database
        get_info = '''SELECT * from "{}"'''.format(format_item_model(item_model))
        # The cursor is what actaully gets data from the database
        cur = conn.cursor()

        try: 
            # Execute the selection of data
            cur.execute(get_info)
        
        except sqlite3.OperationalError as e:
            print(str(e))
            return json.dumps({'success': False, 'msg': str(e)}), 404

        # Get the data
        sql_data = cur.fetchall()

        # List of dictionaries to return
        price_data = []

        # Zip the retailer_order with each entry to get a dict of each retailer's prices
        for entry in sql_data:
            price_data.append(dict(zip(DB_ORDER, entry)))
        return_data = {}
        return_data['prices'] = price_data
        return_data['item_model'] = item_model
        return_data['title'] = title
        return_data['image'] = image

        # return the data with a 200 success error code
        return json.dumps(return_data), 200

@app.route("/", methods=["PUT"])
def put_price_data():
    if request.method == "PUT":
        data = request.json
        item_model = data['item_model'].lower()
        item_model = format_item_model(item_model)

        conn = sqlite3.connect(PRICES_DB)
        
        # Use the cursor to execute tasks
        cursor = conn.cursor()

        # Create the table with all the retailers 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS "{}" (
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
        rakuten float); '''.format(item_model))

        # List used to insert the date and prices into the database
        insert_values = [datetime.date.today()]

        # Get only the actual information about each retailer from the data dict
        # Note: We're treating 0's as invalid information
        for retailer in DB_ORDER[1:]:
            try:
                value = data["data"][retailer + "_data"]
                
                # The item model is part of the data, so don't include that
                if type(value) == str or type(value) == bool:
                    continue
                
                # If there was just blank price information, don't include it
                elif value[1] is None or value[1] == '':
                    insert_values.append("0")
                    continue

                # Convert the price to a float to make sure it's actual price information
                # Convert it back to a string to add to the database
                insert_values.append(str(float(value[1][1:])))
            
            except:
                insert_values.append("0")

        # Need a tuple because that's how the prices get inserted into the "?"
        insert_values = tuple(insert_values)
        insert_format = ''' INSERT INTO "''' + item_model + '''" (date, amazon, bestbuy, newegg, walmart, bandh, 
        ebay, tigerdirect, microcenter, jet, outlet, superbiiz, target, rakuten) VALUES(''' + "?, " * (len(DB_ORDER) - 1) + '''?)'''

        # Just to check that everything is working
        print(insert_format)

        # Add the data to the databse
        cursor.execute(insert_format, insert_values)
        conn.commit()

        # Close the connections
        cursor.close()
        conn.close()

        # # Open a connection the the plyvel database
        # ply_db = plyvel.DB(ITEM_MODEL_DB, create_if_missing = True)

        # # Put the item_model into the database/do nothing if its already there
        # ply_db.put(bytes(item_model, encoding='utf-8'), bytes(True))
        
        # # Close the plyvel database
        # ply_db.close()

        return json.dumps({"success": True}), 201

@app.route("/item_model_data", methods=["GET"])
@cross_origin
def item_model_data():
    """
    Prints the item models with the title to the terminal
    {"item_model": "title", "item_model2": "title2" ...}
    """

    return_data = {}
    for key, value in ply_db:
        return_data[key.decode("utf-8")] = value.decode('utf-8')

    return json.dumps(return_data), 200

@app.route("/search_item_models", methods=["GET"])
@cross_origin()
def search_item_models():
    search_title = request.args.get("search")
    item_model_data = requests.get("http://localhost:5003/item_model_data").json()
    title_data = get_similar_titles(search_title, item_model_data)
    title_data["item_model_data"] = item_model_data
    return json.dumps(title_data), 200

@app.route("/item_model_data", methods=["PUT"])
def put_item_model():
    """
    This function will simply put an item model into the plyvel database
    """
    item_model = request.json['item_model'].lower().strip()
    title = request.json['title'].strip()

    # Put the item model into the db
    ply_db.put(bytes(item_model, encoding='utf-8'), bytes(title, encoding='utf-8'))


    return json.dumps({"success": True}), 201

@app.route("/image_data", methods=["PUT"])
def put_image_data():
    """
    This function has an item model as a key and a link 
    to the image as the value
    Example: {'item_model1': 'link1', 'item_model2': 'link2'...}
    """

    item_model = request.json['item_model'].lower().strip()
    image_link = request.json['image'].strip()

    # Put the image into the database
    image_db.put(bytes(item_model, encoding='utf-8'), bytes(image_link, encoding='utf-8'))

    return json.dumps({"success": True}), 201

@app.route("/item_model_data", methods=["DELETE"])
def delete_item_model():
    """
    In reality, this function should never be used, but its useful
    for testing
    """
    item_model = request.json['item_model'].lower().strip()

    # Delete the item model from the database
    ply_db.delete(bytes(item_model, encoding='utf-8'))


    return json.dumps({"success": True}), 200

@app.route("/", methods=["DELETE"])
def delete_data():
    item_model = request.json['item_model'].lower().strip()

    # We check if "check" is equal to None (meaning the item model is not in the database)
    check = ply_db.get(bytes(item_model, encoding='utf-8'))
    
    print(item_model, check)

    
    try:
        # Establish the connection to the prices database
        conn = sqlite3.connect(FAKE_DATA)
        cursor = conn.cursor()
        # As long as there is something in "check" the item_model exists
        if check is not None:
            # Delete the item_model in the plyvel database as well
            ply_db.delete(bytes(item_model, encoding='utf-8'))

            # DROP TABLE essentially will delete the table
            delete_str = 'DROP TABLE "' + format_item_model(item_model) + '"'

            # Execute the deletion of the table and close the connection
            cursor.execute(delete_str)
            conn.commit()
            conn.close()

            return json.dumps({'success': True}), 200
            
    except sqlite3.OperationalError:
        conn.close()
        return json.dumps({'success': False, "msg":"Item model not in the sql database"}), 400
    
    finally:
        conn.close()
    
    return json.dumps({'success': True, "msg": "Item model not found (plyvel db)"}), 200

@app.route('/shutdown', methods=['GET'])
def stopServer():
    ply_db.close()
    image_db.close()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Server not running with Werkzeug Server')
    func()
    return json.dumps({'success': True, 'msg': 'Server is shutting down'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, threaded=True)
