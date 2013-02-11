import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
sys.path.append("../utils")
sys.path.append('../CAS')
from CAS.CASGql import CASGql

class UseService(webapp.RequestHandler):
    
    def get(self, use_config_name):
        user = users.get_current_user()
        q = db.Query(Use)
        q.filter('user =',user)
        q.filter('config_name =',use_config_name)
        use = q.get()
        use_dict = {}
        use_dict['cas_number'] = use.cas_number
        cas = CASGql("apppest:cas","CAS")
        use_dict['formulated_product_name'] = use.formulated_product_name 
        use_dict['percent_ai'] = use.percent_ai
        use_dict['met_file'] = use.met_file 
        use_dict['przm_scenario'] = use.przm_scenario
        use_dict['exams_environment_file'] = use.exams_environment_file 
        use_dict['application_method'] = use.application_method
        use_dict['application_type'] = use.application_type 
        use_dict['app_type'] = use.app_type
        use_dict['weight_of_one_granule'] = use.weight_of_one_granule 
        use_dict['wetted_in'] = use.wetted_in
        use_dict['incorporation_depth'] = use.incorporation_depth 
        use_dict['percent_incorporated'] = use.percent_incorporated
        use_dict['application_kg_rate'] = use.application_kg_rate 
        use_dict['application_lbs_rate'] = use.application_lbs_rate
        use_dict['seed_treatment_formulation_name'] = use.seed_treatment_formulation_name 
        use_dict['density_of_product'] = use.density_of_product
        use_dict['maximum_seedling_rate_per_use'] = use.maximum_seedling_rate_per_use 
        use_dict['application_rate_per_use'] = use.application_rate_per_use
        use_dict['application_date'] = use.application_date.__str__()
        use_dict['number_of_applications'] = use.number_of_applications
        use_dict['interval_between_applications'] = use.interval_between_applications 
        use_dict['application_efficiency'] = use.application_efficiency
        use_dict['spray_drift'] = use.spray_drift 
        use_dict['runoff'] = use.runoff 
        #use_json = simplejson.dumps(data)
        self.response.out.write(use_dict)
        

class Use(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    cas_number = db.StringProperty()
    formulated_product_name = db.StringProperty()
    percent_ai = db.FloatProperty() 
    met_file = db.StringProperty()
    przm_scenario = db.StringProperty()
    exams_environment_file = db.StringProperty()
    application_method = db.StringProperty()
    application_type = db.StringProperty()
    app_type = db.StringProperty()
    weight_of_one_granule = db.FloatProperty()
    wetted_in = db.BooleanProperty()
    incorporation_depth = db.FloatProperty()
    percent_incorporated = db.FloatProperty()
    application_kg_rate = db.FloatProperty()
    application_lbs_rate = db.FloatProperty()
    seed_treatment_formulation_name = db.StringProperty()
    density_of_product = db.FloatProperty()
    maximum_seedling_rate_per_use = db.FloatProperty()
    application_rate_per_use = db.FloatProperty()
    application_date = db.DateProperty()
    number_of_applications = db.FloatProperty()
    interval_between_applications = db.FloatProperty()
    application_efficiency = db.FloatProperty()
    spray_drift = db.FloatProperty()
    runoff = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)

application = webapp.WSGIApplication([('/use/(.*)', UseService)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()