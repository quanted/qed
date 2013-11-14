# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import json
from exams import exams_model,exams_tables
from uber import uber_lib
import base64
import urllib
from google.appengine.api import urlfetch
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################               

def get_jid(exams_obj):

    url='https://api.picloud.com/r/3303/exams_s1'

    chem_name = exams_obj.chem_name
    scenarios = exams_obj.scenarios
    met = exams_obj.met
    farm = exams_obj.farm
    mw = exams_obj.mw
    sol = exams_obj.sol
    koc = exams_obj.koc
    vp = exams_obj.vp
    aem = exams_obj.aem
    anm = exams_obj.anm
    aqp = exams_obj.aqp
    tmper = exams_obj.tmper
    n_ph = exams_obj.n_ph
    ph_out = exams_obj.ph_out
    hl_out = exams_obj.hl_out

    input_list=[chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out]
    input_list=json.dumps(input_list)
    data = urllib.urlencode({"input_list":input_list})
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
    jid= json.loads(response.content)['jid']
    output_st = ''
        
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)

class examsOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()   
        chem_name = form.getvalue('chemical_name')
        scenarios =form.getvalue('scenarios')
        farm =form.getvalue('farm_pond')
        mw = form.getvalue('molecular_weight')
        sol = form.getvalue('solubility')
        koc = form.getvalue('Koc')
        vp = form.getvalue('vapor_pressure')
        aem = form.getvalue('aerobic_aquatic_metabolism')
        anm = form.getvalue('anaerobic_aquatic_metabolism')
        aqp = form.getvalue('aquatic_direct_photolysis')
        tmper = form.getvalue('temperature')

        n_ph = float(form.getvalue('n_ph'))
        ph_out = []
        hl_out = []
        for i in range(int(n_ph)):
            j=i+1
            ph_temp = form.getvalue('ph'+str(j))
            ph_out.append(float(ph_temp))
            hl_temp = float(form.getvalue('hl'+str(j)))
            hl_out.append(hl_temp)  

        exams_obj = exams_model.exams(chem_name, scenarios, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)

        final_res=get_jid(exams_obj)
        exams_obj.link = final_res[2]
        # print exams_obj.__dict__.items()
        # print final_res
        # print final_res[2]

        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'exams','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'exams', 
                'model_attributes':'EXAMS Output'})
        html = html + exams_tables.table_all(exams_obj)

        html = html + """
        <br><div><table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">EXAMS Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
        </table><br></div>"""%(exams_obj.link)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', examsOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
