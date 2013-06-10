import numpy as np
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvr():
	headings = ["Parameter", "Value", "Results"]
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

def table_1(pvuheadings, tmpl, sm):
    #chemical_name, ar2, h, f_inhaled, ddsi, mw, vp
    #pre-table 1
    html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical</H3>
        <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span>Table 1. Application and Chemical Information</H4>
        <div class="out_ container_output">
        """
    #table 1
    t1data = gett1data(sm)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
        """
    return html

def gett1data(sm):
    data = { 
        "Parameter": ['Chemical Name','Application Rate','Direct Spray Column Height',
            'Spray Fraction Inhaled','Direct Spray Inhalation Duration','Molecular Weight','Vapor Pressure',],
        "Value": [sm.chemical_name, sm.application_rate, sm.column_height, sm.spray_drift_fraction, sm.direct_spray_duration, 
            sm.molecular_weight, sm.vapor_pressure,],
        "Units": ['', 'lbs a.i./A', 'm','','minutes','g/mol','torr', ],
    }
    return data

def table_2(pvuheadings, tmpl, sm):
    # #pre-table 2
    html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Toxicity Properties</H4>
                <div class="out_ container_output">
    """
    #table 2
    t2data = gett2data(sm)
    t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
    html = html + """
        </div>
        </div>
        """
    return html

def gett2data(sm):
    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Tested Bird Body Weight','Mineau Scaling Factor',
            'Mammalian Inhalation LC50','Rat Inhalation Study Duration','Assessed Mammal Body Weight','Tested Mammal Body Weight',
            'Mammal Oral LD50',],
        "Value": [sm.avian_oral_ld50, sm.body_weight_assessed_bird, sm.body_weight_tested_bird, sm.mineau_scaling_factor, 
            sm.mammal_inhalation_lc50, sm.duration_mammal_inhalation_study, sm.body_weight_assessed_mammal, sm.body_weight_tested_mammal,
            sm.mammal_oral_ld50,],
        "Units": ['mg/kg-bw','kg','kg','mg/kg-bw','hours','kg','kg','mg/kg-bw',],
    }
    return data

def table_3(pvuheadings, tmpl, sm):
    # #pre-table 3
    html = """
        <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section5"><span></span>Table 3. Avian Calculated Outputs</H4>
                <div class="out_ container_output">
    """
    #table 3
    t3data = gett3data(sm)
    t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
    html = html + """
        </div>
        """
    return html

def gett3data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        #"Value": [cs,ir_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian,],
        "Value": [sm.sat_air_conc,sm.inh_rate_avian,sm.vid_avian,
            sm.estimated_avian_inhalation_ld50,sm.adjusted_avian_inhalation_ld50,sm.ratio_vid_avian,
            sm.sid_avian,sm.ratio_sid_avian,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_4(pvuheadings, tmpl, sm):
    # #pre-table 3
    html = """
                <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
                <div class="out_ container_output">
    """
    #table 3
    t4data = gett4data(sm)
    t4rows = gethtmlrowsfromcols(t4data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadings)))
    html = html + """
        </div>
        </div>
        """
    return html

def gett4data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": [sm.sat_air_conc,sm.inh_rate_mammal,sm.vid_mammal,
            sm.mammal_inhalation_ld50,sm.adjusted_mammal_inhalation_ld50,sm.ratio_vid_mammal,
            sm.sid_mammal,sm.ratio_sid_mammal,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

