# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import keys_Picloud_S3
import base64
import urllib
import json
import cgi, cgitb
cgitb.enable()
from google.appengine.api import urlfetch
import logging
logger = logging.getLogger('historyoutputPage')


api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
########call the function################# 

def get_output_html(jid, model_name):
    all_dic = {"jid":jid, "model_name":model_name}
    data = json.dumps(all_dic)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/get_html_output'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    html_output = json.loads(response.content)['html_output']
    return html_output

class historyoutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        jid = form.getvalue('jid')
        model_name = form.getvalue('model_name')
        html = get_output_html(jid, model_name)
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', historyoutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    

