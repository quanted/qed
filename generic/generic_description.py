
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: jharston
"""
import webapp2 as webapp
# from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from uber import uber_lib

# from django.views.generic import View
# from django.shortcuts import render, get_object_or_404, render_to_response
# from django.template.loader import render_to_string
# from django.http import HttpResponse

class genericDescriptionPage(webapp.RequestHandler):
    def get(self):
        text_file = open('generic/generic_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Generic Description")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'generic','page':'description'})
        html = html + template.render(templatepath + '03ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04ubertext_start.html', {
                'model_page':'#', 
                'model_attributes':'Generic Overview', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([(r'/.*', genericDescriptionPage)], debug=True)

# def main():
#     run_wsgi_app(app)

# if __name__ == '__main__':
#     main()
# 

# class genericDescriptionPage(View):
#     def get(self, request):
#         text_file = open('generic/generic_description.txt','r')
#         x = text_file.read()
        
#         html = render_to_string('01uberheader.html', {'title':'Ubertool'})
#         html = html + render_to_string('02uberintroblock_wmodellinks.html', {'model':'generic','page':'description'})
#         html = html + render_to_string('03ubertext_links_left.html', {})                       
#         html = html + render_to_string('04ubertext_start.html', {
#                 'model_page':'#', 
#                 'model_attributes':'Generic Overview', 
#                 'text_paragraph':x})
#         html = html + render_to_string('04ubertext_end.html', {})
#         html = html + render_to_string('05ubertext_links_right.html', {})
#         html = html + render_to_string('06uberfooter.html', {'links': ''})

#         response = HttpResponse()
#         response.write(html)

# app = webapp.WSGIApplication([('/(.*?)_description\.html', genericDescriptionPage)], debug=True)

# def main():
#     run_wsgi_app(app)

# if __name__ == '__main__':
#     main()
