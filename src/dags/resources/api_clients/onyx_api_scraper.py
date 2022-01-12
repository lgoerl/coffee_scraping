import gzip
import json
import logging
import requests
from bs4 import BeautifulSoup
from dagster import resource
from dagster.utils import file_relative_path
from typing import Any, Dict, Optional

from resources.scrapers.base_api_scraper import BaseScraper

roaster_name = "Onyx"
base_url = "https://onyxcoffeelab.com"
products_url = f"{base_url}/collections/coffee"
request_header = {"User-Agent": "Mozilla/5.0"}

feature_map = {
    "cup": "tasting_notes"
}

class OnyxScraper(BaseScraper):
    def __init__(self):
        super().__init__(roaster_name)
        
    def get_active_roasts(self):
        response = requests.get(products_url, headers=request_header)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("a", class_="product-preview", href=True)
        if not products:
            raise ValueError(
                f"No products found. "+
                f"Check {products_url} to verify products are linked in <a> tags with class='product-preview'"
            )
        return [p["href"] for p in products]
    
    def get_roast(self, roast_href):
        roast_url = f"{base_url}/{roast_href}"
        logging.info(f"Scraping roast attributes at {roast_url}.")
        response = requests.get(roast_url, headers=request_header)
        soup = BeautifulSoup(response.text, "html.parser")
        stats = soup.find("div", class_=lambda t: t and "coffee-stats" in t)
        try:
            title = soup.title.text.replace("Onyx Coffee Lab", "").replace("\n", "")
            description = soup.find("div", class_="main-blurb").find("p").text
        except Exception as e:
            raise ValueError(
                f"Title or description missing. "+
                f"Check {roast_url} to verify description in div class 'main-blurb'"
            )
        features = {
            "href": roast_href,
            "roaster": roaster_name,
            "name": title,
            "description": description,
        }
        for feat in stats.find_all(class_="a-feature"):
            feature_label = feat.find(class_="label").text.replace(":", "").lower()
            feature_value = feat.find(class_="value").text
            features[feature_map.get(feature_label, feature_label)] = feature_value
        if set(features.keys()) == {"href", "title"}:
            raise ValueError(
                f"No attributes found. "+
                f"Check {roast_url} to verify roast notes are under '+coffee-stats' div tag as feature/value tags of 'a-feature' class"
            )
        return features



class OnyxMockScraper(BaseScraper):
    def __init__(self):
        super().__init__(roaster_name)
        file_path = file_relative_path(__file__, "../snapshot.gzip")
        with gzip.open(file_path, "r") as f:
            self._items: Dict[str, HNItemRecord] = json.loads(f.read().decode())
        
    def get_active_roasts(self):
        return self._items.keys()
    
    def get_roast(self, roast_href):
        return self._items[roast_href]


@resource(description=f"Fetch current roasts and meta from {base_url}")
def onyx_api_client(init_context):
    return OnyxScraper()

@resource(description=f"Mock responses from {base_url} for testing")
def onyx_mock_api_client(init_context):
    return OnyxMockScraper()
