import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
import time
import datetime
from stir import stir_model
from stir import stir_parameters
import logging

logger = logging.getLogger("StirTables")

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvuqaqc():
    headings = ["Parameter", "Value", "Expected Value", "Units"]
    return headings

def getheaderpvr():
	headings = ["Parameter", "Value", "Results"]
	return headings

def getheaderpvrqaqc():
    headings = ["Parameter", "Value", "Expected Value", "Results", "Expected Results"]
    return headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
    return headings

def getheadersum_5():
    headings = ["Parameter", "Mean", "Std", "Min", "Max"]
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

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>STIR <a href="http://www.epa.gov/oppefed1/models/terrestrial/stir/stir_user_guide.html">Version 1.0</a> (Beta)<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

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

def table_sum_1(i,application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure):
        #pre-table sum_input_1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Batch Summary Statistics (Iterations=%s)</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Chemical Properties</H4>
                <div class="out_ container_output">
        """%(i-1)

        #table sum_input_1
        tsuminputdata_1 = gettsumdata_1(application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure)
        tsuminputrows_1 = gethtmlrowsfromcols(tsuminputdata_1, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows_1, headings=sumheadings)))
        html = html + """
        </div>
        """
        return html

def gettsumdata_1(application_rate,column_height,spray_drift_fraction,direct_spray_duration,molecular_weight,vapor_pressure):

    data = { 
        "Parameter": ['Application Rate', 'Direct Spray Column Height', 'Spray Fraction Inhaled', 'Direct Spray Inhalation Duration', 
                      'Molecular Weight', 'Vapor Pressure', ],
        "Mean": ['%.2e' % numpy.mean(application_rate), '%.2e' % numpy.mean(column_height), '%.2e' % numpy.mean(spray_drift_fraction), '%.2e' % numpy.mean(direct_spray_duration), '%.2e' % numpy.mean(molecular_weight), '%.2e' % numpy.mean(vapor_pressure),],
        "Std":  ['%.2e' % numpy.std(application_rate), '%.2e' % numpy.mean(column_height), '%.2e' % numpy.mean(spray_drift_fraction), '%.2e' % numpy.mean(direct_spray_duration), '%.2e' % numpy.std(molecular_weight), '%.2e' % numpy.std(vapor_pressure),],
        "Min":  ['%.2e' % numpy.min(application_rate), '%.2e' % numpy.mean(column_height), '%.2e' % numpy.mean(spray_drift_fraction), '%.2e' % numpy.mean(direct_spray_duration), '%.2e' % numpy.min(molecular_weight), '%.2e' % numpy.min(vapor_pressure),],
        "Max":  ['%.2e' % numpy.max(application_rate), '%.2e' % numpy.mean(column_height), '%.2e' % numpy.mean(spray_drift_fraction), '%.2e' % numpy.mean(direct_spray_duration), '%.2e' % numpy.max(molecular_weight), '%.2e' % numpy.max(vapor_pressure),],
        "Unit": ['lbs a.i./A', 'm','','minutes','g/mol','torr',],
    }
    return data

def table_1qaqc(pvuheadings, tmpl, sm):
    #chemical_name, ar2, h, f_inhaled, ddsi, mw, vp
    #pre-table 1
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span>Table 1. Application and Chemical Information</H4>
            <div class="out_ container_output">
        """
    #table 1
    t1data = gett1dataqaqc(sm)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
        """
    return html

def gett1dataqaqc(sm):
    data = { 
        "Parameter": ['Chemical Name','Application Rate','Direct Spray Column Height',
            'Spray Fraction Inhaled','Direct Spray Inhalation Duration','Molecular Weight','Vapor Pressure',],
        "Value": [sm.chemical_name_expected, sm.application_rate, sm.column_height, sm.spray_drift_fraction, sm.direct_spray_duration, 
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
        "Units": ['mg/kg-bw','kg','kg','','mg/kg-bw','hours','kg','kg','mg/kg-bw',],
    }
    return data

def table_sum_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50):
    #pre-table sum_input_2
    html = """
        <H4 class="out_1 collapsible" id="section3"><span></span>Toxicity  Properties</H4>
            <div class="out_ container_output">
    """

    #table sum_input_2
    tsuminputdata_2 = gettsumdata_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50)
    tsuminputrows_2 = gethtmlrowsfromcols(tsuminputdata_2, sumheadings)
    html = html + tmpl.render(Context(dict(data=tsuminputrows_2, headings=sumheadings)))
    html = html + """
            </div>
    </div>
    <br>
    """
    return html

def gettsumdata_2(avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor,mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal,mammal_oral_ld50):

    data = { 
        "Parameter": ['Avian Oral LD50','Assessed Bird Body Weight','Tested Bird Body Weight','Mineau Scaling Factor',
            'Mammalian Inhalation LC50','Rat Inhalation Study Duration','Assessed Mammal Body Weight','Tested Mammal Body Weight',
            'Mammal Oral LD50',],
        "Mean": ['%.2e' % numpy.mean(avian_oral_ld50), '%.2e' % numpy.mean(body_weight_assessed_bird), '%.2e' % numpy.mean(body_weight_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor), '%.2e' % numpy.mean(mammal_inhalation_lc50), '%.2e' % numpy.mean(duration_mammal_inhalation_study),'%.2e' % numpy.mean(body_weight_assessed_mammal), '%.2e' % numpy.mean(body_weight_tested_mammal), '%.2e' % numpy.mean(mammal_oral_ld50),],
        "Std":  ['%.2e' % numpy.std(avian_oral_ld50), '%.2e' % numpy.mean(body_weight_assessed_bird), '%.2e' % numpy.mean(body_weight_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor), '%.2e' % numpy.std(mammal_inhalation_lc50), '%.2e' % numpy.std(duration_mammal_inhalation_study),'%.2e' % numpy.std(body_weight_assessed_mammal), '%.2e' % numpy.std(body_weight_tested_mammal), '%.2e' % numpy.std(mammal_oral_ld50),],
        "Min":  ['%.2e' % numpy.min(avian_oral_ld50), '%.2e' % numpy.mean(body_weight_assessed_bird), '%.2e' % numpy.mean(body_weight_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor), '%.2e' % numpy.min(mammal_inhalation_lc50), '%.2e' % numpy.min(duration_mammal_inhalation_study),'%.2e' % numpy.min(body_weight_assessed_mammal), '%.2e' % numpy.min(body_weight_tested_mammal), '%.2e' % numpy.min(mammal_oral_ld50),],
        "Max":  ['%.2e' % numpy.max(avian_oral_ld50), '%.2e' % numpy.mean(body_weight_assessed_bird), '%.2e' % numpy.mean(body_weight_tested_bird), '%.2e' % numpy.mean(mineau_scaling_factor), '%.2e' % numpy.max(mammal_inhalation_lc50), '%.2e' % numpy.max(duration_mammal_inhalation_study),'%.2e' % numpy.max(body_weight_assessed_mammal), '%.2e' % numpy.max(body_weight_tested_mammal), '%.2e' % numpy.max(mammal_oral_ld50),],
        "Unit": ['mg/kg-bw','kg','kg','','mg/kg-bw','hours','kg','kg','mg/kg-bw',],
    }
    return data

def table_3(pvuheadings, tmpl, sm):
    # #pre-table 3
    html = """
    <br>
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
    return {'html':html, 'sat_air_conc':sm.sat_air_conc, 'inh_rate_avian':sm.inh_rate_avian, 'vid_avian':sm.vid_avian,
            'estimated_avian_inhalation_ld50':sm.estimated_avian_inhalation_ld50, 'adjusted_avian_inhalation_ld50':sm.adjusted_avian_inhalation_ld50, 'ratio_vid_avian':sm.ratio_vid_avian,
            'sid_avian':sm.sid_avian, 'ratio_sid_avian':sm.ratio_sid_avian}

def gett3data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        #"Value": [cs,ir_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian,],
        "Value": ['%.2e' % sm.sat_air_conc,'%.2e' % sm.inh_rate_avian,'%.2e' % sm.vid_avian,
            '%.2e' % sm.estimated_avian_inhalation_ld50,'%.2e' % sm.adjusted_avian_inhalation_ld50,'%.2e' % sm.ratio_vid_avian,
            '%.2e' % sm.sid_avian,'%.2e' % sm.ratio_sid_avian,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_sum_3(sat_air_conc,inh_rate_avian,vid_avian,estimated_avian_inhalation_ld50,adjusted_avian_inhalation_ld50,ratio_vid_avian,sid_avian,ratio_sid_avian):
    #pre-table sum_3
    html = """
    <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section3"><span></span>Avian Calculated Outputs</H4>
            <div class="out_ container_output">
    """

    #table sum_output_3
    tsuminputdata_3 = gettsumdata_3(sat_air_conc,inh_rate_avian,vid_avian,estimated_avian_inhalation_ld50,adjusted_avian_inhalation_ld50,ratio_vid_avian,sid_avian,ratio_sid_avian)
    tsuminputrows_3 = gethtmlrowsfromcols(tsuminputdata_3,sumheadings)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_3, headings=sumheadings)))
    html = html + """
            </div>
    """
    return html

def gettsumdata_3(sat_air_conc,inh_rate_avian,vid_avian,estimated_avian_inhalation_ld50,adjusted_avian_inhalation_ld50,ratio_vid_avian,sid_avian,ratio_sid_avian):

    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Mean": ['%.2e' % numpy.mean(sat_air_conc), '%.2e' % numpy.mean(inh_rate_avian), '%.2e' % numpy.mean(vid_avian), '%.2e' % numpy.mean(estimated_avian_inhalation_ld50), '%.2e' % numpy.mean(adjusted_avian_inhalation_ld50), '%.2e' % numpy.mean(ratio_vid_avian),'%.2e' % numpy.mean(sid_avian), '%.2e' % numpy.mean(ratio_sid_avian),],
        "Std":  ['%.2e' % numpy.std(sat_air_conc), '%.2e' % numpy.mean(inh_rate_avian), '%.2e' % numpy.mean(vid_avian), '%.2e' % numpy.mean(estimated_avian_inhalation_ld50), '%.2e' % numpy.std(adjusted_avian_inhalation_ld50), '%.2e' % numpy.std(ratio_vid_avian),'%.2e' % numpy.std(sid_avian), '%.2e' % numpy.std(ratio_sid_avian),],
        "Min":  ['%.2e' % numpy.min(sat_air_conc), '%.2e' % numpy.mean(inh_rate_avian), '%.2e' % numpy.mean(vid_avian), '%.2e' % numpy.mean(estimated_avian_inhalation_ld50), '%.2e' % numpy.min(adjusted_avian_inhalation_ld50), '%.2e' % numpy.min(ratio_vid_avian),'%.2e' % numpy.min(sid_avian), '%.2e' % numpy.min(ratio_sid_avian),],
        "Max":  ['%.2e' % numpy.max(sat_air_conc), '%.2e' % numpy.mean(inh_rate_avian), '%.2e' % numpy.mean(vid_avian), '%.2e' % numpy.mean(estimated_avian_inhalation_ld50), '%.2e' % numpy.max(adjusted_avian_inhalation_ld50), '%.2e' % numpy.max(ratio_vid_avian),'%.2e' % numpy.max(sid_avian), '%.2e' % numpy.max(ratio_sid_avian),],
        "Unit": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_3qaqc(pvuheadingsqaqc, tmpl, sm):
    # #pre-table 3
    html = """
    <br>
        <H3 class="out_3 collapsible" id="section4"><span></span>Calculated Estimates</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section5"><span></span>Table 3. Avian Calculated Outputs</H4>
                <div class="out_ container_output">
    """
    #table 3
    t3data = gett3dataqaqc(sm)
    t3rows = gethtmlrowsfromcols(t3data,pvuheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadingsqaqc)))
    html = html + """
        </div>
        """
    return html

def gett3dataqaqc(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Avian Inhalation Rate','Maximum 1-hour Avian Vapor Inhalation Dose',
          'Estimated Avian Inhalation LD50','Adjusted Avian Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Bird','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        #"Value": [cs,ir_avian,vid_avian,ld50est,ld50adj,ratio_vd_avian,sid_avian,ratio_sid_avian,],
        "Value": ['%.2e' % sm.sat_air_conc,'%.2e' % sm.inh_rate_avian,'%.2e' % sm.vid_avian,
            '%.2e' % sm.estimated_avian_inhalation_ld50,'%.2e' % sm.adjusted_avian_inhalation_ld50,'%.2e' % sm.ratio_vid_avian,
            '%.2e' % sm.sid_avian,'%.2e' % sm.ratio_sid_avian,],
        "Expected Value": ['%.2e' % sm.sat_air_conc_expected,'%.2e' % sm.inh_rate_avian_expected,'%.2e' % sm.vid_avian_expected,
            '%.2e' % sm.estimated_avian_inhalation_ld50_expected,'%.2e' % sm.adjusted_avian_inhalation_ld50_expected,'%.2e' % sm.ratio_vid_avian_expected,
            '%.2e' % sm.sid_avian_expected,'%.2e' % sm.ratio_sid_avian_expected,],
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
        """
    return {'html':html, 'sat_air_conc':sm.sat_air_conc, 'inh_rate_mammal':sm.inh_rate_mammal, 'vid_mammal':sm.vid_mammal,
            'mammal_inhalation_ld50':sm.mammal_inhalation_ld50, 'adjusted_mammal_inhalation_ld50':sm.adjusted_mammal_inhalation_ld50, 'ratio_vid_mammal':sm.ratio_vid_mammal,
            'sid_mammal':sm.sid_mammal, 'ratio_sid_mammal':sm.ratio_sid_mammal}

def gett4data(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": ['%.2e' % sm.sat_air_conc,'%.2e' % sm.inh_rate_mammal,'%.2e' % sm.vid_mammal,
            '%.2e' % sm.mammal_inhalation_ld50,'%.2e' % sm.adjusted_mammal_inhalation_ld50,'%.2e' % sm.ratio_vid_mammal,
            '%.2e' % sm.sid_mammal,'%.2e' % sm.ratio_sid_mammal,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_sum_4(sat_air_conc,inh_rate_mammal,vid_mammal,mammal_inhalation_ld50,adjusted_mammal_inhalation_ld50,ratio_vid_mammal,sid_mammal,ratio_sid_mammal):
    #pre-table sum_4
    html = """
        <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
            <div class="out_ container_output">
    """

    #table sum_output_4
    tsuminputdata_4 = gettsumdata_4(sat_air_conc,inh_rate_mammal,vid_mammal,mammal_inhalation_ld50,adjusted_mammal_inhalation_ld50,ratio_vid_mammal,sid_mammal,ratio_sid_mammal)
    tsuminputrows_4 = gethtmlrowsfromcols(tsuminputdata_4,sumheadings)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_4, headings=sumheadings)))
    html = html + """
    </div>
    """
    return html

def gettsumdata_4(sat_air_conc,inh_rate_mammal,vid_mammal,mammal_inhalation_ld50,adjusted_mammal_inhalation_ld50,ratio_vid_mammal,sid_mammal,ratio_sid_mammal):

    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50'],
        "Mean": ['%.2e' % numpy.mean(sat_air_conc), '%.2e' % numpy.mean(inh_rate_mammal), '%.2e' % numpy.mean(vid_mammal), '%.2e' % numpy.mean(mammal_inhalation_ld50), '%.2e' % numpy.mean(adjusted_mammal_inhalation_ld50), '%.2e' % numpy.mean(ratio_vid_mammal),'%.2e' % numpy.mean(sid_mammal), '%.2e' % numpy.mean(ratio_sid_mammal),],
        "Std":  ['%.2e' % numpy.std(sat_air_conc), '%.2e' % numpy.mean(inh_rate_mammal), '%.2e' % numpy.mean(vid_mammal), '%.2e' % numpy.mean(mammal_inhalation_ld50), '%.2e' % numpy.std(adjusted_mammal_inhalation_ld50), '%.2e' % numpy.std(ratio_vid_mammal),'%.2e' % numpy.std(sid_mammal), '%.2e' % numpy.std(ratio_sid_mammal),],
        "Min":  ['%.2e' % numpy.min(sat_air_conc), '%.2e' % numpy.mean(inh_rate_mammal), '%.2e' % numpy.mean(vid_mammal), '%.2e' % numpy.mean(mammal_inhalation_ld50), '%.2e' % numpy.min(adjusted_mammal_inhalation_ld50), '%.2e' % numpy.min(ratio_vid_mammal),'%.2e' % numpy.min(sid_mammal), '%.2e' % numpy.min(ratio_sid_mammal),],
        "Max":  ['%.2e' % numpy.max(sat_air_conc), '%.2e' % numpy.mean(inh_rate_mammal), '%.2e' % numpy.mean(vid_mammal), '%.2e' % numpy.mean(mammal_inhalation_ld50), '%.2e' % numpy.max(adjusted_mammal_inhalation_ld50), '%.2e' % numpy.max(ratio_vid_mammal),'%.2e' % numpy.max(sid_mammal), '%.2e' % numpy.max(ratio_sid_mammal),],
        "Unit": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_4qaqc(pvuheadingsqaqc, tmpl, sm):
    # #pre-table 3
    html = """
        <H4 class="out_4 collapsible" id="section6"><span></span>Table 4. Mammal Calculated Outputs</H4>
            <div class="out_ container_output">
    """
    #table 3
    t4data = gett4dataqaqc(sm)
    t4rows = gethtmlrowsfromcols(t4data,pvuheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t4rows, headings=pvuheadingsqaqc)))
    html = html + """
        </div>
        """
    return html

def gett4dataqaqc(sm):
    data = { 
        "Parameter": ['Saturated Air Concentration of Pesticide','Mammal Inhalation Rate','Maximum 1-hour Mammal Vapor Inhalation Dose',
          'Mammal Inhalation LD50','Adjusted Mammal Inhalation LD50','Ratio of Vapor Dose to Adjusted Inhalation LD50',
          'Spray Droplet Inhalation Dose of Assessed Mammal','Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD50',],
        "Value": ['%.2e' % sm.sat_air_conc,'%.2e' % sm.inh_rate_mammal,'%.2e' % sm.vid_mammal,
            '%.2e' % sm.mammal_inhalation_ld50,'%.2e' % sm.adjusted_mammal_inhalation_ld50,'%.2e' % sm.ratio_vid_mammal,
            '%.2e' % sm.sid_mammal,'%.2e' % sm.ratio_sid_mammal,],
        "Expected Value": ['%.2e' % sm.sat_air_conc_expected,'%.2e' % sm.inh_rate_mammal_expected,'%.2e' % sm.vid_mammal_expected,
            '%.2e' % sm.mammal_inhalation_ld50_expected,'%.2e' % sm.adjusted_mammal_inhalation_ld50_expected,'%.2e' % sm.ratio_vid_mammal_expected,
            '%.2e' % sm.sid_mammal_expected,'%.2e' % sm.ratio_sid_mammal_expected,],
        "Units": ['mg/m3','cm3/hr','mg/kg-bw','mg/kg-bw','mg/kg-bw','unitless','mg/kg-bw','unitless',],
    }
    return data

def table_5(pvuheadings, tmpl, sm):
    # #pre-table 5
    html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
                <div class="out_ container_output">
    """
    #table 3
    t5data = gett5data(sm)
    t5rows = gethtmlrowsfromcols(t5data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvuheadings)))
    html = html + """
        </div>
    </div>
    """
    return {'html':html, 'ratio_vid_avian':sm.ratio_vid_avian, 'ratio_sid_avian':sm.ratio_sid_avian, 'ratio_vid_mammal':sm.ratio_vid_mammal,
            'ratio_sid_mammal':sm.ratio_sid_mammal}

def gett5data(sm):
    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50',],
        "Value": ['%.2e' % sm.ratio_vid_avian,'%.2e' % sm.ratio_sid_avian,'%.2e' % sm.ratio_vid_mammal,'%.2e' % sm.ratio_sid_mammal,],
        "Results": [sm.loc_vid_avian,sm.loc_sid_avian,sm.loc_vid_mammal,sm.loc_sid_mammal,],
    }
    return data

def table_sum_5(ratio_vid_avian, ratio_sid_avian, ratio_vid_mammal, ratio_sid_mammal):
    #pre-table sum_5
    html = """
        <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
            <div class="out_ container_output">
    """

    #table sum_output_5
    tsuminputdata_5 = gettsumdata_5(ratio_vid_avian, ratio_sid_avian, ratio_vid_mammal, ratio_sid_mammal)
    tsuminputrows_5 = gethtmlrowsfromcols(tsuminputdata_5,sumheadings_5)       
    html = html + tmpl.render(Context(dict(data=tsuminputrows_5, headings=sumheadings_5)))
    html = html + """
        </div>
    </div>
    """
    return html

def gettsumdata_5(ratio_vid_avian, ratio_sid_avian, ratio_vid_mammal, ratio_sid_mammal):

    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50'],
        "Mean": ['%.2e' % numpy.mean(ratio_vid_avian), '%.2e' % numpy.mean(ratio_sid_avian), '%.2e' % numpy.mean(ratio_vid_mammal), '%.2e' % numpy.mean(ratio_sid_mammal),],
        "Std":  ['%.2e' % numpy.std(ratio_vid_avian), '%.2e' % numpy.mean(ratio_sid_avian), '%.2e' % numpy.mean(ratio_vid_mammal), '%.2e' % numpy.mean(ratio_sid_mammal),],
        "Min":  ['%.2e' % numpy.min(ratio_vid_avian), '%.2e' % numpy.mean(ratio_sid_avian), '%.2e' % numpy.mean(ratio_vid_mammal), '%.2e' % numpy.mean(ratio_sid_mammal),],
        "Max":  ['%.2e' % numpy.max(ratio_vid_avian), '%.2e' % numpy.mean(ratio_sid_avian), '%.2e' % numpy.mean(ratio_vid_mammal), '%.2e' % numpy.mean(ratio_sid_mammal),],
    }
    return data

def table_5qaqc(pvuheadingsqaqc, tmpl, sm):
    # #pre-table 5
    html = """
            <H4 class="out_5 collapsible" id="section5"><span></span>Table 5. Inference</H4>
                <div class="out_ container_output">
    """
    #table 3
    t5data = gett5dataqaqc(sm)
    t5rows = gethtmlrowsfromcols(t5data,pvuheadingsqaqc)
    html = html + tmpl.render(Context(dict(data=t5rows, headings=pvuheadingsqaqc)))
    html = html + """
        </div>
    </div>
    """
    return html

def gett5dataqaqc(sm):
    data = { 
        "Parameter": ['Avian: Ratio of Vapor Dose to Adjusted Inhalation LD50','Avian: Ratio of Droplet Dose to Adjusted Inhalation LD50',
          'Mammal: Ratio of Vapor Dose to Adjusted Inhalation LD50','Mammal: Ratio of Droplet Dose to Adjusted Inhalation LD50',],
        "Value": ['%.2e' % sm.ratio_vid_avian,'%.2e' % sm.ratio_sid_avian,'%.2e' % sm.ratio_vid_mammal,'%.2e' % sm.ratio_sid_mammal,],
        "Expected Value": ['%.2e' % sm.ratio_vid_avian_expected,'%.2e' % sm.ratio_sid_avian_expected,'%.2e' % sm.ratio_vid_mammal_expected,'%.2e' % sm.ratio_sid_mammal_expected,],
        "Results": [sm.loc_vid_avian,sm.loc_sid_avian,sm.loc_vid_mammal,sm.loc_sid_mammal,],
        "Expected Results": [sm.loc_vid_avian_expected,sm.loc_sid_avian_expected,sm.loc_vid_mammal_expected,sm.loc_sid_mammal_expected,],
    }
    return data

pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
sumheadings = getheadersum()
sumheadings_5 = getheadersum_5()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all_batch(sm):
    html = table_1(pvuheadings,tmpl,sm)
    html = html + table_2(pvuheadings,tmpl,sm)
    html = html + table_3(pvuheadings,tmpl,sm)['html']
    html = html + table_4(pvuheadings,tmpl,sm)['html']
    html = html + table_5(pvrheadings,tmpl,sm)['html']
    return html