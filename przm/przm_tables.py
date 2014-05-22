import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from przm import przm_model
import time
import datetime
import os
from google.appengine.ext.webapp import template

def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvu2():
    headings = ["Parameter", "Value", "Units"]
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
 
def gett1data(przm_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Standard OPP/EFED Scenarios', 'Weather station', 'Met filename',
                      'INP filename', 'RUN filename', 'Number of applications',],
        "Value": ['%s' % przm_obj.chemical_name, przm_obj.Scenarios, '%s' % przm_obj.station, '%s' % przm_obj.met_o,
                  '%s' % przm_obj.inp_o, '%s' % przm_obj.run_o, '%s' % przm_obj.NOA,],
    }
    return data

def gett2data(przm_obj, i):
    data = { 
        "Parameter": ['Application timing', 'Days relevant to the application', 'Application method', 'Application rate',
                      'Chemical application Method', 'Efficiency', 'Drift pond', 'Incorporation depth (DEPI)',],
        "Value": ['%s' % przm_obj.Apt_p[i], przm_obj.DayRe_l[i], '%s' % przm_obj.Ap_mp[i], '%s' % przm_obj.Ar_l[i],
                  '%s' % przm_obj.CAM_f_p[i], '%s' % przm_obj.EFF_p[i], '%s' % przm_obj.Drft_p[i], '%s' % przm_obj.DEPI_p[i],],
        "Units": ['', 'days', '', 'kg/ha', '', '', '', 'cm'],
    }
    return data

pvuheadings = getheaderpvu()
pvuheadings2 = getheaderpvu2()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(przm_obj):
    table1_out = table_1(przm_obj)
    table2_out = table_2(przm_obj)
    table3_out = table_3(przm_obj)
    table4_out = table_4(przm_obj)
    table5_out = table_5(przm_obj)
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_plot = template.render(templatepath + 'przm-output-jqplot.html', {'model_index': przm_obj.iter_index, 
                                                                           'plot_index1': 2*przm_obj.iter_index+1, 
                                                                           'plot_index2': 2*przm_obj.iter_index+2})
    html_all = table1_out + table2_out + table3_out + table4_out + table5_out + html_plot
    return html_all


def timestamp(przm_obj="", batch_jid=""):
    if przm_obj:
        st = datetime.datetime.strptime(przm_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>PRZM<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_1(przm_obj):
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section1"><span></span>Profile</H4>
            <div class="out_ container_output">
    """
    t1data = gett1data(przm_obj)
    t1rows = gethtmlrowsfromcols(t1data, pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
    </div>
    """
    return html

def table_2(przm_obj):
    html_table2 = """"""
    for i in range(przm_obj.NOA):
        html = """
            <H4 class="out_2 collapsible" id="section2"><span></span>Application %s</H4>
                <div class="out_ container_output">
        """%(i+1)
        t2data = gett2data(przm_obj, i)
        t2rows = gethtmlrowsfromcols(t2data, pvuheadings2)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings2))) + """</div>"""
        html_table2 = html_table2 + html
    return html_table2

def table_3(przm_obj):
    html = """
    <H3 class="out_3 collapsible" id="section1"><span></span>User Outputs</H3>
    <div class="out_3">
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
    </div>"""%(przm_obj.link)
    return html

def table_4(przm_obj):
    html = """
        <H4 class="out_4 collapsible" id="section1" style="display: none"><span></span>Plot</H4>
            <div class="out_4 container_output">
                <table class="out_" style="display: none">
                    <tr>
                        <td id="x_pre_irr">pre+irr</td>
                        <td id="x_pre_irr_val_%s">%s</td>
                    </tr>
                    <tr>
                        <td id="x_leachate">leachate</td>
                        <td id="x_leachate_val_%s">%s</td>
                    </tr>                          
                    <tr>
                        <td id="x_et">et</td>
                        <td id="x_et_val_%s">%s</td>
                    </tr>
                    <tr>
                        <td id="x_runoff">runoff</td>
                        <td id="x_runoff_val_%s">%s</td>
                    </tr>                          
                </table>
            </div>"""%(przm_obj.iter_index, przm_obj.x_pre_irr, przm_obj.iter_index, przm_obj.x_leachate, przm_obj.iter_index, przm_obj.x_et, przm_obj.iter_index, przm_obj.x_runoff)
    return html

def table_5(przm_obj):
    html = """
        <H3 class="out_3 collapsible" id="section1"><span></span>Plots</H3>
            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                <div id="chart%s" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                <div id="chart%s" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
        """%((2*przm_obj.iter_index+1), (2*przm_obj.iter_index+2))
    return html

