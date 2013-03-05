import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

class EcosystemInputsService(webapp.RequestHandler):
    def get(self, ecosys_inputs):
        user = users.get_current_user()
        q = db.Query(EcosystemInputs)
        q.filter('user =',user)
        q.filter('config_name =',eco_inputs)
        ecosys = q.get()
        use_dict = {}
        use_dict['concentration_of_particulate_organic_carbon']=ecosys.concentration_of_particulate_organic_carbon
        use_dict['concentration_of_dissolved_organic_carbon']=ecosys.concentration_of_dissolved_organic_carbon
        use_dict['concentration_of_dissolved_oxygen']=ecosys.concentration_of_dissolved_oxygen
        use_dict['water_temperature']=ecosys.water_temperature
        use_dict['concentration_of_suspended_solids']=ecosys.concentration_of_suspended_solids
        use_dict['sediment_organic_carbon']=ecosys.sediment_organic_carbon
        use_json = simplejson.dumps(use_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(use_json)

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
    
application = webapp.WSGIApplication([('/ecosys/(.*)', EcosystemsInputsService)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()