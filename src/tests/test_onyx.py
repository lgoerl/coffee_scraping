import pickle, logging
from mock import patch
from dags.resources import (
    OnyxMockScraper,
    daily_partitioned_config,
    RESOURCES_PROD
)
from dags.jobs.scrape_onyx import get_active_products, scrape_onyx_test
from dagster.utils import file_relative_path

scraper = OnyxMockScraper()

class TestOnyxScraper():
    # @patch.object(scraper, "get_url", new=lambda x,headers: api_responses[x])
    def test_get_active_roasts(self):
        # import pytest; pytest.set_trace()
        assert set(scraper.get_active_roasts()) == set([
            '/products/southern-weather', '/products/geometry', '/products/monarch', '/products/power-nap',\
            '/products/tropical-weather', '/products/krampus', '/products/framily', '/products/decaf-colombia-aponte-village',\
            '/products/mexico-la-ilusion-coe-4', '/products/ethiopia-basha-bekele-zero-o2-natural',\
            '/products/ethiopia-worka-chelbesa-anaerobic', '/products/colombia-jose-salazar-coe-6',\
            '/products/animal-collective-collaboration', '/products/panama-carolyn-saraceni-anaerobic',\
            '/products/costa-rica-las-lajas-yellow-honey','/products/colombia-juan-jimenez',\
            '/products/ethiopia-negusse-nare-low-o2', '/products/costa-rica-volcan-azul-anaerobic-sl-28',\
            '/products/el-salvador-santa-rosa', '/products/colombia-aponte-village', '/products/ethiopia-negusse-nare-bombe-natural',\
            '/products/decaf-colombia-el-vergel', '/products/ethiopia-dumerso-layered', '/products/costa-rica-las-lajas-natural-2',\
            '/products/costa-rica-cascara', '/products/cold-brew', '/products/eclipse'
        ])

    # @patch.object(scraper, "get_url", new=lambda x,headers: api_responses[x])
    def test_get_roast(self):
        assert scraper.get_roast("/products/geometry") == {
            "href": "/products/geometry",
            "roaster": "Onyx",
            "name": " Geometry",
            "description": 'Geometry has been defined as "describing spaces that lie beyond the normal range of human experience." Soon it will also be defined as "that coffee from Onyx that I am in love with and completely redefined my relationship with coffee."\nIt\'s our answer for everything and has two of our favorite coffees—a washed processed Ethiopian & Colombian. This blend has become one of our favorite coffees. We love it as a filter coffee, and we love it as espresso. And not only does is it taste great as either but it\'s easy to dial in as espresso or filter.',
            "origin": "Colombia, Ethiopia",
            "process": "Washed",
            "elevation": "1950 - 2100 Meters",
            "tasting_notes": "Berries, Sweet Lemon, Earl Grey, Honey, Silky & Round"
        }

class TestOnyxJob():
    @patch.object(scraper, "get_url", new=lambda x,headers: api_responses[x])
    def test_job(self):
        result = scrape_onyx_test.execute_in_process(partition_key=None)
        # import pytest; pytest.set_trace()
        assert result.success
