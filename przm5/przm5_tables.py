from django.template import Context, Template
from django.utils.safestring import mark_safe
from przm5 import przm5_model
import time
import datetime
import os
from google.appengine.ext.webapp import template

def timestamp(przm5_obj):
    # ts = time.time()
    # st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    st = datetime.datetime.strptime(przm5_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A %Y-%m-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>PRZM<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


def table_all(przm5_obj):
    table1_out = table_1()
    table2_out = table_2(przm5_obj)
    table3_out = table_3(przm5_obj)
    table4_out = table_4(przm5_obj)
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_plot = template.render(templatepath + 'przm5-output-jqplot.html', {})
    html_all = timestamp(przm5_obj) + table1_out + table2_out + table3_out + table4_out + html_plot
    return html_all


def table_1():
    html = """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                <div class="out_input_table out_">
                </div>"""
    return html

def table_2(przm5_obj):
    html = """  <H3 class="out_3 collapsible" id="section1"><span></span>User Outputs</H3>
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
                </div>"""%(przm5_obj.link)
    return html

def table_3(przm5_obj):
    html = """  <H4 class="out_4 collapsible" id="section1" style="display: none"><span></span>Plot</H4>
                <div class="out_4 container_output">
                    <table class="out_" style="display: none">
                        <tr>
                            <td id="x_pre_irr">pre+irr</td>
                            <td id="x_pre_irr_val_%s">%s</td>
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
                </div>"""%(1, przm5_obj.PRCP_IRRG_sum, 1, przm5_obj.CEVP_TETD_sum, 1, przm5_obj.RUNF_sum)
    return html

def table_4(przm5_obj):
    html = """
            <H3 class="out_3 collapsible" id="section1"><span></span>Plots</H3>
            <div class="out_3">
                <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                    <div id="chart1" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
                <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                    <div id="chart2" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
            </div>
           """
    return html

