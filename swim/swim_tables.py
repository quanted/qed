import numpy
import time, datetime
from django.template import Context, Template
from django.utils.safestring import mark_safe
from swim import swim_model
from swim import swim_parameters
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpv5():
    headings_l = ["Age group",],
    headings = ["Age group", "Inh_c", "Inh_nc", "Ing_c", "Ing_nc", "Der_c", "Der_nc"]
    return headings_l, headings


def getheadersum1():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Units"]
    return headings

def getheadersum5():
    headings_l = ["Age group", "Metric"],
    headings = ["Age group", "Metric", "Inh_c", "Inh_nc", "Ing_c", "Ing_nc", "Der_c", "Der_nc"]
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

def getdjtemplate_5():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
        {% for l_heading in l_headings %}
            <th rowspan="3">{{ l_heading }}</th>
        {% endfor %}
            <th colspan="6">Exposure route</th>
        </tr>
        <tr>
            <th colspan="2">Inhalation</th>
            <th colspan="2">Ingestion</th>
            <th colspan="2">Dermal</th>
        </tr>
        <tr>
            <th scope="col">Competitive</th>
            <th scope="col">Non-competitive</th> 
            <th scope="col">Competitive</th>
            <th scope="col">Non-competitive</th> 
            <th scope="col">Competitive</th>
            <th scope="col">Non-competitive</th> 
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
pv5headings = getheaderpv5()
sumheadings1 = getheadersum1()
sumheadings5 = getheadersum5()

djtemplate = getdjtemplate()
djtemplate_5 = getdjtemplate_5()
tmpl = Template(djtemplate)
tmpl_5 = Template(djtemplate_5)


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>SWIM<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_all(swim_obj):
    table1_out=table_1(swim_obj)
    table2_out=table_2(swim_obj)
    table3_out=table_3(swim_obj)
    table4_out=table_4(swim_obj)
    table5_out=table_5(swim_obj)
    table6_out=table_6(swim_obj)

    html = table1_out
    html = html + table2_out
    html = html + table3_out
    html = html + table4_out
    html = html + table5_out
    html = html + table6_out
    return html


def gett1data(swim_obj):
    data = { 
        "Parameter": ['Chemical name', 'Log Kow', 'Molecular weight of substance', "Henry's law constant",
                      'Gas constant', 'Ambient air temp', 'Water concentration', 'NOAEL',],
        "Value": ['%s' % swim_obj.chemical_name, '%s' % swim_obj.log_kow, '%s' % swim_obj.mw, '%s' % swim_obj.hlc,
                  '%s' % swim_obj.r, '%s' % swim_obj.T, '%s' % swim_obj.cw, '%s' % swim_obj.noael,],
        "Units": ['', '', 'g/mol', 'atm-m<sup>3</sup>/mole', 'atm-m<sup>3</sup>/mole-K', '<sup>o</sup>C', 'mg/L', 'mg/kg/day',],
        }
    return data

def gett2data(swim_obj):
    data = { 
        "Parameter": ['Body weight all adult', 'Body weight female adult', 'Surface area exposed (Competitive)', "Surface area exposed (Non-competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-competitive)'],
        "Value": ['%s' % swim_obj.bw_aa, '%s' % swim_obj.bw_fa, '%s' % swim_obj.sa_a_c, '%s' % swim_obj.sa_a_nc,
                  '%s' % swim_obj.et_a_c, '%s' % swim_obj.et_a_nc, '%s' % swim_obj.ir_a_c, '%s' % swim_obj.ir_a_nc,
                  '%s' % swim_obj.igr_a_c, '%s' % swim_obj.igr_a_nc,],
        "Units": ['kg', 'kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

def gett3data(swim_obj):
    data = { 
        "Parameter": ['Body weight', 'Surface area exposed (Competitive)', "Surface area exposed (Non-competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-competitive)'],
        "Value": ['%s' % swim_obj.bw_c1, '%s' % swim_obj.sa_c1_c, '%s' % swim_obj.sa_c1_nc,
                  '%s' % swim_obj.et_c1_c, '%s' % swim_obj.et_c1_nc, '%s' % swim_obj.ir_c1_c, '%s' % swim_obj.ir_c1_nc,
                  '%s' % swim_obj.igr_c1_c, '%s' % swim_obj.igr_c1_nc,],
        "Units": ['kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

def gett4data(swim_obj):
    data = { 
        "Parameter": ['Body weight', 'Surface area exposed (Competitive)', "Surface area exposed (Non-competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-competitive)'],
        "Value": ['%s' % swim_obj.bw_c2, '%s' % swim_obj.sa_c2_c, '%s' % swim_obj.sa_c2_nc,
                  '%s' % swim_obj.et_c2_c, '%s' % swim_obj.et_c2_nc, '%s' % swim_obj.ir_c2_c, '%s' % swim_obj.ir_c2_nc,
                  '%s' % swim_obj.igr_c2_c, '%s' % swim_obj.igr_c2_nc,],
        "Units": ['kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

def gett5data(swim_obj):
    data = { 
        "Age group": ['Adult', 'Female adult', 'Children (6-<11)', 'Children (11-<16)',],
        "Inh_c": ['%.3e' % swim_obj.inh_c_aa, '%.3e' % swim_obj.inh_c_fa, '%.3e' % swim_obj.inh_c_c1, '%.3e' % swim_obj.inh_c_c2,],
        "Inh_nc": ['%.3e' % swim_obj.inh_nc_aa, '%.3e' % swim_obj.inh_nc_fa, '%.3e' % swim_obj.inh_nc_c1, '%.3e' % swim_obj.inh_nc_c2,],
        "Ing_c": ['%.3e' % swim_obj.ing_c_aa, '%.3e' % swim_obj.ing_c_fa, '%.3e' % swim_obj.ing_c_c1, '%.3e' % swim_obj.ing_c_c2,],
        "Ing_nc": ['%.3e' % swim_obj.ing_nc_aa, '%.3e' % swim_obj.ing_nc_fa, '%.3e' % swim_obj.ing_nc_c1, '%.3e' % swim_obj.ing_nc_c2,],
        "Der_c": ['%.3e' % swim_obj.der_c_aa, '%.3e' % swim_obj.der_c_fa, '%.3e' % swim_obj.der_c_c1, '%.3e' % swim_obj.der_c_c2,],
        "Der_nc": ['%.3e' % swim_obj.der_nc_aa, '%.3e' % swim_obj.der_nc_fa, '%.3e' % swim_obj.der_nc_c1, '%.3e' % swim_obj.der_nc_c2,],
        }
    return data

def gett6data(swim_obj):
    data = { 
        "Age group": ['Adult', 'Female adult', 'Children (6-<11)', 'Children (11-<16)',],
        "Inh_c": ['%.3e' % swim_obj.inh_c_aa_moe, '%.3e' % swim_obj.inh_c_fa_moe, '%.3e' % swim_obj.inh_c_c1_moe, '%.3e' % swim_obj.inh_c_c2_moe,],
        "Inh_nc": ['%.3e' % swim_obj.inh_nc_aa_moe, '%.3e' % swim_obj.inh_nc_fa_moe, '%.3e' % swim_obj.inh_nc_c1_moe, '%.3e' % swim_obj.inh_nc_c2_moe,],
        "Ing_c": ['%.3e' % swim_obj.ing_c_aa_moe, '%.3e' % swim_obj.ing_c_fa_moe, '%.3e' % swim_obj.ing_c_c1_moe, '%.3e' % swim_obj.ing_c_c2_moe,],
        "Ing_nc": ['%.3e' % swim_obj.ing_nc_aa_moe, '%.3e' % swim_obj.ing_nc_fa_moe, '%.3e' % swim_obj.ing_nc_c1_moe, '%.3e' % swim_obj.ing_nc_c2_moe,],
        "Der_c": ['%.3e' % swim_obj.der_c_aa_moe, '%.3e' % swim_obj.der_c_fa_moe, '%.3e' % swim_obj.der_c_c1_moe, '%.3e' % swim_obj.der_c_c2_moe,],
        "Der_nc": ['%.3e' % swim_obj.der_nc_aa_moe, '%.3e' % swim_obj.der_nc_fa_moe, '%.3e' % swim_obj.der_nc_c1_moe, '%.3e' % swim_obj.der_nc_c2_moe,],
        }
    return data

def gettsumdata_1(log_kow, mw, hlc, r, T, cw, noael):
    data = { 
        "Parameter": ['Log Kow', 'Molecular weight of substance', "Henry's law constant", 
                      'Gas constant', 'Ambient air temp', 'Water concentration', 'NOAEL',],
        "Mean": ['%.4e' % numpy.mean(log_kow), '%.4e' % numpy.mean(mw), '%.4e' % numpy.mean(hlc), '%.4e' % numpy.mean(r), '%.4e' % numpy.mean(T), '%.4e' % numpy.mean(cw), '%.4e' % numpy.mean(noael)],
        "Std": ['%.4e' % numpy.std(log_kow), '%.4e' % numpy.std(mw), '%.4e' % numpy.std(hlc), '%.4e' % numpy.std(r), '%.4e' % numpy.std(T), '%.4e' % numpy.std(cw), '%.4e' % numpy.std(noael)],
        "Min": ['%.4e' % numpy.min(log_kow), '%.4e' % numpy.min(mw), '%.4e' % numpy.min(hlc), '%.4e' % numpy.min(r), '%.4e' % numpy.min(T), '%.4e' % numpy.min(cw), '%.4e' % numpy.min(noael)],
        "Max": ['%.4e' % numpy.max(log_kow), '%.4e' % numpy.max(mw), '%.4e' % numpy.max(hlc), '%.4e' % numpy.max(r), '%.4e' % numpy.max(T), '%.4e' % numpy.max(cw), '%.4e' % numpy.max(noael)],
        "Units": ['', 'g/mol', 'atm-m<sup>3</sup>/mole', 'atm-m<sup>3</sup>/mole-K', '<sup>o</sup>C', 'mg/L', 'mg/kg/day',],
    }
    return data

def gettsumdata_2(bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc):
    data = { 
        "Parameter": ['Body weight all adult', 'Body weight female adult', 'Surface area exposed (Competitive)', "Surface area exposed (Non-competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-competitive)'],
        "Mean": ['%.4e' % numpy.mean(bw_aa), '%.4e' % numpy.mean(bw_fa), '%.4e' % numpy.mean(sa_a_c), '%.4e' % numpy.mean(sa_a_nc), '%.4e' % numpy.mean(et_a_c), '%.4e' % numpy.mean(et_a_nc), 
                 '%.4e' % numpy.mean(ir_a_c), '%.4e' % numpy.mean(ir_a_nc), '%.4e' % numpy.mean(igr_a_c), '%.4e' % numpy.mean(igr_a_nc),],
        "Std": ['%.4e' % numpy.std(bw_aa), '%.4e' % numpy.std(bw_fa), '%.4e' % numpy.std(sa_a_c), '%.4e' % numpy.std(sa_a_nc), '%.4e' % numpy.std(et_a_c), '%.4e' % numpy.std(et_a_nc), 
                '%.4e' % numpy.std(ir_a_c), '%.4e' % numpy.std(ir_a_nc), '%.4e' % numpy.std(igr_a_c), '%.4e' % numpy.std(igr_a_nc),],
        "Min": ['%.4e' % numpy.min(bw_aa), '%.4e' % numpy.min(bw_fa), '%.4e' % numpy.min(sa_a_c), '%.4e' % numpy.min(sa_a_nc), '%.4e' % numpy.min(et_a_c), '%.4e' % numpy.min(et_a_nc), 
                '%.4e' % numpy.min(ir_a_c), '%.4e' % numpy.min(ir_a_nc), '%.4e' % numpy.min(igr_a_c), '%.4e' % numpy.min(igr_a_nc),],
        "Max": ['%.4e' % numpy.max(bw_aa), '%.4e' % numpy.max(bw_fa), '%.4e' % numpy.max(sa_a_c), '%.4e' % numpy.max(sa_a_nc), '%.4e' % numpy.max(et_a_c), '%.4e' % numpy.max(et_a_nc), 
                '%.4e' % numpy.max(ir_a_c), '%.4e' % numpy.max(ir_a_nc), '%.4e' % numpy.max(igr_a_c), '%.4e' % numpy.max(igr_a_nc),],
        "Units": ['kg', 'kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
    }
    return data

def gettsumdata_3(bw_aa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc):
    data = { 
        "Parameter": ['Body weight', 'Surface area exposed (Competitive)', "Surface area exposed (Non-competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-competitive)'],
        "Mean": ['%.4e' % numpy.mean(bw_aa), '%.4e' % numpy.mean(sa_a_c), '%.4e' % numpy.mean(sa_a_nc), '%.4e' % numpy.mean(et_a_c), '%.4e' % numpy.mean(et_a_nc), 
                 '%.4e' % numpy.mean(ir_a_c), '%.4e' % numpy.mean(ir_a_nc), '%.4e' % numpy.mean(igr_a_c), '%.4e' % numpy.mean(igr_a_nc),],
        "Std": ['%.4e' % numpy.std(bw_aa), '%.4e' % numpy.std(sa_a_c), '%.4e' % numpy.std(sa_a_nc), '%.4e' % numpy.std(et_a_c), '%.4e' % numpy.std(et_a_nc), 
                '%.4e' % numpy.std(ir_a_c), '%.4e' % numpy.std(ir_a_nc), '%.4e' % numpy.std(igr_a_c), '%.4e' % numpy.std(igr_a_nc),],
        "Min": ['%.4e' % numpy.min(bw_aa), '%.4e' % numpy.min(sa_a_c), '%.4e' % numpy.min(sa_a_nc), '%.4e' % numpy.min(et_a_c), '%.4e' % numpy.min(et_a_nc), 
                '%.4e' % numpy.min(ir_a_c), '%.4e' % numpy.min(ir_a_nc), '%.4e' % numpy.min(igr_a_c), '%.4e' % numpy.min(igr_a_nc),],
        "Max": ['%.4e' % numpy.max(bw_aa), '%.4e' % numpy.max(sa_a_c), '%.4e' % numpy.max(sa_a_nc), '%.4e' % numpy.max(et_a_c), '%.4e' % numpy.max(et_a_nc), 
                '%.4e' % numpy.max(ir_a_c), '%.4e' % numpy.max(ir_a_nc), '%.4e' % numpy.max(igr_a_c), '%.4e' % numpy.max(igr_a_nc),],
        "Units": ['kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
    }
    return data

def gettsumdata_5(inh_c_aa, inh_c_fa, inh_c_c1, inh_c_c2, inh_nc_aa, inh_nc_fa, 
                                        inh_nc_c1, inh_nc_c2, ing_c_aa, ing_c_fa, ing_c_c1, ing_c_c2, 
                                        ing_nc_aa, ing_nc_fa, ing_nc_c1, ing_nc_c2, der_c_aa, der_c_fa, 
                                        der_c_c1, der_c_c2, der_nc_aa, der_nc_fa, der_nc_c1, der_nc_c2):
    data = { 
        "Age group": ['Adult', 'Adult', 'Adult', 'Adult', 
                      'Female adult', 'Female adult', 'Female adult', 'Female adult', 
                      'Children (6-<11)', 'Children (6-<11)', 'Children (6-<11)', 'Children (6-<11)', 
                      'Children (11-<16)', 'Children (11-<16)', 'Children (11-<16)', 'Children (11-<16)',],
        "Metric": ['Mean', 'Std', 'Min', 'Max', 
                   'Mean', 'Std', 'Min', 'Max',
                   'Mean', 'Std', 'Min', 'Max',
                   'Mean', 'Std', 'Min', 'Max',],
        "Inh_c": ['%.3e' % numpy.mean(inh_c_aa), '%.3e' % numpy.std(inh_c_aa), '%.3e' % numpy.min(inh_c_aa), '%.3e' % numpy.max(inh_c_aa),
                  '%.3e' % numpy.mean(inh_c_fa), '%.3e' % numpy.std(inh_c_fa), '%.3e' % numpy.min(inh_c_fa), '%.3e' % numpy.max(inh_c_fa),
                  '%.3e' % numpy.mean(inh_c_c1), '%.3e' % numpy.std(inh_c_c1), '%.3e' % numpy.min(inh_c_c1), '%.3e' % numpy.max(inh_c_c1),
                  '%.3e' % numpy.mean(inh_c_c2), '%.3e' % numpy.std(inh_c_c2), '%.3e' % numpy.min(inh_c_c2), '%.3e' % numpy.max(inh_c_c2),],
        "Inh_nc": ['%.3e' % numpy.mean(inh_nc_aa), '%.3e' % numpy.std(inh_nc_aa), '%.3e' % numpy.min(inh_nc_aa), '%.3e' % numpy.max(inh_nc_aa), 
                   '%.3e' % numpy.mean(inh_nc_fa), '%.3e' % numpy.std(inh_nc_fa), '%.3e' % numpy.min(inh_nc_fa), '%.3e' % numpy.max(inh_nc_fa), 
                   '%.3e' % numpy.mean(inh_nc_c1), '%.3e' % numpy.std(inh_nc_c1), '%.3e' % numpy.min(inh_nc_c1), '%.3e' % numpy.max(inh_nc_c1), 
                   '%.3e' % numpy.mean(inh_nc_c2), '%.3e' % numpy.std(inh_nc_c2), '%.3e' % numpy.min(inh_nc_c2), '%.3e' % numpy.max(inh_nc_c2),],
        "Ing_c": ['%.3e' % numpy.mean(ing_c_aa), '%.3e' % numpy.std(ing_c_aa), '%.3e' % numpy.min(ing_c_aa), '%.3e' % numpy.max(ing_c_aa), 
                  '%.3e' % numpy.mean(ing_c_fa), '%.3e' % numpy.std(ing_c_fa), '%.3e' % numpy.min(ing_c_fa), '%.3e' % numpy.max(ing_c_fa), 
                  '%.3e' % numpy.mean(ing_c_c1), '%.3e' % numpy.std(ing_c_c1), '%.3e' % numpy.min(ing_c_c1), '%.3e' % numpy.max(ing_c_c1), 
                  '%.3e' % numpy.mean(ing_c_c2), '%.3e' % numpy.std(ing_c_c2), '%.3e' % numpy.min(ing_c_c2), '%.3e' % numpy.max(ing_c_c2),],
        "Ing_nc": ['%.3e' % numpy.mean(ing_nc_aa), '%.3e' % numpy.std(ing_nc_aa), '%.3e' % numpy.min(ing_nc_aa), '%.3e' % numpy.max(ing_nc_aa), 
                   '%.3e' % numpy.mean(ing_nc_fa), '%.3e' % numpy.std(ing_nc_fa), '%.3e' % numpy.min(ing_nc_fa), '%.3e' % numpy.max(ing_nc_fa), 
                   '%.3e' % numpy.mean(ing_nc_c1), '%.3e' % numpy.std(ing_nc_c1), '%.3e' % numpy.min(ing_nc_c1), '%.3e' % numpy.max(ing_nc_c1), 
                   '%.3e' % numpy.mean(ing_nc_c2), '%.3e' % numpy.std(ing_nc_c2), '%.3e' % numpy.min(ing_nc_c2), '%.3e' % numpy.max(ing_nc_c2),],
        "Der_c": ['%.3e' % numpy.mean(der_c_aa), '%.3e' % numpy.std(der_c_aa), '%.3e' % numpy.min(der_c_aa), '%.3e' % numpy.max(der_c_aa), 
                  '%.3e' % numpy.mean(der_c_fa), '%.3e' % numpy.std(der_c_fa), '%.3e' % numpy.min(der_c_fa), '%.3e' % numpy.max(der_c_fa), 
                  '%.3e' % numpy.mean(der_c_c1), '%.3e' % numpy.std(der_c_c1), '%.3e' % numpy.min(der_c_c1), '%.3e' % numpy.max(der_c_c1), 
                  '%.3e' % numpy.mean(der_c_c2), '%.3e' % numpy.std(der_c_c2), '%.3e' % numpy.min(der_c_c2), '%.3e' % numpy.max(der_c_c2),],
        "Der_nc": ['%.3e' % numpy.mean(der_nc_aa), '%.3e' % numpy.std(der_nc_aa), '%.3e' % numpy.min(der_nc_aa), '%.3e' % numpy.max(der_nc_aa), 
                   '%.3e' % numpy.mean(der_nc_fa), '%.3e' % numpy.std(der_nc_fa), '%.3e' % numpy.min(der_nc_fa), '%.3e' % numpy.max(der_nc_fa), 
                   '%.3e' % numpy.mean(der_nc_c1), '%.3e' % numpy.std(der_nc_c1), '%.3e' % numpy.min(der_nc_c1), '%.3e' % numpy.max(der_nc_c1), 
                   '%.3e' % numpy.mean(der_nc_c2), '%.3e' % numpy.std(der_nc_c2), '%.3e' % numpy.min(der_nc_c2), '%.3e' % numpy.max(der_nc_c2),],
        }
    return data

def table_1(swim_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs:</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical</H4>
            <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(swim_obj)
        t1rows = gethtmlrowsfromcols(t1data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
            </div>
        """
        return html

def table_2(swim_obj):
        #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section2"><span></span>Adult</H4>
            <div class="out_ container_output">
        """
        #table 2
        t2data = gett2data(swim_obj)
        t2rows = gethtmlrowsfromcols(t2data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
            </div>
        """
        return html

def table_3(swim_obj):
        #pre-table 3
        html = """
            <H4 class="out_3 collapsible" id="section3"><span></span>Children (6-11)</H4>
            <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(swim_obj)
        t3rows = gethtmlrowsfromcols(t3data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
            </div>
        """
        return html

def table_4(swim_obj):
        #pre-table 4
        html = """
            <H4 class="out_4 collapsible" id="section4"><span></span>Children (11-16)</H4>
            <div class="out_ container_output">
        """
        #table 4
        t4data = gett4data(swim_obj)
        t4rows = gethtmlrowsfromcols(t4data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_5(swim_obj):
        #pre-table 5
        html = """
        <H3 class="out_5 collapsible" id="section5"><span></span>Results</H3>
        <div class="out_">
            <H4 class="out_5 collapsible" id="section5"><span></span>Exposure dose (mg/kg/day)</H4>
            <div class="out_ container_output">
        """
        #table 5
        t5data = gett5data(swim_obj)
        t5rows = gethtmlrowsfromcols(t5data, pv5headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t5rows, l_headings=[pv5headings[0][0][0]])))
        html = html + """
            </div>
        """
        return html

def table_6(swim_obj):
        #pre-table 6
        html = """
            <H4 class="out_6 collapsible" id="section6"><span></span>Margin of exposure (MOE)</H4>
            <div class="out_ container_output">
        """
        #table 6
        t6data = gett6data(swim_obj)
        t6rows = gethtmlrowsfromcols(t6data, pv5headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t6rows, l_headings=[pv5headings[0][0][0]])))
        html = html + """
            </div>
        </div><br>
        """
        return html

def table_sum_1(i, log_kow, mw, hlc, r, T, cw, noael):
        #pre-table sum_input_1
        html = """
            <H3 class="out_0 collapsible" id="section4"><span></span>User Inputs</H3>
            <div class="out_ container_output">
                <H4 class="out_1 collapsible" id="section4"><span></span>Chemical</H4>
                <div class="out_ container_output">
        """
        #table sum_input_1
        tsuminputdata_1 = gettsumdata_1(log_kow, mw, hlc, r, T, cw, noael)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings1)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings1)))
        html = html + """
                </div>
        """
        return html

def table_sum_2(bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc):
        #pre-table sum_input_2
        html = """
            <H4 class="out_2 collapsible" id="section4"><span></span>Adult</H4>
            <div class="out_ container_output">
        """
        #table sum_input_2
        tsuminputdata_2 = gettsumdata_2(bw_aa, bw_fa, sa_a_c, sa_a_nc, et_a_c, et_a_nc, ir_a_c, ir_a_nc, igr_a_c, igr_a_nc)
        tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings1)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings1)))
        html = html + """
            </div>
        """
        return html

def table_sum_3(bw_c1, sa_c1_c, sa_c1_nc, et_c1_c, et_c1_nc, ir_c1_c, ir_c1_nc, igr_c1_c, igr_c1_nc):
        #pre-table sum_input_3
        html = """
            <H4 class="out_3 collapsible" id="section4"><span></span>Children (6-11)</H4>
            <div class="out_ container_output">
        """
        #table sum_input_3
        tsuminputdata_3 = gettsumdata_3(bw_c1, sa_c1_c, sa_c1_nc, et_c1_c, et_c1_nc, ir_c1_c, ir_c1_nc, igr_c1_c, igr_c1_nc)
        tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3, sumheadings1)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings1)))
        html = html + """
            </div>
        """
        return html

def table_sum_4(bw_c2, sa_c2_c, sa_c2_nc, et_c2_c, et_c2_nc, ir_c2_c, ir_c2_nc, igr_c2_c, igr_c2_nc):
        #pre-table sum_input_4
        html = """
            <H4 class="out_4 collapsible" id="section4"><span></span>Children (11-16)</H4>
            <div class="out_4 container_output">
        """
        #table sum_input_4
        tsuminputdata_4 = gettsumdata_3(bw_c2, sa_c2_c, sa_c2_nc, et_c2_c, et_c2_nc, ir_c2_c, ir_c2_nc, igr_c2_c, igr_c2_nc)
        tsuminputrows_4 = gethtmlrowsfromcols(tsuminputdata_4, sumheadings1)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_4, headings=sumheadings1)))
        html = html + """
            </div>
        </div>
        """
        return html

def table_sum_5(inh_c_aa, inh_c_fa, inh_c_c1, inh_c_c2, inh_nc_aa, inh_nc_fa, 
                inh_nc_c1, inh_nc_c2, ing_c_aa, ing_c_fa, ing_c_c1, ing_c_c2, 
                ing_nc_aa, ing_nc_fa, ing_nc_c1, ing_nc_c2, der_c_aa, der_c_fa, 
                der_c_c1, der_c_c2, der_nc_aa, der_nc_fa, der_nc_c1, der_nc_c2):
        #pre-table sum_input_5
        html = """
            <H3 class="out_5 collapsible" id="section4"><span></span>Results</H3>
            <div class="out_5 container_output">
                <H4 class="out_5 collapsible" id="section5"><span></span>Exposure dose (mg/kg/day)</H4>
                <div class="out_5 container_output">
        """
        #table sum_input_5
        tsuminputdata_5 = gettsumdata_5(inh_c_aa, inh_c_fa, inh_c_c1, inh_c_c2, inh_nc_aa, inh_nc_fa, 
                                        inh_nc_c1, inh_nc_c2, ing_c_aa, ing_c_fa, ing_c_c1, ing_c_c2, 
                                        ing_nc_aa, ing_nc_fa, ing_nc_c1, ing_nc_c2, der_c_aa, der_c_fa, 
                                        der_c_c1, der_c_c2, der_nc_aa, der_nc_fa, der_nc_c1, der_nc_c2)
        tsuminputrows_5 = gethtmlrowsfromcols(tsuminputdata_5, sumheadings5[1])
        html = html + tmpl_5.render(Context(dict(data=tsuminputrows_5, l_headings=[sumheadings5[0][0][0], sumheadings5[0][0][1]])))
        html = html + """
            </div>
        """
        return html

def table_sum_6(inh_c_aa_moe, inh_c_fa_moe, inh_c_c1_moe, inh_c_c2_moe, inh_nc_aa_moe, inh_nc_fa_moe, 
                inh_nc_c1_moe, inh_nc_c2_moe, ing_c_aa_moe, ing_c_fa_moe, ing_c_c1_moe, ing_c_c2_moe, 
                ing_nc_aa_moe, ing_nc_fa_moe, ing_nc_c1_moe, ing_nc_c2_moe, der_c_aa_moe, der_c_fa_moe, 
                der_c_c1_moe, der_c_c2_moe, der_nc_aa_moe, der_nc_fa_moe, der_nc_c1_moe, der_nc_c2):
        #pre-table sum_input_6
        html = """
            <H4 class="out_6 collapsible" id="section6"><span></span>Margin of exposure (MOE)</H4>
            <div class="out_ container_output">
        """
        #table sum_input_6
        tsuminputdata_6 = gettsumdata_5(inh_c_aa_moe, inh_c_fa_moe, inh_c_c1_moe, inh_c_c2_moe, inh_nc_aa_moe, inh_nc_fa_moe, 
                                        inh_nc_c1_moe, inh_nc_c2_moe, ing_c_aa_moe, ing_c_fa_moe, ing_c_c1_moe, ing_c_c2_moe, 
                                        ing_nc_aa_moe, ing_nc_fa_moe, ing_nc_c1_moe, ing_nc_c2_moe, der_c_aa_moe, der_c_fa_moe, 
                                        der_c_c1_moe, der_c_c2_moe, der_nc_aa_moe, der_nc_fa_moe, der_nc_c1_moe, der_nc_c2)
        tsuminputrows_6 = gethtmlrowsfromcols(tsuminputdata_6, sumheadings5[1])
        html = html + tmpl_5.render(Context(dict(data=tsuminputrows_6, l_headings=[sumheadings5[0][0][0], sumheadings5[0][0][1]])))
        html = html + """
            </div>
        </div>
        """
        return html


