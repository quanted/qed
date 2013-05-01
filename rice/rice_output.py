# Tier I Rice Model v1.0

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
import numpy as np
import cgi
import cgitb
cgitb.enable()
import datetime
import sys
#sys.path.append("./rice")
import rice as rice_model
import logging
sys.path.append("../utils")
import utils.json_utils


class RiceExecutePage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolUseConfigurationPage")       
        form = cgi.FieldStorage() 
        config_name = str(form.getvalue('config_name'))
        rice = rice_model.Rice()
        
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
            rice.user = user
        rice.config_name = config_name        
        rice.chemical_name = form.getvalue('chemical_name')
        rice.mai = float(form.getvalue('mai'))
        rice.dsed = float(form.getvalue('dsed'))
        rice.a = float(form.getvalue('area'))
        rice.pb = float(form.getvalue('pb'))
        rice.dw = float(form.getvalue('dw'))
        rice.osed = float(form.getvalue('osed'))
        rice.kd = float(form.getvalue('Kd'))
        rice.mai1_out=rice_model.mai1(rice.mai, rice.a) 
        rice.cw_out=rice_model.cw(rice.mai1_out, rice.dw, rice.dsed, rice.osed, rice.pb, rice.kd)
        rice.put()
        q = db.Query(rice_model.Rice)
        q.filter("user =", user)
        q.filter("config_name =", config_name)
        for new_use in q:
            logger.info(new_use.to_xml())
        text_file = open('rice/rice_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html',{
                'model':'rice', 
                'model_attributes':'Rice Model Output'})     
        html = html + """
        <table border="1">
        <tr><H3>User Inputs</H3></tr>
        <tr>
        <td>Input Name</td>
        <td>Value</td>
        <td>Unit</td>
        </tr>        
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        <td>-</td>
        </tr>
        <tr>
        <td>Mass of Applied Ingredient Applied to Paddy</td>
        <td>%s</td>
        <td>kg</td>
        </tr>
        <tr>
        <td>Sediment Depth</td>
        <td>%s</td>
        <td>m</td>
        </tr>
        <tr>
        <td>Area of the Rice Paddy</td>
        <td>%s</td>
        <td>m<sup>2</sup></td>
        </tr>
        <tr>
        <td>Bulk Density of Sediment</td>
        <td>%s</td>
        <td>kg/m<sup>3</sup></td>
        </tr>
        <tr>
        <td>Water Column Depth</td>
        <td>%s</td>
        <td>m</td>
        </tr>
        <tr>
        <td>Porosity of Sediment</td>
        <td>%s</td>
        <td>-</td>
        </tr>
        <tr>
        <td>Water-Sediment Partitioning Coefficient</td>
        <td>%s</td>
        <td>L/kg</td>
        </table>
        """ % (rice.chemical_name, rice.mai, rice.dsed, rice.a, rice.pb, rice.dw, rice.osed, rice.kd)
        html = html + """
        <table border="1">
        <tr><H3>Rice Model Outputs</H3></tr><br>
        <tr>Tier I Surface Water Estimated Exposure Concentrations (EEC) of %s From Use on Rice</tr>
        <tr>
        <td>Source</td>
        <td>Application Rate (kg a.i./A)</td>
        <td>Peak & Chronic EEC (&microg/L)</td>
        </tr>
        <tr>
        <td>Paddy Water/Tail Water</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        </table>
        """  % (rice.chemical_name, rice.mai1_out, rice.cw_out)             
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceExecutePage)],
                              debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

    
    

