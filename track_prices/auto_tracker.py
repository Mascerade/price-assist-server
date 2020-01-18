from apscheduler.schedulers.blocking import BlockingScheduler
import requests

def price_updater():
    data = requests.get("http://localhost:5003/item_model_data").json()
    for item_model in data["item_models"]:
        data = requests.get("http://localhost/api/query?retailer=None&price=None&item_model=" + item_model + "&return_type=json").json()
    for item_model, _ in data.items():
        data = requests.get("http://localhost:5000/api/query?retailer=None&price=None&item_model=" + item_model + "&return_type=json").json()
        requests.put("http://localhost:5003/", json = {"item_model": item_model, "data": data})


sched = BlockingScheduler()
sched.add_job(price_updater, trigger='cron', hour='15', minute='00')
sched.start()
