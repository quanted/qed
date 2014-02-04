from django.template import Context, Template
from django.utils.safestring import mark_safe
from vvwm import vvwm_model
import time
import datetime
import os
from google.appengine.ext.webapp import template

def getheaderpv():
    headings = ["Parameter", "Value"]
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

def gett1data(vvwm_obj):
    data = {
        "Parameter": ["Peak 1-in-10", "Chronic 1-in-10", "Simulation Avg", "4-day Avg", "21-day Avg", "60-day Avg", "90-day Avg"],
        "Value": [vvwm_obj.WC_peak[0], vvwm_obj.WC_chronic[0], vvwm_obj.WC_simavg[0], vvwm_obj.WC_4dayavg[0], vvwm_obj.WC_21dayavg[0], vvwm_obj.WC_60dayavg[0], vvwm_obj.WC_90dayavg[0]]
    }
    return data

def gett2data(vvwm_obj):
    data = {
        "Parameter": ["Benthic Pore Water Peak 1-in-10", "Benthic Pore Water 21-day avg 1-in-10", "Benthic Conversion Factor", "Sediment Bioavailable Fraction"],
        "Value": [vvwm_obj.Ben_peak[0], vvwm_obj.Ben_21dayavg[0], vvwm_obj.Ben_convfact[0], vvwm_obj.Ben_massfract[0]]
    }
    return data

def gett3data(vvwm_obj):
    data = {
        "Parameter": ["Washout", "Metabolism", "Hydrolysis", "Photolysis", "Volatilization", "Total"],
        "Value": [vvwm_obj.EWCH_washout[0], vvwm_obj.EWCH_metabolism[0], vvwm_obj.EWCH_hydrolysis[0], vvwm_obj.EWCH_photolysis[0], vvwm_obj.EWCH_volatilization[0], vvwm_obj.EWCH_total[0]]
    }
    return data

def gett4data(vvwm_obj):
    data = {
        "Parameter": ["Burial", "Metabolism", "Hydrolysis", "Total"],
        "Value": [vvwm_obj.EBH_burial[0], vvwm_obj.EBH_metabolism[0], vvwm_obj.EBH_hydrolysis[0], vvwm_obj.EBH_total[0]]
    }
    return data

def gett5data(vvwm_obj):
    data = {
        "Parameter": ["Runoff", "Erosion", "Drift"],
        "Value": [vvwm_obj.RT_runoff[0], vvwm_obj.RT_erosion[0], vvwm_obj.RT_drift[0]]
    }
    return data

pvheadings = getheaderpv()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def timestamp(vvwm_obj):
    # ts = time.time()
    # st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    st = datetime.datetime.strptime(vvwm_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A %Y-%m-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>VVWM<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


def table_all(vvwm_obj):
    table1_out = table_1()
    table2_out = table_2(vvwm_obj)
    table3_out = table_3(vvwm_obj)
    table4_out = table_4(vvwm_obj)
    table5_out = table_5(vvwm_obj)
    table6_out = table_6(vvwm_obj)
    table7_out = table_7(vvwm_obj)
    table8a_out = table_8a(vvwm_obj)
    table8b_out = table_8b(vvwm_obj)
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_plot = template.render(templatepath + 'vvwm-output-jqplot.html', {})
    html_all = timestamp(vvwm_obj) + table1_out + table7_out + table2_out + table3_out + table4_out + table5_out + table6_out + table8a_out + table8b_out + html_plot
    return html_all


def table_1():
    html = """
    <H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_input_table out_">

    </div>"""
    return html

def table_7(vvwm_obj):
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section3"><span></span>VVWM Output Files</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section1"><span></span>Download</H4>
            <div class="out_ container_output">
                <table class="out_">
                    <tr>
                        <th scope="col">Outputs</div></th>
                        <th scope="col">Value</div></th>                            
                    </tr>
                    <tr>
                        <td>Simulation is finished. Please download your file from here</td>
                        <td><a href=%s>Link</a></td>
                    </tr>
                </table>
            </div>
    </div>"""%(vvwm_obj.link)
    return html

def table_2(vvwm_obj):
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section3"><span></span>VVWM Output: Pond</H3>
    <div class="out_1">
        <H4 class="out_1 collapsible" id="section4"><span></span>Water Column 1-in-10 Year Concentration (ppb)</H4>
            <div class="out_ container_output">
    """
    t1data = gett1data(vvwm_obj)
    t1rows = gethtmlrowsfromcols(t1data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_3(vvwm_obj):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Benthic 1-in-10 Year Concentration (ppb)</H4>
            <div class="out_ container_output">
    """
    t2data = gett2data(vvwm_obj)
    t2rows = gethtmlrowsfromcols(t2data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t2rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_4(vvwm_obj):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Effective Water Column Halflives (day)</H4>
            <div class="out_ container_output">
    """
    t3data = gett3data(vvwm_obj)
    t3rows = gethtmlrowsfromcols(t3data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_5(vvwm_obj):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Effective Benthic Halflives (day)</H4>
            <div class="out_ container_output">
    """
    t4data = gett4data(vvwm_obj)
    t4rows = gethtmlrowsfromcols(t4data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_6(vvwm_obj):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Relative Transport</H4>
            <div class="out_ container_output">
    """
    t5data = gett5data(vvwm_obj)
    t5rows = gethtmlrowsfromcols(t5data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvheadings)))
    html = html + """
            </div>
    </div>
    """
    return html

def table_8a(vvwm_obj):
    html = """
    <H4 class="out_4 collapsible" id="section1" style="display: none"><span></span>Plot</H4>
        <div class="out_4 container_output">
            <table class="out_" style="display: none">
                <tr>
                    <td id="x_wc">wc</td>
                    <td id="x_wc_val_%s">%s</td>
                </tr>
                <tr>
                    <td id="x_ben">ben</td>
                    <td id="x_ben_val_%s">%s</td>
                </tr>
            </table>
        </div>"""%(1, vvwm_obj.peak_li, 1, vvwm_obj.ben_peak_li)
    return html

def table_8b(vvwm_obj):
    html = """
    <br>
    <H3 class="out_3 collapsible" id="section1"><span></span>Plots</H3>
        <div class="out_3">
            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                <div id="chart1" style="margin-top:20px; margin-left:20px; width:600px; height:400px;">
                </div>
        </div>"""
    return html

