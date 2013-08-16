import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from kabam import kabam_model,kabam_parameters
import logging
import time
import datetime

logger = logging.getLogger("KabamTables")

def getheaderpvu():
        headings = ["Parameter","Value","Units"]
        return headings

def getheaderptldr():
        headings = ["Parameter","Total","Lipid Normalized","Diet Contribution","Respiration Contribution"]
        return headings

# def getheaderptldrqaqc():
#         headings = ["Parameter","Total","Total-Expected","Lipid Normalized","Lipid Normalized-Expected","Diet Contribution","Diet Contribution-Expected","Respiration Contribution","Respiration Contribution-Expected"]
#         return headings

def getheaderttb():
        headings = ["Trophic Level","Total BCF","Total BAF"]
        return headings

# def getheaderttbqaqc():
#         headings = ["Trophic Level","Total BCF","Total BCF-Expected","Total BAF","Total BAF-Expected"]
#         return headings

def getheadertbbbb():
        headings = ["Trophic Level","BCF","BAF","BMF","BSAF"]
        return headings

# def getheadertbbbbqaqc():
#         headings = ["Trophic Level","BCF","BCF-Expected","BAF","BAF-Expected","BMF","BMF-Expected","BSAF","BSAF-Expected"]
#         return headings

def getheaderwbdwddd():
        headings = ["Wildlife Species","Body Weight (kg)","Dry Food Ingestion Rate (kg-dry food/kg-bw/day)","Wet Food Ingestion Rate (kg-wet food/kg-bw/day)","Drinking Water Intake (L/d)","Dose Based (mg/kg-bw/d)","Dietary Based (ppm)"]
        return headings

def getheaderwadadcdcd():
        headings = ["Wildlife Species","Acute Dose Based (mg/kg-bw)","Acute Dietary Based (mg/kg-diet)","Chronic Dose Based (mg/kg-bw)","Chronic Dietary Based (mg/kg-diet)"]
        return headings

# def getheadersum():
#     headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
#     return headings

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


def gett1data(kabam_obj):
    data = { 
        "Parameter": ['Chemical Name',mark_safe('Log K<sub>OW</sub>'),mark_safe('K<sub>OC</sub>'),'Pore Water EEC','Water Column EEC'],
        "Value": [kabam_obj.chemical_name,kabam_obj.l_kow, kabam_obj.k_oc, kabam_obj.c_wdp_2, kabam_obj.water_column_EEC],
        "Units": ['','','L/kg OC',mark_safe('&#956;g/L'),mark_safe('&#956;g/L')],
    }
    return data

# def gett1dataqaqc(kabam_obj):
#     data = { 
#         "Parameter": ['Chemical Name',mark_safe('Log K<sub>OW</sub>'),mark_safe('K<sub>OC</sub>'),'Pore Water EEC','Water Column EEC'],
#         "Value": [kabam_obj.chemical_name,],
#         "Units": ['','','L/kg OC',mark_safe('&#956;g/L'),mark_safe('&#956;g/L')],
#     }
#     return data

def gett2data(kabam_obj):
    data = { 
        "Parameter": ['Water Total','Water Freely Dissolved','Sediment Pore Water','Sediment in Solid','Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        "Total": ['%.0f' % kabam_obj.water_column_EEC,'%.0f' % kabam_obj.water_d,'%.0f' % (1e6*kabam_obj.c_wdp_2),'%.0f' % (1e6*kabam_obj.c_s),'%.0f' % (1e6*kabam_obj.cb_phytoplankton),'%.0f' % (1e6*kabam_obj.cb_zoo),'%.0f' % (1e6*kabam_obj.cb_beninv),'%.0f' % (1e6*kabam_obj.cbf_ff),'%.0f' % (1e6*kabam_obj.cb_sf),'%.0f' % (1e6*kabam_obj.cb_mf),'%.0f' % (1e6*kabam_obj.cb_lf)],
        "Lipid Normalized": ['NA','NA','NA','NA','%.0f' % kabam_obj.cbl_phytoplankton,'%.0f' % kabam_obj.cbl_zoo,'%.0f' % kabam_obj.cbl_beninv,'%.0f' % kabam_obj.cbl_ff,'%.0f' % kabam_obj.cbl_sf,'%.0f' % kabam_obj.cbl_mf,'%.0f' % kabam_obj.cbl_lf],
        "Diet Contribution": ['NA','NA','NA','NA','NA','%.2f' % (1e6*kabam_obj.cbd_zoo),'%.2f' % (1e6*kabam_obj.cbd_beninv),'%.2f' % (1e6*kabam_obj.cbd_ff),'%.2f' % (1e6*kabam_obj.cbd_sf),'%.2f' % (1e6*kabam_obj.cbd_mf),'%.2f' % (1e6*kabam_obj.cbd_lf)],
        "Respiration Contribution": ['NA','NA','NA','NA','removed','%.2f' % (1e6*kabam_obj.cbr_zoo),'%.2f' % (1e6*kabam_obj.cbr_beninv),'%.2f' % (1e6*kabam_obj.cbr_ff),'%.2f' % (1e6*kabam_obj.cbr_sf),'%.2f' % (1e6*kabam_obj.cbr_mf),'%.2f' % (1e6*kabam_obj.cbr_lf)],
    }
    return data
    # Removed: "Total": ['%.3f' % kabam_obj.water_column_EEC,'%.3f' % kabam_obj.water_d,'%.3f' % kabam_obj.c_wdp_2,'%.3f' % kabam_obj.c_s_f,'%.3f' % kabam_obj.cb_phytoplankton_f,'%.3f' % kabam_obj.cb_zoo_f,'%.3f' % kabam_obj.cb_beninv_f,'%.3f' % kabam_obj.cb_ff_f,'%.3f' % kabam_obj.cb_sf_f,'%.3f' % kabam_obj.cb_mf_f,'%.3f' % kabam_obj.cb_lf_f],
    # Removed: "Respiration Contribution": ['NA','NA','NA','NA','%.3f' % kabam_obj.cbr_phytoplankton,'%.3f' % kabam_obj.cbr_zoo,'%.3f' % kabam_obj.cbr_beninv,'%.3f' % kabam_obj.cbr_ff,'%.3f' % kabam_obj.cbr_sf,'%.3f' % kabam_obj.cbr_mf,'%.3f' % kabam_obj.cbr_lf],

# def gett2dataqaqc(kabam_obj):
#     data = { 
#         "Parameter": ['Water Total','Water Freely Dissolved','Sediment Pore Water','Sediment in Solid','Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
#         "Total": [kabam_obj.,],
#         "Lipid Normalized": [kabam_obj.,],
#         "Diet Contribution": [kabam_obj.,],
#         "Respiration Contribution": [kabam_obj.,],
#         "Units": ['%','%','%','%','%','%','%','%','%','%','%'],
#     }
#     return data

def gett3data(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        "Total BCF": ['%.2f' % kabam_obj.cbcf_phytoplankton,'%.2f' % kabam_obj.cbf_zoo,'%.2f' % kabam_obj.cbf_beninv,'%.2f' % kabam_obj.cbf_ff,'%.2f' % kabam_obj.cbf_sf,'%.2f' % kabam_obj.cbf_mf,'%.2f' % kabam_obj.cbf_lf],
        "Total BAF": ['%.2f' % kabam_obj.cbaf_phytoplankton,'%.2f' % kabam_obj.cbaf_zoo,'%.2f' % kabam_obj.cbaf_beninv,'%.2f' % kabam_obj.cbaf_ff,'%.2f' % kabam_obj.cbaf_sf,'%.2f' % kabam_obj.cbaf_mf,'%.2f' % kabam_obj.cbaf_lf],
    }
    return data

# def gett3dataqaqc(kabam_obj):
#     data = { 
#         "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
#         "Total BCF": [kabam_obj.,],
#         "Total BCF-Expected": [kabam_obj.,],
#         "Total BAF": [kabam_obj.,],
#         "Total BAF-Expected": [kabam_obj.,],
#     }
#     return data

def gett4data(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        "BCF": ['%.2f' % kabam_obj.cbcfl_phytoplankton,'%.2f' % kabam_obj.cbfl_zoo,'%.2f' % kabam_obj.cbfl_beninv,'%.2f' % kabam_obj.cbfl_ff,'%.2f' % kabam_obj.cbfl_sf,'%.2f' % kabam_obj.cbfl_mf,'%.2f' % kabam_obj.cbfl_lf],
        "BAF": ['%.2f' % kabam_obj.cbafl_phytoplankton,'%.2f' % kabam_obj.cbafl_zoo,'%.2f' % kabam_obj.cbafl_beninv,'%.2f' % kabam_obj.cbafl_ff,'%.2f' % kabam_obj.cbafl_sf,'%.2f' % kabam_obj.cbafl_mf,'%.2f' % kabam_obj.cbafl_lf],
        "BMF": ['NA','%.2f' % kabam_obj.bmf_zoo,'%.2f' % kabam_obj.bmf_beninv,'%.2f' % kabam_obj.bmf_ff,'%.2f' % kabam_obj.bmf_sf,'%.2f' % kabam_obj.cbmf_mf,'%.2f' % kabam_obj.cbmf_lf],
        "BSAF": ['%.2f' % kabam_obj.cbsafl_phytoplankton,'%.2f' % kabam_obj.cbsafl_zoo,'%.2f' % kabam_obj.cbsafl_beninv,'%.2f' % kabam_obj.cbsafl_ff,'%.2f' % kabam_obj.cbsafl_sf,'%.2f' % kabam_obj.cbsafl_mf,'%.2f' % kabam_obj.cbsafl_lf],
    }
    return data

# def gett4dataqaqc(kabam_obj):
#     data = { 
#         "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
#         "BCF": [kabam_obj.,],
#         "BCF-Expected": [kabam_obj.,],
#         "BAF": [kabam_obj.,],
#         "BAF-Expected": [kabam_obj.,],
#         "BMF": [kabam_obj.,],
#         "BMF-Expected": [kabam_obj.,],
#         "BSAF": [kabam_obj.,],
#         "BSAF-Expected": [kabam_obj.,],
#     }
#     return data

def gett5data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Body Weight (kg)": ['%.2f' % kabam_obj.mweight[:,0],'%.2f' % kabam_obj.mweight[:,1],'%.2f' % kabam_obj.mweight[:,2],'%.2f' % kabam_obj.mweight[:,3],'%.2f' % kabam_obj.mweight[:,4],'%.2f' % kabam_obj.mweight[:,5],'%.2f' % kabam_obj.aweight[:,0],'%.2f' % kabam_obj.aweight[:,1],'%.2f' % kabam_obj.aweight[:,2],'%.2f' % kabam_obj.aweight[:,3],'%.2f' % kabam_obj.aweight[:,4],'%.2f' % kabam_obj.aweight[:,5]],
        "Dry Food Ingestion Rate (kg-dry food/kg-bw/day)": ['%.2f' % kabam_obj.dfir[:,0],'%.2f' % kabam_obj.dfir[:,1],'%.2f' % kabam_obj.dfir[:,2],'%.2f' % kabam_obj.dfir[:,3],'%.2f' % kabam_obj.dfir[:,4],'%.2f' % kabam_obj.dfir[:,5],'%.2f' % kabam_obj.dfir_a[:,0],'%.2f' % kabam_obj.dfir_a[:,1],'%.2f' % kabam_obj.dfir_a[:,2],'%.2f' % kabam_obj.dfir_a[:,3],'%.2f' % kabam_obj.dfir_a[:,4],'%.2f' % kabam_obj.dfir_a[:,5]],
        "Wet Food Ingestion Rate (kg-wet food/kg-bw/day)": ['%.2f' % kabam_obj.wet_food_ingestion_m[:,0],'%.2f' % kabam_obj.wet_food_ingestion_m[:,1],'%.2f' % kabam_obj.wet_food_ingestion_m[:,2],'%.2f' % kabam_obj.wet_food_ingestion_m[:,3],'%.2f' % kabam_obj.wet_food_ingestion_m[:,4],'%.2f' % kabam_obj.wet_food_ingestion_m[:,5],'%.2f' % kabam_obj.wet_food_ingestion_a[:,0],'%.2f' % kabam_obj.wet_food_ingestion_a[:,1],'%.2f' % kabam_obj.wet_food_ingestion_a[:,2],'%.2f' % kabam_obj.wet_food_ingestion_a[:,3],'%.2f' % kabam_obj.wet_food_ingestion_a[:,4],'%.2f' % kabam_obj.wet_food_ingestion_a[:,5]],
        "Drinking Water Intake (L/d)": ['%.2f' % kabam_obj.drinking_water_intake_m[:,0],'%.2f' % kabam_obj.drinking_water_intake_m[:,1],'%.2f' % kabam_obj.drinking_water_intake_m[:,2],'%.2f' % kabam_obj.drinking_water_intake_m[:,3],'%.2f' % kabam_obj.drinking_water_intake_m[:,4],'%.2f' % kabam_obj.drinking_water_intake_m[:,5],'%.2f' % kabam_obj.drinking_water_intake_a[:,0],'%.2f' % kabam_obj.drinking_water_intake_a[:,1],'%.2f' % kabam_obj.drinking_water_intake_a[:,2],'%.2f' % kabam_obj.drinking_water_intake_a[:,3],'%.2f' % kabam_obj.drinking_water_intake_a[:,4],'%.2f' % kabam_obj.drinking_water_intake_a[:,5]],
        "Dose Based (mg/kg-bw/d)": ['%.2f' % kabam_obj.db4[:,0],'%.2f' % kabam_obj.db4[:,1],'%.2f' % kabam_obj.db4[:,2],'%.2f' % kabam_obj.db4[:,3],'%.2f' % kabam_obj.db4[:,4],'%.2f' % kabam_obj.db4[:,5],'%.2f' % kabam_obj.db4a[:,0],'%.2f' % kabam_obj.db4a[:,1],'%.2f' % kabam_obj.db4a[:,2],'%.2f' % kabam_obj.db4a[:,3],'%.2f' % kabam_obj.db4a[:,4],'%.2f' % kabam_obj.db4a[:,5]],
        "Dietary Based (ppm)": ['%.2f' % kabam_obj.db5[0],'%.2f' % kabam_obj.db5[1],'%.2f' % kabam_obj.db5[2],'%.2f' % kabam_obj.db5[3],'%.2f' % kabam_obj.db5[4],'%.2f' % kabam_obj.db5[5],'%.2f' % kabam_obj.db5a[0],'%.2f' % kabam_obj.db5a[1],'%.2f' % kabam_obj.db5a[2],'%.2f' % kabam_obj.db5a[3],'%.2f' % kabam_obj.db5a[4],'%.2f' % kabam_obj.db5a[5]],
    }
    return data

# def gett5dataqaqc(kabam_obj):
#     data = { 
#         "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
#         "Body Weight (kg)": [kabam_obj.,],
#         "Body Weight (kg)-Expected": [kabam_obj.,],
#         "Dry Food Ingestion Rate (kg-dry food/kg-bw/day)": [kabam_obj.,],
#         "Dry Food Ingestion Rate (kg-dry food/kg-bw/day)-Expected": [kabam_obj.,],
#         "Wet Food Ingestion Rate (kg-wet food/kg-bw/day)": [kabam_obj.,],
#         "Wet Food Ingestion Rate (kg-wet food/kg-bw/day)-Expected": [kabam_obj.,],
#         "Drinking Water Intake (L/d)": [kabam_obj.,],
#         "Drinking Water Intake (L/d)-Expected": [kabam_obj.,],
#         "Dose Based (mg/kg-bw/d)": [],
#         "Dose Based (mg/kg-bw/d)-Expected": [],
#         "Dietary Based (ppm)": [],
#         "Dietary Based (ppm)-Expected": [],
#     }
#     return data

def gett6data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Acute Dose Based (mg/kg-bw)": [kabam_obj.acute_dose_based_m[:,0][0],kabam_obj.acute_dose_based_m[:,1][0],kabam_obj.acute_dose_based_m[:,2][0],kabam_obj.acute_dose_based_m[:,3][0],kabam_obj.acute_dose_based_m[:,4][0],kabam_obj.acute_dose_based_m[:,5][0],kabam_obj.acute_dose_based_a[:,0][0],kabam_obj.acute_dose_based_a[:,1][0],kabam_obj.acute_dose_based_a[:,2][0],kabam_obj.acute_dose_based_a[:,3][0],kabam_obj.acute_dose_based_a[:,4][0],kabam_obj.acute_dose_based_a[:,0][0]],
        "Acute Dietary Based (mg/kg-diet)": [kabam_obj.mammalian_ld50,kabam_obj.mammalian_ld50,kabam_obj.mammalian_ld50,kabam_obj.mammalian_ld50,kabam_obj.mammalian_ld50,kabam_obj.mammalian_ld50,kabam_obj.avian_ld50,kabam_obj.avian_ld50,kabam_obj.avian_ld50,kabam_obj.avian_ld50,kabam_obj.avian_ld50,kabam_obj.avian_ld50],
        "Chronic Dose Based (mg/kg-bw)": [kabam_obj.chronic_dose_based_m[:,0][0],kabam_obj.chronic_dose_based_m[:,1][0],kabam_obj.chronic_dose_based_m[:,2][0],kabam_obj.chronic_dose_based_m[:,3][0],kabam_obj.chronic_dose_based_m[:,4][0],kabam_obj.chronic_dose_based_m[:,5][0],'NA','NA','NA','NA','NA','NA'],
        "Chronic Dietary Based (mg/kg-diet)": [kabam_obj.mammalian_chronic_endpoint,kabam_obj.mammalian_chronic_endpoint,kabam_obj.mammalian_chronic_endpoint,kabam_obj.mammalian_chronic_endpoint,kabam_obj.mammalian_chronic_endpoint,kabam_obj.mammalian_chronic_endpoint,kabam_obj.avian_lc50,kabam_obj.avian_lc50,kabam_obj.avian_lc50,kabam_obj.avian_lc50,kabam_obj.avian_lc50,kabam_obj.avian_lc50],
    }
    return data

def gett7data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Acute Dose Based (mg/kg-bw)": [kabam_obj.acute_rq_dose_m[:,0][0],kabam_obj.acute_rq_dose_m[:,1][0],kabam_obj.acute_rq_dose_m[:,2][0],kabam_obj.acute_rq_dose_m[:,3][0],kabam_obj.acute_rq_dose_m[:,4][0],kabam_obj.acute_rq_dose_m[:,5][0],kabam_obj.acute_rq_dose_a[:,0][0],kabam_obj.acute_rq_dose_a[:,1][0],kabam_obj.acute_rq_dose_a[:,2][0],kabam_obj.acute_rq_dose_a[:,3][0],kabam_obj.acute_rq_dose_a[:,4][0],kabam_obj.acute_rq_dose_a[:,5][0]],
        "Acute Dietary Based (mg/kg-diet)": [kabam_obj.acute_rq_diet_m[0],kabam_obj.acute_rq_diet_m[1],kabam_obj.acute_rq_diet_m[2],kabam_obj.acute_rq_diet_m[3],kabam_obj.acute_rq_diet_m[4],kabam_obj.acute_rq_diet_m[5],kabam_obj.acute_rq_diet_a[0],kabam_obj.acute_rq_diet_a[1],kabam_obj.acute_rq_diet_a[2],kabam_obj.acute_rq_diet_a[3],kabam_obj.acute_rq_diet_a[4],kabam_obj.acute_rq_diet_a[5]],
        "Chronic Dose Based (mg/kg-bw)": [kabam_obj.chronic_rq_dose_m[:,0][0],kabam_obj.chronic_rq_dose_m[:,1][0],kabam_obj.chronic_rq_dose_m[:,2][0],kabam_obj.chronic_rq_dose_m[:,3][0],kabam_obj.chronic_rq_dose_m[:,4][0],kabam_obj.chronic_rq_dose_m[:,5][0],'NA','NA','NA','NA','NA','NA'],
        "Chronic Dietary Based (mg/kg-diet)": [kabam_obj.chronic_rq_diet_m[0],kabam_obj.chronic_rq_diet_m[1],kabam_obj.chronic_rq_diet_m[2],kabam_obj.chronic_rq_diet_m[3],kabam_obj.chronic_rq_diet_m[4],kabam_obj.chronic_rq_diet_m[5],kabam_obj.chronic_rq_diet_a[0],kabam_obj.chronic_rq_diet_a[1],kabam_obj.chronic_rq_diet_a[2],kabam_obj.chronic_rq_diet_a[3],kabam_obj.chronic_rq_diet_a[4],kabam_obj.chronic_rq_diet_a[5]],
    }
    return data

pvuheadings = getheaderpvu()
headerptldr = getheaderptldr()
# headerptldrqaqc = getheaderptldrqaqc()
headerttb = getheaderttb()
# headerttbqaqc = getheaderttbqaqc()
headertbbbb = getheadertbbbb()
# headertbbbbqaqc = getheadertbbbbqaqc()
headerwbdwddd = getheaderwbdwddd()
headerwadadcdcd = getheaderwadadcdcd()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(kabam_obj):
    html_all = table_1(kabam_obj)      
    html_all = html_all + table_2(kabam_obj)
    html_all = html_all + table_3(kabam_obj)
    html_all = html_all + table_4(kabam_obj)
    html_all = html_all + table_5(kabam_obj)
    html_all = html_all + table_6(kabam_obj)
    html_all = html_all + table_7(kabam_obj)
    return html_all

# def table_all_qaqc(kabam_obj):
#     html_all = table_1_qaqc(kabam_obj)
#     html_all = html_all + table_2_qaqc(kabam_obj)
#     html_all = html_all + table_3_qaqc(kabam_obj)
#     return html_all

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Kabam Version 1.0 (Beta)<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_1(kabam_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Information</H4>
                <div class="out_ container_output">
        """
        t1data = gett1data(kabam_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(kabam_obj):
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section1"><span></span>Kabam Output</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Ecosystem Components (%)</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data(kabam_obj)
        t2rows = gethtmlrowsfromcols(t2data,headerptldr)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=headerptldr)))
        html = html + """
                </div>
        """
        return html

def table_3(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Total BCF and BAF Values in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """
        t3data = gett3data(kabam_obj)
        t3rows = gethtmlrowsfromcols(t3data,headerttb)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=headerttb)))
        html = html + """
                </div>
        """
        return html

def table_4(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Lipid-normalized BCF, BAF, BMF, and BSAF Values in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """
        t4data = gett4data(kabam_obj)
        t4rows = gethtmlrowsfromcols(t4data,headertbbbb)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=headertbbbb)))
        html = html + """
                </div>
        """
        return html

def table_5(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of EECs for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t5data = gett5data(kabam_obj)
        t5rows = gethtmlrowsfromcols(t5data,headerwbdwddd)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=headerwbdwddd)))
        html = html + """
                </div>
        """
        return html

def table_6(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of toxicity values for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t6data = gett6data(kabam_obj)
        t6rows = gethtmlrowsfromcols(t6data,headerwadadcdcd)
        html = html + tmpl.render(Context(dict(data=t6rows, headings=headerwadadcdcd)))
        html = html + """
                </div>
        """
        return html

def table_7(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of RQ values for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t7data = gett7data(kabam_obj)
        t7rows = gethtmlrowsfromcols(t7data,headerwadadcdcd)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=headerwadadcdcd)))
        html = html + """
                </div>
        </div>
        """
        return html
