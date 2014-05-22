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

def gett1data(vvwm_obj, i):
    data = {
        "Parameter": ["Peak 1-in-10", "Chronic 1-in-10", "Simulation Avg", "4-day Avg", "21-day Avg", "60-day Avg", "90-day Avg"],
        "Value": [vvwm_obj.WC_peak[i], vvwm_obj.WC_chronic[i], vvwm_obj.WC_simavg[i], vvwm_obj.WC_4dayavg[i], vvwm_obj.WC_21dayavg[i], vvwm_obj.WC_60dayavg[i], vvwm_obj.WC_90dayavg[i]]
    }
    return data

def gett2data(vvwm_obj, i):
    data = {
        "Parameter": ["Benthic Pore Water Peak 1-in-10", "Benthic Pore Water 21-day avg 1-in-10", "Benthic Conversion Factor", "Sediment Bioavailable Fraction"],
        "Value": [vvwm_obj.Ben_peak[i], vvwm_obj.Ben_21dayavg[i], vvwm_obj.Ben_convfact[i], vvwm_obj.Ben_massfract[i]]
    }
    return data

def gett3data(vvwm_obj, i):
    data = {
        "Parameter": ["Washout", "Metabolism", "Hydrolysis", "Photolysis", "Volatilization", "Total"],
        "Value": [vvwm_obj.EWCH_washout[i], vvwm_obj.EWCH_metabolism[i], vvwm_obj.EWCH_hydrolysis[i], vvwm_obj.EWCH_photolysis[i], vvwm_obj.EWCH_volatilization[i], vvwm_obj.EWCH_total[i]]
    }
    return data

def gett4data(vvwm_obj, i):
    data = {
        "Parameter": ["Burial", "Metabolism", "Hydrolysis", "Total"],
        "Value": [vvwm_obj.EBH_burial[i], vvwm_obj.EBH_metabolism[i], vvwm_obj.EBH_hydrolysis[i], vvwm_obj.EBH_total[i]]
    }
    return data

def gett5data(vvwm_obj, i):
    data = {
        "Parameter": ["Runoff", "Erosion", "Drift"],
        "Value": [vvwm_obj.RT_runoff[i], vvwm_obj.RT_erosion[i], vvwm_obj.RT_drift[i]]
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
    templatepath = os.path.dirname(__file__) + '/../templates/'
    if vvwm_obj.vvwmSimType == '0':
        html_plot1 = template.render(templatepath + 'vvwm-output-jqplot.html', {'plotNumber':1, 'title':'Pond'})
        html_plot2 = template.render(templatepath + 'vvwm-output-jqplot2.html', {'plotNumber':2, 'title':'Reservoir'})
        html_all = timestamp(vvwm_obj) + table_1() + table_7(vvwm_obj) + table_2(vvwm_obj, 0) + table_3(vvwm_obj, 0) + table_4(vvwm_obj, 0) + table_5(vvwm_obj, 0) + table_6(vvwm_obj, 0) + table_8a(vvwm_obj, 0) + table_8b(vvwm_obj, 0) + html_plot1 + table_2(vvwm_obj, 1) + table_3(vvwm_obj, 1) + table_4(vvwm_obj, 1) + table_5(vvwm_obj, 1) + table_6(vvwm_obj, 1) + table_8a2(vvwm_obj, 1) + table_8b(vvwm_obj, 1) + html_plot2
    else:
        if vvwm_obj.vvwmSimType == '5':
            plotTitle = 'Pond'
        elif vvwm_obj.vvwmSimType == '4':
            plotTitle = 'Reservoir'
        elif vvwm_obj.vvwmSimType == '6' or vvwm_obj.vvwmSimType == '1' or vvwm_obj.vvwmSimType == '2' or vvwm_obj.vvwmSimType == '3':
            plotTitle = 'Custom'
        html_plot = template.render(templatepath + 'vvwm-output-jqplot.html', {'plotNumber':1, 'title':plotTitle})
        html_all = timestamp(vvwm_obj) + table_1() + table_7(vvwm_obj) + table_2(vvwm_obj, 0) + table_3(vvwm_obj, 0) + table_4(vvwm_obj, 0) + table_5(vvwm_obj, 0) + table_6(vvwm_obj, 0) + table_8a(vvwm_obj, 0) + table_8b(vvwm_obj, 0) + html_plot
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
                        <th colspan="2">Output File</div></th>
                    </tr>
                    <tr>
                        <td>Simulation is finished. Please download your file from here</td>
                        <td><a href=%s>Link</a></td>
                    </tr>
                </table>
            </div>
    </div>"""%(vvwm_obj.link)
    return html

def table_2(vvwm_obj, i):
    if vvwm_obj.vvwmSimType == '5':
        vvwmSimType_text = 'Pond'
    elif vvwm_obj.vvwmSimType == '4':
        vvwmSimType_text = 'Reservoir'
    elif vvwm_obj.vvwmSimType == '6' or vvwm_obj.vvwmSimType == '1' or vvwm_obj.vvwmSimType == '2' or vvwm_obj.vvwmSimType == '3':
        vvwmSimType_text = 'Custom'
    elif vvwm_obj.vvwmSimType == '0':
        if i == 0:
            vvwmSimType_text = 'Pond'
        if i == 1:
            vvwmSimType_text = 'Reservoir'
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section3"><span></span>VVWM Output: %s</H3>
    <div class="out_1">
        <H4 class="out_1 collapsible" id="section4"><span></span>Water Column 1-in-10 Year Concentration (ppb)</H4>
            <div class="out_ container_output">
    """%(vvwmSimType_text)
    t1data = gett1data(vvwm_obj, i)
    t1rows = gethtmlrowsfromcols(t1data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_3(vvwm_obj, i):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Benthic 1-in-10 Year Concentration (ppb)</H4>
            <div class="out_ container_output">
    """
    t2data = gett2data(vvwm_obj, i)
    t2rows = gethtmlrowsfromcols(t2data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t2rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_4(vvwm_obj, i):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Effective Water Column Halflives (day)</H4>
            <div class="out_ container_output">
    """
    t3data = gett3data(vvwm_obj, i)
    t3rows = gethtmlrowsfromcols(t3data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_5(vvwm_obj, i):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Effective Benthic Halflives (day)</H4>
            <div class="out_ container_output">
    """
    t4data = gett4data(vvwm_obj, i)
    t4rows = gethtmlrowsfromcols(t4data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvheadings)))
    html = html + """
            </div>
    """
    return html

def table_6(vvwm_obj, i):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span>Relative Transport</H4>
            <div class="out_ container_output">
    """
    t5data = gett5data(vvwm_obj, i)
    t5rows = gethtmlrowsfromcols(t5data,pvheadings)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvheadings)))
    html = html + """
            </div>
    </div>
    """
    return html

def table_8a(vvwm_obj, i):
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
        </div>"""%(i+1, vvwm_obj.peak_li1, i+1, vvwm_obj.ben_peak_li1)
    return html

def table_8a2(vvwm_obj, i):
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
        </div>"""%(i+1, vvwm_obj.peak_li2, i+1, vvwm_obj.ben_peak_li2)
    return html

def table_8b(vvwm_obj, i):
    html = """
    <br>
    <H3 class="out_3 collapsible" id="section1"><span></span>Plots</H3>
        <div class="out_3">
            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                <div id="chart%s" style="margin-top:20px; margin-left:20px; width:600px; height:400px;">
                </div>
        </div>"""%(i+1)
    return html

