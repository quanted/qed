import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from earthworm import earthworm_model,earthworm_parameters
import logging
import time
import datetime
import os
from google.appengine.ext.webapp import template

logger = logging.getLogger("earthwormTables")

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Earthworm Fugacity Modeling<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def getheaderpvu():
    headings = ["Parameter", "Value", "Units"]
    return headings    

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Units"]
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

def earthwormoutput(earthworm_obj):
    data = { 
        "Parameter": ['Chemical concentration in earthworm tissue',],
        "Value": ['%.5e' %earthworm_obj.earthworm_fugacity_out,],
        
        "Units": ['g/kg',],
    }
    return data


def gettsumdata(Kow, L, Cs, Kd, Ps, Cw, MW, Pe):
    data = { 
        "Parameter": [mark_safe('Octanol to water partition coefficient K<sub>OW</sub>'), 'Lipid fraction of earthworm L', mark_safe('Chemical concentration in soil C<sub>S</sub>'), mark_safe('Soil partitioning coefficient K<sub>d</sub>'), 
                    mark_safe('Bulk density of soil &#961;<sub>s</sub>'),mark_safe('Chemical concentration in pore water of soil C<sub>W</sub>'),
                    mark_safe('Molecular weight of chemical MW'),mark_safe('Density of earthworm &#961;<sub>E</sub>')],
        "Mean": ['%.2e' % numpy.mean(Kow),'%.2e' % numpy.mean(L),'%.2e' % numpy.mean(Cs), '%.2e' % numpy.mean(Kd), 
                 '%.2e' % numpy.mean(Ps), '%.2e' % numpy.mean(Cw), '%.2e' % numpy.mean(MW), '%.2e' % numpy.mean(Pe),],
        "Std":  ['%.2e' % numpy.std(Kow),'%.2e' % numpy.std(L),'%.2e' % numpy.std(Cs), '%.2e' % numpy.std(Kd), 
                '%.2e' % numpy.std(Ps), '%.2e' % numpy.std(Cw), '%.2e' % numpy.std(MW), '%.2e' % numpy.std(Pe),],
        "Min":  ['%.2e' % numpy.min(Kow),'%.2e' % numpy.min(L),'%.2e' % numpy.min(Cs), '%.2e' % numpy.min(Kd), 
                '%.2e' % numpy.min(Ps), '%.2e' % numpy.min(Cw), '%.2e' % numpy.min(MW), '%.2e' % numpy.min(Pe),],
        "Max":  ['%.2e' % numpy.max(Kow),'%.2e' % numpy.max(L),'%.2e' % numpy.max(Cs), '%.2e' % numpy.max(Kd), 
                '%.2e' % numpy.max(Ps), '%.2e' % numpy.max(Cw), '%.2e' % numpy.max(MW), '%.2e' % numpy.max(Pe),],
        "Units": ['none', 'none', mark_safe('mol/m<sup>3</sup>'),mark_safe('cm<sup>3</sup>/g'),mark_safe('g/cm<sup>3</sup>'),mark_safe('mol/m<sup>3</sup>'),'g/mol',mark_safe('kg/m<sup>3</sup>'),],
    }
    return data


def gettsumdata_out(Ce_out):
    data = { 
        "Parameter": ['Chemical concentration in earthworm tissue',],
        "Mean":['%.2e' % numpy.mean(Ce_out),],
        "Std":['%.2e' % numpy.std(Ce_out),],
        "Min":['%.2e' % numpy.min(Ce_out),],
        "Max":['%.2e' % numpy.max(Ce_out),],
        "Units": ['g/kg',],
    }
    return data


pvuheadings = getheaderpvu()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(earthworm_obj):
    table1_out = table_1()
    table2_out = table_2(earthworm_obj)
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_all = table1_out + table2_out 
    return html_all

def table_1():
    html = """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                <div class="out_input_table out_">
                </div>
                
                <script type="text/javascript">
                    $(document).ready(function(){

                    // Initialize output page//

                    //$('#export_menu').hide()

                    $(".out_input_table").append(localStorage.html_input);
                    $(".out_input_table :input").attr('disabled', true);

                    element_all = localStorage.html_new.split("&")
                    // console.log(element_all)
                    element1 = localStorage.html_new.split("&")[0].split("=")
                    // console.log(element_all.length)
                    for (i=0; i<element_all.length; i++) {
                        element_name_t = element_all[i].split("=")[0]
                        element_val_t = element_all[i].split("=")[1]
                        $('[name="'+element_name_t+'"]').val(element_val_t)
                    }
                    $(".input_button").hide()
                    })
                </script>"""
    return html

def table_2(earthworm_obj):
        html = """
            <H4 class="out_4 collapsible" id="section2"><span></span>Earthworm Fugacity Modeling Output</H4>
                <div class="out_ container_output">
        """
        t2data = earthwormoutput(earthworm_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_1batch(pvuheadings, tmpl, earthworm_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Input</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = getdata_batch(earthworm_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def getdata_batch(earthworm_obj):
    data = { 
        "Parameter": [mark_safe('Octanol to water partition coefficient K<sub>OW</sub>'), 'Lipid fraction of earthworm L', mark_safe('Chemical concentration in soil C<sub>S</sub>'), mark_safe('Soil partitioning coefficient K<sub>d</sub>'), 
                    mark_safe('Bulk density of soil &#961;<sub>s</sub>'),mark_safe('Chemical concentration in pore water of soil C<sub>W</sub>'),
                    mark_safe('Molecular weight of chemical MW'),mark_safe('Density of earthworm &#961;<sub>E</sub>')],
        "Value": [earthworm_obj.k_ow, earthworm_obj.l_f_e, earthworm_obj.c_s, earthworm_obj.k_d, earthworm_obj.p_s, earthworm_obj.c_w, earthworm_obj.m_w, earthworm_obj.p_e],
        "Units": ['none', 'none', mark_safe('mol/m<sup>3</sup>'),mark_safe('cm<sup>3</sup>/g'),mark_safe('g/cm<sup>3</sup>'),mark_safe('mol/m<sup>3</sup>'),'g/mol',mark_safe('kg/m<sup>3</sup>'),],
    }
    return data

def table_all_batch(pvuheadings, sumheadings, tmpl,earthworm_obj):
    html_all = table_1batch(pvuheadings, tmpl, earthworm_obj)
    html_all = html_all + table_2(earthworm_obj)
    return html_all

def table_all_sum(sumheadings, tmpl, Kow, L, Cs, Kd, Ps, Cw, MW, Pe,Ce_out):
    html_all_sum = table_sum_input(sumheadings, tmpl, Kow, L, Cs, Kd, Ps, Cw, MW, Pe)
    html_all_sum += table_sum_output(sumheadings, tmpl, Ce_out)
    return html_all_sum

def table_sum_input(sumheadings, tmpl, Kow, L, Cs, Kd, Ps, Cw, MW, Pe):
        #pre-table sum_input
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsuminputdata = gettsumdata(Kow, L, Cs, Kd, Ps, Cw, MW, Pe)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        html = html + """
                </div>
        """
        return html

def table_sum_output(sumheadings, tmpl, Ce_out):

        #pre-table sum_input
        html = """
        <br>
            <H4 class="out_1 collapsible" id="section3"><span></span>Earthworm Fagacity Model Batch Outputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(Ce_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html