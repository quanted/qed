import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv
from przm import przm_batchmodel, przm_batchoutput
import json
import base64
import urllib
from google.appengine.api import urlfetch
import keys_Picloud_S3
import logging
logger = logging.getLogger('PRZM Batch Model')
from uber import uber_lib
# from threading import Thread
# import Queue
# import multiprocessing
from collections import OrderedDict
# import rest_funcs
# from google.appengine.api import taskqueue
from google.appengine.api import background_thread
import sys

class przmBatchOutputPageBackend(webapp.RequestHandler):
    def post(self):
        data_all = sys.stdin
        loggger.info(data_all)
        # html=""
        # iter_html = przm_batchmodel.loop_html(thefile)
        t = background_thread.BackgroundThread(target=przm_batchoutput.przmBatchOutputPage, args=[thefile])
        t.start()
        # logging(t)
        # self.response.out.write(html)

app = webapp.WSGIApplication([('/backend.html', przmBatchOutputPageBackend)], debug=True)
