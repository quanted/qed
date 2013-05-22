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
    

def lesliegrow(n_o, T, l_m,S):
    n_f=np.zeros(shape=(S,T))
    for i in range(0, T):
        n=np.dot(l_m, n_o)
        n_o=n
        n_f[:,i]=n.squeeze()
    return n_f.tolist()

class leslieOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        #text_file = open('.txt','r')
        #x1 = text_file.read()

        T = form.getvalue('T')
        T = int(T)
        S = form.getvalue('S')
        S = int(S)

        l_m = np.zeros(shape=(S,S))
        n_o = np.zeros(shape=(S,1))
        
        for i in range(S):
            n_o_temp = form.getvalue('no'+str(i))
            n_o[i,] = n_o_temp            
            for j in range(S):        
                l_m_temp = form.getvalue('a'+str(i)+str(j))
                l_m[i,j] = l_m_temp

        x=lesliegrow(n_o, T, l_m,S)
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'leslie','page':'output'})
        html = html + template.render(templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'leslie', 
                'model_attributes':'Leslie Matrix Outputs'})
        html = html + """<table class="out-in out_" width="550" border="1">
                          <tr>
                            <th scope="col" width="250"><div align="center">Inputs</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                                                
                          <tr>
                            <td><div align="center">Simulation duration</div></td>
                            <td><div align="center">time unit</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Modeled stages</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td id="MS"><div align="center">%s</div></td>
                          </tr>
                          <tr style="display:none">
                            <td><div align="center">Leslie Matrix</div></td>
                            <td><div align="center">&nbsp</div></td>
                            <td id="LM"><div align="center">%s</div></td>
                          </tr>
                          <tr style="display:none">
                            <td><div align="center">Initial numbers</div></td>
                            <td><div align="center">&nbsp</div></td>
                            <td id="IN"><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                              
                        </table>
                        <p>&nbsp;</p>"""%(T, S, l_m.tolist(), n_o.tolist())
                        
        html = html + """<table class="lm out_" border="1">"""
                                            
        html = html + """<table class="ii out_" border="1">"""
                                             

        html = html +  """<table width="400" border="1" style="display: none">
                          <tr>
                            <td>X</td>
                            <td id="final">%s</td>
                          </tr>
                       
                          </table>"""%(x)
        html = html + template.render(templatepath + 'leslie-output-jqplot.html', {})                         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', leslieOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
