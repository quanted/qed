# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import cgi
import cgitb
from vvwm import vvwm_model, vvwm_tables
import keys_Picloud_S3
import base64
import urllib
import json
from google.appengine.api import urlfetch
import logging
logger = logging.getLogger('vvwm Model')

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
########call the function################# 
def save_dic(output_html, model_object_dict, model_name):
    all_dic = {"model_name":model_name, "_id":model_object_dict['jid'], "run_type":"single", "output_html":output_html, "model_object_dict":model_object_dict}
    data = json.dumps(all_dic)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/save_history'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   


class vvwmOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        args={}
        for key in form:
            args[key] = form.getvalue(key)
        vvwm_obj = vvwm_model.vvwm(args)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'vvwm','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'vvwm', 
                'model_attributes':'VVWM Output'})
        html = html + vvwm_tables.table_all(vvwm_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        # save_dic("", przm5_obj.__dict__, 'przm5')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', vvwmOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    