import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from dust import dust_model
from dust import dust_parameters
import time
import datetime

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
    <table class="out_">
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

def gett1data(dust_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Label EPA Reg. No.', 'Maximum Single Application Rate', 
            'Fraction of Pesticide Assumed at the Surface','Dislodgeable Foliar Residue',],
        "Value": [dust_obj.chemical_name, dust_obj.label_epa_reg_no, dust_obj.ar_lb, dust_obj.frac_pest_surface, dust_obj.dislodge_fol_res,],
        "Units": ['', '', 'lbs a.i./A', '','mg a.i./cm^2', ],
    }
    return data

def gett2data(dust_obj):
    data = { 
        "Parameter": ['Bird Acute Oral Study (OCSPP 850.2100) MRID#', 'Additional Comments About the Study (if any)', 
            mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 
            'Tested Bird Body Weight','Mineau Scaling Factor for Birds',
            mark_safe('Mammal Acute Dermal (OCSPP 870.1200) MRID#'),'Additional Comments About Study (if any)',
            mark_safe('Mammal Acute Dermal LD<sub>50</sub>'), 'Avian Dermal type', mark_safe('Mammal Acute Oral LD<sub>50</sub>'),'Tested Mammal Body Weight',],
        "Value": [dust_obj.bird_acute_oral_study, dust_obj.bird_study_add_comm, dust_obj.low_bird_acute_ld50, dust_obj.test_bird_bw, dust_obj.mineau_scaling_factor, dust_obj.mamm_acute_derm_study,
               dust_obj.mamm_study_add_comm, dust_obj.mam_acute_derm_ld50, dust_obj.mam_acute_oral_ld50, dust_obj.test_mam_bw,],
        "Units": ['', '', 'mg a.i./kg-bw', 'g','','','', 'mg a.i./kg-bw','mg a.i./kg-bw','g', ],
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

def gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mam_acute_derm_ld50, mam_acute_oral_ld50,test_mam_bw,mineau_scaling_factor):
    data = { 
        "Parameter": ['Maximum Single Application Rate', 'Fraction of Pesticide Assumed at the Surface', 'Dislodgeable Foliar Residue', 
                     mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 'Tested Bird Body Weight', 'Mineau Scaling Factor for Birds',
                     mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),'Tested Mammal Body Weight',mark_safe('Mammal Acute Dermal LD<sub>50</sub>')],
        "Mean": ['%.2e' % numpy.mean(ar_lb),'%.2e' % numpy.mean(frac_pest_surface),'%.2e' % numpy.mean(dislodge_fol_res), '%.2e' % numpy.mean(low_bird_acute_ld50), 
                 '%.2e' % numpy.mean(test_bird_bw), '%.2e' % numpy.mean(mineau_scaling_factor), '%.2e' % numpy.mean(mam_acute_derm_ld50), '%.2e' % numpy.mean(test_mam_bw), '%.2e' % numpy.mean(mam_acute_oral_ld50),],
        "Std": ['%.2e' % numpy.std(ar_lb),'%.2e' % numpy.std(frac_pest_surface),'%.2e' % numpy.std(dislodge_fol_res), '%.2e' % numpy.std(low_bird_acute_ld50), 
                '%.2e' % numpy.std(test_bird_bw), '%.2e' % numpy.std(mineau_scaling_factor), '%.2e' % numpy.std(mam_acute_derm_ld50), '%.2e' % numpy.std(test_mam_bw), '%.2e' % numpy.std(mam_acute_oral_ld50),],
        "Min": ['%.2e' % numpy.min(ar_lb),'%.2e' % numpy.min(frac_pest_surface),'%.2e' % numpy.min(dislodge_fol_res), '%.2e' % numpy.min(low_bird_acute_ld50), 
                '%.2e' % numpy.min(test_bird_bw), '%.2e' % numpy.min(mineau_scaling_factor), '%.2e' % numpy.min(mam_acute_derm_ld50), '%.2e' % numpy.min(test_mam_bw), '%.2e' % numpy.min(mam_acute_oral_ld50),],
        "Max": ['%.2e' % numpy.max(ar_lb),'%.2e' % numpy.max(frac_pest_surface),'%.2e' % numpy.max(dislodge_fol_res), '%.2e' % numpy.max(low_bird_acute_ld50), 
                 '%.2e' % numpy.max(test_bird_bw), '%.2e' % numpy.max(mineau_scaling_factor), '%.2e' % numpy.max(mam_acute_derm_ld50), '%.2e' % numpy.max(test_mam_bw), '%.2e' % numpy.max(mam_acute_oral_ld50),],
        "Unit": ['lbs a.i./A', '', 'mg a.i./cm^2', 'mg a.i./kg-bw', 'g', '', 'mg a.i./kg-bw', 'g', 'mg a.i./kg-bw'],
    }
    return data

def gettsumdata_out(gran_bird_ex_derm_dose_out,gran_repamp_ex_derm_dose_out,gran_mam_ex_derm_dose_out,fol_bird_ex_derm_dose_out,fol_repamp_ex_derm_dose_out,fol_mam_ex_derm_dose_out,bgs_bird_ex_derm_dose_out,bgs_repamp_ex_derm_dose_out,bgs_mam_ex_derm_dose_out,ratio_gran_bird_out,ratio_gran_rep_out,ratio_gran_amp_out,ratio_gran_mam_out,ratio_fol_bird_out,ratio_fol_rep_out,ratio_fol_amp_out,ratio_fol_mam_out,ratio_bgs_bird_out,ratio_bgs_rep_out,ratio_bgs_amp_out,ratio_bgs_mam_out):
    data = { 
        "Parameter": ['Granular Application Bird External Dermal Dose', 'Granular Application Reptile/Amphibian External Dermal Dose', 'Granular Application Mammal External Dermal Dose', 
                      'Foliar Spray Application Bird External Dermal Dose', 'Foliar Spray Application Reptile/Amphibian External Dermal Dose', 'Foliar Spray Application Mammal External Dermal Dose',
                      'Bare Ground Spray Application Bird External Dermal Dose', 'Bare Ground Spray Application Reptile/Amphibian External Dermal Dose', 'Bare Ground Spray Application Mammal External Dermal Dose',
                      'Granular Ratio of Exposure to Toxicity Bird', 'Granular Ratio of Exposure to Toxicity Reptile', 'Granular Ratio of Exposure to Toxicity Amphibian', 'Granular Ratio of Exposure to Toxicity Mammal',
                      'Foliar Spray Ratio of Exposure to Toxicity Bird', 'Foliar Spray Ratio of Exposure to Toxicity Reptile', 'Foliar Spray Ratio of Exposure to Toxicity Amphibian', 'Foliar Spray Ratio of Exposure to Toxicity Mammal',
                      'Bare Ground Spray Ratio of Exposure to Toxicity Bird', 'Bare Ground Spray Ratio of Exposure to Toxicity Reptile', 'Bare Ground Spray Ratio of Exposure to Toxicity Amphibian', 'Bare Ground Spray Ratio of Exposure to Toxicity Mammal'],                 
        "Mean": ['%.2e' % numpy.mean(gran_bird_ex_derm_dose_out),'%.2e' % numpy.mean(gran_repamp_ex_derm_dose_out),'%.2e' % numpy.mean(gran_mam_ex_derm_dose_out),
        '%.2e' % numpy.mean(fol_bird_ex_derm_dose_out),'%.2e' % numpy.mean(fol_repamp_ex_derm_dose_out),'%.2e' % numpy.mean(fol_mam_ex_derm_dose_out),
        '%.2e' % numpy.mean(bgs_bird_ex_derm_dose_out),'%.2e' % numpy.mean(bgs_repamp_ex_derm_dose_out),'%.2e' % numpy.mean(bgs_mam_ex_derm_dose_out),
        '%.2e' % numpy.mean(ratio_gran_bird_out),'%.2e' % numpy.mean(ratio_gran_rep_out),'%.2e' % numpy.mean(ratio_gran_amp_out),
        '%.2e' % numpy.mean(ratio_gran_mam_out),'%.2e' % numpy.mean(ratio_fol_bird_out),'%.2e' % numpy.mean(ratio_fol_rep_out),
        '%.2e' % numpy.mean(ratio_fol_amp_out),'%.2e' % numpy.mean(ratio_fol_mam_out),'%.2e' % numpy.mean(ratio_bgs_bird_out),
        '%.2e' % numpy.mean(ratio_bgs_rep_out),'%.2e' % numpy.mean(ratio_bgs_amp_out),'%.2e' % numpy.mean(ratio_bgs_mam_out),],
        "Std": ['%.2e' % numpy.std(gran_bird_ex_derm_dose_out),'%.2e' % numpy.std(gran_repamp_ex_derm_dose_out),'%.2e' % numpy.std(gran_mam_ex_derm_dose_out),
        '%.2e' % numpy.std(fol_bird_ex_derm_dose_out),'%.2e' % numpy.std(fol_repamp_ex_derm_dose_out),'%.2e' % numpy.std(fol_mam_ex_derm_dose_out),
        '%.2e' % numpy.std(bgs_bird_ex_derm_dose_out),'%.2e' % numpy.std(bgs_repamp_ex_derm_dose_out),'%.2e' % numpy.std(bgs_mam_ex_derm_dose_out),
        '%.2e' % numpy.std(ratio_gran_bird_out),'%.2e' % numpy.std(ratio_gran_rep_out),'%.2e' % numpy.std(ratio_gran_amp_out),
        '%.2e' % numpy.std(ratio_gran_mam_out),'%.2e' % numpy.std(ratio_fol_bird_out),'%.2e' % numpy.std(ratio_fol_rep_out),
        '%.2e' % numpy.std(ratio_fol_amp_out),'%.2e' % numpy.std(ratio_fol_mam_out),'%.2e' % numpy.std(ratio_bgs_bird_out),
        '%.2e' % numpy.std(ratio_bgs_rep_out),'%.2e' % numpy.std(ratio_bgs_amp_out),'%.2e' % numpy.std(ratio_bgs_mam_out),],
        "Min": ['%.2e' % numpy.min(gran_bird_ex_derm_dose_out),'%.2e' % numpy.min(gran_repamp_ex_derm_dose_out),'%.2e' % numpy.min(gran_mam_ex_derm_dose_out),
        '%.2e' % numpy.min(fol_bird_ex_derm_dose_out),'%.2e' % numpy.min(fol_repamp_ex_derm_dose_out),'%.2e' % numpy.min(fol_mam_ex_derm_dose_out),
        '%.2e' % numpy.min(bgs_bird_ex_derm_dose_out),'%.2e' % numpy.min(bgs_repamp_ex_derm_dose_out),'%.2e' % numpy.min(bgs_mam_ex_derm_dose_out),
        '%.2e' % numpy.min(ratio_gran_bird_out),'%.2e' % numpy.min(ratio_gran_rep_out),'%.2e' % numpy.min(ratio_gran_amp_out),
        '%.2e' % numpy.min(ratio_gran_mam_out),'%.2e' % numpy.min(ratio_fol_bird_out),'%.2e' % numpy.min(ratio_fol_rep_out),
        '%.2e' % numpy.min(ratio_fol_amp_out),'%.2e' % numpy.min(ratio_fol_mam_out),'%.2e' % numpy.min(ratio_bgs_bird_out),
        '%.2e' % numpy.min(ratio_bgs_rep_out),'%.2e' % numpy.min(ratio_bgs_amp_out),'%.2e' % numpy.min(ratio_bgs_mam_out),],
        "Max": ['%.2e' % numpy.max(gran_bird_ex_derm_dose_out),'%.2e' % numpy.max(gran_repamp_ex_derm_dose_out),'%.2e' % numpy.max(gran_mam_ex_derm_dose_out),
        '%.2e' % numpy.max(fol_bird_ex_derm_dose_out),'%.2e' % numpy.max(fol_repamp_ex_derm_dose_out),'%.2e' % numpy.max(fol_mam_ex_derm_dose_out),
        '%.2e' % numpy.max(bgs_bird_ex_derm_dose_out),'%.2e' % numpy.max(bgs_repamp_ex_derm_dose_out),'%.2e' % numpy.max(bgs_mam_ex_derm_dose_out),
        '%.2e' % numpy.max(ratio_gran_bird_out),'%.2e' % numpy.max(ratio_gran_rep_out),'%.2e' % numpy.max(ratio_gran_amp_out),
        '%.2e' % numpy.max(ratio_gran_mam_out),'%.2e' % numpy.max(ratio_fol_bird_out),'%.2e' % numpy.max(ratio_fol_rep_out),
        '%.2e' % numpy.max(ratio_fol_amp_out),'%.2e' % numpy.max(ratio_fol_mam_out),'%.2e' % numpy.max(ratio_bgs_bird_out),
        '%.2e' % numpy.max(ratio_bgs_rep_out),'%.2e' % numpy.max(ratio_bgs_amp_out),'%.2e' % numpy.max(ratio_bgs_mam_out)],           

        #['%.2e' % numpy.mean(granbirdderm_out),'%.2e' % numpy.mean(granherpderm_out), '%.2e' % numpy.mean(granmammderm_out), 
                # '%.2e' % numpy.mean(folbirdderm_out), '%.2e' % numpy.mean(folherpderm_out), '%.2e' % numpy.mean(folmammderm_out), 
                # '%.2e' % numpy.mean(barebirdderm_out), '%.2e' % numpy.mean(bareherpderm_out), '%.2e' % numpy.mean(baremammderm_out),]
                # '%.2e' % numpy.mean(granbirdrisk_out), '%.2e' % numpy.mean(granreprisk_out), '%.2e' % numpy.mean(granamphibrisk_out), '%.2e' % numpy.mean(granmammrisk_out),
                # '%.2e' % numpy.mean(folbirdrisk_out), '%.2e' % numpy.mean(folreprisk_out), '%.2e' % numpy.mean(folamphibrisk_out), '%.2e' % numpy.mean(folmammrisk_out),
                # '%.2e' % numpy.mean(barebirdrisk_out), '%.2e' % numpy.mean(barereprisk_out), '%.2e' % numpy.mean(bareamphibrisk_out), '%.2e' % numpy.mean(baremammrisk_out),],

        # "Std": ['%.2e' % numpy.std(granbirdderm_out),'%.2e' % numpy.std(granherpderm_out), '%.2e' % numpy.std(granmammderm_out), 
        #         '%.2e' % numpy.std(folbirdderm_out), '%.2e' % numpy.std(folherpderm_out), '%.2e' % numpy.std(folmammderm_out), 
        #         '%.2e' % numpy.std(barebirdderm_out), '%.2e' % numpy.std(bareherpderm_out), '%.2e' % numpy.std(baremammderm_out),
        #         '%.2e' % numpy.std(granbirdrisk_out), '%.2e' % numpy.std(granreprisk_out), '%.2e' % numpy.std(granamphibrisk_out), '%.2e' % numpy.std(granmammrisk_out),
        #         '%.2e' % numpy.std(folbirdrisk_out), '%.2e' % numpy.std(folreprisk_out), '%.2e' % numpy.std(folamphibrisk_out), '%.2e' % numpy.std(folmammrisk_out),
        #         '%.2e' % numpy.std(barebirdrisk_out), '%.2e' % numpy.std(barereprisk_out), '%.2e' % numpy.std(bareamphibrisk_out), '%.2e' % numpy.std(baremammrisk_out),],

        # "Min": ['%.2e' % numpy.min(granbirdderm_out),'%.2e' % numpy.min(granherpderm_out), '%.2e' % numpy.min(granmammderm_out), 
        #         '%.2e' % numpy.min(folbirdderm_out), '%.2e' % numpy.min(folherpderm_out), '%.2e' % numpy.min(folmammderm_out), 
        #         '%.2e' % numpy.min(barebirdderm_out), '%.2e' % numpy.min(bareherpderm_out), '%.2e' % numpy.min(baremammderm_out),
        #         '%.2e' % numpy.min(granbirdrisk_out), '%.2e' % numpy.min(granreprisk_out), '%.2e' % numpy.min(granamphibrisk_out), '%.2e' % numpy.min(granmammrisk_out),
        #         '%.2e' % numpy.min(folbirdrisk_out), '%.2e' % numpy.min(folreprisk_out), '%.2e' % numpy.min(folamphibrisk_out), '%.2e' % numpy.min(folmammrisk_out),
        #         '%.2e' % numpy.min(barebirdrisk_out), '%.2e' % numpy.min(barereprisk_out), '%.2e' % numpy.min(bareamphibrisk_out), '%.2e' % numpy.min(baremammrisk_out),],

        #  "Max": ['%.2e' % numpy.max(granbirdderm_out),'%.2e' % numpy.max(granherpderm_out), '%.2e' % numpy.max(granmammderm_out),
        #          '%.2e' % numpy.max(folbirdderm_out), '%.2e' % numpy.max(folherpderm_out), '%.2e' % numpy.max(folmammderm_out), 
        #          '%.2e' % numpy.max(barebirdderm_out),'%.2e' % numpy.max(bareherpderm_out), '%.2e' % numpy.max(baremammderm_out),
        #          '%.2e' % numpy.max(granbirdrisk_out), '%.2e' % numpy.max(granreprisk_out), '%.2e' % numpy.max(granamphibrisk_out), '%.2e' % numpy.max(granmammrisk_out),
        #          '%.2e' % numpy.max(folbirdrisk_out), '%.2e' % numpy.max(folreprisk_out), '%.2e' % numpy.max(folamphibrisk_out), '%.2e' % numpy.max(folmammrisk_out),
        #          '%.2e' % numpy.max(barebirdrisk_out), '%.2e' % numpy.max(barereprisk_out), '%.2e' % numpy.max(bareamphibrisk_out), '%.2e' % numpy.max(baremammrisk_out),],

        "Unit": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw','','','','','','','','','','','','',],
    }
    return data

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(dust_obj):
    table3_out = table_3(dust_obj)
    table4_out = table_4(dust_obj)
    table5_out = table_5(dust_obj)
    table6_out = table_6(dust_obj)
    table7_out = table_7(dust_obj)
    table8_out = table_8(dust_obj)

    html_all = table_1(dust_obj)
    html_all = html_all + table_2(dust_obj)
    html_all = html_all + table3_out['html']
    html_all = html_all + table4_out['html']
    html_all = html_all + table5_out['html']
    html_all = html_all + table6_out['html']
    html_all = html_all + table7_out['html']
    html_all = html_all + table8_out['html']
    return html_all, table3_out, table4_out, table5_out, table6_out, table7_out, table8_out

def timestamp(dust_obj="", batch_jid=""):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    if dust_obj:
        st = datetime.datetime.strptime(dust_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>Dust Version 0.1 (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_sum_input(i, ar_lb,frac_pest_surface,dislodge_fol_res,low_bird_acute_ld50,test_bird_bw,mam_acute_derm_ld50, mam_acute_oral_ld50,test_mam_bw,mineau_scaling_factor):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><td><H3>Summary Statistics (Iterations=%s)</H3></td></tr>
        <tr></tr>
        </table>
        """%(i-1)
        #table sum_input
        tsuminputdata = gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mam_acute_derm_ld50,mam_acute_oral_ld50, test_mam_bw,mineau_scaling_factor)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html

def table_sum_output(gran_bird_ex_derm_dose_out,gran_repamp_ex_derm_dose_out,gran_mam_ex_derm_dose_out,fol_bird_ex_derm_dose_out,fol_repamp_ex_derm_dose_out,fol_mam_ex_derm_dose_out,bgs_bird_ex_derm_dose_out,bgs_repamp_ex_derm_dose_out,bgs_mam_ex_derm_dose_out,ratio_gran_bird_out,ratio_gran_rep_out,ratio_gran_amp_out,ratio_gran_mam_out,ratio_fol_bird_out,ratio_fol_rep_out,ratio_fol_amp_out,ratio_fol_mam_out,ratio_bgs_bird_out,ratio_bgs_rep_out,ratio_bgs_amp_out,ratio_bgs_mam_out):

        #pre-table sum_input
        html = """
        <br>
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(gran_bird_ex_derm_dose_out,gran_repamp_ex_derm_dose_out,gran_mam_ex_derm_dose_out,fol_bird_ex_derm_dose_out,fol_repamp_ex_derm_dose_out,fol_mam_ex_derm_dose_out,bgs_bird_ex_derm_dose_out,bgs_repamp_ex_derm_dose_out,bgs_mam_ex_derm_dose_out,ratio_gran_bird_out,ratio_gran_rep_out,ratio_gran_amp_out,ratio_gran_mam_out,ratio_fol_bird_out,ratio_fol_rep_out,ratio_fol_amp_out,ratio_fol_mam_out,ratio_bgs_bird_out,ratio_bgs_rep_out,ratio_bgs_amp_out,ratio_bgs_mam_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        return html

def table_1(dust_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical Identity</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(dust_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(dust_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Toxicity Properties</H4>
                <div class="out_ container_output">
        """
        #table 2
        t2data = gett2data(dust_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_3(dust_obj):
        #pre-table 3
        html = """
        <br>
        <H3 class="out_3 collapsible" id="section4"><span></span>Exposure Estimates</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section5"><span></span>Granular Application</H4>
                <div class="out_ container_output">
        """
        #table 3
        granbirdderm = dust_obj.gran_bird_ex_derm_dose
        granherpderm = dust_obj.gran_repamp_ex_derm_dose
        granmammderm = dust_obj.gran_mam_ex_derm_dose
        t3data = gett3data(granbirdderm, granherpderm, granmammderm)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return {'html':html, 'granbirdderm':granbirdderm, 'granherpderm':granherpderm, 'granmammderm':granmammderm}

def table_4(dust_obj):
        #pre-table 4
        html = """     
            <H4 class="out_4 collapsible" id="section5"><span></span>Foliar Spray Application (contact with foliar residues and directly applied spray)</H4>
                <div class="out_ container_output">
        """
        #table 4
        folbirdderm = dust_obj.fol_bird_ex_derm_dose
        folherpderm = dust_obj.fol_repamp_ex_derm_dose
        folmammderm = dust_obj.fol_mam_ex_derm_dose
        t4data = gett4data(folbirdderm, folherpderm, folmammderm)
        t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return {'html':html, 'folbirdderm':folbirdderm, 'folherpderm':folherpderm, 'folmammderm':folmammderm}

def table_5(dust_obj):
        #pre-table 5
        html = """         
            <H4 class="out_5 collapsible" id="section6"><span></span>Bare Ground Spray Application (contact with soil residues and directly applied spray)</H4>
                <div class="out_ container_output">
        """
        #table 5
        barebirdderm = dust_obj.bgs_bird_ex_derm_dose
        bareherpderm = dust_obj.bgs_repamp_ex_derm_dose
        baremammderm = dust_obj.bgs_mam_ex_derm_dose
        t5data = gett5data(barebirdderm, bareherpderm, baremammderm)
        t5rows = gethtmlrowsfromcols(t5data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'barebirdderm':barebirdderm, 'bareherpderm':bareherpderm, 'baremammderm':baremammderm}


def table_6(dust_obj):
        #pre-table 6
        html = """        
        <br>
        <H3 class="out_6 collapsible" id="section7"><span></span>Ratio of Exposure to Toxicity</H3>
        <div class="out_">
            <H4 class="out_6 collapsible" id="section8"><span></span>Granular</H4>
                <div class="out_ container_output">
        """
        #table 6
        granbirdrisk = dust_obj.ratio_gran_bird
        granbirdmess = dust_obj.LOC_gran_bird
        granreprisk = dust_obj.ratio_gran_rep
        granrepmess = dust_obj.LOC_gran_rep
        granamphibrisk = dust_obj.ratio_gran_amp
        granamphibmess = dust_obj.LOC_gran_amp
        granmammrisk = dust_obj.ratio_gran_mam
        granmammmess = dust_obj.LOC_gran_mam
        t6data = gett6data(granbirdrisk, granbirdmess, granreprisk, granrepmess, granamphibrisk, granamphibmess, granmammrisk, granmammmess)
        t6rows = gethtmlrowsfromcols(t6data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t6rows, headings=pvrheadings)))
        html = html + """
                </div>
        """
        return {'html':html, 'granbirdrisk':granbirdrisk, 'granreprisk':granreprisk, 
                'granamphibrisk':granamphibrisk, 'granmammrisk':granmammrisk}

def table_7(dust_obj):
        #pre-table 7
        html = """         
            <H4 class="out_7 collapsible" id="section9"><span></span>Foliar Spray</H4>
                <div class="out_ container_output">
        """
        #table 7
        folbirdrisk = dust_obj.ratio_fol_bird
        folbirdmess = dust_obj.LOC_fol_bird
        folreprisk = dust_obj.ratio_fol_rep
        folrepmess = dust_obj.LOC_fol_rep
        folamphibrisk = dust_obj.ratio_fol_amp
        folamphibmess = dust_obj.LOC_fol_amp
        folmammrisk = dust_obj.ratio_fol_mam
        folmammmess = dust_obj.LOC_fol_mam
        t7data = gett7data(folbirdrisk, folbirdmess, folreprisk, folrepmess, folamphibrisk, folamphibmess, folmammrisk, folmammmess)
        t7rows = gethtmlrowsfromcols(t7data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=pvrheadings)))
        html = html + """
                </div>
        """
        return {'html':html, 'folbirdrisk':folbirdrisk, 'folreprisk':folreprisk, 
                'folamphibrisk':folamphibrisk, 'folmammrisk':folmammrisk}


def table_8(dust_obj):
        #pre-table 8
        html = """          
            <H4 class="out_8 collapsible" id="section10"><span></span>Bare Ground Spray</H4>
                <div class="out_ container_output">
        """
        #table 8
        barebirdrisk = dust_obj.ratio_bgs_bird
        barebirdmess = dust_obj.LOC_bgs_bird
        barereprisk = dust_obj.ratio_bgs_rep
        barerepmess = dust_obj.LOC_bgs_rep
        bareamphibrisk = dust_obj.ratio_bgs_amp
        bareamphibmess = dust_obj.LOC_bgs_amp
        baremammrisk = dust_obj.ratio_bgs_mam
        baremammmess = dust_obj.LOC_bgs_mam
        t8data = gett8data(barebirdrisk, barebirdmess, barereprisk, barerepmess, bareamphibrisk, bareamphibmess, baremammrisk, baremammmess)
        t8rows = gethtmlrowsfromcols(t8data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t8rows, headings=pvrheadings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'barebirdrisk':barebirdrisk, 'barereprisk':barereprisk, 
                'bareamphibrisk':bareamphibrisk, 'baremammrisk':baremammrisk}
