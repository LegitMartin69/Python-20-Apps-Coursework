import time
import requests
import selectorlib
from datetime import datetime


global URL
URL = "http://programmer100.pythonanywhere.com"

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    print("DEBUG: Source scraped, returning...")
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    # Extracts the value from the returned dictionary with the key "tours"
    value = extractor.extract(source)["home"]
    print(f"DEBUG: Value extracted: {value}, returning...")
    return value


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(datetime.now().strftime("%Y-%d-%m-%H-%M-%S") + "," + extracted + "\n")
    print("DEBUG: Data stored")


if __name__ == "__main__":
    with open("data.txt", "w") as file:
        file.write("date,temperature\n")
    print("DEBUG: header created, file wiped...")
    for i in range(1,20):
        scraped = scrape(URL)
        extracted = extract(scraped)
        store(extracted)
        time.sleep(2)
