# -*- coding: utf-8 -*-

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
sys.path.append("../dust")
from dust import dust_model

class DUSTExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        label_epa_reg_no = form.getvalue('label_epa_reg_no')
        ar_lb = form.getvalue('application_rate')
        frac_pest_surface = form.getvalue('frac_pest_assumed_at_surface')
        dislodge_fol_res = form.getvalue('dislodgeable_foliar_residue')
        bird_acute_oral_study = form.getvalue('bird_acute_oral_study')
        bird_study_add_comm = form.getvalue('bird_study_add_comm')
        low_bird_acute_ld50 = form.getvalue('low_bird_acute_oral_ld50')
        test_bird_bw = form.getvalue('tested_bird_body_weight')
        mamm_acute_derm_study = form.getvalue('mamm_acute_derm_study')
        mamm_study_add_comm = form.getvalue('mamm_study_add_comm')
        mam_acute_derm_ld50 = form.getvalue('mamm_acute_derm_ld50')
        test_mam_bw = form.getvalue('tested_mamm_body_weight')
        mineau = form.getvalue('mineau')
        
#        text_file = open('','r')
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'dust', 
                'model_attributes':'DUST Output'})   
        html = html + """
        <table border="1">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <br></br>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Label EPA Reg. No.</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Maximum Single Application Rate</td>
        <td>%s</td>
        <td>lbs a.i./A</td>
        </tr>
        <tr>
        <td>Fraction of Pesticide Assumed at Surface</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Dislodgeable Foliar Residue</td>
        <td>%s</td>
        <td>mg a.i./cm<sup>2</sup></td>
        </tr>
        </table>
        
        <table border="1">
        <tr><H4>Toxicity Properties</H4></tr>
        <tr>
        <td>Bird Acute Oral Study (OCSPP 850.2100) MRID#</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Additional Comments About the Study (if any)</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub></td>
        <td>%s</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Tested Bird Body Weight</td>
        <td>%s</td>
        <td>g</td>
        </tr>
        <tr>
        <td>Mineau Scaling Factor for Birds</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Mammal Acute Dermal (OCSPP 870.1200) MRID#</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Additional Comments About Study (if any)</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Mammal Acute Drmal LD<sub>50</sub></td>
        <td>%s</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Tested Mammal Body Weight</td>
        <td>%s</td>
        <td>g</td>
        </tr>
        </table>
        <br></br>

        <table border="1">
        <tr><H3>Exposure Estimates</H3></tr>
        <br></br>
        <tr><H4>Granular Application</H4></tr>
        <tr>(contact with soil residues via dust and soil surface)</tr>
        <tr>
        <td>Bird External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Reptile/Amphibian External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Mammal External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        </table>
        
        <table border="1">
        <tr><H4>Foliar Spray Application</H4></tr>
        <tr>(contact with foliar residues and directly applied spray)</tr>
        <tr>
        <td>Bird External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Reptile/Amphibian External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Mammal External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        </table>
        
        <table border="1">
        <tr><H4>Bare Ground Spray Application</H4></tr>
        <tr>(contact with soil residues and directly applied spray)</tr>
        <tr>
        <td>Bird External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Reptile/Amphibian External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        <tr>
        <td>Mammal External Dermal Dose</td>
        <td>%0.2E</td>
        <td>mg a.i./kg-bw</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>Ratio of Exposure to Toxicity</H3></tr>
        <br></br>
        <tr><H4>Granular</H4></tr>
        <tr>
        <td>Bird</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Reptile</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Amphibian</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Mammal</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        </table>
        
        <table border="1">
        <tr><H4>Foliar Spray</H4></tr>
        <tr>
        <td>Bird</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Reptile</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Amphibian</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td> 
        </tr>
        <tr>
        <td>Mammal</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        </table>
        
        <table border="1">
        <tr><H4>Bare Ground Spray</H4></tr>
        <tr>
        <td>Bird</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Reptile</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Amphibian</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        <tr>
        <td>Mammal</td>
        <td>%0.2E</td>
        <td><H5><font color="red">%s</font></H5></td>
        </tr>
        </table>
        
        """ % (chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, 
               dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
               low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study,
               mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw,
               dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface), 
dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),
dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),
dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),
dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),
dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),
dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),
dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),
dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),
dust_model.ratio_gran_bird(dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_gran_bird(dust_model.ratio_gran_bird(dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_gran_rep(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_gran_rep(dust_model.ratio_gran_rep(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_gran_amp(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
dust_model.LOC_gran_amp(dust_model.ratio_gran_amp(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
dust_model.ratio_gran_mam(dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
dust_model.LOC_gran_mam(dust_model.ratio_gran_mam(dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))),
dust_model.ratio_fol_bird(dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_fol_bird(dust_model.ratio_fol_bird(dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_fol_rep(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_fol_rep(dust_model.ratio_fol_rep(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_fol_amp(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
dust_model.LOC_fol_amp(dust_model.ratio_fol_amp(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
dust_model.ratio_fol_mam(dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
dust_model.LOC_fol_mam(dust_model.ratio_fol_mam(dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))),
dust_model.ratio_bgs_bird(dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_bgs_bird(dust_model.ratio_bgs_bird(dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_bgs_rep(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
dust_model.LOC_bgs_rep(dust_model.ratio_bgs_rep(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
dust_model.ratio_bgs_amp(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
dust_model.LOC_bgs_amp(dust_model.ratio_bgs_amp(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
dust_model.ratio_bgs_mam(dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
dust_model.LOC_bgs_mam(dust_model.ratio_bgs_mam(dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)))  )
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', DUSTExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()


    
