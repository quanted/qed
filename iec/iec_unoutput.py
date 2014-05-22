# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../iec")
from iec import iec_model,iec_tables
from uber import uber_lib
from django.template import Context, Template
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import StringIO
import urllib, base64
import string
import random

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

def hist_plot(data, num_bin, title, i, k):
    plt.figure(i)
    plt.hist(data, bins=num_bin)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    fig = plt.gcf()

    imgdata = StringIO.StringIO()
    fig.savefig(imgdata, format='png', transparent=True)
    imgdata.seek(0)  # rewind the data
    uri_1 = 'data:image/png;base64,' + (base64.b64encode(imgdata.buf))
    uri_2 = '<img id="chart%s" src = "%s"/>' % (k, uri_1)
    return uri_2

class iecUnoutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        NOI = int(form.getvalue('NOI'))
        LC50 = form.getvalue('LC50')
        if LC50=="Uniform":
            LC50_lower=float(form.getvalue('LC50_lower'))
            LC50_upper=float(form.getvalue('LC50_upper'))
            LC50_pool=np.random.uniform(LC50_lower, LC50_upper, NOI)
        elif LC50=="Normal":
            LC50_mean=float(form.getvalue('LC50_mean'))
            LC50_std=float(form.getvalue('LC50_std'))
            LC50_pool=np.random.normal(LC50_mean, LC50_std, NOI)
        elif LC50=="Log-normal":
            LC50_mean=float(form.getvalue('LC50_mean'))
            LC50_std=float(form.getvalue('LC50_std'))
            LC50_pool=np.random.lognormal(LC50_mean, LC50_std, NOI)

        threshold = form.getvalue('threshold')
        if threshold=="Uniform":
            threshold_lower=float(form.getvalue('threshold_lower'))
            threshold_upper=float(form.getvalue('threshold_upper'))
            threshold_pool=np.random.uniform(threshold_lower, threshold_upper, NOI)
        elif threshold=="Normal":
            threshold_mean=float(form.getvalue('threshold_mean'))
            threshold_std=float(form.getvalue('threshold_std'))
            threshold_pool=np.random.normal(threshold_mean, threshold_std, NOI)
        elif threshold=="Log-normal":
            threshold_mean=float(form.getvalue('threshold_mean'))
            threshold_std=float(form.getvalue('threshold_std'))
            threshold_pool=np.random.lognormal(threshold_mean, threshold_std, NOI)

        dose_response = form.getvalue('dose_response')
        if dose_response=="Uniform":
            dose_response_lower=float(form.getvalue('dose_response_lower'))
            dose_response_upper=float(form.getvalue('dose_response_upper'))
            dose_response_pool=np.random.uniform(dose_response_lower, dose_response_upper, NOI)
        elif dose_response=="Normal":
            dose_response_mean=float(form.getvalue('dose_response_mean'))
            dose_response_std=float(form.getvalue('dose_response_std'))
            dose_response_pool=np.random.normal(dose_response_mean, dose_response_std, NOI)
        elif dose_response=="Log-normal":
            dose_response_mean=float(form.getvalue('dose_response_mean'))
            dose_response_std=float(form.getvalue('dose_response_std'))
            dose_response_pool=np.random.lognormal(dose_response_mean, dose_response_std, NOI)

        z_score_f_pool=[]
        F8_f_pool=[]
        chance_f_pool=[]

        for i in range(NOI):
            iec_obj_temp = iec_model.iec(True, True, dose_response_pool[i], LC50_pool[i], threshold_pool[i])
            z_score_f_pool.append(iec_obj_temp.z_score_f_out)
            F8_f_pool.append(iec_obj_temp.F8_f_out)
            chance_f_pool.append(iec_obj_temp.chance_f_out)


        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "IEC Uncertainty Output")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'iec','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'iec', 
                'model_attributes':'IEC Uncertainty Output'})
        html = html + iec_tables.timestamp()
        html = html + iec_tables.table_all_un(LC50_pool, threshold_pool, dose_response_pool, z_score_f_pool, F8_f_pool, chance_f_pool)

        num_bin_z_score = int(1+3.3*np.log10(len(z_score_f_pool)))
        num_bin_chance_f = int(1+3.3*np.log10(len(chance_f_pool)))

        html = html + '<div>'
        html = html + hist_plot(z_score_f_pool, num_bin_z_score, 'Z Score', id_generator(), 1) + '<br>'
        html = html + hist_plot(chance_f_pool, num_bin_chance_f, 'Chance F', id_generator(), 2) + '<br>'
        html = html + '</div>'

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {}) 
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', iecUnoutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

     
