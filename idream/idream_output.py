# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
from idream import idream_model
from idream import idream_tables

class idreamOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        tier = form.getvalue('tier')
        ai_name = form.getvalue('ai_name')
        prod_re = form.getvalue('prod_re')
        ai = form.getvalue('ai')
        ai = float(ai)/100

        liq_rte = form.getvalue('liq_rte')
        liq_rte =float(liq_rte)/100
        fruit_rte = form.getvalue('fruit_rte')
        fruit_rte =float(fruit_rte)/100
        bread_rte = form.getvalue('bread_rte')
        bread_rte =float(bread_rte)/100
        cheese_rte = form.getvalue('cheese_rte')
        cheese_rte =float(cheese_rte)/100
        veg_rte = fruit_rte
        meat_rte = form.getvalue('meat_rte')
        meat_rte =float(meat_rte)/100
        pure_rte = form.getvalue('pure_rte')
        pure_rte =float(pure_rte)/100
        piec_rte = form.getvalue('piec_rte')
        piec_rte =float(piec_rte)/100
        powd_rte = bread_rte

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'idream','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'idream', 
                'model_attributes':'IDREAM Output'})

        if tier == 'Tier 2':
            idream_obj = idream_model.idream(tier, ai_name, prod_re, ai)
        # print idream_obj.__dict__.items()
        else:
            idream_obj = idream_model.idream3(tier, ai_name, prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte)

        html = html + idream_tables.timestamp()
        html = html + idream_tables.table_all(idream_obj)

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', idreamOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    
