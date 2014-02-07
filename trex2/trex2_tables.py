import numpy
import time, datetime
from django.template import Context, Template
from django.utils.safestring import mark_safe
from trex2 import trex2_model
from trex2 import trex2_parameters
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva():
    headings = ["App", "Rate", "Day of Application"]
    headings_show = ["App", "Rate (lb ai/acre)", "Day of Application"]
    headings_show_seed = ["App", "Rate (fl oz/cwt)", "Day of Application"]
    return headings, headings_show, headings_show_seed

def getheaderpv5():
    headings_1 = ["Avian (20g)", "Mammalian (15g)"]
    headings_2 = ["Size", "AAcute #1", "AAcute #2", "AChronic", "MAcute #1", "MAcute #2", "MChronic"]
    headings_2_show = ["", "Acute #1", "Acute #2", "Chronic", "Acute #1", "Acute #2", "Chronic"]
    headings_3_show = ["Size", "(mg ai /kg-bw/day)/LD50", "mg ai ft<sup>-2</sup>/(LD50*bw)", "mg kg<sup>-1</sup>seed/NOAEL", "(mg ai /kg-bw/day)/LD50", "mg ai ft<sup>-2</sup>/(LD50*bw)", "mg a.i./kg-bw/day/adjusted NOAEL"]

    return headings_1, headings_2, headings_2_show, headings_3_show

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

def getheadersum5():
    headings_1 = ["Avian (20g)", "Mammalian (15g)"]
    headings_2 = ["Size", "Metric", "AAcute #1", "AAcute #2", "AChronic", "MAcute #1", "MAcute #2", "MChronic"]
    headings_2_show = ["Size", "Metric", "Acute #1", "Acute #2", "Chronic", "Acute #1", "Acute #2", "Chronic"]
    return headings_1, headings_2, headings_2_show

def getheadersum6():
    headings_1 = ["Metric", "Application Target"]
    headings_1_c_span = [1, 5]
    headings_1_r_span = [2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods/Seeds", "Arthropods"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods/Seeds", "Arthropods"]
    return headings_1_zip, headings_2, headings_2_show

def getheadersum7():
    headings_1 = ["Animal Size", "Metric", "Application Target"]
    headings_1_c_span = [1, 1, 6]
    headings_1_r_span = [2, 2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Animal Size", "Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]
    # headings_2 = ["Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]    
    return headings_1_zip, headings_2, headings_2_show

def getheadersum8():
    headings_1 = ["Type", "Metric", "Application Target"]
    headings_1_c_span = [1, 1, 5]
    headings_1_r_span = [2, 2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Type", "Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods"]    
    return headings_1_zip, headings_2, headings_2_show

def getheadersum9():
    headings_1 = ["Animal Size", "Metric", "Application Target"]
    headings_1_c_span = [1, 1, 6]
    headings_1_r_span = [2, 2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Animal Size", "Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]    
    return headings_1_zip, headings_2, headings_2_show

def getheadersum10():
    headings_1 = ["Animal Size", "Type", "Metric", "Application Target"]
    headings_1_c_span = [1, 1, 1, 6]
    headings_1_r_span = [2, 2, 2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Animal Size", "Type", "Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods", "Arthropods", "Seeds"]    
    return headings_1_zip, headings_2, headings_2_show

def getheadersum11():
    headings_1 = ["Type", "Metric", "Application Target"]
    headings_1_c_span = [1, 1, 5]
    headings_1_r_span = [2, 2, 1]
    headings_1_zip = zip(headings_1, headings_1_c_span, headings_1_r_span)
    headings_2 = ["Type", "Metric", "Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods/Seeds", "Arthropods"]
    headings_2_show = ["Short Grass", "Tall Grass", "Broadleaf Plants", "Fruits/Pods/Seeds", "Arthropods"]    
    return headings_1_zip, headings_2, headings_2_show

def getheadersum12():
    headings = ["Animal Size", "Metric", "Avian", "Mammal"]
    return headings

def getheaderpv5_qaqc():
    headings_1 = ["Avian (20g)", "Mammalian (15g)"]
    headings_2 = ["Type", "Size", "AAcute #1", "AAcute #2", "AChronic", "MAcute #1", "MAcute #2", "MChronic"]
    headings_2_show = ["", "", "Acute #1", "Acute #2", "Chronic", "Acute #1", "Acute #2", "Chronic"]
    headings_3_show = ["Type", "Size", "(mg ai /kg-bw/day)/LD50", "mg ai ft<sup>-2</sup>/(LD50*bw)", "mg kg<sup>-1</sup>seed/NOAEL", "(mg ai /kg-bw/day)/LD50", "mg ai ft<sup>-2</sup>/(LD50*bw)", "mg a.i./kg-bw/day/adjusted NOAEL"]
    return headings_1, headings_2, headings_2_show, headings_3_show

def getheaderpv6_qaqc():
    headings = ["Type", "Application Target", "Value"]
    return headings

def getheaderpv7_qaqc():
    headings = ["Type", "Application Target", "Small", "Medium", "Large"]
    return headings

def getheaderpv8_qaqc():
    headings = ["Type", "Application Target", "Acute", "Chronic"]
    return headings

def getheaderpv10_qaqc():
    headings = ["Type", "Application Target", "Acute_sm", "Chronic_sm", "Acute_md", "Chronic_md", "Acute_lg", "Chronic_lg"]
    return headings

def getheaderpv12_qaqc():
    headings = ["Type", "Animal Size", "Avian", "Mammal"]
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
        {% if sub_headings_1 %}
            <tr>
            {% for sub_heading_1 in sub_headings_1 %}
                <th>{{ sub_heading_1|safe }}</th>
            {% endfor %}
            </tr>
        {% endif %}
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

def getdjtemplate_sum():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
            {% for heading, th_c_span, th_r_span in headings %}
                <th colspan={{ th_c_span|default:'1' }} rowspan={{ th_r_span|default:'1' }}>{{ heading }}</th>
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
    {% if data %}
        {% for row in data %}
                <tr>
                    {% for val in row %}
                        <td>{{ val|default:'' }}</td>
                    {% endfor %}
                </tr>
        {% endfor %}
    {% endif %}

    {% if data_cols %}
        {% for data_col in data_cols %}
            <tr>
                <td rowspan='4'>{{ data_col|default:''}}</td>
                    {% for row in data_new %}
                        {% for val in row %}
                            <td>{{ val|default:'' }}</td>
                        {% endfor %}
                    {% endfor %}
            </tr>
        {% endfor %}
    {% endif %}


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

def getdjtemplate_10_qaqc():
    dj_template ="""
    <table class="out_">
    {# headings #}
      <tr>
        <th rowspan="2">Type</div></th>
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
sumheadings_5 = getheadersum5()
sumheadings_6 = getheadersum6()
sumheadings_7 = getheadersum7()
sumheadings_8 = getheadersum8()
sumheadings_9 = getheadersum9()
sumheadings_10 = getheadersum10()
sumheadings_11 = getheadersum11()
sumheadings_12 = getheadersum12()

pv5headings_qaqc = getheaderpv5_qaqc()
pv6headings_qaqc = getheaderpv6_qaqc()
pv7headings_qaqc = getheaderpv7_qaqc()
pv8headings_qaqc = getheaderpv8_qaqc()
pv10headings_qaqc = getheaderpv10_qaqc()
pv12headings_qaqc = getheaderpv12_qaqc()

djtemplate = getdjtemplate()
djtemplate_sum = getdjtemplate_sum()
djtemplate_10 = getdjtemplate_10()
djtemplate_10_qaqc = getdjtemplate_10_qaqc()

tmpl = Template(djtemplate)
tmpl_sum = Template(djtemplate_sum)
tmpl_10 = Template(djtemplate_10)
tmpl_10_qaqc = Template(djtemplate_10_qaqc)




def gett1data_broad(trex2_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Use', 'Formulated product name', 'Percentage active ingredient', 
                      'Application type', 'Percentage incorporated', 'Foliar dissipation half-life',],
        "Value": ['%s' % trex2_obj.chem_name, '%s' % trex2_obj.use, '%s' % trex2_obj.formu_name, '%s' % trex2_obj.a_i_t1, '%s' % trex2_obj.Application_type, 
                  '%s' % trex2_obj.p_i, '%s' % trex2_obj.h_l,],
        "Units": ['', '', '', '%', '', '%', 'days',],
    }
    return data

def gett1data_band(trex2_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Use', 'Formulated product name', 'Percentage active ingredient', 
                      'Application type', 'Row spacing', 'Bandwidth', 'Percentage incorporated', 'Foliar dissipation half-life',],
        "Value": ['%s' % trex2_obj.chem_name, '%s' % trex2_obj.use, '%s' % trex2_obj.formu_name, '%s' % trex2_obj.a_i_t1, '%s' % trex2_obj.Application_type, 
                  '%.4s' % trex2_obj.r_s, '%.4s' % trex2_obj.b_w_t1, '%s' % trex2_obj.p_i, '%s' % trex2_obj.h_l,],
        "Units": ['', '', '', '%', '', 'inch', 'inch', '%', 'days',],
    }
    return data

def gett1data_seed(trex2_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Use', 'Formulated product name', 'Percentage active ingredient', 
                      'Application type', 'Seed treatment formulation name', 'Crop use', 'Density of product', 'Seeding rare'],
        "Value": ['%s' % trex2_obj.chem_name, '%s' % trex2_obj.use, '%s' % trex2_obj.formu_name, '%s' % trex2_obj.a_i_t1, '%s' % trex2_obj.Application_type, 
                  '%s' % trex2_obj.seed_treatment_formulation_name, '%s' % trex2_obj.seed_crop_v, '%s' % trex2_obj.den, '%s' % trex2_obj.m_s_r_p,],
        "Units": ['', '', '', '%', '', '', '', 'lbs/gal', 'lbs/acre',],
    }
    return data

def gett2data(index, rate, day):
    data = { 
        "App": ['%s' %index,  ],
        "Rate": [rate,],
        "Day of Application": ['%s' %day,],
    }
    return data

def gett3data(trex2_obj):
    data = { 
        "Parameter": ['Avian LD50', 'Test species (for Avian LD50)', 'Weight',
                      'Avian LC50', 'Test species (for Avian LC50)', 'Weight',
                      'Avian NOAEC', 'Test species (for Avian NOAEC)', 'Weight',
                      'Avian NOAEL', 'Test species (for Avian NOAEL)', 'Weight',
                      'Body weight of assessed bird small', 'Body weight of assessed bird medium', 
                      'Body weight of assessed bird large', 'Mineau scaling factor', ],
        "Value": ['%s' % trex2_obj.ld50_bird, '%s' % trex2_obj.Species_of_the_tested_bird_avian_ld50, '%s' % trex2_obj.tw_bird_ld50,
                  '%s' % trex2_obj.lc50_bird, '%s' % trex2_obj.Species_of_the_tested_bird_avian_lc50, '%s' % trex2_obj.tw_bird_lc50,
                  '%s' % trex2_obj.NOAEC_bird, '%s' % trex2_obj.Species_of_the_tested_bird_avian_NOAEC, '%s' % trex2_obj.tw_bird_NOAEC,
                  '%s' % trex2_obj.NOAEL_bird, '%s' % trex2_obj.Species_of_the_tested_bird_avian_NOAEL, '%s' % trex2_obj.tw_bird_NOAEL,
                  '%s' % trex2_obj.aw_bird_sm, '%s' % trex2_obj.aw_bird_md, '%s' % trex2_obj.aw_bird_lg, '%s' % trex2_obj.x, ],
        "Units": ['mg/kg-bw', '', 'g', 'mg/kg-diet', '', 'g', 'mg/kg-diet', '', 'g', 'mg/kg-bw', '', 'g', 'g', 'g', 'g', ''],
    }
    return data

def gett4data(trex_obj):
    data = { 
        "Parameter": ['Mammalian LD50', 'Mammalian LC50', 'Mammalian NOAEC', 'Mammalian NOAEL', 'Body weight of assessed mammal small',
                      'Body weight of assessed mammal medium', 'Body weight of assessed mammal large', 
                      'Body weight of tested mammal', ],
        "Value": ['%s' % trex_obj.ld50_mamm, '%s' % trex_obj.lc50_mamm, '%s' % trex_obj.NOAEC_mamm, '%s' % trex_obj.NOAEL_mamm, 
                  '%s' % trex_obj.aw_mamm_sm, '%s' % trex_obj.aw_mamm_md, '%s' % trex_obj.aw_mamm_lg, '%s' % trex_obj.tw_mamm, ],
        "Units": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', 'g', 'g', 'g', 'g', ],
    }
    return data

def gett5data(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
              sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
              sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l):
    data = { 
        "Size": ['Small', 'Medium','Large',],
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

def gett7_add_data(ARQ_bird_SG_sm, ARQ_bird_SG_md, ARQ_bird_SG_lg, ARQ_bird_TG_sm, ARQ_bird_TG_md, ARQ_bird_TG_lg, ARQ_bird_BP_sm, ARQ_bird_BP_md, ARQ_bird_BP_lg, ARQ_bird_FP_sm, ARQ_bird_FP_md, ARQ_bird_FP_lg, ARQ_bird_AR_sm, ARQ_bird_AR_md, ARQ_bird_AR_lg, ARQ_bird_SE_sm, ARQ_bird_SE_md, ARQ_bird_SE_lg):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods', 'Arthropods', 'Seeds',],
        "Small": ['%.2e' % ARQ_bird_SG_sm, '%.2e' % ARQ_bird_TG_sm, '%.2e' % ARQ_bird_BP_sm, '%.2e' % ARQ_bird_FP_sm, '%.2e' % ARQ_bird_AR_sm, '%.2e' % ARQ_bird_SE_sm],
        "Medium": ['%.2e' % ARQ_bird_SG_md, '%.2e' % ARQ_bird_TG_md, '%.2e' % ARQ_bird_BP_md, '%.2e' % ARQ_bird_FP_md, '%.2e' % ARQ_bird_AR_md, '%.2e' % ARQ_bird_SE_md],
        "Large": ['%.2e' % ARQ_bird_SG_lg, '%.2e' % ARQ_bird_TG_lg, '%.2e' % ARQ_bird_BP_lg, '%.2e' % ARQ_bird_FP_lg, '%.2e' % ARQ_bird_AR_lg, '%.2e' % ARQ_bird_SE_lg],
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

def gett11data_na(ARQ_diet_mamm_SG,CRQ_diet_bird_SG,ARQ_diet_mamm_TG,CRQ_diet_bird_TG,ARQ_diet_mamm_BP,CRQ_diet_bird_BP,ARQ_diet_mamm_FP,CRQ_diet_bird_FP,ARQ_diet_mamm_AR,CRQ_diet_bird_AR):
    data = { 
        "Application Target": ['Short Grass', 'Tall Grass', 'Broadleaf Plants', 'Fruits/Pods/Seeds', 'Arthropods',],
        "Acute": ['%s' % ARQ_diet_mamm_SG, '%s' % ARQ_diet_mamm_TG, '%s' % ARQ_diet_mamm_BP, '%s' % ARQ_diet_mamm_FP, '%s' % ARQ_diet_mamm_AR],
        "Chronic": ['%.2e' % CRQ_diet_bird_SG, '%.2e' % CRQ_diet_bird_TG, '%.2e' % CRQ_diet_bird_BP, '%.2e' % CRQ_diet_bird_FP, '%.2e' % CRQ_diet_bird_AR],
    }
    return data 

def gett12data(LD50_rg_bird_sm,LD50_rg_mamm_sm,LD50_rg_bird_md,LD50_rg_mamm_md,LD50_rg_bird_lg,LD50_rg_mamm_lg):
    data = { 
        "Animal Size": ['Small', 'Medium', 'Large', ] ,
        "Avian": ['%.2e' % LD50_rg_bird_sm, '%.2e' % LD50_rg_bird_md, '%.2e' % LD50_rg_bird_lg,],
        "Mammal": ['%.2e' % LD50_rg_mamm_sm, '%.2e' % LD50_rg_mamm_md, '%.2e' % LD50_rg_mamm_lg,],
    }
    return data

def gett5data_qaqc(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
                   sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
                   sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l,
                   sa_bird_1_s_exp, sa_bird_2_s_exp, sc_bird_s_exp, sa_mamm_1_s_exp, sa_mamm_2_s_exp, sc_mamm_s_exp,
                   sa_bird_1_m_exp, sa_bird_2_m_exp, sc_bird_m_exp, sa_mamm_1_m_exp, sa_mamm_2_m_exp, sc_mamm_m_exp,
                   sa_bird_1_l_exp, sa_bird_2_l_exp, sc_bird_l_exp, sa_mamm_1_l_exp, sa_mamm_2_l_exp, sc_mamm_l_exp):
    data = { 
        "Type": ['Calculated Value', 'Expected Value','Calculated Value', 'Expected Value','Calculated Value', 'Expected Value',],
        "Size": ['Small', 'Small', 'Medium', 'Medium', 'Large', 'Large',],
        "AAcute #1": ['%.2e' % sa_bird_1_s, '%.2e' % sa_bird_1_s_exp, '%.2e' % sa_bird_1_m, '%.2e' % sa_bird_1_m_exp, '%.2e' % sa_bird_1_l, '%.2e' % sa_bird_1_l_exp,],
        "AAcute #2": ['%.2e' % sa_bird_2_s, '%.2e' % sa_bird_2_s_exp, '%.2e' % sa_bird_2_m, '%.2e' % sa_bird_2_m_exp, '%.2e' % sa_bird_2_l, '%.2e' % sa_bird_2_l_exp,],
        "AChronic":  ['%.2e' % sc_bird_s, '%.2e' % sc_bird_s_exp, '%.2e' % sc_bird_m, '%.2e' % sc_bird_m_exp, '%.2e' % sc_bird_l, '%.2e' % sc_bird_l_exp,],
        "MAcute #1": ['%.2e' % sa_mamm_1_s, '%.2e' % sa_mamm_1_s_exp, '%.2e' % sa_mamm_1_m, '%.2e' % sa_mamm_1_m_exp, '%.2e' % sa_mamm_1_l, '%.2e' % sa_mamm_1_l_exp,],
        "MAcute #2": ['%.2e' % sa_mamm_2_s, '%.2e' % sa_mamm_2_s_exp, '%.2e' % sa_mamm_2_m, '%.2e' % sa_mamm_2_m_exp, '%.2e' % sa_mamm_2_l, '%.2e' % sa_mamm_2_l_exp,],
        "MChronic":  ['%.2e' % sc_mamm_s, '%.2e' % sc_mamm_s_exp, '%.2e' % sc_mamm_m, '%.2e' % sc_mamm_m_exp, '%.2e' % sc_mamm_l, '%.2e' % sc_mamm_l_exp,],
    }
    return data

def gett6data_qaqc(EEC_diet_SG, EEC_diet_TG, EEC_diet_BP, EEC_diet_FR, EEC_diet_AR, EEC_diet_SG_exp, EEC_diet_TG_exp, EEC_diet_BP_exp, EEC_diet_FR_exp, EEC_diet_AR_exp):
    data = { 
        "Type": ['Calculated Value', 'Expected Value','Calculated Value', 'Expected Value','Calculated Value', 'Expected Value','Calculated Value', 'Expected Value','Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods/Seeds', 'Fruits/Pods/Seeds', 'Arthropods', 'Arthropods',],
        "Value": ['%.2e' % EEC_diet_SG, '%.2e' % EEC_diet_SG_exp, '%.2e' % EEC_diet_TG, '%.2e' % EEC_diet_TG_exp, '%.2e' % EEC_diet_BP, '%.2e' % EEC_diet_BP_exp, '%.2e' % EEC_diet_FR, '%.2e' % EEC_diet_FR_exp, '%.2e' % EEC_diet_AR, '%.2e' % EEC_diet_AR_exp],
    }
    return data

def gett7data_qaqc(EEC_dose_bird_SG_sm, EEC_dose_bird_SG_md, EEC_dose_bird_SG_lg, EEC_dose_bird_TG_sm, EEC_dose_bird_TG_md, EEC_dose_bird_TG_lg, EEC_dose_bird_BP_sm, EEC_dose_bird_BP_md, EEC_dose_bird_BP_lg, EEC_dose_bird_FP_sm, EEC_dose_bird_FP_md, EEC_dose_bird_FP_lg, EEC_dose_bird_AR_sm, EEC_dose_bird_AR_md, EEC_dose_bird_AR_lg, EEC_dose_bird_SE_sm, EEC_dose_bird_SE_md, EEC_dose_bird_SE_lg,
                   EEC_dose_bird_SG_sm_exp, EEC_dose_bird_SG_md_exp, EEC_dose_bird_SG_lg_exp, EEC_dose_bird_TG_sm_exp, EEC_dose_bird_TG_md_exp, EEC_dose_bird_TG_lg_exp, EEC_dose_bird_BP_sm_exp, EEC_dose_bird_BP_md_exp, EEC_dose_bird_BP_lg_exp, EEC_dose_bird_FP_sm_exp, EEC_dose_bird_FP_md_exp, EEC_dose_bird_FP_lg_exp, EEC_dose_bird_AR_sm_exp, EEC_dose_bird_AR_md_exp, EEC_dose_bird_AR_lg_exp, EEC_dose_bird_SE_sm_exp, EEC_dose_bird_SE_md_exp, EEC_dose_bird_SE_lg_exp):
    data = {
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods', 'Fruits/Pods', 'Arthropods', 'Arthropods', 'Seeds', 'Seeds',],
        "Small":  ['%.2e' % EEC_dose_bird_SG_sm, '%.2e' % EEC_dose_bird_SG_sm_exp, '%.2e' % EEC_dose_bird_TG_sm, '%.2e' % EEC_dose_bird_TG_sm_exp, '%.2e' % EEC_dose_bird_BP_sm, '%.2e' % EEC_dose_bird_BP_sm_exp, '%.2e' % EEC_dose_bird_FP_sm, '%.2e' % EEC_dose_bird_FP_sm_exp, '%.2e' % EEC_dose_bird_AR_sm, '%.2e' % EEC_dose_bird_AR_sm_exp, '%.2e' % EEC_dose_bird_SE_sm, '%.2e' % EEC_dose_bird_SE_sm_exp],
        "Medium": ['%.2e' % EEC_dose_bird_SG_md, '%.2e' % EEC_dose_bird_SG_md_exp, '%.2e' % EEC_dose_bird_TG_md, '%.2e' % EEC_dose_bird_TG_md_exp, '%.2e' % EEC_dose_bird_BP_md, '%.2e' % EEC_dose_bird_BP_md_exp, '%.2e' % EEC_dose_bird_FP_md, '%.2e' % EEC_dose_bird_FP_md_exp, '%.2e' % EEC_dose_bird_AR_md, '%.2e' % EEC_dose_bird_AR_md_exp, '%.2e' % EEC_dose_bird_SE_md, '%.2e' % EEC_dose_bird_SE_md_exp],
        "Large":  ['%.2e' % EEC_dose_bird_SG_lg, '%.2e' % EEC_dose_bird_SG_lg_exp, '%.2e' % EEC_dose_bird_TG_lg, '%.2e' % EEC_dose_bird_TG_lg_exp, '%.2e' % EEC_dose_bird_BP_lg, '%.2e' % EEC_dose_bird_BP_lg_exp, '%.2e' % EEC_dose_bird_FP_lg, '%.2e' % EEC_dose_bird_FP_lg_exp, '%.2e' % EEC_dose_bird_AR_lg, '%.2e' % EEC_dose_bird_AR_lg_exp, '%.2e' % EEC_dose_bird_SE_lg, '%.2e' % EEC_dose_bird_SE_lg_exp],
    }
    return data

def gett7_add_data_qaqc(ARQ_bird_SG_sm, ARQ_bird_SG_md, ARQ_bird_SG_lg, ARQ_bird_TG_sm, ARQ_bird_TG_md, ARQ_bird_TG_lg, ARQ_bird_BP_sm, ARQ_bird_BP_md, ARQ_bird_BP_lg, ARQ_bird_FP_sm, ARQ_bird_FP_md, ARQ_bird_FP_lg, ARQ_bird_AR_sm, ARQ_bird_AR_md, ARQ_bird_AR_lg, ARQ_bird_SE_sm, ARQ_bird_SE_md, ARQ_bird_SE_lg,
                        ARQ_bird_SG_sm_exp, ARQ_bird_SG_md_exp, ARQ_bird_SG_lg_exp, ARQ_bird_TG_sm_exp, ARQ_bird_TG_md_exp, ARQ_bird_TG_lg_exp, ARQ_bird_BP_sm_exp, ARQ_bird_BP_md_exp, ARQ_bird_BP_lg_exp, ARQ_bird_FP_sm_exp, ARQ_bird_FP_md_exp, ARQ_bird_FP_lg_exp, ARQ_bird_AR_sm_exp, ARQ_bird_AR_md_exp, ARQ_bird_AR_lg_exp, ARQ_bird_SE_sm_exp, ARQ_bird_SE_md_exp, ARQ_bird_SE_lg_exp):
    data = {
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods', 'Fruits/Pods', 'Arthropods', 'Arthropods', 'Seeds', 'Seeds',],
        "Small":  ['%.2e' % ARQ_bird_SG_sm, '%.2e' % ARQ_bird_SG_sm_exp, '%.2e' % ARQ_bird_TG_sm, '%.2e' % ARQ_bird_TG_sm_exp, '%.2e' % ARQ_bird_BP_sm, '%.2e' % ARQ_bird_BP_sm_exp, '%.2e' % ARQ_bird_FP_sm, '%.2e' % ARQ_bird_FP_sm_exp, '%.2e' % ARQ_bird_AR_sm, '%.2e' % ARQ_bird_AR_sm_exp, '%.2e' % ARQ_bird_SE_sm, '%.2e' % ARQ_bird_SE_sm_exp],
        "Medium": ['%.2e' % ARQ_bird_SG_md, '%.2e' % ARQ_bird_SG_md_exp, '%.2e' % ARQ_bird_TG_md, '%.2e' % ARQ_bird_TG_md_exp, '%.2e' % ARQ_bird_BP_md, '%.2e' % ARQ_bird_BP_md_exp, '%.2e' % ARQ_bird_FP_md, '%.2e' % ARQ_bird_FP_md_exp, '%.2e' % ARQ_bird_AR_md, '%.2e' % ARQ_bird_AR_md_exp, '%.2e' % ARQ_bird_SE_md, '%.2e' % ARQ_bird_SE_md_exp],
        "Large":  ['%.2e' % ARQ_bird_SG_lg, '%.2e' % ARQ_bird_SG_lg_exp, '%.2e' % ARQ_bird_TG_lg, '%.2e' % ARQ_bird_TG_lg_exp, '%.2e' % ARQ_bird_BP_lg, '%.2e' % ARQ_bird_BP_lg_exp, '%.2e' % ARQ_bird_FP_lg, '%.2e' % ARQ_bird_FP_lg_exp, '%.2e' % ARQ_bird_AR_lg, '%.2e' % ARQ_bird_AR_lg_exp, '%.2e' % ARQ_bird_SE_lg, '%.2e' % ARQ_bird_SE_lg_exp],
    }
    return data

def gett8data_qaqc(ARQ_diet_bird_SG_A, ARQ_diet_bird_SG_C, ARQ_diet_bird_TG_A, ARQ_diet_bird_TG_C, ARQ_diet_bird_BP_A, ARQ_diet_bird_BP_C, ARQ_diet_bird_FP_A, ARQ_diet_bird_FP_C, ARQ_diet_bird_AR_A, ARQ_diet_bird_AR_C,
                   ARQ_diet_bird_SG_A_exp, ARQ_diet_bird_SG_C_exp, ARQ_diet_bird_TG_A_exp, ARQ_diet_bird_TG_C_exp, ARQ_diet_bird_BP_A_exp, ARQ_diet_bird_BP_C_exp, ARQ_diet_bird_FP_A_exp, ARQ_diet_bird_FP_C_exp, ARQ_diet_bird_AR_A_exp, ARQ_diet_bird_AR_C_exp):
    data = {
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods', 'Fruits/Pods', 'Arthropods', 'Arthropods',],
        "Acute":   ['%.2e' % ARQ_diet_bird_SG_A, '%.2e' % ARQ_diet_bird_SG_A_exp, '%.2e' % ARQ_diet_bird_TG_A, '%.2e' % ARQ_diet_bird_TG_A_exp, '%.2e' % ARQ_diet_bird_BP_A, '%.2e' % ARQ_diet_bird_BP_A_exp, '%.2e' % ARQ_diet_bird_FP_A, '%.2e' % ARQ_diet_bird_FP_A_exp, '%.2e' % ARQ_diet_bird_AR_A, '%.2e' % ARQ_diet_bird_AR_A_exp,],
        "Chronic": ['%.2e' % ARQ_diet_bird_SG_C, '%.2e' % ARQ_diet_bird_SG_C_exp, '%.2e' % ARQ_diet_bird_TG_C, '%.2e' % ARQ_diet_bird_TG_C_exp, '%.2e' % ARQ_diet_bird_BP_C, '%.2e' % ARQ_diet_bird_BP_C_exp, '%.2e' % ARQ_diet_bird_FP_C, '%.2e' % ARQ_diet_bird_FP_C_exp, '%.2e' % ARQ_diet_bird_AR_C, '%.2e' % ARQ_diet_bird_AR_C_exp,],
    }
    return data  

def gett9data_qaqc(EEC_dose_mamm_SG_sm,EEC_dose_mamm_SG_md,EEC_dose_mamm_SG_lg,EEC_dose_mamm_TG_sm,EEC_dose_mamm_TG_md,EEC_dose_mamm_TG_lg,EEC_dose_mamm_BP_sm,EEC_dose_mamm_BP_md,EEC_dose_mamm_BP_lg,EEC_dose_mamm_FP_sm,EEC_dose_mamm_FP_md,EEC_dose_mamm_FP_lg,EEC_dose_mamm_AR_sm,EEC_dose_mamm_AR_md,EEC_dose_mamm_AR_lg,EEC_dose_mamm_SE_sm,EEC_dose_mamm_SE_md,EEC_dose_mamm_SE_lg,
                   EEC_dose_mamm_SG_sm_exp, EEC_dose_mamm_SG_md_exp, EEC_dose_mamm_SG_lg_exp, EEC_dose_mamm_TG_sm_exp, EEC_dose_mamm_TG_md_exp, EEC_dose_mamm_TG_lg_exp, EEC_dose_mamm_BP_sm_exp, EEC_dose_mamm_BP_md_exp, EEC_dose_mamm_BP_lg_exp, EEC_dose_mamm_FP_sm_exp, EEC_dose_mamm_FP_md_exp, EEC_dose_mamm_FP_lg_exp, EEC_dose_mamm_AR_sm_exp, EEC_dose_mamm_AR_md_exp, EEC_dose_mamm_AR_lg_exp, EEC_dose_mamm_SE_sm_exp, EEC_dose_mamm_SE_md_exp, EEC_dose_mamm_SE_lg_exp):
    data = { 
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods', 'Fruits/Pods', 'Arthropods', 'Arthropods', 'Seeds', 'Seeds',],
        "Small":  ['%.2e' % EEC_dose_mamm_SG_sm, '%.2e' % EEC_dose_mamm_SG_sm_exp, '%.2e' % EEC_dose_mamm_TG_sm, '%.2e' % EEC_dose_mamm_TG_sm_exp, '%.2e' % EEC_dose_mamm_BP_sm, '%.2e' % EEC_dose_mamm_BP_sm_exp, '%.2e' % EEC_dose_mamm_FP_sm, '%.2e' % EEC_dose_mamm_FP_sm_exp, '%.2e' % EEC_dose_mamm_AR_sm, '%.2e' % EEC_dose_mamm_AR_sm_exp, '%.2e' % EEC_dose_mamm_SE_sm, '%.2e' % EEC_dose_mamm_SE_sm_exp],
        "Medium": ['%.2e' % EEC_dose_mamm_SG_md, '%.2e' % EEC_dose_mamm_SG_md_exp, '%.2e' % EEC_dose_mamm_TG_md, '%.2e' % EEC_dose_mamm_TG_md_exp, '%.2e' % EEC_dose_mamm_BP_md, '%.2e' % EEC_dose_mamm_BP_md_exp, '%.2e' % EEC_dose_mamm_FP_md, '%.2e' % EEC_dose_mamm_FP_md_exp, '%.2e' % EEC_dose_mamm_AR_md, '%.2e' % EEC_dose_mamm_AR_md_exp, '%.2e' % EEC_dose_mamm_SE_md, '%.2e' % EEC_dose_mamm_SE_md_exp],
        "Large":  ['%.2e' % EEC_dose_mamm_SG_lg, '%.2e' % EEC_dose_mamm_SG_lg_exp, '%.2e' % EEC_dose_mamm_TG_lg, '%.2e' % EEC_dose_mamm_TG_lg_exp, '%.2e' % EEC_dose_mamm_BP_lg, '%.2e' % EEC_dose_mamm_BP_lg_exp, '%.2e' % EEC_dose_mamm_FP_lg, '%.2e' % EEC_dose_mamm_FP_lg_exp, '%.2e' % EEC_dose_mamm_AR_lg, '%.2e' % EEC_dose_mamm_AR_lg_exp, '%.2e' % EEC_dose_mamm_SE_lg, '%.2e' % EEC_dose_mamm_SE_lg_exp],
    }
    return data

def gett10data_qaqc(ARQ_dose_mamm_SG_sm,CRQ_dose_mamm_SG_sm,ARQ_dose_mamm_SG_md,CRQ_dose_mamm_SG_md,ARQ_dose_mamm_SG_lg,CRQ_dose_mamm_SG_lg,ARQ_dose_mamm_TG_sm,CRQ_dose_mamm_TG_sm,ARQ_dose_mamm_TG_md,CRQ_dose_mamm_TG_md,ARQ_dose_mamm_TG_lg,CRQ_dose_mamm_TG_lg,ARQ_dose_mamm_BP_sm,CRQ_dose_mamm_BP_sm,ARQ_dose_mamm_BP_md,CRQ_dose_mamm_BP_md,ARQ_dose_mamm_BP_lg,CRQ_dose_mamm_BP_lg,ARQ_dose_mamm_FP_sm,CRQ_dose_mamm_FP_sm,ARQ_dose_mamm_FP_md,CRQ_dose_mamm_FP_md,ARQ_dose_mamm_FP_lg,CRQ_dose_mamm_FP_lg,ARQ_dose_mamm_AR_sm,CRQ_dose_mamm_AR_sm,ARQ_dose_mamm_AR_md,CRQ_dose_mamm_AR_md,ARQ_dose_mamm_AR_lg,CRQ_dose_mamm_AR_lg,ARQ_dose_mamm_SE_sm,CRQ_dose_mamm_SE_sm,ARQ_dose_mamm_SE_md,CRQ_dose_mamm_SE_md,ARQ_dose_mamm_SE_lg,CRQ_dose_mamm_SE_lg,
                    ARQ_dose_mamm_SG_sm_exp, CRQ_dose_mamm_SG_sm_exp, ARQ_dose_mamm_SG_md_exp, CRQ_dose_mamm_SG_md_exp, ARQ_dose_mamm_SG_lg_exp, CRQ_dose_mamm_SG_lg_exp, ARQ_dose_mamm_TG_sm_exp, CRQ_dose_mamm_TG_sm_exp, ARQ_dose_mamm_TG_md_exp, CRQ_dose_mamm_TG_md_exp, ARQ_dose_mamm_TG_lg_exp, CRQ_dose_mamm_TG_lg_exp, ARQ_dose_mamm_BP_sm_exp, CRQ_dose_mamm_BP_sm_exp, ARQ_dose_mamm_BP_md_exp, CRQ_dose_mamm_BP_md_exp, ARQ_dose_mamm_BP_lg_exp, CRQ_dose_mamm_BP_lg_exp, ARQ_dose_mamm_FP_sm_exp, CRQ_dose_mamm_FP_sm_exp, ARQ_dose_mamm_FP_md_exp, CRQ_dose_mamm_FP_md_exp, ARQ_dose_mamm_FP_lg_exp, CRQ_dose_mamm_FP_lg_exp, ARQ_dose_mamm_AR_sm_exp, CRQ_dose_mamm_AR_sm_exp, ARQ_dose_mamm_AR_md_exp, CRQ_dose_mamm_AR_md_exp, ARQ_dose_mamm_AR_lg_exp, CRQ_dose_mamm_AR_lg_exp, ARQ_dose_mamm_SE_sm_exp, CRQ_dose_mamm_SE_sm_exp, ARQ_dose_mamm_SE_md_exp, CRQ_dose_mamm_SE_md_exp, ARQ_dose_mamm_SE_lg_exp, CRQ_dose_mamm_SE_lg_exp):
    data = {
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods', 'Fruits/Pods', 'Arthropods', 'Arthropods', 'Seeds', 'Seeds',],
        "Acute_sm":   ['%.2e' % ARQ_dose_mamm_SG_sm, '%.2e' % ARQ_dose_mamm_SG_sm_exp, '%.2e' % ARQ_dose_mamm_TG_sm, '%.2e' % ARQ_dose_mamm_TG_sm_exp, '%.2e' % ARQ_dose_mamm_BP_sm, '%.2e' % ARQ_dose_mamm_BP_sm_exp, '%.2e' % ARQ_dose_mamm_FP_sm, '%.2e' % ARQ_dose_mamm_FP_sm_exp, '%.2e' % ARQ_dose_mamm_AR_sm, '%.2e' % ARQ_dose_mamm_AR_sm_exp, '%.2e' % ARQ_dose_mamm_SE_sm, '%.2e' % ARQ_dose_mamm_SE_sm_exp],
        "Chronic_sm": ['%.2e' % CRQ_dose_mamm_SG_sm, '%.2e' % CRQ_dose_mamm_SG_sm_exp, '%.2e' % CRQ_dose_mamm_TG_sm, '%.2e' % CRQ_dose_mamm_TG_sm_exp, '%.2e' % CRQ_dose_mamm_BP_sm, '%.2e' % CRQ_dose_mamm_BP_sm_exp, '%.2e' % CRQ_dose_mamm_FP_sm, '%.2e' % CRQ_dose_mamm_FP_sm_exp, '%.2e' % CRQ_dose_mamm_AR_sm, '%.2e' % CRQ_dose_mamm_AR_sm_exp, '%.2e' % CRQ_dose_mamm_SE_sm, '%.2e' % CRQ_dose_mamm_SE_sm_exp],
        "Acute_md":   ['%.2e' % ARQ_dose_mamm_SG_md, '%.2e' % ARQ_dose_mamm_SG_md_exp, '%.2e' % ARQ_dose_mamm_TG_md, '%.2e' % ARQ_dose_mamm_TG_md_exp, '%.2e' % ARQ_dose_mamm_BP_md, '%.2e' % ARQ_dose_mamm_BP_md_exp, '%.2e' % ARQ_dose_mamm_FP_md, '%.2e' % ARQ_dose_mamm_FP_md_exp, '%.2e' % ARQ_dose_mamm_AR_md, '%.2e' % ARQ_dose_mamm_AR_md_exp, '%.2e' % ARQ_dose_mamm_SE_md, '%.2e' % ARQ_dose_mamm_SE_md_exp],
        "Chronic_md": ['%.2e' % CRQ_dose_mamm_SG_md, '%.2e' % CRQ_dose_mamm_SG_md_exp, '%.2e' % CRQ_dose_mamm_TG_md, '%.2e' % CRQ_dose_mamm_TG_md_exp, '%.2e' % CRQ_dose_mamm_BP_md, '%.2e' % CRQ_dose_mamm_BP_md_exp, '%.2e' % CRQ_dose_mamm_FP_md, '%.2e' % CRQ_dose_mamm_FP_md_exp, '%.2e' % CRQ_dose_mamm_AR_md, '%.2e' % CRQ_dose_mamm_AR_md_exp, '%.2e' % CRQ_dose_mamm_SE_md, '%.2e' % CRQ_dose_mamm_SE_md_exp],
        "Acute_lg":   ['%.2e' % ARQ_dose_mamm_SG_lg, '%.2e' % ARQ_dose_mamm_SG_lg_exp, '%.2e' % ARQ_dose_mamm_TG_lg, '%.2e' % ARQ_dose_mamm_TG_lg_exp, '%.2e' % ARQ_dose_mamm_BP_lg, '%.2e' % ARQ_dose_mamm_BP_lg_exp, '%.2e' % ARQ_dose_mamm_FP_lg, '%.2e' % ARQ_dose_mamm_FP_lg_exp, '%.2e' % ARQ_dose_mamm_AR_lg, '%.2e' % ARQ_dose_mamm_AR_lg_exp, '%.2e' % ARQ_dose_mamm_SE_lg, '%.2e' % ARQ_dose_mamm_SE_lg_exp],
        "Chronic_lg": ['%.2e' % CRQ_dose_mamm_SG_lg, '%.2e' % CRQ_dose_mamm_SG_lg_exp, '%.2e' % CRQ_dose_mamm_TG_lg, '%.2e' % CRQ_dose_mamm_TG_lg_exp, '%.2e' % CRQ_dose_mamm_BP_lg, '%.2e' % CRQ_dose_mamm_BP_lg_exp, '%.2e' % CRQ_dose_mamm_FP_lg, '%.2e' % CRQ_dose_mamm_FP_lg_exp, '%.2e' % CRQ_dose_mamm_AR_lg, '%.2e' % CRQ_dose_mamm_AR_lg_exp, '%.2e' % CRQ_dose_mamm_SE_lg, '%.2e' % CRQ_dose_mamm_SE_lg_exp], 
    }
    return data

def gett11data_na_qaqc(ARQ_diet_mamm_SG,CRQ_diet_bird_SG,ARQ_diet_mamm_TG,CRQ_diet_bird_TG,ARQ_diet_mamm_BP,CRQ_diet_bird_BP,ARQ_diet_mamm_FP,CRQ_diet_bird_FP,ARQ_diet_mamm_AR,CRQ_diet_bird_AR,
                       ARQ_diet_mamm_SG_exp,CRQ_diet_bird_SG_exp,ARQ_diet_mamm_TG_exp,CRQ_diet_bird_TG_exp,ARQ_diet_mamm_BP_exp,CRQ_diet_bird_BP_exp,ARQ_diet_mamm_FP_exp,CRQ_diet_bird_FP_exp,ARQ_diet_mamm_AR_exp,CRQ_diet_bird_AR_exp):
    data = {
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],
        "Application Target": ['Short Grass', 'Short Grass', 'Tall Grass', 'Tall Grass', 'Broadleaf Plants', 'Broadleaf Plants', 'Fruits/Pods/Seeds', 'Fruits/Pods/Seeds', 'Arthropods', 'Arthropods'],
        "Acute": ['%s' % ARQ_diet_mamm_SG, '%s' % ARQ_diet_mamm_SG_exp, '%s' % ARQ_diet_mamm_TG, '%s' % ARQ_diet_mamm_TG_exp, '%s' % ARQ_diet_mamm_BP, '%s' % ARQ_diet_mamm_BP_exp, '%s' % ARQ_diet_mamm_FP, '%s' % ARQ_diet_mamm_FP_exp, '%s' % ARQ_diet_mamm_AR, '%s' % ARQ_diet_mamm_AR_exp],
        "Chronic": ['%.2e' % CRQ_diet_bird_SG, '%.2e' % CRQ_diet_bird_SG_exp, '%.2e' % CRQ_diet_bird_TG, '%.2e' % CRQ_diet_bird_TG_exp, '%.2e' % CRQ_diet_bird_BP, '%.2e' % CRQ_diet_bird_BP_exp, '%.2e' % CRQ_diet_bird_FP, '%.2e' % CRQ_diet_bird_FP_exp, '%.2e' % CRQ_diet_bird_AR, '%.2e' % CRQ_diet_bird_AR_exp],
    }
    return data 

def gett12data_qaqc(LD50_rg_bird_sm,LD50_rg_mamm_sm,LD50_rg_bird_md,LD50_rg_mamm_md,LD50_rg_bird_lg,LD50_rg_mamm_lg,
                    LD50_rg_bird_sm_exp,LD50_rg_mamm_sm_exp,LD50_rg_bird_md_exp,LD50_rg_mamm_md_exp,LD50_rg_bird_lg_exp,LD50_rg_mamm_lg_exp):
    data = { 
        "Type": ['Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value', 'Calculated Value', 'Expected Value',],        "Animal Size": ['Small', 'Small', 'Medium', 'Medium', 'Large', 'Large', ] ,
        "Avian":  ['%.2e' % LD50_rg_bird_sm, '%.2e' % LD50_rg_bird_sm_exp, '%.2e' % LD50_rg_bird_md, '%.2e' % LD50_rg_bird_md_exp, '%.2e' % LD50_rg_bird_lg, '%.2e' % LD50_rg_bird_lg_exp,],
        "Mammal": ['%.2e' % LD50_rg_mamm_sm, '%.2e' % LD50_rg_mamm_sm_exp, '%.2e' % LD50_rg_mamm_md, '%.2e' % LD50_rg_mamm_md_exp, '%.2e' % LD50_rg_mamm_lg, '%.2e' % LD50_rg_mamm_lg_exp,],
    }
    return data

def gettsumdata_1(a_i, r_s, b_w, p_i, den, Foliar_dissipation_half_life, n_a, rate_out_t):

    if 'N/A' in p_i:
        p_i_mean='N/A'
        p_i_std='N/A'
        p_i_min='N/A'
        p_i_max='N/A'
    else:
        p_i_mean='%.2e' % numpy.mean(p_i)
        p_i_std='%.2e' % numpy.std(p_i)
        p_i_min='%.2e' % numpy.min(p_i)
        p_i_max='%.2e' % numpy.max(p_i)
    data = { 
        "Parameter": ['Percentage active ingredient', 'Row spacing', 'Bandwidth', 'Percentage incorporated', 
                      'Density of product', 'Foliar dissipation half-life', 'Number of application', 'Application rate', ],
        "Mean": ['%.2e' % numpy.mean(a_i), '%.2e' % numpy.mean(r_s), '%.2e' % numpy.mean(b_w), p_i_mean, '%.2e' % numpy.mean(den), '%.2e' % numpy.mean(Foliar_dissipation_half_life), '%.2e' % numpy.mean(n_a), '%.2e' % numpy.mean(rate_out_t),],
        "Std": ['%.2e' % numpy.std(a_i),'%.2e' % numpy.mean(r_s), '%.2e' % numpy.mean(b_w), p_i_std, '%.2e' % numpy.mean(den), '%.2e' % numpy.std(Foliar_dissipation_half_life), '%.2e' % numpy.std(n_a), '%.2e' % numpy.std(rate_out_t),],
        "Min": ['%.2e' % numpy.min(a_i),'%.2e' % numpy.mean(r_s), '%.2e' % numpy.mean(b_w), p_i_min, '%.2e' % numpy.mean(den), '%.2e' % numpy.min(Foliar_dissipation_half_life), '%.2e' % numpy.min(n_a), '%.2e' % numpy.min(rate_out_t),],
        "Max": ['%.2e' % numpy.max(a_i),'%.2e' % numpy.mean(r_s), '%.2e' % numpy.mean(b_w), p_i_max, '%.2e' % numpy.mean(den), '%.2e' % numpy.max(Foliar_dissipation_half_life), '%.2e' % numpy.max(n_a), '%.2e' % numpy.max(rate_out_t),],
        "Unit": ['%', 'inch', 'inch', '%', 'lbs/gal', 'days', '', ],
    }
    return data

def gettsumdata_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, 
            bw_assessed_bird_l, tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, mineau_scaling_factor):

    if 'N/A' in avian_NOAEL:
        avian_lc50_mean='N/A'
        avian_lc50_std='N/A'
        avian_lc50_min='N/A'
        avian_lc50_max='N/A'
    else:
        avian_lc50_mean='%.2e' % numpy.mean(avian_lc50)
        avian_lc50_std='%.2e' % numpy.std(avian_lc50)
        avian_lc50_min='%.2e' % numpy.min(avian_lc50)
        avian_lc50_max='%.2e' % numpy.max(avian_lc50)

    data = { 
        "Parameter": ['Avian LD50', 'Weight (LD50)', 'Avian LC50', 'Weight (LC50)',
                      'Avian NOAEC', 'Weight (NOAEC)', 'Avian NOAEL', 'Weight (NOAEL)',
                      'Body weight of assessed bird small', 'Body weight of assessed bird medium', 'Body weight of assessed bird large', 
                      'Mineau scaling factor', ],
        "Mean": ['%.2e' % numpy.mean(avian_ld50), '%.2e' % numpy.mean(tw_bird_ld50), avian_lc50_mean, '%.2e' % numpy.mean(tw_bird_lc50), '%.2e' % numpy.mean(avian_NOAEC), '%.2e' % numpy.mean(tw_bird_NOAEC), '%.2e' % numpy.mean(avian_NOAEL), '%.2e' % numpy.mean(tw_bird_NOAEL), '%.2e' % numpy.mean(bw_assessed_bird_s), '%.2e' % numpy.mean(bw_assessed_bird_m), '%.2e' % numpy.mean(bw_assessed_bird_l), '%.2e' % numpy.mean(mineau_scaling_factor), ],
        "Std": ['%.2e' % numpy.std(avian_ld50), '%.2e' % numpy.std(tw_bird_ld50), avian_lc50_std, '%.2e' % numpy.std(tw_bird_lc50), '%.2e' % numpy.std(avian_NOAEC), '%.2e' % numpy.std(tw_bird_NOAEC), '%.2e' % numpy.std(avian_NOAEL), '%.2e' % numpy.std(tw_bird_NOAEL), '%.2e' % numpy.std(bw_assessed_bird_s), '%.2e' % numpy.std(bw_assessed_bird_m), '%.2e' % numpy.std(bw_assessed_bird_l), '%.2e' % numpy.std(mineau_scaling_factor), ],
        "Min": ['%.2e' % numpy.min(avian_ld50), '%.2e' % numpy.min(tw_bird_ld50), avian_lc50_min, '%.2e' % numpy.min(tw_bird_lc50), '%.2e' % numpy.min(avian_NOAEC), '%.2e' % numpy.min(tw_bird_NOAEC), '%.2e' % numpy.min(avian_NOAEL), '%.2e' % numpy.min(tw_bird_NOAEL), '%.2e' % numpy.min(bw_assessed_bird_s), '%.2e' % numpy.min(bw_assessed_bird_m), '%.2e' % numpy.min(bw_assessed_bird_l), '%.2e' % numpy.min(mineau_scaling_factor), ],
        "Max": ['%.2e' % numpy.max(avian_ld50), '%.2e' % numpy.max(tw_bird_ld50), avian_lc50_max, '%.2e' % numpy.max(tw_bird_lc50), '%.2e' % numpy.max(avian_NOAEC), '%.2e' % numpy.max(tw_bird_NOAEC), '%.2e' % numpy.max(avian_NOAEL), '%.2e' % numpy.max(tw_bird_NOAEL), '%.2e' % numpy.max(bw_assessed_bird_s), '%.2e' % numpy.max(bw_assessed_bird_m), '%.2e' % numpy.max(bw_assessed_bird_l), '%.2e' % numpy.max(mineau_scaling_factor), ],
        "Unit": ['mg/kg-bw', 'g', 'mg/kg-diet', 'g', 'mg/kg-diet', 'g', 'mg/kg-bw', 'g', 'g', 'g', 'g', '', ],
    }
    return data

def gettsumdata_3(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, 
              bw_assessed_mamm_l, bw_tested_mamm):

    if 'N/A' in mammalian_lc50:
        mammalian_lc50_mean='N/A'
        mammalian_lc50_std='N/A'
        mammalian_lc50_min='N/A'
        mammalian_lc50_max='N/A'
    else:
        mammalian_lc50_mean='%.2e' % numpy.mean(mammalian_lc50)
        mammalian_lc50_std='%.2e' % numpy.std(mammalian_lc50)
        mammalian_lc50_min='%.2e' % numpy.min(mammalian_lc50)
        mammalian_lc50_max='%.2e' % numpy.max(mammalian_lc50)

    data = { 
        "Parameter": ['Mammalian LD50', 'Mammalian LC50', 'Mammalian NOAEC', 'Mammalian NOAEL', 'Body weight of assessed mammal small',
                      'Body weight of assessed mammal medium', 'Body weight of assessed mammal large', 
                      'Body weight of tested mammal', ],
        "Mean": ['%.2e' % numpy.mean(mammalian_ld50), mammalian_lc50_mean, '%.2e' % numpy.mean(mammalian_NOAEC), '%.2e' % numpy.mean(mammalian_NOAEL), '%.2e' % numpy.mean(bw_assessed_mamm_s), '%.2e' % numpy.mean(bw_assessed_mamm_m), '%.2e' % numpy.mean(bw_assessed_mamm_l), '%.2e' % numpy.mean(bw_tested_mamm), ],
        "Std": ['%.2e' % numpy.std(mammalian_ld50), mammalian_lc50_std, '%.2e' % numpy.std(mammalian_NOAEC), '%.2e' % numpy.std(mammalian_NOAEL), '%.2e' % numpy.std(bw_assessed_mamm_s), '%.2e' % numpy.std(bw_assessed_mamm_m), '%.2e' % numpy.std(bw_assessed_mamm_l), '%.2e' % numpy.std(bw_tested_mamm), ],
        "Min": ['%.2e' % numpy.min(mammalian_ld50), mammalian_lc50_min, '%.2e' % numpy.min(mammalian_NOAEC), '%.2e' % numpy.min(mammalian_NOAEL), '%.2e' % numpy.min(bw_assessed_mamm_s), '%.2e' % numpy.min(bw_assessed_mamm_m), '%.2e' % numpy.min(bw_assessed_mamm_l), '%.2e' % numpy.min(bw_tested_mamm), ],
        "Max": ['%.2e' % numpy.max(mammalian_ld50), mammalian_lc50_max, '%.2e' % numpy.max(mammalian_NOAEC), '%.2e' % numpy.max(mammalian_NOAEL), '%.2e' % numpy.max(bw_assessed_mamm_s), '%.2e' % numpy.max(bw_assessed_mamm_m), '%.2e' % numpy.max(bw_assessed_mamm_l), '%.2e' % numpy.max(bw_tested_mamm), ],
        "Unit": ['mg/kg-bw', 'mg/kg-diet', 'mg/kg-diet', 'mg/kg-bw', 'g', 'g', 'g', 'g', ],
    }
    return data

def gettsumdata_5(sa_bird_1_s_out, sa_bird_2_s_out, sc_bird_s_out, sa_mamm_1_s_out, sa_mamm_2_s_out, sc_mamm_s_out, sa_bird_1_m_out, sa_bird_2_m_out, sc_bird_m_out, sa_mamm_1_m_out, sa_mamm_2_m_out, sc_mamm_m_out, sa_bird_1_l_out, sa_bird_2_l_out, sc_bird_l_out, sa_mamm_1_l_out, sa_mamm_2_l_out, sc_mamm_l_out):
    data = { 
        "Size": ['Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "AAcute #1": ['%.2e' % numpy.mean(sa_bird_1_s_out), '%.2e' % numpy.std(sa_bird_1_s_out), '%.2e' % numpy.min(sa_bird_1_s_out), '%.2e' % numpy.max(sa_bird_1_s_out), 
                      '%.2e' % numpy.mean(sa_bird_1_m_out), '%.2e' % numpy.std(sa_bird_1_m_out), '%.2e' % numpy.min(sa_bird_1_m_out), '%.2e' % numpy.max(sa_bird_1_m_out),
                      '%.2e' % numpy.mean(sa_bird_1_l_out), '%.2e' % numpy.std(sa_bird_1_l_out), '%.2e' % numpy.min(sa_bird_1_l_out), '%.2e' % numpy.max(sa_bird_1_l_out),],
        
        "AAcute #2": ['%.2e' % numpy.mean(sa_bird_2_s_out), '%.2e' % numpy.std(sa_bird_2_s_out), '%.2e' % numpy.min(sa_bird_2_s_out), '%.2e' % numpy.max(sa_bird_2_s_out),
                      '%.2e' % numpy.mean(sa_bird_2_m_out), '%.2e' % numpy.std(sa_bird_2_m_out), '%.2e' % numpy.min(sa_bird_2_m_out), '%.2e' % numpy.max(sa_bird_2_m_out),
                      '%.2e' % numpy.mean(sa_bird_2_l_out), '%.2e' % numpy.std(sa_bird_2_l_out), '%.2e' % numpy.min(sa_bird_2_l_out), '%.2e' % numpy.max(sa_bird_2_l_out),],
        
        "AChronic":  ['%.2e' % numpy.mean(sc_bird_s_out), '%.2e' % numpy.std(sc_bird_s_out), '%.2e' % numpy.min(sc_bird_s_out), '%.2e' % numpy.max(sc_bird_s_out),
                      '%.2e' % numpy.mean(sc_bird_m_out), '%.2e' % numpy.std(sc_bird_m_out), '%.2e' % numpy.min(sc_bird_m_out), '%.2e' % numpy.max(sc_bird_m_out),
                      '%.2e' % numpy.mean(sc_bird_l_out), '%.2e' % numpy.std(sc_bird_l_out), '%.2e' % numpy.min(sc_bird_l_out), '%.2e' % numpy.max(sc_bird_l_out),],
        
        "MAcute #1": ['%.2e' % numpy.mean(sa_mamm_1_s_out), '%.2e' % numpy.std(sa_mamm_1_s_out), '%.2e' % numpy.min(sa_mamm_1_s_out), '%.2e' % numpy.max(sa_mamm_1_s_out),
                      '%.2e' % numpy.mean(sa_mamm_1_m_out), '%.2e' % numpy.std(sa_mamm_1_m_out), '%.2e' % numpy.min(sa_mamm_1_m_out), '%.2e' % numpy.max(sa_mamm_1_m_out),
                      '%.2e' % numpy.mean(sa_mamm_1_l_out), '%.2e' % numpy.std(sa_mamm_1_l_out), '%.2e' % numpy.min(sa_mamm_1_l_out), '%.2e' % numpy.max(sa_mamm_1_l_out),],
        
        "MAcute #2": ['%.2e' % numpy.mean(sa_mamm_2_s_out), '%.2e' % numpy.std(sa_mamm_2_s_out), '%.2e' % numpy.min(sa_mamm_2_s_out), '%.2e' % numpy.max(sa_mamm_2_s_out),
                      '%.2e' % numpy.mean(sa_mamm_2_m_out), '%.2e' % numpy.std(sa_mamm_2_m_out), '%.2e' % numpy.min(sa_mamm_2_m_out), '%.2e' % numpy.max(sa_mamm_2_m_out),
                      '%.2e' % numpy.mean(sa_mamm_2_l_out), '%.2e' % numpy.std(sa_mamm_2_l_out), '%.2e' % numpy.min(sa_mamm_2_l_out), '%.2e' % numpy.max(sa_mamm_2_l_out),],
        
        "MChronic":  ['%.2e' % numpy.mean(sc_mamm_s_out), '%.2e' % numpy.std(sc_mamm_s_out), '%.2e' % numpy.min(sc_mamm_s_out), '%.2e' % numpy.max(sc_mamm_s_out),
                      '%.2e' % numpy.mean(sc_mamm_m_out), '%.2e' % numpy.std(sc_mamm_m_out), '%.2e' % numpy.min(sc_mamm_m_out), '%.2e' % numpy.max(sc_mamm_m_out),
                      '%.2e' % numpy.mean(sc_mamm_l_out), '%.2e' % numpy.std(sc_mamm_l_out), '%.2e' % numpy.min(sc_mamm_l_out), '%.2e' % numpy.max(sc_mamm_l_out),],
    }
    return data

def gettsumdata_6(EEC_diet_SG_RBG_out, EEC_diet_TG_RBG_out, EEC_diet_BP_RBG_out, EEC_diet_FR_RBG_out, EEC_diet_AR_RBG_out):
    data = { 
        "Metric": ['Mean', 'Std', 'Min', 'Max',],
        "Short Grass": ['%.2e' % numpy.mean(EEC_diet_SG_RBG_out), '%.2e' % numpy.std(EEC_diet_SG_RBG_out), '%.2e' % numpy.min(EEC_diet_SG_RBG_out), '%.2e' % numpy.max(EEC_diet_SG_RBG_out),],
        "Tall Grass": ['%.2e' % numpy.mean(EEC_diet_TG_RBG_out), '%.2e' % numpy.std(EEC_diet_TG_RBG_out), '%.2e' % numpy.min(EEC_diet_TG_RBG_out), '%.2e' % numpy.max(EEC_diet_TG_RBG_out),],
        "Broadleaf Plants": ['%.2e' % numpy.mean(EEC_diet_BP_RBG_out), '%.2e' % numpy.std(EEC_diet_BP_RBG_out), '%.2e' % numpy.min(EEC_diet_BP_RBG_out), '%.2e' % numpy.max(EEC_diet_BP_RBG_out),],
        "Fruits/Pods/Seeds": ['%.2e' % numpy.mean(EEC_diet_FR_RBG_out), '%.2e' % numpy.std(EEC_diet_FR_RBG_out), '%.2e' % numpy.min(EEC_diet_FR_RBG_out), '%.2e' % numpy.max(EEC_diet_FR_RBG_out),],
        "Arthropods": ['%.2e' % numpy.mean(EEC_diet_AR_RBG_out), '%.2e' % numpy.std(EEC_diet_AR_RBG_out), '%.2e' % numpy.min(EEC_diet_AR_RBG_out), '%.2e' % numpy.max(EEC_diet_AR_RBG_out),],
    }
    return data

def gettsumdata_7(EEC_dose_bird_SG_sm_out, EEC_dose_bird_SG_md_out, EEC_dose_bird_SG_lg_out, EEC_dose_bird_TG_sm_out, EEC_dose_bird_TG_md_out, EEC_dose_bird_TG_lg_out, EEC_dose_bird_BP_sm_out, EEC_dose_bird_BP_md_out, EEC_dose_bird_BP_lg_out, EEC_dose_bird_FP_sm_out, EEC_dose_bird_FP_md_out, EEC_dose_bird_FP_lg_out, EEC_dose_bird_AR_sm_out, EEC_dose_bird_AR_md_out, EEC_dose_bird_AR_lg_out, EEC_dose_bird_SE_sm_out, EEC_dose_bird_SE_md_out, EEC_dose_bird_SE_lg_out):
    data = { 
        "Animal Size": ['Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Short Grass": ['%.2e' % numpy.mean(EEC_dose_bird_SG_sm_out), '%.2e' % numpy.std(EEC_dose_bird_SG_sm_out), '%.2e' % numpy.min(EEC_dose_bird_SG_sm_out), '%.2e' % numpy.max(EEC_dose_bird_SG_sm_out),
                        '%.2e' % numpy.mean(EEC_dose_bird_SG_md_out), '%.2e' % numpy.std(EEC_dose_bird_SG_md_out), '%.2e' % numpy.min(EEC_dose_bird_SG_md_out), '%.2e' % numpy.max(EEC_dose_bird_SG_md_out),
                        '%.2e' % numpy.mean(EEC_dose_bird_SG_lg_out), '%.2e' % numpy.std(EEC_dose_bird_SG_lg_out), '%.2e' % numpy.min(EEC_dose_bird_SG_lg_out), '%.2e' % numpy.max(EEC_dose_bird_SG_lg_out),],
        
        "Tall Grass": ['%.2e' % numpy.mean(EEC_dose_bird_TG_sm_out), '%.2e' % numpy.std(EEC_dose_bird_TG_sm_out), '%.2e' % numpy.min(EEC_dose_bird_TG_sm_out), '%.2e' % numpy.max(EEC_dose_bird_TG_sm_out),
                       '%.2e' % numpy.mean(EEC_dose_bird_TG_md_out), '%.2e' % numpy.std(EEC_dose_bird_TG_md_out), '%.2e' % numpy.min(EEC_dose_bird_TG_md_out), '%.2e' % numpy.max(EEC_dose_bird_TG_md_out),
                       '%.2e' % numpy.mean(EEC_dose_bird_TG_lg_out), '%.2e' % numpy.std(EEC_dose_bird_TG_lg_out), '%.2e' % numpy.min(EEC_dose_bird_TG_lg_out), '%.2e' % numpy.max(EEC_dose_bird_TG_lg_out),],
        
        "Broadleaf Plants": ['%.2e' % numpy.mean(EEC_dose_bird_BP_sm_out), '%.2e' % numpy.std(EEC_dose_bird_BP_sm_out), '%.2e' % numpy.min(EEC_dose_bird_BP_sm_out), '%.2e' % numpy.max(EEC_dose_bird_BP_sm_out),
                             '%.2e' % numpy.mean(EEC_dose_bird_BP_md_out), '%.2e' % numpy.std(EEC_dose_bird_BP_md_out), '%.2e' % numpy.min(EEC_dose_bird_BP_md_out), '%.2e' % numpy.max(EEC_dose_bird_BP_md_out),
                             '%.2e' % numpy.mean(EEC_dose_bird_BP_lg_out), '%.2e' % numpy.std(EEC_dose_bird_BP_lg_out), '%.2e' % numpy.min(EEC_dose_bird_BP_lg_out), '%.2e' % numpy.max(EEC_dose_bird_BP_lg_out),],

        "Fruits/Pods": ['%.2e' % numpy.mean(EEC_dose_bird_FP_sm_out), '%.2e' % numpy.std(EEC_dose_bird_FP_sm_out), '%.2e' % numpy.min(EEC_dose_bird_FP_sm_out), '%.2e' % numpy.max(EEC_dose_bird_FP_sm_out),
                              '%.2e' % numpy.mean(EEC_dose_bird_FP_md_out), '%.2e' % numpy.std(EEC_dose_bird_FP_md_out), '%.2e' % numpy.min(EEC_dose_bird_FP_md_out), '%.2e' % numpy.max(EEC_dose_bird_FP_md_out),
                              '%.2e' % numpy.mean(EEC_dose_bird_FP_lg_out), '%.2e' % numpy.std(EEC_dose_bird_FP_lg_out), '%.2e' % numpy.min(EEC_dose_bird_FP_lg_out), '%.2e' % numpy.max(EEC_dose_bird_FP_lg_out),],

        "Arthropods": ['%.2e' % numpy.mean(EEC_dose_bird_AR_sm_out), '%.2e' % numpy.std(EEC_dose_bird_AR_sm_out), '%.2e' % numpy.min(EEC_dose_bird_AR_sm_out), '%.2e' % numpy.max(EEC_dose_bird_AR_sm_out),
                       '%.2e' % numpy.mean(EEC_dose_bird_AR_md_out), '%.2e' % numpy.std(EEC_dose_bird_AR_md_out), '%.2e' % numpy.min(EEC_dose_bird_AR_md_out), '%.2e' % numpy.max(EEC_dose_bird_AR_md_out),
                       '%.2e' % numpy.mean(EEC_dose_bird_AR_lg_out), '%.2e' % numpy.std(EEC_dose_bird_AR_lg_out), '%.2e' % numpy.min(EEC_dose_bird_AR_lg_out), '%.2e' % numpy.max(EEC_dose_bird_AR_lg_out),],

        "Seeds": ['%.2e' % numpy.mean(EEC_dose_bird_SE_sm_out), '%.2e' % numpy.std(EEC_dose_bird_SE_sm_out), '%.2e' % numpy.min(EEC_dose_bird_SE_sm_out), '%.2e' % numpy.max(EEC_dose_bird_SE_sm_out),
                  '%.2e' % numpy.mean(EEC_dose_bird_SE_md_out), '%.2e' % numpy.std(EEC_dose_bird_SE_md_out), '%.2e' % numpy.min(EEC_dose_bird_SE_md_out), '%.2e' % numpy.max(EEC_dose_bird_SE_md_out),
                  '%.2e' % numpy.mean(EEC_dose_bird_SE_lg_out), '%.2e' % numpy.std(EEC_dose_bird_SE_lg_out), '%.2e' % numpy.min(EEC_dose_bird_SE_lg_out), '%.2e' % numpy.max(EEC_dose_bird_SE_lg_out),],
    }
    return data

def gettsumdata_8(ARQ_diet_bird_SG_A_out, ARQ_diet_bird_SG_C_out, ARQ_diet_bird_TG_A_out, ARQ_diet_bird_TG_C_out, ARQ_diet_bird_BP_A_out, ARQ_diet_bird_BP_C_out, ARQ_diet_bird_FP_A_out, ARQ_diet_bird_FP_C_out, ARQ_diet_bird_AR_A_out, ARQ_diet_bird_AR_C_out):
    data = { 
        "Type": ['Acute', 'Acute', 'Acute', 'Acute', 'Chronic', 'Chronic', 'Chronic', 'Chronic',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Short Grass": ['%.2e' % numpy.mean(ARQ_diet_bird_SG_A_out), '%.2e' % numpy.std(ARQ_diet_bird_SG_A_out), '%.2e' % numpy.min(ARQ_diet_bird_SG_A_out), '%.2e' % numpy.max(ARQ_diet_bird_SG_A_out),
                        '%.2e' % numpy.mean(ARQ_diet_bird_SG_C_out), '%.2e' % numpy.std(ARQ_diet_bird_SG_C_out), '%.2e' % numpy.min(ARQ_diet_bird_SG_C_out), '%.2e' % numpy.max(ARQ_diet_bird_SG_C_out),],
        
        "Tall Grass": ['%.2e' % numpy.mean(ARQ_diet_bird_TG_A_out), '%.2e' % numpy.std(ARQ_diet_bird_TG_A_out), '%.2e' % numpy.min(ARQ_diet_bird_TG_A_out), '%.2e' % numpy.max(ARQ_diet_bird_TG_A_out),
                       '%.2e' % numpy.mean(ARQ_diet_bird_TG_C_out), '%.2e' % numpy.std(ARQ_diet_bird_TG_C_out), '%.2e' % numpy.min(ARQ_diet_bird_TG_C_out), '%.2e' % numpy.max(ARQ_diet_bird_TG_C_out),],
        
        "Broadleaf Plants": ['%.2e' % numpy.mean(ARQ_diet_bird_BP_A_out), '%.2e' % numpy.std(ARQ_diet_bird_BP_A_out), '%.2e' % numpy.min(ARQ_diet_bird_BP_A_out), '%.2e' % numpy.max(ARQ_diet_bird_BP_A_out),
                             '%.2e' % numpy.mean(ARQ_diet_bird_BP_C_out), '%.2e' % numpy.std(ARQ_diet_bird_BP_C_out), '%.2e' % numpy.min(ARQ_diet_bird_BP_C_out), '%.2e' % numpy.max(ARQ_diet_bird_BP_C_out),],

        "Fruits/Pods": ['%.2e' % numpy.mean(ARQ_diet_bird_FP_A_out), '%.2e' % numpy.std(ARQ_diet_bird_FP_A_out), '%.2e' % numpy.min(ARQ_diet_bird_FP_A_out), '%.2e' % numpy.max(ARQ_diet_bird_FP_A_out),
                              '%.2e' % numpy.mean(ARQ_diet_bird_FP_C_out), '%.2e' % numpy.std(ARQ_diet_bird_FP_C_out), '%.2e' % numpy.min(ARQ_diet_bird_FP_C_out), '%.2e' % numpy.max(ARQ_diet_bird_FP_C_out),],

        "Arthropods": ['%.2e' % numpy.mean(ARQ_diet_bird_AR_A_out), '%.2e' % numpy.std(ARQ_diet_bird_AR_A_out), '%.2e' % numpy.min(ARQ_diet_bird_AR_A_out), '%.2e' % numpy.max(ARQ_diet_bird_AR_A_out),
                       '%.2e' % numpy.mean(ARQ_diet_bird_AR_C_out), '%.2e' % numpy.std(ARQ_diet_bird_AR_C_out), '%.2e' % numpy.min(ARQ_diet_bird_AR_C_out), '%.2e' % numpy.max(ARQ_diet_bird_AR_C_out),],
    }
    return data    

def gettsumdata_9(EEC_dose_mamm_SG_sm_out, EEC_dose_mamm_SG_md_out, EEC_dose_mamm_SG_lg_out, EEC_dose_mamm_TG_sm_out, EEC_dose_mamm_TG_md_out, EEC_dose_mamm_TG_lg_out, EEC_dose_mamm_BP_sm_out, EEC_dose_mamm_BP_md_out, EEC_dose_mamm_BP_lg_out, EEC_dose_mamm_FP_sm_out, EEC_dose_mamm_FP_md_out, EEC_dose_mamm_FP_lg_out, EEC_dose_mamm_AR_sm_out, EEC_dose_mamm_AR_md_out, EEC_dose_mamm_AR_lg_out, EEC_dose_mamm_SE_sm_out, EEC_dose_mamm_SE_md_out, EEC_dose_mamm_SE_lg_out):
    data = { 
        "Animal Size": ['Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Short Grass": ['%.2e' % numpy.mean(EEC_dose_mamm_SG_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_SG_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_SG_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_SG_sm_out),
                        '%.2e' % numpy.mean(EEC_dose_mamm_SG_md_out), '%.2e' % numpy.std(EEC_dose_mamm_SG_md_out), '%.2e' % numpy.min(EEC_dose_mamm_SG_md_out), '%.2e' % numpy.max(EEC_dose_mamm_SG_md_out),
                        '%.2e' % numpy.mean(EEC_dose_mamm_SG_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_SG_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_SG_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_SG_lg_out),],
        
        "Tall Grass": ['%.2e' % numpy.mean(EEC_dose_mamm_TG_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_TG_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_TG_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_TG_sm_out),
                       '%.2e' % numpy.mean(EEC_dose_mamm_TG_md_out), '%.2e' % numpy.std(EEC_dose_mamm_TG_md_out), '%.2e' % numpy.min(EEC_dose_mamm_TG_md_out), '%.2e' % numpy.max(EEC_dose_mamm_TG_md_out),
                       '%.2e' % numpy.mean(EEC_dose_mamm_TG_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_TG_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_TG_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_TG_lg_out),],
        
        "Broadleaf Plants": ['%.2e' % numpy.mean(EEC_dose_mamm_BP_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_BP_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_BP_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_BP_sm_out),
                             '%.2e' % numpy.mean(EEC_dose_mamm_BP_md_out), '%.2e' % numpy.std(EEC_dose_mamm_BP_md_out), '%.2e' % numpy.min(EEC_dose_mamm_BP_md_out), '%.2e' % numpy.max(EEC_dose_mamm_BP_md_out),
                             '%.2e' % numpy.mean(EEC_dose_mamm_BP_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_BP_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_BP_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_BP_lg_out),],

        "Fruits/Pods": ['%.2e' % numpy.mean(EEC_dose_mamm_FP_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_FP_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_FP_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_FP_sm_out),
                              '%.2e' % numpy.mean(EEC_dose_mamm_FP_md_out), '%.2e' % numpy.std(EEC_dose_mamm_FP_md_out), '%.2e' % numpy.min(EEC_dose_mamm_FP_md_out), '%.2e' % numpy.max(EEC_dose_mamm_FP_md_out),
                              '%.2e' % numpy.mean(EEC_dose_mamm_FP_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_FP_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_FP_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_FP_lg_out),],

        "Arthropods": ['%.2e' % numpy.mean(EEC_dose_mamm_AR_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_AR_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_AR_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_AR_sm_out),
                       '%.2e' % numpy.mean(EEC_dose_mamm_AR_md_out), '%.2e' % numpy.std(EEC_dose_mamm_AR_md_out), '%.2e' % numpy.min(EEC_dose_mamm_AR_md_out), '%.2e' % numpy.max(EEC_dose_mamm_AR_md_out),
                       '%.2e' % numpy.mean(EEC_dose_mamm_AR_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_AR_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_AR_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_AR_lg_out),],

        "Seeds": ['%.2e' % numpy.mean(EEC_dose_mamm_SE_sm_out), '%.2e' % numpy.std(EEC_dose_mamm_SE_sm_out), '%.2e' % numpy.min(EEC_dose_mamm_SE_sm_out), '%.2e' % numpy.max(EEC_dose_mamm_SE_sm_out),
                  '%.2e' % numpy.mean(EEC_dose_mamm_SE_md_out), '%.2e' % numpy.std(EEC_dose_mamm_SE_md_out), '%.2e' % numpy.min(EEC_dose_mamm_SE_md_out), '%.2e' % numpy.max(EEC_dose_mamm_SE_md_out),
                  '%.2e' % numpy.mean(EEC_dose_mamm_SE_lg_out), '%.2e' % numpy.std(EEC_dose_mamm_SE_lg_out), '%.2e' % numpy.min(EEC_dose_mamm_SE_lg_out), '%.2e' % numpy.max(EEC_dose_mamm_SE_lg_out),],
    }
    return data

def gettsumdata_10(ARQ_dose_mamm_SG_sm, CRQ_dose_mamm_SG_sm, ARQ_dose_mamm_SG_md, CRQ_dose_mamm_SG_md, ARQ_dose_mamm_SG_lg, CRQ_dose_mamm_SG_lg, ARQ_dose_mamm_TG_sm, CRQ_dose_mamm_TG_sm, ARQ_dose_mamm_TG_md, CRQ_dose_mamm_TG_md, ARQ_dose_mamm_TG_lg, CRQ_dose_mamm_TG_lg, ARQ_dose_mamm_BP_sm, CRQ_dose_mamm_BP_sm, ARQ_dose_mamm_BP_md, CRQ_dose_mamm_BP_md, ARQ_dose_mamm_BP_lg, CRQ_dose_mamm_BP_lg, ARQ_dose_mamm_FP_sm, CRQ_dose_mamm_FP_sm, ARQ_dose_mamm_FP_md, CRQ_dose_mamm_FP_md, ARQ_dose_mamm_FP_lg, CRQ_dose_mamm_FP_lg, ARQ_dose_mamm_AR_sm, CRQ_dose_mamm_AR_sm, ARQ_dose_mamm_AR_md, CRQ_dose_mamm_AR_md, ARQ_dose_mamm_AR_lg, CRQ_dose_mamm_AR_lg, ARQ_dose_mamm_SE_sm, CRQ_dose_mamm_SE_sm, ARQ_dose_mamm_SE_md, CRQ_dose_mamm_SE_md, ARQ_dose_mamm_SE_lg, CRQ_dose_mamm_SE_lg):
    data = { 
        "Animal Size": ['Small', 'Small', 'Small', 'Small', 'Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large', 'Large', 'Large', 'Large', 'Large',],
        "Type": ['Acute', 'Acute', 'Acute', 'Acute', 'Chronic', 'Chronic', 'Chronic', 'Chronic', 'Acute', 'Acute', 'Acute', 'Acute', 'Chronic', 'Chronic', 'Chronic', 'Chronic', 'Acute', 'Acute', 'Acute', 'Acute', 'Chronic', 'Chronic', 'Chronic', 'Chronic',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        
        "Short Grass": ['%.2e' % numpy.mean(ARQ_dose_mamm_SG_sm), '%.2e' % numpy.std(ARQ_dose_mamm_SG_sm), '%.2e' % numpy.min(ARQ_dose_mamm_SG_sm), '%.2e' % numpy.max(ARQ_dose_mamm_SG_sm),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_SG_sm), '%.2e' % numpy.std(CRQ_dose_mamm_SG_sm), '%.2e' % numpy.min(CRQ_dose_mamm_SG_sm), '%.2e' % numpy.max(CRQ_dose_mamm_SG_sm),
                        '%.2e' % numpy.mean(ARQ_dose_mamm_SG_md), '%.2e' % numpy.std(ARQ_dose_mamm_SG_md), '%.2e' % numpy.min(ARQ_dose_mamm_SG_md), '%.2e' % numpy.max(ARQ_dose_mamm_SG_md),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_SG_md), '%.2e' % numpy.std(CRQ_dose_mamm_SG_md), '%.2e' % numpy.min(CRQ_dose_mamm_SG_md), '%.2e' % numpy.max(CRQ_dose_mamm_SG_md),
                        '%.2e' % numpy.mean(ARQ_dose_mamm_SG_lg), '%.2e' % numpy.std(ARQ_dose_mamm_SG_lg), '%.2e' % numpy.min(ARQ_dose_mamm_SG_lg), '%.2e' % numpy.max(ARQ_dose_mamm_SG_lg),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_SG_lg), '%.2e' % numpy.std(CRQ_dose_mamm_SG_lg), '%.2e' % numpy.min(CRQ_dose_mamm_SG_lg), '%.2e' % numpy.max(CRQ_dose_mamm_SG_lg),],
        
        "Tall Grass": ['%.2e' % numpy.mean(ARQ_dose_mamm_TG_sm), '%.2e' % numpy.std(ARQ_dose_mamm_TG_sm), '%.2e' % numpy.min(ARQ_dose_mamm_TG_sm), '%.2e' % numpy.max(ARQ_dose_mamm_TG_sm),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_TG_sm), '%.2e' % numpy.std(CRQ_dose_mamm_TG_sm), '%.2e' % numpy.min(CRQ_dose_mamm_TG_sm), '%.2e' % numpy.max(CRQ_dose_mamm_TG_sm),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_TG_md), '%.2e' % numpy.std(ARQ_dose_mamm_TG_md), '%.2e' % numpy.min(ARQ_dose_mamm_TG_md), '%.2e' % numpy.max(ARQ_dose_mamm_TG_md),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_TG_md), '%.2e' % numpy.std(CRQ_dose_mamm_TG_md), '%.2e' % numpy.min(CRQ_dose_mamm_TG_md), '%.2e' % numpy.max(CRQ_dose_mamm_TG_md),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_TG_lg), '%.2e' % numpy.std(ARQ_dose_mamm_TG_lg), '%.2e' % numpy.min(ARQ_dose_mamm_TG_lg), '%.2e' % numpy.max(ARQ_dose_mamm_TG_lg),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_TG_lg), '%.2e' % numpy.std(CRQ_dose_mamm_TG_lg), '%.2e' % numpy.min(CRQ_dose_mamm_TG_lg), '%.2e' % numpy.max(CRQ_dose_mamm_TG_lg),],

        "Broadleaf Plants": ['%.2e' % numpy.mean(ARQ_dose_mamm_BP_sm), '%.2e' % numpy.std(ARQ_dose_mamm_BP_sm), '%.2e' % numpy.min(ARQ_dose_mamm_BP_sm), '%.2e' % numpy.max(ARQ_dose_mamm_BP_sm),
                             '%.2e' % numpy.mean(CRQ_dose_mamm_BP_sm), '%.2e' % numpy.std(CRQ_dose_mamm_BP_sm), '%.2e' % numpy.min(CRQ_dose_mamm_BP_sm), '%.2e' % numpy.max(CRQ_dose_mamm_BP_sm),
                             '%.2e' % numpy.mean(ARQ_dose_mamm_BP_md), '%.2e' % numpy.std(ARQ_dose_mamm_BP_md), '%.2e' % numpy.min(ARQ_dose_mamm_BP_md), '%.2e' % numpy.max(ARQ_dose_mamm_BP_md),
                             '%.2e' % numpy.mean(CRQ_dose_mamm_BP_md), '%.2e' % numpy.std(CRQ_dose_mamm_BP_md), '%.2e' % numpy.min(CRQ_dose_mamm_BP_md), '%.2e' % numpy.max(CRQ_dose_mamm_BP_md),
                             '%.2e' % numpy.mean(ARQ_dose_mamm_BP_lg), '%.2e' % numpy.std(ARQ_dose_mamm_BP_lg), '%.2e' % numpy.min(ARQ_dose_mamm_BP_lg), '%.2e' % numpy.max(ARQ_dose_mamm_BP_lg),
                             '%.2e' % numpy.mean(CRQ_dose_mamm_BP_lg), '%.2e' % numpy.std(CRQ_dose_mamm_BP_lg), '%.2e' % numpy.min(CRQ_dose_mamm_BP_lg), '%.2e' % numpy.max(CRQ_dose_mamm_BP_lg),],

        "Fruits/Pods": ['%.2e' % numpy.mean(ARQ_dose_mamm_FP_sm), '%.2e' % numpy.std(ARQ_dose_mamm_FP_sm), '%.2e' % numpy.min(ARQ_dose_mamm_FP_sm), '%.2e' % numpy.max(ARQ_dose_mamm_FP_sm),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_FP_sm), '%.2e' % numpy.std(CRQ_dose_mamm_FP_sm), '%.2e' % numpy.min(CRQ_dose_mamm_FP_sm), '%.2e' % numpy.max(CRQ_dose_mamm_FP_sm),
                        '%.2e' % numpy.mean(ARQ_dose_mamm_FP_md), '%.2e' % numpy.std(ARQ_dose_mamm_FP_md), '%.2e' % numpy.min(ARQ_dose_mamm_FP_md), '%.2e' % numpy.max(ARQ_dose_mamm_FP_md),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_FP_md), '%.2e' % numpy.std(CRQ_dose_mamm_FP_md), '%.2e' % numpy.min(CRQ_dose_mamm_FP_md), '%.2e' % numpy.max(CRQ_dose_mamm_FP_md),
                        '%.2e' % numpy.mean(ARQ_dose_mamm_FP_lg), '%.2e' % numpy.std(ARQ_dose_mamm_FP_lg), '%.2e' % numpy.min(ARQ_dose_mamm_FP_lg), '%.2e' % numpy.max(ARQ_dose_mamm_FP_lg),
                        '%.2e' % numpy.mean(CRQ_dose_mamm_FP_lg), '%.2e' % numpy.std(CRQ_dose_mamm_FP_lg), '%.2e' % numpy.min(CRQ_dose_mamm_FP_lg), '%.2e' % numpy.max(CRQ_dose_mamm_FP_lg),],

        "Arthropods": ['%.2e' % numpy.mean(ARQ_dose_mamm_AR_sm), '%.2e' % numpy.std(ARQ_dose_mamm_AR_sm), '%.2e' % numpy.min(ARQ_dose_mamm_AR_sm), '%.2e' % numpy.max(ARQ_dose_mamm_AR_sm),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_AR_sm), '%.2e' % numpy.std(CRQ_dose_mamm_AR_sm), '%.2e' % numpy.min(CRQ_dose_mamm_AR_sm), '%.2e' % numpy.max(CRQ_dose_mamm_AR_sm),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_AR_md), '%.2e' % numpy.std(ARQ_dose_mamm_AR_md), '%.2e' % numpy.min(ARQ_dose_mamm_AR_md), '%.2e' % numpy.max(ARQ_dose_mamm_AR_md),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_AR_md), '%.2e' % numpy.std(CRQ_dose_mamm_AR_md), '%.2e' % numpy.min(CRQ_dose_mamm_AR_md), '%.2e' % numpy.max(CRQ_dose_mamm_AR_md),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_AR_lg), '%.2e' % numpy.std(ARQ_dose_mamm_AR_lg), '%.2e' % numpy.min(ARQ_dose_mamm_AR_lg), '%.2e' % numpy.max(ARQ_dose_mamm_AR_lg),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_AR_lg), '%.2e' % numpy.std(CRQ_dose_mamm_AR_lg), '%.2e' % numpy.min(CRQ_dose_mamm_AR_lg), '%.2e' % numpy.max(CRQ_dose_mamm_AR_lg),],

        "Seeds":      ['%.2e' % numpy.mean(ARQ_dose_mamm_AR_sm), '%.2e' % numpy.std(ARQ_dose_mamm_SE_sm), '%.2e' % numpy.min(ARQ_dose_mamm_SE_sm), '%.2e' % numpy.max(ARQ_dose_mamm_SE_sm),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_SE_sm), '%.2e' % numpy.std(CRQ_dose_mamm_SE_sm), '%.2e' % numpy.min(CRQ_dose_mamm_SE_sm), '%.2e' % numpy.max(CRQ_dose_mamm_SE_sm),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_SE_md), '%.2e' % numpy.std(ARQ_dose_mamm_SE_md), '%.2e' % numpy.min(ARQ_dose_mamm_SE_md), '%.2e' % numpy.max(ARQ_dose_mamm_SE_md),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_SE_md), '%.2e' % numpy.std(CRQ_dose_mamm_SE_md), '%.2e' % numpy.min(CRQ_dose_mamm_SE_md), '%.2e' % numpy.max(CRQ_dose_mamm_SE_md),
                       '%.2e' % numpy.mean(ARQ_dose_mamm_SE_lg), '%.2e' % numpy.std(ARQ_dose_mamm_SE_lg), '%.2e' % numpy.min(ARQ_dose_mamm_SE_lg), '%.2e' % numpy.max(ARQ_dose_mamm_SE_lg),
                       '%.2e' % numpy.mean(CRQ_dose_mamm_SE_lg), '%.2e' % numpy.std(CRQ_dose_mamm_SE_lg), '%.2e' % numpy.min(CRQ_dose_mamm_SE_lg), '%.2e' % numpy.max(CRQ_dose_mamm_SE_lg),],
    }
    return data    

def gettsumdata_11(ARQ_diet_mamm_SG, CRQ_diet_mamm_SG, ARQ_diet_mamm_TG, CRQ_diet_mamm_TG, ARQ_diet_mamm_BP, CRQ_diet_mamm_BP, ARQ_diet_mamm_FP, CRQ_diet_mamm_FP, ARQ_diet_mamm_AR, CRQ_diet_mamm_AR):
    if 'N/A' in ARQ_diet_mamm_SG:
        ARQ_diet_mamm_SG_mean='N/A'
        ARQ_diet_mamm_SG_std='N/A'
        ARQ_diet_mamm_SG_min='N/A'
        ARQ_diet_mamm_SG_max='N/A'
        ARQ_diet_mamm_TG_mean='N/A'
        ARQ_diet_mamm_TG_std='N/A'
        ARQ_diet_mamm_TG_min='N/A'
        ARQ_diet_mamm_TG_max='N/A'
        ARQ_diet_mamm_BP_mean='N/A'
        ARQ_diet_mamm_BP_std='N/A'
        ARQ_diet_mamm_BP_min='N/A'
        ARQ_diet_mamm_BP_max='N/A'
        ARQ_diet_mamm_FP_mean='N/A'
        ARQ_diet_mamm_FP_std='N/A'
        ARQ_diet_mamm_FP_min='N/A'
        ARQ_diet_mamm_FP_max='N/A'
        ARQ_diet_mamm_AR_mean='N/A'
        ARQ_diet_mamm_AR_std='N/A'
        ARQ_diet_mamm_AR_min='N/A'
        ARQ_diet_mamm_AR_max='N/A'
    else:
        ARQ_diet_mamm_SG_mean='%.2e' % numpy.mean(ARQ_diet_mamm_SG)
        ARQ_diet_mamm_SG_std='%.2e' % numpy.std(ARQ_diet_mamm_SG)
        ARQ_diet_mamm_SG_min='%.2e' % numpy.min(ARQ_diet_mamm_SG)
        ARQ_diet_mamm_SG_max='%.2e' % numpy.max(ARQ_diet_mamm_SG)
        ARQ_diet_mamm_TG_mean='%.2e' % numpy.mean(ARQ_diet_mamm_TG)
        ARQ_diet_mamm_TG_std='%.2e' % numpy.std(ARQ_diet_mamm_TG)
        ARQ_diet_mamm_TG_min='%.2e' % numpy.min(ARQ_diet_mamm_TG)
        ARQ_diet_mamm_TG_max='%.2e' % numpy.max(ARQ_diet_mamm_TG)
        ARQ_diet_mamm_BP_mean='%.2e' % numpy.mean(ARQ_diet_mamm_BP)
        ARQ_diet_mamm_BP_std='%.2e' % numpy.std(ARQ_diet_mamm_BP)
        ARQ_diet_mamm_BP_min='%.2e' % numpy.min(ARQ_diet_mamm_BP)
        ARQ_diet_mamm_BP_max='%.2e' % numpy.max(ARQ_diet_mamm_BP)
        ARQ_diet_mamm_FP_mean='%.2e' % numpy.mean(ARQ_diet_mamm_FP)
        ARQ_diet_mamm_FP_std='%.2e' % numpy.std(ARQ_diet_mamm_FP)
        ARQ_diet_mamm_FP_min='%.2e' % numpy.min(ARQ_diet_mamm_FP)
        ARQ_diet_mamm_FP_max='%.2e' % numpy.max(ARQ_diet_mamm_FP)
        ARQ_diet_mamm_AR_mean='%.2e' % numpy.mean(ARQ_diet_mamm_AR)
        ARQ_diet_mamm_AR_std='%.2e' % numpy.std(ARQ_diet_mamm_AR)
        ARQ_diet_mamm_AR_min='%.2e' % numpy.min(ARQ_diet_mamm_AR)
        ARQ_diet_mamm_AR_max='%.2e' % numpy.max(ARQ_diet_mamm_AR)
    data = { 
        "Type": ['Acute', 'Acute', 'Acute', 'Acute', 'Chronic', 'Chronic', 'Chronic', 'Chronic',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Short Grass": [ARQ_diet_mamm_SG_mean, ARQ_diet_mamm_SG_std, ARQ_diet_mamm_SG_min, ARQ_diet_mamm_SG_max,
                        '%.2e' % numpy.mean(CRQ_diet_mamm_SG), '%.2e' % numpy.std(CRQ_diet_mamm_SG), '%.2e' % numpy.min(CRQ_diet_mamm_SG), '%.2e' % numpy.max(CRQ_diet_mamm_SG),],
        
        "Tall Grass": [ARQ_diet_mamm_TG_mean, ARQ_diet_mamm_TG_std, ARQ_diet_mamm_TG_min, ARQ_diet_mamm_TG_max,
                       '%.2e' % numpy.mean(CRQ_diet_mamm_TG), '%.2e' % numpy.std(CRQ_diet_mamm_TG), '%.2e' % numpy.min(CRQ_diet_mamm_TG), '%.2e' % numpy.max(CRQ_diet_mamm_TG),],
        
        "Broadleaf Plants": [ARQ_diet_mamm_BP_mean, ARQ_diet_mamm_BP_std, ARQ_diet_mamm_BP_min, ARQ_diet_mamm_BP_max,
                             '%.2e' % numpy.mean(CRQ_diet_mamm_BP), '%.2e' % numpy.std(CRQ_diet_mamm_BP), '%.2e' % numpy.min(CRQ_diet_mamm_BP), '%.2e' % numpy.max(CRQ_diet_mamm_BP),],

        "Fruits/Pods/Seeds": [ARQ_diet_mamm_FP_mean, ARQ_diet_mamm_FP_std, ARQ_diet_mamm_FP_min, ARQ_diet_mamm_FP_max,
                              '%.2e' % numpy.mean(CRQ_diet_mamm_FP), '%.2e' % numpy.std(CRQ_diet_mamm_FP), '%.2e' % numpy.min(CRQ_diet_mamm_FP), '%.2e' % numpy.max(CRQ_diet_mamm_FP),],

        "Arthropods": [ARQ_diet_mamm_AR_mean, ARQ_diet_mamm_AR_std, ARQ_diet_mamm_AR_min, ARQ_diet_mamm_AR_max,
                       '%.2e' % numpy.mean(CRQ_diet_mamm_AR), '%.2e' % numpy.std(CRQ_diet_mamm_AR), '%.2e' % numpy.min(CRQ_diet_mamm_AR), '%.2e' % numpy.max(CRQ_diet_mamm_AR),],
    }
    return data    

def gettsumdata_12(LD50_rg_bird_sm_out, LD50_rg_mamm_sm_out, LD50_rg_bird_md_out, LD50_rg_mamm_md_out, LD50_rg_bird_lg_out, LD50_rg_mamm_lg_out):
    data = { 
        "Animal Size": ['Small', 'Small', 'Small', 'Small', 'Medium', 'Medium', 'Medium', 'Medium', 'Large', 'Large', 'Large', 'Large',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max', 'Mean', 'Std', 'Min', 'Max',],
        "Avian":  ['%.2e' % numpy.mean(LD50_rg_bird_sm_out), '%.2e' % numpy.std(LD50_rg_bird_sm_out), '%.2e' % numpy.min(LD50_rg_bird_sm_out), '%.2e' % numpy.max(LD50_rg_bird_sm_out), 
                   '%.2e' % numpy.mean(LD50_rg_bird_md_out), '%.2e' % numpy.std(LD50_rg_bird_md_out), '%.2e' % numpy.min(LD50_rg_bird_md_out), '%.2e' % numpy.max(LD50_rg_bird_md_out),
                   '%.2e' % numpy.mean(LD50_rg_bird_lg_out), '%.2e' % numpy.std(LD50_rg_bird_lg_out), '%.2e' % numpy.min(LD50_rg_bird_lg_out), '%.2e' % numpy.max(LD50_rg_bird_lg_out),],
        "Mammal": ['%.2e' % numpy.mean(LD50_rg_mamm_sm_out), '%.2e' % numpy.std(LD50_rg_mamm_sm_out), '%.2e' % numpy.min(LD50_rg_mamm_sm_out), '%.2e' % numpy.max(LD50_rg_mamm_sm_out), 
                   '%.2e' % numpy.mean(LD50_rg_mamm_md_out), '%.2e' % numpy.std(LD50_rg_mamm_md_out), '%.2e' % numpy.min(LD50_rg_mamm_md_out), '%.2e' % numpy.max(LD50_rg_mamm_md_out),
                   '%.2e' % numpy.mean(LD50_rg_mamm_lg_out), '%.2e' % numpy.std(LD50_rg_mamm_lg_out), '%.2e' % numpy.min(LD50_rg_mamm_lg_out), '%.2e' % numpy.max(LD50_rg_mamm_lg_out),],
    }
    return data

def table_all(trex2_obj):

    table1_out=table_1(trex2_obj)
    table2_out=table_2(trex2_obj)
    table3_out=table_3(trex2_obj)
    table4_out=table_4(trex2_obj)

    html = table1_out
    html = html + table2_out
    html = html + table3_out
    html = html + table4_out

    if trex2_obj.Application_type == 'Seed Treatment':
        table5_out=table_5(trex2_obj)

        html = html + table5_out['html']
        return html, table5_out
    else:
        a_r_p=0
        table6_out=table_6(trex2_obj)
        table7_out=table_7(trex2_obj)
        table7_add_out=table_7_add(trex2_obj)
        table8_out=table_8(trex2_obj)
        table9_out=table_9(trex2_obj)
        table10_out=table_10(trex2_obj)
        table11_out=table_11(trex2_obj)

        html = html + table6_out['html']
        html = html + table7_out['html']
        html = html + table7_add_out['html']
        html = html + table8_out['html']
        html = html + table9_out['html']
        html = html + table10_out['html']
        html = html + table11_out['html']

        if trex2_obj.Application_type == 'Row/Band/In-furrow-Granular':
            table12_out=table_12(trex2_obj)
            html = html + table12_out['html']
            return html, table6_out, table7_out, table7_add_out, table8_out, table9_out, table10_out, table11_out, table12_out

        elif trex2_obj.Application_type == 'Row/Band/In-furrow-Liquid':
            table13_out=table_13(trex2_obj)
            html = html + table13_out['html']
            return html, table6_out, table7_out, table7_add_out, table8_out, table9_out, table10_out, table11_out, table13_out

        elif trex2_obj.Application_type == 'Broadcast-Granular':
            table14_out=table_14(trex2_obj)
            html = html + table14_out['html']
            return html, table6_out, table7_out, table7_add_out, table8_out, table9_out, table10_out, table11_out, table14_out

        elif trex2_obj.Application_type == 'Broadcast-Liquid':
            table15_out=table_15(trex2_obj)
            html = html + table15_out['html']
            return html, table6_out, table7_out, table7_add_out, table8_out, table9_out, table10_out, table11_out, table15_out

def timestamp(trex2_obj="", batch_jid=""):
    if trex2_obj:
        st = datetime.datetime.strptime(trex2_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>T-Rex <a href="http://www.epa.gov/oppefed1/models/terrestrial/trex/t_rex_user_guide.htm">Version 1.5.2</a> (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_all_qaqc(trex2_obj):
    table1_out=table_1(trex2_obj)
    table2_out=table_2(trex2_obj)
    table3_out=table_3(trex2_obj)
    table4_out=table_4(trex2_obj)
    a_r_p=0

    if trex2_obj.Application_type != 'Seed Treatment':
        table6_out_qaqc=table_6_qaqc(trex2_obj)
        table7_out_qaqc=table_7_qaqc(trex2_obj)
        table_7_add_out_qaqc=table_7_add_qaqc(trex2_obj)
        table8_out_qaqc=table_8_qaqc(trex2_obj)
        table9_out_qaqc=table_9_qaqc(trex2_obj)
        table10_out_qaqc=table_10_qaqc(trex2_obj)
        table11_out_qaqc=table_11_qaqc(trex2_obj)
        table15_out_qaqc=table_15_qaqc(trex2_obj)

        html_all = table1_out+table2_out+table3_out+table4_out+table6_out_qaqc+\
                   table7_out_qaqc+table_7_add_out_qaqc+table8_out_qaqc+table9_out_qaqc+\
                   table10_out_qaqc+table11_out_qaqc+table15_out_qaqc
    else:
        table5_out_qaqc=table_5_qaqc(trex2_obj)
        html_all = table1_out+table2_out+table3_out+table4_out+table5_out_qaqc

    return html_all

def table_sum_1(i, a_i, r_s, b_w, p_i, den, Foliar_dissipation_half_life, n_a, ar_lb):
        #pre-table sum_input_1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Batch Summary Statistics (Iterations=%s)</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """%(i-1)

        rate_out_t=[]
        for jj in ar_lb:
            rate_out_t.append(numpy.mean(jj))
        
        #table sum_input_1
        tsuminputdata_1 = gettsumdata_1(a_i, r_s, b_w, p_i, den, Foliar_dissipation_half_life, n_a, rate_out_t)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def table_sum_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, bw_assessed_bird_l, tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, mineau_scaling_factor):
        #pre-table sum_input_2
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Toxicity Properties (Avian)</H4>
                <div class="out_ container_output">
        """
        #table sum_input_2
        tsuminputdata_2 = gettsumdata_2(avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, bw_assessed_bird_s, bw_assessed_bird_m, bw_assessed_bird_l, tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, mineau_scaling_factor)
        tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def table_sum_3(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, bw_assessed_mamm_l, bw_tested_mamm):
        #pre-table sum_input_3
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Toxicity Properties (Mammal)</H4>
                <div class="out_ container_output">
        """
        #table sum_input_3
        tsuminputdata_3 = gettsumdata_3(mammalian_ld50, mammalian_lc50, mammalian_NOAEC, mammalian_NOAEL, bw_assessed_mamm_s, bw_assessed_mamm_m, 
              bw_assessed_mamm_l, bw_tested_mamm)
        tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html

def table_sum_5(Application_type_ST, sa_bird_1_s_out, sa_bird_2_s_out, sc_bird_s_out, sa_mamm_1_s_out, sa_mamm_2_s_out, sc_mamm_s_out, sa_bird_1_m_out, sa_bird_2_m_out, sc_bird_m_out, sa_mamm_1_m_out, sa_mamm_2_m_out, sc_mamm_m_out, sa_bird_1_l_out, sa_bird_2_l_out, sc_bird_l_out, sa_mamm_1_l_out, sa_mamm_2_l_out, sc_mamm_l_out):
        #pre-table sum_5
        html = """
        <H3 class="out_3 collapsible" id="section4"><span></span>Batch Outputs: Application Type : Seed Treatment (N=%s)</H3>
                <div class="out_ container_output">
        """%(Application_type_ST)

        #table sum_output_5
        tsuminputdata_5 = gettsumdata_5(sa_bird_1_s_out, sa_bird_2_s_out, sc_bird_s_out, sa_mamm_1_s_out, sa_mamm_2_s_out, sc_mamm_s_out, sa_bird_1_m_out, sa_bird_2_m_out, sc_bird_m_out, sa_mamm_1_m_out, sa_mamm_2_m_out, sc_mamm_m_out, sa_bird_1_l_out, sa_bird_2_l_out, sc_bird_l_out, sa_mamm_1_l_out, sa_mamm_2_l_out, sc_mamm_l_out)
        tsuminputrows_5 = gethtmlrowsfromcols(tsuminputdata_5,sumheadings_5[1])       
        html = html + tmpl.render(Context(dict(data=tsuminputrows_5, headings=sumheadings_5[0], sub_headings=sumheadings_5[2], th_span='5')))
        html = html + """
                </div>
        """
        return html

def table_sum_6(Application_type, Application_type_str, EEC_diet_SG_RBG_out, EEC_diet_TG_RBG_out, EEC_diet_BP_RBG_out, EEC_diet_FR_RBG_out, EEC_diet_AR_RBG_out):
        #pre-table sum_6
        html = """
        <br>
        <H3 class="out_3 collapsible" id="section4"><span></span>Batch Outputs: Application Type : %s (N=%s)</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section3"><span></span>Dietary based EECs (ppm)</H4>
                <div class="out_ container_output">
        """%(Application_type_str, Application_type)

        #table sum_output_6
        tsuminputdata_6 = gettsumdata_6(EEC_diet_SG_RBG_out, EEC_diet_TG_RBG_out, EEC_diet_BP_RBG_out, EEC_diet_FR_RBG_out, EEC_diet_AR_RBG_out)
        tsuminputrows_6 = gethtmlrowsfromcols(tsuminputdata_6, sumheadings_6[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_6, headings=sumheadings_6[0], sub_headings=sumheadings_6[2])))
        html = html + """
                </div>
        """
        return html

def table_sum_7(EEC_dose_bird_SG_sm_out, EEC_dose_bird_SG_md_out, EEC_dose_bird_SG_lg_out, EEC_dose_bird_TG_sm_out, EEC_dose_bird_TG_md_out, EEC_dose_bird_TG_lg_out, EEC_dose_bird_BP_sm_out, EEC_dose_bird_BP_md_out, EEC_dose_bird_BP_lg_out, EEC_dose_bird_FP_sm_out, EEC_dose_bird_FP_md_out, EEC_dose_bird_FP_lg_out, EEC_dose_bird_AR_sm_out, EEC_dose_bird_AR_md_out, EEC_dose_bird_AR_lg_out, EEC_dose_bird_SE_sm_out, EEC_dose_bird_SE_md_out, EEC_dose_bird_SE_lg_out):
        #pre-table sum_7
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Avian Dosed Based EECs</H4>
                <div class="out_ container_output">
        """

        #table sum_output_7
        tsuminputdata_7 = gettsumdata_7(EEC_dose_bird_SG_sm_out, EEC_dose_bird_SG_md_out, EEC_dose_bird_SG_lg_out, EEC_dose_bird_TG_sm_out, EEC_dose_bird_TG_md_out, EEC_dose_bird_TG_lg_out, EEC_dose_bird_BP_sm_out, EEC_dose_bird_BP_md_out, EEC_dose_bird_BP_lg_out, EEC_dose_bird_FP_sm_out, EEC_dose_bird_FP_md_out, EEC_dose_bird_FP_lg_out, EEC_dose_bird_AR_sm_out, EEC_dose_bird_AR_md_out, EEC_dose_bird_AR_lg_out, EEC_dose_bird_SE_sm_out, EEC_dose_bird_SE_md_out, EEC_dose_bird_SE_lg_out)
        tsuminputrows_7 = gethtmlrowsfromcols(tsuminputdata_7, sumheadings_7[1])
        # html = html + tmpl_sum.render(Context(dict(data_new=tsuminputrows_7, headings=sumheadings_7[0], sub_headings=sumheadings_7[2], data_cols=["Small", "Medium", "Large"])))
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_7, headings=sumheadings_7[0], sub_headings=sumheadings_7[2])))
        html = html + """
                </div>
        """
        return html

def table_sum_7_add(ARQ_bird_SG_RBG_sm_out, ARQ_bird_SG_RBG_md_out, ARQ_bird_SG_RBG_lg_out, ARQ_bird_TG_RBG_sm_out, ARQ_bird_TG_RBG_md_out, ARQ_bird_TG_RBG_lg_out, ARQ_bird_BP_RBG_sm_out, ARQ_bird_BP_RBG_md_out, ARQ_bird_BP_RBG_lg_out, ARQ_bird_FP_RBG_sm_out, ARQ_bird_FP_RBG_md_out, ARQ_bird_FP_RBG_lg_out, ARQ_bird_AR_RBG_sm_out, ARQ_bird_AR_RBG_md_out, ARQ_bird_AR_RBG_lg_out, ARQ_bird_SE_RBG_sm_out, ARQ_bird_SE_RBG_md_out, ARQ_bird_SE_RBG_lg_out):
        #pre-table sum_7_add
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Avian Dosed Based RQs</H4>
                <div class="out_ container_output">
        """

        #table sum_output_7
        tsuminputdata_7_add = gettsumdata_7(ARQ_bird_SG_RBG_sm_out, ARQ_bird_SG_RBG_md_out, ARQ_bird_SG_RBG_lg_out, ARQ_bird_TG_RBG_sm_out, ARQ_bird_TG_RBG_md_out, ARQ_bird_TG_RBG_lg_out, ARQ_bird_BP_RBG_sm_out, ARQ_bird_BP_RBG_md_out, ARQ_bird_BP_RBG_lg_out, ARQ_bird_FP_RBG_sm_out, ARQ_bird_FP_RBG_md_out, ARQ_bird_FP_RBG_lg_out, ARQ_bird_AR_RBG_sm_out, ARQ_bird_AR_RBG_md_out, ARQ_bird_AR_RBG_lg_out, ARQ_bird_SE_RBG_sm_out, ARQ_bird_SE_RBG_md_out, ARQ_bird_SE_RBG_lg_out)
        tsuminputrows_7_add = gethtmlrowsfromcols(tsuminputdata_7_add, sumheadings_7[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_7_add, headings=sumheadings_7[0], sub_headings=sumheadings_7[2])))
        html = html + """
                </div>
        """
        return html

def table_sum_8(ARQ_diet_bird_SG_A_out, ARQ_diet_bird_SG_C_out, ARQ_diet_bird_TG_A_out, ARQ_diet_bird_TG_C_out, ARQ_diet_bird_BP_A_out, ARQ_diet_bird_BP_C_out, ARQ_diet_bird_FP_A_out, ARQ_diet_bird_FP_C_out, ARQ_diet_bird_AR_A_out, ARQ_diet_bird_AR_C_out):
        #pre-table sum_8
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Avian Diet Based RQs</H4>
                <div class="out_ container_output">
        """

        #table sum_output_8
        tsuminputdata_8 = gettsumdata_8(ARQ_diet_bird_SG_A_out, ARQ_diet_bird_SG_C_out, ARQ_diet_bird_TG_A_out, ARQ_diet_bird_TG_C_out, ARQ_diet_bird_BP_A_out, ARQ_diet_bird_BP_C_out, ARQ_diet_bird_FP_A_out, ARQ_diet_bird_FP_C_out, ARQ_diet_bird_AR_A_out, ARQ_diet_bird_AR_C_out)
        tsuminputrows_8 = gethtmlrowsfromcols(tsuminputdata_8, sumheadings_8[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_8, headings=sumheadings_8[0], sub_headings=sumheadings_8[2])))
        html = html + """
                </div>
        """
        return html

def table_sum_9(EEC_dose_mamm_SG_sm_out, EEC_dose_mamm_SG_md_out, EEC_dose_mamm_SG_lg_out, EEC_dose_mamm_TG_sm_out, EEC_dose_mamm_TG_md_out, EEC_dose_mamm_TG_lg_out, EEC_dose_mamm_BP_sm_out, EEC_dose_mamm_BP_md_out, EEC_dose_mamm_BP_lg_out, EEC_dose_mamm_FP_sm_out, EEC_dose_mamm_FP_md_out, EEC_dose_mamm_FP_lg_out, EEC_dose_mamm_AR_sm_out, EEC_dose_mamm_AR_md_out, EEC_dose_mamm_AR_lg_out, EEC_dose_mamm_SE_sm_out, EEC_dose_mamm_SE_md_out, EEC_dose_mamm_SE_lg_out):
        #pre-table sum_9
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Mammalian Dose Based EECs (mg/kg-bw)</H4>
                <div class="out_ container_output">
        """

        #table sum_output_9
        tsuminputdata_9 = gettsumdata_9(EEC_dose_mamm_SG_sm_out, EEC_dose_mamm_SG_md_out, EEC_dose_mamm_SG_lg_out, EEC_dose_mamm_TG_sm_out, EEC_dose_mamm_TG_md_out, EEC_dose_mamm_TG_lg_out, EEC_dose_mamm_BP_sm_out, EEC_dose_mamm_BP_md_out, EEC_dose_mamm_BP_lg_out, EEC_dose_mamm_FP_sm_out, EEC_dose_mamm_FP_md_out, EEC_dose_mamm_FP_lg_out, EEC_dose_mamm_AR_sm_out, EEC_dose_mamm_AR_md_out, EEC_dose_mamm_AR_lg_out, EEC_dose_mamm_SE_sm_out, EEC_dose_mamm_SE_md_out, EEC_dose_mamm_SE_lg_out)
        tsuminputrows_9 = gethtmlrowsfromcols(tsuminputdata_9, sumheadings_9[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_9, headings=sumheadings_9[0], sub_headings=sumheadings_9[2])))
        html = html + """
                </div>
        """
        return html

def table_sum_10(ARQ_dose_mamm_SG_sm, CRQ_dose_mamm_SG_sm, ARQ_dose_mamm_SG_md, CRQ_dose_mamm_SG_md, ARQ_dose_mamm_SG_lg, CRQ_dose_mamm_SG_lg, ARQ_dose_mamm_TG_sm, CRQ_dose_mamm_TG_sm, ARQ_dose_mamm_TG_md, CRQ_dose_mamm_TG_md, ARQ_dose_mamm_TG_lg, CRQ_dose_mamm_TG_lg, ARQ_dose_mamm_BP_sm, CRQ_dose_mamm_BP_sm, ARQ_dose_mamm_BP_md, CRQ_dose_mamm_BP_md, ARQ_dose_mamm_BP_lg, CRQ_dose_mamm_BP_lg, ARQ_dose_mamm_FP_sm, CRQ_dose_mamm_FP_sm, ARQ_dose_mamm_FP_md, CRQ_dose_mamm_FP_md, ARQ_dose_mamm_FP_lg, CRQ_dose_mamm_FP_lg, ARQ_dose_mamm_AR_sm, CRQ_dose_mamm_AR_sm, ARQ_dose_mamm_AR_md, CRQ_dose_mamm_AR_md, ARQ_dose_mamm_AR_lg, CRQ_dose_mamm_AR_lg, ARQ_dose_mamm_SE_sm, CRQ_dose_mamm_SE_sm, ARQ_dose_mamm_SE_md, CRQ_dose_mamm_SE_md, ARQ_dose_mamm_SE_lg, CRQ_dose_mamm_SE_lg):
        #pre-table sum_10
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Mammalian Dose Based RQs</H4>
                <div class="out_ container_output">
        """

        #table sum_output_10
        tsuminputdata_10 = gettsumdata_10(ARQ_dose_mamm_SG_sm, CRQ_dose_mamm_SG_sm, ARQ_dose_mamm_SG_md, CRQ_dose_mamm_SG_md, ARQ_dose_mamm_SG_lg, CRQ_dose_mamm_SG_lg, ARQ_dose_mamm_TG_sm, CRQ_dose_mamm_TG_sm, ARQ_dose_mamm_TG_md, CRQ_dose_mamm_TG_md, ARQ_dose_mamm_TG_lg, CRQ_dose_mamm_TG_lg, ARQ_dose_mamm_BP_sm, CRQ_dose_mamm_BP_sm, ARQ_dose_mamm_BP_md, CRQ_dose_mamm_BP_md, ARQ_dose_mamm_BP_lg, CRQ_dose_mamm_BP_lg, ARQ_dose_mamm_FP_sm, CRQ_dose_mamm_FP_sm, ARQ_dose_mamm_FP_md, CRQ_dose_mamm_FP_md, ARQ_dose_mamm_FP_lg, CRQ_dose_mamm_FP_lg, ARQ_dose_mamm_AR_sm, CRQ_dose_mamm_AR_sm, ARQ_dose_mamm_AR_md, CRQ_dose_mamm_AR_md, ARQ_dose_mamm_AR_lg, CRQ_dose_mamm_AR_lg, ARQ_dose_mamm_SE_sm, CRQ_dose_mamm_SE_sm, ARQ_dose_mamm_SE_md, CRQ_dose_mamm_SE_md, ARQ_dose_mamm_SE_lg, CRQ_dose_mamm_SE_lg)
        tsuminputrows_10 = gethtmlrowsfromcols(tsuminputdata_10, sumheadings_10[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_10, headings=sumheadings_10[0], sub_headings=sumheadings_10[2])))
        html = html + """
                </div>
        """
        return html


def table_sum_11(ARQ_diet_mamm_SG, CRQ_diet_mamm_SG, ARQ_diet_mamm_TG, CRQ_diet_mamm_TG, ARQ_diet_mamm_BP, CRQ_diet_mamm_BP, ARQ_diet_mamm_FP, CRQ_diet_mamm_FP, ARQ_diet_mamm_AR, CRQ_diet_mamm_AR):
        #pre-table sum_11
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Mammalian Dietary Based RQs</H4>
                <div class="out_ container_output">
        """
        #table sum_output_11
        tsuminputdata_11 = gettsumdata_11(ARQ_diet_mamm_SG, CRQ_diet_mamm_SG, ARQ_diet_mamm_TG, CRQ_diet_mamm_TG, ARQ_diet_mamm_BP, CRQ_diet_mamm_BP, ARQ_diet_mamm_FP, CRQ_diet_mamm_FP, ARQ_diet_mamm_AR, CRQ_diet_mamm_AR)
        tsuminputrows_11 = gethtmlrowsfromcols(tsuminputdata_11, sumheadings_11[1])
        html = html + tmpl_sum.render(Context(dict(data=tsuminputrows_11, headings=sumheadings_11[0], sub_headings=sumheadings_11[2])))
        html = html + """
                </div>
        """
        return html


def table_sum_12(LD50_rg_bird_sm_out, LD50_rg_mamm_sm_out, LD50_rg_bird_md_out, LD50_rg_mamm_md_out, LD50_rg_bird_lg_out, LD50_rg_mamm_lg_out):
        #pre-table sum_12
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>LD50ft-2(mg/kg-bw)</H4>
                <div class="out_ container_output">
        """
        #table sum_output_12
        tsuminputdata_12 = gettsumdata_12(LD50_rg_bird_sm_out, LD50_rg_mamm_sm_out, LD50_rg_bird_md_out, LD50_rg_mamm_md_out, LD50_rg_bird_lg_out, LD50_rg_mamm_lg_out)
        tsuminputrows_12 = gethtmlrowsfromcols(tsuminputdata_12, sumheadings_12)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_12, headings=sumheadings_12)))
        return html

def table_sum_13(LD50_rl_bird_sm_out, LD50_rl_mamm_sm_out, LD50_rl_bird_md_out, LD50_rl_mamm_md_out, LD50_rl_bird_lg_out, LD50_rl_mamm_lg_out):
        #pre-table sum_13
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>LD50ft-2(mg/kg-bw)</H4>
                <div class="out_ container_output">
        """

        #table sum_output_13
        tsuminputdata_13 = gettsumdata_12(LD50_rl_bird_sm_out, LD50_rl_mamm_sm_out, LD50_rl_bird_md_out, LD50_rl_mamm_md_out, LD50_rl_bird_lg_out, LD50_rl_mamm_lg_out)
        tsuminputrows_13 = gethtmlrowsfromcols(tsuminputdata_13, sumheadings_12)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_13, headings=sumheadings_12)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_sum_14(LD50_bg_bird_sm_out, LD50_bg_mamm_sm_out, LD50_bg_bird_md_out, LD50_bg_mamm_md_out, LD50_bg_bird_lg_out, LD50_bg_mamm_lg_out):
        #pre-table sum_14
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>LD50ft-2(mg/kg-bw)</H4>
                <div class="out_ container_output">
        """

        #table sum_output_14
        tsuminputdata_14 = gettsumdata_12(LD50_bg_bird_sm_out, LD50_bg_mamm_sm_out, LD50_bg_bird_md_out, LD50_bg_mamm_md_out, LD50_bg_bird_lg_out, LD50_bg_mamm_lg_out)
        tsuminputrows_14 = gethtmlrowsfromcols(tsuminputdata_14, sumheadings_12)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_14, headings=sumheadings_12)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_sum_15(LD50_bl_bird_sm_out, LD50_bl_mamm_sm_out, LD50_bl_bird_md_out, LD50_bl_mamm_md_out, LD50_bl_bird_lg_out, LD50_bl_mamm_lg_out):
        #pre-table sum_15
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>LD50ft-2(mg/kg-bw)</H4>
                <div class="out_ container_output">
        """

        #table sum_output_15
        tsuminputdata_15 = gettsumdata_12(LD50_bl_bird_sm_out, LD50_bl_mamm_sm_out, LD50_bl_bird_md_out, LD50_bl_mamm_md_out, LD50_bl_bird_lg_out, LD50_bl_mamm_lg_out)
        tsuminputrows_15 = gethtmlrowsfromcols(tsuminputdata_15, sumheadings_12)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_15, headings=sumheadings_12)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_1(trex2_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs:</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """
        #table 1
        if trex2_obj.Application_type=="Broadcast-Liquid" or trex2_obj.Application_type=="Broadcast-Granular":
            t1data = gett1data_broad(trex2_obj)
        elif trex2_obj.Application_type=="Row/Band/In-furrow-Granular" or trex2_obj.Application_type=="Row/Band/In-furrow-Liquid": 
            t1data = gett1data_band(trex2_obj)
        else:
            t1data = gett1data_seed(trex2_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(trex2_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Chemical Application (n=%s)</H4>
                <div class="out_ container_output">
        """ %(trex2_obj.n_a)
        #table 2
        t2data_all=[]
        for i in range(int(trex2_obj.n_a)):
            rate_temp=trex2_obj.ar_lb[i]
            day_temp=trex2_obj.day_out[i]
            t2data_temp=gett2data(i+1, rate_temp, day_temp)
            t2data_all.append(t2data_temp)
        t2data = dict([(k,[t2data_ind[k][0] for t2data_ind in t2data_all]) for k in t2data_temp])
        t2rows = gethtmlrowsfromcols(t2data,pvaheadings[0])
        if trex2_obj.Application_type=="Seed Treatment":
            html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings[1])))
        else:
            html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings[2])))
        html = html + """
                </div>
        """
        return html

def table_3(trex2_obj):
        #pre-table 3
        html = """
            <H4 class="out_3 collapsible" id="section4"><span></span>Toxicity Properties (Avian)</H4>
                <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(trex2_obj)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_4(trex2_obj):
        #pre-table 4
        html = """
            <H4 class="out_4 collapsible" id="section5"><span></span>Toxicity Properties (Mammal)</H4>
                <div class="out_ container_output">
        """
        #table 4
        t4data = gett4data(trex2_obj)
        t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_5(trex2_obj):
        #pre-table 5
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section6"><span></span>Results (Upper Bound Kenaga): Application Type : %s</H3>
            <div class="out_ container_output">
        """%(trex2_obj.Application_type)
        #table 5
        sa_bird_1_s=trex2_obj.sa_bird_1_s
        sa_bird_2_s=trex2_obj.sa_bird_2_s
        sc_bird_s=trex2_obj.sc_bird_s
        sa_mamm_1_s=trex2_obj.sa_mamm_1_s
        sa_mamm_2_s=trex2_obj.sa_mamm_2_s
        sc_mamm_s=trex2_obj.sc_mamm_s
        
        sa_bird_1_m=trex2_obj.sa_bird_1_m
        sa_bird_2_m=trex2_obj.sa_bird_2_m
        sc_bird_m=trex2_obj.sc_bird_m
        sa_mamm_1_m=trex2_obj.sa_mamm_1_m
        sa_mamm_2_m=trex2_obj.sa_mamm_2_m
        sc_mamm_m=trex2_obj.sc_mamm_m
             
        sa_bird_1_l=trex2_obj.sa_bird_1_l
        sa_bird_2_l=trex2_obj.sa_bird_2_l
        sc_bird_l=trex2_obj.sc_bird_l
        sa_mamm_1_l=trex2_obj.sa_mamm_1_l
        sa_mamm_2_l=trex2_obj.sa_mamm_2_l
        sc_mamm_l=trex2_obj.sc_mamm_l

        t5data = gett5data(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
                           sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
                           sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l)
        t5rows = gethtmlrowsfromcols(t5data,pv5headings[1])     
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pv5headings[0], sub_headings=pv5headings[2], sub_headings_1=pv5headings[3], th_span='4')))
        html = html + """
                </div>
        """  
        return {'html':html, 'sa_bird_1_s':sa_bird_1_s, 'sa_bird_2_s':sa_bird_2_s, 'sc_bird_s':sc_bird_s, 'sa_mamm_1_s':sa_mamm_1_s, 'sa_mamm_2_s':sa_mamm_2_s, 'sc_mamm_s':sc_mamm_s,
                             'sa_bird_1_m':sa_bird_1_m, 'sa_bird_2_m':sa_bird_2_m, 'sc_bird_m':sc_bird_m, 'sa_mamm_1_m':sa_mamm_1_m, 'sa_mamm_2_m':sa_mamm_2_m, 'sc_mamm_m':sc_mamm_m,
                             'sa_bird_1_l':sa_bird_1_l, 'sa_bird_2_l':sa_bird_2_l, 'sc_bird_l':sc_bird_l, 'sa_mamm_1_l':sa_mamm_1_l, 'sa_mamm_2_l':sa_mamm_2_l, 'sc_mamm_l':sc_mamm_l}

def table_6(trex2_obj):
        #pre-table 6
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section6"><span></span>Results: Application Type : %s</H3>
        <div class="out_">
            <H4 class="out_ collapsible" id="section7"><span></span>Dietary Based EECs (mg/kg-dietary item)</H4>
                <div class="out_ container_output">
        """%(trex2_obj.Application_type)
        #table 6
        EEC_diet_SG=trex2_obj.EEC_diet_SG
        EEC_diet_TG=trex2_obj.EEC_diet_TG
        EEC_diet_BP=trex2_obj.EEC_diet_BP
        EEC_diet_FR=trex2_obj.EEC_diet_FR
        EEC_diet_AR=trex2_obj.EEC_diet_AR

        t6data = gett6data(EEC_diet_SG, EEC_diet_TG, EEC_diet_BP, EEC_diet_FR, EEC_diet_AR)
        t6rows = gethtmlrowsfromcols(t6data,pv6headings)
        html = html + tmpl.render(Context(dict(data=t6rows, headings=pv6headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'EEC_diet_SG':EEC_diet_SG, 'EEC_diet_TG':EEC_diet_TG, 'EEC_diet_BP':EEC_diet_BP, 'EEC_diet_FR':EEC_diet_FR, 'EEC_diet_AR':EEC_diet_AR}


def table_7(trex2_obj):
        #pre-table 7
        html = """
            <H4 class="out_ collapsible" id="section8"><span></span>Avian Dose Based EECs (mg/kg-bw)</H4>
                <div class="out_ container_output">
        """
        #table 7
        EEC_dose_bird_SG_sm=trex2_obj.EEC_dose_bird_SG_sm
        EEC_dose_bird_SG_md=trex2_obj.EEC_dose_bird_SG_md
        EEC_dose_bird_SG_lg=trex2_obj.EEC_dose_bird_SG_lg
        EEC_dose_bird_TG_sm=trex2_obj.EEC_dose_bird_TG_sm
        EEC_dose_bird_TG_md=trex2_obj.EEC_dose_bird_TG_md
        EEC_dose_bird_TG_lg=trex2_obj.EEC_dose_bird_TG_lg
        EEC_dose_bird_BP_sm=trex2_obj.EEC_dose_bird_BP_sm
        EEC_dose_bird_BP_md=trex2_obj.EEC_dose_bird_BP_md
        EEC_dose_bird_BP_lg=trex2_obj.EEC_dose_bird_BP_lg
        EEC_dose_bird_FP_sm=trex2_obj.EEC_dose_bird_FP_sm
        EEC_dose_bird_FP_md=trex2_obj.EEC_dose_bird_FP_md
        EEC_dose_bird_FP_lg=trex2_obj.EEC_dose_bird_FP_lg
        EEC_dose_bird_AR_sm=trex2_obj.EEC_dose_bird_AR_sm
        EEC_dose_bird_AR_md=trex2_obj.EEC_dose_bird_AR_md
        EEC_dose_bird_AR_lg=trex2_obj.EEC_dose_bird_AR_lg
        EEC_dose_bird_SE_sm=trex2_obj.EEC_dose_bird_SE_sm
        EEC_dose_bird_SE_md=trex2_obj.EEC_dose_bird_SE_md
        EEC_dose_bird_SE_lg=trex2_obj.EEC_dose_bird_SE_lg
                      
        t7data = gett7data(EEC_dose_bird_SG_sm, EEC_dose_bird_SG_md, EEC_dose_bird_SG_lg, EEC_dose_bird_TG_sm, EEC_dose_bird_TG_md, EEC_dose_bird_TG_lg, EEC_dose_bird_BP_sm, EEC_dose_bird_BP_md, EEC_dose_bird_BP_lg, EEC_dose_bird_FP_sm, EEC_dose_bird_FP_md, EEC_dose_bird_FP_lg, EEC_dose_bird_AR_sm, EEC_dose_bird_AR_md, EEC_dose_bird_AR_lg, EEC_dose_bird_SE_sm, EEC_dose_bird_SE_md, EEC_dose_bird_SE_lg)
        t7rows = gethtmlrowsfromcols(t7data,pv7headings)       
        html = html + tmpl.render(Context(dict(data=t7rows, headings=pv7headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'EEC_dose_bird_SG_sm':EEC_dose_bird_SG_sm, 'EEC_dose_bird_SG_md':EEC_dose_bird_SG_md, 'EEC_dose_bird_SG_lg':EEC_dose_bird_SG_lg, 'EEC_dose_bird_TG_sm':EEC_dose_bird_TG_sm, 'EEC_dose_bird_TG_md':EEC_dose_bird_TG_md, 'EEC_dose_bird_TG_lg':EEC_dose_bird_TG_lg,
                             'EEC_dose_bird_BP_sm':EEC_dose_bird_BP_sm, 'EEC_dose_bird_BP_md':EEC_dose_bird_BP_md, 'EEC_dose_bird_BP_lg':EEC_dose_bird_BP_lg, 'EEC_dose_bird_FP_sm':EEC_dose_bird_FP_sm, 'EEC_dose_bird_FP_md':EEC_dose_bird_FP_md, 'EEC_dose_bird_FP_lg':EEC_dose_bird_FP_lg,
                             'EEC_dose_bird_AR_sm':EEC_dose_bird_AR_sm, 'EEC_dose_bird_AR_md':EEC_dose_bird_AR_md, 'EEC_dose_bird_AR_lg':EEC_dose_bird_AR_lg, 'EEC_dose_bird_SE_sm':EEC_dose_bird_SE_sm, 'EEC_dose_bird_SE_md':EEC_dose_bird_SE_md, 'EEC_dose_bird_SE_lg':EEC_dose_bird_SE_lg}

def table_7_add(trex2_obj):
        #pre-table 7
        html = """
            <H4 class="out_ collapsible" id="section8_add"><span></span>Avian Dose Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 7_add
        ARQ_bird_SG_sm=trex2_obj.ARQ_bird_SG_sm
        ARQ_bird_SG_md=trex2_obj.ARQ_bird_SG_md
        ARQ_bird_SG_lg=trex2_obj.ARQ_bird_SG_lg
        ARQ_bird_TG_sm=trex2_obj.ARQ_bird_TG_sm
        ARQ_bird_TG_md=trex2_obj.ARQ_bird_TG_md
        ARQ_bird_TG_lg=trex2_obj.ARQ_bird_TG_lg
        ARQ_bird_BP_sm=trex2_obj.ARQ_bird_BP_sm
        ARQ_bird_BP_md=trex2_obj.ARQ_bird_BP_md
        ARQ_bird_BP_lg=trex2_obj.ARQ_bird_BP_lg
        ARQ_bird_FP_sm=trex2_obj.ARQ_bird_FP_sm
        ARQ_bird_FP_md=trex2_obj.ARQ_bird_FP_md
        ARQ_bird_FP_lg=trex2_obj.ARQ_bird_FP_lg
        ARQ_bird_AR_sm=trex2_obj.ARQ_bird_AR_sm
        ARQ_bird_AR_md=trex2_obj.ARQ_bird_AR_md
        ARQ_bird_AR_lg=trex2_obj.ARQ_bird_AR_lg
        ARQ_bird_SE_sm=trex2_obj.ARQ_bird_SE_sm
        ARQ_bird_SE_md=trex2_obj.ARQ_bird_SE_md
        ARQ_bird_SE_lg=trex2_obj.ARQ_bird_SE_lg
                      
        t7_add_data = gett7_add_data(ARQ_bird_SG_sm, ARQ_bird_SG_md, ARQ_bird_SG_lg, ARQ_bird_TG_sm, ARQ_bird_TG_md, ARQ_bird_TG_lg, ARQ_bird_BP_sm, ARQ_bird_BP_md, ARQ_bird_BP_lg, ARQ_bird_FP_sm, ARQ_bird_FP_md, ARQ_bird_FP_lg, ARQ_bird_AR_sm, ARQ_bird_AR_md, ARQ_bird_AR_lg, ARQ_bird_SE_sm, ARQ_bird_SE_md, ARQ_bird_SE_lg)
        t7_add_rows = gethtmlrowsfromcols(t7_add_data,pv7headings)       
        html = html + tmpl.render(Context(dict(data=t7_add_rows, headings=pv7headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'ARQ_bird_SG_sm':ARQ_bird_SG_sm, 'ARQ_bird_SG_md':ARQ_bird_SG_md, 'ARQ_bird_SG_lg':ARQ_bird_SG_lg, 'ARQ_bird_TG_sm':ARQ_bird_TG_sm, 'ARQ_bird_TG_md':ARQ_bird_TG_md, 'ARQ_bird_TG_lg':ARQ_bird_TG_lg, 
                             'ARQ_bird_BP_sm':ARQ_bird_BP_sm, 'ARQ_bird_BP_md':ARQ_bird_BP_md, 'ARQ_bird_BP_lg':ARQ_bird_BP_lg, 'ARQ_bird_FP_sm':ARQ_bird_FP_sm, 'ARQ_bird_FP_md':ARQ_bird_FP_md, 'ARQ_bird_FP_lg':ARQ_bird_FP_lg, 
                             'ARQ_bird_AR_sm':ARQ_bird_AR_sm, 'ARQ_bird_AR_md':ARQ_bird_AR_md, 'ARQ_bird_AR_lg':ARQ_bird_AR_lg, 'ARQ_bird_SE_sm':ARQ_bird_SE_sm, 'ARQ_bird_SE_md':ARQ_bird_SE_md, 'ARQ_bird_SE_lg':ARQ_bird_SE_lg}

def table_8(trex2_obj):
        #pre-table 8
        html = """
            <H4 class="out_ collapsible" id="section9"><span></span>Avian Dietary Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 8
        ARQ_diet_bird_SG_A=trex2_obj.ARQ_diet_bird_SG_A
        ARQ_diet_bird_SG_C=trex2_obj.ARQ_diet_bird_SG_C
        ARQ_diet_bird_TG_A=trex2_obj.ARQ_diet_bird_TG_A
        ARQ_diet_bird_TG_C=trex2_obj.ARQ_diet_bird_TG_C
        ARQ_diet_bird_BP_A=trex2_obj.ARQ_diet_bird_BP_A
        ARQ_diet_bird_BP_C=trex2_obj.ARQ_diet_bird_BP_C
        ARQ_diet_bird_FP_A=trex2_obj.ARQ_diet_bird_FP_A
        ARQ_diet_bird_FP_C=trex2_obj.ARQ_diet_bird_FP_C
        ARQ_diet_bird_AR_A=trex2_obj.ARQ_diet_bird_AR_A
        ARQ_diet_bird_AR_C=trex2_obj.ARQ_diet_bird_AR_C
                      
        t8data = gett8data(ARQ_diet_bird_SG_A, ARQ_diet_bird_SG_C, ARQ_diet_bird_TG_A, ARQ_diet_bird_TG_C, ARQ_diet_bird_BP_A, ARQ_diet_bird_BP_C, ARQ_diet_bird_FP_A, ARQ_diet_bird_FP_C, ARQ_diet_bird_AR_A, ARQ_diet_bird_AR_C)
        t8rows = gethtmlrowsfromcols(t8data,pv8headings)       
        html = html + tmpl.render(Context(dict(data=t8rows, headings=pv8headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'ARQ_diet_bird_SG_A':ARQ_diet_bird_SG_A, 'ARQ_diet_bird_SG_C':ARQ_diet_bird_SG_C, 
                             'ARQ_diet_bird_TG_A':ARQ_diet_bird_TG_A, 'ARQ_diet_bird_TG_C':ARQ_diet_bird_TG_C, 
                             'ARQ_diet_bird_BP_A':ARQ_diet_bird_BP_A, 'ARQ_diet_bird_BP_C':ARQ_diet_bird_BP_C,
                             'ARQ_diet_bird_FP_A':ARQ_diet_bird_FP_A, 'ARQ_diet_bird_FP_C':ARQ_diet_bird_FP_C, 
                             'ARQ_diet_bird_AR_A':ARQ_diet_bird_AR_A, 'ARQ_diet_bird_AR_C':ARQ_diet_bird_AR_C}


def table_9(trex2_obj):
        #pre-table 9
        html = """
            <H4 class="out_ collapsible" id="section10"><span></span>Mammalian Dose Based EECs (mg/kg-bw)</H4>
                <div class="out_ container_output">
        """
        #table 9
        EEC_dose_mamm_SG_sm=trex2_obj.EEC_dose_mamm_SG_sm
        EEC_dose_mamm_SG_md=trex2_obj.EEC_dose_mamm_SG_md
        EEC_dose_mamm_SG_lg=trex2_obj.EEC_dose_mamm_SG_lg
        EEC_dose_mamm_TG_sm=trex2_obj.EEC_dose_mamm_TG_sm
        EEC_dose_mamm_TG_md=trex2_obj.EEC_dose_mamm_TG_md
        EEC_dose_mamm_TG_lg=trex2_obj.EEC_dose_mamm_TG_lg
        EEC_dose_mamm_BP_sm=trex2_obj.EEC_dose_mamm_BP_sm
        EEC_dose_mamm_BP_md=trex2_obj.EEC_dose_mamm_BP_md
        EEC_dose_mamm_BP_lg=trex2_obj.EEC_dose_mamm_BP_lg
        EEC_dose_mamm_FP_sm=trex2_obj.EEC_dose_mamm_FP_sm
        EEC_dose_mamm_FP_md=trex2_obj.EEC_dose_mamm_FP_md
        EEC_dose_mamm_FP_lg=trex2_obj.EEC_dose_mamm_FP_lg
        EEC_dose_mamm_AR_sm=trex2_obj.EEC_dose_mamm_AR_sm
        EEC_dose_mamm_AR_md=trex2_obj.EEC_dose_mamm_AR_md
        EEC_dose_mamm_AR_lg=trex2_obj.EEC_dose_mamm_AR_lg
        EEC_dose_mamm_SE_sm=trex2_obj.EEC_dose_mamm_SE_sm
        EEC_dose_mamm_SE_md=trex2_obj.EEC_dose_mamm_SE_md
        EEC_dose_mamm_SE_lg=trex2_obj.EEC_dose_mamm_SE_lg
                      
        t9data = gett9data(EEC_dose_mamm_SG_sm,EEC_dose_mamm_SG_md,EEC_dose_mamm_SG_lg,EEC_dose_mamm_TG_sm,EEC_dose_mamm_TG_md,EEC_dose_mamm_TG_lg,EEC_dose_mamm_BP_sm,EEC_dose_mamm_BP_md,EEC_dose_mamm_BP_lg,EEC_dose_mamm_FP_sm,EEC_dose_mamm_FP_md,EEC_dose_mamm_FP_lg,EEC_dose_mamm_AR_sm,EEC_dose_mamm_AR_md,EEC_dose_mamm_AR_lg,EEC_dose_mamm_SE_sm,EEC_dose_mamm_SE_md,EEC_dose_mamm_SE_lg)
        t9rows = gethtmlrowsfromcols(t9data,pv7headings)       
        html = html + tmpl.render(Context(dict(data=t9rows, headings=pv7headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'EEC_dose_mamm_SG_sm':EEC_dose_mamm_SG_sm, 'EEC_dose_mamm_SG_md':EEC_dose_mamm_SG_md, 'EEC_dose_mamm_SG_lg':EEC_dose_mamm_SG_lg, 'EEC_dose_mamm_TG_sm':EEC_dose_mamm_TG_sm, 'EEC_dose_mamm_TG_md':EEC_dose_mamm_TG_md, 'EEC_dose_mamm_TG_lg':EEC_dose_mamm_TG_lg,
                             'EEC_dose_mamm_BP_sm':EEC_dose_mamm_BP_sm, 'EEC_dose_mamm_BP_md':EEC_dose_mamm_BP_md, 'EEC_dose_mamm_BP_lg':EEC_dose_mamm_BP_lg, 'EEC_dose_mamm_FP_sm':EEC_dose_mamm_FP_sm, 'EEC_dose_mamm_FP_md':EEC_dose_mamm_FP_md, 'EEC_dose_mamm_FP_lg':EEC_dose_mamm_FP_lg,
                             'EEC_dose_mamm_AR_sm':EEC_dose_mamm_AR_sm, 'EEC_dose_mamm_AR_md':EEC_dose_mamm_AR_md, 'EEC_dose_mamm_AR_lg':EEC_dose_mamm_AR_lg, 'EEC_dose_mamm_SE_sm':EEC_dose_mamm_SE_sm, 'EEC_dose_mamm_SE_md':EEC_dose_mamm_SE_md, 'EEC_dose_mamm_SE_lg':EEC_dose_mamm_SE_lg}

def table_10(trex2_obj):
        #pre-table 10
        html = """
            <H4 class="out_ collapsible" id="section11"><span></span>Mammalian Dose Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 10
        ARQ_dose_mamm_SG_sm=trex2_obj.ARQ_dose_mamm_SG_sm
        CRQ_dose_mamm_SG_sm=trex2_obj.CRQ_dose_mamm_SG_sm
        ARQ_dose_mamm_SG_md=trex2_obj.ARQ_dose_mamm_SG_md
        CRQ_dose_mamm_SG_md=trex2_obj.CRQ_dose_mamm_SG_md
        ARQ_dose_mamm_SG_lg=trex2_obj.ARQ_dose_mamm_SG_lg
        CRQ_dose_mamm_SG_lg=trex2_obj.CRQ_dose_mamm_SG_lg
        
        ARQ_dose_mamm_TG_sm=trex2_obj.ARQ_dose_mamm_TG_sm
        CRQ_dose_mamm_TG_sm=trex2_obj.CRQ_dose_mamm_TG_sm
        ARQ_dose_mamm_TG_md=trex2_obj.ARQ_dose_mamm_TG_md
        CRQ_dose_mamm_TG_md=trex2_obj.CRQ_dose_mamm_TG_md
        ARQ_dose_mamm_TG_lg=trex2_obj.ARQ_dose_mamm_TG_lg
        CRQ_dose_mamm_TG_lg=trex2_obj.CRQ_dose_mamm_TG_lg
        
        ARQ_dose_mamm_BP_sm=trex2_obj.ARQ_dose_mamm_BP_sm
        CRQ_dose_mamm_BP_sm=trex2_obj.CRQ_dose_mamm_BP_sm
        ARQ_dose_mamm_BP_md=trex2_obj.ARQ_dose_mamm_BP_md
        CRQ_dose_mamm_BP_md=trex2_obj.CRQ_dose_mamm_BP_md
        ARQ_dose_mamm_BP_lg=trex2_obj.ARQ_dose_mamm_BP_lg
        CRQ_dose_mamm_BP_lg=trex2_obj.CRQ_dose_mamm_BP_lg
        
        ARQ_dose_mamm_FP_sm=trex2_obj.ARQ_dose_mamm_FP_sm
        CRQ_dose_mamm_FP_sm=trex2_obj.CRQ_dose_mamm_FP_sm
        ARQ_dose_mamm_FP_md=trex2_obj.ARQ_dose_mamm_FP_md
        CRQ_dose_mamm_FP_md=trex2_obj.CRQ_dose_mamm_FP_md
        ARQ_dose_mamm_FP_lg=trex2_obj.ARQ_dose_mamm_FP_lg
        CRQ_dose_mamm_FP_lg=trex2_obj.CRQ_dose_mamm_FP_lg
        
        ARQ_dose_mamm_AR_sm=trex2_obj.ARQ_dose_mamm_AR_sm
        CRQ_dose_mamm_AR_sm=trex2_obj.CRQ_dose_mamm_AR_sm
        ARQ_dose_mamm_AR_md=trex2_obj.ARQ_dose_mamm_AR_md
        CRQ_dose_mamm_AR_md=trex2_obj.CRQ_dose_mamm_AR_md
        ARQ_dose_mamm_AR_lg=trex2_obj.ARQ_dose_mamm_AR_lg
        CRQ_dose_mamm_AR_lg=trex2_obj.CRQ_dose_mamm_AR_lg
        
        ARQ_dose_mamm_SE_sm=trex2_obj.ARQ_dose_mamm_SE_sm
        CRQ_dose_mamm_SE_sm=trex2_obj.CRQ_dose_mamm_SE_sm
        ARQ_dose_mamm_SE_md=trex2_obj.ARQ_dose_mamm_SE_md
        CRQ_dose_mamm_SE_md=trex2_obj.CRQ_dose_mamm_SE_md
        ARQ_dose_mamm_SE_lg=trex2_obj.ARQ_dose_mamm_SE_lg
        CRQ_dose_mamm_SE_lg=trex2_obj.CRQ_dose_mamm_SE_lg
                      
        t10data = gett10data(ARQ_dose_mamm_SG_sm,CRQ_dose_mamm_SG_sm,ARQ_dose_mamm_SG_md,CRQ_dose_mamm_SG_md,ARQ_dose_mamm_SG_lg,CRQ_dose_mamm_SG_lg,ARQ_dose_mamm_TG_sm,CRQ_dose_mamm_TG_sm,ARQ_dose_mamm_TG_md,CRQ_dose_mamm_TG_md,ARQ_dose_mamm_TG_lg,CRQ_dose_mamm_TG_lg,ARQ_dose_mamm_BP_sm,CRQ_dose_mamm_BP_sm,ARQ_dose_mamm_BP_md,CRQ_dose_mamm_BP_md,ARQ_dose_mamm_BP_lg,CRQ_dose_mamm_BP_lg,ARQ_dose_mamm_FP_sm,CRQ_dose_mamm_FP_sm,ARQ_dose_mamm_FP_md,CRQ_dose_mamm_FP_md,ARQ_dose_mamm_FP_lg,CRQ_dose_mamm_FP_lg,ARQ_dose_mamm_AR_sm,CRQ_dose_mamm_AR_sm,ARQ_dose_mamm_AR_md,CRQ_dose_mamm_AR_md,ARQ_dose_mamm_AR_lg,CRQ_dose_mamm_AR_lg,ARQ_dose_mamm_SE_sm,CRQ_dose_mamm_SE_sm,ARQ_dose_mamm_SE_md,CRQ_dose_mamm_SE_md,ARQ_dose_mamm_SE_lg,CRQ_dose_mamm_SE_lg)
        t10rows = gethtmlrowsfromcols(t10data, pv10headings)       
        html = html + tmpl_10.render(Context(dict(data=t10rows)))
        html = html + """
                </div>
        """
        return {'html':html, 'ARQ_dose_mamm_SG_sm':ARQ_dose_mamm_SG_sm, 'CRQ_dose_mamm_SG_sm':CRQ_dose_mamm_SG_sm, 'ARQ_dose_mamm_SG_md':ARQ_dose_mamm_SG_md, 'CRQ_dose_mamm_SG_md':CRQ_dose_mamm_SG_md, 'ARQ_dose_mamm_SG_lg':ARQ_dose_mamm_SG_lg, 'CRQ_dose_mamm_SG_lg':CRQ_dose_mamm_SG_lg,
                             'ARQ_dose_mamm_TG_sm':ARQ_dose_mamm_TG_sm, 'CRQ_dose_mamm_TG_sm':CRQ_dose_mamm_TG_sm, 'ARQ_dose_mamm_TG_md':ARQ_dose_mamm_TG_md, 'CRQ_dose_mamm_TG_md':CRQ_dose_mamm_TG_md, 'ARQ_dose_mamm_TG_lg':ARQ_dose_mamm_TG_lg, 'CRQ_dose_mamm_TG_lg':CRQ_dose_mamm_TG_lg,
                             'ARQ_dose_mamm_BP_sm':ARQ_dose_mamm_BP_sm, 'CRQ_dose_mamm_BP_sm':CRQ_dose_mamm_BP_sm, 'ARQ_dose_mamm_BP_md':ARQ_dose_mamm_BP_md, 'CRQ_dose_mamm_BP_md':CRQ_dose_mamm_BP_md, 'ARQ_dose_mamm_BP_lg':ARQ_dose_mamm_BP_lg, 'CRQ_dose_mamm_BP_lg':CRQ_dose_mamm_BP_lg,
                             'ARQ_dose_mamm_FP_sm':ARQ_dose_mamm_FP_sm, 'CRQ_dose_mamm_FP_sm':CRQ_dose_mamm_FP_sm, 'ARQ_dose_mamm_FP_md':ARQ_dose_mamm_FP_md, 'CRQ_dose_mamm_FP_md':CRQ_dose_mamm_FP_md, 'ARQ_dose_mamm_FP_lg':ARQ_dose_mamm_FP_lg, 'CRQ_dose_mamm_FP_lg':CRQ_dose_mamm_FP_lg,
                             'ARQ_dose_mamm_AR_sm':ARQ_dose_mamm_AR_sm, 'CRQ_dose_mamm_AR_sm':CRQ_dose_mamm_AR_sm, 'ARQ_dose_mamm_AR_md':ARQ_dose_mamm_AR_md, 'CRQ_dose_mamm_AR_md':CRQ_dose_mamm_AR_md, 'ARQ_dose_mamm_AR_lg':ARQ_dose_mamm_AR_lg, 'CRQ_dose_mamm_AR_lg':CRQ_dose_mamm_AR_lg,
                             'ARQ_dose_mamm_SE_sm':ARQ_dose_mamm_SE_sm, 'CRQ_dose_mamm_SE_sm':CRQ_dose_mamm_SE_sm, 'ARQ_dose_mamm_SE_md':ARQ_dose_mamm_SE_md, 'CRQ_dose_mamm_SE_md':CRQ_dose_mamm_SE_md, 'ARQ_dose_mamm_SE_lg':ARQ_dose_mamm_SE_lg, 'CRQ_dose_mamm_SE_lg':CRQ_dose_mamm_SE_lg}

def table_11(trex2_obj):
        #pre-table 11
        html = """
            <H4 class="out_ collapsible" id="section12"><span></span>Mammalian Dietary Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 11
        ARQ_diet_mamm_SG=trex2_obj.ARQ_diet_mamm_SG
        CRQ_diet_mamm_SG=trex2_obj.CRQ_diet_mamm_SG
        ARQ_diet_mamm_TG=trex2_obj.ARQ_diet_mamm_TG
        CRQ_diet_mamm_TG=trex2_obj.CRQ_diet_mamm_TG
        ARQ_diet_mamm_BP=trex2_obj.ARQ_diet_mamm_BP
        CRQ_diet_mamm_BP=trex2_obj.CRQ_diet_mamm_BP
        ARQ_diet_mamm_FP=trex2_obj.ARQ_diet_mamm_FP
        CRQ_diet_mamm_FP=trex2_obj.CRQ_diet_mamm_FP
        ARQ_diet_mamm_AR=trex2_obj.ARQ_diet_mamm_AR
        CRQ_diet_mamm_AR=trex2_obj.CRQ_diet_mamm_AR
        if ARQ_diet_mamm_SG=='N/A':
            t11data = gett11data_na(ARQ_diet_mamm_SG,CRQ_diet_mamm_SG,ARQ_diet_mamm_TG,CRQ_diet_mamm_TG,ARQ_diet_mamm_BP,CRQ_diet_mamm_BP,ARQ_diet_mamm_FP,CRQ_diet_mamm_FP,ARQ_diet_mamm_AR,CRQ_diet_mamm_AR)
        else:
            t11data = gett11data(ARQ_diet_mamm_SG,CRQ_diet_mamm_SG,ARQ_diet_mamm_TG,CRQ_diet_mamm_TG,ARQ_diet_mamm_BP,CRQ_diet_mamm_BP,ARQ_diet_mamm_FP,CRQ_diet_mamm_FP,ARQ_diet_mamm_AR,CRQ_diet_mamm_AR)
        t11rows = gethtmlrowsfromcols(t11data,pv8headings)       
        html = html + tmpl.render(Context(dict(data=t11rows, headings=pv8headings)))
        html = html + """
                </div>
        """
        return {'html':html, 'ARQ_diet_mamm_SG':ARQ_diet_mamm_SG, 'CRQ_diet_mamm_SG':CRQ_diet_mamm_SG, 'ARQ_diet_mamm_TG':ARQ_diet_mamm_TG, 'CRQ_diet_mamm_TG':CRQ_diet_mamm_TG,
                             'ARQ_diet_mamm_BP':ARQ_diet_mamm_BP, 'CRQ_diet_mamm_BP':CRQ_diet_mamm_BP, 'ARQ_diet_mamm_FP':ARQ_diet_mamm_FP, 'CRQ_diet_mamm_FP':CRQ_diet_mamm_FP,
                             'ARQ_diet_mamm_AR':ARQ_diet_mamm_AR, 'CRQ_diet_mamm_AR':CRQ_diet_mamm_AR}


def table_12(trex2_obj):
        #pre-table 12
        html = """
            <H4 class="out_ collapsible" id="section13"><span></span>LD<sub>50</sub> ft<sup>-2</sup></H4>
                <div class="out_ container_output">
        """
        #table 12
        LD50_rg_bird_sm=trex2_obj.LD50_rg_bird_sm
        LD50_rg_mamm_sm=trex2_obj.LD50_rg_mamm_sm
        LD50_rg_bird_md=trex2_obj.LD50_rg_bird_md
        LD50_rg_mamm_md=trex2_obj.LD50_rg_mamm_md
        LD50_rg_bird_lg=trex2_obj.LD50_rg_bird_lg
        LD50_rg_mamm_lg=trex2_obj.LD50_rg_mamm_lg

        t12data = gett12data(LD50_rg_bird_sm,LD50_rg_mamm_sm,LD50_rg_bird_md,LD50_rg_mamm_md,LD50_rg_bird_lg,LD50_rg_mamm_lg)
        t12rows = gethtmlrowsfromcols(t12data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t12rows, headings=pv12headings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'LD50_rg_bird_sm':LD50_rg_bird_sm, 'LD50_rg_mamm_sm':LD50_rg_mamm_sm,
                             'LD50_rg_bird_md':LD50_rg_bird_md, 'LD50_rg_mamm_md':LD50_rg_mamm_md,
                             'LD50_rg_bird_lg':LD50_rg_bird_lg, 'LD50_rg_mamm_lg':LD50_rg_mamm_lg}


def table_13(trex2_obj):
        #pre-table 13
        html = """
            <H4 class="out_ collapsible" id="section13"><span></span>LD<sub>50</sub> ft<sup>-2</sup></H4>
                <div class="out_ container_output">
        """
        #table 13
        LD50_rl_bird_sm=trex2_obj.LD50_rl_bird_sm
        LD50_rl_mamm_sm=trex2_obj.LD50_rl_mamm_sm
        LD50_rl_bird_md=trex2_obj.LD50_rl_bird_md
        LD50_rl_mamm_md=trex2_obj.LD50_rl_mamm_md
        LD50_rl_bird_lg=trex2_obj.LD50_rl_bird_lg
        LD50_rl_mamm_lg=trex2_obj.LD50_rl_mamm_lg

        t13data = gett12data(LD50_rl_bird_sm,LD50_rl_mamm_sm,LD50_rl_bird_md,LD50_rl_mamm_md,LD50_rl_bird_lg,LD50_rl_mamm_lg)
        t13rows = gethtmlrowsfromcols(t13data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t13rows, headings=pv12headings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'LD50_rl_bird_sm':LD50_rl_bird_sm, 'LD50_rl_mamm_sm':LD50_rl_mamm_sm,
                             'LD50_rl_bird_md':LD50_rl_bird_md, 'LD50_rl_mamm_md':LD50_rl_mamm_md,
                             'LD50_rl_bird_lg':LD50_rl_bird_lg, 'LD50_rl_mamm_lg':LD50_rl_mamm_lg}


def table_14(trex2_obj):
        #pre-table 14
        html = """
            <H4 class="out_ collapsible" id="section13"><span></span>LD<sub>50</sub> ft<sup>-2</sup></H4>
                <div class="out_ container_output">
        """
        #table 14
        LD50_bg_bird_sm=trex2_obj.LD50_bg_bird_sm
        LD50_bg_mamm_sm=trex2_obj.LD50_bg_mamm_sm
        LD50_bg_bird_md=trex2_obj.LD50_bg_bird_md
        LD50_bg_mamm_md=trex2_obj.LD50_bg_mamm_md
        LD50_bg_bird_lg=trex2_obj.LD50_bg_bird_lg
        LD50_bg_mamm_lg=trex2_obj.LD50_bg_mamm_lg

        t14data = gett12data(LD50_bg_bird_sm,LD50_bg_mamm_sm,LD50_bg_bird_md,LD50_bg_mamm_md,LD50_bg_bird_lg,LD50_bg_mamm_lg)
        t14rows = gethtmlrowsfromcols(t14data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t14rows, headings=pv12headings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'LD50_bg_bird_sm':LD50_bg_bird_sm, 'LD50_bg_mamm_sm':LD50_bg_mamm_sm,
                             'LD50_bg_bird_md':LD50_bg_bird_md, 'LD50_bg_mamm_md':LD50_bg_mamm_md,
                             'LD50_bg_bird_lg':LD50_bg_bird_lg, 'LD50_bg_mamm_lg':LD50_bg_mamm_lg}
                             
def table_15(trex2_obj):
        #pre-table 15
        html = """
            <H4 class="out_ collapsible" id="section13"><span></span>LD<sub>50</sub> ft<sup>-2</sup></H4>
                <div class="out_ container_output">
        """
        #table 15
        LD50_bl_bird_sm=trex2_obj.LD50_bl_bird_sm
        LD50_bl_mamm_sm=trex2_obj.LD50_bl_mamm_sm
        LD50_bl_bird_md=trex2_obj.LD50_bl_bird_md
        LD50_bl_mamm_md=trex2_obj.LD50_bl_mamm_md
        LD50_bl_bird_lg=trex2_obj.LD50_bl_bird_lg
        LD50_bl_mamm_lg=trex2_obj.LD50_bl_mamm_lg

        t15data = gett12data(LD50_bl_bird_sm,LD50_bl_mamm_sm,LD50_bl_bird_md,LD50_bl_mamm_md,LD50_bl_bird_lg,LD50_bl_mamm_lg)
        t15rows = gethtmlrowsfromcols(t15data,pv12headings)       
        html = html + tmpl.render(Context(dict(data=t15rows, headings=pv12headings)))
        html = html + """
                </div>
        </div>
        """
        return {'html':html, 'LD50_bl_bird_sm':LD50_bl_bird_sm, 'LD50_bl_mamm_sm':LD50_bl_mamm_sm,
                             'LD50_bl_bird_md':LD50_bl_bird_md, 'LD50_bl_mamm_md':LD50_bl_mamm_md,
                             'LD50_bl_bird_lg':LD50_bl_bird_lg, 'LD50_bl_mamm_lg':LD50_bl_mamm_lg}

def table_5_qaqc(trex2_obj):
        #pre-table 5_qaqc
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section6"><span></span>Results (Upper Bound Kenaga): Application Type : Seed Treatment</H3>
            <div class="out_ container_output">
        """
        #table 5_qaqc
        sa_bird_1_s=trex2_obj.sa_bird_1_s
        sa_bird_2_s=trex2_obj.sa_bird_2_s
        sc_bird_s=trex2_obj.sc_bird_s
        sa_mamm_1_s=trex2_obj.sa_mamm_1_s
        sa_mamm_2_s=trex2_obj.sa_mamm_2_s
        sc_mamm_s=trex2_obj.sc_mamm_s
        
        sa_bird_1_m=trex2_obj.sa_bird_1_m
        sa_bird_2_m=trex2_obj.sa_bird_2_m
        sc_bird_m=trex2_obj.sc_bird_m
        sa_mamm_1_m=trex2_obj.sa_mamm_1_m
        sa_mamm_2_m=trex2_obj.sa_mamm_2_m
        sc_mamm_m=trex2_obj.sc_mamm_m
             
        sa_bird_1_l=trex2_obj.sa_bird_1_l
        sa_bird_2_l=trex2_obj.sa_bird_2_l
        sc_bird_l=trex2_obj.sc_bird_l
        sa_mamm_1_l=trex2_obj.sa_mamm_1_l
        sa_mamm_2_l=trex2_obj.sa_mamm_2_l
        sc_mamm_l=trex2_obj.sc_mamm_l

        sa_bird_1_s_exp=trex2_obj.sa_bird_1_s_out_exp
        sa_bird_2_s_exp=trex2_obj.sa_bird_2_s_out_exp
        sc_bird_s_exp=trex2_obj.sc_bird_s_out_exp
        sa_mamm_1_s_exp=trex2_obj.sa_mamm_1_s_out_exp
        sa_mamm_2_s_exp=trex2_obj.sa_mamm_2_s_out_exp
        sc_mamm_s_exp=trex2_obj.sc_mamm_s_out_exp
        
        sa_bird_1_m_exp=trex2_obj.sa_bird_1_m_out_exp
        sa_bird_2_m_exp=trex2_obj.sa_bird_2_m_out_exp
        sc_bird_m_exp=trex2_obj.sc_bird_m_out_exp
        sa_mamm_1_m_exp=trex2_obj.sa_mamm_1_m_out_exp
        sa_mamm_2_m_exp=trex2_obj.sa_mamm_2_m_out_exp
        sc_mamm_m_exp=trex2_obj.sc_mamm_m_out_exp
             
        sa_bird_1_l_exp=trex2_obj.sa_bird_1_l_out_exp
        sa_bird_2_l_exp=trex2_obj.sa_bird_2_l_out_exp
        sc_bird_l_exp=trex2_obj.sc_bird_l_out_exp
        sa_mamm_1_l_exp=trex2_obj.sa_mamm_1_l_out_exp
        sa_mamm_2_l_exp=trex2_obj.sa_mamm_2_l_out_exp
        sc_mamm_l_exp=trex2_obj.sc_mamm_l_out_exp

        t5data_qaqc = gett5data_qaqc(sa_bird_1_s, sa_bird_2_s, sc_bird_s, sa_mamm_1_s, sa_mamm_2_s, sc_mamm_s, 
                           sa_bird_1_m, sa_bird_2_m, sc_bird_m, sa_mamm_1_m, sa_mamm_2_m, sc_mamm_m,
                           sa_bird_1_l, sa_bird_2_l, sc_bird_l, sa_mamm_1_l, sa_mamm_2_l, sc_mamm_l,
                           sa_bird_1_s_exp, sa_bird_2_s_exp, sc_bird_s_exp, sa_mamm_1_s_exp, sa_mamm_2_s_exp, sc_mamm_s_exp, 
                           sa_bird_1_m_exp, sa_bird_2_m_exp, sc_bird_m_exp, sa_mamm_1_m_exp, sa_mamm_2_m_exp, sc_mamm_m_exp,
                           sa_bird_1_l_exp, sa_bird_2_l_exp, sc_bird_l_exp, sa_mamm_1_l_exp, sa_mamm_2_l_exp, sc_mamm_l_exp)
        t5rows_qaqc = gethtmlrowsfromcols(t5data_qaqc, pv5headings_qaqc[1])     
        html = html + tmpl.render(Context(dict(data=t5rows_qaqc, headings=pv5headings_qaqc[0], sub_headings=pv5headings_qaqc[2], sub_headings_1=pv5headings_qaqc[3], th_span='4')))
        html = html + """
                </div>
        """  
        return html

def table_6_qaqc(trex2_obj):
        #pre-table 6_qaqc
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section6"><span></span>Results: Application Type : Broadcast-Liquid</H3>
        <div class="out_">
            <H4 class="out_ collapsible" id="section7"><span></span>Dietary Based EECs (mg/kg-dietary item)</H4>
                <div class="out_ container_output">
        """
        #table 6_qaqc
        EEC_diet_SG=trex2_obj.EEC_diet_SG
        EEC_diet_TG=trex2_obj.EEC_diet_TG
        EEC_diet_BP=trex2_obj.EEC_diet_BP
        EEC_diet_FR=trex2_obj.EEC_diet_FR
        EEC_diet_AR=trex2_obj.EEC_diet_AR

        EEC_diet_SG_exp=trex2_obj.EEC_diet_SG_BL_out_exp
        EEC_diet_TG_exp=trex2_obj.EEC_diet_TG_BL_out_exp
        EEC_diet_BP_exp=trex2_obj.EEC_diet_BP_BL_out_exp
        EEC_diet_FR_exp=trex2_obj.EEC_diet_FR_BL_out_exp
        EEC_diet_AR_exp=trex2_obj.EEC_diet_AR_BL_out_exp

        t6data_qaqc = gett6data_qaqc(EEC_diet_SG, EEC_diet_TG, EEC_diet_BP, EEC_diet_FR, EEC_diet_AR, EEC_diet_SG_exp, EEC_diet_TG_exp, EEC_diet_BP_exp, EEC_diet_FR_exp, EEC_diet_AR_exp)
        t6rows_qaqc = gethtmlrowsfromcols(t6data_qaqc,pv6headings_qaqc)
        html = html + tmpl.render(Context(dict(data=t6rows_qaqc, headings=pv6headings_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_7_qaqc(trex2_obj):
        #pre-table 7
        html = """
            <H4 class="out_ collapsible" id="section8"><span></span>Avian Dose Based EECs (mg/kg-bw)</H4>
                <div class="out_ container_output">
        """
        #table 7
        EEC_dose_bird_SG_sm=trex2_obj.EEC_dose_bird_SG_sm
        EEC_dose_bird_SG_md=trex2_obj.EEC_dose_bird_SG_md
        EEC_dose_bird_SG_lg=trex2_obj.EEC_dose_bird_SG_lg
        EEC_dose_bird_TG_sm=trex2_obj.EEC_dose_bird_TG_sm
        EEC_dose_bird_TG_md=trex2_obj.EEC_dose_bird_TG_md
        EEC_dose_bird_TG_lg=trex2_obj.EEC_dose_bird_TG_lg
        EEC_dose_bird_BP_sm=trex2_obj.EEC_dose_bird_BP_sm
        EEC_dose_bird_BP_md=trex2_obj.EEC_dose_bird_BP_md
        EEC_dose_bird_BP_lg=trex2_obj.EEC_dose_bird_BP_lg
        EEC_dose_bird_FP_sm=trex2_obj.EEC_dose_bird_FP_sm
        EEC_dose_bird_FP_md=trex2_obj.EEC_dose_bird_FP_md
        EEC_dose_bird_FP_lg=trex2_obj.EEC_dose_bird_FP_lg
        EEC_dose_bird_AR_sm=trex2_obj.EEC_dose_bird_AR_sm
        EEC_dose_bird_AR_md=trex2_obj.EEC_dose_bird_AR_md
        EEC_dose_bird_AR_lg=trex2_obj.EEC_dose_bird_AR_lg
        EEC_dose_bird_SE_sm=trex2_obj.EEC_dose_bird_SE_sm
        EEC_dose_bird_SE_md=trex2_obj.EEC_dose_bird_SE_md
        EEC_dose_bird_SE_lg=trex2_obj.EEC_dose_bird_SE_lg

        EEC_dose_bird_SG_sm_exp=trex2_obj.EEC_dose_bird_SG_BL_sm_out_exp
        EEC_dose_bird_SG_md_exp=trex2_obj.EEC_dose_bird_SG_BL_md_out_exp
        EEC_dose_bird_SG_lg_exp=trex2_obj.EEC_dose_bird_SG_BL_lg_out_exp
        EEC_dose_bird_TG_sm_exp=trex2_obj.EEC_dose_bird_TG_BL_sm_out_exp
        EEC_dose_bird_TG_md_exp=trex2_obj.EEC_dose_bird_TG_BL_md_out_exp
        EEC_dose_bird_TG_lg_exp=trex2_obj.EEC_dose_bird_TG_BL_lg_out_exp
        EEC_dose_bird_BP_sm_exp=trex2_obj.EEC_dose_bird_BP_BL_sm_out_exp
        EEC_dose_bird_BP_md_exp=trex2_obj.EEC_dose_bird_BP_BL_md_out_exp
        EEC_dose_bird_BP_lg_exp=trex2_obj.EEC_dose_bird_BP_BL_lg_out_exp
        EEC_dose_bird_FP_sm_exp=trex2_obj.EEC_dose_bird_FP_BL_sm_out_exp
        EEC_dose_bird_FP_md_exp=trex2_obj.EEC_dose_bird_FP_BL_md_out_exp
        EEC_dose_bird_FP_lg_exp=trex2_obj.EEC_dose_bird_FP_BL_lg_out_exp
        EEC_dose_bird_AR_sm_exp=trex2_obj.EEC_dose_bird_AR_BL_sm_out_exp
        EEC_dose_bird_AR_md_exp=trex2_obj.EEC_dose_bird_AR_BL_md_out_exp
        EEC_dose_bird_AR_lg_exp=trex2_obj.EEC_dose_bird_AR_BL_lg_out_exp
        EEC_dose_bird_SE_sm_exp=trex2_obj.EEC_dose_bird_SE_BL_sm_out_exp
        EEC_dose_bird_SE_md_exp=trex2_obj.EEC_dose_bird_SE_BL_md_out_exp
        EEC_dose_bird_SE_lg_exp=trex2_obj.EEC_dose_bird_SE_BL_lg_out_exp


        t7data_qaqc = gett7data_qaqc(EEC_dose_bird_SG_sm, EEC_dose_bird_SG_md, EEC_dose_bird_SG_lg, EEC_dose_bird_TG_sm, EEC_dose_bird_TG_md, EEC_dose_bird_TG_lg, EEC_dose_bird_BP_sm, EEC_dose_bird_BP_md, EEC_dose_bird_BP_lg, EEC_dose_bird_FP_sm, EEC_dose_bird_FP_md, EEC_dose_bird_FP_lg, EEC_dose_bird_AR_sm, EEC_dose_bird_AR_md, EEC_dose_bird_AR_lg, EEC_dose_bird_SE_sm, EEC_dose_bird_SE_md, EEC_dose_bird_SE_lg,
                                     EEC_dose_bird_SG_sm_exp, EEC_dose_bird_SG_md_exp, EEC_dose_bird_SG_lg_exp, EEC_dose_bird_TG_sm_exp, EEC_dose_bird_TG_md_exp, EEC_dose_bird_TG_lg_exp, EEC_dose_bird_BP_sm_exp, EEC_dose_bird_BP_md_exp, EEC_dose_bird_BP_lg_exp, EEC_dose_bird_FP_sm_exp, EEC_dose_bird_FP_md_exp, EEC_dose_bird_FP_lg_exp, EEC_dose_bird_AR_sm_exp, EEC_dose_bird_AR_md_exp, EEC_dose_bird_AR_lg_exp, EEC_dose_bird_SE_sm_exp, EEC_dose_bird_SE_md_exp, EEC_dose_bird_SE_lg_exp)
        t7rows_qaqc = gethtmlrowsfromcols(t7data_qaqc, pv7headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t7rows_qaqc, headings=pv7headings_qaqc)))
        html = html + """
                </div>
        """
        return html


def table_7_add_qaqc(trex2_obj):
        #pre-table 7
        html = """
            <H4 class="out_ collapsible" id="section8_add"><span></span>Avianr Dose Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 7_add
        ARQ_bird_SG_sm=trex2_obj.ARQ_bird_SG_sm
        ARQ_bird_SG_md=trex2_obj.ARQ_bird_SG_md
        ARQ_bird_SG_lg=trex2_obj.ARQ_bird_SG_lg
        ARQ_bird_TG_sm=trex2_obj.ARQ_bird_TG_sm
        ARQ_bird_TG_md=trex2_obj.ARQ_bird_TG_md
        ARQ_bird_TG_lg=trex2_obj.ARQ_bird_TG_lg
        ARQ_bird_BP_sm=trex2_obj.ARQ_bird_BP_sm
        ARQ_bird_BP_md=trex2_obj.ARQ_bird_BP_md
        ARQ_bird_BP_lg=trex2_obj.ARQ_bird_BP_lg
        ARQ_bird_FP_sm=trex2_obj.ARQ_bird_FP_sm
        ARQ_bird_FP_md=trex2_obj.ARQ_bird_FP_md
        ARQ_bird_FP_lg=trex2_obj.ARQ_bird_FP_lg
        ARQ_bird_AR_sm=trex2_obj.ARQ_bird_AR_sm
        ARQ_bird_AR_md=trex2_obj.ARQ_bird_AR_md
        ARQ_bird_AR_lg=trex2_obj.ARQ_bird_AR_lg
        ARQ_bird_SE_sm=trex2_obj.ARQ_bird_SE_sm
        ARQ_bird_SE_md=trex2_obj.ARQ_bird_SE_md
        ARQ_bird_SE_lg=trex2_obj.ARQ_bird_SE_lg

        ARQ_bird_SG_sm_exp=trex2_obj.ARQ_bird_SG_BL_sm_out_exp
        ARQ_bird_SG_md_exp=trex2_obj.ARQ_bird_SG_BL_md_out_exp
        ARQ_bird_SG_lg_exp=trex2_obj.ARQ_bird_SG_BL_lg_out_exp
        ARQ_bird_TG_sm_exp=trex2_obj.ARQ_bird_TG_BL_sm_out_exp
        ARQ_bird_TG_md_exp=trex2_obj.ARQ_bird_TG_BL_md_out_exp
        ARQ_bird_TG_lg_exp=trex2_obj.ARQ_bird_TG_BL_lg_out_exp
        ARQ_bird_BP_sm_exp=trex2_obj.ARQ_bird_BP_BL_sm_out_exp
        ARQ_bird_BP_md_exp=trex2_obj.ARQ_bird_BP_BL_md_out_exp
        ARQ_bird_BP_lg_exp=trex2_obj.ARQ_bird_BP_BL_lg_out_exp
        ARQ_bird_FP_sm_exp=trex2_obj.ARQ_bird_FP_BL_sm_out_exp
        ARQ_bird_FP_md_exp=trex2_obj.ARQ_bird_FP_BL_md_out_exp
        ARQ_bird_FP_lg_exp=trex2_obj.ARQ_bird_FP_BL_lg_out_exp
        ARQ_bird_AR_sm_exp=trex2_obj.ARQ_bird_AR_BL_sm_out_exp
        ARQ_bird_AR_md_exp=trex2_obj.ARQ_bird_AR_BL_md_out_exp
        ARQ_bird_AR_lg_exp=trex2_obj.ARQ_bird_AR_BL_lg_out_exp
        ARQ_bird_SE_sm_exp=trex2_obj.ARQ_bird_SE_BL_sm_out_exp
        ARQ_bird_SE_md_exp=trex2_obj.ARQ_bird_SE_BL_md_out_exp
        ARQ_bird_SE_lg_exp=trex2_obj.ARQ_bird_SE_BL_lg_out_exp

        t7_add_data_qaqc = gett7_add_data_qaqc(ARQ_bird_SG_sm, ARQ_bird_SG_md, ARQ_bird_SG_lg, ARQ_bird_TG_sm, ARQ_bird_TG_md, ARQ_bird_TG_lg, ARQ_bird_BP_sm, ARQ_bird_BP_md, ARQ_bird_BP_lg, ARQ_bird_FP_sm, ARQ_bird_FP_md, ARQ_bird_FP_lg, ARQ_bird_AR_sm, ARQ_bird_AR_md, ARQ_bird_AR_lg, ARQ_bird_SE_sm, ARQ_bird_SE_md, ARQ_bird_SE_lg, 
                                              ARQ_bird_SG_sm_exp, ARQ_bird_SG_md_exp, ARQ_bird_SG_lg_exp, ARQ_bird_TG_sm_exp, ARQ_bird_TG_md_exp, ARQ_bird_TG_lg_exp, ARQ_bird_BP_sm_exp, ARQ_bird_BP_md_exp, ARQ_bird_BP_lg_exp, ARQ_bird_FP_sm_exp, ARQ_bird_FP_md_exp, ARQ_bird_FP_lg_exp, ARQ_bird_AR_sm_exp, ARQ_bird_AR_md_exp, ARQ_bird_AR_lg_exp, ARQ_bird_SE_sm_exp, ARQ_bird_SE_md_exp, ARQ_bird_SE_lg_exp)
        t7_add_rows_qaqc = gethtmlrowsfromcols(t7_add_data_qaqc, pv7headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t7_add_rows_qaqc, headings=pv7headings_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_8_qaqc(trex2_obj):
        #pre-table 8 qaqc
        html = """
            <H4 class="out_ collapsible" id="section9"><span></span>Avian Dietary Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 8
        ARQ_diet_bird_SG_A=trex2_obj.ARQ_diet_bird_SG_A
        ARQ_diet_bird_SG_C=trex2_obj.ARQ_diet_bird_SG_C
        ARQ_diet_bird_TG_A=trex2_obj.ARQ_diet_bird_TG_A
        ARQ_diet_bird_TG_C=trex2_obj.ARQ_diet_bird_TG_C
        ARQ_diet_bird_BP_A=trex2_obj.ARQ_diet_bird_BP_A
        ARQ_diet_bird_BP_C=trex2_obj.ARQ_diet_bird_BP_C
        ARQ_diet_bird_FP_A=trex2_obj.ARQ_diet_bird_FP_A
        ARQ_diet_bird_FP_C=trex2_obj.ARQ_diet_bird_FP_C
        ARQ_diet_bird_AR_A=trex2_obj.ARQ_diet_bird_AR_A
        ARQ_diet_bird_AR_C=trex2_obj.ARQ_diet_bird_AR_C

        ARQ_diet_bird_SG_A_exp=trex2_obj.ARQ_diet_bird_SG_A_BL_out_exp
        ARQ_diet_bird_SG_C_exp=trex2_obj.ARQ_diet_bird_SG_C_BL_out_exp
        ARQ_diet_bird_TG_A_exp=trex2_obj.ARQ_diet_bird_TG_A_BL_out_exp
        ARQ_diet_bird_TG_C_exp=trex2_obj.ARQ_diet_bird_TG_C_BL_out_exp
        ARQ_diet_bird_BP_A_exp=trex2_obj.ARQ_diet_bird_BP_A_BL_out_exp
        ARQ_diet_bird_BP_C_exp=trex2_obj.ARQ_diet_bird_BP_C_BL_out_exp
        ARQ_diet_bird_FP_A_exp=trex2_obj.ARQ_diet_bird_FP_A_BL_out_exp
        ARQ_diet_bird_FP_C_exp=trex2_obj.ARQ_diet_bird_FP_C_BL_out_exp
        ARQ_diet_bird_AR_A_exp=trex2_obj.ARQ_diet_bird_AR_A_BL_out_exp
        ARQ_diet_bird_AR_C_exp=trex2_obj.ARQ_diet_bird_AR_C_BL_out_exp

        t8data_qaqc = gett8data_qaqc(ARQ_diet_bird_SG_A, ARQ_diet_bird_SG_C, ARQ_diet_bird_TG_A, ARQ_diet_bird_TG_C, ARQ_diet_bird_BP_A, ARQ_diet_bird_BP_C, ARQ_diet_bird_FP_A, ARQ_diet_bird_FP_C, ARQ_diet_bird_AR_A, ARQ_diet_bird_AR_C,
                                     ARQ_diet_bird_SG_A_exp, ARQ_diet_bird_SG_C_exp, ARQ_diet_bird_TG_A_exp, ARQ_diet_bird_TG_C_exp, ARQ_diet_bird_BP_A_exp, ARQ_diet_bird_BP_C_exp, ARQ_diet_bird_FP_A_exp, ARQ_diet_bird_FP_C_exp, ARQ_diet_bird_AR_A_exp, ARQ_diet_bird_AR_C_exp)
        t8rows_qaqc = gethtmlrowsfromcols(t8data_qaqc, pv8headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t8rows_qaqc, headings=pv8headings_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_9_qaqc(trex2_obj):
        #pre-table 9_qaqc
        html = """
            <H4 class="out_ collapsible" id="section10"><span></span>Mammalian Dose Based EECs (mg/kg-bw)</H4>
                <div class="out_ container_output">
        """
        #table 9_qaqc
        EEC_dose_mamm_SG_sm=trex2_obj.EEC_dose_mamm_SG_sm
        EEC_dose_mamm_SG_md=trex2_obj.EEC_dose_mamm_SG_md
        EEC_dose_mamm_SG_lg=trex2_obj.EEC_dose_mamm_SG_lg
        EEC_dose_mamm_TG_sm=trex2_obj.EEC_dose_mamm_TG_sm
        EEC_dose_mamm_TG_md=trex2_obj.EEC_dose_mamm_TG_md
        EEC_dose_mamm_TG_lg=trex2_obj.EEC_dose_mamm_TG_lg
        EEC_dose_mamm_BP_sm=trex2_obj.EEC_dose_mamm_BP_sm
        EEC_dose_mamm_BP_md=trex2_obj.EEC_dose_mamm_BP_md
        EEC_dose_mamm_BP_lg=trex2_obj.EEC_dose_mamm_BP_lg
        EEC_dose_mamm_FP_sm=trex2_obj.EEC_dose_mamm_FP_sm
        EEC_dose_mamm_FP_md=trex2_obj.EEC_dose_mamm_FP_md
        EEC_dose_mamm_FP_lg=trex2_obj.EEC_dose_mamm_FP_lg
        EEC_dose_mamm_AR_sm=trex2_obj.EEC_dose_mamm_AR_sm
        EEC_dose_mamm_AR_md=trex2_obj.EEC_dose_mamm_AR_md
        EEC_dose_mamm_AR_lg=trex2_obj.EEC_dose_mamm_AR_lg
        EEC_dose_mamm_SE_sm=trex2_obj.EEC_dose_mamm_SE_sm
        EEC_dose_mamm_SE_md=trex2_obj.EEC_dose_mamm_SE_md
        EEC_dose_mamm_SE_lg=trex2_obj.EEC_dose_mamm_SE_lg

        EEC_dose_mamm_SG_sm_exp=trex2_obj.EEC_dose_mamm_SG_sm_BL_out_exp
        EEC_dose_mamm_SG_md_exp=trex2_obj.EEC_dose_mamm_SG_md_BL_out_exp
        EEC_dose_mamm_SG_lg_exp=trex2_obj.EEC_dose_mamm_SG_lg_BL_out_exp
        EEC_dose_mamm_TG_sm_exp=trex2_obj.EEC_dose_mamm_TG_sm_BL_out_exp
        EEC_dose_mamm_TG_md_exp=trex2_obj.EEC_dose_mamm_TG_md_BL_out_exp
        EEC_dose_mamm_TG_lg_exp=trex2_obj.EEC_dose_mamm_TG_lg_BL_out_exp
        EEC_dose_mamm_BP_sm_exp=trex2_obj.EEC_dose_mamm_BP_sm_BL_out_exp
        EEC_dose_mamm_BP_md_exp=trex2_obj.EEC_dose_mamm_BP_md_BL_out_exp
        EEC_dose_mamm_BP_lg_exp=trex2_obj.EEC_dose_mamm_BP_lg_BL_out_exp
        EEC_dose_mamm_FP_sm_exp=trex2_obj.EEC_dose_mamm_FP_sm_BL_out_exp
        EEC_dose_mamm_FP_md_exp=trex2_obj.EEC_dose_mamm_FP_md_BL_out_exp
        EEC_dose_mamm_FP_lg_exp=trex2_obj.EEC_dose_mamm_FP_lg_BL_out_exp
        EEC_dose_mamm_AR_sm_exp=trex2_obj.EEC_dose_mamm_AR_sm_BL_out_exp
        EEC_dose_mamm_AR_md_exp=trex2_obj.EEC_dose_mamm_AR_md_BL_out_exp
        EEC_dose_mamm_AR_lg_exp=trex2_obj.EEC_dose_mamm_AR_lg_BL_out_exp
        EEC_dose_mamm_SE_sm_exp=trex2_obj.EEC_dose_mamm_SE_sm_BL_out_exp
        EEC_dose_mamm_SE_md_exp=trex2_obj.EEC_dose_mamm_SE_md_BL_out_exp
        EEC_dose_mamm_SE_lg_exp=trex2_obj.EEC_dose_mamm_SE_lg_BL_out_exp

        t9data_qaqc = gett9data_qaqc(EEC_dose_mamm_SG_sm,EEC_dose_mamm_SG_md,EEC_dose_mamm_SG_lg,EEC_dose_mamm_TG_sm,EEC_dose_mamm_TG_md,EEC_dose_mamm_TG_lg,EEC_dose_mamm_BP_sm,EEC_dose_mamm_BP_md,EEC_dose_mamm_BP_lg,EEC_dose_mamm_FP_sm,EEC_dose_mamm_FP_md,EEC_dose_mamm_FP_lg,EEC_dose_mamm_AR_sm,EEC_dose_mamm_AR_md,EEC_dose_mamm_AR_lg,EEC_dose_mamm_SE_sm,EEC_dose_mamm_SE_md,EEC_dose_mamm_SE_lg,
                                     EEC_dose_mamm_SG_sm_exp, EEC_dose_mamm_SG_md_exp, EEC_dose_mamm_SG_lg_exp, EEC_dose_mamm_TG_sm_exp, EEC_dose_mamm_TG_md_exp, EEC_dose_mamm_TG_lg_exp, EEC_dose_mamm_BP_sm_exp, EEC_dose_mamm_BP_md_exp, EEC_dose_mamm_BP_lg_exp, EEC_dose_mamm_FP_sm_exp, EEC_dose_mamm_FP_md_exp, EEC_dose_mamm_FP_lg_exp, EEC_dose_mamm_AR_sm_exp, EEC_dose_mamm_AR_md_exp, EEC_dose_mamm_AR_lg_exp, EEC_dose_mamm_SE_sm_exp, EEC_dose_mamm_SE_md_exp, EEC_dose_mamm_SE_lg_exp)
        t9rows_qaqc = gethtmlrowsfromcols(t9data_qaqc, pv7headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t9rows_qaqc, headings=pv7headings_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_10_qaqc(trex2_obj):
        #pre-table 10_qaqc
        html = """
            <H4 class="out_ collapsible" id="section11"><span></span>Mammalian Dose Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 10_qaqc
        ARQ_dose_mamm_SG_sm=trex2_obj.ARQ_dose_mamm_SG_sm
        CRQ_dose_mamm_SG_sm=trex2_obj.CRQ_dose_mamm_SG_sm
        ARQ_dose_mamm_SG_md=trex2_obj.ARQ_dose_mamm_SG_md
        CRQ_dose_mamm_SG_md=trex2_obj.CRQ_dose_mamm_SG_md
        ARQ_dose_mamm_SG_lg=trex2_obj.ARQ_dose_mamm_SG_lg
        CRQ_dose_mamm_SG_lg=trex2_obj.CRQ_dose_mamm_SG_lg
        
        ARQ_dose_mamm_TG_sm=trex2_obj.ARQ_dose_mamm_TG_sm
        CRQ_dose_mamm_TG_sm=trex2_obj.CRQ_dose_mamm_TG_sm
        ARQ_dose_mamm_TG_md=trex2_obj.ARQ_dose_mamm_TG_md
        CRQ_dose_mamm_TG_md=trex2_obj.CRQ_dose_mamm_TG_md
        ARQ_dose_mamm_TG_lg=trex2_obj.ARQ_dose_mamm_TG_lg
        CRQ_dose_mamm_TG_lg=trex2_obj.CRQ_dose_mamm_TG_lg
        
        ARQ_dose_mamm_BP_sm=trex2_obj.ARQ_dose_mamm_BP_sm
        CRQ_dose_mamm_BP_sm=trex2_obj.CRQ_dose_mamm_BP_sm
        ARQ_dose_mamm_BP_md=trex2_obj.ARQ_dose_mamm_BP_md
        CRQ_dose_mamm_BP_md=trex2_obj.CRQ_dose_mamm_BP_md
        ARQ_dose_mamm_BP_lg=trex2_obj.ARQ_dose_mamm_BP_lg
        CRQ_dose_mamm_BP_lg=trex2_obj.CRQ_dose_mamm_BP_lg
        
        ARQ_dose_mamm_FP_sm=trex2_obj.ARQ_dose_mamm_FP_sm
        CRQ_dose_mamm_FP_sm=trex2_obj.CRQ_dose_mamm_FP_sm
        ARQ_dose_mamm_FP_md=trex2_obj.ARQ_dose_mamm_FP_md
        CRQ_dose_mamm_FP_md=trex2_obj.CRQ_dose_mamm_FP_md
        ARQ_dose_mamm_FP_lg=trex2_obj.ARQ_dose_mamm_FP_lg
        CRQ_dose_mamm_FP_lg=trex2_obj.CRQ_dose_mamm_FP_lg
        
        ARQ_dose_mamm_AR_sm=trex2_obj.ARQ_dose_mamm_AR_sm
        CRQ_dose_mamm_AR_sm=trex2_obj.CRQ_dose_mamm_AR_sm
        ARQ_dose_mamm_AR_md=trex2_obj.ARQ_dose_mamm_AR_md
        CRQ_dose_mamm_AR_md=trex2_obj.CRQ_dose_mamm_AR_md
        ARQ_dose_mamm_AR_lg=trex2_obj.ARQ_dose_mamm_AR_lg
        CRQ_dose_mamm_AR_lg=trex2_obj.CRQ_dose_mamm_AR_lg
        
        ARQ_dose_mamm_SE_sm=trex2_obj.ARQ_dose_mamm_SE_sm
        CRQ_dose_mamm_SE_sm=trex2_obj.CRQ_dose_mamm_SE_sm
        ARQ_dose_mamm_SE_md=trex2_obj.ARQ_dose_mamm_SE_md
        CRQ_dose_mamm_SE_md=trex2_obj.CRQ_dose_mamm_SE_md
        ARQ_dose_mamm_SE_lg=trex2_obj.ARQ_dose_mamm_SE_lg
        CRQ_dose_mamm_SE_lg=trex2_obj.CRQ_dose_mamm_SE_lg

#########
        ARQ_dose_mamm_SG_sm_exp=trex2_obj.ARQ_dose_mamm_SG_sm_BL_out_exp
        CRQ_dose_mamm_SG_sm_exp=trex2_obj.CRQ_dose_mamm_SG_sm_BL_out_exp
        ARQ_dose_mamm_SG_md_exp=trex2_obj.ARQ_dose_mamm_SG_md_BL_out_exp
        CRQ_dose_mamm_SG_md_exp=trex2_obj.CRQ_dose_mamm_SG_md_BL_out_exp
        ARQ_dose_mamm_SG_lg_exp=trex2_obj.ARQ_dose_mamm_SG_lg_BL_out_exp
        CRQ_dose_mamm_SG_lg_exp=trex2_obj.CRQ_dose_mamm_SG_lg_BL_out_exp
        
        ARQ_dose_mamm_TG_sm_exp=trex2_obj.ARQ_dose_mamm_TG_sm_BL_out_exp
        CRQ_dose_mamm_TG_sm_exp=trex2_obj.CRQ_dose_mamm_TG_sm_BL_out_exp
        ARQ_dose_mamm_TG_md_exp=trex2_obj.ARQ_dose_mamm_TG_md_BL_out_exp
        CRQ_dose_mamm_TG_md_exp=trex2_obj.CRQ_dose_mamm_TG_md_BL_out_exp
        ARQ_dose_mamm_TG_lg_exp=trex2_obj.ARQ_dose_mamm_TG_lg_BL_out_exp
        CRQ_dose_mamm_TG_lg_exp=trex2_obj.CRQ_dose_mamm_TG_lg_BL_out_exp
        
        ARQ_dose_mamm_BP_sm_exp=trex2_obj.ARQ_dose_mamm_BP_sm_BL_out_exp
        CRQ_dose_mamm_BP_sm_exp=trex2_obj.CRQ_dose_mamm_BP_sm_BL_out_exp
        ARQ_dose_mamm_BP_md_exp=trex2_obj.ARQ_dose_mamm_BP_md_BL_out_exp
        CRQ_dose_mamm_BP_md_exp=trex2_obj.CRQ_dose_mamm_BP_md_BL_out_exp
        ARQ_dose_mamm_BP_lg_exp=trex2_obj.ARQ_dose_mamm_BP_lg_BL_out_exp
        CRQ_dose_mamm_BP_lg_exp=trex2_obj.CRQ_dose_mamm_BP_lg_BL_out_exp
        
        ARQ_dose_mamm_FP_sm_exp=trex2_obj.ARQ_dose_mamm_FP_sm_BL_out_exp
        CRQ_dose_mamm_FP_sm_exp=trex2_obj.CRQ_dose_mamm_FP_sm_BL_out_exp
        ARQ_dose_mamm_FP_md_exp=trex2_obj.ARQ_dose_mamm_FP_md_BL_out_exp
        CRQ_dose_mamm_FP_md_exp=trex2_obj.CRQ_dose_mamm_FP_md_BL_out_exp
        ARQ_dose_mamm_FP_lg_exp=trex2_obj.ARQ_dose_mamm_FP_lg_BL_out_exp
        CRQ_dose_mamm_FP_lg_exp=trex2_obj.CRQ_dose_mamm_FP_lg_BL_out_exp
        
        ARQ_dose_mamm_AR_sm_exp=trex2_obj.ARQ_dose_mamm_AR_sm_BL_out_exp
        CRQ_dose_mamm_AR_sm_exp=trex2_obj.CRQ_dose_mamm_AR_sm_BL_out_exp
        ARQ_dose_mamm_AR_md_exp=trex2_obj.ARQ_dose_mamm_AR_md_BL_out_exp
        CRQ_dose_mamm_AR_md_exp=trex2_obj.CRQ_dose_mamm_AR_md_BL_out_exp
        ARQ_dose_mamm_AR_lg_exp=trex2_obj.ARQ_dose_mamm_AR_lg_BL_out_exp
        CRQ_dose_mamm_AR_lg_exp=trex2_obj.CRQ_dose_mamm_AR_lg_BL_out_exp
        
        ARQ_dose_mamm_SE_sm_exp=trex2_obj.ARQ_dose_mamm_SE_sm_BL_out_exp
        CRQ_dose_mamm_SE_sm_exp=trex2_obj.CRQ_dose_mamm_SE_sm_BL_out_exp
        ARQ_dose_mamm_SE_md_exp=trex2_obj.ARQ_dose_mamm_SE_md_BL_out_exp
        CRQ_dose_mamm_SE_md_exp=trex2_obj.CRQ_dose_mamm_SE_md_BL_out_exp
        ARQ_dose_mamm_SE_lg_exp=trex2_obj.ARQ_dose_mamm_SE_lg_BL_out_exp
        CRQ_dose_mamm_SE_lg_exp=trex2_obj.CRQ_dose_mamm_SE_lg_BL_out_exp

        t10data_qaqc = gett10data_qaqc(ARQ_dose_mamm_SG_sm,CRQ_dose_mamm_SG_sm,ARQ_dose_mamm_SG_md,CRQ_dose_mamm_SG_md,ARQ_dose_mamm_SG_lg,CRQ_dose_mamm_SG_lg,ARQ_dose_mamm_TG_sm,CRQ_dose_mamm_TG_sm,ARQ_dose_mamm_TG_md,CRQ_dose_mamm_TG_md,ARQ_dose_mamm_TG_lg,CRQ_dose_mamm_TG_lg,ARQ_dose_mamm_BP_sm,CRQ_dose_mamm_BP_sm,ARQ_dose_mamm_BP_md,CRQ_dose_mamm_BP_md,ARQ_dose_mamm_BP_lg,CRQ_dose_mamm_BP_lg,ARQ_dose_mamm_FP_sm,CRQ_dose_mamm_FP_sm,ARQ_dose_mamm_FP_md,CRQ_dose_mamm_FP_md,ARQ_dose_mamm_FP_lg,CRQ_dose_mamm_FP_lg,ARQ_dose_mamm_AR_sm,CRQ_dose_mamm_AR_sm,ARQ_dose_mamm_AR_md,CRQ_dose_mamm_AR_md,ARQ_dose_mamm_AR_lg,CRQ_dose_mamm_AR_lg,ARQ_dose_mamm_SE_sm,CRQ_dose_mamm_SE_sm,ARQ_dose_mamm_SE_md,CRQ_dose_mamm_SE_md,ARQ_dose_mamm_SE_lg,CRQ_dose_mamm_SE_lg,
                                       ARQ_dose_mamm_SG_sm_exp, CRQ_dose_mamm_SG_sm_exp, ARQ_dose_mamm_SG_md_exp, CRQ_dose_mamm_SG_md_exp, ARQ_dose_mamm_SG_lg_exp, CRQ_dose_mamm_SG_lg_exp, ARQ_dose_mamm_TG_sm_exp, CRQ_dose_mamm_TG_sm_exp, ARQ_dose_mamm_TG_md_exp, CRQ_dose_mamm_TG_md_exp, ARQ_dose_mamm_TG_lg_exp, CRQ_dose_mamm_TG_lg_exp, ARQ_dose_mamm_BP_sm_exp, CRQ_dose_mamm_BP_sm_exp, ARQ_dose_mamm_BP_md_exp, CRQ_dose_mamm_BP_md_exp, ARQ_dose_mamm_BP_lg_exp, CRQ_dose_mamm_BP_lg_exp, ARQ_dose_mamm_FP_sm_exp, CRQ_dose_mamm_FP_sm_exp, ARQ_dose_mamm_FP_md_exp, CRQ_dose_mamm_FP_md_exp, ARQ_dose_mamm_FP_lg_exp, CRQ_dose_mamm_FP_lg_exp, ARQ_dose_mamm_AR_sm_exp, CRQ_dose_mamm_AR_sm_exp, ARQ_dose_mamm_AR_md_exp, CRQ_dose_mamm_AR_md_exp, ARQ_dose_mamm_AR_lg_exp, CRQ_dose_mamm_AR_lg_exp, ARQ_dose_mamm_SE_sm_exp, CRQ_dose_mamm_SE_sm_exp, ARQ_dose_mamm_SE_md_exp, CRQ_dose_mamm_SE_md_exp, ARQ_dose_mamm_SE_lg_exp, CRQ_dose_mamm_SE_lg_exp)
        t10rows_qaqc = gethtmlrowsfromcols(t10data_qaqc, pv10headings_qaqc)       
        html = html + tmpl_10_qaqc.render(Context(dict(data=t10rows_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_11_qaqc(trex2_obj):
        #pre-table 11_qaqc
        html = """
            <H4 class="out_ collapsible" id="section12"><span></span>Mammalian Dietary Based RQs</H4>
                <div class="out_ container_output">
        """
        #table 11_qaqc
        ARQ_diet_mamm_SG=trex2_obj.ARQ_diet_mamm_SG
        CRQ_diet_mamm_SG=trex2_obj.CRQ_diet_mamm_SG
        ARQ_diet_mamm_TG=trex2_obj.ARQ_diet_mamm_TG
        CRQ_diet_mamm_TG=trex2_obj.CRQ_diet_mamm_TG
        ARQ_diet_mamm_BP=trex2_obj.ARQ_diet_mamm_BP
        CRQ_diet_mamm_BP=trex2_obj.CRQ_diet_mamm_BP
        ARQ_diet_mamm_FP=trex2_obj.ARQ_diet_mamm_FP
        CRQ_diet_mamm_FP=trex2_obj.CRQ_diet_mamm_FP
        ARQ_diet_mamm_AR=trex2_obj.ARQ_diet_mamm_AR
        CRQ_diet_mamm_AR=trex2_obj.CRQ_diet_mamm_AR

        ARQ_diet_mamm_SG_exp=trex2_obj.ARQ_diet_mamm_SG_BL_out_exp
        CRQ_diet_mamm_SG_exp=trex2_obj.CRQ_diet_mamm_SG_BL_out_exp
        ARQ_diet_mamm_TG_exp=trex2_obj.ARQ_diet_mamm_TG_BL_out_exp
        CRQ_diet_mamm_TG_exp=trex2_obj.CRQ_diet_mamm_TG_BL_out_exp
        ARQ_diet_mamm_BP_exp=trex2_obj.ARQ_diet_mamm_BP_BL_out_exp
        CRQ_diet_mamm_BP_exp=trex2_obj.CRQ_diet_mamm_BP_BL_out_exp
        ARQ_diet_mamm_FP_exp=trex2_obj.ARQ_diet_mamm_FP_BL_out_exp
        CRQ_diet_mamm_FP_exp=trex2_obj.CRQ_diet_mamm_FP_BL_out_exp
        ARQ_diet_mamm_AR_exp=trex2_obj.ARQ_diet_mamm_AR_BL_out_exp
        CRQ_diet_mamm_AR_exp=trex2_obj.CRQ_diet_mamm_AR_BL_out_exp

        t11data_qaqc = gett11data_na_qaqc(ARQ_diet_mamm_SG,CRQ_diet_mamm_SG,ARQ_diet_mamm_TG,CRQ_diet_mamm_TG,ARQ_diet_mamm_BP,CRQ_diet_mamm_BP,ARQ_diet_mamm_FP,CRQ_diet_mamm_FP,ARQ_diet_mamm_AR,CRQ_diet_mamm_AR,
                                          ARQ_diet_mamm_SG_exp,CRQ_diet_mamm_SG_exp,ARQ_diet_mamm_TG_exp,CRQ_diet_mamm_TG_exp,ARQ_diet_mamm_BP_exp,CRQ_diet_mamm_BP_exp,ARQ_diet_mamm_FP_exp,CRQ_diet_mamm_FP_exp,ARQ_diet_mamm_AR_exp,CRQ_diet_mamm_AR_exp)
        t11rows_qaqc = gethtmlrowsfromcols(t11data_qaqc, pv8headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t11rows_qaqc, headings=pv8headings_qaqc)))
        html = html + """
                </div>
        """
        return html

def table_15_qaqc(trex2_obj):
        #pre-table 15_qaqc
        html = """
            <H4 class="out_ collapsible" id="section13"><span></span>LD<sub>50</sub> ft<sup>-2</sup></H4>
                <div class="out_ container_output">
        """
        #table 15_qaqc
        LD50_bl_bird_sm=trex2_obj.LD50_bl_bird_sm
        LD50_bl_mamm_sm=trex2_obj.LD50_bl_mamm_sm
        LD50_bl_bird_md=trex2_obj.LD50_bl_bird_md
        LD50_bl_mamm_md=trex2_obj.LD50_bl_mamm_md
        LD50_bl_bird_lg=trex2_obj.LD50_bl_bird_lg
        LD50_bl_mamm_lg=trex2_obj.LD50_bl_mamm_lg

        LD50_bl_bird_sm_exp=trex2_obj.LD50_bl_bird_sm
        LD50_bl_mamm_sm_exp=trex2_obj.LD50_bl_mamm_sm
        LD50_bl_bird_md_exp=trex2_obj.LD50_bl_bird_md
        LD50_bl_mamm_md_exp=trex2_obj.LD50_bl_mamm_md
        LD50_bl_bird_lg_exp=trex2_obj.LD50_bl_bird_lg
        LD50_bl_mamm_lg_exp=trex2_obj.LD50_bl_mamm_lg

        t15data_qaqc = gett12data_qaqc(LD50_bl_bird_sm,LD50_bl_mamm_sm,LD50_bl_bird_md,LD50_bl_mamm_md,LD50_bl_bird_lg,LD50_bl_mamm_lg,
                                       LD50_bl_bird_sm_exp,LD50_bl_mamm_sm_exp,LD50_bl_bird_md_exp,LD50_bl_mamm_md_exp,LD50_bl_bird_lg_exp,LD50_bl_mamm_lg_exp)
        t15rows_qaqc = gethtmlrowsfromcols(t15data_qaqc, pv12headings_qaqc)       
        html = html + tmpl.render(Context(dict(data=t15rows_qaqc, headings=pv12headings_qaqc)))
        html = html + """
                </div>
        </div>
        """
        return html
