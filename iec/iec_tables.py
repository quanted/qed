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
    <table class="out_" >
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
        "Value": ['%.2f' % z_score_f,'%.2e' % F8_f,'%.2f' % chance_f, ],
    }
    return data

ivheadings = getheaderiv()
ovheadings = getheaderov()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all():
    html_all = table_1(ivheadings,tmpl,LC50,threshold,dose_response)
    html_all = html_all + table_2(ovheadings,tmpl,z_score_f,F8_f,chance_f)
    return html_all

def table_1(LC50,threshold,dose_response):
    #pre-table 1
        html = """
            <div class="out_1">
                <H3>User Inputs</H3>
            </div>
        """
    #table 1
        t1data = gett1data(LC50,threshold,dose_response)
        t1rows = gethtmlrowsfromcols(t1data,ivheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=ivheadings)))
        return html

def table_2(dose_response, LC50, threshold):
    #pre-table 1
        html = """
            <div class="out_2">
                <H3>Model Output</H3>
            </div>
        """
        z_score_f=iec_model.z_score_f(dose_response, LC50, threshold)
        F8_f=iec_model.F8_f(dose_response, LC50, threshold)
        chance_f=iec_model.chance_f(dose_response, LC50, threshold)

    #table 2
        t2data = gett2data(z_score_f,F8_f,chance_f)
        t2rows = gethtmlrowsfromcols(t2data,ovheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=ovheadings)))
        return html