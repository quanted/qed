import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from exams import exams_model
import datetime

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpva():
    headings = ["Index", "Test pH", "Half-life (days)"]
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


def gett1data(exams_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Scenario', 'Farm Pond (no flow)', 'Molecular Weight',
                      'Solubility', 'Aquatic Sediment', 'Vapor Pressure', 'Aerobic aquatic metabolism', 'Anaerobic aquatic metabolism',
                      'Aquatic Direct Photolysis', 'Test Temperature',],
        "Value": ['%s' % exams_obj.chem_name, '%s' % exams_obj.scenarios, '%s' % exams_obj.farm, '%s' % exams_obj.mw,
                  '%s' % exams_obj.sol, '%s' % exams_obj.koc, '%s' % exams_obj.vp, '%s' % exams_obj.aem, '%s' % exams_obj.anm,
                  '%s' % exams_obj.aqp, '%s' % exams_obj.tmper,],
        "Units": ['', '', '', 'g/mol', 'mg/L', 'mL/g', 'torr', 'days', 'days', 'days', '<sup>o</sup>C'],
    }
    return data

def gett2data(index, pH, HL):
    data = { 
        "Index": ['%s' %index,  ],
        "Test pH": [pH,],
        "Half-life (days)": [HL,],
    }
    return data

pvuheadings = getheaderpvu()
pvaheadings = getheaderpva()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def timestamp(exams_obj):
    st = datetime.datetime.strptime(exams_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>EXAMS<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


def table_all(exams_obj):
    table1_out = table_1(exams_obj)
    table2_out = table_2(exams_obj)
    table3_out = table_3(exams_obj)
    html_all = table1_out + table2_out + table3_out

    return html_all


def table_1(exams_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs:</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(exams_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(exams_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Hydrolysis Tests (Number of Tested pH=%s)</H4>
                <div class="out_ container_output">
        """ %(exams_obj.n_ph)
        #table 2
        t2data_all=[]
        for i in range(int(exams_obj.n_ph)):
            ph_out_temp=exams_obj.ph_out[i]
            hl_out_temp=exams_obj.hl_out[i]
            t2data_temp=gett2data(i+1, ph_out_temp, hl_out_temp)
            t2data_all.append(t2data_temp)
        t2data = dict([(k,[t2data_ind[k][0] for t2data_ind in t2data_all]) for k in t2data_temp])
        t2rows = gethtmlrowsfromcols(t2data,pvaheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvaheadings)))
        html = html + """
                </div>
        """
        return html

def table_3(exams_obj):
        html = """
        <br><div><table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">EXAMS Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
        </table><br></div></div>"""%(exams_obj.link)
        return html

