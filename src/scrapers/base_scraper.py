import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import time
import logging
import json

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.data = {
            "name": "",
            "location": "",
            "menu": [],
            "features": {},
            "hours": {},
            "contact": {}
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def _check_robots_txt(self):
        try:
            rp = RobotFileParser()
            rp.set_url(f"{self.base_url}/robots.txt")
            rp.read()
            return rp.can_fetch("*", self.base_url)
        except Exception as e:
            logging.warning(f"Robots.txt check failed: {str(e)}")
            return True

    def _get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            return None

    def scrape(self):
        if not self._check_robots_txt():
            logging.error(f"Scraping blocked by robots.txt for {self.base_url}")
            return None
            
        soup = self._get_page(self.base_url)
        if not soup:
            return None
            
        self._parse(soup)
        return self.data

    def _parse(self, soup):
        raise NotImplementedError("Subclasses must implement this method")
