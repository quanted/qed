import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
import json
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
import logging
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../rice")
from rice.rice_output import RiceBatchRunner
sys.path.append("../terrplant")
ricePlantRunner = RiceBatchRunner()
from terrplant.terrplant_output import TerrPlantBatchRunner
terrPlantRunner = TerrPlantBatchRunner()
sys.path.append("../batch")
from batch import Batch
import pickle
from django.utils import simplejson

logger = logging.getLogger("BatchService")

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
    
def processUbertoolBatchRunsIntoBatchModelRuns(ubertools):
    logger.info("Start Ubertool Batching")
    batch_id = ubertools['id']
    user = users.get_current_user()
    q = db.Query(Batch)
    q.filter('user =',user)
    q.filter('key =',batch_id)
    batch = q.get()
    if not batch:
        batch = Batch()
        batch.user = user
    logger.info(batch.to_xml())
    ubertools_results = {}
    ubertools_data = ubertools['ubertools']
    for ubertool in ubertools_data:
        combined_ubertool_props = combineUbertoolProperties(ubertool)
        ubertool_id = combined_ubertool_props["ubertool-config-name"]
        ubertool_result = {}
        logger.info(combined_ubertool_props)
        ubertool_result = terrPlantRunner.runTerrPlantModel(combined_ubertool_props,ubertool_result)
        #perform on all other eco models
        ubertools_results[ubertool_id]=ubertool_result
    batch.completed = db.DateTimeProperty.now()
    results_pickle = pickle.dumps(ubertools_results)
    batch.ubertool_results = results_pickle
    batch.put()
    logger.info(batch.to_xml())
    
        
def combineUbertoolProperties(ubertool):
    combined_ubertool_props = {}
    for key in ubertool:
        if key == "config_name":
            combined_ubertool_props["ubertool-config-name"] = ubertool[key]
        else:
            ubertool_config = ubertool[key]
            for config_key in ubertool_config:
                if not config_key == "config_name":
                    combined_ubertool_props[config_key] = ubertool_config[config_key]
    return combined_ubertool_props
    
def processVariousBatchRunsIntoBatchModelRuns(data):
    logger.info(data)

class BatchService(webapp.RequestHandler):
        
    def post(self):
        data = json.loads(self.request.body)
        data = convert(data)
        logger.info(data)
        if 'ubertools' in data:
            processUbertoolBatchRunsIntoBatchModelRuns(data)
        else:
            processVariousBatchRunsIntoBatchModelRuns(data)
        batch_json = simplejson.dumps(data['id'])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)
        
        
application = webapp.WSGIApplication([('/batch', BatchService)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()