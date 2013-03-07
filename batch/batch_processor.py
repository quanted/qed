import google.appengine.ext.db as db
import datetime
import time
import webapp2 as webapp
from django.utils import simplejson
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import sys
import logging


class BatchService(webapp.RequestHandler):
    
    def post(self):
        logger = logging.getLogger("BatchService")
        form = cgi.FieldStorage()
        logger.info(form)
    
    
app = webapp.WSGIApplication([('/batch/(.*)', BatchService)],
                                      debug=True)
def main():
  run_wsgi_app(app)

if __name__ == "__main__":
  main()