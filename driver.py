import subprocess
# run command: python driver.py
# Run the scrapy spider command for manga crawler 
subprocess.run(["scrapy", "crawl", "manga", "-o", "manga.json"], check=True)

# Run the Python script
subprocess.run(["python", "sorting.py"], check=True)