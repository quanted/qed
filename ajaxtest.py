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
import math 
import cgitb
import json

cgitb.enable()
import base64
import urllib
from google.appengine.api import urlfetch
from datetime import datetime,timedelta

import sys
# lib_path = os.path.abspath()
# sys.path.append(lib_path)
import keys_Picloud_S3

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################  

# def get_jid(pdf_t, pdf_nop, pdf_p):

#     url='https://api.picloud.com/r/3303/generatepdf_pi_s1'
#     input_str=[pdf_t, pdf_nop, pdf_p]
#     input_str=json.dumps(input_str)
#     data = urllib.urlencode({"input_str":input_str})
#     response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
#     jid= json.loads(response.content)['jid']
#     output_st = "running"
    
#     while output_st!="done":
#         response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
#         output_st = json.loads(response_st.content)['info']['%s' %jid]['status']
    

#     url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
#     response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
#     output_val = json.loads(response_val.content)['result']
#     return(jid, output_st, output_val)

# class ajaxTest(webapp.RequestHandler):
#     def post(self):
#         # form = cgi.FieldStorage()   
#         # pdf_t = form.getvalue('pdf_t')
#         # pdf_nop = form.getvalue('pdf_nop')
#         # pdf_p = json.loads(form.getvalue('pdf_p'))
#         # final_res=get_jid(pdf_t, pdf_nop, pdf_p)[2]
#         templatepath = os.path.dirname(__file__) + '/templates/'
#         # html = template.render(templatepath + 'popup_eco.html', {
#         #     'title':'Ubertool',
#         #     'model_page':final_res,
#         #     'model_attributes':'Please download your PDF here','text_paragraph':''})
#         self.response.out.write(html)

def urlCheck():
    check = urlfetch.fetch(url='https://api.picloud.com/job/?jids=3700&field=status', headers=http_headers)
    check_output = json.loads(check.content)['info']['%s' %jid]['status']
    return check_output

class ajaxTest(webapp.RequestHandler):
    def post(self):
        templatepath = os.path.dirname(__file__) + '/templates/'
        urlCheck = urlCheck()
        html = template.render(templatepath + 'popup_ajaxTest.html')
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', ajaxTest)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  