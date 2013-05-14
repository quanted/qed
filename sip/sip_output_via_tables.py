# Screening Imbibiton Program v1.0 (SIP)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import sys
sys.path.append("../sip")
from sip import sip_model

class SIPExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        select_receptor = form.getvalue('select_receptor')
        bw_bird = form.getvalue('body_weight_of_bird')
        bw_mamm = form.getvalue('body_weight_of_mammal')
        sol = form.getvalue('solubility')
        ld50 = form.getvalue('ld50')
        aw_bird = form.getvalue('body_weight_of_the_assessed_bird')
        tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        aw_mamm = form.getvalue('body_weight_of_the_assessed_mammal')
        tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        mineau = form.getvalue('mineau_scaling_factor')
        noaec = form.getvalue('NOAEC')
        noael = form.getvalue('NOAEL')
            
        text_file = open('sip/sip_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'sip','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'sip', 
                'model_attributes':'SIP Output'})           
        html = html + """


        <table border="1" class="out_1">
        <tr>
            <th>User Inputs</th>
            <th>Values</th>
            <th>Units</th>
        </tr>
        <tr>
            <td>Chemical Name</td>
            <td>%s</td>
            <td></td>
        </tr>
        <tr>
            <td>Receptor Selected</td>
            <td>%s</td>
            <td></td>
        </tr>
        <tr>
            <td>Body Weight of Bird</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Body Weight of Mammal</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Solubility</td>
            <td>%s</td>
            <td>mg/L</td>
        </tr>
        <tr>
            <td>LD<sub>50</sub></td>
            <td>%s</td>
            <td>mg/kg</td>
        </tr>
        <tr>
            <td>Body Weight of Assessed Bird</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Body Weight of Tested Bird</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Body Weight of Assessed Mammal</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Body Weight of Tested Mammal</td>
            <td>%s</td>
            <td>kg</td>
        </tr>
        <tr>
            <td>Mineau Scaling Factor</td>
            <td>%s</td>
            <td></td>
        </tr>
        <tr>
            <td>NOAEC</td>
            <td>%s</td>
            <td>mg/kg</td>
        </tr>
        <tr>
            <td>NOAEL</td>
            <td>%s</td>
            <td>mg/kg</td>
        </tr>
        </table>
		<br>
        """ % (chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)

        html = html + """
        <table border="1" class="out_2">
        <tr>
            <th>SIP Outputs</th>
            <th>Mammalian Results (%s kg)</th>
            <th></th>
        </tr>
        <tr>
            <td>Parameter</td>
            <td>Acute</td>
            <td>Chronic</td>
        </tr>
        <tr>
            <td>Upper Bound Exposure</td>
            <td>%0.2E mg/kg-bw</td>
            <td>%0.2E mg/kg-bw</td>
        </tr>
        <tr>
            <td>Adjusted Toxicity Value</td>
            <td>%0.2E mg/kg-bw</td>
            <td>%0.2E mg/kg-bw</td>
        </tr>
        <tr>
            <td>Ratio of Exposure to Toxicity</td>
            <td>%0.2E</td>
            <td>%0.2E</td>
        </tr>
        <tr>
            <td>Conclusion</td>
            <td><font color="red">%s</font></td>
            <td><font color="red">%s</font></td>
        </tr>
        </table><br>
        
        <table border="1" class="out_3">
        <tr>
            <th>SIP Outputs</th>
            <th>>Avian Results (%s kg)</th>
            <th></th>
        </tr>
        <tr>
            <td>Parameter</td>
            <td>Acute</td>
            <td>Chronic</td>
        </tr>
        <tr>
            <td>Upper Bound Exposure</td>
            <td>%0.2E mg/kg-bw</td>
            <td>%0.2E mg/kg-bw</td>
        </tr>
        <tr>
            <td>Adjusted Toxicity Value</td>
            <td>%0.2E mg/kg-bw</td>
            <td>%0.2E mg/kg-bw</td>
        </tr>
        <tr>
            <td>Ratio of Exposure to Toxicity</td>
            <td>%0.2E</td>
            <td>%0.2E</td>
        </tr>
        <tr>
            <td>Conclusion</td>
            <td><font color="red">%s</font></td>
            <td><font color="red">%s</font></td>
        </tr>
        </table>
        """  % (aw_mamm,
                sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),
                sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),
                sip_model.at_mamm(ld50,aw_mamm,tw_mamm),
                sip_model.act(noael,tw_mamm,aw_mamm),
                sip_model.acute_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.at_mamm(ld50,aw_mamm,tw_mamm)),
                sip_model.chron_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.act(noael,tw_mamm,aw_mamm)),
                sip_model.acuconm(sip_model.acute_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.at_mamm(ld50,aw_mamm,tw_mamm))),
                sip_model.chronconm(sip_model.chron_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.act(noael,tw_mamm,aw_mamm))),
                aw_bird,
                sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird), 
                sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird), 
                sip_model.at_bird(ld50,aw_bird,tw_bird,mineau),
                sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird),
                sip_model.acute_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.at_bird(ld50,aw_bird,tw_bird,mineau)),
                sip_model.chron_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird)),
                sip_model.acuconb(sip_model.acute_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.at_bird(ld50,aw_bird,tw_bird,mineau))),             
                sip_model.chronconb(sip_model.chron_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird))))             
        
        html = html + """
         #pre-table 1
        <table>
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """
        pvuheadings = sip_tables.getheaderpvu()
        pvrheadings = sip_tables.getheaderpvr()
        djtemplate = sip_tables.getdjtemplate()
        tmpl = Template(djtemplate)

        #table 1
        t1data = sip_tables.gett1data(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)
        t1rows = sip_tables.gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
         #pre-table 2
        <table>
        <tr><H3>Outputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """
        #table 2
        t2data = sip_tables.gett2data(aw_bird, bw_bird, sol, ld50, tw_bird, mineau, noaec)
        t2rows = sip_tables.gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', SIPExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

    
    