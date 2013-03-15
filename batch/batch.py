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
import pickle

logger = logging.getLogger("Batch")

class Batch(db.Expando):
    user = db.UserProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    ubertool_results = db.TextProperty()
    ubertools = db.TextProperty()
    completed = db.DateTimeProperty()
    
class BatchResultsService(webapp.RequestHandler):
    
    def get(self,batch_run_id):
        user = users.get_current_user()
        '''
        q = db.Query(Batch)
        q.filter('user =',user)
        q.filter('key = ', batch_run_id)
        '''
        batchs = Batch.all()
        batch = None
        for poss_batch in batchs:
            if str(poss_batch.key()) == batch_run_id and str(poss_batch.user) == str(user):
                batch = poss_batch
                batch.user = user
        logger.info(batch.to_xml())
        if not batch:
            batch = Batch()
            batch.user = user
            logger.info(batch.to_xml())
        batch_results = {}
        batch_json = None
        if batch.ubertool_results:
            batch_results['ubertool_data'] = pickle.loads(batch.ubertool_results)
            if batch.completed:
                batch_results['completed'] = str(batch.completed)
        batch_json = simplejson.dumps(batch_results)
        logger.info(batch_json)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)
        
class BatchConfigurationNamesService(webapp.RequestHandler):
    
    def get(self):
        batch_dict = {}
        user = users.get_current_user()
        q = db.Query(Batch)
        q.filter('user =',user)
        for batch in q:
            batch_completed = False
            if batch.completed:
                batch_completed = str(batch.completed)
            batch_dict[str(batch.key())] = batch_completed 
        #logger.info(batch_dict)
        batch_json = simplejson.dumps(batch_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)

        
application = webapp.WSGIApplication([('/batch_results/(.*)', BatchResultsService),
                                      ('/batch_configs', BatchConfigurationNamesService)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()