# Tier I Rice Model v1.0

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
# from google.appengine.api import users
# from google.appengine.ext import db
import numpy as np
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../rice")
from rice import rice_model,rice_parameters,rice_tables
import datetime
from uber import uber_lib

class RiceExecutePage(webapp.RequestHandler):
    def post(self):
        # logger = logging.getLogger("UbertoolUseConfigurationPage")
        form = cgi.FieldStorage() 
        # config_name = str(form.getvalue('config_name'))


        # user = users.get_current_user()
        # if user:
        #     logger.info(user.user_id())
        #     rice.user = user
        # rice.config_name = config_name


        chemical_name = form.getvalue('chemical_name')
        mai = form.getvalue('mai')
        dsed = form.getvalue('dsed')
        a = form.getvalue('area')
        pb = form.getvalue('pb')
        dw = form.getvalue('dw')
        osed = form.getvalue('osed')
        kd = form.getvalue('Kd')
        rice_obj = rice_model.rice(True,True,chemical_name, mai, dsed, a, pb, dw, osed, kd)


        # rice.put()
        # q = db.Query(rice_model.Rice)
        # q.filter("user =", user)
        # q.filter("config_name =", config_name)
        # for new_use in q:
        #     logger.info(new_use.to_xml())


        text_file = open('rice/rice_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Rice Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html',{
                'model':'rice', 
                'model_attributes':'Rice Model Output'})
        html = html + rice_tables.timestamp()
        html = html + rice_tables.table_all(rice_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
