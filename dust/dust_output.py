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
from dust import dust_tables
from django.template import Context, Template

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
        
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'dust', 
                'model_attributes':'DUST Output'})   

        #pre-table 1
        html = html + """
        <table>
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """

        pvuheadings = dust_tables.getheaderpvu()
        pvrheadings = dust_tables.getheaderpvr()
        djtemplate = dust_tables.getdjtemplate()
        tmpl = Template(djtemplate)

        #table 1
        t1data = dust_tables.gett1data(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res)
        t1rows = dust_tables.gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))

        #pre-table 2
        html = html + """
        <table>
        <tr><H4>Toxicity Properties</H4></tr>
        <tr></tr>
        </table>
        """

        #table 2
        t2data = dust_tables.gett2data(bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, 
            mamm_acute_derm_study,mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw)
        t2rows = dust_tables.gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        
        #pre-table 3
        html = html + """
        <table>
        <tr><H3>Exposure Estimates</H3></tr>
        <tr><H4>Granular Application</H4></tr>
        <tr>(contact with soil residues via dust and soil surface)</tr>
        </table>
        """

        #table 3
        granbirdderm = dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        granherpderm = dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface) 
        granmammderm = dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        t3data = dust_tables.gett3data(granbirdderm,granherpderm,granmammderm)
        t3rows = dust_tables.gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))

        #pre-table 4
        html = html + """     
        <table>
        <tr><H4>Foliar Spray Application</H4></tr>
        <tr>(contact with foliar residues and directly applied spray)</tr>
        </table>
        """

        #table 4
        folbirdderm = dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        folherpderm = dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        folmammderm = dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        t4data = dust_tables.gett4data(folbirdderm,folherpderm,folmammderm)
        t4rows = dust_tables.gethtmlrowsfromcols(t4data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))

        #pre-table 5
        html = html + """         
        <table>
        <tr><H4>Bare Ground Spray Application</H4></tr>
        <tr>(contact with soil residues and directly applied spray)</tr>
        </table>
        """

        #table 5
        barebirdderm = dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        bareherpderm = dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        baremammderm = dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        t5data = dust_tables.gett5data(barebirdderm,bareherpderm,baremammderm)
        t5rows = dust_tables.gethtmlrowsfromcols(t5data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pvuheadings)))

        #pre-table 6
        html = html + """        
        <table>
        <tr><H3>Ratio of Exposure to Toxicity</H3></tr>
        <tr><H4>Granular</H4></tr>
        </table>
        """

        #table 6
        granbirdrisk = dust_model.ratio_gran_bird(dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        granbirdmess = dust_model.LOC_gran_bird(dust_model.ratio_gran_bird(dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        granreprisk = dust_model.ratio_gran_rep(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        granrepmess = dust_model.LOC_gran_rep(dust_model.ratio_gran_rep(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        granamphibrisk = dust_model.ratio_gran_amp(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))
        granamphibmess = dust_model.LOC_gran_amp(dust_model.ratio_gran_amp(dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)))
        granmammrisk = dust_model.ratio_gran_mam(dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))
        granmammmess = dust_model.LOC_gran_mam(dust_model.ratio_gran_mam(dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)))
        t6data = dust_tables.gett6data(granbirdrisk,granbirdmess,granreprisk,granrepmess,granamphibrisk,granamphibmess,granmammrisk,granmammmess)
        t6rows = dust_tables.gethtmlrowsfromcols(t6data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t6rows, headings=pvrheadings)))

        #pre-table 7
        html = html + """         
        <table>
        <tr><H4>Foliar Spray</H4></tr>
        </table>
        """

        #table 7
        folbirdrisk = dust_model.ratio_fol_bird(dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        folbirdmess = dust_model.LOC_fol_bird(dust_model.ratio_fol_bird(dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        folreprisk = dust_model.ratio_fol_rep(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        folrepmess = dust_model.LOC_fol_rep(dust_model.ratio_fol_rep(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        folamphibrisk = dust_model.ratio_fol_amp(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))
        folamphibmess = dust_model.LOC_fol_amp(dust_model.ratio_fol_amp(dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)))
        folmammrisk = dust_model.ratio_fol_mam(dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))
        folmammmess = dust_model.LOC_fol_mam(dust_model.ratio_fol_mam(dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb)),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)))
        t7data = dust_tables.gett7data(folbirdrisk,folbirdmess,folreprisk,folrepmess,folamphibrisk,folamphibmess,folmammrisk,folmammmess)
        t7rows = dust_tables.gethtmlrowsfromcols(t7data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=pvrheadings)))

        #pre-table 8
        html = html + """          
        <table>
        <tr><H4>Bare Ground Spray</H4></tr>
        </table>
        """

        #table 8
        barebirdrisk = dust_model.ratio_bgs_bird(dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        barebirdmess = dust_model.LOC_bgs_bird(dust_model.ratio_bgs_bird(dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        barereprisk = dust_model.ratio_bgs_rep(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))
        barerepmess = dust_model.LOC_bgs_rep(dust_model.ratio_bgs_rep(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.birdrep_derm_ld50(dust_model.bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)))
        bareamphibrisk = dust_model.ratio_bgs_amp(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))
        bareamphibmess = dust_model.LOC_bgs_amp(dust_model.ratio_bgs_amp(dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)))
        baremammrisk = dust_model.ratio_bgs_mam(dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))
        baremammmess = dust_model.LOC_bgs_mam(dust_model.ratio_bgs_mam(dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface),dust_model.mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)))
        t8data = dust_tables.gett8data(barebirdrisk,barebirdmess,barereprisk,barerepmess,bareamphibrisk,bareamphibmess,baremammrisk,baremammmess)
        t8rows = dust_tables.gethtmlrowsfromcols(t8data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t8rows, headings=pvrheadings)))

        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)


app = webapp.WSGIApplication([('/.*', DUSTExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()


    
