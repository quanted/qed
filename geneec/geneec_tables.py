import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from geneec import geneec_model
import time
import datetime

def getheaderpvu():
  headings = ["Parameter", "Value", "Units"]
  return headings

def getheaderpvuqaqc():
  headings = ["Parameter", "Value", "Expected Value", "Units"]
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
 
# '%s' % geneec_obj.hydrolysis, 
def gett1dataAerial(geneec_obj):
    if geneec_obj.aerial_size_dist == "a":
      aerial_dist = 'Very Fine to Fine'
    if geneec_obj.aerial_size_dist == "b":
      aerial_dist = 'Fine to Medium (EFED Default)'
    if geneec_obj.aerial_size_dist == "c":
      aerial_dist = 'Medium to Coarse'
    if geneec_obj.aerial_size_dist == "d":
      aerial_dist = 'Coarse to Very Coarse'
    data = { 
        "Parameter": [ 'Chemical Name', 'Application target', 'Application rate', 'Number of applications',
                      'Interval between applications', mark_safe('K<sub>OC</sub>'), 'Aerobic soil metabolism half-life', 'Wet in',
                      'Aerial size dist', 'Width of the no-spray zone', 'Solubility', 'Aerobic aquatic metabolism half-life', 'Photolysis, aquatic half-life' ],
        "Value": [ geneec_obj.chem_name, geneec_obj.application_target, '%s' % geneec_obj.application_rate, '%s' % geneec_obj.number_of_applications,
                  '%s' % geneec_obj.interval_between_applications, '%s' % geneec_obj.Koc, '%s' % geneec_obj.aerobic_soil_metabolism, '%s' % geneec_obj.wet_in,
                  '%s' % aerial_dist, '%s' % geneec_obj.no_spray_drift, '%s' % geneec_obj.solubility, '%s' % geneec_obj.aerobic_aquatic_metabolism, '%s' % geneec_obj.photolysis_aquatic_half_life ],
        "Units": [ '', '', 'lbs a.i./A', '', 'days', 'mL/g OC', 'days', '', '', 'ft', 'mg/L', 'days', 'days' ]
    }
    return data

def gett1dataAerial_qaqc(geneec_obj):
    if geneec_obj.aerial_size_dist == "a":
      aerial_dist = 'Very Fine to Fine'
    if geneec_obj.aerial_size_dist == "b":
      aerial_dist = 'Fine to Medium (EFED Default)'
    if geneec_obj.aerial_size_dist == "c":
      aerial_dist = 'Medium to Coarse'
    if geneec_obj.aerial_size_dist == "d":
      aerial_dist = 'Coarse to Very Coarse'
    data = { 
        "Parameter": [ 'Chemical Name', 'Application target', 'Application rate', 'Number of applications',
                      'Interval between applications', mark_safe('K<sub>OC</sub>'), 'Aerobic soil metabolism half-life', 'Wet in',
                      'Aerial size dist', 'Width of the no-spray zone', 'Solubility', 'Aerobic aquatic metabolism half-life', 'Photolysis, aquatic half-life' ],
        "Value": [ geneec_obj.chem_name_exp, geneec_obj.application_target, '%s' % geneec_obj.application_rate, '%s' % geneec_obj.number_of_applications,
                  '%s' % geneec_obj.interval_between_applications, '%s' % geneec_obj.Koc, '%s' % geneec_obj.aerobic_soil_metabolism, '%s' % geneec_obj.wet_in,
                  '%s' % aerial_dist, '%s' % geneec_obj.no_spray_drift, '%s' % geneec_obj.solubility, '%s' % geneec_obj.aerobic_aquatic_metabolism, '%s' % geneec_obj.photolysis_aquatic_half_life ],
        "Units": [ '', '', 'lbs a.i./A', '', 'days', 'mL/g OC', 'days', '', '', 'ft', 'mg/L', 'days', 'days' ]
    }
    return data

def gett1dataGround(geneec_obj):
    if geneec_obj.ground_spray_type == 'a':
      sprayType = 'Low Boom Ground Spray (20" or less)'
    if geneec_obj.ground_spray_type == 'b':
      sprayType = 'High Boom Ground Spray (20-50"; EFED Default)'
    if geneec_obj.spray_quality == 'a':
      sprayQual = 'Fine (EFED Default)'
    if geneec_obj.spray_quality == 'b':
      sprayQual = 'Medium'
    data = { 
        "Parameter": [ 'Chemical Name', 'Application target', 'Application rate', 'Number of applications',
                      'Interval between applications', mark_safe('K<sub>OC</sub>'), 'Aerobic soil metabolism half-life', 'Wet in',
                      'Ground spray type', 'Spray quality', 'Width of the no-spray zone', 'Incorporation depth', 'Solubility', 'Aerobic aquatic metabolism half-life', 'Photolysis, aquatic half-life' ],
        "Value": [ geneec_obj.chem_name, geneec_obj.application_target, '%s' % geneec_obj.application_rate, '%s' % geneec_obj.number_of_applications,
                  '%s' % geneec_obj.interval_between_applications, '%s' % geneec_obj.Koc, '%s' % geneec_obj.aerobic_soil_metabolism, '%s' % geneec_obj.wet_in,
                  '%s' % sprayType, '%s' % sprayQual, '%s' % geneec_obj.no_spray_drift, '%s' % geneec_obj.incorporation_depth, '%s' % geneec_obj.solubility, '%s' % geneec_obj.aerobic_aquatic_metabolism, '%s' % geneec_obj.photolysis_aquatic_half_life ],
        "Units": [ '', '', 'lbs a.i./A', '', 'days', 'mL/g OC', 'days', '', '','', 'ft', 'in', 'mg/L', 'days', 'days' ]
    }
    return data

def gett1dataAirBlast(geneec_obj):
    if geneec_obj.airblast_type == 'a':
      airblast = 'Orchards and Dormant Vineyards'
    if geneec_obj.airblast_type == 'b':
      airblast = 'Foliated Vineyards'
    data = { 
        "Parameter": [ 'Chemical Name', 'Application target', 'Application rate', 'Number of applications',
                      'Interval between applications', mark_safe('K<sub>OC</sub>'), 'Aerobic soil metabolism half-life', 'Wet in',
                      'Aerial size dist', 'Width of the no-spray zone', 'Solubility', 'Aerobic aquatic metabolism half-life', 'Photolysis, aquatic half-life' ],
        "Value": [ geneec_obj.chem_name, geneec_obj.application_target, '%s' % geneec_obj.application_rate, '%s' % geneec_obj.number_of_applications,
                  '%s' % geneec_obj.interval_between_applications, '%s' % geneec_obj.Koc, '%s' % geneec_obj.aerobic_soil_metabolism, '%s' % geneec_obj.wet_in,
                  '%s' % airblast, '%s' % geneec_obj.no_spray_drift, '%s' % geneec_obj.solubility, '%s' % geneec_obj.aerobic_aquatic_metabolism, '%s' % geneec_obj.photolysis_aquatic_half_life ],
        "Units": [ '', '', 'lbs a.i./A', '', 'days', 'mL/g OC', 'days', '', '', 'ft', 'mg/L', 'days', 'days' ]
    }
    return data

def gett1dataGranular(geneec_obj):
    data = { 
        "Parameter": [ 'Chemical Name', 'Application target', 'Application rate', 'Number of applications',
                      'Interval between applications', mark_safe('K<sub>OC</sub>'), 'Aerobic soil metabolism half-life', 'Wet in',
                      'Incorporation depth', 'Solubility', 'Aerobic aquatic metabolism half-life', 'Photolysis, aquatic half-life' ],
        "Value": [ geneec_obj.chem_name, geneec_obj.application_target, '%s' % geneec_obj.application_rate, '%s' % geneec_obj.number_of_applications,
                  '%s' % geneec_obj.interval_between_applications, '%s' % geneec_obj.Koc, '%s' % geneec_obj.aerobic_soil_metabolism, '%s' % geneec_obj.wet_in,
                  '%s' % geneec_obj.incorporation_depth, '%s' % geneec_obj.solubility, '%s' % geneec_obj.aerobic_aquatic_metabolism, '%s' % geneec_obj.photolysis_aquatic_half_life ],
        "Units": [ '', '', 'lbs a.i./A', '', 'days', 'mL/g OC', 'days', '', 'ft', 'mg/L', 'days', 'days' ]
    }
    return data

def gett2data(geneec_obj):
    data = { 
        "Parameter": [ 'Peak GEEC','Maximum 4-day Average GEEC','Maximum 21-day Average GEEC','Maximum 60-day Average GEEC','Maximum 90-day Average GEEC' ],
        "Value": [ '%.1f'%geneec_obj.output_val[0], '%.1f'%geneec_obj.output_val[1], '%.1f'%geneec_obj.output_val[2], '%.1f'%geneec_obj.output_val[3], '%.1f'%geneec_obj.output_val[4] ],
        "Units": [ 'ppb','ppb','ppb','ppb','ppb' ]
    }
    return data

def gett2data_qaqc(geneec_obj):
    data = { 
        "Parameter": [ 'Peak GEEC','Maximum 4-day Average GEEC','Maximum 21-day Average GEEC','Maximum 60-day Average GEEC','Maximum 90-day Average GEEC' ],
        "Value": [ '%.1f'%geneec_obj.output_val[0], '%.1f'%geneec_obj.output_val[1], '%.1f'%geneec_obj.output_val[2], '%.1f'%geneec_obj.output_val[3], '%.1f'%geneec_obj.output_val[4] ],
        "Expected Value": [ '%.1f'%geneec_obj.GEEC_peak_exp, '%.1f'%geneec_obj.GEEC_4avg_exp, '%.1f'%geneec_obj.GEEC_21avg_exp, '%.1f'%geneec_obj.GEEC_60avg_exp, '%.1f'%geneec_obj.GEEC_90avg_exp ],
        "Units": [ 'ppb','ppb','ppb','ppb','ppb' ]
    }
    return data

pvuheadings = getheaderpvu()
pvuheadingsqaqc = getheaderpvuqaqc()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(geneec_obj):
    table1_out = table_1(geneec_obj)
    table2_out = table_2(geneec_obj)
    html_all = table1_out + table2_out
    return html_all

def table_all_qaqc(geneec_obj):
    table1_out = table_1_qaqc(geneec_obj)
    table2_out = table_2_qaqc(geneec_obj)
    html_all = table1_out + table2_out
    return html_all

def timestamp(geneec_obj):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>GENEEC Version 2.0 (Beta)<br>
        <b>Computing Time = %.8ss<b><br>
    """%(geneec_obj.elapsed)
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_1(geneec_obj):
        if geneec_obj.application_method_label == 'Aerial Spray':
          t1data = gett1dataAerial(geneec_obj)
        if geneec_obj.application_method_label == 'Ground Spray':
          t1data = gett1dataGround(geneec_obj)
        if geneec_obj.application_method_label == 'Airblast Spray (Orchard & Vineyard)':
          t1data = gett1dataAirBlast(geneec_obj)
        if geneec_obj.application_method_label == 'Granular (Non-spray)':
          t1data = gett1dataGranular(geneec_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties: %s</H4>
                <div class="out_ container_output">
        """%geneec_obj.application_method_label
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html

def table_1_qaqc(geneec_obj):
        t1data = gett1dataAerial_qaqc(geneec_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Properties: %s</H4>
                <div class="out_ container_output">
        """%geneec_obj.application_method_label
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        <br>
        """
        return html

def table_2(geneec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
            <H4 class="out_2 collapsible" id="section3"><span></span>Generic Expected Environmental Concentration (GEEC)</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data(geneec_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2_qaqc(geneec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>Model Output</H3>
        <div class="out_">
            <H4 class="out_2 collapsible" id="section3"><span></span>Generic Expected Environmental Concentration (GEEC)</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data_qaqc(geneec_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

