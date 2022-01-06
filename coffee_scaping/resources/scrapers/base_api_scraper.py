import hasher
import sqlalchemy

class BaseScraper():
    def __init__(self, roaster, sql_engine):
        self.return_columns = ["roaster", "name", "origin", "description", "active", "updated_on"]
        self.roaster = roaster
        self.engine = sql_engine
        
    def get_active_roasts(self):
        pass
    
    def set_missing_to_inactive(self):
        pass
    
    def upsert_df(self):
        pass
        
    def notify(self):
        pass

    def extract_df(self):
        pass
    
    def execute(self):
        active_roasts = self.get_active_roasts()
        df = self.extract_df()
        df = df.merge(active_roasts, on=[], how="outer")
        df = self.set_missing_to_inactive(df)
        self.upsert_df(df)