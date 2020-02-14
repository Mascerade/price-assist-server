import requests

while True:
    user_input = input("Do you want to GET, PUT or DELETE? ")

    if user_input.lower() == "get":
        pass

    elif user_input.lower() == "put":
        data = requests.get("http://localhost:5000/api/query?retailer=None&price=None&item_model=yd1600bbafbox&return_type=json").json()
        requests.put("http://localhost:5003/", json = {"item_model": "yd1600bbafbox", "data": data})
        requests.put("http://localhost:5003/item_model_data", json={"item_model": data["item_model"], "title": data["title"]})

    elif user_input.lower() == "delete":
        item_model = 'bx80684i99900k'
        requests.delete("http://localhost:5003/", json = {"item_model": item_model})

    elif user_input.lower() == "put item model":
        item_model = input("What item model do you want to put into the database? ")
        requests.put("http://localhost:5003/item_model_data", json={"item_model": item_model, "title": "test"})

    elif user_input.lower() == "delete item model":
        item_model = input("What item model do you want to put into the database? ")
        requests.delete("http://localhost:5003/item_model_data", json={"item_model": item_model})
