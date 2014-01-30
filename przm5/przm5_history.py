# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'

import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
from uber import uber_lib
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch
import json
import datetime, time
import history_tables
import logging
logger = logging.getLogger('Przm5 History')

class user_hist(object):
    def __init__(self, user_id, model_name):
        self.user_id = user_id
        self.model_name = model_name
    ############Provide the key and connect to the picloud####################
        api_key=keys_Picloud_S3.picloud_api_key
        api_secretkey=keys_Picloud_S3.picloud_api_secretkey
        base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
        http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
    ########call the function################# 
        self.all_dic = {"user_id": user_id, "model_name":model_name}
        self.data = json.dumps(self.all_dic)
        self.url=os.environ['UBERTOOL_REST_SERVER']+'/user_history'
        self.response = urlfetch.fetch(url=self.url, payload=self.data, method=urlfetch.POST, headers=http_headers, deadline=60)
        # logger.info(self.response.content)
        self.output_val = json.loads(self.response.content)['hist_all']
        self.total_num = len(self.output_val)
        self.user_id = []
        self.time_id = []
        self.jid = []
        self.run_type = []
        self.model_name = "przm5"

        for element in self.output_val:
            self.user_id.append(element['user_id'])
            self.jid.append(element['_id'])
            self.time_id.append(datetime.datetime.strptime(element['_id'], '%Y%m%d%H%M%S%f').strftime('%Y-%m-%d %H:%M:%S'))
            self.run_type.append(element['run_type'])
        # logger.info(self.time_id)



class PRZM5historyPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm5','page':'history'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04uberalgorithm_start.html', {
                'model':'przm5', 
                'model_attributes':'PRZM5 User History'})
        html = html + template.render (templatepath + 'history_pagination.html', {})                
        hist_obj = user_hist('admin', 'przm5')
        html = html + history_tables.table_all(hist_obj)
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZM5historyPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    

