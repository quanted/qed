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
from rice.rice_output import RiceBatchRun

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
    for ubertool in ubertools:
        combined_ubertool_props = combineUbertoolProperties(ubertool)
        logger.info(ubertools)
        
def combineUbertoolProperties(ubertool):
    combined_ubertool_props = {}
    for key in ubertool:
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
            processUbertoolBatchRunsIntoBatchModelRuns(data['ubertools'])
        else:
            processVariousBatchRunsIntoBatchModelRuns(data)
        batch_json = simplejson.dumps(batch_dict['id'])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(batch_json)
        
        
application = webapp.WSGIApplication([('/batch', BatchService)],debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()