from apscheduler.schedulers.blocking import BlockingScheduler
import requests

def price_updater():
    data = requests.get("http://localhost:5003/item_model_data").json()

    for item_model, _ in data.items():
        data = requests.get("http://localhost:5000/price-assist/api/network-scrapers?retailer=None&price=None&item_model=" + item_model + "&title=None&return_type=json").json()
        add_scrapers = requests.get("http://localhost:5000/price-assist/api/process-scrapers?retailer=None&price=None&item_model=" + item_model + "&title=None&return_type=json").json()
        
        # Identifier is already in the original scraper data so delete this
        del add_scrapers["identifier"]
        
        # Update the original scrapers with the new scrapers
        data.update(add_scrapers)

        # Send the data to the track prices db
        requests.put("http://localhost:5003/", json = {"item_model": item_model, "data": data})

# Sets up the cron scheduler for automatically updating the database
sched = BlockingScheduler()
sched.add_job(price_updater, trigger='cron', hour='15', minute='30')
sched.start()
