import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from trex2 import trex2_model
from trex2 import trex2_parameters

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva():
    headings = ["App", "Rate", "Number of Days"]
    return headings

def getheaderpv5():
    headings_1 = ["Avian (20g)", "Mammalian (15g)"]
    headings_2 = ["Size", "AAcute #1", "AAcute #2", "AChronic", "MAcute #1", "MAcute #2", "MChronic"]
    headings_2_show = ["Size", "Acute #1", "Acute #2", "Chronic", "Acute #1", "Acute #2", "Chronic"]
    return headings_1, headings_2, headings_2_show

def getheaderpv6():
    headings = ["Application Target", "Value"]
    return headings

def getheaderpv7():
    headings = ["Application Target", "Small", "Medium", "Large"]
    return headings

def getheaderpv8():
    headings = ["Application Target", "Acute", "Chronic"]
    return headings

def getheaderpv10():
    headings = ["Application Target", "Acute_sm", "Chronic_sm", "Acute_md", "Chronic_md", "Acute_lg", "Chronic_lg"]
    return headings

def getheaderpv12():
    headings = ["Animal Size", "Avian", "Mammal"]
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
            <th colspan={{ th_span|default:'1' }}>{{ heading }}</th>
        {% endfor %}
        </tr>
    
    {% if sub_headings %}
        <tr>
        {% for sub_heading in sub_headings %}
            <th>{{ sub_heading }}</th>
        {% endfor %}
        </tr>
    {% endif %}
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

def getdjtemplate_10():
    dj_template ="""
    <table class="out_">
    {# headings #}
      <tr>
        <th rowspan="2">Application Target</div></th>
        <th colspan="2">Small</th>
        <th colspan="2">Medium</th>
        <th colspan="2">Large</th>
        </tr>
        <tr>
        <th scope="col">Acute</div></th>       
        <th scope="col">Chronic</div></th> 
        <th scope="col">Acute</div></th> 
        <th scope="col">Chronic</div></th>  
        <th scope="col">Acute</div></th> 
        <th scope="col">Chronic</div></th>                  
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

def gett1data(chemical_name, Use, Formulated_product_name, percent_ai, Application_type, r_s, b_w, percent_incorporated,
              density_of_product, Foliar_dissipation_half_life):
    data = { 
        "Parameter": ['Chemical Name', 'Use', 'Formulated product name', 'Percentage active ingredient', 
                      'Application type', 'Row spacing', 'Bandwidth', 'Percentage incorporated', 'Density of product', 'Foliar dissipation half-life',],
        "Value": ['%s' % chemical_name, '%s' % Use, '%s' % Formulated_product_name, '%s' % percent_ai, '%s' % Application_type, 
                  '%.4s' % r_s, '%.4s' % b_w, '%s' % percent_incorporated, '%s' % density_of_product, '%s' % Foliar_dissipation_half_life,],
        "Units": ['', '', '', '%', '', 'inch', 'inch', '%', 'lbs/gal', 'days',],
    }
    return data

def gett2data(index, rate, day):
    data = { 
        "App": ['%s' %index,  ],
        "Rate": [rate,],
        "Number of Days": [day,],
    }
    return data

def gett3data(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, 
            bw_assessed_bird_l, Species_tested_bird, bw_tested_bird, mineau_scaling_factor):
    data = { 
        "Parameter": ['Avian LD50', 'Avian LC50', 'Avian NOAEC', 'Avian NOAEL', 'Body weight of assessed bird small',
                      'Body weight of assessed bird medium', 'Body weight of assessed bird large', 
                      'Species of the tested bird', 'Body weight of tested bird', 'Mineau scaling factor', ],
        "Value": ['%s' % avian_ld50, '%s' % avian_lc50, '%s' % avian_NOAEC, '%s' % avian_NOAEL, 
                  '%s' % bw_assessed_bird_s, '%s' % bw_assessed_bird_m, '%s' % bw_assessed_bird_l,
                  '%s' % Species_tested_bird, '%s' % bw_tested_bird, '%s' % mineau_scaling_factor, ],
        "Units": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', 'g', 'g', 'g', '', 'g', '', ],
    }
    return data

def gett4data(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, 
              bw_assessed_mamm_l, bw_tested_mamm):
    data = { 
        "Parameter": ['Mammalian LD50', 'Mammalian LC50', 'Mammalian NOAEC', 'Mammalian NOAEL', 'Body weight of assessed mammal small',
                      'Body weight of assessed mammal medium', 'Body weight of assessed mammal large', 
                      'Body weight of tested mammal', ],
        "Value": ['%s' % mammalian_ld50, '%s' % mammalian_lc50, '%s' % mammalian_NOAEC, '%s' % mammalian_NOAEL, 
                  '%s' % bw_assessed_mamm_s, '%s' % bw_assessed_mamm_m, '%s' % bw_assessed_mamm_l, '%s' % bw_tested_mamm, ],
        "Units": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', 'g', 'g', 'g', 'g', ],
    }
    return data

def gett5data(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
              sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
              sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l):
    data = { 
        "Size": ['Small', 'Medium','Large', ],
        "AAcute #1": ['%.2e' % sa_bird_1_s, '%.2e' % sa_bird_1_m, '%.2e' % sa_bird_1_l,],
        "AAcute #2": ['%.2e' % sa_bird_2_s, '%.2e' % sa_bird_2_m, '%.2e' % sa_bird_2_l,],
        "AChronic": ['%.2e' % sc_bird_s, '%.2e' % sc_bird_m, '%.2e' % sc_bird_l,],
        "MAcute #1": ['%.2e' % sa_mamm_1_s, '%.2e' % sa_mamm_1_m, '%.2e' % sa_mamm_1_l,],
        "MAcute #2": ['%.2e' % sa_mamm_2_s, '%.2e' % sa_mamm_2_m, '%.2e' % sa_mamm_2_l,],
        "MChronic": ['%.2e' % sc_mamm_s, '%.2e' % sc_mamm_m, '%.2e' % sc_mamm_l,],
    }
    return data

def gett6data(EEC_diet_SG, EEC_diet_TG, EEC_diet_BP, EEC_diet_FR, EEC_diet_AR):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods/Seeds', 'Arthropods',],
        "Value": ['%.2e' % EEC_diet_SG, '%.2e' % EEC_diet_TG, '%.2e' % EEC_diet_BP, '%.2e' % EEC_diet_FR, '%.2e' % EEC_diet_AR],
    }
    return data

def gett7data(EEC_dose_bird_SG_sm, EEC_dose_bird_SG_md, EEC_dose_bird_SG_lg, EEC_dose_bird_TG_sm, EEC_dose_bird_TG_md, EEC_dose_bird_TG_lg, EEC_dose_bird_BP_sm, EEC_dose_bird_BP_md, EEC_dose_bird_BP_lg, EEC_dose_bird_FP_sm, EEC_dose_bird_FP_md, EEC_dose_bird_FP_lg, EEC_dose_bird_AR_sm, EEC_dose_bird_AR_md, EEC_dose_bird_AR_lg, EEC_dose_bird_SE_sm, EEC_dose_bird_SE_md, EEC_dose_bird_SE_lg):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods', 'Arthropods', 'Seeds',],
        "Small": ['%.2e' % EEC_dose_bird_SG_sm, '%.2e' % EEC_dose_bird_TG_sm, '%.2e' % EEC_dose_bird_BP_sm, '%.2e' % EEC_dose_bird_FP_sm, '%.2e' % EEC_dose_bird_AR_sm, '%.2e' % EEC_dose_bird_SE_sm],
        "Medium": ['%.2e' % EEC_dose_bird_SG_md, '%.2e' % EEC_dose_bird_TG_md, '%.2e' % EEC_dose_bird_BP_md, '%.2e' % EEC_dose_bird_FP_md, '%.2e' % EEC_dose_bird_AR_md, '%.2e' % EEC_dose_bird_SE_md],
        "Large": ['%.2e' % EEC_dose_bird_SG_lg, '%.2e' % EEC_dose_bird_TG_lg, '%.2e' % EEC_dose_bird_BP_lg, '%.2e' % EEC_dose_bird_FP_lg, '%.2e' % EEC_dose_bird_AR_lg, '%.2e' % EEC_dose_bird_SE_lg],
    }
    return data

def gett8data(ARQ_diet_bird_SG_A, ARQ_diet_bird_SG_C, ARQ_diet_bird_TG_A, ARQ_diet_bird_TG_C, ARQ_diet_bird_BP_A, ARQ_diet_bird_BP_C, ARQ_diet_bird_FP_A, ARQ_diet_bird_FP_C, ARQ_diet_bird_AR_A, ARQ_diet_bird_AR_C):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods', 'Arthropods',],
        "Acute": ['%.2e' % ARQ_diet_bird_SG_A, '%.2e' % ARQ_diet_bird_TG_A, '%.2e' % ARQ_diet_bird_BP_A, '%.2e' % ARQ_diet_bird_FP_A, '%.2e' % ARQ_diet_bird_AR_A,],
        "Chronic": ['%.2e' % ARQ_diet_bird_SG_C, '%.2e' % ARQ_diet_bird_TG_C, '%.2e' % ARQ_diet_bird_BP_C, '%.2e' % ARQ_diet_bird_FP_C, '%.2e' % ARQ_diet_bird_AR_C,],
    }
    return data  

def gett9data(EEC_dose_mamm_SG_sm,EEC_dose_mamm_SG_md,EEC_dose_mamm_SG_lg,EEC_dose_mamm_TG_sm,EEC_dose_mamm_TG_md,EEC_dose_mamm_TG_lg,EEC_dose_mamm_BP_sm,EEC_dose_mamm_BP_md,EEC_dose_mamm_BP_lg,EEC_dose_mamm_FP_sm,EEC_dose_mamm_FP_md,EEC_dose_mamm_FP_lg,EEC_dose_mamm_AR_sm,EEC_dose_mamm_AR_md,EEC_dose_mamm_AR_lg,EEC_dose_mamm_SE_sm,EEC_dose_mamm_SE_md,EEC_dose_mamm_SE_lg):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods', 'Arthropods', 'Seeds',],
        "Small": ['%.2e' % EEC_dose_mamm_SG_sm, '%.2e' % EEC_dose_mamm_TG_sm, '%.2e' % EEC_dose_mamm_BP_sm, '%.2e' % EEC_dose_mamm_FP_sm, '%.2e' % EEC_dose_mamm_AR_sm, '%.2e' % EEC_dose_mamm_SE_sm],
        "Medium": ['%.2e' % EEC_dose_mamm_SG_md, '%.2e' % EEC_dose_mamm_TG_md, '%.2e' % EEC_dose_mamm_BP_md, '%.2e' % EEC_dose_mamm_FP_md, '%.2e' % EEC_dose_mamm_AR_md, '%.2e' % EEC_dose_mamm_SE_md],
        "Large": ['%.2e' % EEC_dose_mamm_SG_lg, '%.2e' % EEC_dose_mamm_TG_lg, '%.2e' % EEC_dose_mamm_BP_lg, '%.2e' % EEC_dose_mamm_FP_lg, '%.2e' % EEC_dose_mamm_AR_lg, '%.2e' % EEC_dose_mamm_SE_lg],
    }
    return data

def gett10data(ARQ_dose_mamm_SG_sm,CRQ_dose_mamm_SG_sm,ARQ_dose_mamm_SG_md,CRQ_dose_mamm_SG_md,ARQ_dose_mamm_SG_lg,CRQ_dose_mamm_SG_lg,ARQ_dose_mamm_TG_sm,CRQ_dose_mamm_TG_sm,ARQ_dose_mamm_TG_md,CRQ_dose_mamm_TG_md,ARQ_dose_mamm_TG_lg,CRQ_dose_mamm_TG_lg,ARQ_dose_mamm_BP_sm,CRQ_dose_mamm_BP_sm,ARQ_dose_mamm_BP_md,CRQ_dose_mamm_BP_md,ARQ_dose_mamm_BP_lg,CRQ_dose_mamm_BP_lg,ARQ_dose_mamm_FP_sm,CRQ_dose_mamm_FP_sm,ARQ_dose_mamm_FP_md,CRQ_dose_mamm_FP_md,ARQ_dose_mamm_FP_lg,CRQ_dose_mamm_FP_lg,ARQ_dose_mamm_AR_sm,CRQ_dose_mamm_AR_sm,ARQ_dose_mamm_AR_md,CRQ_dose_mamm_AR_md,ARQ_dose_mamm_AR_lg,CRQ_dose_mamm_AR_lg,ARQ_dose_mamm_SE_sm,CRQ_dose_mamm_SE_sm,ARQ_dose_mamm_SE_md,CRQ_dose_mamm_SE_md,ARQ_dose_mamm_SE_lg,CRQ_dose_mamm_SE_lg):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods', 'Arthropods', 'Seeds',],
        "Acute_sm": ['%.2e' % ARQ_dose_mamm_SG_sm, '%.2e' % ARQ_dose_mamm_TG_sm, '%.2e' % ARQ_dose_mamm_BP_sm, '%.2e' % ARQ_dose_mamm_FP_sm, '%.2e' % ARQ_dose_mamm_AR_sm, '%.2e' % ARQ_dose_mamm_SE_sm],
        "Chronic_sm": ['%.2e' % CRQ_dose_mamm_SG_sm, '%.2e' % CRQ_dose_mamm_TG_sm, '%.2e' % CRQ_dose_mamm_BP_sm, '%.2e' % CRQ_dose_mamm_FP_sm, '%.2e' % CRQ_dose_mamm_AR_sm, '%.2e' % CRQ_dose_mamm_SE_sm],
        "Acute_md": ['%.2e' % ARQ_dose_mamm_SG_md, '%.2e' % ARQ_dose_mamm_TG_md, '%.2e' % ARQ_dose_mamm_BP_md, '%.2e' % ARQ_dose_mamm_FP_md, '%.2e' % ARQ_dose_mamm_AR_md, '%.2e' % ARQ_dose_mamm_SE_md],
        "Chronic_md": ['%.2e' % CRQ_dose_mamm_SG_md, '%.2e' % CRQ_dose_mamm_TG_md, '%.2e' % CRQ_dose_mamm_BP_md, '%.2e' % CRQ_dose_mamm_FP_md, '%.2e' % CRQ_dose_mamm_AR_md, '%.2e' % CRQ_dose_mamm_SE_md],
        "Acute_lg": ['%.2e' % ARQ_dose_mamm_SG_lg, '%.2e' % ARQ_dose_mamm_TG_lg, '%.2e' % ARQ_dose_mamm_BP_lg, '%.2e' % ARQ_dose_mamm_FP_lg, '%.2e' % ARQ_dose_mamm_AR_lg, '%.2e' % ARQ_dose_mamm_SE_lg],
        "Chronic_lg": ['%.2e' % CRQ_dose_mamm_SG_lg, '%.2e' % CRQ_dose_mamm_TG_lg, '%.2e' % CRQ_dose_mamm_BP_lg, '%.2e' % CRQ_dose_mamm_FP_lg, '%.2e' % CRQ_dose_mamm_AR_lg, '%.2e' % CRQ_dose_mamm_SE_lg], 
    }
    return data

def gett11data(ARQ_diet_mamm_SG,CRQ_diet_bird_SG,ARQ_diet_mamm_TG,CRQ_diet_bird_TG,ARQ_diet_mamm_BP,CRQ_diet_bird_BP,ARQ_diet_mamm_FP,CRQ_diet_bird_FP,ARQ_diet_mamm_AR,CRQ_diet_bird_AR):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods/Seeds', 'Arthropods',],
        "Acute": ['%.2e' % ARQ_diet_mamm_SG, '%.2e' % ARQ_diet_mamm_TG, '%.2e' % ARQ_diet_mamm_BP, '%.2e' % ARQ_diet_mamm_FP, '%.2e' % ARQ_diet_mamm_AR],
        "Chronic": ['%.2e' % CRQ_diet_bird_SG, '%.2e' % CRQ_diet_bird_TG, '%.2e' % CRQ_diet_bird_BP, '%.2e' % CRQ_diet_bird_FP, '%.2e' % CRQ_diet_bird_AR],
    }
    return data 


def gett12data(LD50_rg_bird_sm,LD50_rg_mamm_sm,LD50_rg_bird_md,LD50_rg_mamm_md,LD50_rg_bird_lg,LD50_rg_mamm_lg):
    data = { 
        "Animal Size": ['Small', 'Medium', 'Large',],
        "Avian": ['%.2e' % LD50_rg_bird_sm, '%.2e' % LD50_rg_bird_md, '%.2e' % LD50_rg_bird_lg,],
        "Mammal": ['%.2e' % LD50_rg_mamm_sm, '%.2e' % LD50_rg_mamm_md, '%.2e' % LD50_rg_mamm_lg,],
    }
    return data



def gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
    data = { 
        "Parameter": ['Maximum Single Application Rate', 'Fraction of Pesticide Assumed at the Surface', 'Dislodgeable Foliar Residue', 
                     mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 'Tested Bird Body Weight', 'Mineau Scaling Factor for Birds',
                     mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),'Tested Mammal Body Weight',],
        "Mean": ['%.2e' % numpy.mean(ar_lb),'%.2e' % numpy.mean(frac_pest_surface),'%.2e' % numpy.mean(dislodge_fol_res), '%.2e' % numpy.mean(low_bird_acute_ld50), 
                 '%.2e' % numpy.mean(test_bird_bw), '%.2e' % numpy.mean(mineau), '%.2e' % numpy.mean(mam_acute_derm_ld50), '%.2e' % numpy.mean(test_mam_bw),],
        "Std": ['%.2e' % numpy.std(ar_lb),'%.2e' % numpy.std(frac_pest_surface),'%.2e' % numpy.std(dislodge_fol_res), '%.2e' % numpy.std(low_bird_acute_ld50), 
                '%.2e' % numpy.std(test_bird_bw), '%.2e' % numpy.std(mineau), '%.2e' % numpy.std(mam_acute_derm_ld50), '%.2e' % numpy.std(test_mam_bw),],
        "Min": ['%.2e' % numpy.min(ar_lb),'%.2e' % numpy.min(frac_pest_surface),'%.2e' % numpy.min(dislodge_fol_res), '%.2e' % numpy.min(low_bird_acute_ld50), 
                '%.2e' % numpy.min(test_bird_bw), '%.2e' % numpy.min(mineau), '%.2e' % numpy.min(mam_acute_derm_ld50), '%.2e' % numpy.min(test_mam_bw),],
         "Max": ['%.2e' % numpy.max(ar_lb),'%.2e' % numpy.max(frac_pest_surface),'%.2e' % numpy.max(dislodge_fol_res), '%.2e' % numpy.max(low_bird_acute_ld50), 
                 '%.2e' % numpy.max(test_bird_bw), '%.2e' % numpy.max(mineau), '%.2e' % numpy.max(mam_acute_derm_ld50), '%.2e' % numpy.max(test_mam_bw),],
        "Unit": ['lbs a.i./A', '', 'mg a.i./cm^2', 'mg a.i./kg-bw', 'g', '', 'mg a.i./kg-bw', 'g'],
    }
    return data

def gettsumdata_out(granbirdderm_out, granherpderm_out, granmammderm_out,folbirdderm_out, folherpderm_out, folmammderm_out, barebirdderm_out, bareherpderm_out, baremammderm_out, granbirdrisk_out, granreprisk_out, granamphibrisk_out, granmammrisk_out, folbirdrisk_out, folreprisk_out, folamphibrisk_out, folmammrisk_out,  barebirdrisk_out, barereprisk_out, bareamphibrisk_out, baremammrisk_out):
    data = { 
        "Parameter": ['Granular Application Bird External Dermal Dose', 'Granular Application Reptile/Amphibian External Dermal Dose', 'Granular Application Mammal External Dermal Dose', 
                      'Foliar Spray Application Bird External Dermal Dose', 'Foliar Spray Application Reptile/Amphibian External Dermal Dose', 'Foliar Spray Application Mammal External Dermal Dose',
                      'Bare Ground Spray Application Bird External Dermal Dose', 'Bare Ground Spray Application Reptile/Amphibian External Dermal Dose', 'Bare Ground Spray Application Mammal External Dermal Dose',
                      'Granular Application Bird Ratio of Exposure to Toxicity', 'Granular Application Reptile Ratio of Exposure to Toxicity', 'Granular Application Amphibian Ratio of Exposure to Toxicity', 'Granular Application Mammal Ratio of Exposure to Toxicity',
                      'Foliar Spray Application Bird Ratio of Exposure to Toxicity', 'Foliar Spray Application Reptile Ratio of Exposure to Toxicity', 'Foliar Spray Application Amphibian Ratio of Exposure to Toxicity', 'Foliar Spray Application Mammal Ratio of Exposure to Toxicity',
                      'Bare Ground Spray Application Bird Ratio of Exposure to Toxicity', 'Bare Ground Spray Application Reptile Ratio of Exposure to Toxicity', 'Bare Ground Spray Application Amphibian Ratio of Exposure to Toxicity', 'Bare Ground Spray Application Mammal Ratio of Exposure to Toxicity',],

        "Mean": ['%.2e' % numpy.mean(granbirdderm_out),'%.2e' % numpy.mean(granherpderm_out), '%.2e' % numpy.mean(granmammderm_out), 
                 '%.2e' % numpy.mean(folbirdderm_out), '%.2e' % numpy.mean(folherpderm_out), '%.2e' % numpy.mean(folmammderm_out), 
                 '%.2e' % numpy.mean(barebirdderm_out), '%.2e' % numpy.mean(bareherpderm_out), '%.2e' % numpy.mean(baremammderm_out),
                 '%.2e' % numpy.mean(granbirdrisk_out), '%.2e' % numpy.mean(granreprisk_out), '%.2e' % numpy.mean(granamphibrisk_out), '%.2e' % numpy.mean(granmammrisk_out),
                 '%.2e' % numpy.mean(folbirdrisk_out), '%.2e' % numpy.mean(folreprisk_out), '%.2e' % numpy.mean(folamphibrisk_out), '%.2e' % numpy.mean(folmammrisk_out),
                 '%.2e' % numpy.mean(barebirdrisk_out), '%.2e' % numpy.mean(barereprisk_out), '%.2e' % numpy.mean(bareamphibrisk_out), '%.2e' % numpy.mean(baremammrisk_out),],

        "Std": ['%.2e' % numpy.std(granbirdderm_out),'%.2e' % numpy.std(granherpderm_out), '%.2e' % numpy.std(granmammderm_out), 
                '%.2e' % numpy.std(folbirdderm_out), '%.2e' % numpy.std(folherpderm_out), '%.2e' % numpy.std(folmammderm_out), 
                '%.2e' % numpy.std(barebirdderm_out), '%.2e' % numpy.std(bareherpderm_out), '%.2e' % numpy.std(baremammderm_out),
                '%.2e' % numpy.std(granbirdrisk_out), '%.2e' % numpy.std(granreprisk_out), '%.2e' % numpy.std(granamphibrisk_out), '%.2e' % numpy.std(granmammrisk_out),
                '%.2e' % numpy.std(folbirdrisk_out), '%.2e' % numpy.std(folreprisk_out), '%.2e' % numpy.std(folamphibrisk_out), '%.2e' % numpy.std(folmammrisk_out),
                '%.2e' % numpy.std(barebirdrisk_out), '%.2e' % numpy.std(barereprisk_out), '%.2e' % numpy.std(bareamphibrisk_out), '%.2e' % numpy.std(baremammrisk_out),],

        "Min": ['%.2e' % numpy.min(granbirdderm_out),'%.2e' % numpy.min(granherpderm_out), '%.2e' % numpy.min(granmammderm_out), 
                '%.2e' % numpy.min(folbirdderm_out), '%.2e' % numpy.min(folherpderm_out), '%.2e' % numpy.min(folmammderm_out), 
                '%.2e' % numpy.min(barebirdderm_out), '%.2e' % numpy.min(bareherpderm_out), '%.2e' % numpy.min(baremammderm_out),
                '%.2e' % numpy.min(granbirdrisk_out), '%.2e' % numpy.min(granreprisk_out), '%.2e' % numpy.min(granamphibrisk_out), '%.2e' % numpy.min(granmammrisk_out),
                '%.2e' % numpy.min(folbirdrisk_out), '%.2e' % numpy.min(folreprisk_out), '%.2e' % numpy.min(folamphibrisk_out), '%.2e' % numpy.min(folmammrisk_out),
                '%.2e' % numpy.min(barebirdrisk_out), '%.2e' % numpy.min(barereprisk_out), '%.2e' % numpy.min(bareamphibrisk_out), '%.2e' % numpy.min(baremammrisk_out),],

         "Max": ['%.2e' % numpy.max(granbirdderm_out),'%.2e' % numpy.max(granherpderm_out), '%.2e' % numpy.max(granmammderm_out),
                 '%.2e' % numpy.max(folbirdderm_out), '%.2e' % numpy.max(folherpderm_out), '%.2e' % numpy.max(folmammderm_out), 
                 '%.2e' % numpy.max(barebirdderm_out),'%.2e' % numpy.max(bareherpderm_out), '%.2e' % numpy.max(baremammderm_out),
                 '%.2e' % numpy.max(granbirdrisk_out), '%.2e' % numpy.max(granreprisk_out), '%.2e' % numpy.max(granamphibrisk_out), '%.2e' % numpy.max(granmammrisk_out),
                 '%.2e' % numpy.max(folbirdrisk_out), '%.2e' % numpy.max(folreprisk_out), '%.2e' % numpy.max(folamphibrisk_out), '%.2e' % numpy.max(folmammrisk_out),
                 '%.2e' % numpy.max(barebirdrisk_out), '%.2e' % numpy.max(barereprisk_out), '%.2e' % numpy.max(bareamphibrisk_out), '%.2e' % numpy.max(baremammrisk_out),],

        "Unit": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw',
                 '', '', '', '','', '', '', '','', '', '', '',],
    }
    return data

pvuheadings = getheaderpvu()
pvaheadings = getheaderpva()
pvrheadings = getheaderpvr()
pv5headings = getheaderpv5()
pv6headings = getheaderpv6()
pv7headings = getheaderpv7()
pv8headings = getheaderpv8()
pv10headings = getheaderpv10()
pv12headings = getheaderpv12()

sumheadings = getheadersum()

djtemplate = getdjtemplate()
djtemplate_10 = getdjtemplate_10()

tmpl = Template(djtemplate)
tmpl_10 = Template(djtemplate_10)


def table_all(pvuheadings, pvrheadings, tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm, low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):
    table3_out = table_3(pvuheadings, tmpl, ar_lb, frac_pest_surface)
    table4_out = table_4(pvuheadings, tmpl, ar_lb, dislodge_fol_res)
    table5_out = table_5(pvuheadings, tmpl, ar_lb, frac_pest_surface)
    table6_out = table_6(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    table7_out = table_7(pvrheadings, tmpl, ar_lb, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
    table8_out = table_8(pvrheadings, tmpl, ar_lb, frac_pest_surface, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)

    html_all = table_1(pvuheadings, tmpl, chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res)
    html_all = html_all + table_2(pvuheadings, tmpl, bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, 
                         mamm_acute_derm_study,mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw)
    html_all = html_all + table3_out['html']
    html_all = html_all + table4_out['html']
    html_all = html_all + table5_out['html']
    html_all = html_all + table6_out['html']
    html_all = html_all + table7_out['html']
    html_all = html_all + table8_out['html']
    return html_all, table3_out, table4_out, table5_out, table6_out, table7_out, table8_out

def table_sum_input(sumheadings, tmpl, i, ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><td><H3>Summary Statistics (Iterations=%s)</H3></td></tr>
        <tr></tr>
        </table>
        """%(i-1)
        #table sum_input
        tsuminputdata = gettsumdata(ar_lb, frac_pest_surface, dislodge_fol_res, low_bird_acute_ld50, test_bird_bw, mineau, mam_acute_derm_ld50, test_mam_bw)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html

def table_sum_output(granbirdderm_out, granherpderm_out, granmammderm_out, folbirdderm_out, folherpderm_out, folmammderm_out, barebirdderm_out, bareherpderm_out, baremammderm_out, granbirdrisk_out, granreprisk_out, granamphibrisk_out, granmammrisk_out, folbirdrisk_out, folreprisk_out, folamphibrisk_out, folmammrisk_out, barebirdrisk_out, barereprisk_out, bareamphibrisk_out, baremammrisk_out):
        #pre-table sum_input
        html = """
        <br>
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(granbirdderm_out, granherpderm_out, granmammderm_out,
                    folbirdderm_out, folherpderm_out, folmammderm_out,
                    barebirdderm_out, bareherpderm_out, baremammderm_out,
                    granbirdrisk_out, granreprisk_out, granamphibrisk_out, granmammrisk_out,
                    folbirdrisk_out, folreprisk_out, folamphibrisk_out, folmammrisk_out,
                    barebirdrisk_out, barereprisk_out, bareamphibrisk_out, baremammrisk_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        return html

def table_1(chemical_name, Use, Formulated_product_name, percent_ai, Application_type, r_s, b_w, percent_incorporated, density_of_product, Foliar_dissipation_half_life):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs:</H3>
        <div>
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(chemical_name, Use, Formulated_product_name, percent_ai, Application_type, r_s, b_w, percent_incorporated,
                           density_of_product, Foliar_dissipation_half_life)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(noa, rate_out, day_out):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Chemical Application (n=%s)</H4>
                <div class="out_ container_output">
        """ %(noa)
        #table 2
        t2data_all=[]
        for i in range(int(noa)):
            rate_temp=rate_out[i]
            day_temp=day_out[i]
            t2data_temp=gett2data(i+1, rate_temp, day_temp)
            t2data_all.append(t2data_temp)
        t2data = dict([(k,[t2data_ind[k][0] for t2data_ind in t2data_all]) for k in t2data_temp])
        t2rows = gethtmlrowsfromcols(t2data,pvaheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings)))
        html = html + """
                </div>
        """
        return html

def table_3(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, bw_assessed_bird_l, Species_tested_bird, bw_tested_bird, mineau_scaling_factor):
        #pre-table 3
        html = """
            <H4 class="out_3 collapsible" id="section4"><span></span>Toxicity Properties (Avian)</H4>
                <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, 
            bw_assessed_bird_l, Species_tested_bird, bw_tested_bird, mineau_scaling_factor)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_4(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, bw_assessed_mamm_l, bw_tested_mamm):
        #pre-table 4
        html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Toxicity Properties (Mammal)</H4>              <div class="out_ container_output">
        """
        #table 4
        t4data = gett4data(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, 
              bw_assessed_mamm_l, bw_tested_mamm)
        t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_5(Application_type, a_r_p, a_i, den, ld50_bird, aw_bird_sm, tw_bird, x, m_s_r_p, NOAEC_bird, ld50_mamm, aw_mamm_sm, tw_mamm, NOAEL_mamm, aw_bird_md, aw_mamm_md, aw_bird_lg,  aw_mamm_lg):
        #pre-table 5
        html = """
        <H3 class="out_5 collapsible" id="section6"><span></span>Results</H3>
        <div>
        <H3 class="out_">Application Type : %s</H3>
        """%(Application_type)
        #table 5
        sa_bird_1_s=trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird,trex2_model.fi_bird, ld50_bird, aw_bird_sm, tw_bird, x) 
        sa_bird_2_s=trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_sm, tw_bird, x) 
        sc_bird_s=trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird)
        sa_mamm_1_s=trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_sm, tw_mamm)
        sa_mamm_2_s=trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_sm, tw_mamm)
        sc_mamm_s=trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_sm,tw_mamm, trex2_model.ANOAEL_mamm)
        
        sa_bird_1_m=trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird, trex2_model.fi_bird, ld50_bird, aw_bird_md, tw_bird, x) 
        sa_bird_2_m=trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_md, tw_bird, x) 
        sc_bird_m=trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird)
        sa_mamm_1_m=trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_md, tw_mamm)
        sa_mamm_2_m=trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_md, tw_mamm)
        sc_mamm_m=trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_md,tw_mamm, trex2_model.ANOAEL_mamm)
             
        sa_bird_1_l=trex2_model.sa_bird_1(a_r_p, a_i, den, trex2_model.at_bird,trex2_model.fi_bird, ld50_bird, aw_bird_lg, tw_bird, x) 
        sa_bird_2_l=trex2_model.sa_bird_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_bird, ld50_bird, aw_bird_lg, tw_bird, x) 
        sc_bird_l=trex2_model.sc_bird(a_r_p, a_i, den, NOAEC_bird)
        sa_mamm_1_l=trex2_model.sa_mamm_1(a_r_p, a_i, den, trex2_model.at_mamm, trex2_model.fi_mamm, ld50_mamm, aw_mamm_lg, tw_mamm)
        sa_mamm_2_l=trex2_model.sa_mamm_2(a_r_p, a_i, den, m_s_r_p, trex2_model.at_mamm, ld50_mamm, aw_mamm_lg, tw_mamm)
        sc_mamm_l=trex2_model.sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_lg,tw_mamm, trex2_model.ANOAEL_mamm)

        t5data = gett5data(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
                           sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
                           sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l)
        t5rows = gethtmlrowsfromcols(t5data,pv5headings[1])       
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pv5headings[0], sub_headings=pv5headings[2], th_span='4')))
        return html

def table_6(Application_type, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 6
        html = """
            <div class="out_6">
              <H3>Results</H3>
              <H3>Application Type : %s<H3>
              <H4>Dietary based EECs (ppm)<H4>
            </div>
        """%(Application_type)
        #table 6
        EEC_diet_SG=trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_diet_TG=trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_diet_BP=trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_diet_FR=trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_diet_AR=trex2_model.EEC_diet(trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)                       

        t6data = gett6data(EEC_diet_SG, EEC_diet_TG, EEC_diet_BP, EEC_diet_FR, EEC_diet_AR)
        t6rows = gethtmlrowsfromcols(t6data,pv6headings)       
        html = html + tmpl.render(Context(dict(data=t6rows, headings=pv6headings)))
        return html

def table_7(aw_bird_sm, aw_bird_md, aw_bird_lg, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 7
        html = """
            <div class="out_7">
              <H4>Avian Dosed Based EECs<H4>
            </div>
        """
        #table 7
        EEC_dose_bird_SG_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_bird_SG_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_bird_SG_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_bird_TG_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_bird_TG_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_bird_TG_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_bird_BP_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_bird_BP_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_bird_BP_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_bird_FP_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_bird_FP_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_bird_FP_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_bird_AR_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_bird_AR_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_bird_AR_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.9, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_bird_SE_sm=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_sm, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_bird_SE_md=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_md, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_bird_SE_lg=trex2_model.EEC_dose_bird(trex2_model.EEC_diet, aw_bird_lg, trex2_model.fi_bird, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)                     
                      
        t7data = gett7data(EEC_dose_bird_SG_sm, EEC_dose_bird_SG_md, EEC_dose_bird_SG_lg, EEC_dose_bird_TG_sm, EEC_dose_bird_TG_md, EEC_dose_bird_TG_lg, EEC_dose_bird_BP_sm, EEC_dose_bird_BP_md, EEC_dose_bird_BP_lg, EEC_dose_bird_FP_sm, EEC_dose_bird_FP_md, EEC_dose_bird_FP_lg, EEC_dose_bird_AR_sm, EEC_dose_bird_AR_md, EEC_dose_bird_AR_lg, EEC_dose_bird_SE_sm, EEC_dose_bird_SE_md, EEC_dose_bird_SE_lg)
        t7rows = gethtmlrowsfromcols(t7data,pv7headings)       
        html = html + tmpl.render(Context(dict(data=t7rows, headings=pv7headings)))
        return html

def table_8(lc50_bird, NOAEC_bird, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 8
        html = """
            <div class="out_8">
              <H4>Avian Diet Based RQs<H4>
            </div>
        """
        #table 8
        ARQ_diet_bird_SG_A=trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        ARQ_diet_bird_SG_C=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l,day_out)
        ARQ_diet_bird_TG_A=trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l,day_out)
        ARQ_diet_bird_TG_C=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l,day_out)
        ARQ_diet_bird_BP_A=trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        ARQ_diet_bird_BP_C=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        ARQ_diet_bird_FP_A=trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_diet_bird_FP_C=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_diet_bird_AR_A=trex2_model.ARQ_diet_bird(trex2_model.EEC_diet, lc50_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        ARQ_diet_bird_AR_C=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
                      
        t8data = gett8data(ARQ_diet_bird_SG_A, ARQ_diet_bird_SG_C, ARQ_diet_bird_TG_A, ARQ_diet_bird_TG_C, ARQ_diet_bird_BP_A, ARQ_diet_bird_BP_C, ARQ_diet_bird_FP_A, ARQ_diet_bird_FP_C, ARQ_diet_bird_AR_A, ARQ_diet_bird_AR_C)
        t8rows = gethtmlrowsfromcols(t8data,pv8headings)       
        html = html + tmpl.render(Context(dict(data=t8rows, headings=pv8headings)))
        return html

def table_9(aw_mamm_sm, aw_mamm_md, aw_mamm_lg, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 9
        html = """
            <div class="out_9">
              <H4>Mammalian Dose Based EECs (mg/kg-bw)<H4>
            </div>
        """
        #table 9
        EEC_dose_mamm_SG_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_mamm_SG_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_mamm_SG_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        EEC_dose_mamm_TG_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_mamm_TG_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_mamm_TG_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        EEC_dose_mamm_BP_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_mamm_BP_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_mamm_BP_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        EEC_dose_mamm_FP_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_mamm_FP_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_mamm_FP_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_mamm_AR_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_mamm_AR_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_mamm_AR_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        EEC_dose_mamm_SE_sm=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_sm, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_mamm_SE_md=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_md, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        EEC_dose_mamm_SE_lg=trex2_model.EEC_dose_mamm(trex2_model.EEC_diet, aw_mamm_lg, trex2_model.fi_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
                      
        t9data = gett9data(EEC_dose_mamm_SG_sm,EEC_dose_mamm_SG_md,EEC_dose_mamm_SG_lg,EEC_dose_mamm_TG_sm,EEC_dose_mamm_TG_md,EEC_dose_mamm_TG_lg,EEC_dose_mamm_BP_sm,EEC_dose_mamm_BP_md,EEC_dose_mamm_BP_lg,EEC_dose_mamm_FP_sm,EEC_dose_mamm_FP_md,EEC_dose_mamm_FP_lg,EEC_dose_mamm_AR_sm,EEC_dose_mamm_AR_md,EEC_dose_mamm_AR_lg,EEC_dose_mamm_SE_sm,EEC_dose_mamm_SE_md,EEC_dose_mamm_SE_lg)
        t9rows = gethtmlrowsfromcols(t9data,pv7headings)       
        html = html + tmpl.render(Context(dict(data=t9rows, headings=pv7headings)))
        return html

def table_10(aw_mamm_sm, aw_mamm_md, aw_mamm_lg, ld50_mamm, NOAEL_mamm, tw_mamm, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 10
        html = """
            <div class="out_10">
              <H4>Mammalian Dose Based EECs (mg/kg-bw)<H4>
            </div>
        """
        #table 10
        ARQ_dose_mamm_SG_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        CRQ_dose_mamm_SG_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out)
        ARQ_dose_mamm_SG_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        CRQ_dose_mamm_SG_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out)
        ARQ_dose_mamm_SG_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        CRQ_dose_mamm_SG_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out)
        
        ARQ_dose_mamm_TG_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        CRQ_dose_mamm_TG_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out)
        ARQ_dose_mamm_TG_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        CRQ_dose_mamm_TG_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out)
        ARQ_dose_mamm_TG_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        CRQ_dose_mamm_TG_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out)
        
        ARQ_dose_mamm_BP_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        CRQ_dose_mamm_BP_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out)
        ARQ_dose_mamm_BP_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        CRQ_dose_mamm_BP_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out)
        ARQ_dose_mamm_BP_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        CRQ_dose_mamm_BP_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out)
        
        ARQ_dose_mamm_FP_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_FP_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_dose_mamm_FP_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_FP_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_dose_mamm_FP_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_FP_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out)
        
        ARQ_dose_mamm_AR_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        CRQ_dose_mamm_AR_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out)
        ARQ_dose_mamm_AR_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        CRQ_dose_mamm_AR_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out)
        ARQ_dose_mamm_AR_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        CRQ_dose_mamm_AR_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out)
        
        ARQ_dose_mamm_SE_sm=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_SE_sm=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_dose_mamm_SE_md=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_SE_md=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_dose_mamm_SE_lg=trex2_model.ARQ_dose_mamm(trex2_model.EEC_dose_mamm, trex2_model.at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.1, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_dose_mamm_SE_lg=trex2_model.CRQ_dose_mamm(trex2_model.EEC_diet, trex2_model.EEC_dose_mamm, trex2_model.ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out)
                      
        t10data = gett10data(ARQ_dose_mamm_SG_sm,CRQ_dose_mamm_SG_sm,ARQ_dose_mamm_SG_md,CRQ_dose_mamm_SG_md,ARQ_dose_mamm_SG_lg,CRQ_dose_mamm_SG_lg,ARQ_dose_mamm_TG_sm,CRQ_dose_mamm_TG_sm,ARQ_dose_mamm_TG_md,CRQ_dose_mamm_TG_md,ARQ_dose_mamm_TG_lg,CRQ_dose_mamm_TG_lg,ARQ_dose_mamm_BP_sm,CRQ_dose_mamm_BP_sm,ARQ_dose_mamm_BP_md,CRQ_dose_mamm_BP_md,ARQ_dose_mamm_BP_lg,CRQ_dose_mamm_BP_lg,ARQ_dose_mamm_FP_sm,CRQ_dose_mamm_FP_sm,ARQ_dose_mamm_FP_md,CRQ_dose_mamm_FP_md,ARQ_dose_mamm_FP_lg,CRQ_dose_mamm_FP_lg,ARQ_dose_mamm_AR_sm,CRQ_dose_mamm_AR_sm,ARQ_dose_mamm_AR_md,CRQ_dose_mamm_AR_md,ARQ_dose_mamm_AR_lg,CRQ_dose_mamm_AR_lg,ARQ_dose_mamm_SE_sm,CRQ_dose_mamm_SE_sm,ARQ_dose_mamm_SE_md,CRQ_dose_mamm_SE_md,ARQ_dose_mamm_SE_lg,CRQ_dose_mamm_SE_lg)
        t10rows = gethtmlrowsfromcols(t10data, pv10headings)       
        html = html + tmpl_10.render(Context(dict(data=t10rows)))
        return html




def table_11(lc50_mamm, NOAEC_bird, n_a, rate_out, a_i, h_l, day_out):
        #pre-table 11
        html = """
            <div class="out_11">
              <H4>Mammalian Dietary Based RQs (mg/kg-bw)<H4>
            </div>
        """
        #table 11
        ARQ_diet_mamm_SG=trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        CRQ_diet_bird_SG=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 240, h_l, day_out)
        ARQ_diet_mamm_TG=trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        CRQ_diet_bird_TG=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 110, h_l, day_out)
        ARQ_diet_mamm_BP=trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        CRQ_diet_bird_BP=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 135, h_l, day_out)
        ARQ_diet_mamm_FP=trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        CRQ_diet_bird_FP=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 15, h_l, day_out)
        ARQ_diet_mamm_AR=trex2_model.ARQ_diet_mamm(trex2_model.EEC_diet, lc50_mamm, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
        CRQ_diet_bird_AR=trex2_model.CRQ_diet_bird(trex2_model.EEC_diet, NOAEC_bird, trex2_model.C_0, n_a, rate_out, a_i, 94, h_l, day_out)
  
        t11data = gett11data(ARQ_diet_mamm_SG,CRQ_diet_bird_SG,ARQ_diet_mamm_TG,CRQ_diet_bird_TG,ARQ_diet_mamm_BP,CRQ_diet_bird_BP,ARQ_diet_mamm_FP,CRQ_diet_bird_FP,ARQ_diet_mamm_AR,CRQ_diet_bird_AR)
        t11rows = gethtmlrowsfromcols(t11data,pv8headings)       
        html = html + tmpl.render(Context(dict(data=t11rows, headings=pv8headings)))
        return html


def table_12(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x):
        #pre-table 12
        html = """
            <div class="out_12">
              <H4>LD50ft-2(mg/kg-bw)<H4>
            </div>
        """
        #table 12
        LD50_rg_bird_sm=trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_sm, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rg_mamm_sm=trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_sm, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_rg_bird_md=trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_md, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rg_mamm_md=trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_md, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_rg_bird_lg=trex2_model.LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_lg, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rg_mamm_lg=trex2_model.LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_lg, trex2_model.at_mamm, ld50_mamm, tw_mamm)

        t12data = gett12data(LD50_rg_bird_sm,LD50_rg_mamm_sm,LD50_rg_bird_md,LD50_rg_mamm_md,LD50_rg_bird_lg,LD50_rg_mamm_lg)
        t12rows = gethtmlrowsfromcols(t12data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t12rows, headings=pv12headings)))
        return html

def table_13(Application_type, rate_out, a_i, p_i, b_w, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x):
        #pre-table 13
        html = """
            <div class="out_13">
              <H4>LD50ft-2(mg/kg-bw)<H4>
            </div>
        """
        #table 13
        LD50_rl_bird_sm=trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_sm, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rl_mamm_sm=trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_sm, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_rl_bird_md=trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_md, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rl_mamm_md=trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_md, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_rl_bird_lg=trex2_model.LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_lg, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_rl_mamm_lg=trex2_model.LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_lg, trex2_model.at_mamm, ld50_mamm, tw_mamm)

        t13data = gett12data(LD50_rl_bird_sm,LD50_rl_mamm_sm,LD50_rl_bird_md,LD50_rl_mamm_md,LD50_rl_bird_lg,LD50_rl_mamm_lg)
        t13rows = gethtmlrowsfromcols(t13data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t13rows, headings=pv12headings)))
        return html

def table_14(Application_type, rate_out, a_i, p_i, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x):
        #pre-table 14
        html = """
            <div class="out_14">
              <H4>LD50ft-2(mg/kg-bw)<H4>
            </div>
        """
        #table 14
        LD50_bg_bird_sm=trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bg_mamm_sm=trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_bg_bird_md=trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bg_mamm_md=trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_bg_bird_lg=trex2_model.LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bg_mamm_lg=trex2_model.LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, trex2_model.at_mamm, ld50_mamm, tw_mamm)

        t14data = gett12data(LD50_bg_bird_sm,LD50_bg_mamm_sm,LD50_bg_bird_md,LD50_bg_mamm_md,LD50_bg_bird_lg,LD50_bg_mamm_lg)
        t14rows = gethtmlrowsfromcols(t14data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t14rows, headings=pv12headings)))
        return html

def table_15(Application_type, rate_out, a_i, p_i, aw_bird_sm, aw_mamm_sm, aw_bird_md, aw_mamm_md, aw_bird_lg, aw_mamm_lg, ld50_bird, ld50_mamm, tw_bird, tw_mamm, x):
        #pre-table 15
        html = """
            <div class="out_15">
              <H4>LD50ft-2(mg/kg-bw)<H4>
            </div>
        """
        #table 15
        LD50_bl_bird_sm=trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bl_mamm_sm=trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_bl_bird_md=trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bl_mamm_md=trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, trex2_model.at_mamm, ld50_mamm, tw_mamm)
        LD50_bl_bird_lg=trex2_model.LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, trex2_model.at_bird, ld50_bird, tw_bird, x)
        LD50_bl_mamm_lg=trex2_model.LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, trex2_model.at_mamm, ld50_mamm, tw_mamm)

        t15data = gett12data(LD50_bl_bird_sm,LD50_bl_mamm_sm,LD50_bl_bird_md,LD50_bl_mamm_md,LD50_bl_bird_lg,LD50_bl_mamm_lg)
        t15rows = gethtmlrowsfromcols(t15data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t15rows, headings=pv12headings)))
        return html
