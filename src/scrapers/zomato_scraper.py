import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

class ZomatoScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.data = {
            "name": "",
            "location": {"address": "", "city": ""},
            "menu": [],
            "features": {},
            "hours": "",
            "contact": {"phone": "", "website": url}
        }

    def scrape(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example parsing logic; adjust selectors as needed
            self.data['name'] = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Unknown"
            address = soup.find('p', class_='sc-dmyCSP')
            self.data['location']['address'] = address.get_text(strip=True) if address else "Not found"
            self.data['features']['vegetarian'] = "vegetarian" in soup.text.lower()
            self.data['features']['gluten_free'] = "gluten" in soup.text.lower()
            self.data['hours'] = "Not available"
            self.data['contact']['phone'] = "Not available"
            # Menu parsing example (update for real site)
            menu_section = soup.find_all('div', class_='menu-item')
            for item in menu_section:
                name = item.find('span', class_='item-name').get_text(strip=True) if item.find('span', class_='item-name') else "Unnamed"
                price = item.find('span', class_='item-price').get_text(strip=True) if item.find('span', class_='item-price') else "N/A"
                desc = item.find('span', class_='item-desc').get_text(strip=True) if item.find('span', class_='item-desc') else ""
                self.data['menu'].append({"name": name, "price": price, "description": desc})
            return self.data
        except Exception as e:
            print(f"Scraping failed for {self.url}: {e}")
            return None

    def save(self):
        Path('data/raw').mkdir(parents=True, exist_ok=True)
        fname = self.data['name'].replace(' ', '_').replace('/', '_') or 'restaurant'
        with open(f'data/raw/{fname}.json', 'w') as f:
            json.dump(self.data, f, indent=2)
