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
from leslie_probit import leslie_probit_model
from leslie_probit import leslie_probit_tables


class leslie_probit_OutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        a_n = form.getvalue('animal_name')
        c_n = form.getvalue('chemical_name')
        app_target = form.getvalue('app_target')
        ai = form.getvalue('ai')
        hl = form.getvalue('hl')
        sol = form.getvalue('sol')
        t = form.getvalue('t')
        n_a = float(form.getvalue('noa'))

        rate_out = []
        day_out = []
        for i in range(int(n_a)):
           j=i+1
           rate_temp = form.getvalue('rate'+str(j))
           rate_out.append(float(rate_temp))
           day_temp = float(form.getvalue('day'+str(j)))
           day_out.append(day_temp)  

        b = form.getvalue('b')
        test_species = form.getvalue('test_species')
        ld50_test = form.getvalue('ld50_test')
        bw_test = form.getvalue('bw_test')
        ass_species = form.getvalue('ass_species')
        bw_ass = form.getvalue('bw_ass')
        x = form.getvalue('mineau_scaling_factor')

        c = form.getvalue('c')
        s = form.getvalue('s')
        s = int(s)

        l_m = np.zeros(shape=(s,s))
        n_o = np.zeros(shape=(s,1))
        
        for i in range(s):
            n_o_temp = form.getvalue('no'+str(i))
            if float(n_o_temp)<=0:
                n_o_temp=0.0000000001
            n_o[i,] = float(n_o_temp)            
            for j in range(s):        
                l_m_temp = form.getvalue('aa'+str(i)+str(j))
                if float(l_m_temp)<=0:
                    l_m_temp=0.00000000001
                l_m[i,j] = float(l_m_temp)

        # x=lesliedrgrow(S, l_m, n_o, T, HL, Con, a, b, c)
        # x=x.tolist()
        # x_f=copy.deepcopy(x)
        
        # for m in range(0,S):
        #     for n in range(0,T+1):
        #         x[m][n]=format(x[m][n],'3.2E')

        leslie_probit_obj = leslie_probit_model.leslie_probit(a_n, c_n, app_target, ai, hl, sol, t, n_a, rate_out, day_out, b, test_species, ld50_test, bw_test, ass_species, bw_ass, x, c, s, l_m, n_o)      
        # print leslie_probit_obj.b[4]

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'leslie_probit','page':'output'})
        html = html + template.render(templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'leslie_probit', 
                'model_attributes':'Leslie Model with Logistic Dose Response Output'})

        html = html + leslie_probit_tables.table_all(leslie_probit_obj)

        html = html +  """<table width="400" border="1" style="display:none">
                          <tr>
                            <td>number of class</td>
                            <td id="n_o_c">%s</td>
                          </tr>
                          <tr>
                            <td>final population</td>
                            <td id="final">%s</td>
                          </tr>                          
                          <tr>
                            <td>final population no impact</td>
                            <td id="final_no">%s</td>
                          </tr>                          
                          <tr>
                            <td>concentrations</td>
                            <td id="conc">%s</td>
                          </tr>                          
                          </table>"""%(leslie_probit_obj.s, leslie_probit_obj.out[4], leslie_probit_obj.out_no, leslie_probit_obj.conc_out)
        html = html + template.render(templatepath + 'lesliedr_probit_jqplot.html', {})                         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', leslie_probit_OutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()





































