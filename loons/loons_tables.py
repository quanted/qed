import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from loons import loons_model, loons_parameters
import logging
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva2():
    headings = ["Class", "Initial Population"]
    return headings

def getheaderpva3(s):
    headings = ["Class"]
    for i in range(s):
        if i != 3:
            name_temp = 'Juvenile Year'+str(i+1)
            headings.append(name_temp)
        if i==3:
            headings.append("Adult")
    return headings

def getheaderpva3a():
    headings = ["Class", "Juvenile Year 1", "Juvenile Year 2", "Juvenile Year 3", "Adult"]
    return headings

def getheaderpva4():
    headings = ["Parameter", "Sensitivity", "Elasticity"]
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

def gett1data(loons_obj):
    data = { 
        "Parameter": [mark_safe('Pairing propensity for age &ge; 3'), "Chicks raised to mid-Aug per paired female", "Assumed proportion of chicks that are female", mark_safe('Annual survival for age &ge; 3'), mark_safe('Annual survival for age < 3'), "Modeling duration"],
        "Value": [loons_obj.b, loons_obj.m, loons_obj.r, loons_obj.pa, loons_obj.sj, loons_obj.t],
        "Units": ['', '', '', '', '', 'year'],
    }
    return data

def gett3adata(loons_obj):
    data = { 
        "Class": ["Juvenile Year 1", "Juvenile Year 2", "Juvenile Year 3", "Adult"],
        "Juvenile Year 1": ['%.2f' %loons_obj.l_m[0,0], '%.2f' %loons_obj.l_m[1,0], '%.2f' %loons_obj.l_m[2,0], '%.2f' %loons_obj.l_m[3,0]],
        "Juvenile Year 2": ['%.2f' %loons_obj.l_m[0,1], '%.2f' %loons_obj.l_m[1,1], '%.2f' %loons_obj.l_m[2,1], '%.2f' %loons_obj.l_m[3,1]],
        "Juvenile Year 3": ['%.2f' %loons_obj.l_m[0,2], '%.2f' %loons_obj.l_m[1,2], '%.2f' %loons_obj.l_m[2,2], '%.2f' %loons_obj.l_m[3,2]],
        "Adult": ['%.2f' %loons_obj.l_m[0,3], '%.2f' %loons_obj.l_m[1,3], '%.2f' %loons_obj.l_m[2,3], '%.2f' %loons_obj.l_m[3,3]],
    }
    return data

def gett4data(loons_obj):
    data = { 
        "Parameter": [mark_safe('Pairing propensity for age &ge; 3'), "Chicks raised to mid-Aug per paired female", mark_safe('Annual survival for age < 3'), "Juvenile Maturation rate",
                      mark_safe('Annual survival for age &ge; 3'), "Per capita fecundity", "Probility of a juvenile growing into an adult", "Probility of a juvenile remain in the class"],
        "Sensitivity": ['%.4f' %loons_obj.sen_b, '%.4f' % loons_obj.sen_m, '%.4f' % loons_obj.sen_sj, '%.4f' % loons_obj.sen_rj,  
                        '%.4f' %loons_obj.sen_pa, '%.4f' % loons_obj.sen_fa, '%.4f' % loons_obj.sen_gj, '%.4f' % loons_obj.sen_pj],
        "Elasticity": ['%.4f' %loons_obj.ela_b, '%.4f' % loons_obj.ela_m, '%.4f' % loons_obj.ela_sj, '%.4f' % loons_obj.ela_rj,  
                       '%.4f' %loons_obj.ela_pa, '%.4f' % loons_obj.ela_fa, '%.4f' % loons_obj.ela_gj, '%.4f' % loons_obj.ela_pj],
    }
    return data

pvuheadings = getheaderpvu()
pva2headings = getheaderpva2()
pva3aheadings = getheaderpva3a()
pva4headings = getheaderpva4()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(loons_obj):
    # html_all = timestamp()      
    html_all = table_1(loons_obj)      
    html_all = html_all + table_2(loons_obj)
    html_all = html_all + table_3(loons_obj)
    html_all = html_all + table_4(loons_obj)
    html_all = html_all + table_5(loons_obj)
    return html_all

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Loons Population Model<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_1(loons_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section1"><span></span>Vital rates</H4>
                <div class="out_ container_output">
        """
        t1data = gett1data(loons_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(loons_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section4"><span></span>Initial population</H4>
                <div class="out_ container_output">
        """
        #table 3
        t2data={}
        pva2headings = getheaderpva2()
        pva3headings = getheaderpva3(4)
        loons_obj.n_o.astype(str)
        t2data["Initial Population"] = [k[0] for k in loons_obj.n_o.tolist()]
        t2data['Class']=pva3headings[1:(4+1)]
        t2rows = gethtmlrowsfromcols(t2data, pva2headings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pva2headings)))
        html = html + """
                </div>
        """
        return html

# def table_3(loons_obj):
#         # #pre-table 4
#         html = """
#             <H4 class="out_3 collapsible" id="section3"><span></span>Leslie matrix</H4>
#                 <div class="out_3 container_output">
#         """ 
#         #table 3
#         pva3headings = getheaderpva3(4)
#         loons_obj.l_m.astype(str)
#         t3data = dict(zip(pva3headings[1:(4+1)], loons_obj.l_m.T.tolist()))
#         t3data['Class']=pva3headings[1:(4+1)]
#         t3rows = gethtmlrowsfromcols(t3data, pva3headings)
#         html = html + tmpl.render(Context(dict(data=t3rows, headings=pva3headings)))
#         html = html + """
#                 </div>
#         """
#         return html


def table_3(loons_obj):
        html = """
            <H4 class="out_3 collapsible" id="section1"><span></span>Leslie matrix</H4>
                <div class="out_ container_output">
        """
        t3data = gett3adata(loons_obj)
        t3rows = gethtmlrowsfromcols(t3data,pva3aheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pva3aheadings)))
        html = html + """
                </div>
        """
        return html

def table_4(loons_obj):
        html = """
        <H3 class="out_4 collapsible" id="section4"><span></span>Outputs</H3>
        <div class="out_4">
            <H4 class="out_4 collapsible" id="section4"><span></span>Sensitivity and elasticity</H4>
                <div class="out_ container_output">
        """
        t4data = gett4data(loons_obj)
        t4rows = gethtmlrowsfromcols(t4data,pva4headings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pva4headings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_5(loons_obj):
        html = """
            <H4 class="out_4 collapsible" id="section4"><span></span>Population growth rate confidence interval (Iteration = %s)</H4>
                <div class="out_ container_output">
                    <table class="out_">
                        <tr>
                            <th>Parameter</th>
                            <th>2.5th percentile</th>
                            <th>97.5th percentile</th>
                        </tr>
                        <tr>
                            <td>Population growth rate (&lambda;)</td>
                            <td>%.4f</td>
                            <td>%.4f</td>
                        </tr>
                    </table>
                </div>
        """ % (10000, loons_obj.lamda_ci_out_025, loons_obj.lamda_ci_out_975)
        return html
