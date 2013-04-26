import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from iec import iec_model
from iec import iec_parameters

def getheaderiv():
  headings = ["User Input", "Value"]
  return headings

def getheaderov():
  headings = ["IEC Output", "Value"]
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
    <table id="output" >
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

def gett1data(LC50,threshold,dose_response):
    data = { 
        "User Input": ['LC50 or LD50', 'Threshold', 'Slope',],
        "Value": [LC50, threshold, dose_response,],
    }
    return data

def gett2data(z_score_f,F8_f,chance_f):
    data = { 
        "IEC Output": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Value": ['%.2f' % z_score_f,'%.2f' % F8_f,'%.2f' % chance_f, ],
    }
    return data

ivheadings = getheaderiv()
ovheadings = getheaderov()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all():
    table1_out = table_1(ivheadings,tmpl,LC50,threshold,dose_response)
    table2_out = table_2(ovheadings,tmpl,z_score_f,F8_f,chance_f)

    html_all = table_1(ivheadings,tmpl,LC50,threshold,dose_response)
    html_all = html_all + table_2(ovheadings,tmpl,z_score_f,F8_f,chance_f)
    return html_all, table1_out, table2_out

def table_1(ivheadings,tmpl,LC50,threshold,dose_response):
    #pre-table 1
        html = """
        <table border="1" border="1" class="out_1">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """
    #table 1
        t1data = gett1data(LC50,threshold,dose_response)
        t1rows = gethtmlrowsfromcols(t1data,ivheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=ivheadings)))
        return html

def table_2(ovheadings,tmpl,z_score_f,F8_f,chance_f):
    #pre-table 1
        html = """
        <table border="1" border="1" class="out_2">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr><H4>Application and Chemical Information</H4></tr>
        <tr></tr>
        </table>
        """
    #table 2
        t2data = gett2data(z_score_f,F8_f,chance_f)
        t2rows = gethtmlrowsfromcols(t2data,ovheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=ovheadings)))
        return html