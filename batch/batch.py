#Create flexible object containing a dictionary of inputs, outputs, target operation, batch id for processing and retrieval
from google.appengine.ext import db
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
import numpy as np
import cgi
import cgitb
cgitb.enable()
from django.utils import simplejson
import logging

logger = logging.getLogger("Batch")

class Batch(db.Expando):
    user = db.UserProperty
    created = db.DateTimeProperty(auto_now_add=True)
    completed = db.DateTimeProperty
    
class BatchResultsService(webapp.RequestHandler):
    
    def get(self,batch_run_id):
        user = users.get_current_user()
        q = db.Query(Batch)
        q.filter('user =',user)
        q.filter('key =',batch_run_id)
        batch = q.get()
        batch_results['complete'] = false
        batch_json = None
        if batch.ubertools_results:
            batch_results['ubertool_data'] = batch.ubertools_results
            batch_json = simplejson.dumps(batch_results)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)
        
class BatchConfigurationNamesService(webapp.RequestHandler):
    
    def get(self):
        batch_dict = {}
        user = users.get_current_user()
        q = db.Query(Batch)
        #q.filter('user =',user)
        for batch in q:
            batch_completion = False
            if batch.completed:
                batch_completion = True
            batch_dict[batch.key()] = batch.completed
        logger.info(batch_dict)
        batch_json = simplejson.dumps(batch_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)

        
application = webapp.WSGIApplication([('/batch_results/(.*)', BatchResultsService),
                                      ('/batch_configs', BatchConfigurationNamesService)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()