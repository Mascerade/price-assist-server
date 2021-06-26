import requests
from bs4 import BeautifulSoup

# This program was used to get all of the user-agents in scrapers.txt
y = int(1)
while y < 11:
    print(y)
    data = requests.get("https://developers.whatismybrowser.com/useragents/explore/software_name/android/" + str(y))
    data = data.text
    soup = BeautifulSoup(data, "lxml")

    with open("../user_agents/scrapers_master2.txt", "a") as scraper_file:
        for x in soup.find_all("td", "useragent"):
            scraper_file.write(x.text + "\n")

    y += 1