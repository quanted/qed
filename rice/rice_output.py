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
from rice import rice_model
import logging


# The mass of the sediment at equilibrium with the water column

def msed(dsed,a,pb):
    try:
        dsed = float(dsed)
        a = float(a)
        pb = float(pb)
    except IndexError:
        raise IndexError\
        ('The sediment depth, area of the rice paddy, and/or the bulk'\
        ' density of the sediment must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The sediment depth must be a real number, not "%m"' % dsed)
    except ValueError:
        raise ValueError\
        ('The area of the rice paddy must be a real number, not "%ha"' % a)
    except ValueError:
        raise ValueError\
        ('The bulk density of the sediment must be a real number, not "%kg/m3".' %pb)
    if dsed < 0:
        raise ValueError\
        ('dsed=%g is a non-physical value.' % dsed)
    if a < 0:
        raise ValueError\
        ('a=%g is a non-physical value.' % a)
    if pb < 0:
        raise ValueError\
        ('pb=%g is a non-physical value.' %pb)
    return dsed * a * pb




# The volume of the water column plus pore water

def vw(dw,a,dsed,osed):
    try:
        dw = float(dw)
        a = float(a)
        dsed = float(dsed)
        osed = float(osed)
    except IndexError:
        raise IndexError\
        ('The water column depth, area of the rice paddy, sediment depth, and/or'\
        ' porosity of sediment must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The water column depth must be a real number, not "%m"' % dw)
    except ValueError:
        raise ValueError\
        ('The area of the rice paddy must be a real number, not "%ha"' % a)
    except ValueError:
        raise ValueError\
        ('The sediment depth must be a real number, not "%cm"' % dsed)
    except ValueError:
        raise ValueError\
        ('The porosity of sediment must be a real number"' % osed)
    if dw < 0:
        raise ValueError\
        ('dw=%g is a non-physical value.' % dw)
    if a < 0:
        raise ValueError\
        ('a=%g is a non-physical value.' % a)
    if dsed < 0:
        raise ValueError\
        ('dsed=%g is a non-physical value.' % dsed)
    if osed < 0:
        raise ValueError\
        ('osed=%g is a non-physical value.' % osed)
    return(dw * a) + (dsed * osed * a)



# The pesticide mass per unit area

def mai1(mai,a):
    mai = float(mai)
    a = float(a)
    return mai/a
#    if a <= 0:
#     print('The area of the rice paddy must be greater than 0 m2')




# Water Concentration

def cw(mai1,dw,dsed,osed,pb,kd):
    try:
        mai1 = float(mai1)
        dw = float(dw)
        dsed = float(dsed)
        osed = float(osed)
        pb = float(pb)
        kd = float(kd)
    except IndexError:
        raise IndexError\
        ('The mass of pesticide applied per unit area, water column depth,'\
        ' the sediment depth, porosity of sediment, the bulk density of sediment,'\
        'and/or the water-sediment partitioning coefficient must be supplied on'\
        ' the command line.')
    except ValueError:
        raise ValueError\
        ('The mass of pesticide applied per unit area must be a real number, '\
        'not "%kg/ha"' %mai1)
    except ValueError:
        raise ValueError\
        ('The water column depth must be a real number, not "%cm"' % dw)
    except ValueError:
        raise ValueError\
        ('The sediment depth must be a real number, not "%cm"' %dsed)
    except ValueError:
        raise ValueError\
        ('The porosity of the sediment must be a real number' %osed)
    except ValueError:
        raise ValueError\
        ('The bulk density of the sediment must be a real number, not"%kg/m3"' %pb)
    except ValueError:
        raise ValueError\
        ('The water-sediment partitioning coefficient must be a real number,'\
        ' not"%kg/L"' %kd)
    if mai1 < 0:
        raise ValueError\
        ('mai1=%g is a non-physical value.' % mai1)
    if dw < 0:
        raise ValueError\
        ('dw=%g is a non-physical value.' % dw)
    if dsed < 0:
        raise ValueError\
        ('dsed=%g is a non-physical value.' % dsed)
    if osed < 0:
        raise ValueError\
        ('osed=g% is a non-physical value.' %osed)
    if pb < 0:
        raise ValueError\
        ('pb=g% is a non-physical value.' %pb)
    if kd < 0:
        raise ValueError\
        ('kd=g% is a non-physical value.' % kd)
    return mai1 / (dw + (dsed * (osed + (pb * kd))))


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
        rice.mai1_out=mai1(rice.mai, rice.a) 
        rice.cw_out=cw(rice.mai1_out, rice.dw, rice.dsed, rice.osed, rice.pb, rice.kd)
        rice.put()
            
        text_file = open('rice/rice_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'rice'})
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
        <td>Application Rate (lbs a.i./A)</td>
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
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', RiceExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

    
    

