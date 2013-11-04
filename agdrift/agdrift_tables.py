import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from agdrift import agdrift_model
from agdrift import agdrift_parameters
import time
import datetime
import logging

logger = logging.getLogger("AgdriftTables")

def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvr():
    headings = ["Parameter", "Value"]
    return headings

# def getheadersum():
#     headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
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


def gett1data(agdrift_obj):
    data = { 
        "Parameter": ['Application method', 'Orchard type', 'Drop size', 'Ecosystem type', ],
        "Value": [agdrift_obj.application_method, agdrift_obj.orchard_type, agdrift_obj.drop_size, agdrift_obj.ecosystem_type,],
    }
    return data

#def gett2data(agdrift_obj):
#    data = { 
#        "Parameter": ['Distance', 'Spray drift fraction',],
#        "Value": [agdrift_obj.results[0], agdrift_obj.results[1],],
#    }
#    return data
def gett2data(agdrift_obj):
    #logger.info(vars(iec_obj))
    data = { 
        "Parameter": ['Spray drift fraction of applied', 'Initial Average Deposition (g/ha)', 'Initial Average Deposition (lb/ac)', 'Initial Average Concentration (ng/L)', 'Initial Average Deposition (mg/cm2)',],
        "Value": ['%.2f' % agdrift_obj.init_avg_dep_foa,'%.2e' % agdrift_obj.avg_depo_gha,'%.2f' % agdrift_obj.avg_depo_lbac, '%.2f' % agdrift_obj.deposition_ngL, '%.2f' % agdrift_obj.deposition_mgcm],
    }
    return data

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# pvrheadingsqaqc = getheaderpvrqaqc()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(agdrift_obj):
    html_all = table_1(agdrift_obj)     
    html_all = html_all + table_2(agdrift_obj)
    html_all = html_all + table_3(agdrift_obj)
    return html_all

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>agdrift Version 0.1 (Beta)<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html


def table_1(agdrift_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section1"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        t1data = gett1data(agdrift_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(agdrift_obj):
        html = """
        <H4 class="out_2 collapsible" id="section2"><span></span>Model Output</H4>
            <div class="out_ container_output">
        """
        t2data = gett2data(agdrift_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
            </div>
        """
        return html        

def table_3(agdrift_obj):
        html = """
        <table style="display:none;">
            <tr>
                <td>distance</td>
                <td id="distance">%s</td>
            </tr>
            <tr>
                <td>deposition</td>
                <td id="deposition">%s</td>
            </tr>
        </table>
        <br>
        <h3 class="out_2 collapsible" id="section2"><span></span>Results</h3>
            <H4 class="out_2 collapsible" id="section3"><span></span>Plot of spray drift</H4>
                <div class="out_">
        """%(agdrift_obj.x, agdrift_obj.y)
        # t2data = gett2data(agdrift_obj)
        # t2rows = gethtmlrowsfromcols(t2data,pvrheadings)
        # html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        # html = html + """
        #         </div>
        # """
        return html


