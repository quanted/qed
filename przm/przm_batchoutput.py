import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from przm import przm_batchmodel, przm_tables
import json
import base64
import urllib
import logging
logger = logging.getLogger('PRZM Batch Model')
from uber import uber_lib
from datetime import datetime,timedelta
import time
import csv

def generate_batch_jid():
    ts = datetime.now()
    if(time.daylight):
        ts1 = timedelta(hours=-4)+ts
    else:
        ts1 = timedelta(hours=-5)+ts
    batch_jid = ts1.strftime('%Y%m%d%H%M%S%f')
    return batch_jid

class przmBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        przm_batchmodel.loop_html(thefile, generate_batch_jid())
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm',
                'model_attributes':'PRZM Batch Output'})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przmBatchOutputPage)], debug=True)


def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
