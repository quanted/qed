import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from therps import therps_model

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpv5():
    headings_l = ["LC50 (ppm)",],
    headings = ["LC50", "EEC_BP", "ARQ_BP", "EEC_FR", "ARQ_FR", "EEC_HM", "ARQ_HM", "EEC_IM", "ARQ_IM", "EEC_TP", "ARQ_TP"]
    return headings_l, headings

def getheaderpv6():
    headings_l = ["NOAEC (ppm)",],
    headings = ["NOAEC", "EEC_BP", "CRQ_BP", "EEC_FR", "CRQ_FR", "EEC_HM", "CRQ_HM", "EEC_IM", "CRQ_IM", "EEC_TP", "CRQ_TP"]
    return headings_l, headings

def getheaderpv7():
    headings_l = ["Size Class (g)", "Adjusted LD50", ],
    headings = ["Size", "LD50_AD", "EEC_BP", "ARQ_BP", "EEC_FR", "ARQ_FR", "EEC_HM", "ARQ_HM", "EEC_IM", "ARQ_IM", "EEC_TP", "ARQ_TP"]
    return headings_l, headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def getheaderpv5_sum():
    headings_l = ["Metric",],
    headings = ["Metric", "EEC_BP", "ARQ_BP", "EEC_FR", "ARQ_FR", "EEC_HM", "ARQ_HM", "EEC_IM", "ARQ_IM", "EEC_TP", "ARQ_TP"]
    return headings_l, headings

def getheaderpv7_sum():
    headings_l = ["Size Class (g)", "Metric", "Weight (g)", "Adjusted LD50", ],
    headings = ["Size class", "Metric", "Size", "LD50_AD", "EEC_BP", "ARQ_BP", "EEC_FR", "ARQ_FR", "EEC_HM", "ARQ_HM", "EEC_IM", "ARQ_IM", "EEC_TP", "ARQ_TP"]
    return headings_l, headings


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

def getdjtemplate_5():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
        {% for l_heading in l_headings %}
            <th rowspan="3">{{ l_heading }}</th>
        {% endfor %}
            <th colspan="10">EECs and RQs</th>
        </tr>
        <tr>
            <th colspan="2">Broadleaf Plants/Small Insects</th>
            <th colspan="2">Fruits/Pods/Seeds/Large Insects</th>
            <th colspan="2">Small Herbivore Mammals</th>
            <th colspan="2">Small Insectivore Mammals</th>
            <th colspan="2">Small Amphibians</th>
        </tr>
        <tr>
            <th scope="col">EEC</th>       
            <th scope="col">RQ</th> 
            <th scope="col">EEC</th> 
            <th scope="col">RQ</th>  
            <th scope="col">EEC</th> 
            <th scope="col">RQ</th>
            <th scope="col">EEC</th> 
            <th scope="col">RQ</th>  
            <th scope="col">EEC</th> 
            <th scope="col">RQ</th>
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

def gett1data(chemical_name, Use, Formulated_product_name, percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate):
    data = { 
        "Parameter": ['Chemical Name', 'Use', 'Formulated product name', 'Percentage active ingredient', 'Foliar dissipation half-life', 'Number of applications',
                      'Interval between applications', 'Application rate',],
        "Value": ['%s' % chemical_name, '%s' % Use, '%s' % Formulated_product_name, '%s' % percent_ai, '%s' % Foliar_dissipation_half_life, '%s' % number_of_applications, 
                  '%s' % interval_between_applications, '%s' % application_rate,],
        "Units": ['', '', '', '%', 'days', '', 'days', 'lbs a.i./A',],
    }
    return data

def gett2data(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, Species_of_the_tested_bird, body_weight_of_the_tested_bird, mineau_scaling_factor):
    data = { 
        "Parameter": ['Avian LD50', 'Avian LC50', 'Avian NOAEC', 'Avian NOAEL', 'Species of the tested bird', 'Body weight of the tested bird', 'Mineau scaling factor', ],
        "Value": ['%s' % avian_ld50, '%s' % avian_lc50, '%s' % avian_NOAEC, '%s' % avian_NOAEL, '%s' % Species_of_the_tested_bird, '%s' % body_weight_of_the_tested_bird, '%s' % mineau_scaling_factor,],
        "Units": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', '', 'g', '',],
    }
    return data

def gett3data(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a):
    data = { 
        "Parameter": ['Body weight of assessed small herptile', 'Body weight of assessed medium herptile', 'Body weight of assessed large herptile', 
                      "Water content of the assessed small herptile's diet", "Water content of the assessed medium herptile's diet", "Water content of the assessed large herptile's diet", 
                      'Weight of the mammal consumed by assessed frog', 'Weight of the herptile consumed by assessed frog', ],
        "Value": ['%s' % bw_herp_a_sm, '%s' % bw_herp_a_md, '%s' % bw_herp_a_lg, '%s' % wp_herp_a_sm, '%s' % wp_herp_a_md, '%s' % wp_herp_a_lg, '%s' % c_mamm_a, '%s' % c_herp_a,],
        "Units": ['g', 'g', 'g', '%', '%', '%', 'g', 'g',],
    }
    return data

def gett5data(lc50_bird, EEC_diet_herp_BL, EEC_ARQ_herp_BL, EEC_diet_herp_FR, EEC_ARQ_herp_FR, EEC_diet_herp_HM, EEC_ARQ_herp_HM, EEC_diet_herp_IM, EEC_ARQ_herp_IM, EEC_diet_herp_TP, EEC_ARQ_herp_TP):
    data = { 
        "LC50":   ['%0.2E' % lc50_bird,],
        "EEC_BP": ['%0.2E' % EEC_diet_herp_BL,],
        "ARQ_BP":  ['%0.2E' % EEC_ARQ_herp_BL,],
        "EEC_FR": ['%0.2E' % EEC_diet_herp_FR,], 
        "ARQ_FR":  ['%0.2E' % EEC_ARQ_herp_FR,], 
        "EEC_HM": ['%0.2E' % EEC_diet_herp_HM,],
        "ARQ_HM":  ['%0.2E' % EEC_ARQ_herp_HM,],
        "EEC_IM": ['%0.2E' % EEC_diet_herp_IM,],
        "ARQ_IM":  ['%0.2E' % EEC_ARQ_herp_IM,],
        "EEC_TP": ['%0.2E' % EEC_diet_herp_TP,],
        "ARQ_TP":  ['%0.2E' % EEC_ARQ_herp_TP,],
    }
    return data

def gett6data(NOAEC_bird, EEC_diet_herp_BL, EEC_CRQ_herp_BL, EEC_diet_herp_FR, EEC_CRQ_herp_FR, EEC_diet_herp_HM, EEC_CRQ_herp_HM, EEC_diet_herp_IM, EEC_CRQ_herp_IM, EEC_diet_herp_TP, EEC_CRQ_herp_TP):
    data = { 
        "NOAEC":   ['%0.2E' % NOAEC_bird,],
        "EEC_BP": ['%0.2E' % EEC_diet_herp_BL,],
        "CRQ_BP":  ['%0.2E' % EEC_CRQ_herp_BL,],
        "EEC_FR": ['%0.2E' % EEC_diet_herp_FR,], 
        "CRQ_FR":  ['%0.2E' % EEC_CRQ_herp_FR,], 
        "EEC_HM": ['%0.2E' % EEC_diet_herp_HM,],
        "CRQ_HM":  ['%0.2E' % EEC_CRQ_herp_HM,],
        "EEC_IM": ['%0.2E' % EEC_diet_herp_IM,],
        "CRQ_IM":  ['%0.2E' % EEC_CRQ_herp_IM,],
        "EEC_TP": ['%0.2E' % EEC_diet_herp_TP,],
        "CRQ_TP":  ['%0.2E' % EEC_CRQ_herp_TP,],
    }
    return data

def gett7data(LD50_AD_sm, LD50_AD_md, LD50_AD_lg,
              EEC_dose_BP_sm, EEC_dose_BP_md, EEC_dose_BP_lg, ARQ_dose_BP_sm, ARQ_dose_BP_md, ARQ_dose_BP_lg,
              EEC_dose_FR_sm, EEC_dose_FR_md, EEC_dose_FR_lg, ARQ_dose_FR_sm, ARQ_dose_FR_md, ARQ_dose_FR_lg,
              EEC_dose_HM_md, EEC_dose_HM_lg, ARQ_dose_HM_md, ARQ_dose_HM_lg,
              EEC_dose_IM_md, EEC_dose_IM_lg, ARQ_dose_IM_md, ARQ_dose_IM_lg,
              EEC_dose_TP_md, EEC_dose_TP_lg, ARQ_dose_TP_md, ARQ_dose_TP_lg):
    data = { 
        "Size": ['1.4', '37', '238', ],
        "LD50_AD": ['%0.2E' % LD50_AD_sm, '%0.2E' % LD50_AD_md, '%0.2E' % LD50_AD_lg,],
        "EEC_BP": ['%0.2E' % EEC_dose_BP_sm, '%0.2E' % EEC_dose_BP_md, '%0.2E' % EEC_dose_BP_lg,],
        "ARQ_BP": ['%0.2E' % ARQ_dose_BP_sm, '%0.2E' % ARQ_dose_BP_md, '%0.2E' % ARQ_dose_BP_lg,],
        "EEC_FR": ['%0.2E' % EEC_dose_FR_sm, '%0.2E' % EEC_dose_FR_md, '%0.2E' % EEC_dose_FR_lg,],
        "ARQ_FR": ['%0.2E' % ARQ_dose_FR_sm, '%0.2E' % ARQ_dose_FR_md, '%0.2E' % ARQ_dose_FR_lg,],
        "EEC_HM": ['N/A', '%0.2E' % EEC_dose_HM_md, '%0.2E' % EEC_dose_HM_lg,],
        "ARQ_HM": ['N/A', '%0.2E' % ARQ_dose_HM_md, '%0.2E' % ARQ_dose_HM_lg,],
        "EEC_IM": ['N/A', '%0.2E' % EEC_dose_IM_md, '%0.2E' % EEC_dose_IM_lg,],
        "ARQ_IM": ['N/A', '%0.2E' % ARQ_dose_IM_md, '%0.2E' % ARQ_dose_IM_lg,],
        "EEC_TP": ['N/A', '%0.2E' % EEC_dose_TP_md, '%0.2E' % EEC_dose_TP_lg,],
        "ARQ_TP": ['N/A', '%0.2E' % ARQ_dose_TP_md, '%0.2E' % ARQ_dose_TP_lg,],
    }
    return data


def gettsumdata_1(percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate):
    data = { 
        "Parameter": ['Percentage active ingredient', 'Foliar dissipation half-life', 'Number of applications',
                      'Interval between applications', 'Application rate',],
        "Mean": ['%.2e' % numpy.mean(percent_ai),'%.2e' % numpy.mean(Foliar_dissipation_half_life),'%.2e' % numpy.mean(number_of_applications), '%.2e' % numpy.mean(interval_between_applications), '%.2e' % numpy.mean(application_rate),],
        "Std": ['%.2e' % numpy.std(percent_ai),'%.2e' % numpy.std(Foliar_dissipation_half_life),'%.2e' % numpy.std(number_of_applications), '%.2e' % numpy.std(interval_between_applications), '%.2e' % numpy.std(application_rate),],
        "Min": ['%.2e' % numpy.min(percent_ai),'%.2e' % numpy.min(Foliar_dissipation_half_life),'%.2e' % numpy.min(number_of_applications), '%.2e' % numpy.min(interval_between_applications), '%.2e' % numpy.min(application_rate),],
        "Max": ['%.2e' % numpy.max(percent_ai),'%.2e' % numpy.max(Foliar_dissipation_half_life),'%.2e' % numpy.max(number_of_applications), '%.2e' % numpy.max(interval_between_applications), '%.2e' % numpy.max(application_rate),],
        "Unit": ['%', 'days', '', 'days', 'lbs a.i./A',],
    }
    return data

def gettsumdata_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, body_weight_of_the_tested_bird, mineau_scaling_factor):
    data = { 
        "Parameter": ['Avian LD50', 'Avian LC50', 'Avian NOAEC', 'Avian NOAEL', 'Body weight of the tested bird', 'Mineau scaling factor',],
        "Mean": ['%.2e' % numpy.mean(avian_ld50),'%.2e' % numpy.mean(avian_lc50),'%.2e' % numpy.mean(avian_NOAEC), '%.2e' % numpy.mean(avian_NOAEL), '%.2e' % numpy.mean(body_weight_of_the_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor),],
        "Std": ['%.2e' % numpy.std(avian_ld50),'%.2e' % numpy.std(avian_lc50),'%.2e' % numpy.std(avian_NOAEC), '%.2e' % numpy.std(avian_NOAEL), '%.2e' % numpy.std(body_weight_of_the_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor),],
        "Min": ['%.2e' % numpy.min(avian_ld50),'%.2e' % numpy.min(avian_lc50),'%.2e' % numpy.min(avian_NOAEC), '%.2e' % numpy.min(avian_NOAEL), '%.2e' % numpy.min(body_weight_of_the_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor),],
        "Max": ['%.2e' % numpy.max(avian_ld50),'%.2e' % numpy.max(avian_lc50),'%.2e' % numpy.max(avian_NOAEC), '%.2e' % numpy.max(avian_NOAEL), '%.2e' % numpy.max(body_weight_of_the_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor),],
        "Unit": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', 'g', '',],
    }
    return data

def gettsumdata_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a):
    data = { 
        "Parameter": ['Body weight of assessed small herptile', 'Body weight of assessed medium herptile', 'Body weight of assessed large herptile', "Water content of the assessed small herptile's diet", "Water content of the assessed medium herptile's diet", "Water content of the assessed large herptile's diet", 'Weight of the mammal consumed by assessed frog', 'Weight of the herptile consumed by assessed frog',],
        "Mean": ['%.2e' % numpy.mean(bw_herp_a_sm),'%.2e' % numpy.mean(bw_herp_a_md),'%.2e' % numpy.mean(bw_herp_a_lg), '%.2e' % numpy.mean(wp_herp_a_sm), '%.2e' % numpy.mean(wp_herp_a_md), '%.2e' % numpy.mean(wp_herp_a_lg), '%.2e' % numpy.mean(c_mamm_a), '%.2e' % numpy.mean(c_herp_a)],
        "Std": ['%.2e' % numpy.std(bw_herp_a_sm),'%.2e' % numpy.std(bw_herp_a_md),'%.2e' % numpy.std(bw_herp_a_lg), '%.2e' % numpy.std(wp_herp_a_sm), '%.2e' % numpy.std(wp_herp_a_md), '%.2e' % numpy.mean(wp_herp_a_lg), '%.2e' % numpy.mean(c_mamm_a), '%.2e' % numpy.mean(c_herp_a)],
        "Min": ['%.2e' % numpy.min(bw_herp_a_sm),'%.2e' % numpy.min(bw_herp_a_md),'%.2e' % numpy.min(bw_herp_a_lg), '%.2e' % numpy.min(wp_herp_a_sm), '%.2e' % numpy.min(wp_herp_a_md), '%.2e' % numpy.mean(wp_herp_a_lg), '%.2e' % numpy.mean(c_mamm_a), '%.2e' % numpy.mean(c_herp_a)],
        "Max": ['%.2e' % numpy.max(bw_herp_a_sm),'%.2e' % numpy.max(bw_herp_a_md),'%.2e' % numpy.max(bw_herp_a_lg), '%.2e' % numpy.max(wp_herp_a_sm), '%.2e' % numpy.max(wp_herp_a_md), '%.2e' % numpy.mean(wp_herp_a_lg), '%.2e' % numpy.mean(c_mamm_a), '%.2e' % numpy.mean(c_herp_a)],
        "Unit": ['g', 'g', 'g', '%', '%', '%', 'g', 'g',],
    }
    return data

def gettsumdata_5(EEC_diet_herp_BL_out, EEC_ARQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_ARQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_ARQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_ARQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_ARQ_herp_TP_out):
    data = { 
        "Metric":   ['Mean', 'Std', 'Min', 'Max',],
        "EEC_BP": ['%.2e' % numpy.mean(EEC_diet_herp_BL_out), '%.2e' % numpy.std(EEC_diet_herp_BL_out), '%.2e' % numpy.min(EEC_diet_herp_BL_out), '%.2e' % numpy.max(EEC_diet_herp_BL_out)],
        "ARQ_BP": ['%.2e' % numpy.mean(EEC_ARQ_herp_BL_out), '%.2e' % numpy.std(EEC_ARQ_herp_BL_out), '%.2e' % numpy.min(EEC_ARQ_herp_BL_out), '%.2e' % numpy.max(EEC_ARQ_herp_BL_out)],
        "EEC_FR": ['%.2e' % numpy.mean(EEC_diet_herp_FR_out), '%.2e' % numpy.std(EEC_diet_herp_FR_out), '%.2e' % numpy.min(EEC_diet_herp_FR_out), '%.2e' % numpy.max(EEC_diet_herp_FR_out)],
        "ARQ_FR": ['%.2e' % numpy.mean(EEC_ARQ_herp_FR_out), '%.2e' % numpy.std(EEC_ARQ_herp_FR_out), '%.2e' % numpy.min(EEC_ARQ_herp_FR_out), '%.2e' % numpy.max(EEC_ARQ_herp_FR_out)],
        "EEC_HM": ['%.2e' % numpy.mean(EEC_diet_herp_HM_out), '%.2e' % numpy.std(EEC_diet_herp_HM_out), '%.2e' % numpy.min(EEC_diet_herp_HM_out), '%.2e' % numpy.max(EEC_diet_herp_HM_out)],
        "ARQ_HM": ['%.2e' % numpy.mean(EEC_ARQ_herp_HM_out), '%.2e' % numpy.std(EEC_ARQ_herp_HM_out), '%.2e' % numpy.min(EEC_ARQ_herp_HM_out), '%.2e' % numpy.max(EEC_ARQ_herp_HM_out)],
        "EEC_IM": ['%.2e' % numpy.mean(EEC_diet_herp_IM_out), '%.2e' % numpy.std(EEC_diet_herp_IM_out), '%.2e' % numpy.min(EEC_diet_herp_IM_out), '%.2e' % numpy.max(EEC_diet_herp_IM_out)],
        "ARQ_IM": ['%.2e' % numpy.mean(EEC_ARQ_herp_IM_out), '%.2e' % numpy.std(EEC_ARQ_herp_IM_out), '%.2e' % numpy.min(EEC_ARQ_herp_IM_out), '%.2e' % numpy.max(EEC_ARQ_herp_IM_out)],
        "EEC_TP": ['%.2e' % numpy.mean(EEC_diet_herp_TP_out), '%.2e' % numpy.std(EEC_diet_herp_TP_out), '%.2e' % numpy.min(EEC_diet_herp_TP_out), '%.2e' % numpy.max(EEC_diet_herp_TP_out)],
        "ARQ_TP": ['%.2e' % numpy.mean(EEC_ARQ_herp_TP_out), '%.2e' % numpy.std(EEC_ARQ_herp_TP_out), '%.2e' % numpy.min(EEC_ARQ_herp_TP_out), '%.2e' % numpy.max(EEC_ARQ_herp_TP_out)],
    }
    return data

def gettsumdata_6(EEC_diet_herp_BL_out, EEC_CRQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_CRQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_CRQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_CRQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_CRQ_herp_TP_out):
    data = { 
        "Metric":   ['Mean', 'Std', 'Min', 'Max',],
        "EEC_BP": ['%.2e' % numpy.mean(EEC_diet_herp_BL_out), '%.2e' % numpy.std(EEC_diet_herp_BL_out), '%.2e' % numpy.min(EEC_diet_herp_BL_out), '%.2e' % numpy.max(EEC_diet_herp_BL_out)],
        "ARQ_BP": ['%.2e' % numpy.mean(EEC_CRQ_herp_BL_out), '%.2e' % numpy.std(EEC_CRQ_herp_BL_out), '%.2e' % numpy.min(EEC_CRQ_herp_BL_out), '%.2e' % numpy.max(EEC_CRQ_herp_BL_out)],
        "EEC_FR": ['%.2e' % numpy.mean(EEC_diet_herp_FR_out), '%.2e' % numpy.std(EEC_diet_herp_FR_out), '%.2e' % numpy.min(EEC_diet_herp_FR_out), '%.2e' % numpy.max(EEC_diet_herp_FR_out)],
        "ARQ_FR": ['%.2e' % numpy.mean(EEC_CRQ_herp_FR_out), '%.2e' % numpy.std(EEC_CRQ_herp_FR_out), '%.2e' % numpy.min(EEC_CRQ_herp_FR_out), '%.2e' % numpy.max(EEC_CRQ_herp_FR_out)],
        "EEC_HM": ['%.2e' % numpy.mean(EEC_diet_herp_HM_out), '%.2e' % numpy.std(EEC_diet_herp_HM_out), '%.2e' % numpy.min(EEC_diet_herp_HM_out), '%.2e' % numpy.max(EEC_diet_herp_HM_out)],
        "ARQ_HM": ['%.2e' % numpy.mean(EEC_CRQ_herp_HM_out), '%.2e' % numpy.std(EEC_CRQ_herp_HM_out), '%.2e' % numpy.min(EEC_CRQ_herp_HM_out), '%.2e' % numpy.max(EEC_CRQ_herp_HM_out)],
        "EEC_IM": ['%.2e' % numpy.mean(EEC_diet_herp_IM_out), '%.2e' % numpy.std(EEC_diet_herp_IM_out), '%.2e' % numpy.min(EEC_diet_herp_IM_out), '%.2e' % numpy.max(EEC_diet_herp_IM_out)],
        "ARQ_IM": ['%.2e' % numpy.mean(EEC_CRQ_herp_IM_out), '%.2e' % numpy.std(EEC_CRQ_herp_IM_out), '%.2e' % numpy.min(EEC_CRQ_herp_IM_out), '%.2e' % numpy.max(EEC_CRQ_herp_IM_out)],
        "EEC_TP": ['%.2e' % numpy.mean(EEC_diet_herp_TP_out), '%.2e' % numpy.std(EEC_diet_herp_TP_out), '%.2e' % numpy.min(EEC_diet_herp_TP_out), '%.2e' % numpy.max(EEC_diet_herp_TP_out)],
        "ARQ_TP": ['%.2e' % numpy.mean(EEC_CRQ_herp_TP_out), '%.2e' % numpy.std(EEC_CRQ_herp_TP_out), '%.2e' % numpy.min(EEC_CRQ_herp_TP_out), '%.2e' % numpy.max(EEC_CRQ_herp_TP_out)],
    }
    return data

def gettsumdata_7(bw_herp_a_sm_out, bw_herp_a_md_out, bw_herp_a_lg_out, LD50_AD_sm_out, LD50_AD_md_out, LD50_AD_lg_out,
                  EEC_dose_BP_sm_out, EEC_dose_BP_md_out, EEC_dose_BP_lg_out, ARQ_dose_BP_sm_out, ARQ_dose_BP_md_out, ARQ_dose_BP_lg_out,
                  EEC_dose_FR_sm_out, EEC_dose_FR_md_out, EEC_dose_FR_lg_out, ARQ_dose_FR_sm_out, ARQ_dose_FR_md_out, ARQ_dose_FR_lg_out,
                  EEC_dose_HM_md_out, EEC_dose_HM_lg_out, ARQ_dose_HM_md_out, ARQ_dose_HM_lg_out,
                  EEC_dose_IM_md_out, EEC_dose_IM_lg_out, ARQ_dose_IM_md_out, ARQ_dose_IM_lg_out,
                  EEC_dose_TP_md_out, EEC_dose_TP_lg_out, ARQ_dose_TP_md_out, ARQ_dose_TP_lg_out):
    data = { 
        "Size class": ['Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large'],
        "Metric":  ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Size":    ['%.2e' % numpy.mean(bw_herp_a_sm_out), '%.2e' % numpy.std(bw_herp_a_sm_out), '%.2e' % numpy.min(bw_herp_a_sm_out), '%.2e' % numpy.max(bw_herp_a_sm_out),
                    '%.2e' % numpy.mean(bw_herp_a_md_out), '%.2e' % numpy.std(bw_herp_a_md_out), '%.2e' % numpy.min(bw_herp_a_md_out), '%.2e' % numpy.max(bw_herp_a_md_out),
                    '%.2e' % numpy.mean(bw_herp_a_lg_out), '%.2e' % numpy.std(bw_herp_a_lg_out), '%.2e' % numpy.min(bw_herp_a_lg_out), '%.2e' % numpy.max(bw_herp_a_lg_out),],
        "LD50_AD": ['%.2e' % numpy.mean(LD50_AD_sm_out), '%.2e' % numpy.std(LD50_AD_sm_out), '%.2e' % numpy.min(LD50_AD_sm_out), '%.2e' % numpy.max(LD50_AD_sm_out),
                    '%.2e' % numpy.mean(LD50_AD_md_out), '%.2e' % numpy.std(LD50_AD_md_out), '%.2e' % numpy.min(LD50_AD_md_out), '%.2e' % numpy.max(LD50_AD_md_out),
                    '%.2e' % numpy.mean(LD50_AD_lg_out), '%.2e' % numpy.std(LD50_AD_lg_out), '%.2e' % numpy.min(LD50_AD_lg_out), '%.2e' % numpy.max(LD50_AD_lg_out),],
        "EEC_BP":  ['%.2e' % numpy.mean(EEC_dose_BP_sm_out), '%.2e' % numpy.std(EEC_dose_BP_sm_out), '%.2e' % numpy.min(EEC_dose_BP_sm_out), '%.2e' % numpy.max(EEC_dose_BP_sm_out),
                    '%.2e' % numpy.mean(EEC_dose_BP_md_out), '%.2e' % numpy.std(EEC_dose_BP_md_out), '%.2e' % numpy.min(EEC_dose_BP_md_out), '%.2e' % numpy.max(EEC_dose_BP_md_out),
                    '%.2e' % numpy.mean(EEC_dose_BP_lg_out), '%.2e' % numpy.std(EEC_dose_BP_lg_out), '%.2e' % numpy.min(EEC_dose_BP_lg_out), '%.2e' % numpy.max(EEC_dose_BP_lg_out),],
        "ARQ_BP":  ['%.2e' % numpy.mean(ARQ_dose_BP_sm_out), '%.2e' % numpy.std(ARQ_dose_BP_sm_out), '%.2e' % numpy.min(ARQ_dose_BP_sm_out), '%.2e' % numpy.max(ARQ_dose_BP_sm_out),
                    '%.2e' % numpy.mean(ARQ_dose_BP_md_out), '%.2e' % numpy.std(ARQ_dose_BP_md_out), '%.2e' % numpy.min(ARQ_dose_BP_md_out), '%.2e' % numpy.max(ARQ_dose_BP_md_out),
                    '%.2e' % numpy.mean(ARQ_dose_BP_lg_out), '%.2e' % numpy.std(ARQ_dose_BP_lg_out), '%.2e' % numpy.min(ARQ_dose_BP_lg_out), '%.2e' % numpy.max(ARQ_dose_BP_lg_out),],
        "EEC_FR":  ['%.2e' % numpy.mean(EEC_dose_FR_sm_out), '%.2e' % numpy.std(EEC_dose_FR_sm_out), '%.2e' % numpy.min(EEC_dose_FR_sm_out), '%.2e' % numpy.max(EEC_dose_FR_sm_out),
                    '%.2e' % numpy.mean(EEC_dose_FR_md_out), '%.2e' % numpy.std(EEC_dose_FR_md_out), '%.2e' % numpy.min(EEC_dose_FR_md_out), '%.2e' % numpy.max(EEC_dose_FR_md_out),
                    '%.2e' % numpy.mean(EEC_dose_FR_lg_out), '%.2e' % numpy.std(EEC_dose_FR_lg_out), '%.2e' % numpy.min(EEC_dose_FR_lg_out), '%.2e' % numpy.max(EEC_dose_FR_lg_out),],
        "ARQ_FR":  ['%.2e' % numpy.mean(ARQ_dose_FR_sm_out), '%.2e' % numpy.std(ARQ_dose_FR_sm_out), '%.2e' % numpy.min(ARQ_dose_FR_sm_out), '%.2e' % numpy.max(ARQ_dose_FR_sm_out),
                    '%.2e' % numpy.mean(ARQ_dose_FR_md_out), '%.2e' % numpy.std(ARQ_dose_FR_md_out), '%.2e' % numpy.min(ARQ_dose_FR_md_out), '%.2e' % numpy.max(ARQ_dose_FR_md_out),
                    '%.2e' % numpy.mean(ARQ_dose_FR_lg_out), '%.2e' % numpy.std(ARQ_dose_FR_lg_out), '%.2e' % numpy.min(ARQ_dose_FR_lg_out), '%.2e' % numpy.max(ARQ_dose_FR_lg_out),],
        "EEC_HM":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(EEC_dose_HM_md_out), '%.2e' % numpy.std(EEC_dose_HM_md_out), '%.2e' % numpy.min(EEC_dose_HM_md_out), '%.2e' % numpy.max(EEC_dose_HM_md_out),
                    '%.2e' % numpy.mean(EEC_dose_HM_lg_out), '%.2e' % numpy.std(EEC_dose_HM_lg_out), '%.2e' % numpy.min(EEC_dose_HM_lg_out), '%.2e' % numpy.max(EEC_dose_HM_lg_out),],
        "ARQ_HM":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(ARQ_dose_HM_md_out), '%.2e' % numpy.std(ARQ_dose_HM_md_out), '%.2e' % numpy.min(ARQ_dose_HM_md_out), '%.2e' % numpy.max(ARQ_dose_HM_md_out),
                    '%.2e' % numpy.mean(ARQ_dose_HM_lg_out), '%.2e' % numpy.std(ARQ_dose_HM_lg_out), '%.2e' % numpy.min(ARQ_dose_HM_lg_out), '%.2e' % numpy.max(ARQ_dose_HM_lg_out),],
        "EEC_IM":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(EEC_dose_IM_md_out), '%.2e' % numpy.std(EEC_dose_IM_md_out), '%.2e' % numpy.min(EEC_dose_IM_md_out), '%.2e' % numpy.max(EEC_dose_IM_md_out),
                    '%.2e' % numpy.mean(EEC_dose_IM_lg_out), '%.2e' % numpy.std(EEC_dose_IM_lg_out), '%.2e' % numpy.min(EEC_dose_IM_lg_out), '%.2e' % numpy.max(EEC_dose_IM_lg_out),],
        "ARQ_IM":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(ARQ_dose_IM_md_out), '%.2e' % numpy.std(ARQ_dose_IM_md_out), '%.2e' % numpy.min(ARQ_dose_IM_md_out), '%.2e' % numpy.max(ARQ_dose_IM_md_out),
                    '%.2e' % numpy.mean(ARQ_dose_IM_lg_out), '%.2e' % numpy.std(ARQ_dose_IM_lg_out), '%.2e' % numpy.min(ARQ_dose_IM_lg_out), '%.2e' % numpy.max(ARQ_dose_IM_lg_out),],
        "EEC_TP":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(EEC_dose_TP_md_out), '%.2e' % numpy.std(EEC_dose_TP_md_out), '%.2e' % numpy.min(EEC_dose_TP_md_out), '%.2e' % numpy.max(EEC_dose_TP_md_out),
                    '%.2e' % numpy.mean(EEC_dose_TP_lg_out), '%.2e' % numpy.std(EEC_dose_TP_lg_out), '%.2e' % numpy.min(EEC_dose_TP_lg_out), '%.2e' % numpy.max(EEC_dose_TP_lg_out),],
        "ARQ_TP":  ['N/A', 'N/A', 'N/A', 'N/A',
                    '%.2e' % numpy.mean(ARQ_dose_TP_md_out), '%.2e' % numpy.std(ARQ_dose_TP_md_out), '%.2e' % numpy.min(ARQ_dose_TP_md_out), '%.2e' % numpy.max(ARQ_dose_TP_md_out),
                    '%.2e' % numpy.mean(ARQ_dose_TP_lg_out), '%.2e' % numpy.std(ARQ_dose_TP_lg_out), '%.2e' % numpy.min(ARQ_dose_TP_lg_out), '%.2e' % numpy.max(ARQ_dose_TP_lg_out),],
    }
    return data


pvuheadings = getheaderpvu()
pv5headings = getheaderpv5()
pv6headings = getheaderpv6()
pv7headings = getheaderpv7()

sumheadings = getheadersum()
sumheadings_5 = getheaderpv5_sum()
sumheadings_7 = getheaderpv7_sum()
djtemplate = getdjtemplate()
djtemplate_5 = getdjtemplate_5()

tmpl = Template(djtemplate)
tmpl_5 = Template(djtemplate_5)


def table_all(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, 
              Species_of_the_tested_bird, tw_bird, x, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a):
    table1_out = table_1(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r)
    table2_out = table_2(ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, Species_of_the_tested_bird, tw_bird, x)
    table3_out = table_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a)
    table5_out = table_5(lc50_bird, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, wp_herp_a_sm)
    table6_out = table_6(NOAEC_bird, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, wp_herp_a_sm)
    table7_out = table_7(ld50_bird, tw_bird, x, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg)

    html_all = table1_out
    html_all = html_all + table2_out
    html_all = html_all + table3_out
    html_all = html_all + table5_out['html']
    html_all = html_all + table6_out['html']
    html_all = html_all + table7_out['html']
    return html_all, table5_out, table6_out, table7_out

def table_sum_1(i, percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H3>Summary Statistics (Iterations=%s)</H3>
              <H3>Batch Inputs:</H3>
              <H4>Chemical Properties</H4>
            </div>
        """%(i-1)

        #table sum_input
        tsuminputdata_1 = gettsumdata_1(percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings)))
        return html

def table_sum_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, body_weight_of_the_tested_bird, mineau_scaling_factor):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H4>Toxicity Properties</H4>
            </div>
        """

        #table sum_input
        tsuminputdata_2 = gettsumdata_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, body_weight_of_the_tested_bird, mineau_scaling_factor)
        tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings)))
        return html

def table_sum_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H4>Assessed Species Inputs</H4>
            </div>
        """

        #table sum_input
        tsuminputdata_3 = gettsumdata_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a)
        tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings)))
        return html

def table_sum_5(EEC_diet_herp_BL_out, EEC_ARQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_ARQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_ARQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_ARQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_ARQ_herp_TP_out):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H3>Batch outputs:</H3>
              <H4>Upper Bound Kenaga, Subacute Terrestrial Herpetofauna Dietary Based Risk Quotients</H4>
            </div>
        """

        #table sum_input
        tsuminputdata_5 = gettsumdata_5(EEC_diet_herp_BL_out, EEC_ARQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_ARQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_ARQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_ARQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_ARQ_herp_TP_out)
        tsuminputrows_5 = gethtmlrowsfromcols(tsuminputdata_5, sumheadings_5[1])
        html = html + tmpl_5.render(Context(dict(data=tsuminputrows_5, l_headings=sumheadings_5[0][0])))
        return html

def table_sum_6(EEC_diet_herp_BL_out, EEC_CRQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_CRQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_CRQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_CRQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_CRQ_herp_TP_out):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H4>Upper Bound Kenaga, Chronic Terrestrial Herpetofauna Dietary Based Risk Quotients</H4>
            </div>
        """

        #table sum_input
        tsuminputdata_6 = gettsumdata_6(EEC_diet_herp_BL_out, EEC_CRQ_herp_BL_out, EEC_diet_herp_FR_out, EEC_CRQ_herp_FR_out, EEC_diet_herp_HM_out, EEC_CRQ_herp_HM_out, EEC_diet_herp_IM_out, EEC_CRQ_herp_IM_out, EEC_diet_herp_TP_out, EEC_CRQ_herp_TP_out)
        tsuminputrows_6 = gethtmlrowsfromcols(tsuminputdata_6, sumheadings_5[1])
        html = html + tmpl_5.render(Context(dict(data=tsuminputrows_6, l_headings=sumheadings_5[0][0])))
        return html

def table_sum_7(bw_herp_a_sm_out, bw_herp_a_md_out, bw_herp_a_lg_out, LD50_AD_sm_out, LD50_AD_md_out, LD50_AD_lg_out,
                  EEC_dose_BP_sm_out, EEC_dose_BP_md_out, EEC_dose_BP_lg_out, ARQ_dose_BP_sm_out, ARQ_dose_BP_md_out, ARQ_dose_BP_lg_out,
                  EEC_dose_FR_sm_out, EEC_dose_FR_md_out, EEC_dose_FR_lg_out, ARQ_dose_FR_sm_out, ARQ_dose_FR_md_out, ARQ_dose_FR_lg_out,
                  EEC_dose_HM_md_out, EEC_dose_HM_lg_out, ARQ_dose_HM_md_out, ARQ_dose_HM_lg_out,
                  EEC_dose_IM_md_out, EEC_dose_IM_lg_out, ARQ_dose_IM_md_out, ARQ_dose_IM_lg_out,
                  EEC_dose_TP_md_out, EEC_dose_TP_lg_out, ARQ_dose_TP_md_out, ARQ_dose_TP_lg_out):
        #pre-table sum_input
        html = """
            <div class="out_1">
              <H4>Upper Bound Kenaga_out, Acute Terrestrial Herpetofauna Dose-Based Risk Quotients</H4>
            </div>
        """

        #table sum_input
        tsuminputdata_7 = gettsumdata_7(bw_herp_a_sm_out, bw_herp_a_md_out, bw_herp_a_lg_out, LD50_AD_sm_out, LD50_AD_md_out, LD50_AD_lg_out,
                  EEC_dose_BP_sm_out, EEC_dose_BP_md_out, EEC_dose_BP_lg_out, ARQ_dose_BP_sm_out, ARQ_dose_BP_md_out, ARQ_dose_BP_lg_out,
                  EEC_dose_FR_sm_out, EEC_dose_FR_md_out, EEC_dose_FR_lg_out, ARQ_dose_FR_sm_out, ARQ_dose_FR_md_out, ARQ_dose_FR_lg_out,
                  EEC_dose_HM_md_out, EEC_dose_HM_lg_out, ARQ_dose_HM_md_out, ARQ_dose_HM_lg_out,
                  EEC_dose_IM_md_out, EEC_dose_IM_lg_out, ARQ_dose_IM_md_out, ARQ_dose_IM_lg_out,
                  EEC_dose_TP_md_out, EEC_dose_TP_lg_out, ARQ_dose_TP_md_out, ARQ_dose_TP_lg_out)
        tsuminputrows_7 = gethtmlrowsfromcols(tsuminputdata_7, sumheadings_7[1])
        html = html + tmpl_5.render(Context(dict(data=tsuminputrows_7, l_headings=[sumheadings_7[0][0][0], sumheadings_7[0][0][1], sumheadings_7[0][0][2], sumheadings_7[0][0][3]])))
        return html


def table_1(chemical_name, Use, Formulated_product_name, percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs:</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(chemical_name, Use, Formulated_product_name, percent_ai, Foliar_dissipation_half_life, number_of_applications, interval_between_applications, application_rate)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, Species_of_the_tested_bird, body_weight_of_the_tested_bird, mineau_scaling_factor):
        #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Toxicity Properties</H4>
                <div class="out_ container_output">
        """
        #table 2
        t2data = gett2data(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, Species_of_the_tested_bird, body_weight_of_the_tested_bird, mineau_scaling_factor)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_3(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a):
        #pre-table 3
        html = """
            <H4 class="out_3 collapsible" id="section4"><span></span>Assessed Species Inputs</H4>
                <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg, c_mamm_a, c_herp_a)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_5(lc50_bird, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, wp_herp_a_sm):
        #pre-table 5
        html = """
        <br>
        <H3 class="out_5 collapsible" id="section5"><span></span>Results</H3>
        <div class="out_">
            <H4 class="out_5 collapsible" id="section6"><span></span>Upper Bound Kenaga, Subacute Terrestrial Herpetofauna Dietary Based Risk Quotients</H4>
                <div class="out_ container_output">
        """
        #table 5
        EEC_diet_herp_BL=therps_model.EEC_diet(therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_ARQ_herp_BL=therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_diet_herp_FR=therps_model.C_0(a_r, a_i, 15)
        EEC_ARQ_herp_FR=therps_model.ARQ_diet_herp(therps_model.EEC_diet, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        EEC_diet_herp_HM=therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_ARQ_herp_HM=therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_diet_herp_IM=therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_ARQ_herp_IM=therps_model.ARQ_diet_mamm(therps_model.EEC_diet_mamm, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_diet_herp_TP=therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm)
        EEC_ARQ_herp_TP=therps_model.ARQ_diet_tp(therps_model.EEC_diet_tp, lc50_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm)

        t5data = gett5data(lc50_bird, EEC_diet_herp_BL, EEC_ARQ_herp_BL, EEC_diet_herp_FR, EEC_ARQ_herp_FR, EEC_diet_herp_HM, EEC_ARQ_herp_HM, EEC_diet_herp_IM, EEC_ARQ_herp_IM, EEC_diet_herp_TP, EEC_ARQ_herp_TP)
        t5rows = gethtmlrowsfromcols(t5data,pv5headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t5rows, l_headings=pv5headings[0][0])))
        html = html + """
                </div>
        """
        return {'html':html, 'EEC_diet_herp_BL':EEC_diet_herp_BL, 'EEC_ARQ_herp_BL':EEC_ARQ_herp_BL, 'EEC_diet_herp_FR':EEC_diet_herp_FR, 'EEC_ARQ_herp_FR':EEC_ARQ_herp_FR, 
                'EEC_diet_herp_HM':EEC_diet_herp_HM, 'EEC_ARQ_herp_HM':EEC_ARQ_herp_HM, 'EEC_diet_herp_IM':EEC_diet_herp_IM, 'EEC_ARQ_herp_IM':EEC_ARQ_herp_IM, 'EEC_diet_herp_TP':EEC_diet_herp_TP, 'EEC_ARQ_herp_TP':EEC_ARQ_herp_TP}

def table_6(NOAEC_bird, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, wp_herp_a_sm):
        #pre-table 6
        html = """
            <H4 class="out_6 collapsible" id="section7"><span></span>Upper Bound Kenaga, Chronic Terrestrial Herpetofauna Dietary Based Risk Quotients</H4>
                <div class="out_ container_output">
        """
        #table 6
        EEC_diet_herp_BL=therps_model.EEC_diet(therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_CRQ_herp_BL=therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_diet_herp_FR=therps_model.C_0(a_r, a_i, 15)
        EEC_CRQ_herp_FR=therps_model.CRQ_diet_herp(therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        EEC_diet_herp_HM=therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_CRQ_herp_HM=therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_diet_herp_IM=therps_model.EEC_diet_mamm(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_CRQ_herp_IM=therps_model.CRQ_diet_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, therps_model.fi_mamm, c_mamm_a, 0.8)
        EEC_diet_herp_TP=therps_model.EEC_diet_tp(therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm)
        EEC_CRQ_herp_TP=therps_model.CRQ_diet_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, NOAEC_bird, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm)

        t6data = gett6data(NOAEC_bird, EEC_diet_herp_BL, EEC_CRQ_herp_BL, EEC_diet_herp_FR, EEC_CRQ_herp_FR, EEC_diet_herp_HM, EEC_CRQ_herp_HM, EEC_diet_herp_IM, EEC_CRQ_herp_IM, EEC_diet_herp_TP, EEC_CRQ_herp_TP)
        t6rows = gethtmlrowsfromcols(t6data,pv6headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t6rows, l_headings=pv6headings[0][0])))
        html = html + """
                </div>
        """
        return {'html':html, 'EEC_diet_herp_BL':EEC_diet_herp_BL, 'EEC_CRQ_herp_BL':EEC_CRQ_herp_BL, 'EEC_diet_herp_FR':EEC_diet_herp_FR, 'EEC_CRQ_herp_FR':EEC_CRQ_herp_FR, 
                'EEC_diet_herp_HM':EEC_diet_herp_HM, 'EEC_CRQ_herp_HM':EEC_CRQ_herp_HM, 'EEC_diet_herp_IM':EEC_diet_herp_IM, 'EEC_CRQ_herp_IM':EEC_CRQ_herp_IM, 'EEC_diet_herp_TP':EEC_diet_herp_TP, 'EEC_CRQ_herp_TP':EEC_CRQ_herp_TP}

def table_7(ld50_bird, tw_bird, x, n_a, i_a, a_r, a_i, h_l, c_mamm_a, c_herp_a, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, wp_herp_a_lg):
        #pre-table 7
        html = """
            <H4 class="out_7 collapsible" id="section8"><span></span>Upper Bound Kenaga, Acute Terrestrial Herpetofauna Dose-Based Risk Quotients</H4>
                <div class="out_ container_output">
        """
        #table 7
        LD50_AD_sm=therps_model.at_bird(ld50_bird, bw_herp_a_sm, tw_bird, x)
        LD50_AD_md=therps_model.at_bird(ld50_bird, bw_herp_a_md, tw_bird, x)
        LD50_AD_lg=therps_model.at_bird(ld50_bird, bw_herp_a_lg, tw_bird, x)

        EEC_dose_BP_sm=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_sm, therps_model.fi_herp, wp_herp_a_sm, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_dose_BP_md=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_md, therps_model.fi_herp, wp_herp_a_md, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        EEC_dose_BP_lg=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_lg, therps_model.fi_herp, wp_herp_a_lg, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        ARQ_dose_BP_sm=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_sm, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_sm, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        ARQ_dose_BP_md=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_md, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_md, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)
        ARQ_dose_BP_lg=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_lg, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_lg, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l)

        EEC_dose_FR_sm=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_sm, therps_model.fi_herp, wp_herp_a_sm, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        EEC_dose_FR_md=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_md, therps_model.fi_herp, wp_herp_a_md, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        EEC_dose_FR_lg=therps_model.EEC_dose_herp(therps_model.EEC_diet, bw_herp_a_lg, therps_model.fi_herp, wp_herp_a_lg, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        ARQ_dose_FR_sm=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_sm, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_sm, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        ARQ_dose_FR_md=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_md, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_md, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        ARQ_dose_FR_lg=therps_model.ARQ_dose_herp(therps_model.EEC_dose_herp, therps_model.EEC_diet, bw_herp_a_lg, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, wp_herp_a_lg, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)

        EEC_dose_HM_md=therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, bw_herp_a_md, c_mamm_a, 0.8)
        EEC_dose_HM_lg=therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l, bw_herp_a_lg, c_mamm_a, 0.8)
        ARQ_dose_HM_md=therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_md, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, 0.8, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l)
        ARQ_dose_HM_lg=therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_lg, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, 0.8, therps_model.C_0, n_a, i_a, a_r, a_i, 240, h_l)

        EEC_dose_IM_md=therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, bw_herp_a_md, c_mamm_a, 0.8)
        EEC_dose_IM_lg=therps_model.EEC_dose_mamm(therps_model.EEC_diet_mamm, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l, bw_herp_a_lg, c_mamm_a, 0.8)
        ARQ_dose_IM_md=therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_md, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, 0.8, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)
        ARQ_dose_IM_lg=therps_model.ARQ_dose_mamm(therps_model.EEC_dose_mamm, therps_model.EEC_diet_mamm, bw_herp_a_lg, therps_model.fi_herp, therps_model.at_bird, ld50_bird, tw_bird, x, c_mamm_a, 0.8, therps_model.C_0, n_a, i_a, a_r, a_i, 15, h_l)

        EEC_dose_TP_md=therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        EEC_dose_TP_lg=therps_model.EEC_dose_tp(therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm, wp_herp_a_md)
        ARQ_dose_TP_md=therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, therps_model.at_bird, ld50_bird, bw_herp_a_md, tw_bird, x)
        ARQ_dose_TP_lg=therps_model.ARQ_dose_tp(therps_model.EEC_dose_tp, therps_model.EEC_diet_tp, therps_model.EEC_diet, therps_model.C_0, n_a, i_a, a_r, a_i, 135, h_l, therps_model.fi_herp, c_herp_a, wp_herp_a_sm, wp_herp_a_md, therps_model.at_bird, ld50_bird, bw_herp_a_lg, tw_bird, x)

        t7data = gett7data(LD50_AD_sm, LD50_AD_md, LD50_AD_lg,
                           EEC_dose_BP_sm, EEC_dose_BP_md, EEC_dose_BP_lg, ARQ_dose_BP_sm, ARQ_dose_BP_md, ARQ_dose_BP_lg,
                           EEC_dose_FR_sm, EEC_dose_FR_md, EEC_dose_FR_lg, ARQ_dose_FR_sm, ARQ_dose_FR_md, ARQ_dose_FR_lg,
                           EEC_dose_HM_md, EEC_dose_HM_lg, ARQ_dose_HM_md, ARQ_dose_HM_lg,
                           EEC_dose_IM_md, EEC_dose_IM_lg, ARQ_dose_IM_md, ARQ_dose_IM_lg,
                           EEC_dose_TP_md, EEC_dose_TP_lg, ARQ_dose_TP_md, ARQ_dose_TP_lg)

        t7rows = gethtmlrowsfromcols(t7data, pv7headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t7rows, l_headings=[pv7headings[0][0][0], pv7headings[0][0][1]])))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'LD50_AD_sm': LD50_AD_sm, 'LD50_AD_md': LD50_AD_md, 'LD50_AD_lg': LD50_AD_lg, 
                'EEC_dose_BP_sm': EEC_dose_BP_sm, 'EEC_dose_BP_md': EEC_dose_BP_md, 'EEC_dose_BP_lg': EEC_dose_BP_lg, 
                'ARQ_dose_BP_sm': ARQ_dose_BP_sm, 'ARQ_dose_BP_md': ARQ_dose_BP_md, 'ARQ_dose_BP_lg': ARQ_dose_BP_lg, 
                'EEC_dose_FR_sm': EEC_dose_FR_sm, 'EEC_dose_FR_md': EEC_dose_FR_md, 'EEC_dose_FR_lg': EEC_dose_FR_lg, 
                'ARQ_dose_FR_sm': ARQ_dose_FR_sm, 'ARQ_dose_FR_md': ARQ_dose_FR_md, 'ARQ_dose_FR_lg': ARQ_dose_FR_lg,
                'EEC_dose_HM_md': EEC_dose_HM_md, 'EEC_dose_HM_lg': EEC_dose_HM_lg, 'ARQ_dose_HM_md': ARQ_dose_HM_md, 
                'ARQ_dose_HM_lg': ARQ_dose_HM_lg, 'EEC_dose_IM_md': EEC_dose_IM_md, 'EEC_dose_IM_lg': EEC_dose_IM_lg, 
                'ARQ_dose_IM_md': ARQ_dose_IM_md, 'ARQ_dose_IM_lg': ARQ_dose_IM_lg, 'EEC_dose_TP_md': EEC_dose_TP_md, 
                'EEC_dose_TP_lg': EEC_dose_TP_lg, 'ARQ_dose_TP_md': ARQ_dose_TP_md, 'ARQ_dose_TP_lg': ARQ_dose_TP_lg}
