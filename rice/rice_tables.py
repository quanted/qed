from django.template import Context, Template
from django.utils.safestring import mark_safe
# import rice_model,rice_parameters
import logging

logger = logging.getLogger("RiceTables")

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvuqaqc():
    headings = ["Parameter", "Value", "Expected-Value", "Units"]
    return headings

def getheadersum():
    headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
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

def gett1data(rice_obj):
    data = { 
        "Parameter": ['Chemical Name','Mass applied to patty','Area of patty','Sediment Depth','Sediment bulk density','Water column depth','Sediment porosity','Water-Sediment partitioning coefficient'],
        "Value": [rice_obj.chemical_name,rice_obj.mai,rice_obj.a,rice_obj.dsed,rice_obj.pb,rice_obj.dw,rice_obj.osed,rice_obj.kd],
        "Units": ['','kg',mark_safe('m<sup>2</sup>'),'m',mark_safe('kg/m<sup>3</sup>'),'m','','L/kg'],
    }
    return data

def gett1dataqaqc(rice_obj):
    data = { 
        "Parameter": ['Chemical Name','Mass applied to patty','Area of patty','Sediment Depth','Sediment bulk density','Water column depth','Sediment porosity','Water-Sediment partitioning coefficient'],
        "Value": [rice_obj.chemical_name,rice_obj.mai,rice_obj.a,rice_obj.dsed,rice_obj.pb,rice_obj.dw,rice_obj.osed,rice_obj.kd],
        "Expected-Value": [rice_obj.chemical_name_expected,rice_obj.mai,rice_obj.a,rice_obj.dsed,rice_obj.pb,rice_obj.dw,rice_obj.osed,rice_obj.kd],
        "Units": ['','kg',mark_safe('m<sup>2</sup>'),'m',mark_safe('kg/m<sup>3</sup>'),'m','','L/kg'],
    }
    return data

def gett2data(rice_obj):
    data = { 
        "Parameter": ['Sediment Mass', 'Water Column Volume', 'Mass per unit area', 'Water Concentration',],
        "Value": ['%.3f' % rice_obj.msed, '%.3f' % rice_obj.vw, '%.3f' % rice_obj.mai1, '%.3f' % rice_obj.cw,],
        "Units": ['mass', 'volume', 'mass/area', 'mass/volume',],
    }
    return data

def gett2dataqaqc(rice_obj):
    data = { 
        "Parameter": ['Sediment Mass', 'Water Column Volume', 'Mass per unit area', 'Water Concentration',],
        "Value": ['%.3f' % rice_obj.msed, '%.3f' % rice_obj.vw, '%.3f' % rice_obj.mai1, '%.3f' % rice_obj.cw,],
        "Expected-Value": ['%.3f' % rice_obj.msed_expected, '%.3f' % rice_obj.vw_expected, '%.3f' % rice_obj.mai1_expected, '%.3f' % rice_obj.cw_expected,],
        "Units": ['mass', 'volume', 'mass/area', 'mass/volume',],
    }
    return data



# def gettsumdata(bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael):
#     data = { 
#         "Parameter": ['BW Quail', 'BW Duck', 'BW Bird Other', 'BW Rat', 'BW Mammal Other', 'Avian LD50', 'Mammalian LD50', 
#                     'Solubility','AW Bird' , 'Mineau', 'AW Mammalian', 'NOAEC','NOAEL'],
#         "Mean": ['%.2e' % numpy.mean(bw_quail),'%.2e' % numpy.mean(bw_duck),'%.2e' % numpy.mean(bwb_other), '%.2e' % numpy.mean(bw_rat), 
#                  '%.2e' % numpy.mean(bwm_other), '%.2e' % numpy.mean(sol), '%.2e' % numpy.mean(avian_ld50), '%.2e' % numpy.mean(mammalian_ld50),
#                  '%.2e' % numpy.mean(aw_bird), '%.2e' % numpy.mean(mineau), '%.2e' % numpy.mean(aw_mamm),
#                  '%.2e' % numpy.mean(noaec), '%.2e' % numpy.mean(noael),],
#         "Std": ['%.2e' % numpy.std(bw_quail),'%.2e' % numpy.std(bw_duck),'%.2e' % numpy.std(bwb_other), '%.2e' % numpy.std(bw_rat), 
#                 '%.2e' % numpy.std(bwm_other), '%.2e' % numpy.std(sol), '%.2e' % numpy.std(avian_ld50), '%.2e' % numpy.std(mammalian_ld50),
#                  '%.2e' % numpy.std(aw_bird), '%.2e' % numpy.std(mineau), '%.2e' % numpy.std(aw_mamm),
#                  '%.2e' % numpy.std(noaec),'%.2e' % numpy.std(noael),],
#         "Min": ['%.2e' % numpy.min(bw_quail),'%.2e' % numpy.min(bw_duck),'%.2e' % numpy.min(bwb_other), '%.2e' % numpy.min(bw_rat), 
#                 '%.2e' % numpy.min(bwm_other), '%.2e' % numpy.min(sol), '%.2e' % numpy.min(avian_ld50), '%.2e' % numpy.min(mammalian_ld50),
#                  '%.2e' % numpy.min(aw_bird), '%.2e' % numpy.min(mineau), '%.2e' % numpy.min(aw_mamm),
#                  '%.2e' % numpy.min(noaec),'%.2e' % numpy.min(noael),],
#          "Max": ['%.2e' % numpy.max(bw_quail),'%.2e' % numpy.max(bw_duck),'%.2e' % numpy.max(bwb_other), '%.2e' % numpy.max(bw_rat), 
#                 '%.2e' % numpy.max(bwm_other), '%.2e' % numpy.max(sol), '%.2e' % numpy.max(avian_ld50), '%.2e' % numpy.max(mammalian_ld50),
#                  '%.2e' % numpy.max(aw_bird), '%.2e' % numpy.max(mineau), '%.2e' % numpy.max(aw_mamm),
#                  '%.2e' % numpy.max(noaec),'%.2e' % numpy.max(noael),],
#         "Unit": ['g', 'g', 'g', 'g', 'g','mg/kg-bw', 'mg/kg-bw', 'mg/L','g', '', 'g','mg/kg-diet', 'mg/kg-bw',],
#     }
#     return data

# # def gettsumdata_out(fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
# #                     at_mamm_out, fi_bird_out, det_out, 
# #                     act_out, acute_bird_out, acute_mamm_out, 
# #                     chron_bird_out, chron_mamm_out):
# def gettsumdata_out(dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#     data = {
#         "Parameter": ['Upper Bound Exposure - Avian', 'Upper Bound Exposure - Mammalian',
#                     'Adjusted Toxicity Value (Acute) - Avian',
#                     'Adjusted Toxicity Value (Acute) - Mammalian',
#                     'Adjusted Toxicity Value (Chronic) - Avian',
#                     'Adjusted Toxicity Value (Chronic) - Mammalian',
#                     'Ratio of Exposure to Toxicity (Acute) - Avian',
#                     'Ratio of Exposure to Toxicity (Acute) - Mammalian',
#                     'Ratio of Exposure to Toxicity (Chronic) - Avian',
#                     'Ratio of Exposure to Toxicity (Chronic) - Mammalian',],

#         "Mean": [
#                  '%.2e' % numpy.mean(dose_bird_out), '%.2e' % numpy.mean(dose_mamm_out), '%.2e' % numpy.mean(at_bird_out),
#                  '%.2e' % numpy.mean(at_mamm_out), '%.2e' % numpy.mean(act_out), '%.2e' % numpy.mean(det_out),
#                  '%.2e' % numpy.mean(acute_bird_out), '%.2e' % numpy.mean(acute_mamm_out),
#                  '%.2e' % numpy.mean(chron_bird_out), '%.2e' % numpy.mean(chron_mamm_out),],

#         "Std": ['%.2e' % numpy.std(dose_bird_out), '%.2e' % numpy.std(dose_mamm_out), '%.2e' % numpy.std(at_bird_out),
#                 '%.2e' % numpy.std(at_mamm_out), '%.2e' % numpy.std(act_out), '%.2e' % numpy.std(det_out),
#                 '%.2e' % numpy.std(acute_bird_out), '%.2e' % numpy.std(acute_mamm_out),
#                 '%.2e' % numpy.std(chron_bird_out), '%.2e' % numpy.std(chron_mamm_out),],

#         "Min": ['%.2e' % numpy.min(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
#                 '%.2e' % numpy.min(at_mamm_out), '%.2e' % numpy.min(act_out), '%.2e' % numpy.min(det_out),
#                 '%.2e' % numpy.min(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
#                 '%.2e' % numpy.min(chron_bird_out), '%.2e' % numpy.min(chron_mamm_out),],

#          "Max": ['%.2e' % numpy.max(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
#                 '%.2e' % numpy.max(at_mamm_out), '%.2e' % numpy.max(act_out), '%.2e' % numpy.min(det_out),
#                 '%.2e' % numpy.max(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
#                 '%.2e' % numpy.max(chron_bird_out), '%.2e' % numpy.max(chron_mamm_out),],

#         "Unit": ['mg/kg-bw', 'mg/kg-bw','mg/kg-bw', 'mg/kg-bw', 'mg/kg-bw', 'mg/kg-bw', '','', '', '',],
#     }
#     return data


pvuheadings = getheaderpvu()
pvuheadingsqaqc = getheaderpvuqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(rice_obj):
   
    html_all = table_1(rice_obj)      
    html_all = html_all + table_2(rice_obj)

    return html_all

def table_all_qaqc(rice_obj):
   
    html_all = table_1_qaqc(rice_obj)      
    html_all = html_all + table_2_qaqc(rice_obj)

    return html_all


def table_1(rice_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Model Inputs</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(rice_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_1_qaqc(rice_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Model Inputs</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1dataqaqc(rice_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(rice_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Rice Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Model Output</H4>
                <div class="out_ container_output">
        """
        #table 1
        t2data = gett2data(rice_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2_qaqc(rice_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Rice Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Model Output</H4>
                <div class="out_ container_output">
        """
        #table 1
        t2data = gett2dataqaqc(rice_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html

# def table_all_sum(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael,
#                     dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#     html_all_sum = table_sum_input(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael)
#     html_all_sum += table_sum_output(sumheadings,tmpl,dose_bird_out,dose_mamm_out,at_bird_out, 
#                     at_mamm_out,det_out,act_out,acute_bird_out,acute_mamm_out,chron_bird_out,chron_mamm_out)
#     return html_all_sum

# def table_sum_input(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael):
#         #pre-table sum_input
#         html = """
#         <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
#         <div class="out_">
#             <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
#                 <div class="out_ container_output">
#         """
#         #table sum_input
#         tsuminputdata = gettsumdata(bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael)
#         tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
#         html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
#         html = html + """
#         </div>
#         """
#         return html

# def table_sum_output(sumheadings, tmpl, dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#         #pre-table sum_input
#         html = """
#         <br>
#             <H4 class="out_1 collapsible" id="section3"><span></span>rice Outputs</H4>
#                 <div class="out_ container_output">
#         """
#         #table sum_input
#         tsumoutputdata = gettsumdata_out(dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out)
#         tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
#         html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
#         html = html + """
#                 </div>
#         </div>
#         <br>
#         """
#         return html