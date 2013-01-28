# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 13:55:32 2012

@author: jharston
"""


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()


import math

#Application rate conversion to mg/cm2
def ar_mg(ar_lb):
    ar_lb = float(ar_lb)
    return ar_lb * 0.011208511


#Calculated Bird/Reptile Dermal LD50 (mg a.i./kg-bw)    
def bird_reptile_dermal_ld50(low_bird_acute_ld50):
    low_bird_acute_ld50 = float(low_bird_acute_ld50)
    return 10**(0.84+(0.62*(math.log(low_bird_acute_ld50))))
    

#------Granular Application------

#Bird External Dermal Dose
def gran_bird_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface)/1300)*0.958*(10*(20**0.667)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def gran_repamp_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((ar_mg*frac_pest_surface/1300)*0.958*(8.42*(20**0.694)))/(20.0/1000.0)
    

#Mammal External Dermal Dose
def gran_mam_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((ar_mg*frac_pest_surface/1300)*0.958*(12.3*(15**0.65)))/(15.0/1000.0)
    

#------Foliar Spray Application-------

#Bird External Dermal Dose
def fol_bird_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(10*(20**0.667)))+(ar_mg*((10*(20**0.667))/2)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(8.42*(20**0.694)))+(ar_mg*((8.42*(20**0.694))/2)))/(20.0/1000.0)
    
    
#Mammal External Dermal Dose
def fol_mam_ex_derm_dose(dislodge_fol_res,ar_mg):
    try:
        ar_mg = float(ar_mg)
        dislodge_fol_res = float(dislodge_fol_res)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return ((dislodge_fol_res*6.01*12*(12.3*(15**0.65)))+(ar_mg*((12.3*(15**0.65))/2)))/(15.0/1000.0)
    
    
#------Bare Ground Spray Application-------

#Bird External Dermal Dose
def bgs_bird_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(10*(20**0.667)))+(ar_mg*((10*(20**0.667))/2.0)))/(20.0/1000.0)
    

#Reptile/Amphibian External Dermal Dose
def bgs_repamp_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(8.42*(20**0.694)))+(ar_mg*((8.42*(20**0.694))/2.0)))/(20.0/1000.0)
    
    
#Mammal External Dermal Dose
def bgs_mam_ex_derm_dose(ar_mg,frac_pest_surface):
    try:
        ar_mg = float(ar_mg)
        frac_pest_surface = float(frac_pest_surface)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return (((ar_mg*frac_pest_surface/1300.0)*0.958*(12.3*(20**0.65)))+(ar_mg*((12.3*(20**0.65))/2.0)))/(15.0/1000.0)
    


#------Dermal Toxicity Calculation (ADJ LD50)------

#Estimate 20g Amphibian Dermal LD50 (mg a.i./kg-bw)
def amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau):
    try:
        low_bird_acute_ld50 = float(low_bird_acute_ld50)
        test_bird_bw = float(test_bird_bw)
        mineau = float(mineau)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return low_bird_acute_ld50*((20.0/test_bird_bw)**(mineau-1.0))
    

#Estimate 20g Bird/Reptile Dermal LD50 (mg a.i./kg-bw)
def birdrep_derm_ld50(bird_reptile_dermal_ld50,test_bird_bw,mineau):
    try:
        bird_reptile_dermal_ld50 = float(bird_reptile_dermal_ld50)
        test_bird_bw = float(test_bird_bw)
        mineau = float(mineau)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return bird_reptile_dermal_ld50*((20/test_bird_bw)**(mineau-1))
    

#Estimate 15g Mammal Dermal LD50 (mg a.i./kg-bw)
def mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw):
    try:
        mam_acute_derm_ld50 = float(mam_acute_derm_ld50)
        test_mam_bw = float(test_mam_bw)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('')
    return mam_acute_derm_ld50*((test_mam_bw/15.0)**0.25)
    

#------RATIO OF EXPOSURE TO TOXICITY------


#______Granular

#Bird
def ratio_gran_bird(gran_bird_ex_derm_dose,birdrep_derm_ld50):
    return gran_bird_ex_derm_dose/birdrep_derm_ld50
    
def LOC_gran_bird(ratio_gran_bird):
    if ratio_gran_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_gran_rep(gran_repamp_ex_derm_dose,birdrep_derm_ld50):
    return gran_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_gran_rep(ratio_gran_rep):
    if ratio_gran_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
#Amphibian
def ratio_gran_amp(gran_repamp_ex_derm_dose,amp_derm_ld50):
    return gran_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_gran_amp(ratio_gran_amp):
    if ratio_gran_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
#Mammal
def ratio_gran_mam(gran_mam_ex_derm_dose,mam_derm_ld50):
    return gran_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_gran_mam(ratio_gran_mam):
    if ratio_gran_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    

#_______Foliar Spray

#Bird
def ratio_fol_bird(fol_bird_ex_derm_dose,birdrep_derm_ld50):
    return fol_bird_ex_derm_dose/birdrep_derm_ld50

def LOC_fol_bird(ratio_fol_bird):
    if ratio_fol_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_fol_rep(fol_repamp_ex_derm_dose,birdrep_derm_ld50):
    return fol_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_fol_rep(ratio_fol_rep):
    if ratio_fol_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Amphibian
def ratio_fol_amp(fol_repamp_ex_derm_dose,amp_derm_ld50):
    return fol_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_fol_amp(ratio_fol_amp):
    if ratio_fol_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Mammal
def ratio_fol_mam(fol_mam_ex_derm_dose,mam_derm_ld50):
    return fol_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_fol_mam(ratio_fol_mam):
    if ratio_fol_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    

#_______Bare Ground Spray

#Bird
def ratio_bgs_bird(bgs_bird_ex_derm_dose,birdrep_derm_ld50):
    return bgs_bird_ex_derm_dose/birdrep_derm_ld50
    
def LOC_bgs_bird(ratio_bgs_bird):
    if ratio_bgs_bird < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Reptile
def ratio_bgs_rep(bgs_repamp_ex_derm_dose,birdrep_derm_ld50):
    return bgs_repamp_ex_derm_dose/birdrep_derm_ld50
    
def LOC_bgs_rep(ratio_bgs_rep):
    if ratio_bgs_rep < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Amphibian
def ratio_bgs_amp(bgs_repamp_ex_derm_dose,amp_derm_ld50):
    return bgs_repamp_ex_derm_dose/amp_derm_ld50
    
def LOC_bgs_amp(ratio_bgs_amp):
    if ratio_bgs_amp < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
#Mammal
def ratio_bgs_mam(bgs_mam_ex_derm_dose,mam_derm_ld50):
    return bgs_mam_ex_derm_dose/mam_derm_ld50
    
def LOC_bgs_mam(ratio_bgs_mam):
    if ratio_bgs_mam < 0.01:
        return ('Exposure Not Likely Significant')
    else:
        return ('Potentially Significant Pathway')    
    
    
    
    
  

    
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
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'dust'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html', {})   
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
               gran_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface), 
gran_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),
gran_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),
fol_bird_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),
fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),
fol_mam_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),
bgs_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),
bgs_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),
bgs_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),
ratio_gran_bird(gran_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_gran_bird(ratio_gran_bird(gran_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_gran_rep(gran_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_gran_rep(ratio_gran_rep(gran_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_gran_amp(gran_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
LOC_gran_amp(ratio_gran_amp(gran_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
ratio_gran_mam(gran_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
LOC_gran_mam(ratio_gran_mam(gran_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))),
ratio_fol_bird(fol_bird_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_fol_bird(ratio_fol_bird(fol_bird_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_fol_rep(fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_fol_rep(ratio_fol_rep(fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_fol_amp(fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
LOC_fol_amp(ratio_fol_amp(fol_repamp_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
ratio_fol_mam(fol_mam_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
LOC_fol_mam(ratio_fol_mam(fol_mam_ex_derm_dose(dislodge_fol_res,ar_mg(ar_lb)),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw))),
ratio_bgs_bird(bgs_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_bgs_bird(ratio_bgs_bird(bgs_bird_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_bgs_rep(bgs_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau)),
LOC_bgs_rep(ratio_bgs_rep(bgs_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),birdrep_derm_ld50(bird_reptile_dermal_ld50(low_bird_acute_ld50),test_bird_bw,mineau))),
ratio_bgs_amp(bgs_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau)),
LOC_bgs_amp(ratio_bgs_amp(bgs_repamp_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),amp_derm_ld50(low_bird_acute_ld50,test_bird_bw,mineau))),
ratio_bgs_mam(bgs_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)),
LOC_bgs_mam(ratio_bgs_mam(bgs_mam_ex_derm_dose(ar_mg(ar_lb),frac_pest_surface),mam_derm_ld50(mam_acute_derm_ld50,test_mam_bw)))  )
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', DUSTExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()


    
