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
    
#def maxsusgrow(N_o,K,rho,T):
#    index_set = range(T+1)
#    x = np.zeros(len(index_set))
#    x[0] = N_o
#    rho=rho/100
#    H=K*rho/4
#    for n in index_set[1:]:
#        x[n] = K/2-1/(4*(1/(2*K-4*N_o)-(rho*n/(4*K))))
#    x=x.tolist()
#    return H, x

def dmaxsusgrow(K,rho):
    index_set = range(K+1)
    x = np.zeros((len(index_set),2))  
    rho=rho/100
    H=rho*K/4
    for n in range(1,K+1):
        x[n][0] = n
        x[n][1] = rho*n*(1-float(n)/K)
    x=x.tolist()
    
    return H, x

class maxsusOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        #text_file = open('.txt','r')
        #x1 = text_file.read()
#        N_o = form.getvalue('N_o')
#        N_o = float(N_o)
        K = form.getvalue('K')
        K = int(K)
        rho = form.getvalue('rho')
        rho = float(rho)
#        T = form.getvalue('T')
#        T = int(T)
                       
        H=dmaxsusgrow(K,rho)[0]
        x_out=dmaxsusgrow(K,rho)[1]
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'maxsus','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'maxsus', 
                'model_attributes':'Maximum Sustainable Yield Model Output'})
        html = html + """<table class="out_">
                          <tr>
                            <th scope="col" width="250">Inputs</th>
                            <th scope="col" width="150">Unit</th>                            
                            <th scope="col" width="150">Value</th>
                          </tr>                       
                          <tr>
                            <td>Carrying capacity</td>
                            <td>&nbsp</td>                            
                            <td>%s</td>
                          </tr>                          
                          <tr>
                            <td>Initial growth rate</td>
                            <td>&#37;</td>                            
                            <td>%s</td>
                          </tr>                                                                                                                                                               
                        </table>
                        <p>&nbsp;</p>"""%(K, rho)

        html = html +  """<table width="400" border="1" style="display: none">
                          <tr >
                            <td>X</td>
                            <td id="x_out_val">%s</td>
                          </tr>
                          <tr >
                            <td>H</td>
                            <td id="H_val">%s</td>
                          </tr>                          
                          </table>"""%(x_out,H)
        html = html + template.render(templatepath + 'maxsus-output-jqplot.html', {})                         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', maxsusOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
