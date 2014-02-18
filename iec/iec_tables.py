import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
import time
import datetime
from iec import iec_model
from iec import iec_parameters
import time
import datetime
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

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def getheadersum_un():
    headings = ["Parameter", "Mean", "Std", "Min", "Max"]
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



def gett1data(iec_obj):
    data = { 
        "Parameter": ['LC50 or LD50', 'Threshold', 'Slope',],
        "Value": [iec_obj.LC50, iec_obj.threshold, iec_obj.dose_response,],
    }
    return data

def gettsumdata_1(LC50_pool, threshold_pool, dose_response_pool):
    data = { 
        "Parameter": ['LC50 or LD50', 'Threshold', 'Slope',],
        "Mean": ['%.2e' % numpy.mean(LC50_pool),'%.2e' % numpy.mean(threshold_pool),'%.2e' % numpy.mean(dose_response_pool)],
        "Std": ['%.2e' % numpy.std(LC50_pool),'%.2e' % numpy.std(threshold_pool),'%.2e' % numpy.std(dose_response_pool)],
        "Min": ['%.2e' % numpy.min(LC50_pool),'%.2e' % numpy.min(threshold_pool),'%.2e' % numpy.min(dose_response_pool)],
        "Max": ['%.2e' % numpy.max(LC50_pool),'%.2e' % numpy.max(threshold_pool),'%.2e' % numpy.max(dose_response_pool)],
    }
    return data

def gett2data(iec_obj):
    #logger.info(vars(iec_obj))
    data = { 
        "Parameter": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Value": ['%.2f' % iec_obj.z_score_f_out,'%.2e' % iec_obj.F8_f_out,'%.2f' % iec_obj.chance_f_out, ],
    }
    return data

def gettsumdata_2_un(z_score_f_pool, F8_f_pool, chance_f_pool):
    data = { 
        "Parameter": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Mean": ['%.2e' % numpy.mean(z_score_f_pool),'%.2e' % numpy.mean(F8_f_pool),'%.2e' % numpy.mean(chance_f_pool)],
        "Std": ['%.2e' % numpy.std(z_score_f_pool),'%.2e' % numpy.std(F8_f_pool),'%.2e' % numpy.std(chance_f_pool)],
        "Min": ['%.2e' % numpy.min(z_score_f_pool),'%.2e' % numpy.min(F8_f_pool),'%.2e' % numpy.min(chance_f_pool)],
        "Max": ['%.2e' % numpy.max(z_score_f_pool),'%.2e' % numpy.max(F8_f_pool),'%.2e' % numpy.max(chance_f_pool)],
    }
    return data

def gett2dataqaqc(iec_obj):
    data = { 
        "Parameter": ['Z Score', '"F8"', 'Chance of Individual Effect',],
        "Value": ['%.2f' % iec_obj.z_score_f_out,'%.2e' % iec_obj.F8_f_out,'%.2f' % iec_obj.chance_f_out, ],
        "Expected Value": ['%.2f' % iec_obj.z_score_f_out_expected,'%.2e' % iec_obj.F8_f_out_expected,'%.2f' % iec_obj.chance_f_out_expected, ],
    }
    return data

# def gettsumdata(dose_response,LC50,threshold)
def gettsumdata(dose_response,LC50,threshold):
    data = { 
        "Parameter": ['Dose Response', 'LC50', 'Threshold'],
        "Mean": ['%.2e' % numpy.mean(dose_response), '%.2e' % numpy.mean(LC50),'%.2e' % numpy.mean(threshold),],
        "Std": ['%.2e' % numpy.std(dose_response),'%.2e' % numpy.std(LC50),'%.2e' % numpy.std(threshold),],
        "Min": ['%.2e' % numpy.min(dose_response),'%.2e' % numpy.min(LC50),'%.2e' % numpy.min(threshold),],
         "Max": ['%.2e' % numpy.max(dose_response),'%.2e' % numpy.max(LC50),'%.2e' % numpy.max(threshold),],
        "Unit": ['','mg/kg-bw', '',],
    }
    return data

# def gettsumdata_out(dose_response,LC50,threshold):
def gettsumdata_out(z_score_f_out, F8_f_out, chance_f_out):
    data = {
        "Parameter": ['Z Score F', 'F8', 'Chance F',],
        "Mean": ['%.2e' % numpy.mean(z_score_f_out),'%.2e' % numpy.mean(F8_f_out),'%.2e' % numpy.mean(chance_f_out),],
        "Std": ['%.2e' % numpy.std(z_score_f_out),'%.2e' % numpy.std(F8_f_out),'%.2e' % numpy.std(chance_f_out),],
        "Min": ['%.2e' % numpy.min(z_score_f_out),'%.2e' % numpy.min(F8_f_out),'%.2e' % numpy.min(chance_f_out),],
         "Max": ['%.2e' % numpy.max(z_score_f_out),'%.2e' % numpy.max(F8_f_out),'%.2e' % numpy.max(chance_f_out),],
        "Unit": ['','mg/kg-bw', '',],
    }
    return data

ivheadings = getheaderiv()
ovheadings = getheaderov()
ivheadings_un = getheadersum_un()
ovheadingsqaqc = getheaderovqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(iec_obj):
    html_all = table_1(iec_obj)
    html_all = html_all + table_2(iec_obj)
    return html_all

def table_all_qaqc(iec_obj):
    html_all = table_1(iec_obj)
    html_all = html_all + table_2_qaqc(iec_obj)
    return html_all

def timestamp(iec_obj="", batch_jid=""):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    if iec_obj:
        st = datetime.datetime.strptime(iec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>IEC Version 1.0 (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

# def timestamp():
#     ts = time.time()
#     st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
#     html="""
#     <div class="out_">
#         <b>IEC Version 1.0</a> (Beta)<br>
#     """
#     html = html + st
#     html = html + " (UTC)</b>"
#     html = html + """
#     </div>"""
#     return html

def table_all_un(LC50_pool, threshold_pool, dose_response_pool, z_score_f_pool, F8_f_pool, chance_f_pool):
    html_all = table_1_un(LC50_pool, F8_f_pool, dose_response_pool)
    html_all = html_all + table_2_un(z_score_f_pool, threshold_pool, chance_f_pool)
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


def table_all_sum(dose_response,LC50,threshold,z_score_f_out, F8_f_out, chance_f_out):
    html_all_sum = table_sum_input(dose_response,LC50,threshold)
    html_all_sum += table_sum_output(z_score_f_out, F8_f_out, chance_f_out)
    return html_all_sum

def table_sum_input(dose_response,LC50,threshold):
        #pre-table sum_input
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsuminputdata = gettsumdata(dose_response,LC50,threshold)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def table_sum_output(z_score_f_out, F8_f_out, chance_f_out):
        #pre-table sum_input
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>IEC Outputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(z_score_f_out, F8_f_out, chance_f_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        html = html + """
                </div>
        </div>
        <br>"""
        return html
        
def table_1_un(LC50_pool, threshold_pool, dose_response_pool):
        html = """
        <H4 class="out_1 collapsible" id="section1"><span></span>User Inputs</H4>
            <div class="out_ container_output">
        """
        t1data_un = gettsumdata_1(LC50_pool, threshold_pool, dose_response_pool)
        t1rows_un = gethtmlrowsfromcols(t1data_un,ivheadings_un)
        html = html + tmpl.render(Context(dict(data=t1rows_un, headings=ivheadings_un)))
        html = html + """
            </div>
        """
        return html

def table_2_un(z_score_f_pool, F8_f_pool, chance_f_pool):
        html = """
        <H4 class="out_2 collapsible" id="section1"><span></span>Outputs</H4>
            <div class="out_ container_output">
        """
        t2data_un = gettsumdata_2_un(z_score_f_pool, F8_f_pool, chance_f_pool)
        t2rows_un = gethtmlrowsfromcols(t2data_un,ivheadings_un)
        html = html + tmpl.render(Context(dict(data=t2rows_un, headings=ivheadings_un)))
        html = html + """
            </div>
        """
        return html