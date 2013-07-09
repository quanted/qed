import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from przm_exams import przm_exams_model

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


def table_all(przm_exams_obj):
    table1_out = table_1(przm_exams_obj)
    table2_out = table_2(przm_exams_obj)

    table3_out = table_3(przm_exams_obj)
    table4_out = table_4(przm_exams_obj)
    html_all = table1_out+table2_out+table3_out+table4_out

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

# Apt_p_j, DayRe_j, Ap_mp_j, Ar_j, Unit_p_j, CAM_f_p_j, EFF_p_j, Drft_p_j, DEPI_p_j
# Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
# [('n_ph', 3.0), ('CAM_f', ['1', '1']), ('unit_p', 'kg/ha'), ('Ap_mp', ['Ground Sprayer', 'Ground Sprayer'])
# ('anm', '28'), ('DD', ['01', '03']), ('sol', '24'), ('YY', '61'), ('tmper', '30'), ('unit', '1')
# ('DEPI_text', ['4.00', '4.00']), ('koc', '25'), ('scenarios', 'FL Citrus MLRA-156A')
# ('ph_out', [5.0, 7.0, 9.0]), ('run_o', 'FL1Cit-P.RUN'), ('chem_name', 'Forchlorfenuron')
# ('aqp', '29'), ('hl_out', [12.0, 13.0, 14.0]), ('farm', 'Yes'), ('Drft_p', ['0.0100', '0.0100'])
# ('noa', 2), ('CAM_f_p', ['1-Soil applied (4cm incorporation, linearly decreasing with depth)', '1-Soil applied (4cm incorporation, linearly decreasing with depth)'])

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
