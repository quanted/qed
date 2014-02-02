# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import httplib
import http_check_tables
from django.utils.safestring import mark_safe

class aboutPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/templates/'                     
        html = template.render(templatepath+'01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath+'02uberintroblock_nomodellinks.html', {'title2':'Ecological Risk Web Applications','title3':''})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {}) 

        #url needs to be modified to know what version/branch currently on and to run locally
        #print os.environ['CURRENT_VERSION_ID']
        url = "pypest.appspot.com"
        models = ["fdadiet", "idream", "ocexposure", "resexposure", "swim", "efast", "wpem", "iaqx", "antimicrobial", "consexpo", "rddr", "hedgas", "benchdose", "qsarhe",
            "dietexphe", "orehe", "inerts", "qsarreg", "dietexpreg", "orereg"]
        #qaqc takes too long and needs to be run separately
        pagenames=["_description.html", "_input.html", "_algorithms.html", "_references.html", "_batchinput.html", "_history.html"]
        url_strings = []
        http_counter = []
        http_page = []
        http_status = []
        http_reason = []

        for model in models:
            for pagename in pagenames:
                url_strings.append("/" + model + pagename)

        conn = httplib.HTTPConnection(host=url)
        xx=""
        counter = 0
        for url_string in url_strings:
            #conn = httplib.HTTPConnection(host=url)
            counter = counter + 1
            conn.request("GET",url_string)
            r1 = conn.getresponse()
            xx = "<p>" + xx + str(counter) + " " + mark_safe("<a href='http://" + url + url_string + "'>" + url_string + "</a>") + " " + str(r1.status) + " " + r1.reason + "<br>"
            http_counter.append(counter) 
            http_page.append(mark_safe("<a href='http://" + url + url_string + "'>" + url_string + "</a>")) 
            http_status.append(r1.status)
            http_reason.append(r1.reason)

        http_headings = http_check_tables.gethttpheader()
        http_html = http_check_tables.table_1(http_headings, http_counter, http_page, http_status, http_reason)
        #print dir(r1)
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'',
                'model_attributes':'Human Health Model Integration Testing','text_paragraph':http_html})
        #html = html + http_html
        html = html + template.render (templatepath+'04ubertext_end.html',{})
        html = html + template.render (templatepath+'05ubertext_links_right.html', {})
        html = html + template.render(templatepath+'06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', aboutPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()  