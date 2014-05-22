from django.template import Context, Template
from przm_exams import przm_exams_model
import os
from google.appengine.ext.webapp import template
import datetime

def getheaderpvu_1():
	headings = ["Parameter", "Value"]
	return headings

def getheaderpvu_2():
    headings = ["Application", "Days relevant to the application", "Application method",
                "Application rate", "Unit", "Chemical application Method", "Efficiency",
                "Efficiency", "Incorporation depth (DEPI)"]
    return headings

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


def gett1data(przm_exams_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Scenarios', 'Met Filename',],
        "Value": ['%s' % przm_exams_obj.chem_name, '%s' % przm_exams_obj.scenarios, '%s' % przm_exams_obj.met_o,],
    }
    return data

def gett2data(index, Apt_p, DayRe, Ap_mp, Ar, Unit, CAM_f_p, EFF_p, Drft_p, DEPI_f):
    data = { 
        "Application": ['%s' %index,  ],
        "Days relevant to the application": [DayRe,],
        "Application method": [Ap_mp,],
        "Application rate": [Ar,],
        "Unit": [Unit,],
        "Chemical application Method": [CAM_f_p,],
        "Efficiency": [EFF_p,],
        "Efficiency": [Drft_p,],
        "Incorporation depth (DEPI)": [DEPI_f,],
    }
    return data

def gett3data(przm_exams_obj):
    data = { 
        "Parameter": ['Farm Pond (no flow)', 'Molecular Weight', 'Solubility', 
                      'Aquatic Sediment', 'Vapor Pressure', 'Aerobic aquatic metabolism', 
                      'Anaerobic aquatic metabolism', 'Aquatic Direct Photolysis', 'Test Temperature',],
        "Value": ['%s' % przm_exams_obj.farm, '%s' % przm_exams_obj.mw, '%s' % przm_exams_obj.sol, 
                  '%s' % przm_exams_obj.koc, '%s' % przm_exams_obj.vp, '%s' % przm_exams_obj.aem, 
                  '%s' % przm_exams_obj.anm, '%s' % przm_exams_obj.aqp, '%s' % przm_exams_obj.tmper,],
        "Units": ['', 'g/mol', 'mg/L', 'mL/g', 'torr', 'days', 'days', 'days', '<sup>o</sup>C'],
    }
    return data


def gett4data(index, pH, HL):
    data = { 
        "Index": ['%s' %index,  ],
        "Test pH": [pH,],
        "Half-life (days)": [HL,],
    }
    return data

pvuheadings_1 = getheaderpvu_1()
pvuheadings_2 = getheaderpvu_2()
pvuheadings = getheaderpvu()
pvaheadings = getheaderpva()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def timestamp(przm_exams_obj):
    st = datetime.datetime.strptime(przm_exams_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>PRZM-EXAMS<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_all(przm_exams_obj):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    table1_out = table_1(przm_exams_obj)
    table2_out = table_2(przm_exams_obj)
    table3_out = table_3(przm_exams_obj)
    table4_out = table_4(przm_exams_obj)
    table5_out = table_5(przm_exams_obj)
    table6_out = template.render(templatepath + 'przm_exams_jqplot.html', {})

    html_all = table1_out+table2_out+table3_out+table4_out+table5_out+table6_out+"</div></div>"

    return html_all


def table_1(przm_exams_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>PRZM Inputs:</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span></H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(przm_exams_obj)
        t1rows = gethtmlrowsfromcols(t1data, pvuheadings_1)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings_1)))
        html = html + """
                </div>
        """
        return html

def table_2(przm_exams_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Applications (Number of Applications=%s)</H4>
                <div class="out_ container_output">
        """ %(przm_exams_obj.noa)
        #table 2
        t2data_all=[]
        for i in range(int(przm_exams_obj.noa)):
            Apt_p_temp=przm_exams_obj.Apt_p[i]
            DayRe_temp=przm_exams_obj.DayRe[i]
            Ap_mp_temp=przm_exams_obj.Ap_mp[i]
            Unit_temp=przm_exams_obj.unit_p
            Ar_temp=przm_exams_obj.Ar[i]
            CAM_f_p_temp=przm_exams_obj.CAM_f_p[i]
            EFF_p_temp=przm_exams_obj.EFF_p[i]
            Drft_p_temp=przm_exams_obj.Drft_p[i]
            DEPI_f_temp=przm_exams_obj.DEPI_f[i]


            t2data_temp=gett2data(i+1, Apt_p_temp, DayRe_temp, Ap_mp_temp, Ar_temp, 
                                  Unit_temp, CAM_f_p_temp, EFF_p_temp, Drft_p_temp, DEPI_f_temp)
            t2data_all.append(t2data_temp)
        t2data = dict([(k,[t2data_ind[k][0] for t2data_ind in t2data_all]) for k in t2data_temp])
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings_2)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings_2)))
        html = html + """
                </div>
        """
        return html

def table_3(przm_exams_obj):
        #pre-table 3
        html = """
        <H3 class="out_3 collapsible" id="section1"><span></span>EXAMS Inputs:</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section2"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(przm_exams_obj)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_4(przm_exams_obj):
        # #pre-table 4
        html = """
            <H4 class="out_4 collapsible" id="section3"><span></span>Hydrolysis Tests (Number of Tested pH=%s)</H4>
                <div class="out_ container_output">
        """ %(przm_exams_obj.n_ph)
        #table 4
        t4data_all=[]
        for i in range(int(przm_exams_obj.n_ph)):
            ph_out_temp=przm_exams_obj.ph_out[i]
            hl_out_temp=przm_exams_obj.hl_out[i]
            t4data_temp=gett4data(i+1, ph_out_temp, hl_out_temp)
            t4data_all.append(t4data_temp)
        t4data = dict([(k,[t4data_ind[k][0] for t4data_ind in t4data_all]) for k in t4data_temp])
        t4rows = gethtmlrowsfromcols(t4data,pvaheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=pvaheadings)))
        html = html + """
                </div>
        """
        return html

def table_5(przm_exams_obj):
        html = """
                <br><div><table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">PRZM-EXAMS Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
                          <tr>          
                            <td id="x_pre_irr_val" data-val='%s' style="display: none"></td>  
                            <td id="x_leachate_val" data-val='%s' style="display: none"></td>  
                            <td id="x_et_val" data-val='%s' style="display: none"></td>  
                            <td id="x_runoff_val" data-val='%s' style="display: none"></td>
                            <td id="Lim_inst_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_24h_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_96h_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_21d_val" data-val='%s' style="display: none"></td>
                            <td id="Lim_60d_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_90d_val" data-val='%s' style="display: none"></td>  
                            <td id="Lim_y_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_inst_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_24h_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_96h_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_21d_val" data-val='%s' style="display: none"></td>
                            <td id="Ben_60d_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_90d_val" data-val='%s' style="display: none"></td>  
                            <td id="Ben_y_val" data-val='%s' style="display: none"></td>  
                          </tr>                               
                </table><br></div>"""%(przm_exams_obj.link, przm_exams_obj.x_pre_irr, przm_exams_obj.x_leachate, przm_exams_obj.x_et, przm_exams_obj.x_runoff,
                                       przm_exams_obj.Lim_inst, przm_exams_obj.Lim_24h, przm_exams_obj.Lim_96h, przm_exams_obj.Lim_21d, przm_exams_obj.Lim_60d, przm_exams_obj.Lim_90d, przm_exams_obj.Lim_y,  
                                       przm_exams_obj.Ben_inst, przm_exams_obj.Ben_24h, przm_exams_obj.Ben_96h, przm_exams_obj.Ben_21d, przm_exams_obj.Ben_60d, przm_exams_obj.Ben_90d, przm_exams_obj.Ben_y)
        return html

