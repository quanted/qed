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
    

def yulefurrygrow(N_o, T, rho, Ite):
    index_set = range(T+1)        
    x = np.zeros((Ite,len(index_set)))
    x_mu = np.zeros(len(index_set))
    x_mu[0]=N_o
    rho=rho/100

    for i in range(0,Ite):
    #    rho=1-np.exp(-rho)
        x[i][0]=N_o
        n=0

        while n<T:
            x_mu[n+1]=(1+rho)*x_mu[n]
            
            if x[i][n]<10000:
                m=np.random.random(x[i][n]) 
                n_birth=np.sum(m<rho)
                x[i][n+1]=x[i][n]+n_birth
                
            else:
                x[i][n+1]=(1+rho)*x[i][n]
            n=n+1
                
    x=x.tolist()
    x_mu=x_mu.tolist()
   
    
    return x, x_mu

class yulefurryOutputPage(webapp.RequestHandler):
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
        Ite = form.getvalue('Ite')
        Ite = int(Ite)
                              
        x=yulefurrygrow(N_o, T, rho, Ite)[0]
        x_mu=yulefurrygrow(N_o, T, rho, Ite)[1]
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'yulefurry','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'yulefurry', 
                'model_attributes':'Yule-Furry Markov Process Output'})
        html = html + """<table class="out_">
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
                          <tr>
                            <td>Number of iterations</td>
                            <td>&nbsp</td>                            
                            <td id="ita">%s</td>
                          </tr>                                                                                                                                                                                                                  
                        </table>
                        <p>&nbsp;</p>"""%(N_o, rho, T, Ite)

        html = html +  """<table width="400" border="1" style="display: none">
                          <tr>
                            <td>X</td>
                            <td id="x">%s</td>
                          </tr>
                          <tr >
                            <td>x_mu</td>
                            <td id="x_mu">%s</td>
                          </tr>                          
                          </table>"""%(x,x_mu)
        html = html + template.render(templatepath + 'yulefurry-output-jqplot.html', {})                         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', yulefurryOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
