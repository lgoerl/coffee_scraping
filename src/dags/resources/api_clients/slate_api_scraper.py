import gzip
import json
import logging
import requests
from bs4 import BeautifulSoup
from dagster import resource
from dagster.utils import file_relative_path
from mock import patch
from typing import Any, Dict, Optional

from .base_api_scraper import BaseScraper
from .responses import api_responses

roaster_name = "Slate"
base_url = "https://slatecoffee.com"
products_url = f"{base_url}/product-category/coffee"
request_header = {"User-Agent": "Mozilla/5.0"}

feature_map = {
    "region": "origin",
    "processing": "process",
}
ignore_href = []
# slate has extra features from baseline/Onyx: Producer and Cultivar

class SlateScraper(BaseScraper):
    def __init__(self):
        super().__init__(roaster_name)
        
    def get_active_roasts(self):
        response = self.get_url(products_url, headers=request_header)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find("div", class_="shop-container").find_all("a", class_=lambda v: v and "product__link" in v, href=True)
        if not products:
            raise ValueError(
                f"No products found. "+
                f"Check {products_url} to verify products are linked in <a> tags with class='product__view'"
            )
        return [p["href"] for p in products if p not in ignore_href]
    
    def get_roast(self, roast_href):
        roast_href = roast_href.replace(base_url, "")
        roast_url = base_url + roast_href
        logging.info(f"Scraping roast attributes at {roast_url}.")
        response = self.get_url(roast_url, headers=request_header)
        soup = BeautifulSoup(response.text, "html.parser")
        
        info_tags = soup.find("div", class_="product-short-description").find_all("p")
        if len(info_tags) != 4:
            raise ValueError(f"class product-short-description as unexpected shape at {roast_url}")
        features = {
            "roaster": "Slate",
            "href": roast_url.split(".com")[1],
        }
        attnames = []
        for t in info_tags[0].find_all("strong"):
            if t.find("span"):
                features["name"] = t.find("span").text
                attnames.append(t.text.split("\n")[1].lower())
            else:
                attnames.append(t.text.replace(u"\xa0", "").lower())
        attvals = [v.text for v in info_tags[0].find_all("em")]
        if len(attnames) != len(attvals):
            raise ValueError(f"strong/em key/value pairs have unexpected shape as {roast_url}")
        features.update({feature_map.get(k, k):v for k,v in zip(attnames, attvals)})
        features["tasting_notes"] = info_tags[2].text
        features["description"] = info_tags[3].text
        return features

class SlateMockScraper(SlateScraper):
    def __init__(self, pipeline_test=False):
        super().__init__()
        self.super = SlateScraper()
        self.api_responses = api_responses
        self.pipeline_test = pipeline_test

    def get_url(self, url, **kwargs):
        return api_responses[url]

    def get_active_roasts(self):
        if self.pipeline_test:
            return ["/product/ethiopia-shanta-wene/"]
        else:
            with patch.object(self.super, "get_url", new=lambda x,headers: api_responses[x]):
                return self.super.get_active_roasts()


@resource(description=f"Fetch current roasts and meta from {base_url}")
def slate_api_client(init_context):
    return SlateScraper()

@resource(description=f"Mock responses from {base_url} for testing")
def slate_mock_api_client(init_context):
    return SlateMockScraper(pipeline_test=True)
