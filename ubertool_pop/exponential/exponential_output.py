# -*- coding: utf-8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from logistic import logisticdb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb

cgitb.enable()
    
def exponentialgrow(N_o,rho,T):
    index_set = range(T+1)
    x = np.zeros(len(index_set))
    x[0] = N_o
    for n in index_set[1:]:
        x[n] = N_o*np.exp(rho/100*n)
    x=x.tolist()
    return x



class exponentialOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        #text_file = open('.txt','r')
        #x1 = text_file.read()
        N_o = form.getvalue('N_o')
        N_o = float(N_o)
        rho = form.getvalue('rho')
        rho = float(rho)
        T = form.getvalue('T')
        T = int(T)
                
        x_out=exponentialgrow(N_o,rho,T)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'exponential','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'exponential', 
                'model_attributes':'Exponential Model Output'})
        html = html + """<table width="550" border="1" class="out_table">
                          <tr>
                            <th scope="col" width="250">Inputs</th>
                            <th scope="col" width="150">Unit</th>                            
                            <th scope="col" width="150">Value</th>
                          </tr>
                          <tr>
                            <td>Initial amount of individuals</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>                                                  
                          <tr>
                            <td>Initial growth rate</td>
                            <td>&#37;</td>                            
                            <td>%s</td>
                          </tr>                           
                          <tr>
                            <td>Number of time intervals</td>
                            <td>time unit</td>                            
                            <td>%s</td>
                          </tr>                                                                                                                
                        </table>
                        <p>&nbsp;</p>"""%(N_o, rho, T)

        html = html +  """<table width="400" border="0" style="display: none">
                          <tr>
                            <td>X</td>
                            <td id="x_indi_val">%s</td>
                          </tr>
                          </table>"""%((x_out))
        html = html +   """<div id="chart1" style="margin-top:20px; margin-left:20px; width:650px; height:400px;"></div>"""

        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'exponential-output-jqplot.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', exponentialOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
