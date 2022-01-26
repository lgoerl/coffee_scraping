import requests
import sqlalchemy
from abc import ABC, abstractmethod

return_columns = ["roaster", "name", "origin", "elevation", "description", "tasting_notes", "process"]

class BaseScraper(ABC):
    def __init__(self, roaster):
        self.return_columns = return_columns
        self.roaster = roaster

    def get_url(self, url, **kwargs):
        return requests.get(url, **kwargs)
    
    @abstractmethod
    def get_active_roasts(self):
        pass
    
    @abstractmethod
    def get_roast(self):
        pass
