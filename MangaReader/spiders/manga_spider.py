import scrapy
import re
import os
from urllib.parse import urlparse, urlunparse
import json
from collections import defaultdict
import subprocess

# scrapy crawl manga -o manga.json

class MangaLinkSpider(scrapy.Spider):
    name = "manga"
    
    # delete old json file data if it exists
    def __init__(self, *args, **kwargs):
        super(MangaLinkSpider, self).__init__(*args, **kwargs)
        if os.path.exists("manga.json"):
            os.remove("manga.json")
    
    start_urls = [
        "https://kissmanga.org/manga/manga-ny991307",
        #"https://kissmanga.org/manga/manga-ln951470"
        "https://kissmanga.org/manga/manga-bc979159",
        "https://kissmanga.org/manga/manga-oh991742",
    ]
    
    
    def parse(self, response):
        #general info to pass as meta
        title = response.css("h2 strong.bigChar::text").get()
        title = title.replace('’', "'") # Temp fix bug where special characters (like " ' ") are outputted as their unicode values
        author = response.css("p.info span::text").getall() # bug, white space bullshit. Maybe use .strip()
        genres = response.css("p.info span::text").getall() # bug, white space bullshit. Maybe use .strip()
        chapter_urls = []
        chapter_urls = response.css("h3 a::attr(href)").getall()
        
        #why is adding .jpg to a string such a pain in the a**
        parsed_url = urlparse(response.url)
        manga_id = parsed_url.path.split('/')[-1]
        new_path = "/mangaimage/" + manga_id + ".jpg"
        cover = urlunparse((parsed_url.scheme, parsed_url.netloc, new_path, '', '', ''))
        
        for url in chapter_urls:
            chapter_number = re.findall(r'\d+\.?\d*$', url)[0]
            uid = str(chapter_number).replace('.', '-')
            uid = f"{manga_id}-{uid}"
            yield scrapy.Request(response.urljoin(url), callback=self.parse_chapter, 
                                 meta={
                                        'title': title,
                                        'author': author,
                                        'genres': genres,
                                        'chapter' : chapter_number,
                                        'cover': cover,
                                        'manga-id': manga_id,
                                        'uid': uid,
                                       })
        
    def parse_chapter(self, response):
        image_urls = response.css("div#centerDivVideo img::attr(src)").getall()
        yield {
                "manga-id" : response.meta['manga-id'],
                "uid": response.meta['uid'],
                "Title": response.meta['title'],
                "Chapter": float(response.meta['chapter']),
                "Images": image_urls,
                #"Author": response.meta['author'], #bugged extraction
                #"Genres": response.meta['genres'], #bugged extraction
                "cover": response.meta['cover'],
        }