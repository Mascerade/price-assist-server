import requests
from bs4 import BeautifulSoup

# This program was used to get all of the user-agents in scrapers.txt

data = requests.get("https://developers.whatismybrowser.com/useragents/explore/software_name/safari/")
data = data.text
soup = BeautifulSoup(data, "lxml")

with open("scrapers.txt", "a") as scraper_file:
    print("here")
    for x in soup.find_all("td", "useragent"):
        scraper_file.write(x.text + "\n")
