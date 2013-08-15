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


# def getheadersum1():
#     headings = ["Parameter", "Mean", "Std", "Min", "Max", "Units"]
#     return headings

# def getheadersum2():
#     headings = ["Subpopulation", "Mean", "Std", "Min", "Max"]
#     return headings

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
# pva2headings = getheaderpva2()
# sumheadings1 = getheadersum1()
# sumheadings2 = getheadersum2()

djtemplate = getdjtemplate()
djtemplate_5 = getdjtemplate_5()
tmpl = Template(djtemplate)
tmpl_5 = Template(djtemplate_5)


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>swim<br>
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
        "Parameter": ['Chemical name', 'Log Kow', 'Molecular weight of substance', "Henry's law",
                      'Gas constant', 'Ambient air temp', 'Water concentration', 'NOAEL',],
        "Value": ['%s' % swim_obj.chemical_name, '%s' % swim_obj.log_kow, '%s' % swim_obj.mw, '%s' % swim_obj.hlc,
                  '%s' % swim_obj.r, '%s' % swim_obj.T, '%s' % swim_obj.cw, '%s' % swim_obj.noael,],
        "Units": ['', '', 'g/mol', 'atm-m<sup>3</sup>/mole', 'atm-m<sup>3</sup>/mole-K', '<sup>o</sup>C', 'mg/L', 'mg/kg/day',],
        }
    return data

def gett2data(swim_obj):
    data = { 
        "Parameter": ['Body weight all adult', 'Body weight female adult', 'Surface area exposed (Competitive)', "Surface area exposed (Non-Competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-Competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-Competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-Competitive)'],
        "Value": ['%s' % swim_obj.bw_aa, '%s' % swim_obj.bw_fa, '%s' % swim_obj.sa_a_c, '%s' % swim_obj.sa_a_nc,
                  '%s' % swim_obj.et_a_c, '%s' % swim_obj.et_a_nc, '%s' % swim_obj.ir_a_c, '%s' % swim_obj.ir_a_nc,
                  '%s' % swim_obj.igr_a_c, '%s' % swim_obj.igr_a_nc,],
        "Units": ['kg', 'kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

def gett3data(swim_obj):
    data = { 
        "Parameter": ['Body weight', 'Surface area exposed (Competitive)', "Surface area exposed (Non-Competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-Competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-Competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-Competitive)'],
        "Value": ['%s' % swim_obj.bw_c1, '%s' % swim_obj.sa_c1_c, '%s' % swim_obj.sa_c1_nc,
                  '%s' % swim_obj.et_c1_c, '%s' % swim_obj.et_c1_nc, '%s' % swim_obj.ir_c1_c, '%s' % swim_obj.ir_c1_nc,
                  '%s' % swim_obj.igr_c1_c, '%s' % swim_obj.igr_c1_nc,],
        "Units": ['kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

def gett4data(swim_obj):
    data = { 
        "Parameter": ['Body weight', 'Surface area exposed (Competitive)', "Surface area exposed (Non-Competitive)",
                      'Exposure time (Competitive)', 'Exposure time (Non-Competitive)', 'Inhalation rate of pool water (Competitive)', 'Inhalation rate of pool water (Non-Competitive)',
                      'Ingestion rate of pool water (Competitive)', 'Ingestion rate of pool water (Non-Competitive)'],
        "Value": ['%s' % swim_obj.bw_c2, '%s' % swim_obj.sa_c2_c, '%s' % swim_obj.sa_c2_nc,
                  '%s' % swim_obj.et_c2_c, '%s' % swim_obj.et_c2_nc, '%s' % swim_obj.ir_c2_c, '%s' % swim_obj.ir_c2_nc,
                  '%s' % swim_obj.igr_c2_c, '%s' % swim_obj.igr_c2_nc,],
        "Units": ['kg', 'cm<sup>2</sup>', 'cm<sup>2</sup>', 'hr/day', 'hr/day', 'L/hr', 'L/hr', 'L/hr', 'L/hr',],
        }
    return data

    headings = ["Parameter", "Competitive", "Non-competitive", "Units"]


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
        <div class="out_">
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
        <div class="out_">
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
        <div class="out_">
            <H4 class="out_4 collapsible" id="section4"><span></span>Children (11-16)</H4>
                <div class="out_ container_output">
        """
        #table 4
        t4data = gett4data(swim_obj)
        t4rows = gethtmlrowsfromcols(t4data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_5(swim_obj):
        #pre-table 5
        html = """
        <br>
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
        <br>
        <div class="out_">
            <H4 class="out_6 collapsible" id="section6"><span></span>MOE</H4>
                <div class="out_ container_output">
        """
        #table 6
        t6data = gett6data(swim_obj)
        t6rows = gethtmlrowsfromcols(t6data, pv5headings[1])       
        html = html + tmpl_5.render(Context(dict(data=t6rows, l_headings=[pv5headings[0][0][0]])))
        html = html + """
                </div>
        """
        return html