import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from leslie_probit import leslie_probit_model, leslie_probit_parameters
import logging
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva():
    headings = ["App", "Rate", "Day of Application"]
    headings_show = ["App", "Rate (lb ai/acre)", "Day of Application"]
    return headings, headings_show


def getheaderpva2():
    headings = ["Class", "Initial Population"]
    return headings

def getheaderpva3(s):
    headings = ["Class"]
    for i in range(s):
        name_temp = str(i+1)
        headings.append(name_temp)
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

def gett1data(leslie_probit_obj):
    data = { 
        "Parameter": ["Animal name", "Chemical name", "App target", "% a.i.", "Chemical half life", "Solubility", "Simulation durations"],
        "Value": [leslie_probit_obj.a_n, leslie_probit_obj.c_n, leslie_probit_obj.app_target, 100*leslie_probit_obj.ai, leslie_probit_obj.hl, leslie_probit_obj.sol, leslie_probit_obj.t],
        "Units": ['', '', '', '%', 'days', mark_safe('in water @ 25 &deg;C mg/L'), 'days'],
    }
    return data

def gett2data(index, rate, day):
    data = { 
        "App": ['%s' %index,  ],
        "Rate": [rate,],
        "Day of Application": ['%s' %day,],
    }
    return data

def gett3data(leslie_probit_obj):
    data = { 
        "Parameter": ["Probit dose response slope", "Tested animal", mark_safe("LD<sub>50</sub> of tested animal"), "Body weight of the tested animal", "Assessed animal", "Body weight of assessed animal", "Mineau scaling factor"],
        "Value": [leslie_probit_obj.b, leslie_probit_obj.test_species, leslie_probit_obj.ld50_test, leslie_probit_obj.bw_test, leslie_probit_obj.ass_species, leslie_probit_obj.bw_ass, leslie_probit_obj.x],
        "Units": ['', '', 'mg/kg-bw', 'g', '', 'g', ''],
    }
    return data

def gett4data(index, n_o):
    data = { 
        "Class": ['%s' %index,  ],
        "Initial Population": [n_o[0],],
    }
    return data

# def gett4data(index, n_o, l_m, name):
#     data = {
#         "Class": ['%s' %index,  ],
#         "Initial Population": [n_o,],
#     }
#     for i in name:
#         if (i != "Class") and (i != "Initial Population"):
#             data[i]=[l_m]
#     return data


pvuheadings = getheaderpvu()
pvaheadings = getheaderpva()
pva2headings = getheaderpva2()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(leslie_probit_obj):
    html_all = table_1(leslie_probit_obj)      
    html_all = html_all + table_2(leslie_probit_obj)
    html_all = html_all + table_3(leslie_probit_obj)
    html_all = html_all + table_5(leslie_probit_obj)
    html_all = html_all + table_4(leslie_probit_obj)
    return html_all

# def timestamp():
#     ts = time.time()
#     st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
#     html="""
#     <div class="out_">
#         <b>SIP <a href="http://www.epa.gov/oppefed1/models/terrestrial/sip/sip_user_guide.html">Version 1.0</a> (Beta)<br>
#     """
#     html = html + st
#     html = html + " (UTC)</b>"
#     html = html + """
#     </div>"""
#     return html

def table_1(leslie_probit_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section1"><span></span>Chemical Property</H4>
                <div class="out_ container_output">
        """
        t1data = gett1data(leslie_probit_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(leslie_probit_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section2"><span></span>Chemical Application (n=%s)</H4>
                <div class="out_ container_output">
        """ %(leslie_probit_obj.n_a)
        #table 2
        t2data_all=[]
        for i in range(int(leslie_probit_obj.n_a)):
            rate_temp=leslie_probit_obj.rate_out[i]
            day_temp=leslie_probit_obj.day_out[i]
            t2data_temp=gett2data(i+1, rate_temp, day_temp)
            t2data_all.append(t2data_temp)
        t2data = dict([(k,[t2data_ind[k][0] for t2data_ind in t2data_all]) for k in t2data_temp])
        t2rows = gethtmlrowsfromcols(t2data,pvaheadings[0])
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings[1])))
        html = html + """
                </div>
        """
        return html


def table_3(leslie_probit_obj):
        html = """
        <div class="out_">
            <H4 class="out_3 collapsible" id="section3"><span></span>Dose Response</H4>
                <div class="out_ container_output">
        """
        t3data = gett3data(leslie_probit_obj)
        t3rows = gethtmlrowsfromcols(t3data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_4(leslie_probit_obj):
        # #pre-table 4
        html = """
            <H4 class="out_4 collapsible" id="section4"><span></span>Initial Population</H4>
                <div class="out_ container_output">
        """
        #table 4
        t4data_all=[]
        for i in range(int(leslie_probit_obj.s)):
            n_o_temp=leslie_probit_obj.n_o[i]
            # day_temp=leslie_probit_obj.day_out[i]
            t4data_temp=gett4data(i+1, n_o_temp)
            t4data_all.append(t4data_temp)
        t4data = dict([(k,[t4data_ind[k][0] for t4data_ind in t4data_all]) for k in t4data_temp])
        t4rows = gethtmlrowsfromcols(t4data, pva2headings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pva2headings)))
        html = html + """
                </div>
        """
        return html

def table_5(leslie_probit_obj):
        # #pre-table 4
        html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Leslie Matrix</H4>
                <div class="out_ container_output">
        """ 
        #table 5
        pva3headings = getheaderpva3(leslie_probit_obj.s)
        leslie_probit_obj.l_m.astype(str)
        t5data = dict(zip(pva3headings[1:(leslie_probit_obj.s+1)], leslie_probit_obj.l_m.T.tolist()))
        t5data['Class']=[k+1 for k in range(leslie_probit_obj.s)]
        t5rows = gethtmlrowsfromcols(t5data, pva3headings)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=pva3headings)))
        html = html + """
                </div>
        """
        return html


