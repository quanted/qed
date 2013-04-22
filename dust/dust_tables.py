import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from dust import dust_model
from dust import dust_parameters

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvr():
	headings = ["Parameter", "Value", "Results"]
	return headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows

def getdjtemplate():
    dj_template ="""
    <table id="output">
    {# headings #}
        <tr>
        {% for heading in headings %}
            <th>{{ heading }}</th>
        {% endfor %}
        </tr>
    {# data #}
    {% for row in data %}
    <tr>
        {% for val in row %}
        <td>{{ val|default:'' }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template

def gett1data(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res):
    data = { 
        "Parameter": ['Chemical Name', 'Label EPA Reg. No.', 'Maximum Single Application Rate', 
            'Fraction of Pesticide Assumed at the Surface','Dislodgeable Foliar Residue',],
        "Value": [chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res,],
        "Units": ['', '', 'lbs a.i./A', '','mg a.i./cm^2', ],
    }
    return data

def gett2data(bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study,
               mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):
    data = { 
        "Parameter": ['Bird Acute Oral Study (OCSPP 850.2100) MRID#', 'Additional Comments About the Study (if any)', 
            mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 
            'Tested Bird Body Weight','Mineau Scaling Factor for Birds',
            mark_safe('Mammal Acute Dermal (OCSPP 870.1200) MRID#'),'Additional Comments About Study (if any)',
            mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),'Tested Mammal Body Weight',],
        "Value": [bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study,
               mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw,],
        "Units": ['', '', 'mg a.i./kg-bw', 'g','','','','mg a.i./kg-bw','g', ],
    }
    return data

def gett3data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett4data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett5data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett6data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data

def gett7data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data

def gett8data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data

def gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
    data = { 
        "Parameter": ['Maximum Single Application Rate', 'Fraction of Pesticide Assumed at the Surface', 'Dislodgeable Foliar Residue', 
                     mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 'Tested Bird Body Weight', 'Mineau Scaling Factor for Birds',
                     mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),'Tested Mammal Body Weight',],
        "Mean": ['%5.2f' % numpy.mean(ar_lb),'%5.2f' % numpy.mean(frac_pest_surface),'%5.2f' % numpy.mean(dislodge_fol_res), '%5.2f' % numpy.mean(low_bird_acute_ld50), 
                 '%5.2f' % numpy.mean(test_bird_bw), '%5.2f' % numpy.mean(mineau), '%5.2f' % numpy.mean(mam_acute_derm_ld50), '%5.2f' % numpy.mean(test_mam_bw),],
        "Std": ['%5.2f' % numpy.std(ar_lb),'%5.2f' % numpy.std(frac_pest_surface),'%5.2f' % numpy.std(dislodge_fol_res), '%5.2f' % numpy.std(low_bird_acute_ld50), 
                '%5.2f' % numpy.std(test_bird_bw), '%5.2f' % numpy.std(mineau), '%5.2f' % numpy.std(mam_acute_derm_ld50), '%5.2f' % numpy.std(test_mam_bw),],
        "Min": ['%5.2f' % numpy.min(ar_lb),'%5.2f' % numpy.min(frac_pest_surface),'%5.2f' % numpy.min(dislodge_fol_res), '%5.2f' % numpy.min(low_bird_acute_ld50), 
                '%5.2f' % numpy.min(test_bird_bw), '%5.2f' % numpy.min(mineau), '%5.2f' % numpy.min(mam_acute_derm_ld50), '%5.2f' % numpy.min(test_mam_bw),],
         "Max": ['%5.2f' % numpy.max(ar_lb),'%5.2f' % numpy.max(frac_pest_surface),'%5.2f' % numpy.max(dislodge_fol_res), '%5.2f' % numpy.max(low_bird_acute_ld50), 
                 '%5.2f' % numpy.max(test_bird_bw), '%5.2f' % numpy.max(mineau), '%5.2f' % numpy.max(mam_acute_derm_ld50), '%5.2f' % numpy.max(test_mam_bw),],
        "Unit": ['lbs a.i./A', '', 'mg a.i./cm^2', 'mg a.i./kg-bw', 'g', '', 'mg a.i./kg-bw', 'g'],
    }
    return data

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(pvuheadings, pvrheadings, tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
              low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):

    html_all = table_1(pvuheadings, tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res)
    html_all = html_all + table_2(pvuheadings, tmpl, bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, 
                         mamm_acute_derm_study,mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw)
    html_all = html_all + table_3(pvuheadings, tmpl, ar_lb, frac_pest_surface)
    html_all = html_all + table_4(pvuheadings, tmpl, ar_lb, dislodge_fol_res)
    html_all = html_all + table_5(pvuheadings, tmpl, ar_lb, frac_pest_surface)
    html_all = html_all + table_6(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    html_all = html_all + table_7(pvrheadings, tmpl, ar_lb, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    html_all = html_all + table_8(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    return html_all

def table_sum_input(sumheadings, tmpl, i, ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><H3>Summary Statistics (Iterations=%s)</H3></tr>
        <tr></tr>
        </table>
        """%(i-1)
        #table sum_input
        tsuminputdata = gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html


def table_1(pvuheadings, tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res):
        #pre-table 1
        html = """
        <table border="1" border="1" class="out_1">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """
        #table 1
        t1data = gett1data(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        return html

def table_2(pvuheadings, tmpl, bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, 
            mamm_acute_derm_study,mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):
        # #pre-table 2
        html = """        
        <table border="1" class="out_2">
        <tr><H4>Toxicity Properties</H4></tr>
        <tr></tr>
        </table>
        """

        #table 2
        t2data = gett2data(bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, 
            mamm_acute_derm_study,mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        return html

def table_3(pvuheadings, tmpl, ar_lb, frac_pest_surface):
        #pre-table 3
        html = """
        <table border="1" class="out_3">
        <tr><H3>Exposure Estimates</H3></tr>
        <tr><H4>Granular Application</H4></tr>
        <tr>(contact with soil residues via dust and soil surface)</tr>
        </table>
        """

        #table 3
        granbirdderm = dust_model.gran_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        granherpderm = dust_model.gran_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface) 
        granmammderm = dust_model.gran_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        t3data = gett3data(granbirdderm,granherpderm,granmammderm)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        return html

def table_4(pvuheadings, tmpl, ar_lb, dislodge_fol_res):
        #pre-table 4
        html = """     
        <table border="1" class="out_4">
        <tr><H4>Foliar Spray Application</H4></tr>
        <tr>(contact with foliar residues and directly applied spray)</tr>
        </table>
        """

        #table 4
        folbirdderm = dust_model.fol_bird_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        folherpderm = dust_model.fol_repamp_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        folmammderm = dust_model.fol_mam_ex_derm_dose(dislodge_fol_res,dust_model.ar_mg(ar_lb))
        t4data = gett4data(folbirdderm,folherpderm,folmammderm)
        t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        return html

def table_5(pvuheadings, tmpl, ar_lb, frac_pest_surface):
        #pre-table 5
        html = """         
        <table border="1" class="out_5">
        <tr><H4>Bare Ground Spray Application</H4></tr>
        <tr>(contact with soil residues and directly applied spray)</tr>
        </table>
        """

        #table 5
        barebirdderm = dust_model.bgs_bird_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        bareherpderm = dust_model.bgs_repamp_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        baremammderm = dust_model.bgs_mam_ex_derm_dose(dust_model.ar_mg(ar_lb),frac_pest_surface)
        t5data = gett5data(barebirdderm,bareherpderm,baremammderm)
        t5rows = gethtmlrowsfromcols(t5data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pvuheadings)))
        return html


def table_6(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
        #pre-table 6
        html = """        
        <br></br>
        <table border="1" class="out_6">
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
        t6data = gett6data(granbirdrisk,granbirdmess,granreprisk,granrepmess,granamphibrisk,granamphibmess,granmammrisk,granmammmess)
        t6rows = gethtmlrowsfromcols(t6data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t6rows, headings=pvrheadings)))
        return html

def table_7(pvrheadings, tmpl, ar_lb, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
        #pre-table 7
        html = """         
        <table border="1" class="out_7">
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
        t7data = gett7data(folbirdrisk,folbirdmess,folreprisk,folrepmess,folamphibrisk,folamphibmess,folmammrisk,folmammmess)
        t7rows = gethtmlrowsfromcols(t7data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=pvrheadings)))
        return html

def table_8(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
        #pre-table 8
        html = """          
        <table border="1" class="out_8">
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
        t8data = gett8data(barebirdrisk,barebirdmess,barereprisk,barerepmess,bareamphibrisk,bareamphibmess,baremammrisk,baremammmess)
        t8rows = gethtmlrowsfromcols(t8data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t8rows, headings=pvrheadings)))
        return html