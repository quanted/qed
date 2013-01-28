import google.appengine.ext.db as db
import datetime
import time

class AquaticToxicity(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    acute_toxicity_target_concentration_for_freshwater_fish = db.FloatProperty()
    chronic_toxicity_target_concentration_for_freshwater_fish = db.FloatProperty()
    acute_toxicity_target_concentration_for_freshwater_invertebrates = db.FloatProperty()
    chronic_toxicity_target_concentration_for_freshwater_invertebrates = db.FloatProperty() 
    toxicity_target_concentration_for_nonlisted_vascular_plants = db.FloatProperty()
    toxicity_target_concentration_for_listed_vascular_plants = db.FloatProperty()
    toxicity_target_concentration_for_duckweed = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)