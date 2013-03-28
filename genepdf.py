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
import cgi
import math 
import cgitb
import json

cgitb.enable()
from pfam import input_edit
import base64
import urllib
from google.appengine.api import urlfetch
from datetime import datetime,timedelta

############Provide the key and connect to the picloud####################
api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################  

def get_jid(input_str):

    url='https://api.picloud.com/r/3303/generatepdf_pi_s1'

    input_str=json.dumps(input_str)

    data = urllib.urlencode({"input_str":input_str})

    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
    jid= json.loads(response.content)['jid']
    output_st = ''
        
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)



class pdfPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        extract = form.getvalue('extract')
        # extract_json = json.dumps(extract)
        final_res=get_jid(extract)[2]
               
        text_file2 = open('about_text.txt','r')
        xx = text_file2.read()
        templatepath = os.path.dirname(__file__) + '/templates/'                     
        html = template.render(templatepath+'01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath+'02uberintroblock_nomodellinks.html', {'title2':'Ecological Risk Web Applications','title3':''})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                        
        html = html + template.render(templatepath + '04ubertext_start.html', {
            'model_page':final_res,
            'model_attributes':'Please download your PDF here','text_paragraph':''})
        html = html + extract
        html = html + template.render (templatepath+'04ubertext_end.html',{})
        html = html + template.render (templatepath+'05ubertext_links_right.html', {})
        html = html + template.render(templatepath+'06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', pdfPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  