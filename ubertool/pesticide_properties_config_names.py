import google.appengine.ext.db as db
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
import logging
    
class PesticidePropertiesConfigNamesService(webapp.RequestHandler):
    
    def get(self):
        logger = logging.getLogger("PesticidePropertiesConfigNamesService")
        user = users.get_current_user()
        q = db.Query(PestService)
        q.filter('user =',user)
        pests = q.run()
        pest_config_names = []
        for pest in pests:
            pest_config_names.append(pest.config_name)
        pest_dict = {}
        pest_dict['config_names'] = pest_config_names
        pest_json = simplejson.dumps(pest_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(pest_json)

application = webapp.WSGIApplication([('/pest-config-names',PesticidePropertiesConfigNamesService)],
                                      debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()