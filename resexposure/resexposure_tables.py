import numpy
import time, datetime
from django.template import Context, Template
from django.utils.safestring import mark_safe
from resexposure import resexposure_model
from resexposure import resexposure_parameters
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
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
        <td>{{ val|default:''|safe }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template



pvuheadings = getheaderpvu()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Residential Exposure Model<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html


def table_all(model, all_obj):
    html = timestamp()
    if 'tab_hdflr' in model:
        table_hdflr = table_1(all_obj['tab_hdflr'])
        html = html + table_hdflr
    if 'tab_vlflr' in model:
        table_vlflr = table_2(all_obj['tab_vlflr'])
        html = html + table_vlflr
    if 'tab_cpcln' in model:
        table_cpcln = table_3(all_obj['tab_cpcln'])
        html = html + table_cpcln
    if 'tab_ipcap' in model:
        table_ipcap = table_4(all_obj['tab_ipcap'])
        html = html + table_ipcap
    if 'tab_mactk' in model:
        table_mactk = table_5(all_obj['tab_mactk'])
        html = html + table_mactk
    if 'tab_ccpst' in model:
        table_ccpst = table_6(all_obj['tab_ccpst'])
        html = html + table_ccpst
    if 'tab_ldtpr' in model:
        table_ldtpr = table_7(all_obj['tab_ldtpr'])
        html = html + table_ldtpr
    if 'tab_clopr' in model:
        table_clopr = table_8(all_obj['tab_clopr'])
        html = html + table_clopr
    if 'tab_impdp' in model:
        table_impdp = table_9(all_obj['tab_impdp'])
        html = html + table_impdp
    if 'tab_cldst' in model:
        table_cldst = table_10(all_obj['tab_cldst'])
        html = html + table_cldst
    if 'tab_impty' in model:
        table_impty = table_11(all_obj['tab_impty'])
        html = html + table_impty
    return html

######Hard Surface Floor Cleaner#####
def gett1data_in(re_obj):
    data = { 
        "Parameter": ['Application rate of cleaning solution', 'Percent a.i. in cleaning solution', 'Cleaning solution density',
                      'Conversion factor', 'Conversion factor', 'Fraction of solution remaining on floor',
                      'Transfer factor for hard surfaces', 'Surface area of body in contact with floor', 'Dermal absorption',
                      'Body weight', 'Surface area of hands in contact with floor', 'Frequency of hand to mouth contacts',
                      'Exposure time', 'Saliva extraction factor'],
        "Value": ['%s' % re_obj.ar_hd, '%s' % (100*re_obj.ai_hd), '%s' % re_obj.den_hd,
                  '%s' % re_obj.cf1_hd, '%s' % re_obj.cf2_hd, '%s' % re_obj.fr_hd,
                  '%s' % re_obj.tf_hd, '%s' % re_obj.sa_hd, '%s' % (100*re_obj.da_hd),
                  '%s' % re_obj.bw_hd, '%s' % re_obj.sa_h_hd, '%s' % re_obj.fq_hd,
                  '%s' % re_obj.et_hd, '%s' % (100*re_obj.se_hd), ],
        "Units": ['ft<sup>2</sup>/gallon', '%', 'lb/gallon', 
                  'mg/lb', 'ft<sup>2</sup>/cm<sup>2</sup>', '', 
                  '', 'cm<sup>2</sup>', '%', 
                  'kg', 'cm<sup>2</sup>', 'events/hour', 
                  'hours/day', '%'],
        }
    return data

def gett1data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_hd, '%0.3f' % re_obj.dose_der_hd,
                  '%0.3f' % re_obj.exp_ora_hd, '%0.3f' % re_obj.dose_ora_hd,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Impregnated Hard Surface (i.e. Vinyl Flooring)#####
def gett2data_in(re_obj):
    data = { 
        "Parameter": ['Weight fraction of a.i. in vinyl', 'Vinyl density', 'Vinyl thickness',
                      'Conversion factor', 'Availability factor', 'Transfer factor from vinyl to skin',
                      'Conversion factor', 'Body weight', 'Body surface contacting vinyl',
                      'Dermal absorption', 'Hand to mouth surface area', 'Frequency of hand to mouth contacts',
                      'Exposure time', 'Saliva extraction efficiency'],
        "Value": ['%s' % (100*re_obj.wf_vl), '%s' % re_obj.den_vl, '%s' % re_obj.vt_vl,
                  '%s' % re_obj.cf1_vl, '%s' % (100*re_obj.af_vl), '%s' % (100*re_obj.tf_vl),
                  '%s' % re_obj.cf2_vl, '%s' % re_obj.bw_vl, '%s' % re_obj.sa_vl,
                  '%s' % (100*re_obj.da_vl), '%s' % re_obj.sa_h_vl, '%s' % re_obj.fq_vl,
                  '%s' % re_obj.et_vl, '%s' % (100*re_obj.se_vl),],
        "Units": ['%', 'g/cm<sup>3</sup>', 'mm',
                  'cm/mm', '%', '%',
                  'mg/g', 'kg', 'cm<sup>2</sup>/day',
                  '%', 'cm<sup>2</sup>', 'events/hour', 
                  'hours/day', '%'],
        }
    return data

def gett2data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_vl, '%0.3f' % re_obj.dose_der_vl,
                  '%0.3f' % re_obj.exp_ora_vl, '%0.3f' % re_obj.dose_ora_vl,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Carpet Cleaner #####
def gett3data_in(re_obj):
    data = { 
        "Parameter": ['Application rate of cleaning solution', 'Percent a.i. in cleaning solution', 'Cleaning solution density',
                      'Conversion factor', 'Conversion factor', 'Fraction of solution remaining on floor',
                      'Transfer factor for carpet', 'Body weight', 'Surface area of body in contact with floor',
                      'Dermal absorption', 'Surface area of hands in contact with floor', 'Frequency of hand to mouth contacts',
                      'Exposure Time', 'Saliva extraction factor'],
        "Value": ['%s' % re_obj.ar_cc, '%s' % (100*re_obj.ai_cc), '%s' % re_obj.den_cc,
                  '%s' % re_obj.cf1_cc, '%s' % re_obj.cf2_cc, '%s' % re_obj.fr_cc,
                  '%s' % re_obj.tf_cc, '%s' % re_obj.bw_cc, '%s' % re_obj.sa_cc,
                  '%s' % (100*re_obj.da_cc), '%s' % re_obj.sa_h_cc, '%s' % re_obj.fq_cc,
                  '%s' % re_obj.et_cc, '%s' % (100*re_obj.se_cc),],
        "Units": ['ft<sup>2</sup>/gallon', '%', 'lb/gallon',
                  'mg/lb', 'ft<sup>2</sup>/cm<sup>2</sup>', '',
                  '', 'kg', 'cm<sup>2</sup>',
                  '%', 'cm<sup>2</sup>', 'events/hour', 
                  'hours/day', '%'],
        }
    return data

def gett3data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_cc, '%0.3f' % re_obj.dose_der_cc,
                  '%0.3f' % re_obj.exp_ora_cc, '%0.3f' % re_obj.dose_ora_cc,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Impregnated Carpet#####
def gett4data_in(re_obj):
    data = { 
        "Parameter": ['Carpet density', 'Weight fraction of a.i. in carpet', 'Transfer factor from carpet to skin',
                      'Body weight', 'Surface area of body in contact with carpet', 'Dermal absorption',
                      'Surface area of hands in contact with floor', 'Frequency of hand to mouth contacts', 'Exposure time',
                      'Saliva extraction factor'],
        "Value": ['%s' % re_obj.den_ic, '%s' % re_obj.wf_ic, '%s' % re_obj.tf_ic,
                  '%s' % re_obj.bw_ic, '%s' % re_obj.sa_ic, '%s' % (100*re_obj.da_ic),
                  '%s' % re_obj.sa_h_ic, '%s' % re_obj.fq_ic, '%s' % re_obj.et_ic,
                  '%s' % (100*re_obj.se_ic),],
        "Units": ['mg/cm<sup>2</sup>', '', '',
                  'kg', 'cm<sup>2</sup>', '%',
                  'cm<sup>2</sup>', 'events/hour', 'hours/day',
                  '%'],
        }
    return data

def gett4data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_ic, '%0.3f' % re_obj.dose_der_ic,
                  '%0.3f' % re_obj.exp_ora_ic, '%0.3f' % re_obj.dose_ora_ic,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Mattress Covers and Ticking#####
def gett5data_in(re_obj):
    data = { 
        "Parameter": ['Weight fraction of a.i. in vinyl', 'Vinyl density', 'Transfer factor from vinyl to skin',
                      'Body weight', 'Protection factor from single layer of clothing/sheet', 'Body surface contacting vinyl',
                      'Dermal absorption',],
        "Value": ['%s' % (100*re_obj.wf_mt), '%s' % re_obj.den_mt, '%s' % (100*re_obj.tf_mt),
                  '%s' % re_obj.bw_mt, '%s' % (100*re_obj.pf_mt), '%s' % re_obj.sa_mt,
                  '%s' % (100*re_obj.da_mt),],
        "Units": ['%', 'g/cm<sup>3</sup>', '%',
                  'kg', '%', 'cm<sup>2</sup>/day',
                  '%'],
        }
    return data

def gett5data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_mt, '%0.3f' % re_obj.dose_der_mt],
        "Units": ['mg/day', 'mg/kg/day'],
        }
    return data

######Clothing/Textile Consumer Product Spray Treatment#####
def gett6data_in(re_obj):
    data = { 
        "Parameter": ['Water absorption rate', 'Weight fraction of a.i. in product', 'Body weight',
                      'Transfer factor from clothing to skin', 'Surface area of body in contact with clothing', 'Dermal absorption',
                      'Surface area of textile mouthed', 'Saliva extraction factor'],
        "Value": ['%s' % re_obj.wa_ct, '%s' % (100*re_obj.wf_ct), '%s' % re_obj.bw_ct,
                  '%s' % (100*re_obj.tf_ct), '%s' % re_obj.sa_ct, '%s' % (100*re_obj.da_ct),
                  '%s' % re_obj.sa_m_ct, '%s' % (100*re_obj.se_ct),],
        "Units": ['mg/cm<sup>2</sup>', '%', 'kg',
                  '%', 'cm<sup>2</sup>', '%',
                  'cm<sup>2</sup>', '%'],
        }
    return data

def gett6data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_ct, '%0.3f' % re_obj.dose_der_ct,
                  '%0.3f' % re_obj.exp_ora_ct, '%0.3f' % re_obj.dose_ora_ct,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Laundry Detergent Preservative#####
def gett7data_in(re_obj):
    data = { 
        "Parameter": ['Amount of undiluted product used', 'Weight fraction of a.i. in product', 'Density of fabric',
                      'Weight fraction of detergent deposited on fabric', 'Total weight of fabric', 'Body weight',
                      'Body surface area contacting clothing', 'Weight fraction transferred from clothing to skin', 'Weight fraction remaining on skin',
                      'Dermal absorption', 'Surface area of textile mouthed', 'Saliva extraction factor'],
        "Value": ['%s' % re_obj.ap_lp, '%s' % (100*re_obj.wf_lp), '%s' % re_obj.den_lp,
                  '%s' % (100*re_obj.wfd_lp), '%s' % re_obj.tw_lp, '%s' % re_obj.bw_lp,
                  '%s' % re_obj.sa_lp, '%s' % (100*re_obj.tf_cs_lp), '%s' % (100*re_obj.tf_r_lp),
                  '%s' % (100*re_obj.da_lp), '%s' % re_obj.sa_m_lp, '%s' % (100*re_obj.se_lp),],
        "Units": ['mg', '%', 'mg/cm<sup>2</sup>',
                  '%', 'mg', 'kg',
                  'cm<sup>2</sup>', '%', '%',
                  '%', 'cm<sup>2</sup>', '%'],
        }
    return data

def gett7data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_lp, '%0.3f' % re_obj.dose_der_lp,
                  '%0.3f' % re_obj.exp_ora_lp, '%0.3f' % re_obj.dose_ora_lp,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Clothing/Textile Material Preservative#####
def gett8data_in(re_obj):
    data = { 
        "Parameter": ['Fabric density', 'Weight fraction of a.i. in product', 'Body weight',
                      'Transfer factor from clothing to skin', 'Surface area of body in contact with clothing', 'Dermal absorption',
                      'Surface area of textile mouthed', 'Saliva extraction factor'],
        "Value": ['%s' % re_obj.den_cp, '%s' % (100*re_obj.wf_cp), '%s' % re_obj.bw_cp,
                  '%s' % (100*re_obj.tf_cs_cp), '%s' % re_obj.sa_cp, '%s' % (100*re_obj.da_cp),
                  '%s' % re_obj.sa_m_cp, '%s' % (100*re_obj.se_cp), ],
        "Units": ['mg/cm<sup>2</sup>', '%', 'kg',
                  '%', 'cm<sup>2</sup>', '%',
                  'cm<sup>2</sup>', '%'],
        }
    return data

def gett8data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose', 
                      'Daily Incidental Oral Exposure', 'Daily Incidental Oral Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_cp, '%0.3f' % re_obj.dose_der_cp,
                  '%0.3f' % re_obj.exp_ora_cp, '%0.3f' % re_obj.dose_ora_cp,],
        "Units": ['mg/day', 'mg/kg/day', 'mg/day', 'mg/kg/day'],
        }
    return data

######Impregnated Diapers#####
def gett9data_in(re_obj):
    data = { 
        "Parameter": ['Amount of treated material within diaper', 'Weight fraction of a.i. in product', 'Transferable residue from diaper to skin',
                      'Exposure frequency', 'Dermal absorption', 'Body weight'],
        "Value": ['%s' % re_obj.am_id, '%s' % (100*re_obj.wf_id), '%s' % (100*re_obj.tf_id),
                  '%s' % re_obj.fq_id, '%s' % (100*re_obj.da_id), '%s' % re_obj.bw_id],
        "Units": ['g', '%', '%',
                  'diapers/day', '%', 'kg'],
        }
    return data

def gett9data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_id, '%0.3f' % re_obj.dose_der_id],
        "Units": ['mg/day', 'mg/kg/day'],
        }
    return data

######Cloth Diaper Spray Treatment#####
def gett10data_in(re_obj):
    data = { 
        "Parameter": ['Product absorption rate', 'Weight fraction of a.i. in product', 'Transferable residue from diaper to skin',
                      'Surface area of body in contact with diaper', 'Exposure frequency', 'Dermal absorption',
                      'Body weight'],
        "Value": ['%s' % re_obj.ar_sd, '%s' % (100*re_obj.wf_sd), '%s' % (100*re_obj.tf_sd),
                  '%s' % re_obj.sa_sd, '%s' % re_obj.fq_sd, '%s' % (100*re_obj.da_sd),
                  '%s' % re_obj.bw_sd],
        "Units": ['mg/cm<sup>2</sup>', '%', '%',
                  'cm<sup>2</sup>', 'diapers/day', '%',
                  'kg'],
        }
    return data

def gett10data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_sd, '%0.3f' % re_obj.dose_der_sd],
        "Units": ['mg/day', 'mg/kg/day'],
        }
    return data

######Impregnated Polymer#####
def gett11data_in(re_obj):
    data = { 
        "Parameter": ['Weight fraction of a.i. in product', 'Weight of 500cm<sup>2</sup> toy', 'Fraction available at toy surface',
                      'Surface area of toy', 'Surface area of mouthed', 'Saliva extraction factor',
                      'Body weight'],
        "Value": ['%s' % (100*re_obj.wf_ip), '%s' % re_obj.wt_ip, '%s' % (100*re_obj.fr_sa_ip),
                  '%s' % re_obj.sa_ip, '%s' % re_obj.sa_m_ip, '%s' % (100*re_obj.se_ip),
                  '%s' % re_obj.bw_ip],
        "Units": ['%', 'g', '%',
                  'cm<sup>2</sup>', 'cm<sup>2</sup>', '%',
                  'kg'],
        }
    return data

def gett11data_out(re_obj):
    data = { 
        "Parameter": ['Daily Dermal Systemic Exposure', 'Daily Dermal Systemic Dose'],
        "Value": ['%0.3f' % re_obj.exp_der_ip, '%0.3f' % re_obj.dose_der_ip],
        "Units": ['mg/day', 'mg/kg/day'],
        }
    return data

def table_1(re_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Hard Surface Floor Cleaner:</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section1"><span></span>Inputs</H4>
            <div class="out_1 container_output">
        """
        #table 1 input
        t1data_in = gett1data_in(re_obj)
        t1rows_in = gethtmlrowsfromcols(t1data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_1 collapsible" id="section2"><span></span>Output</H4>
            <div class="out_1 container_output">
        """
        #table 1 output
        t1data_out = gett1data_out(re_obj)
        t1rows_out = gethtmlrowsfromcols(t1data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_2(re_obj):
        #pre-table 2
        html = """
        <H3 class="out_2 collapsible" id="section2"><span></span>Impregnated Hard Surface (i.e. Vinyl Flooring):</H3>
        <div class="out_2">
            <H4 class="out_2 collapsible" id="section2"><span></span>Inputs</H4>
            <div class="out_2 container_output">
        """
        #table 2 input
        t2data_in = gett2data_in(re_obj)
        t2rows_in = gethtmlrowsfromcols(t2data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_2 collapsible" id="section2"><span></span>Output</H4>
            <div class="out_2 container_output">
        """
        #table 2 output
        t2data_out = gett2data_out(re_obj)
        t2rows_out = gethtmlrowsfromcols(t2data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_3(re_obj):
        #pre-table 3
        html = """
        <H3 class="out_3 collapsible" id="section3"><span></span>Carpet Cleaner:</H3>
        <div class="out_3">
            <H4 class="out_3 collapsible" id="section3"><span></span>Inputs</H4>
            <div class="out_3 container_output">
        """
        #table 3 input
        t3data_in = gett3data_in(re_obj)
        t3rows_in = gethtmlrowsfromcols(t3data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_3 collapsible" id="section3"><span></span>Output</H4>
            <div class="out_3 container_output">
        """
        #table 3 output
        t3data_out = gett3data_out(re_obj)
        t3rows_out = gethtmlrowsfromcols(t3data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_4(re_obj):
        #pre-table 4
        html = """
        <H3 class="out_4 collapsible" id="section4"><span></span>Mattress Covers and Ticking:</H4>
        <div class="out_4">
            <H4 class="out_4 collapsible" id="section4"><span></span>Inputs</H4>
            <div class="out_4 container_output">
        """
        #table 4 input
        t4data_in = gett4data_in(re_obj)
        t4rows_in = gethtmlrowsfromcols(t4data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_4 collapsible" id="section4"><span></span>Output</H4>
            <div class="out_4 container_output">
        """
        #table 4 output
        t4data_out = gett4data_out(re_obj)
        t4rows_out = gethtmlrowsfromcols(t4data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_5(re_obj):
        #pre-table 5
        html = """
        <H3 class="out_5 collapsible" id="section5"><span></span>Impregnated Carpet:</H4>
        <div class="out_5">
            <H4 class="out_5 collapsible" id="section5"><span></span>Inputs</H4>
            <div class="out_5 container_output">
        """
        #table 5 input
        t5data_in = gett5data_in(re_obj)
        t5rows_in = gethtmlrowsfromcols(t5data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_5 collapsible" id="section5"><span></span>Output</H5>
            <div class="out_5 container_output">
        """
        #table 5 output
        t5data_out = gett5data_out(re_obj)
        t5rows_out = gethtmlrowsfromcols(t5data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t5rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_6(re_obj):
        #pre-table 6
        html = """
        <H3 class="out_6 collapsible" id="section6"><span></span>Clothing/Textile Consumer Product Spray Treatment:</H4>
        <div class="out_6">
            <H4 class="out_6 collapsible" id="section6"><span></span>Inputs</H4>
            <div class="out_6 container_output">
        """
        #table 6 input
        t6data_in = gett6data_in(re_obj)
        t6rows_in = gethtmlrowsfromcols(t6data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t6rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_6 collapsible" id="section6"><span></span>Output</H6>
            <div class="out_6 container_output">
        """
        #table 6 output
        t6data_out = gett6data_out(re_obj)
        t6rows_out = gethtmlrowsfromcols(t6data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t6rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_7(re_obj):
        #pre-table 7
        html = """
        <H3 class="out_7 collapsible" id="section7"><span></span>Laundry Detergent Preservative:</H4>
        <div class="out_7">
            <H4 class="out_7 collapsible" id="section7"><span></span>Inputs</H4>
            <div class="out_7 container_output">
        """
        #table 7 input
        t7data_in = gett7data_in(re_obj)
        t7rows_in = gethtmlrowsfromcols(t7data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t7rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_7 collapsible" id="section7"><span></span>Output</H4>
            <div class="out_7 container_output">
        """
        #table 7 output
        t7data_out = gett7data_out(re_obj)
        t7rows_out = gethtmlrowsfromcols(t7data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t7rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_8(re_obj):
        #pre-table 8
        html = """
        <H3 class="out_8 collapsible" id="section8"><span></span>Clothing/Textile Material Preservative:</H4>
        <div class="out_8">
            <H4 class="out_8 collapsible" id="section8"><span></span>Inputs</H4>
            <div class="out_8 container_output">
        """
        #table 8 input
        t8data_in = gett8data_in(re_obj)
        t8rows_in = gethtmlrowsfromcols(t8data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t8rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_8 collapsible" id="section8"><span></span>Output</H4>
            <div class="out_8 container_output">
        """
        #table 8 output
        t8data_out = gett8data_out(re_obj)
        t8rows_out = gethtmlrowsfromcols(t8data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t8rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_9(re_obj):
        #pre-table 9
        html = """
        <H3 class="out_9 collapsible" id="section9"><span></span>Impregnated Diapers:</H4>
        <div class="out_9">
            <H4 class="out_9 collapsible" id="section9"><span></span>Inputs</H4>
            <div class="out_9 container_output">
        """
        #table 9 input
        t9data_in = gett9data_in(re_obj)
        t9rows_in = gethtmlrowsfromcols(t9data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t9rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_9 collapsible" id="section9"><span></span>Output</H4>
            <div class="out_9 container_output">
        """
        #table 9 output
        t9data_out = gett9data_out(re_obj)
        t9rows_out = gethtmlrowsfromcols(t9data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t9rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_10(re_obj):
        #pre-table 10
        html = """
        <H3 class="out_10 collapsible" id="section10"><span></span>Cloth Diaper Spray Treatment:</H4>
        <div class="out_10">
            <H4 class="out_10 collapsible" id="section10"><span></span>Inputs</H4>
            <div class="out_10 container_output">
        """
        #table 10 input
        t10data_in = gett10data_in(re_obj)
        t10rows_in = gethtmlrowsfromcols(t10data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t10rows_in, headings=pvuheadings)))
        html = html + """
              </div>
        """
        html = html + """
            <H4 class="out_10 collapsible" id="section10"><span></span>Output</H4>
            <div class="out_10 container_output">
        """
        #table 10 output
        t10data_out = gett10data_out(re_obj)
        t10rows_out = gethtmlrowsfromcols(t10data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t10rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_11(re_obj):
        #pre-table 11
        html = """
        <H3 class="out_11 collapsible" id="section11"><span></span>Impregnated Polymer (i.e toys):</H4>
        <div class="out_11">
            <H4 class="out_11 collapsible" id="section11"><span></span>Inputs</H4>
            <div class="out_11 container_output">
        """
        #table 11 input
        t11data_in = gett11data_in(re_obj)
        t11rows_in = gethtmlrowsfromcols(t11data_in, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t11rows_in, headings=pvuheadings)))
        html = html + """
            </div>
        """
        html = html + """
            <H4 class="out_11 collapsible" id="section11"><span></span>Output</H4>
            <div class="out_11 container_output">
        """
        #table 11 output
        t11data_out = gett11data_out(re_obj)
        t11rows_out = gethtmlrowsfromcols(t11data_out, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t11rows_out, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html
