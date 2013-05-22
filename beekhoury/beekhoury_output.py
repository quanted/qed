# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:34:41 2012

@author: msnyde02
"""

# -*- coding: utf-8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from beekhoury import beekhourydb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
import math

cgitb.enable()

  
# calculate mortality from input mortality values
def m_f(mo, deltam):
    m = mo + deltam
    return m

#eclosion rate function
def e_f(l, w, n):
    e = l * (n / (w + n))
    return e
#recruitment rate function
def r_f(alpha, theta, h, f):
    r = alpha - theta*(f/(h + f))
    return r    
#Rate of increase of forager numbers    
def hr_f(h, r):
    hr = h * r
    return hr
#rate of change of hive bee numbers
def dhdt_f(e, hr):
    dhdt = e - hr
    return dhdt
#rate of change of forager numbers
def dfdt_f(hr, f, mo, deltam):
    m = m_f(mo, deltam)
    dfdt = hr - (m * f)
    return dfdt

#foragers = []
#insides = []
#totalbees = []
def hive(t, no, l, w, alpha, theta, mo, deltam):
    foragers = []
    insides = []
    totalbees = []
    recruit = []
    f = no*0.25
    h = no - f
    n=no
    for i in range(1,t,1):
        e = e_f(l, w, n)
        r = r_f(alpha, theta, h, f)
        hr = hr_f(h, r)
        dhdt = dhdt_f(e, hr)
        dfdt = dfdt_f(hr, f, mo, deltam)
        h = h + dhdt
        f = f + dfdt
        n = h + f
        recruit.append(r)
        foragers.append(f)
        insides.append(h)
        totalbees.append(n)
        #print recruit
    return foragers, insides, totalbees, recruit

       
class beekhouryOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        w = float(form.getvalue('w'))
        alpha = float(form.getvalue('alpha'))
        theta = float(form.getvalue('theta'))
        l = float(form.getvalue('l'))
        mo = float(form.getvalue('mo'))
        deltam = float(form.getvalue('deltam'))
        no = float(form.getvalue('no'))
        t = int(form.getvalue('t'))
    
        m = m_f(mo, deltam)
  #      hive = hive(t, e, r, hr, dhdt, dfdt, no, l, w, n, alpha, theta, mo, deltam)
        # assign value at the 41st day to the precruit variable so it can be used in the age function
        precruit = hive(t, no, l, w, alpha, theta, mo, deltam)[3][40] 
        
# function to determine average age onset of foraging 
        def aaof_f(precruit, t):  
            stay = 1-precruit
            dayrecruit = 0
            aaof = 0.0
            timestep = 1
            for i in range(1,t+1,1):
                #print precruit
                #print dayrecruit
                #print timestep                
                dayrecruit = timestep * precruit * (stay**(timestep-1))
                aaof = aaof + dayrecruit
                timestep = timestep + 1
            return aaof
# function to determine forager lifespan
        def lifespan_f(precruit, t, m, deltam):
            aaof = aaof_f(precruit, t)
            lifespan = (1/(m + deltam)) + aaof
            return lifespan

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'beekhoury','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'beekhoury', 
                'model_attributes':'Khoury Output'})
        html = html + """
        <div class="out_">
            <H3>User Inputs</H3>
            <table border="1">
                <tr>
                    <td>Egg Laying Rate Factor</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Alpha</td>
                    <td>%s</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Theta</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Daily Laying Rate</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Mortality</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Forager Mortality</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Colony Size</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Number of Days</td>
                    <td>%s</td>
                </tr>
            </table>
        </div>
        """ % (w, alpha, theta, l, mo, deltam, no, t)
        html = html + """
        <div class="out_">
            <H3>Outputs for the last day of the model run</H3>
            <table border="1">
                <tr>
                    <td>Total mortality</td>
                    <td>%.2f</td>
                </tr>
                <tr>
                    <td>Forager bees</td>
                    <td>%.0f</td>
                </tr>
                <tr>
                    <td>Hive bees</td>
                    <td>%.0f</td>
                </tr>
                <tr>
                    <td>Total bee population</td>
                    <td>%.0f</td>
                </tr>
                 <tr>
                    <td>Average age onset of foraging</td>
                    <td>%.2f</td>
                </tr>
                 <tr>
                    <td>Forager lifespan</td>
                    <td>%.2f</td>
                </tr>
            </table>
        </div>
        """% (m, hive(t, no, l, w, alpha, theta, mo, deltam)[0][t-2], hive(t, no, l, w, alpha, theta, mo, deltam)[1][t-2], hive(t, no, l, w, alpha, theta, mo, deltam)[2][t-2], aaof_f(precruit, t), lifespan_f(precruit, t, m, deltam))
        html = html +  """
        <table width="400" border="1", style="display:none">
            <tr>
                <td>hive_val_1</td>
                <td id="hive_val_1">%s</td>
            </tr>
            <tr>
                <td>hive_val_2</td>
                <td id="hive_val_2">%s</td>
            </tr>
            <tr>
                <td>hive_val_3</td>
                <td id="hive_val_3">%s</td>
            </tr>                                                    
        </table>
        """%(hive(t, no, l, w, alpha, theta, mo, deltam)[0],hive(t, no, l, w, alpha, theta, mo, deltam)[1],hive(t, no, l, w, alpha, theta, mo, deltam)[2])        
        html = html + template.render(templatepath + 'beekhoury-output-jqplot.html', {})         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
          
       
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', beekhouryOutputPage)], debug=True)
        
      
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()