import google.appengine.ext.db as db
import datetime
import time

class Ubertool(db.Model):
    
    def __init__(self, name, user, inputPageBased=True, **kwargs):
        if inputPageBased:
            self.initViaInputPageData(**kwargs)
        else:
            self.initViaConfiguration(**kwargs)
        pass
        
    def initViaInputPageData(self, **kwargs):
        pass
    
    def initViaConfiguration(self, **kwargs):
        pass