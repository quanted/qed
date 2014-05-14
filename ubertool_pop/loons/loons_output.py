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
from loons import loons_model
from loons import loons_tables


class loons_OutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        b = form.getvalue('b')
        m = form.getvalue('m')
        r = form.getvalue('r')
        pa = form.getvalue('pa')
        sj = form.getvalue('sj')
        t = form.getvalue('t')

        no1 = form.getvalue('no1')
        no2 = form.getvalue('no2')
        no3 = form.getvalue('no3')
        no4 = form.getvalue('no4')
        n_o =[no1, no2, no3, no4]
        n_o = np.asarray(n_o)

        loons_obj = loons_model.loons(b, m, r, pa, sj, t, no1, no2, no3, no4)
        # print loons_obj.b[4]

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'loons','page':'output'})
        html = html + template.render(templatepath + '03pop_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'loons', 
                'model_attributes':'Loons Population Model'})

        html = html + loons_tables.table_all(loons_obj) # 

        html = html +  """<table width="400" border="1" style="display:none">
                          <tr>
                            <td>number of class</td>
                            <td id="n_o_c">4</td>
                          </tr>
                          <tr>
                            <td>final population</td>
                            <td id="final">%s</td>
                          </tr>                          
                          </table>"""%(loons_obj.leslie_out)
        html = html + template.render(templatepath + 'loons_jqplot.html', {})                         

        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)
     
app = webapp.WSGIApplication([('/.*', loons_OutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()





































