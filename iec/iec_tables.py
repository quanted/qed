import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
import time
import datetime
from iec import iec_model
from iec import iec_parameters
import logging

logger = logging.getLogger("IecTables")

def getheaderiv():
  headings = ["Parameter", "Value"]
  return headings

def getheaderov():
  headings = ["Parameter", "Value"]
  return headings

def getheaderovqaqc():
  headings = ["Parameter", "Value", "Expected Value"]
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

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>IEC Version 1.0 (Beta)<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    return html

def gett1data(iec_obj):
    data = { 
        "Parameter": ['LC50 or LD50', 'Threshold', 'Slope',],
        "Value": [iec_obj.LC50, iec_obj.threshold, iec_obj.dose_response,],
    }
    return data

def gett2data(iec_obj):
    logger.info(vars(iec_obj))
    data = { 
        "Parameter": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Value": ['%.2f' % iec_obj.z_score_f_out,'%.2e' % iec_obj.F8_f_out,'%.2f' % iec_obj.chance_f_out, ],
    }
    return data

def gett2dataqaqc(iec_obj):
    data = { 
        "Parameter": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Value": ['%.2f' % iec_obj.z_score_f_out,'%.2e' % iec_obj.F8_f_out,'%.2f' % iec_obj.chance_f_out, ],
        "Expected Value": ['%.2f' % iec_obj.z_score_f_out_expected,'%.2e' % iec_obj.F8_f_out_expected,'%.2f' % iec_obj.chance_f_out_expected, ],
    }
    return data

ivheadings = getheaderiv()
ovheadings = getheaderov()
ovheadingsqaqc = getheaderovqaqc()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(iec_obj):
    html_all = timestamp()
    html_all = html_all + table_1(iec_obj)
    html_all = html_all + table_2(iec_obj)
    return html_all

def table_all_qaqc(iec_obj):
    html_all = table_1(iec_obj)
    html_all = html_all + table_2_qaqc(iec_obj)
    return html_all

def table_1(iec_obj):
        html = """
        <H4 class="out_1 collapsible" id="section1"><span></span>User Inputs</H4>
            <div class="out_ container_output">
        """
        t1data = gett1data(iec_obj)
        t1rows = gethtmlrowsfromcols(t1data,ivheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=ivheadings)))
        html = html + """
            </div>
        """
        return html

def table_2(iec_obj):
        html = """
        <H4 class="out_2 collapsible" id="section2"><span></span>Model Output</H4>
            <div class="out_ container_output">
        """
        t2data = gett2data(iec_obj)
        t2rows = gethtmlrowsfromcols(t2data,ovheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=ovheadings)))
        html = html + """
            </div>
        """
        return html

def table_2_qaqc(iec_obj):
        html = """
        <H4 class="out_2 collapsible" id="section2"><span></span>Model Output</H4>
            <div class="out_ container_output">
        """
        t2data = gett2dataqaqc(iec_obj)
        t2rows = gethtmlrowsfromcols(t2data,ovheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=ovheadingsqaqc)))
        html = html + """
            </div>
        """
        return html