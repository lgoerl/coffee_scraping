import hasher
import sqlalchemy
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, roaster):
        self.return_columns = ["roaster", "name", "origin", "description", "active", "updated_on"]
        self.roaster = roaster
    
    @abstractmethod
    def get_active_roasts(self):
        pass
    
    @abstractmethod
    def get_roast(self):
        pass
