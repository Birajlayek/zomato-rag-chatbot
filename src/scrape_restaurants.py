from src.scrapers.zomato_scraper import ZomatoScraper

restaurant_urls = [
    "https://www.zomato.com/kharagpur/the-curry-room-iit-kharagpur/info",
    "https://www.zomato.com/kharagpur/pizza-hut-inda/info",
]

for url in restaurant_urls:
    scraper = ZomatoScraper(url)
    data = scraper.scrape()
    if data:
        scraper.save()
        print(f"Scraped and saved: {data['name']}")
    else:
        print(f"Failed: {url}")
