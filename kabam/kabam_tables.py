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
        headings = ["Parameter",mark_safe("Total <br>(&#956;g/kg-ww)"),mark_safe("Lipid Normalized <br>(&#956;g/kg-lipid)"),mark_safe("Diet Contribution <br>(&#956;g/kg-ww)"),mark_safe("Respiration Contribution <br>(&#956;g/kg-ww)")]
        return headings

def getheaderttb():
        headings = ["Trophic Level",mark_safe("Total BCF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)"),mark_safe("Total BAF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)")]
        return headings

def getheadertbbbb():
        headings = ["Trophic Level",mark_safe("BCF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"),mark_safe("BAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"),mark_safe("BMF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)"),mark_safe("BSAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)")]
        return headings

def getheaderwbdwddd():
        headings = ["Wildlife Species","Body Weight (kg)","Dry Food Ingestion Rate (kg-dry food/kg-bw/day)","Wet Food Ingestion Rate (kg-wet food/kg-bw/day)","Drinking Water Intake (L/d)","Dose Based (mg/kg-bw/d)","Dietary Based (ppm)"]
        return headings

def getheaderwadadcdcd():
        headings = ["Wildlife Species","Acute Dose Based (mg/kg-bw)","Acute Dietary Based (mg/kg-diet)","Chronic Dose Based (mg/kg-bw)","Chronic Dietary Based (mg/kg-diet)"]
        return headings

def getheaderwadadcdcd_noUnits():
        headings = ["Wildlife Species","Acute Dose Based","Acute Dietary Based","Chronic Dose Based","Chronic Dietary Based"]
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
        "Value": [kabam_obj.chemical_name,kabam_obj.l_kow, kabam_obj.k_oc, (1e6 * kabam_obj.c_wdp), kabam_obj.water_column_EEC],
        "Units": ['','','L/kg OC',mark_safe('&#956;g/L'),mark_safe('&#956;g/L')],
    }
    return data

def gett1dataqaqc(kabam_obj):
    data = { 
        "Parameter": ['Chemical Name',mark_safe('Log K<sub>OW</sub>'),mark_safe('K<sub>OC</sub>'),'Pore Water EEC','Water Column EEC'],
        "Value": [kabam_obj.chemical_name_exp,kabam_obj.l_kow, kabam_obj.k_oc, (1e6 * kabam_obj.c_wdp), kabam_obj.water_column_EEC],
        "Units": ['','','L/kg OC',mark_safe('&#956;g/L'),mark_safe('&#956;g/L')],
    }
    return data

def gett2data(kabam_obj):
    data = { 
        "Parameter": ['Water Total','Water Freely Dissolved','Sediment Pore Water','Sediment in Solid','Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        mark_safe("Total <br>(&#956;g/kg-ww)"): [mark_safe('%.0f (&#956;g/L)' % kabam_obj.water_column_EEC),mark_safe('%.0f (&#956;g/L)' % kabam_obj.water_d),mark_safe('%.0f (&#956;g/L)' % (1e6*kabam_obj.c_wdp)),mark_safe('%.0f (&#956;g/kg-dw)' % (1e6*kabam_obj.c_s)),'%.0f' % (1e6*kabam_obj.cb_phytoplankton),'%.0f' % (1e6*kabam_obj.cb_zoo),'%.0f' % (1e6*kabam_obj.cb_beninv),'%.0f' % (1e6*kabam_obj.cb_ff),'%.0f' % (1e6*kabam_obj.cb_sf),'%.0f' % (1e6*kabam_obj.cb_mf),'%.0f' % (1e6*kabam_obj.cb_lf)],
        mark_safe("Lipid Normalized <br>(&#956;g/kg-lipid)"): ['N/A','N/A','N/A','N/A','%.0f' % kabam_obj.cbl_phytoplankton,'%.0f' % kabam_obj.cbl_zoo,'%.0f' % kabam_obj.cbl_beninv,'%.0f' % kabam_obj.cbl_ff,'%.0f' % kabam_obj.cbl_sf,'%.0f' % kabam_obj.cbl_mf,'%.0f' % kabam_obj.cbl_lf],
        mark_safe("Diet Contribution <br>(&#956;g/kg-ww)"): ['N/A','N/A','N/A','N/A','N/A','%.2f' % (1e6*kabam_obj.cbd_zoo),'%.2f' % (1e6*kabam_obj.cbd_beninv),'%.2f' % (1e6*kabam_obj.cbd_ff),'%.2f' % (1e6*kabam_obj.cbd_sf),'%.2f' % (1e6*kabam_obj.cbd_mf),'%.2f' % (1e6*kabam_obj.cbd_lf)],
        mark_safe("Respiration Contribution <br>(&#956;g/kg-ww)"): ['N/A','N/A','N/A','N/A','%.2f' % (1e6*kabam_obj.cbr_phytoplankton),'%.2f' % (1e6*kabam_obj.cbr_zoo),'%.2f' % (1e6*kabam_obj.cbr_beninv),'%.2f' % (1e6*kabam_obj.cbr_ff),'%.2f' % (1e6*kabam_obj.cbr_sf),'%.2f' % (1e6*kabam_obj.cbr_mf),'%.2f' % (1e6*kabam_obj.cbr_lf)],
    }
    return data
    # Removed: "Total": ['%.3f' % kabam_obj.water_column_EEC,'%.3f' % kabam_obj.water_d,'%.3f' % (1e6 * kabam_obj.c_wdp),'%.3f' % kabam_obj.c_s_f,'%.3f' % kabam_obj.cb_phytoplankton_f,'%.3f' % kabam_obj.cb_zoo_f,'%.3f' % kabam_obj.cb_beninv_f,'%.3f' % kabam_obj.cb_ff_f,'%.3f' % kabam_obj.cb_sf_f,'%.3f' % kabam_obj.cb_mf_f,'%.3f' % kabam_obj.cb_lf_f],
    # Removed: "Respiration Contribution": ['N/A','N/A','N/A','N/A','%.3f' % kabam_obj.cbr_phytoplankton,'%.3f' % kabam_obj.cbr_zoo,'%.3f' % kabam_obj.cbr_beninv,'%.3f' % kabam_obj.cbr_ff,'%.3f' % kabam_obj.cbr_sf,'%.3f' % kabam_obj.cbr_mf,'%.3f' % kabam_obj.cbr_lf],

def gett2dataqaqc(kabam_obj):
    data = { 
        "Parameter": ['Water Total','Water Freely Dissolved','Sediment Pore Water','Sediment in Solid','Phytoplankton','Expected Phytoplankton','Zooplankton','Expected Zooplankton','Benthic Invertebrates','Expected Benthic Invertebrates','Filter Feeders','Expected Filter Feeders','Small Fish','Expected Small Fish','Medium Fish','Expected Medium Fish','Large Fish','Expected Large Fish'],
        mark_safe("Total <br>(&#956;g/kg-ww)"): [mark_safe('%.0f (&#956;g/L)' % kabam_obj.water_column_EEC),mark_safe('%.0f (&#956;g/L)' % kabam_obj.water_d),mark_safe('%.0f (&#956;g/L)' % (1e6*kabam_obj.c_wdp)),mark_safe('%.0f (&#956;g/kg-dw)' % (1e6*kabam_obj.c_s)),'%.0f' % (1e6*kabam_obj.cb_phytoplankton),'%.0f' % kabam_obj.cb_phytoplankton_exp,'%.0f' % (1e6*kabam_obj.cb_zoo),'%.0f' % kabam_obj.cb_zoo_exp,'%.0f' % (1e6*kabam_obj.cb_beninv),'%.0f' % kabam_obj.cb_beninv_exp,'%.0f' % (1e6*kabam_obj.cb_ff),'%.0f' % kabam_obj.cb_ff_exp,'%.0f' % (1e6*kabam_obj.cb_sf),'%.0f' % kabam_obj.cb_sf_exp,'%.0f' % (1e6*kabam_obj.cb_mf),'%.0f' % kabam_obj.cb_mf_exp,'%.0f' % (1e6*kabam_obj.cb_lf),'%.0f' % kabam_obj.cb_lf_exp],
        mark_safe("Lipid Normalized <br>(&#956;g/kg-lipid)"): ['N/A','N/A','N/A','N/A','%.0f' % kabam_obj.cbl_phytoplankton,'%.0f' % kabam_obj.cbl_phytoplankton_exp,'%.0f' % kabam_obj.cbl_zoo,'%.0f' % kabam_obj.cbl_zoo_exp,'%.0f' % kabam_obj.cbl_beninv,'%.0f' % kabam_obj.cbl_beninv_exp,'%.0f' % kabam_obj.cbl_ff,'%.0f' % kabam_obj.cbl_ff_exp,'%.0f' % kabam_obj.cbl_sf,'%.0f' % kabam_obj.cbl_sf_exp,'%.0f' % kabam_obj.cbl_mf,'%.0f' % kabam_obj.cbl_mf_exp,'%.0f' % kabam_obj.cbl_lf,'%.0f' % kabam_obj.cbl_lf_exp],
        mark_safe("Diet Contribution <br>(&#956;g/kg-ww)"): ['N/A','N/A','N/A','N/A','N/A','N/A','%.2f' % (1e6*kabam_obj.cbd_zoo),'%.2f' % kabam_obj.cbd_zoo_exp,'%.2f' % (1e6*kabam_obj.cbd_beninv),'%.2f' % kabam_obj.cbd_beninv_exp,'%.2f' % (1e6*kabam_obj.cbd_ff),'%.2f' % kabam_obj.cbd_ff_exp,'%.2f' % (1e6*kabam_obj.cbd_sf),'%.2f' % kabam_obj.cbd_sf_exp,'%.2f' % (1e6*kabam_obj.cbd_mf),'%.2f' % kabam_obj.cbd_mf_exp,'%.2f' % (1e6*kabam_obj.cbd_lf),'%.2f' % kabam_obj.cbd_lf_exp],
        mark_safe("Respiration Contribution <br>(&#956;g/kg-ww)"): ['N/A','N/A','N/A','N/A','%.2f' % (1e6*kabam_obj.cbr_phytoplankton),'%.2f' % kabam_obj.cbr_phytoplankton_exp,'%.2f' % (1e6*kabam_obj.cbr_zoo),'%.2f' % kabam_obj.cbr_zoo_exp,'%.2f' % (1e6*kabam_obj.cbr_beninv),'%.2f' % kabam_obj.cbr_beninv_exp,'%.2f' % (1e6*kabam_obj.cbr_ff),'%.2f' % kabam_obj.cbr_ff_exp,'%.2f' % (1e6*kabam_obj.cbr_sf),'%.2f' % kabam_obj.cbr_sf_exp,'%.2f' % (1e6*kabam_obj.cbr_mf),'%.2f' % kabam_obj.cbr_mf_exp,'%.2f' % (1e6*kabam_obj.cbr_lf),'%.2f' % kabam_obj.cbr_lf_exp],
    }
    return data

def gett3data(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        mark_safe("Total BCF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbf_phytoplankton,'%.0f' % kabam_obj.cbf_zoo,'%.0f' % kabam_obj.cbf_beninv,'%.0f' % kabam_obj.cbf_ff,'%.0f' % kabam_obj.cbf_sf,'%.0f' % kabam_obj.cbf_mf,'%.0f' % kabam_obj.cbf_lf],
        mark_safe("Total BAF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbaf_phytoplankton,'%.0f' % kabam_obj.cbaf_zoo,'%.0f' % kabam_obj.cbaf_beninv,'%.0f' % kabam_obj.cbaf_ff,'%.0f' % kabam_obj.cbaf_sf,'%.0f' % kabam_obj.cbaf_mf,'%.0f' % kabam_obj.cbaf_lf],
    }
    return data

def gett3dataqaqc(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Expected Phytoplankton','Zooplankton','Expected Zooplankton','Benthic Invertebrates','Expected Benthic Invertebrates','Filter Feeders','Expected Filter Feeders','Small Fish','Expected Small Fish','Medium Fish','Expected Medium Fish','Large Fish','Expected Large Fish'],
        mark_safe("Total BCF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbf_phytoplankton,'%.0f' % kabam_obj.cbf_phytoplankton_exp,'%.0f' % kabam_obj.cbf_zoo,'%.0f' % kabam_obj.cbf_zoo_exp,'%.0f' % kabam_obj.cbf_beninv,'%.0f' % kabam_obj.cbf_beninv_exp,'%.0f' % kabam_obj.cbf_ff,'%.0f' % kabam_obj.cbf_ff_exp,'%.0f' % kabam_obj.cbf_sf,'%.0f' % kabam_obj.cbf_sf_exp,'%.0f' % kabam_obj.cbf_mf,'%.0f' % kabam_obj.cbf_mf_exp,'%.0f' % kabam_obj.cbf_lf,'%.0f' % kabam_obj.cbf_lf_exp],
        mark_safe("Total BAF <br>(&#956;g/kg-ww)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbaf_phytoplankton,'%.0f' % kabam_obj.cbaf_phytoplankton_exp,'%.0f' % kabam_obj.cbaf_zoo,'%.0f' % kabam_obj.cbaf_zoo_exp,'%.0f' % kabam_obj.cbaf_beninv,'%.0f' % kabam_obj.cbaf_beninv_exp,'%.0f' % kabam_obj.cbaf_ff,'%.0f' % kabam_obj.cbaf_ff_exp,'%.0f' % kabam_obj.cbaf_sf,'%.0f' % kabam_obj.cbaf_sf_exp,'%.0f' % kabam_obj.cbaf_mf,'%.0f' % kabam_obj.cbaf_mf_exp,'%.0f' % kabam_obj.cbaf_lf,'%.0f' % kabam_obj.cbaf_lf_exp],
    }
    return data

def gett4data(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Zooplankton','Benthic Invertebrates','Filter Feeders','Small Fish','Medium Fish','Large Fish'],
        mark_safe("BCF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbfl_phytoplankton,'%.0f' % kabam_obj.cbfl_zoo,'%.0f' % kabam_obj.cbfl_beninv,'%.0f' % kabam_obj.cbfl_ff,'%.0f' % kabam_obj.cbfl_sf,'%.0f' % kabam_obj.cbfl_mf,'%.0f' % kabam_obj.cbfl_lf],
        mark_safe("BAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbafl_phytoplankton,'%.0f' % kabam_obj.cbafl_zoo,'%.0f' % kabam_obj.cbafl_beninv,'%.0f' % kabam_obj.cbafl_ff,'%.0f' % kabam_obj.cbafl_sf,'%.0f' % kabam_obj.cbafl_mf,'%.0f' % kabam_obj.cbafl_lf],
        mark_safe("BMF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)"): ['N/A','%.2f' % kabam_obj.bmf_zoo,'%.2f' % kabam_obj.bmf_beninv,'%.2f' % kabam_obj.bmf_ff,'%.2f' % kabam_obj.bmf_sf,'%.2f' % kabam_obj.cbmf_mf,'%.2f' % kabam_obj.cbmf_lf],
        mark_safe("BSAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)"): ['%.0f' % kabam_obj.cbsafl_phytoplankton,'%.0f' % kabam_obj.cbsafl_zoo,'%.0f' % kabam_obj.cbsafl_beninv,'%.0f' % kabam_obj.cbsafl_ff,'%.0f' % kabam_obj.cbsafl_sf,'%.0f' % kabam_obj.cbsafl_mf,'%.0f' % kabam_obj.cbsafl_lf],
    }
    return data

def gett4dataqaqc(kabam_obj):
    data = { 
        "Trophic Level": ['Phytoplankton','Expected Phytoplankton','Zooplankton','Expected Zooplankton','Benthic Invertebrates','Expected Benthic Invertebrates','Filter Feeders','Expected Filter Feeders','Small Fish','Expected Small Fish','Medium Fish','Expected Medium Fish','Large Fish','Expected Large Fish'],
        mark_safe("BCF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbfl_phytoplankton,'%.0f' % kabam_obj.cbfl_phytoplankton_exp,'%.0f' % kabam_obj.cbfl_zoo,'%.0f' % kabam_obj.cbfl_zoo_exp,'%.0f' % kabam_obj.cbfl_beninv,'%.0f' % kabam_obj.cbfl_beninv_exp,'%.0f' % kabam_obj.cbfl_ff,'%.0f' % kabam_obj.cbfl_ff_exp,'%.0f' % kabam_obj.cbfl_sf,'%.0f' % kabam_obj.cbfl_sf_exp,'%.0f' % kabam_obj.cbfl_mf,'%.0f' % kabam_obj.cbfl_mf_exp,'%.0f' % kabam_obj.cbfl_lf,'%.0f' % kabam_obj.cbfl_lf_exp],
        mark_safe("BAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/L)"): ['%.0f' % kabam_obj.cbafl_phytoplankton,'%.0f' % kabam_obj.cbafl_phytoplankton_exp,'%.0f' % kabam_obj.cbafl_zoo,'%.0f' % kabam_obj.cbafl_zoo_exp,'%.0f' % kabam_obj.cbafl_beninv,'%.0f' % kabam_obj.cbafl_beninv_exp,'%.0f' % kabam_obj.cbafl_ff,'%.0f' % kabam_obj.cbafl_ff_exp,'%.0f' % kabam_obj.cbafl_sf,'%.0f' % kabam_obj.cbafl_sf_exp,'%.0f' % kabam_obj.cbafl_mf,'%.0f' % kabam_obj.cbafl_mf_exp,'%.0f' % kabam_obj.cbafl_lf,'%.0f' % kabam_obj.cbafl_lf_exp],
        mark_safe("BMF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)"): ['N/A','%.2f' % kabam_obj.bmf_zoo,'%.2f' % kabam_obj.bmf_zoo_exp,'%.2f' % kabam_obj.bmf_beninv,'%.2f' % kabam_obj.bmf_beninv_exp,'%.2f' % kabam_obj.bmf_ff,'%.2f' % kabam_obj.bmf_ff_exp,'%.2f' % kabam_obj.bmf_sf,'%.2f' % kabam_obj.bmf_sf_exp,'%.2f' % kabam_obj.cbmf_mf,'%.2f' % kabam_obj.cbmf_mf_exp,'%.2f' % kabam_obj.cbmf_lf,'%.2f' % kabam_obj.cbmf_lf_exp],
        mark_safe("BSAF <br>(&#956;g/kg-lipid)/<br>(&#956;g/kg-lipid)"): ['%.0f' % kabam_obj.cbsafl_phytoplankton,'%.0f' % kabam_obj.cbsafl_phytoplankton_exp,'%.0f' % kabam_obj.cbsafl_zoo,'%.0f' % kabam_obj.cbsafl_zoo_exp,'%.0f' % kabam_obj.cbsafl_beninv,'%.0f' % kabam_obj.cbsafl_beninv_exp,'%.0f' % kabam_obj.cbsafl_ff,'%.0f' % kabam_obj.cbsafl_ff_exp,'%.0f' % kabam_obj.cbsafl_sf,'%.0f' % kabam_obj.cbsafl_sf_exp,'%.0f' % kabam_obj.cbsafl_mf,'%.0f' % kabam_obj.cbsafl_mf_exp,'%.0f' % kabam_obj.cbsafl_lf,'%.0f' % kabam_obj.cbsafl_lf_exp],
    }
    return data

def gett5data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Body Weight (kg)": ['%.2f' % kabam_obj.mweight[:,0],'%.2f' % kabam_obj.mweight[:,1],'%.2f' % kabam_obj.mweight[:,2],'%.2f' % kabam_obj.mweight[:,3],'%.2f' % kabam_obj.mweight[:,4],'%.2f' % kabam_obj.mweight[:,5],'%.2f' % kabam_obj.aweight[:,0],'%.2f' % kabam_obj.aweight[:,1],'%.2f' % kabam_obj.aweight[:,2],'%.2f' % kabam_obj.aweight[:,3],'%.2f' % kabam_obj.aweight[:,4],'%.2f' % kabam_obj.aweight[:,5]],
        "Dry Food Ingestion Rate (kg-dry food/kg-bw/day)": ['%.3f' % kabam_obj.dfir[:,0],'%.3f' % kabam_obj.dfir[:,1],'%.3f' % kabam_obj.dfir[:,2],'%.3f' % kabam_obj.dfir[:,3],'%.3f' % kabam_obj.dfir[:,4],'%.3f' % kabam_obj.dfir[:,5],'%.3f' % kabam_obj.dfir_a[:,0],'%.3f' % kabam_obj.dfir_a[:,1],'%.3f' % kabam_obj.dfir_a[:,2],'%.3f' % kabam_obj.dfir_a[:,3],'%.3f' % kabam_obj.dfir_a[:,4],'%.3f' % kabam_obj.dfir_a[:,5]],
        "Wet Food Ingestion Rate (kg-wet food/kg-bw/day)": ['%.3f' % kabam_obj.wet_food_ingestion_m[:,0],'%.3f' % kabam_obj.wet_food_ingestion_m[:,1],'%.3f' % kabam_obj.wet_food_ingestion_m[:,2],'%.3f' % kabam_obj.wet_food_ingestion_m[:,3],'%.3f' % kabam_obj.wet_food_ingestion_m[:,4],'%.3f' % kabam_obj.wet_food_ingestion_m[:,5],'%.3f' % kabam_obj.wet_food_ingestion_a[:,0],'%.3f' % kabam_obj.wet_food_ingestion_a[:,1],'%.3f' % kabam_obj.wet_food_ingestion_a[:,2],'%.3f' % kabam_obj.wet_food_ingestion_a[:,3],'%.3f' % kabam_obj.wet_food_ingestion_a[:,4],'%.3f' % kabam_obj.wet_food_ingestion_a[:,5]],
        "Drinking Water Intake (L/d)": ['%.3f' % kabam_obj.drinking_water_intake_m[:,0],'%.3f' % kabam_obj.drinking_water_intake_m[:,1],'%.3f' % kabam_obj.drinking_water_intake_m[:,2],'%.3f' % kabam_obj.drinking_water_intake_m[:,3],'%.3f' % kabam_obj.drinking_water_intake_m[:,4],'%.3f' % kabam_obj.drinking_water_intake_m[:,5],'%.3f' % kabam_obj.drinking_water_intake_a[:,0],'%.3f' % kabam_obj.drinking_water_intake_a[:,1],'%.3f' % kabam_obj.drinking_water_intake_a[:,2],'%.3f' % kabam_obj.drinking_water_intake_a[:,3],'%.3f' % kabam_obj.drinking_water_intake_a[:,4],'%.3f' % kabam_obj.drinking_water_intake_a[:,5]],
        "Dose Based (mg/kg-bw/d)": ['%.3f' % kabam_obj.db4[:,0],'%.3f' % kabam_obj.db4[:,1],'%.3f' % kabam_obj.db4[:,2],'%.3f' % kabam_obj.db4[:,3],'%.3f' % kabam_obj.db4[:,4],'%.3f' % kabam_obj.db4[:,5],'%.3f' % kabam_obj.db4a[:,0],'%.3f' % kabam_obj.db4a[:,1],'%.3f' % kabam_obj.db4a[:,2],'%.3f' % kabam_obj.db4a[:,3],'%.3f' % kabam_obj.db4a[:,4],'%.3f' % kabam_obj.db4a[:,5]],
        "Dietary Based (ppm)": ['%.2f' % kabam_obj.db5[0],'%.2f' % kabam_obj.db5[1],'%.2f' % kabam_obj.db5[2],'%.2f' % kabam_obj.db5[3],'%.2f' % kabam_obj.db5[4],'%.2f' % kabam_obj.db5[5],'%.2f' % kabam_obj.db5a[0],'%.2f' % kabam_obj.db5a[1],'%.2f' % kabam_obj.db5a[2],'%.2f' % kabam_obj.db5a[3],'%.2f' % kabam_obj.db5a[4],'%.2f' % kabam_obj.db5a[5]],
    }
    return data

def gett5dataqaqc(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','Expected fog/water shrew','rice rate/star nosed mole','Expected rice rate/star nosed mole','small mink','Expected small mink','large mink','Expected large mink','small river otter','Expected small river otter','large river otter','Expected large river otter','sandpipers','Expected sandpipers','cranes','Expected cranes','rails','Expected rails','herons','Expected herons','small osprey','Expected small osprey','white pelican','Expected white pelican'],
        "Body Weight (kg)": ['%.2f' % kabam_obj.mweight[:,0],'%.2f' % kabam_obj.mweight0_exp,'%.2f' % kabam_obj.mweight[:,1],'%.2f' % kabam_obj.mweight1_exp,'%.2f' % kabam_obj.mweight[:,2],'%.2f' % kabam_obj.mweight2_exp,'%.2f' % kabam_obj.mweight[:,3],'%.2f' % kabam_obj.mweight3_exp,'%.2f' % kabam_obj.mweight[:,4],'%.2f' % kabam_obj.mweight4_exp,'%.2f' % kabam_obj.mweight[:,5],'%.2f' % kabam_obj.mweight5_exp,'%.2f' % kabam_obj.aweight[:,0],'%.2f' % kabam_obj.aweight0_exp,'%.2f' % kabam_obj.aweight[:,1],'%.2f' % kabam_obj.aweight1_exp,'%.2f' % kabam_obj.aweight[:,2],'%.2f' % kabam_obj.aweight2_exp,'%.2f' % kabam_obj.aweight[:,3],'%.2f' % kabam_obj.aweight3_exp,'%.2f' % kabam_obj.aweight[:,4],'%.2f' % kabam_obj.aweight4_exp,'%.2f' % kabam_obj.aweight[:,5],'%.2f' % kabam_obj.aweight5_exp],
        "Dry Food Ingestion Rate (kg-dry food/kg-bw/day)": ['%.3f' % kabam_obj.dfir[:,0],'%.3f' % kabam_obj.dfir0_exp,'%.3f' % kabam_obj.dfir[:,1],'%.3f' % kabam_obj.dfir1_exp,'%.3f' % kabam_obj.dfir[:,2],'%.3f' % kabam_obj.dfir2_exp,'%.3f' % kabam_obj.dfir[:,3],'%.3f' % kabam_obj.dfir3_exp,'%.3f' % kabam_obj.dfir[:,4],'%.3f' % kabam_obj.dfir4_exp,'%.3f' % kabam_obj.dfir[:,5],'%.3f' % kabam_obj.dfir5_exp,'%.3f' % kabam_obj.dfir_a[:,0],'%.3f' % kabam_obj.dfira0_exp,'%.3f' % kabam_obj.dfir_a[:,1],'%.3f' % kabam_obj.dfira1_exp,'%.3f' % kabam_obj.dfir_a[:,2],'%.3f' % kabam_obj.dfira2_exp,'%.3f' % kabam_obj.dfir_a[:,3],'%.3f' % kabam_obj.dfira3_exp,'%.3f' % kabam_obj.dfir_a[:,4],'%.3f' % kabam_obj.dfira4_exp,'%.3f' % kabam_obj.dfir_a[:,5],'%.3f' % kabam_obj.dfira5_exp],
        "Wet Food Ingestion Rate (kg-wet food/kg-bw/day)": ['%.3f' % kabam_obj.wet_food_ingestion_m[:,0],'%.3f' % kabam_obj.wet_food_ingestion_m0_exp,'%.3f' % kabam_obj.wet_food_ingestion_m[:,1],'%.3f' % kabam_obj.wet_food_ingestion_m1_exp,'%.3f' % kabam_obj.wet_food_ingestion_m[:,2],'%.3f' % kabam_obj.wet_food_ingestion_m2_exp,'%.3f' % kabam_obj.wet_food_ingestion_m[:,3],'%.3f' % kabam_obj.wet_food_ingestion_m3_exp,'%.3f' % kabam_obj.wet_food_ingestion_m[:,4],'%.3f' % kabam_obj.wet_food_ingestion_m4_exp,'%.3f' % kabam_obj.wet_food_ingestion_m[:,5],'%.3f' % kabam_obj.wet_food_ingestion_m5_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,0],'%.3f' % kabam_obj.wet_food_ingestion_a0_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,1],'%.3f' % kabam_obj.wet_food_ingestion_a1_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,2],'%.3f' % kabam_obj.wet_food_ingestion_a2_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,3],'%.3f' % kabam_obj.wet_food_ingestion_a3_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,4],'%.3f' % kabam_obj.wet_food_ingestion_a4_exp,'%.3f' % kabam_obj.wet_food_ingestion_a[:,5],'%.3f' % kabam_obj.wet_food_ingestion_a5_exp],
        "Drinking Water Intake (L/d)": ['%.3f' % kabam_obj.drinking_water_intake_m[:,0],'%.3f' % kabam_obj.drinking_water_intake_m0_exp,'%.3f' % kabam_obj.drinking_water_intake_m[:,1],'%.3f' % kabam_obj.drinking_water_intake_m1_exp,'%.3f' % kabam_obj.drinking_water_intake_m[:,2],'%.3f' % kabam_obj.drinking_water_intake_m2_exp,'%.3f' % kabam_obj.drinking_water_intake_m[:,3],'%.3f' % kabam_obj.drinking_water_intake_m3_exp,'%.3f' % kabam_obj.drinking_water_intake_m[:,4],'%.3f' % kabam_obj.drinking_water_intake_m4_exp,'%.3f' % kabam_obj.drinking_water_intake_m[:,5],'%.3f' % kabam_obj.drinking_water_intake_m5_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,0],'%.3f' % kabam_obj.drinking_water_intake_a0_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,1],'%.3f' % kabam_obj.drinking_water_intake_a1_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,2],'%.3f' % kabam_obj.drinking_water_intake_a2_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,3],'%.3f' % kabam_obj.drinking_water_intake_a3_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,4],'%.3f' % kabam_obj.drinking_water_intake_a4_exp,'%.3f' % kabam_obj.drinking_water_intake_a[:,5],'%.3f' % kabam_obj.drinking_water_intake_a5_exp],
        "Dose Based (mg/kg-bw/d)": ['%.3f' % kabam_obj.db4[:,0],'%.3f' % kabam_obj.db40_exp,'%.3f' % kabam_obj.db4[:,1],'%.3f' % kabam_obj.db41_exp,'%.3f' % kabam_obj.db4[:,2],'%.3f' % kabam_obj.db42_exp,'%.3f' % kabam_obj.db4[:,3],'%.3f' % kabam_obj.db43_exp,'%.3f' % kabam_obj.db4[:,4],'%.3f' % kabam_obj.db44_exp,'%.3f' % kabam_obj.db4[:,5],'%.3f' % kabam_obj.db45_exp,'%.3f' % kabam_obj.db4a[:,0],'%.3f' % kabam_obj.db4a0_exp,'%.3f' % kabam_obj.db4a[:,1],'%.3f' % kabam_obj.db4a1_exp,'%.3f' % kabam_obj.db4a[:,2],'%.3f' % kabam_obj.db4a2_exp,'%.3f' % kabam_obj.db4a[:,3],'%.3f' % kabam_obj.db4a3_exp,'%.3f' % kabam_obj.db4a[:,4],'%.3f' % kabam_obj.db4a4_exp,'%.3f' % kabam_obj.db4a[:,5],'%.3f' % kabam_obj.db4a5_exp],
        "Dietary Based (ppm)": ['%.2f' % kabam_obj.db5[0],'%.2f' % kabam_obj.db50_exp,'%.2f' % kabam_obj.db5[1],'%.2f' % kabam_obj.db51_exp,'%.2f' % kabam_obj.db5[2],'%.2f' % kabam_obj.db52_exp,'%.2f' % kabam_obj.db5[3],'%.2f' % kabam_obj.db53_exp,'%.2f' % kabam_obj.db5[4],'%.2f' % kabam_obj.db54_exp,'%.2f' % kabam_obj.db5[5],'%.2f' % kabam_obj.db55_exp,'%.2f' % kabam_obj.db5a[0],'%.2f' % kabam_obj.db5a0_exp,'%.2f' % kabam_obj.db5a[1],'%.2f' % kabam_obj.db5a1_exp,'%.2f' % kabam_obj.db5a[2],'%.2f' % kabam_obj.db5a2_exp,'%.2f' % kabam_obj.db5a[3],'%.2f' % kabam_obj.db5a3_exp,'%.2f' % kabam_obj.db5a[4],'%.2f' % kabam_obj.db5a4_exp,'%.2f' % kabam_obj.db5a[5],'%.2f' % kabam_obj.db5a5_exp],
    }
    return data

def gett6data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Acute Dose Based (mg/kg-bw)": ['%.2f' % kabam_obj.acute_dose_based_m[:,0],'%.2f' % kabam_obj.acute_dose_based_m[:,1],'%.2f' % kabam_obj.acute_dose_based_m[:,2],'%.2f' % kabam_obj.acute_dose_based_m[:,3],'%.2f' % kabam_obj.acute_dose_based_m[:,4],'%.2f' % kabam_obj.acute_dose_based_m[:,5],'%.2f' % kabam_obj.acute_dose_based_a[:,0],'%.2f' % kabam_obj.acute_dose_based_a[:,1],'%.2f' % kabam_obj.acute_dose_based_a[:,2],'%.2f' % kabam_obj.acute_dose_based_a[:,3],'%.2f' % kabam_obj.acute_dose_based_a[:,4],'%.2f' % kabam_obj.acute_dose_based_a[:,5]],
        "Acute Dietary Based (mg/kg-diet)": ['N/A','N/A','N/A','N/A','N/A','N/A','%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50],
        "Chronic Dose Based (mg/kg-bw)": ['%.2f' % kabam_obj.chronic_dose_based_m[:,0],'%.2f' % kabam_obj.chronic_dose_based_m[:,1],'%.2f' % kabam_obj.chronic_dose_based_m[:,2],'%.2f' % kabam_obj.chronic_dose_based_m[:,3],'%.2f' % kabam_obj.chronic_dose_based_m[:,4],'%.2f' % kabam_obj.chronic_dose_based_m[:,5],'N/A','N/A','N/A','N/A','N/A','N/A'],
        "Chronic Dietary Based (mg/kg-diet)": ['%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec],
    }
    return data

def gett6dataqaqc(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','Expected fog/water shrew','rice rate/star nosed mole','Expected rice rate/star nosed mole','small mink','Expected small mink','large mink','Expected large mink','small river otter','Expected small river otter','large river otter','Expected large river otter','sandpipers','Expected sandpipers','cranes','Expected cranes','rails','Expected rails','herons','Expected herons','small osprey','Expected small osprey','white pelican','Expected white pelican'],
        "Acute Dose Based (mg/kg-bw)": ['%.2f' % kabam_obj.acute_dose_based_m[:,0],'%.2f' % kabam_obj.acute_dose_based_m0_exp,'%.2f' % kabam_obj.acute_dose_based_m[:,1],'%.2f' % kabam_obj.acute_dose_based_m1_exp,'%.2f' % kabam_obj.acute_dose_based_m[:,2],'%.2f' % kabam_obj.acute_dose_based_m2_exp,'%.2f' % kabam_obj.acute_dose_based_m[:,3],'%.2f' % kabam_obj.acute_dose_based_m3_exp,'%.2f' % kabam_obj.acute_dose_based_m[:,4],'%.2f' % kabam_obj.acute_dose_based_m4_exp,'%.2f' % kabam_obj.acute_dose_based_m[:,5],'%.2f' % kabam_obj.acute_dose_based_m5_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,0],'%.2f' % kabam_obj.acute_dose_based_a0_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,1],'%.2f' % kabam_obj.acute_dose_based_a1_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,2],'%.2f' % kabam_obj.acute_dose_based_a2_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,3],'%.2f' % kabam_obj.acute_dose_based_a3_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,4],'%.2f' % kabam_obj.acute_dose_based_a4_exp,'%.2f' % kabam_obj.acute_dose_based_a[:,5],'%.2f' % kabam_obj.acute_dose_based_a5_exp],
        "Acute Dietary Based (mg/kg-diet)": ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp,'%.2f' % kabam_obj.avian_lc50,'%.2f' % kabam_obj.avian_lc50_exp],
        "Chronic Dose Based (mg/kg-bw)": ['%.2f' % kabam_obj.chronic_dose_based_m[:,0],'%.2f' % kabam_obj.chronic_dose_based_m0_exp,'%.2f' % kabam_obj.chronic_dose_based_m[:,1],'%.2f' % kabam_obj.chronic_dose_based_m1_exp,'%.2f' % kabam_obj.chronic_dose_based_m[:,2],'%.2f' % kabam_obj.chronic_dose_based_m2_exp,'%.2f' % kabam_obj.chronic_dose_based_m[:,3],'%.2f' % kabam_obj.chronic_dose_based_m3_exp,'%.2f' % kabam_obj.chronic_dose_based_m[:,4],'%.2f' % kabam_obj.chronic_dose_based_m4_exp,'%.2f' % kabam_obj.chronic_dose_based_m[:,5],'%.2f' % kabam_obj.chronic_dose_based_m5_exp,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'],
        "Chronic Dietary Based (mg/kg-diet)": ['%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint),'%.0f' % (20 * kabam_obj.mammalian_chronic_endpoint_exp),'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp,'%.0f' % kabam_obj.avian_noaec,'%.0f' % kabam_obj.avian_noaec_exp],
    }
    return data

def gett7data(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','rice rate/star nosed mole','small mink','large mink','small river otter','large river otter','sandpipers','cranes','rails','herons','small osprey','white pelican'],
        "Acute Dose Based": ['%.3f' % kabam_obj.acute_rq_dose_m[:,0],'%.3f' % kabam_obj.acute_rq_dose_m[:,1],'%.3f' % kabam_obj.acute_rq_dose_m[:,2],'%.3f' % kabam_obj.acute_rq_dose_m[:,3],'%.3f' % kabam_obj.acute_rq_dose_m[:,4],'%.3f' % kabam_obj.acute_rq_dose_m[:,5],'%.3f' % kabam_obj.acute_rq_dose_a[:,0],'%.3f' % kabam_obj.acute_rq_dose_a[:,1],'%.3f' % kabam_obj.acute_rq_dose_a[:,2],'%.3f' % kabam_obj.acute_rq_dose_a[:,3],'%.3f' % kabam_obj.acute_rq_dose_a[:,4],'%.3f' % kabam_obj.acute_rq_dose_a[:,5]],
        "Acute Dietary Based": ['N/A','N/A','N/A','N/A','N/A','N/A','%.3f' % kabam_obj.acute_rq_diet_a[0],'%.3f' % kabam_obj.acute_rq_diet_a[1],'%.3f' % kabam_obj.acute_rq_diet_a[2],'%.3f' % kabam_obj.acute_rq_diet_a[3],'%.3f' % kabam_obj.acute_rq_diet_a[4],'%.3f' % kabam_obj.acute_rq_diet_a[5]],
        "Chronic Dose Based": ['%.3f' % kabam_obj.chronic_rq_dose_m[:,0],'%.3f' % kabam_obj.chronic_rq_dose_m[:,1],'%.3f' % kabam_obj.chronic_rq_dose_m[:,2],'%.3f' % kabam_obj.chronic_rq_dose_m[:,3],'%.3f' % kabam_obj.chronic_rq_dose_m[:,4],'%.3f' % kabam_obj.chronic_rq_dose_m[:,5],'N/A','N/A','N/A','N/A','N/A','N/A'],
        "Chronic Dietary Based": ['%.3f' % kabam_obj.chronic_rq_diet_m[0],'%.3f' % kabam_obj.chronic_rq_diet_m[1],'%.3f' % kabam_obj.chronic_rq_diet_m[2],'%.3f' % kabam_obj.chronic_rq_diet_m[3],'%.3f' % kabam_obj.chronic_rq_diet_m[4],'%.3f' % kabam_obj.chronic_rq_diet_m[5],'%.3f' % kabam_obj.chronic_rq_diet_a[0],'%.3f' % kabam_obj.chronic_rq_diet_a[1],'%.3f' % kabam_obj.chronic_rq_diet_a[2],'%.3f' % kabam_obj.chronic_rq_diet_a[3],'%.3f' % kabam_obj.chronic_rq_diet_a[4],'%.3f' % kabam_obj.chronic_rq_diet_a[5]],
    }
    return data

def gett7dataqaqc(kabam_obj):
    data = { 
        "Wildlife Species": ['fog/water shrew','Expected fog/water shrew','rice rate/star nosed mole','Expected rice rate/star nosed mole','small mink','Expected small mink','large mink','Expected large mink','small river otter','Expected small river otter','large river otter','Expected large river otter','sandpipers','Expected sandpipers','cranes','Expected cranes','rails','Expected rails','herons','Expected herons','small osprey','Expected small osprey','white pelican','Expected white pelican'],
        "Acute Dose Based": ['%.3f' % kabam_obj.acute_rq_dose_m[:,0],'%.3f' % kabam_obj.acute_rq_dose_m0_exp,'%.3f' % kabam_obj.acute_rq_dose_m[:,1],'%.3f' % kabam_obj.acute_rq_dose_m1_exp,'%.3f' % kabam_obj.acute_rq_dose_m[:,2],'%.3f' % kabam_obj.acute_rq_dose_m2_exp,'%.3f' % kabam_obj.acute_rq_dose_m[:,3],'%.3f' % kabam_obj.acute_rq_dose_m3_exp,'%.3f' % kabam_obj.acute_rq_dose_m[:,4],'%.3f' % kabam_obj.acute_rq_dose_m4_exp,'%.3f' % kabam_obj.acute_rq_dose_m[:,5],'%.3f' % kabam_obj.acute_rq_dose_m5_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,0],'%.3f' % kabam_obj.acute_rq_dose_a0_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,1],'%.3f' % kabam_obj.acute_rq_dose_a1_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,2],'%.3f' % kabam_obj.acute_rq_dose_a2_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,3],'%.3f' % kabam_obj.acute_rq_dose_a3_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,4],'%.3f' % kabam_obj.acute_rq_dose_a4_exp,'%.3f' % kabam_obj.acute_rq_dose_a[:,5],'%.3f' % kabam_obj.acute_rq_dose_a5_exp],
        "Acute Dietary Based": ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','%.3f' % kabam_obj.acute_rq_diet_a[0],'%.3f' % kabam_obj.acute_rq_diet_a0_exp,'%.3f' % kabam_obj.acute_rq_diet_a[1],'%.3f' % kabam_obj.acute_rq_diet_a1_exp,'%.3f' % kabam_obj.acute_rq_diet_a[2],'%.3f' % kabam_obj.acute_rq_diet_a2_exp,'%.3f' % kabam_obj.acute_rq_diet_a[3],'%.3f' % kabam_obj.acute_rq_diet_a3_exp,'%.3f' % kabam_obj.acute_rq_diet_a[4],'%.3f' % kabam_obj.acute_rq_diet_a4_exp,'%.3f' % kabam_obj.acute_rq_diet_a[5],'%.3f' % kabam_obj.acute_rq_diet_a5_exp],
        "Chronic Dose Based": ['%.3f' % kabam_obj.chronic_rq_dose_m[:,0],'%.3f' % kabam_obj.chronic_rq_dose_m0_exp,'%.3f' % kabam_obj.chronic_rq_dose_m[:,1],'%.3f' % kabam_obj.chronic_rq_dose_m1_exp,'%.3f' % kabam_obj.chronic_rq_dose_m[:,2],'%.3f' % kabam_obj.chronic_rq_dose_m2_exp,'%.3f' % kabam_obj.chronic_rq_dose_m[:,3],'%.3f' % kabam_obj.chronic_rq_dose_m3_exp,'%.3f' % kabam_obj.chronic_rq_dose_m[:,4],'%.3f' % kabam_obj.chronic_rq_dose_m4_exp,'%.3f' % kabam_obj.chronic_rq_dose_m[:,5],'%.3f' % kabam_obj.chronic_rq_dose_m5_exp,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A'],
        "Chronic Dietary Based": ['%.3f' % kabam_obj.chronic_rq_diet_m[0],'%.3f' % kabam_obj.chronic_rq_diet_m0_exp,'%.3f' % kabam_obj.chronic_rq_diet_m[1],'%.3f' % kabam_obj.chronic_rq_diet_m1_exp,'%.3f' % kabam_obj.chronic_rq_diet_m[2],'%.3f' % kabam_obj.chronic_rq_diet_m2_exp,'%.3f' % kabam_obj.chronic_rq_diet_m[3],'%.3f' % kabam_obj.chronic_rq_diet_m3_exp,'%.3f' % kabam_obj.chronic_rq_diet_m[4],'%.3f' % kabam_obj.chronic_rq_diet_m4_exp,'%.3f' % kabam_obj.chronic_rq_diet_m[5],'%.3f' % kabam_obj.chronic_rq_diet_m5_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[0],'%.3f' % kabam_obj.chronic_rq_diet_a0_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[1],'%.3f' % kabam_obj.chronic_rq_diet_a1_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[2],'%.3f' % kabam_obj.chronic_rq_diet_a2_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[3],'%.3f' % kabam_obj.chronic_rq_diet_a3_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[4],'%.3f' % kabam_obj.chronic_rq_diet_a4_exp,'%.3f' % kabam_obj.chronic_rq_diet_a[5],'%.3f' % kabam_obj.chronic_rq_diet_a5_exp],
    }
    return data

pvuheadings = getheaderpvu()
headerptldr = getheaderptldr()
headerttb = getheaderttb()
headertbbbb = getheadertbbbb()
headerwbdwddd = getheaderwbdwddd()
headerwadadcdcd = getheaderwadadcdcd()
headerwadadcdcd_noUnits = getheaderwadadcdcd_noUnits()
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

def table_all_qaqc(kabam_obj):
    html_all = table_1_qaqc(kabam_obj)      
    html_all = html_all + table_2_qaqc(kabam_obj)
    html_all = html_all + table_3_qaqc(kabam_obj)
    html_all = html_all + table_4_qaqc(kabam_obj)
    html_all = html_all + table_5_qaqc(kabam_obj)
    html_all = html_all + table_6_qaqc(kabam_obj)
    html_all = html_all + table_7_qaqc(kabam_obj)
    return html_all

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

def table_1_qaqc(kabam_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Chemical Information</H4>
                <div class="out_ container_output">
        """
        t1data = gett1dataqaqc(kabam_obj)
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
            <H4 class="out_1 collapsible" id="section4"><span></span>Estimated concentrations of %s in ecosystem components</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t2data = gett2data(kabam_obj)
        t2rows = gethtmlrowsfromcols(t2data,headerptldr)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=headerptldr)))
        html = html + """
                </div>
        """
        return html

def table_2_qaqc(kabam_obj):
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section1"><span></span>Kabam Output</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section4"><span></span>Estimated concentrations of %s in ecosystem components</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t2data = gett2dataqaqc(kabam_obj)
        t2rows = gethtmlrowsfromcols(t2data,headerptldr)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=headerptldr)))
        html = html + """
                </div>
        """
        return html

def table_3(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Total BCF and BAF values of %s in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t3data = gett3data(kabam_obj)
        t3rows = gethtmlrowsfromcols(t3data,headerttb)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=headerttb)))
        html = html + """
                </div>
        """
        return html

def table_3_qaqc(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Total BCF and BAF values of %s in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t3data = gett3dataqaqc(kabam_obj)
        t3rows = gethtmlrowsfromcols(t3data,headerttb)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=headerttb)))
        html = html + """
                </div>
        """
        return html

def table_4(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Lipid-normalized BCF, BAF, BMF, and BSAF values of %s in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name)
        t4data = gett4data(kabam_obj)
        t4rows = gethtmlrowsfromcols(t4data,headertbbbb)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=headertbbbb)))
        html = html + """
                </div>
        """
        return html

def table_4_qaqc(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Lipid-normalized BCF, BAF, BMF, and BSAF values of %s in Aquatic Trophic Levels</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t4data = gett4dataqaqc(kabam_obj)
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

def table_5_qaqc(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of EECs for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t5data = gett5dataqaqc(kabam_obj)
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

def table_6_qaqc(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of toxicity values for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t6data = gett6dataqaqc(kabam_obj)
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
        t7rows = gethtmlrowsfromcols(t7data,headerwadadcdcd_noUnits)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=headerwadadcdcd_noUnits)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_7_qaqc(kabam_obj):
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Calculation of RQ values for mammals and birds consuming fish contaminated by %s</H4>
                <div class="out_ container_output">
        """%(kabam_obj.chemical_name_exp)
        t7data = gett7dataqaqc(kabam_obj)
        t7rows = gethtmlrowsfromcols(t7data,headerwadadcdcd_noUnits)
        html = html + tmpl.render(Context(dict(data=t7rows, headings=headerwadadcdcd_noUnits)))
        html = html + """
                </div>
        </div>
        """
        return html