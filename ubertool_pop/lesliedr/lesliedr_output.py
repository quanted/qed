# -*- coding: utf-8 -*-


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
import copy
cgitb.enable()
    
def lesliedrgrow(S, l_m, n_o, T, HL, Con, a, b, c):
    n_f=np.zeros(shape=(S,T+1), dtype=float)
    l_m_temp=np.zeros(shape=(S,S), dtype=float)
    n_csum=np.sum(n_o)
    n_e = S*['0']
    n_f[:,0]=n_o.squeeze()
    
    for i in range(1, T+1):
        for j in range(0,S):
            l_m_temp[0,j]=l_m[0,j]*np.exp(-c*n_csum)
            if j-1>=0:
                l_m_temp[j,j-1]=l_m[j,j-1]*(1-1/(1+np.exp(-a*np.log(float(Con)*(0.5)**(i/HL))-b)))
        n=np.dot(l_m_temp, n_o)
        n_csum=np.sum(n)
        n_o=n
        n_f[:,i]=n.squeeze()
    return n_f

def lesliegrow(S, l_m, n_o, T):
    n_f=np.zeros(shape=(S,T+1), dtype=float)
    n_f[:,0]=n_o.squeeze()
    for i in range(1, T+1):
        n=np.dot(l_m, n_o)
        n_o=n
        n_f[:,i]=n.squeeze()
    return n_f

class lesliedrOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        a_n = form.getvalue('animal_name')
        c_n = form.getvalue('chemical_name')
        HL = form.getvalue('HL')
        HL = float(HL)
        Con = form.getvalue('C')
        Con = float(Con)        
        T = form.getvalue('T')
        T = int(T)
        a = form.getvalue('a')
        a = float(a)
        b = form.getvalue('b')
        b = float(b)
        c = form.getvalue('c')
        c = float(c)
        S = form.getvalue('S')
        S = int(S)

        l_m = np.zeros(shape=(S,S))
        n_o = np.zeros(shape=(S,1))
        
        for i in range(S):
            n_o_temp = form.getvalue('no'+str(i))
            if float(n_o_temp)<=0:
                n_o_temp=0.000001
            n_o[i,] = n_o_temp            
            for j in range(S):        
                l_m_temp = form.getvalue('aa'+str(i)+str(j))
                l_m[i,j] = l_m_temp

        x=lesliedrgrow(S, l_m, n_o, T, HL, Con, a, b, c)
        x=x.tolist()
        x_f=copy.deepcopy(x)
        

        x_no=lesliegrow(S, l_m, n_o, T)
        x_no=x_no.tolist()
        x_no_f=copy.deepcopy(x_no)


        for m in range(0,S):
            for n in range(0,T+1):
                x[m][n]=format(x[m][n],'3.2E')
        
      
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'lesliedr','page':'output'})
        html = html + template.render(templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'lesliedr', 
                'model_attributes':'Leslie Model with Logistic Dose Response Output'})
        html = html + """<table class="out-in out_" width="550" border="1">
                          <tr>
                            <th scope="col" width="250"><div align="center">Inputs</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>
                          <tr>
                            <td><div align="center">Animal name</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Chemical name</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Chemical half life</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Initial concentration</div></td>
                            <td><div align="center">&#956;g/l</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                         
                          <tr>
                            <td><div align="center">Simulation duration</div></td>
                            <td><div align="center">time unit</div></td>                            
                            <td id="sd"><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Logistic model parameter (&#945;)</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Logistic model parameter (&#946;)</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Intensity of the density dependence (&#947;)</div></td>
                            <td><div align="center">&nbsp</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                    
                          <tr>
                            <td><div align="center">Number of age class</div></td>
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
                        <p>&nbsp;</p>"""%(a_n, c_n, HL, Con, T, a, b, c, S, l_m.tolist(), n_o.tolist())
                        
        html = html + """<table class="lm out_" border="1">"""
                                                                                        
        html = html + """<table class="it out_" border="1">"""

        html = html +  """<table width="400" border="1" style="display:none">
                          <tr>
                            <td>X</td>
                            <td id="final">%s</td>
                          </tr>
                          <tr>
                            <td>X_f</td>
                            <td id="final_f">%s</td>
                          </tr>                          
                          <tr>
                            <td>X_f_no</td>
                            <td id="final_f_no">%s</td>
                          </tr>                          
                          </table>"""%(x, x_f, x_no_f)
        html = html + template.render(templatepath + 'lesliedr-output-jqplot.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', lesliedrOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()





































