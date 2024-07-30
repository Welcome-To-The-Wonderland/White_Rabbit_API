import subprocess
import json
import os

# THIS SCRIPT WAS REPLACED BY lambda_function.py TO TRANSFER TO AWS
# run command: python driver.py
start_urls = [
    "https://kissmanga.org/manga/manga-bc979159",
    "https://kissmanga.org/manga/manga-ny991307",
    "https://kissmanga.org/manga/manga-oh991742"
    #"https://kissmanga.org/manga/manga-ln951470",
]

#def driverFunc(start_urls):

start_urls_json = json.dumps(start_urls)

os.environ['START_URLS_JSON'] = start_urls_json

# Run the scrapy spider command for manga crawler 
subprocess.run(["scrapy", "crawl", "manga", "-o", "manga.json"], check=True)

# Run the sorting Python script
subprocess.run(["python", "sorting.py"], check=True)