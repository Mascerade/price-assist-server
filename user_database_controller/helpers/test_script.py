import requests

while True:
    user_input = input("Do you want to GET, PUT or DELETE? ")

    if user_input.lower() == "get":
        pass

    elif user_input.lower() == "post":
        uid_token = input('What do you want the uid token to be? ')
        requests.post("http://localhost:5002/", json = {"uid_token": uid_token})

    elif user_input.lower() == "put":
        uid_token = input("What user do you want to use? ")
        item_model = input("What item model do you want to put? ")
        requests.put("http://localhost:5002/", json={"uid_token": uid_token, "item_model": item_model})
