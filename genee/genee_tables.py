import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from geneec import geneec_model
import time
import datetime

def getheaderpvu():
  headings = ["Parameter", "Value", "Units"]
  return headings

def getheaderpvuqaqc():
  headings = ["Parameter", "Value", "Expected Value", "Units"]
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
            <th colspan={{ th_span|default:'1' }}>{{ heading }}</th>
        {% endfor %}
        </tr>
    
    {% if sub_headings %}
        <tr>
        {% for sub_heading in sub_headings %}
            <th>{{ sub_heading }}</th>
        {% endfor %}
        </tr>
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
 
def gett2data(geneec_obj):
    data = { 
        "Parameter": [ 'Peak GEEC','Maximum 4-day Average GEEC','Maximum 21-day Average GEEC','Maximum 60-day Average GEEC','Maximum 90-day Average GEEC' ],
        "Value": [ '%.1f'%geneec_obj.output_val[0], '%.1f'%geneec_obj.output_val[1], '%.1f'%geneec_obj.output_val[2], '%.1f'%geneec_obj.output_val[3], '%.1f'%geneec_obj.output_val[4] ],
        "Units": [ 'ppb','ppb','ppb','ppb','ppb' ]
    }
    return data

def gett2data_qaqc(geneec_obj):
    data = { 
        "Parameter": [ 'Peak GEEC','Maximum 4-day Average GEEC','Maximum 21-day Average GEEC','Maximum 60-day Average GEEC','Maximum 90-day Average GEEC' ],
        "Value": [ '%.1f'%geneec_obj.output_val[0], '%.1f'%geneec_obj.output_val[1], '%.1f'%geneec_obj.output_val[2], '%.1f'%geneec_obj.output_val[3], '%.1f'%geneec_obj.output_val[4] ],
        "Expected Value": [ '%.1f'%geneec_obj.GEEC_peak_exp, '%.1f'%geneec_obj.GEEC_4avg_exp, '%.1f'%geneec_obj.GEEC_21avg_exp, '%.1f'%geneec_obj.GEEC_60avg_exp, '%.1f'%geneec_obj.GEEC_90avg_exp ],
        "Units": [ 'ppb','ppb','ppb','ppb','ppb' ]
    }
    return data

pvuheadings = getheaderpvu()
pvuheadingsqaqc = getheaderpvuqaqc()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(geneec_obj):
    table1_out = table_1()
    table2_out = table_2(geneec_obj)
    html_all = table1_out + table2_out
    return html_all

def table_all_qaqc(geneec_obj):
    table1_out = table_1_qaqc(geneec_obj)
    table2_out = table_2_qaqc(geneec_obj)
    html_all = table1_out + table2_out
    return html_all

def timestamp(geneec_obj):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>GENEEC Version 2.0 (Beta)<br>
        <b>jid=%s<b><br>
        <b>Computing Time = %.8ss<b><br>
    """%(geneec_obj.jid, geneec_obj.elapsed)
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html


def table_1():
    html = """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                <div class="out_input_table out_">
                </div>"""
    html = html + """<script>
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
                    </script>"""
    return html


def table_1_qaqc(geneec_obj):
        t1data = gett1dataAerial_qaqc(geneec_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties: %s</H4>
                <div class="out_ container_output">
        """%geneec_obj.application_method_label
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html

def table_2(geneec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
            <H4 class="out_2 collapsible" id="section3"><span></span>Generic Expected Environmental Concentration (GEEC)</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data(geneec_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2_qaqc(geneec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
            <H4 class="out_2 collapsible" id="section3"><span></span>Generic Expected Environmental Concentration (GEEC)</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data_qaqc(geneec_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

