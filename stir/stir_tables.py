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
    <table class="out_23">
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
        <div class="out_1">
          <H3>User Inputs: Chemical</H3>
          <H4>Table 1. Application and Chemical Information</H4>
        </div>
    """
    #table 1
    t1data = gett1data(sm)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    return html

def gett1data(sm):
    data = { 
        "Parameter": ['Chemical Name','Application Rate','Direct Spray Column Height',
            'Spray Fraction Inhaled','Direct Spray Inhalation Duration','Molecular Weight','Vapor Pressure',],
        "Value": [sm.chemical_name, sm.ar2, sm.h, sm.f_inhaled, sm.ddsi, sm.mw, sm.vp,],
        "Units": ['', 'lbs a.i./A', 'm','','minutes','g/mol','torr', ],
    }
    return data

def table_2(pvuheadings, tmpl, sm):
    # #pre-table 2
    html = """
        <div class="out_2">
          <H4>Table 2. Toxicity Properties</H4>
        </div>
    """
    #table 2
    t2data = gett2data(sm)
    t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
    return html

def gett2data(sm):
    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Mineau Scaling Factor','Mammalian LC50',
          'Rat Inhalation Study Duration','Assessed Mammal Body Weight','Rat Inhalation LD50','Rat Oral LD50',],
        "Value": [sm.ld50ao, sm.assessed_bw_avian, sm.mineau, sm.lc50, sm.dur, sm.assessed_bw_mammal, sm.ld50ri, sm.ld50ro,],
        "Units": ['mg/kg-bw','kg','','mg/kg-bw','hours','kg','mg/kg-bw','mg/kg-bw',],
    }
    return data

def gett3data(cs,ir_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": [cs,ir_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def gett4data(ld50ao, aw_avian, mineau, lc50, dur, aw_mammal, ld50ri, ld50ro):
    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Mineau Scaling Factor','Mammalian LC50',
          'Rat Inhalation Study Duration','Assessed Mammal Body Weight','Rat Inhalation LD50','Rat Oral LD50',],
        "Value": [ld50ao, aw_avian, mineau, lc50, dur, aw_mammal, ld50ri, ld50ro,],
        "Units": ['mg/kg-bw','kg','','mg/kg-bw','hours','kg','mg/kg-bw','mg/kg-bw',],
    }
    return data

def table_3(pvuheadings, tmpl, sat_air_conc,inh_rate_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian):
        # #pre-table 2
        html = """
            <div class="out_2">
              <H4>Table 3. Avian Calculated Outputs</H4>
            </div>
        """
        #table 2
        t3data = gett3data(sat_air_conc,inh_rate_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian)
        t3rows = gethtmlrowsfromcols(t3data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        return html
