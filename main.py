from fastapi import FastAPI
from fb_scraper import FBPageScraper

app=FastAPI()

@app.get("/{page_id}")
async def read_post(page_id):
    scraper=FBPageScraper(page_id) 
    result=scraper.parse()
    #scraper.save_db(result)
    return result
