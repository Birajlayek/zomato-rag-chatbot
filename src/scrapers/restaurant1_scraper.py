from .base_scraper import BaseScraper

class Restaurant1Scraper(BaseScraper):
    def _parse(self, soup):
        # Name
        self.data['name'] = soup.find('h1', class_='restaurant-name').text.strip()
        
        # Location
        location_div = soup.find('div', class_='address')
        self.data['location'] = {
            'address': location_div.find('span', class_='street').text.strip(),
            'city': location_div.find('span', class_='city').text.strip()
        }
        
        # Menu
        menu_section = soup.find('section', id='menu')
        for item in menu_section.find_all('div', class_='menu-item'):
            self.data['menu'].append({
                'name': item.find('h3').text.strip(),
                'price': item.find('span', class_='price').text.strip(),
                'description': item.find('p', class_='description').text.strip(),
                'tags': [tag.text.strip() for tag in item.find_all('span', class_='dietary-tag')]
            })
        
        # Features
        self.data['features'] = {
            'vegetarian': 'Vegetarian' in soup.find('div', class_='features').text,
            'gluten_free': 'Gluten Free' in soup.find('div', class_='features').text
        }
