import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from agdrift import agdrift_model
from agdrift import agdrift_parameters
import time
import datetime
import logging
from google.appengine.ext.webapp import template
import os


logger = logging.getLogger("AgdriftTables")

def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvr():
    headings = ["Parameter", "Value"]
    return headings

def getheadersum():     
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
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
        "Parameter": ['Spray drift fraction of applied', 'Initial Average Deposition (g/ha)', 'Initial Average Deposition (lb/ac)', 'Initial Average Concentration (ng/L)', 'Initial Average Deposition (mg/cm2)', 'Distance to Point or Waterbody (ft)',],
        # "Value": ['%.3f' % agdrift_obj.init_avg_dep_foa,'%.3f' % agdrift_obj.avg_depo_gha,'%.3f' % agdrift_obj.avg_depo_lbac, '%.3f' % agdrift_obj.deposition_ngL, '%.3f' % agdrift_obj.deposition_mgcm,],
        "Value": ['%.5f' % agdrift_obj.init_avg_dep_foa,'%.5f' % agdrift_obj.avg_depo_gha,'%.5f' % agdrift_obj.avg_depo_lbac, '%.5f' % agdrift_obj.deposition_ngL, '%.5f' % agdrift_obj.deposition_mgcm, '%.d' % int(agdrift_obj.distance),],
    }
    return data

def gettsumdata(application_rate,distance):
    data = { 
        "Parameter": ['Application rate','Distance',],
        "Mean": ['%.2e' % numpy.mean(application_rate),'%.2e' % numpy.mean(distance),],
        "Std": ['%.2e' % numpy.std(application_rate),'%.2e' % numpy.std(distance),],
        "Min": ['%.2e' % numpy.min(application_rate),'%.2e' % numpy.min(distance),],        
        "Max": ['%.2e' % numpy.max(application_rate),'%.2e' % numpy.max(distance),], 
        "Unit": ['lb/ac', 'm',],
    }
    return data

#def gettsumdata_out(init_avg_dep_foa,avg_depo_lbac,avg_depo_gha,deposition_ngL,deposition_mgcm,nasae,y,x,express_y):
def gettsumdata_out(init_avg_dep_foa_out,avg_depo_lbac_out,avg_depo_gha_out,deposition_ngL_out,deposition_mgcm_out,nasae_out,y_out,x_out,express_y_out):
    data = { 
        "Parameter": ['Average deposition','Deposition (lb/ac)', 'Deposition (g/ha)','Deposition (ng/L)','Deposition (mg/cm)','NASAE','Y','X','Express_Y'],                 
        "Mean": ['%.2e' % numpy.mean(init_avg_dep_foa_out),'%.2e' % numpy.mean(avg_depo_lbac_out),'%.2e' % numpy.mean(avg_depo_gha_out),
        '%.2e' % numpy.mean(deposition_ngL_out),'%.2e' % numpy.mean(deposition_mgcm_out),'%.2e' % numpy.mean(nasae_out),'%.2e' % numpy.mean(y_out),
        '%.2e' % numpy.mean(x_out),'%.2e' % numpy.mean(express_y_out),],
        "Std": ['%.2e' % numpy.std(init_avg_dep_foa_out),'%.2e' % numpy.std(avg_depo_lbac_out),'%.2e' % numpy.std(avg_depo_gha_out),
        '%.2e' % numpy.std(deposition_ngL_out),'%.2e' % numpy.std(deposition_mgcm_out),'%.2e' % numpy.std(nasae_out),'%.2e' % numpy.std(y_out),
        '%.2e' % numpy.std(x_out),'%.2e' % numpy.std(express_y_out),],
        "Min": ['%.2e' % numpy.min(init_avg_dep_foa_out),'%.2e' % numpy.min(avg_depo_lbac_out),'%.2e' % numpy.min(avg_depo_gha_out),
        '%.2e' % numpy.min(deposition_ngL_out),'%.2e' % numpy.min(deposition_mgcm_out),'%.2e' % numpy.min(nasae_out),'%.2e' % numpy.min(y_out),
        '%.2e' % numpy.min(x_out),'%.2e' % numpy.min(express_y_out),],
        "Max": ['%.2e' % numpy.max(init_avg_dep_foa_out),'%.2e' % numpy.max(avg_depo_lbac_out),'%.2e' % numpy.max(avg_depo_gha_out),
        '%.2e' % numpy.max(deposition_ngL_out),'%.2e' % numpy.max(deposition_mgcm_out),'%.2e' % numpy.max(nasae_out),'%.2e' % numpy.max(y_out),
        '%.2e' % numpy.max(x_out),'%.2e' % numpy.max(express_y_out),],   
        "Unit": ['lb/ac', 'm','','','','',''],
    }
    return data        

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# pvrheadingsqaqc = getheaderpvrqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(agdrift_obj):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_all = table_1(agdrift_obj)     
    html_all = html_all + table_2(agdrift_obj)
    html_all = html_all + table_3(agdrift_obj)
    html_all = html_all + template.render(templatepath + 'agdrift-output-jqplot.html', {'chart_num':agdrift_obj.loop_indx})
    return html_all

def timestamp(agdrift_obj="", batch_jid=""):
    #ts = time.time()
    #st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    if agdrift_obj:
        st = datetime.datetime.strptime(agdrift_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
    <b>agdrift Version 0.1 (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
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
                <td id="distance%s">%s</td>
            </tr>
            <tr>
                <td>deposition</td>
                <td id="deposition%s">%s</td>
            </tr>
        </table>
        <br>
        <h3 class="out_2 collapsible" id="section2"><span></span>Results</h3>
            <H4 class="out_2 collapsible" id="section3"><span></span>Plot of spray drift</H4>
                <div class="out_">
        """%(agdrift_obj.loop_indx, agdrift_obj.x, agdrift_obj.loop_indx, agdrift_obj.express_y)
        # t2data = gett2data(agdrift_obj)
        # t2rows = gethtmlrowsfromcols(t2data,pvrheadings)
        # html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        # html = html + """
        #         </div>
        # """
        return html

def table_sum_input(i,application_rate,distance):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><td><H3>Summary Statistics (Iterations=%s)</H3></td></tr>
        <tr></tr>
        </table>
        """%(i-1)
        #table sum_input
        tsuminputdata = gettsumdata(application_rate,distance)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html

def table_sum_output(init_avg_dep_foa_out,avg_depo_lbac_out,avg_depo_gha_out,deposition_ngL_out,deposition_mgcm_out,nasae_out,y_out,x_out,express_y_out):

        #pre-table sum_input
        html = """
        <br>
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(init_avg_dep_foa_out,avg_depo_lbac_out,avg_depo_gha_out,deposition_ngL_out,deposition_mgcm_out,nasae_out,y_out,x_out,express_y_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        return html   




