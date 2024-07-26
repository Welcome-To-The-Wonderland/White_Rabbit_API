import subprocess
import json
import os

def lambda_handler(event, context):
    # Extract start_urls from the event
    start_urls = event.get('start_urls', [])
    
    # Convert start_urls to JSON string
    start_urls_json = json.dumps(start_urls)
    
    # Set environment variable
    os.environ['START_URLS_JSON'] = start_urls_json
    
    # Run the scrapy spider command for manga crawler 
    subprocess.run(["scrapy", "crawl", "manga", "-o", "manga.json"], check=True)
    
    # Run the sorting Python script
    subprocess.run(["python", "sorting.py"], check=True)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }