import requests

while True:
    user_input = input("Do you want to GET, PUT or DELETE? ")

    if user_input.lower() == "get":
        pass

    elif user_input.lower() == "put":
        data = requests.get("http://localhost:5000/api/query?retailer=Amazon&price=$471.99&item_model=bx80684i99900k&return_type=json").json()
        requests.put("http://localhost:5003/", json = {"item_model": "bx80684i99900k", "data": data})

    elif user_input.lower() == "delete":
        item_model = 'bx80684i99900k'
        requests.delete("http://localhost:5003/", json = {"item_model": item_model})

    elif user_input.lower() == "put item model":
        item_model = input("What item model do you want to put into the database? ")
        requests.put("http://localhost:5003/item_model_data", json={"item_model": item_model})

    elif user_input.lower() == "delete item model":
        item_model = input("What item model do you want to put into the database? ")
        requests.delete("http://localhost:5003/item_model_data", json={"item_model": item_model})
