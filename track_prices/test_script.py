import requests

while True:
    user_input = input("Do you want to GET, PUT or DELETE? ")

    if user_input.lower() == "get":
        pass

    elif user_input.lower() == "put":
        data = requests.get("http://localhost:5000/api/query?retailer=Amazon&price=$471.99&item_model=YD270XBGAFBOX&return_type=json").json()
        requests.put("http://localhost:5003/", json = {"item_model": "YD270XBGAFBOX", "data": data})

    elif user_input.lower() == "delete":
        pass