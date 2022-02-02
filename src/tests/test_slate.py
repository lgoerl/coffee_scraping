import pickle, logging
from mock import patch
from dags.resources import (
    SlateMockScraper,
    daily_partitioned_config,
    RESOURCES_PROD
)
from dags.jobs.scrape_slate import get_active_products, scrape_slate_test
from dagster.utils import file_relative_path

scraper = SlateMockScraper()

class TestSlateScraper():
    def test_get_active_roasts(self):
        # import pytest; pytest.set_trace()
        assert set(scraper.get_active_roasts()) == set([
            'https://slatecoffee.com/product/ethiopia-shanta-wene/',
            'https://slatecoffee.com/product/guatemala-bella-carmona/',
            'https://slatecoffee.com/product/el_sal_las_ninfas/',
            'https://slatecoffee.com/product/slate-bells-ringing/',
            'https://slatecoffee.com/product/kenya-karimikui-aa/',
            'https://slatecoffee.com/product/nightcap-decaf/',
            'https://slatecoffee.com/product/unfiltered/',
            'https://slatecoffee.com/product/crema/',
            'https://slatecoffee.com/product/cream_sugar/',
            'https://slatecoffee.com/product/under-pressure/',
        ])

    def test_get_roast(self):
        assert scraper.get_roast("https://slatecoffee.com/product/ethiopia-shanta-wene/") == {
            "href": "/product/ethiopia-shanta-wene/",
            "name": "GEDEO ZONE, ETHIOPIA",
            "roaster": "Slate",
            "producer": "1000 smallholder farmers",
            "origin": "Shanta Wene, Bensa Woreda, Sidama, Ethiopia",
            "cultivar": "Kurume",
            "process": "Full natural and dried on raised beds",
            "elevation": "1900 – 2100 masl",
            "tasting_notes": "Boysenberry Syrup, Licorice, Dark Chocolate",
            "description": "Shanta Wene is located in the region of Sidama, know for its complex, spicy, and citric coffees. However, the farms around Shanta Wene are located in Bensa Woreda micro-region, which produces very unique profiles from the rest of the coffees in the greater Sidama Zone. Coffees from Bensa are know to be uniquely fruity and very rich with standout berry and tropical notes. Sidama has one of the most robust cooperative unions in Ethiopia with 53 member cooperatives, as well as a thriving industry of independent washing stations. Testi Ayla is one such independent washing station, operated by Faysel Yonis. Located in Shanta Wene, a small community in eastern Sidama, close to the Harenna Forest preserve. Testi Ayla receives coffee cherries from 1000 smallholder farmers with land averaging only two hectares. These farms are located on some of the highest elevations in the whole of Sidama. This grade 1 natural, which is rare for the region, is dried and dehydrated slowly due to the cool nights and hot afternoon hours. The result is a clean, boysenberry-like cup with abundant complexity and a surprisingly creamy mouthfeel. Upon tasting, you will be greeted by a lingering sweet boysenberry syrup, followed by a unique licorice note and finishing with a rich dark chocolate aftertaste."
        }

class TestSlateJob():
    def test_job(self):
        result = scrape_slate_test.execute_in_process(partition_key=None)
        assert result.success
