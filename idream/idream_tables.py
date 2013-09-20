import numpy
import time, datetime
from django.template import Context, Template
from django.utils.safestring import mark_safe
from idream import idream_model
from idream import idream_parameters
import time
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva():
    headings = ["Subpopulation", "Chronic Exposure (mg/kg/d)"]
    return headings

def getheaderpva2():
    headings = ["Subpopulation", "Acute Exposure (mg/kg/d)"]
    return headings

def getheadersum1():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Units"]
    return headings

def getheadersum2():
    headings = ["Subpopulation", "Mean", "Std", "Min", "Max"]
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
        {% if sub_headings_1 %}
            <tr>
            {% for sub_heading_1 in sub_headings_1 %}
                <th>{{ sub_heading_1|safe }}</th>
            {% endfor %}
            </tr>
        {% endif %}
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



pvuheadings = getheaderpvu()
pvaheadings = getheaderpva()
pva2headings = getheaderpva2()
sumheadings1 = getheadersum1()
sumheadings2 = getheadersum2()

djtemplate = getdjtemplate()

tmpl = Template(djtemplate)


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>IDREAM<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_all(idream_obj):
    if idream_obj.tire == 'Tier 2':
        table1_out=table_1(idream_obj)
        table2_out=table_2(idream_obj)
        table3_out=table_3(idream_obj)

        html = table1_out
        html = html + """
                        <H3 class="out_1 collapsible" id="section1"><span></span>User Outputs:</H3>
                        <div class="out_">
                      """
        html = html + table2_out
        html = html + table3_out
        html = html + """</div>"""

        return html
    else:
        table1_out_3=table_1_3(idream_obj)
        table2_out_3=table_2_3(idream_obj)
        table3_out_3=table_3_3(idream_obj)

        html = table1_out_3
        html = html + """
                        <H3 class="out_1 collapsible" id="section1"><span></span>User Outputs:</H3>
                        <div class="out_">
                      """        
        html = html + table2_out_3
        html = html + table3_out_3
        html = html + """</div>"""
        return html

def gett1data(idream_obj):
    data = { 
        "Parameter": ['Subject active ingredient', 'Product residue', 'In-use active conc',],
        "Value": ['%s' % idream_obj.ai_name, '%s' % idream_obj.prod_re, '%s' % (100*float(idream_obj.ai)),],
        "Units": ['', 'mg/cm<sup>2</sup>', '%',],
        }
    return data

def gett2data(idream_obj):
    data = { 
        "Subpopulation": ['Children 1-2', 'Children 3-5', 'Adults 13+', 'Females 13-49',],
        "Chronic Exposure (mg/kg/d)": ['%.4e' % idream_obj.exp_child_c_1, '%.4e' % idream_obj.exp_child_c_2, '%.4e' % idream_obj.exp_adult_c, '%.4e' % idream_obj.exp_fe_c,],
        }
    return data

def gett3data(idream_obj):
    data = { 
        "Subpopulation": ['Children 1-2', 'Children 3-5', 'Adults 13+', 'Females 13-49',],
        "Acute Exposure (mg/kg/d)": ['%.4e' % idream_obj.exp_child_a_1, '%.4e' % idream_obj.exp_child_a_2, '%.4e' % idream_obj.exp_adult_a, '%.4e' % idream_obj.exp_fe_a,],
        }
    return data

def gett1data_3(idream_obj):
    data = { 
        "Parameter": ['Subject active ingredient', 'Product residue', 'In-use active conc', 'Liquid residue transfer efficiency', 
                      'Fruit residue transfer efficiency', 'Bread residue transfer efficiency', 'Cheese residue transfer efficiency', 
                      'Vegetable residue transfer efficiency ', 'Meat residue transfer efficiency', 'Purees residue transfer efficiency', 
                      'Pieces residue transfer efficiency', 'Powders residue transfer efficiency'],
        "Value": ['%s' % idream_obj.ai_name, '%s' % idream_obj.prod_re, '%s' % (100*float(idream_obj.ai)), '%s' % (100*float(idream_obj.liq_rte)), '%s' % (100*float(idream_obj.fruit_rte)),
                  '%s' % (100*float(idream_obj.bread_rte)), '%s' % (100*float(idream_obj.cheese_rte)), '%s' % (100*float(idream_obj.veg_rte)), '%s' % (100*float(idream_obj.meat_rte)), '%s' % (100*float(idream_obj.pure_rte)),
                  '%s' % (100*float(idream_obj.piec_rte)), '%s' % (100*float(idream_obj.powd_rte)),],
        "Units": ['', 'mg/cm<sup>2</sup>', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%',],
        }
    return data

def gett2data_3(idream_obj):
    data = { 
        "Subpopulation": ['Children 1-2', 'Children 3-5', 'Adults 13+', 'Females 13-49',],
        "Chronic Exposure (mg/kg/d)": ['%.4e' % idream_obj.exp_child_c_1[0], '%.4e' % idream_obj.exp_child_c_2[0], '%.4e' % idream_obj.exp_adult_c[0], '%.4e' % idream_obj.exp_fe_c[0],],
        }
    return data

def gett3data_3(idream_obj):
    data = { 
        "Subpopulation": ['Children 1-2', 'Children 3-5', 'Adults 13+', 'Females 13-49',],
        "Acute Exposure (mg/kg/d)": ['%.4e' % idream_obj.exp_child_a_1, '%.4e' % idream_obj.exp_child_a_2, '%.4e' % idream_obj.exp_adult_a, '%.4e' % idream_obj.exp_fe_a,],
        }
    return data

    
def gettsumdata_1(prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte):
    data = { 
        "Parameter": ['Product residue', 'In-use active conc', 'Liquid residue transfer efficiency', 
                      'Fruit residue transfer efficiency', 'Bread residue transfer efficiency', 'Cheese residue transfer efficiency', 
                      'Vegetable residue transfer efficiency ', 'Meat residue transfer efficiency', 'Purees residue transfer efficiency', 
                      'Pieces residue transfer efficiency', 'Powders residue transfer efficiency'],
        "Mean": ['%.4e' % numpy.mean(prod_re), '%.4e' % numpy.mean(ai), '%.4e' % numpy.mean(liq_rte), '%.4e' % numpy.mean(fruit_rte), '%.4e' % numpy.mean(bread_rte), '%.4e' % numpy.mean(cheese_rte), '%.4e' % numpy.mean(veg_rte), '%.4e' % numpy.mean(meat_rte), '%.4e' % numpy.mean(pure_rte), '%.4e' % numpy.mean(piec_rte), '%.4e' % numpy.mean(powd_rte)],
        "Std": ['%.4e' % numpy.std(prod_re), '%.4e' % numpy.std(ai), '%.4e' % numpy.std(liq_rte), '%.4e' % numpy.std(fruit_rte), '%.4e' % numpy.std(bread_rte), '%.4e' % numpy.std(cheese_rte), '%.4e' % numpy.std(veg_rte), '%.4e' % numpy.std(meat_rte), '%.4e' % numpy.std(pure_rte), '%.4e' % numpy.std(piec_rte), '%.4e' % numpy.std(powd_rte)],
        "Min": ['%.4e' % numpy.min(prod_re), '%.4e' % numpy.min(ai), '%.4e' % numpy.min(liq_rte), '%.4e' % numpy.min(fruit_rte), '%.4e' % numpy.min(bread_rte), '%.4e' % numpy.min(cheese_rte), '%.4e' % numpy.min(veg_rte), '%.4e' % numpy.min(meat_rte), '%.4e' % numpy.min(pure_rte), '%.4e' % numpy.min(piec_rte), '%.4e' % numpy.min(powd_rte)],
        "Max": ['%.4e' % numpy.max(prod_re), '%.4e' % numpy.max(ai), '%.4e' % numpy.max(liq_rte), '%.4e' % numpy.max(fruit_rte), '%.4e' % numpy.max(bread_rte), '%.4e' % numpy.max(cheese_rte), '%.4e' % numpy.max(veg_rte), '%.4e' % numpy.max(meat_rte), '%.4e' % numpy.max(pure_rte), '%.4e' % numpy.max(piec_rte), '%.4e' % numpy.max(powd_rte)],
        "Units": ['mg/cm<sup>2</sup>', '%', '%', '%', '%', '%', '%', '%', '%', '%', '%',],
    }
    return data


def gettsumdata_2(exp_child_c_1_out, exp_child_c_2_out, exp_adult_c_out, exp_fe_c_out):
    data = { 
        "Subpopulation": ['Children 1-2', 'Children 3-5', 'Adults 13+', 'Females 13-49',],
        "Mean": ['%.4e' % numpy.mean(exp_child_c_1_out), '%.4e' % numpy.mean(exp_child_c_2_out), '%.4e' % numpy.mean(exp_adult_c_out), '%.4e' % numpy.mean(exp_fe_c_out)],
        "Std": ['%.4e' % numpy.std(exp_child_c_1_out), '%.4e' % numpy.std(exp_child_c_2_out), '%.4e' % numpy.std(exp_adult_c_out), '%.4e' % numpy.std(exp_fe_c_out)],
        "Min": ['%.4e' % numpy.min(exp_child_c_1_out), '%.4e' % numpy.min(exp_child_c_2_out), '%.4e' % numpy.min(exp_adult_c_out), '%.4e' % numpy.min(exp_fe_c_out)],
        "Max": ['%.4e' % numpy.max(exp_child_c_1_out), '%.4e' % numpy.max(exp_child_c_2_out), '%.4e' % numpy.max(exp_adult_c_out), '%.4e' % numpy.max(exp_fe_c_out)],
    }
    return data

def table_1(idream_obj):
        #pre-table 1
        html = """
            <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs (TIER 2):</H3>
            <div class="out_">
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(idream_obj)
        t1rows = gethtmlrowsfromcols(t1data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
            </div><br>
        """
        return html

def table_1_3(idream_obj):
        #pre-table 1
        html = """
            <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs (TIER 3):</H3>
            <div class="out_ container_output">
        """
        #table 1
        t1data_3 = gett1data_3(idream_obj)
        t1rows_3 = gethtmlrowsfromcols(t1data_3, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows_3, headings=pvuheadings)))
        html = html + """
            </div><br>
        """
        return html

def table_2(idream_obj):
        #pre-table 2
        html = """
            <H4 class="out_ collapsible" id="section2"><span></span>Chronic Assessment</H4>
            <div class="out_ container_output">
        """
        #table 2
        t2data = gett2data(idream_obj)
        t2rows = gethtmlrowsfromcols(t2data, pvaheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings)))
        html = html + """
            </div><br>
        """
        return html

def table_2_3(idream_obj):
        #pre-table 2
        html = """
            <H4 class="out_ collapsible" id="section2"><span></span>Chronic Assessment</H4>
            <div class="out_ container_output">
        """
        #table 2
        t2data_3 = gett2data_3(idream_obj)
        t2rows_3 = gethtmlrowsfromcols(t2data_3, pvaheadings)
        html = html + tmpl.render(Context(dict(data=t2rows_3, headings=pvaheadings)))
        html = html + """
            </div>
        """
        return html

def table_3(idream_obj):
        #pre-table 3
        html = """
            <H4 class="out_ collapsible" id="section3"><span></span>Acute Assessment</H4>
            <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(idream_obj)
        t3rows = gethtmlrowsfromcols(t3data, pva2headings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pva2headings)))
        html = html + """
            </div>
        """
        return html

def table_3_3(idream_obj):
        #pre-table 3
        html = """
            <H4 class="out_ collapsible" id="section3"><span></span>Acute Assessment</H4>
            <div class="out_ container_output">
        """
        #table 3
        t3data_3 = gett3data_3(idream_obj)
        t3rows_3 = gethtmlrowsfromcols(t3data_3, pva2headings)
        html = html + tmpl.render(Context(dict(data=t3rows_3, headings=pva2headings)))
        html = html + """
            </div>
        """
        return html

def table_sum_1(i, prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte):
        #pre-table sum_input_1
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>User Inputs</H4>
            <div class="out_ container_output">
        """
        #table sum_input_1
        tsuminputdata_1 = gettsumdata_1(prod_re, ai, liq_rte, fruit_rte, bread_rte, cheese_rte, veg_rte, meat_rte, pure_rte, piec_rte, powd_rte)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings1)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings1)))
        html = html + """
            </div>
        """
        return html

def table_sum_2(exp_child_c_1_out, exp_child_c_2_out, exp_adult_c_out, exp_fe_c_out):
        #pre-table sum_input_2
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Chronic Exposure (mg/kg/d)</H4>
            <div class="out_ container_output">
        """
        #table sum_input_2
        tsuminputdata_2 = gettsumdata_2(exp_child_c_1_out, exp_child_c_2_out, exp_adult_c_out, exp_fe_c_out)
        tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings2)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings2)))
        html = html + """
            </div>
        """
        return html

def table_sum_3(exp_child_a_1_out, exp_child_a_2_out, exp_adult_a_out, exp_fe_a_out):
        #pre-table sum_input_3
        html = """
            <H4 class="out_1 collapsible" id="section3"><span></span>Acute Exposure (mg/kg/d)</H4>
            <div class="out_ container_output">
        """
        #table sum_input_2
        tsuminputdata_3 = gettsumdata_2(exp_child_a_1_out, exp_child_a_2_out, exp_adult_a_out, exp_fe_a_out)
        tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3, sumheadings2)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings2)))
        html = html + """
            </div>
        """
        return html

