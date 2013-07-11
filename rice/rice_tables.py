import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
import time
import datetime

logger = logging.getLogger("RiceTables")

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvuqaqc():
    headings = ["Parameter", "Value", "Expected-Value", "Units"]
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

def gett1data(rice_obj):
    data = { 
        "Parameter": ['Chemical Name','Mass applied to patty','Area of patty','Sediment Depth',mark_safe('Sediment bulk density, &#961;<sub>b</sub>'),'Water column depth',mark_safe('Sediment porosity, K<sub>d</sub>'), mark_safe('Water-Sediment partitioning coefficient, K<sub>d</sub>')],
        "Value": ['%s' % rice_obj.chemical_name, '%.4f' % rice_obj.mai, '%.2f' % rice_obj.a, '%.2f' % rice_obj.dsed, '%.2f' % rice_obj.pb, '%.2f' % rice_obj.dw, '%.4f' % rice_obj.osed, '%.2f' % rice_obj.kd],
        "Units": ['','kg',mark_safe('m<sup>2</sup>'),'m',mark_safe('kg/m<sup>3</sup>'),'m','','L/kg'],
    }
    return data

def gett1dataqaqc(rice_obj):
    data = { 
        "Parameter": ['Chemical Name','Mass applied to patty','Area of patty','Sediment Depth',mark_safe('Sediment bulk density, &#961;<sub>b</sub>'),'Water column depth',mark_safe('Sediment porosity, K<sub>d</sub>'), mark_safe('Water-Sediment partitioning coefficient, K<sub>d</sub>')],
        "Value": [rice_obj.chemical_name,rice_obj.mai,rice_obj.a,rice_obj.dsed,rice_obj.pb,rice_obj.dw,rice_obj.osed,rice_obj.kd],
        "Expected-Value": [rice_obj.chemical_name_expected,rice_obj.mai,rice_obj.a,rice_obj.dsed,rice_obj.pb,rice_obj.dw,rice_obj.osed,rice_obj.kd],
        "Units": ['','kg',mark_safe('m<sup>2</sup>'),'m',mark_safe('kg/m<sup>3</sup>'),'m','','L/kg'],
    }
    return data

def gett2data(rice_obj):
    data = { 
        "Parameter": ['Sediment Mass', 'Water Column Volume', 'Mass per unit area', 'Water Concentration',],
        "Value": ['%.2f' % rice_obj.msed, '%.2f' % rice_obj.vw, '%.4f' % rice_obj.mai1, '%.4f' % rice_obj.cw,],
        "Units": ['kg', mark_safe('m<sup>3</sup>'), 'kg/ha', mark_safe('&#956;g/L'),],
    }
    return data

def gett2dataqaqc(rice_obj):
    data = { 
        "Parameter": ['Sediment Mass', 'Water Column Volume', 'Mass per unit area', 'Water Concentration',],
        "Value": ['%.2f' % rice_obj.msed, '%.2f' % rice_obj.vw, '%.4f' % rice_obj.mai1, '%.4f' % rice_obj.cw,],
        "Expected-Value": ['%.2f' % rice_obj.msed_expected, '%.2f' % rice_obj.vw_expected, '%.4f' % rice_obj.mai1_expected, '%.4f' % rice_obj.cw_expected,],
        "Units": ['kg', mark_safe('m<sup>3</sup>'), 'kg/ha', mark_safe('&#956;g/L'),],
    }
    return data

def gettsumdata(mai, dsed, a, pb, dw, osed, kd):
    data = {
        "Parameter": ['Mass applied to patty','Area of patty','Sediment Depth',mark_safe('Sediment bulk density, &#961;<sub>b</sub>'),'Water column depth',mark_safe('Sediment porosity, K<sub>d</sub>'), mark_safe('Water-Sediment partitioning coefficient, K<sub>d</sub>')],
        "Mean": ['%.2e' % numpy.mean(mai),'%.2e' % numpy.mean(dsed),'%.2e' % numpy.mean(a), '%.2e' % numpy.mean(pb), 
                 '%.2e' % numpy.mean(dw), '%.2e' % numpy.mean(osed), '%.2e' % numpy.mean(kd)],
        "Std": ['%.2e' % numpy.std(mai),'%.2e' % numpy.std(dsed),'%.2e' % numpy.std(a), '%.2e' % numpy.std(pb), 
                '%.2e' % numpy.std(dw), '%.2e' % numpy.std(osed), '%.2e' % numpy.std(kd)],
        "Min": ['%.2e' % numpy.min(mai),'%.2e' % numpy.min(dsed),'%.2e' % numpy.min(a), '%.2e' % numpy.min(pb), 
                '%.2e' % numpy.min(dw), '%.2e' % numpy.min(osed), '%.2e' % numpy.min(kd)],
         "Max": ['%.2e' % numpy.max(mai),'%.2e' % numpy.max(dsed),'%.2e' % numpy.max(a), '%.2e' % numpy.max(pb), 
                '%.2e' % numpy.max(dw), '%.2e' % numpy.max(osed), '%.2e' % numpy.max(kd)],
        "Unit": ['kg',mark_safe('m<sup>2</sup>'),'m',mark_safe('kg/m<sup>3</sup>'),'m','','L/kg'],
    }
    return data

def gettsumdata_out(msed, vw, mai1, cw):
    data = {
        "Parameter": ['Sediment Mass', 'Water Column Volume', 'Mass per unit area', 'Water Concentration',],
        "Mean": ['%.2e' % numpy.mean(msed),'%.2e' % numpy.mean(vw),'%.2e' % numpy.mean(mai1), '%.2e' % numpy.mean(cw)],
        "Std": ['%.2e' % numpy.std(msed),'%.2e' % numpy.std(vw),'%.2e' % numpy.std(mai1), '%.2e' % numpy.std(cw)],
        "Min": ['%.2e' % numpy.min(msed),'%.2e' % numpy.min(vw),'%.2e' % numpy.min(mai1), '%.2e' % numpy.min(cw)],
         "Max": ['%.2e' % numpy.max(msed),'%.2e' % numpy.max(vw),'%.2e' % numpy.max(mai1), '%.2e' % numpy.max(cw)],
        "Unit": ['kg', mark_safe('m<sup>3</sup>'), 'kg/ha', mark_safe('&#956;g/L'),],
    }
    return data

pvuheadings = getheaderpvu()
pvuheadingsqaqc = getheaderpvuqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(rice_obj):
   
    html_all = table_1(rice_obj)      
    html_all = html_all + table_2(rice_obj)

    return html_all

def table_all_qaqc(rice_obj):
   
    html_all = table_1_qaqc(rice_obj)
    html_all = html_all + table_2_qaqc(rice_obj)

    return html_all

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Tier 1 Rice Model (Version 1.0)<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_1(rice_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Model Inputs</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(rice_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_1_qaqc(rice_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Model Inputs</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1dataqaqc(rice_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(rice_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Rice Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Model Output</H4>
                <div class="out_ container_output">
        """
        #table 1
        t2data = gett2data(rice_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2_qaqc(rice_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Rice Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Model Output</H4>
                <div class="out_ container_output">
        """
        #table 1
        t2data = gett2dataqaqc(rice_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_sum_all(sumheadings, tmpl, mai, dsed, a, pb, dw, osed, kd, msed, vw, mai1, cw):
    html_all_sum = table_sum_input(sumheadings, tmpl, mai, dsed, a, pb, dw, osed, kd)
    html_all_sum += table_sum_output(sumheadings, tmpl, msed, vw, mai1, cw)
    return html_all_sum

def table_sum_input(sumheadings, tmpl, mai, dsed, a, pb, dw, osed, kd):
    #pre-table sum_input
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsuminputdata = gettsumdata(mai, dsed, a, pb, dw, osed, kd)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def table_sum_output(sumheadings, tmpl, msed, vw, mai1, cw):
    #pre-table sum_input
        html = """
        <br>
            <H4 class="out_1 collapsible" id="section3"><span></span>Rice Model Outputs</H4>
                <div class="out_ container_output">
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(msed, vw, mai1, cw)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html