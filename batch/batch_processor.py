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

def processUbertoolBatchRunsIntoBatchModelRuns(data):
    logger.info(data)
    
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