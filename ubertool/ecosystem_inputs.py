import google.appengine.ext.db as db
import datetime
import time

class EcosystemInputs(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    concentration_of_particulate_organic_carbon = db.FloatProperty() 
    concentration_of_dissolved_organic_carbon = db.FloatProperty() 
    concentration_of_dissolved_oxygen = db.FloatProperty() 
    water_temperature = db.FloatProperty() 
    concentration_of_suspended_solids = db.FloatProperty() 
    sediment_organic_carbon = db.FloatProperty() 
    created = db.DateTimeProperty(auto_now_add=True)