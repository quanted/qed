# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012
@author: tao.hong
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
import json
cgitb.enable()
import base64
from google.appengine.api import urlfetch
import sys
import keys_Picloud_S3

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################  

def get_jid(pdf_t, pdf_nop, pdf_p):
    all_dic={"pdf_t" : pdf_t, 
             "pdf_nop" : pdf_nop, 
             "pdf_p" : pdf_p}
    data=json.dumps(all_dic)
    url=url_part1 + '/get_html'
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60) 
    output_val = json.loads(response.content)['result']
    return output_val

class htmlPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        pdf_t = form.getvalue('pdf_t')
        pdf_nop = form.getvalue('pdf_nop')
        pdf_p = json.loads(form.getvalue('pdf_p'))
        final_res=get_jid(pdf_t, pdf_nop, pdf_p)
        text_file2 = open('about_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/templates/'
        html = template.render(templatepath + 'popup_eco.html', {
            'title':'Ubertool',
            'model_page':final_res,
            'model_attributes':'Please download your HTML here','text_paragraph':''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', htmlPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  
