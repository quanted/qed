# TerrPlant Version 1.2.2


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils
sys.path.append("../terrplant")
from terrplant import terrplant_model

class TerrPlantExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        pc_code = form.getvalue('pc_code')
        use = form.getvalue('use')
        application_method = form.getvalue('application_method')
        application_form = form.getvalue('application_form')
        solubility = form.getvalue('solubility')
        I = form.getvalue('incorporation')
        A = form.getvalue('application_rate')
        D = form.getvalue('drift_fraction')
        R = form.getvalue('runoff_fraction')
        nms = form.getvalue('EC25_for_nonlisted_seedling_emergence_monocot')
        nds = form.getvalue('EC25_for_nonlisted_seedling_emergence_dicot')
        lms = form.getvalue('NOAEC_for_listed_seedling_emergence_monocot')
        lds = form.getvalue('NOAEC_for_listed_seedling_emergence_dicot')
        nmv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_monocot')
        ndv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_dicot')
        lmv = form.getvalue('NOAEC_for_listed_vegetative_vigor_monocot')
        ldv = form.getvalue('NOAEC_for_listed_vegetative_vigor_dicot')
        text_file = open('terrplant/terrplant_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html',{'model':'terrplant', 'model_attributes':'TerrPlant Output'})   
        html = html + """
        <table border="1">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>PC Code</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Use</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Method</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Form</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Solubility in Water (ppm)</td>
        <td>%s</td>
        <tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>User Inputs: Input Parameters Used to Derive EECs</H3></tr><br>
        <tr>
        <td>Incorporation</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Rate</td>
        <td>%s</td>
        <td>lbs ai/A</td>
        </tr>
        <tr>
        <td>Drift Fraction</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Runoff Fraction</td>
        <td>%s</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>EECs - Units in (lbs a.i./A)</H3></tr><br>
        <tr>
        <th colspan="1">Description</th>
        <th colspan="1">EEC</th>
        </tr>
        <tr>
        <td>Runoff to Dry Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Runoff to Semi-Aquatic Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Spray Drift</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Total for Dry Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Total for Semi-Aquatic Areas</td>
        <td>%0.2E</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>User Inputs: Plant Survival and Growth Data Used for RQ Derivation - Units in (lbs a.i./A)</H3></tr><br>
        <tr><th> </th>
        <th colspan="2">Seedling Emergence</th>
        <th colspan="2">Vegetative Vigor</th>
        </tr>
        <tr><td>Plant Type</td>
        <td>EC<sub>25</sub></td>
        <td>NOAEC</td>
        <td>EC<sub>25</sub></td>
        <td>NOAEC</td>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>RQ Values for Plants in Dry and Semi-aquatic Areas Exposed to Through Runoff and/or Spray Drift *</H3></tr>
        <tr>
        <th colspan="1">Plant Type</th>
        <th colspan="1">Listed Status</th>
        <th colspan="1">Dry</th>
        <th colspan="1">Semi-Aquatic</th>
        <th colspan="1">Spray Drift</th>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>non-listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>non-listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        </table>
        <H4>* If RQ > 1.0, the Level of Concern is exceeded, resulting in potential risk to that plant group.</H4>
        """ % (chemical_name, pc_code, use, application_method, application_form, solubility,
               I, A, D, R, 
               terrplant_model.rundry(A,I,R), terrplant_model.runsemi(A,I,R), terrplant_model.spray(A,D), terrplant_model.totaldry(terrplant_model.rundry(A,I,R), terrplant_model.spray(A,D)), terrplant_model.totalsemi(terrplant_model.runsemi(A,I,R),terrplant_model.spray(A,D)),
               nms, lms, nmv, lmv, nds, lds, ndv, ldv,
               terrplant_model.nmsRQdry(terrplant_model.totaldry(terrplant_model.rundry(A,I,R),terrplant_model.spray(A,D)),nms), 
terrplant_model.nmsRQsemi(terrplant_model.totalsemi(terrplant_model.runsemi(A,I,R),terrplant_model.spray(A,D)),nms), 
terrplant_model.nmsRQspray(terrplant_model.spray(A,D),nms), 
terrplant_model.lmsRQdry(terrplant_model.totaldry(terrplant_model.rundry(A,I,R),terrplant_model.spray(A,D)),lms), 
terrplant_model.lmsRQsemi(terrplant_model.totalsemi(terrplant_model.runsemi(A,I,R),terrplant_model.spray(A,D)),lms), 
terrplant_model.lmsRQspray(terrplant_model.spray(A,D),lms),
terrplant_model.ndsRQdry(terrplant_model.totaldry(terrplant_model.rundry(A,I,R),terrplant_model.spray(A,D)),nds), 
terrplant_model.ndsRQsemi(terrplant_model.totalsemi(terrplant_model.runsemi(A,I,R),terrplant_model.spray(A,D)),nds), 
terrplant_model.ndsRQspray(terrplant_model.spray(A,D),nds), 
terrplant_model.ldsRQdry(terrplant_model.totaldry(terrplant_model.rundry(A,I,R),terrplant_model.spray(A,D)),lds), 
terrplant_model.ldsRQsemi(terrplant_model.totalsemi(terrplant_model.runsemi(A,I,R),terrplant_model.spray(A,D)),lds), 
terrplant_model.ldsRQspray(terrplant_model.spray(A,D),lds)
)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
