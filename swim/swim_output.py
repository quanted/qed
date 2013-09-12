# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from swim import swim_model
from swim import swim_tables


class swimOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        chemical_name = form.getvalue('chemical_name')
        log_kow = float(form.getvalue('log_kow'))
        mw = float(form.getvalue('mw'))
        hlc = float(form.getvalue('hlc'))
        r = float(form.getvalue('r'))
        T = float(form.getvalue('T'))
        cw = float(form.getvalue('cw'))
        noael = float(form.getvalue('noael'))

        bw_aa = float(form.getvalue('bw_aa'))
        bw_fa = float(form.getvalue('bw_fa'))
        sa_a_c = float(form.getvalue('sa_a_c'))
        sa_a_nc = float(form.getvalue('sa_a_nc'))
        et_a_c = float(form.getvalue('et_a_c'))
        et_a_nc = float(form.getvalue('et_a_nc'))
        ir_a_c = float(form.getvalue('ir_a_c'))
        ir_a_nc = float(form.getvalue('ir_a_nc'))
        igr_a_c = float(form.getvalue('igr_a_c'))
        igr_a_nc = float(form.getvalue('igr_a_nc'))

        bw_c1 = float(form.getvalue('bw_c1'))
        sa_c1_c = float(form.getvalue('sa_c1_c'))
        sa_c1_nc = float(form.getvalue('sa_c1_nc'))
        et_c1_c = float(form.getvalue('et_c1_c'))
        et_c1_nc = float(form.getvalue('et_c1_nc'))
        ir_c1_c = float(form.getvalue('ir_c1_c'))
        ir_c1_nc = float(form.getvalue('ir_c1_nc'))
        igr_c1_c = float(form.getvalue('igr_c1_c'))
        igr_c1_nc = float(form.getvalue('igr_c1_nc'))

        bw_c2 = float(form.getvalue('bw_c2'))
        sa_c2_c = float(form.getvalue('sa_c2_c'))
        sa_c2_nc = float(form.getvalue('sa_c2_nc'))
        et_c2_c = float(form.getvalue('et_c2_c'))
        et_c2_nc = float(form.getvalue('et_c2_nc'))
        ir_c2_c = float(form.getvalue('ir_c2_c'))
        ir_c2_nc = float(form.getvalue('ir_c2_nc'))
        igr_c2_c = float(form.getvalue('igr_c2_c'))
        igr_c2_nc = float(form.getvalue('igr_c2_nc'))

        swim_obj = swim_model.swim(chemical_name, log_kow, mw, hlc, r, T, cw, noael, 
                                     bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc, 
                                     bw_c1, sa_c1_c, sa_c1_nc, et_c1_c, et_c1_nc, ir_c1_c, ir_c1_nc, igr_c1_c, igr_c1_nc, 
                                     bw_c2, sa_c2_c, sa_c2_nc, et_c2_c, et_c2_nc, ir_c2_c, ir_c2_nc, igr_c2_c, igr_c2_nc)

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'swim','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'swim', 
                'model_attributes':'SWIM Output'})

        html = html + swim_tables.timestamp()
        html = html + swim_tables.table_all(swim_obj)

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', swimOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    