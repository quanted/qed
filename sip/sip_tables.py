import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from sip import sip_model
from sip import sip_parameters
import logging

logger = logging.getLogger("SipTables")

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvr():
	headings = ["Parameter", "Acute", "Chronic","Units"]
	return headings

def getheaderpvrqaqc():
    headings = ["Parameter", "Acute", "Acute-Expected", "Chronic", "Chronic-Expected","Units"]
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

def gett1data(sip_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Body Weight of Bird', 'Body Weight of Mammal','Solubility', 'LD<sub>50 avian', 'LD<sub>50 mammal','Body Weight of Assessed Bird','Body Weight of Assessed Mammal','Mineau Scaling Factor','NOAEC','NOAEL',],
        "Value": [sip_obj.chemical_name,  sip_obj.bw_bird, sip_obj.bw_mamm, sip_obj.sol, sip_obj.ld50_a, sip_obj.ld50_m, sip_obj.aw_bird,  sip_obj.aw_mamm, sip_obj.mineau, sip_obj.noaec, sip_obj.noael,],
        "Units": ['', 'g', 'g','mg/L', 'mg/kg','mg/kg','g','g','', 'mg/kg-diet','mg/kg-bw'],
    }
    return data

def gett1dataqaqc(sip_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Body Weight of Bird', 'Body Weight of Mammal','Solubility', 'LD<sub>50 avian', 'LD<sub>50 mammal','Body Weight of Assessed Bird','Body Weight of Assessed Mammal','Mineau Scaling Factor','NOAEC','NOAEL',],
        "Value": [sip_obj.chemical_name_expected,  sip_obj.bw_bird, sip_obj.bw_mamm, sip_obj.sol, sip_obj.ld50_a, sip_obj.ld50_m, sip_obj.aw_bird,  sip_obj.aw_mamm, sip_obj.mineau, sip_obj.noaec, sip_obj.noael,],
        "Units": ['', 'g', 'g','mg/L', 'mg/kg','mg/kg','g','g','', 'mg/kg-diet','mg/kg-bw'],
    }
    return data

def gett2data(sip_obj):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.acute_mamm_out, '%.2e' % sip_obj.at_mamm_out, '%.2e' % sip_obj.acute_mamm_out, '%s' % sip_obj.acuconm_out,],
        "Chronic": ['%.2e' % sip_obj.dose_mamm_out, '%.2e' % sip_obj.act_out, '%.2e' % sip_obj.chron_mamm_out, '%s' % sip_obj.chronconm_out,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gett2dataqaqc(sip_obj):
    logger.info(vars(sip_obj))
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.acute_mamm_out,'%.2e' % sip_obj.at_mamm_out,'%.2e' % sip_obj.acute_mamm_out,'%s' % sip_obj.acuconm_out,],
        "Acute-Expected": ['%.2e' % sip_obj.acute_mamm_out_expected,'%.2e' % sip_obj.at_mamm_out_expected,'%.2e' % sip_obj.acute_mamm_out_expected,'%s' % sip_obj.acuconm_out_expected,],
        "Chronic": ['%.2e' % sip_obj.dose_mamm_out,'%.2e' % sip_obj.act_out,'%.2e' % sip_obj.chron_mamm_out,'%s' % sip_obj.chronconm_out,],
        "Chronic-Expected": ['%.2e' % sip_obj.dose_mamm_out_expected,'%.2e' % sip_obj.act_out_expected,'%.2e' % sip_obj.chron_mamm_out_expected,'%s' % sip_obj.chronconm_out_expected,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gett3data(sip_obj):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.acute_bird_out, '%.2e' % sip_obj.at_bird_out,'%.2e' % sip_obj.acute_bird_out, '%s' % sip_obj.acuconb_out,],
        "Chronic": ['%.2e' % sip_obj.dose_bird_out, '%.2e' % sip_obj.det_out,'%.2e' % sip_obj.chron_bird_out, '%s' % sip_obj.chronconb_out,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gett3dataqaqc(sip_obj):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.acute_bird_out, '%.2e' % sip_obj.at_bird_out, '%.2e' % sip_obj.acute_bird_out, '%s' % sip_obj.acuconb_out,],
        "Acute-Expected": ['%.2e' % sip_obj.acute_bird_out_expected, '%.2e' % sip_obj.at_bird_out_expected, '%.2e' % sip_obj.acute_bird_out_expected, '%s' % sip_obj.acuconb_out_expected,],
        "Chronic": ['%.2e' % sip_obj.dose_bird_out, '%.2e' % sip_obj.act_out, '%.2e' % sip_obj.chron_bird_out, '%s' % sip_obj.chronconb_out,],
        "Chronic-Expected": ['%.2e' % sip_obj.dose_bird_out_expected,'%.2e' % sip_obj.act_out_expected,'%.2e' % sip_obj.chron_bird_out_expected,'%s' % sip_obj.chronconb_out_expected,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gettsumdata(bw_bird, bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, mineau,
                    aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael):
    data = { 
        "Parameter": ['BW Bird', 'BW Mammalian', 'Avian LD50', 'Mammalian LD50', 
                    'Solubility','AW Bird', 'TW Bird', 'Mineau', 'AW Mammalian', 'TW Mammalian',
                    'NOAEL for Avian','Noaec for Avian', 'NOAEL for Mammal','Noaec for Mammal'],
        "Mean": ['%.2e' % numpy.mean(bw_bird),'%.2e' % numpy.mean(bw_mamm),'%.2e' % numpy.mean(avian_ld50), '%.2e' % numpy.mean(mammalian_ld50), 
                 '%.2e' % numpy.mean(sol), '%.2e' % numpy.mean(aw_bird), '%.2e' % numpy.mean(tw_bird), '%.2e' % numpy.mean(mineau),
                 '%.2e' % numpy.mean(aw_mamm), '%.2e' % numpy.mean(tw_mamm), '%.2e' % numpy.mean(avian_noaec),
                 '%.2e' % numpy.mean(avian_noael), '%.2e' % numpy.mean(mammalian_noaec), '%.2e' % numpy.mean(mammalian_noael),],
        "Std": ['%.2e' % numpy.std(bw_bird),'%.2e' % numpy.std(bw_mamm),'%.2e' % numpy.std(avian_ld50), '%.2e' % numpy.std(mammalian_ld50), 
                '%.2e' % numpy.std(sol), '%.2e' % numpy.std(aw_bird), '%.2e' % numpy.std(tw_bird), '%.2e' % numpy.std(mineau),
                 '%.2e' % numpy.std(aw_mamm), '%.2e' % numpy.std(tw_mamm), '%.2e' % numpy.std(avian_noaec),
                 '%.2e' % numpy.std(avian_noael), '%.2e' % numpy.std(mammalian_noaec), '%.2e' % numpy.std(mammalian_noael),],
        "Min": ['%.2e' % numpy.min(bw_bird),'%.2e' % numpy.min(bw_mamm),'%.2e' % numpy.min(avian_ld50), '%.2e' % numpy.min(mammalian_ld50), 
                '%.2e' % numpy.min(sol), '%.2e' % numpy.min(aw_bird), '%.2e' % numpy.min(tw_bird), '%.2e' % numpy.min(mineau),
                 '%.2e' % numpy.min(aw_mamm), '%.2e' % numpy.min(tw_mamm), '%.2e' % numpy.min(avian_noaec),
                 '%.2e' % numpy.min(avian_noael), '%.2e' % numpy.min(mammalian_noaec), '%.2e' % numpy.min(mammalian_noael),],
         "Max": ['%.2e' % numpy.max(bw_bird),'%.2e' % numpy.max(bw_mamm),'%.2e' % numpy.max(avian_ld50), '%.2e' % numpy.max(mammalian_ld50), 
                '%.2e' % numpy.max(sol), '%.2e' % numpy.max(aw_bird), '%.2e' % numpy.max(tw_bird), '%.2e' % numpy.max(mineau),
                 '%.2e' % numpy.max(aw_mamm), '%.2e' % numpy.max(tw_mamm), '%.2e' % numpy.max(avian_noaec),
                 '%.2e' % numpy.max(avian_noael), '%.2e' % numpy.max(mammalian_noaec), '%.2e' % numpy.max(mammalian_noael),],
        "Unit": ['', '', '', '', '','', '', '','', '', '','', '', '',],
    }
    return data

def gettsumdata_out(fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out):
    data = { 
        "Parameter": ['Runoff to Dry Areas', 'Runoff to Semi-Aquatic Areas', 'Spray Drift',
                    'Total to Dry Areas', 'Total to Semi-Aquatic Areas',
                    'Risk Quotient for non-listed monocot seedlings exposed to pesticide X in a dry area',
                    'Risk Quotient for non-listed monocot seedlings exposed to Pesticide X in a semi-aquatic area',
                    'Risk Quotient for non-listed monocot seedlings exposed to Pesticide X via spray drift',
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X in a dry areas',
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X in a semi-aquatic area',
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X via spray drift',
                    'Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas',
                    'Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in semi-aquatic areas',],

        "Mean": [
                 '%.2e' % numpy.mean(fw_bird_out), '%.2e' % numpy.mean(fw_mamm_out), '%.2e' % numpy.mean(dose_bird_out), '%.2e' % numpy.mean(dose_mamm_out), '%.2e' % numpy.mean(at_bird_out),
                 '%.2e' % numpy.mean(at_mamm_out), '%.2e' % numpy.mean(fi_bird_out), '%.2e' % numpy.mean(det_out),
                 '%.2e' % numpy.mean(act_out), '%.2e' % numpy.mean(acute_bird_out), '%.2e' % numpy.mean(acute_mamm_out),
                 '%.2e' % numpy.mean(chron_bird_out), '%.2e' % numpy.mean(chron_mamm_out),],

        "Std": ['%.2e' % numpy.std(fw_bird_out), '%.2e' % numpy.std(fw_mamm_out), '%.2e' % numpy.std(dose_bird_out), '%.2e' % numpy.std(dose_mamm_out), '%.2e' % numpy.std(at_bird_out),
                '%.2e' % numpy.std(at_mamm_out), '%.2e' % numpy.std(fi_bird_out), '%.2e' % numpy.std(det_out),
                '%.2e' % numpy.std(act_out), '%.2e' % numpy.std(acute_bird_out), '%.2e' % numpy.std(acute_mamm_out),
                '%.2e' % numpy.std(chron_bird_out), '%.2e' % numpy.std(chron_mamm_out),],

        "Min": ['%.2e' % numpy.min(fw_bird_out), '%.2e' % numpy.min(fw_mamm_out), '%.2e' % numpy.min(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
                '%.2e' % numpy.min(at_mamm_out), '%.2e' % numpy.min(fi_bird_out), '%.2e' % numpy.min(det_out),
                '%.2e' % numpy.min(act_out), '%.2e' % numpy.min(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
                '%.2e' % numpy.min(chron_bird_out), '%.2e' % numpy.min(chron_mamm_out),],

         "Max": ['%.2e' % numpy.max(fw_bird_out), '%.2e' % numpy.max(fw_mamm_out), '%.2e' % numpy.max(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
                '%.2e' % numpy.max(at_mamm_out), '%.2e' % numpy.max(fi_bird_out), '%.2e' % numpy.min(det_out),
                '%.2e' % numpy.max(act_out), '%.2e' % numpy.max(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
                '%.2e' % numpy.max(chron_bird_out), '%.2e' % numpy.max(chron_mamm_out),],

        "Unit": ['', '','', '', '', '', '','', '', '', '', '','',],
    }
    return data


pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
pvrheadingsqaqc = getheaderpvrqaqc()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(sip_obj):
   
    html_all = table_1(sip_obj)      
    html_all = html_all + table_2(sip_obj)
    html_all = html_all + table_3(sip_obj)

    return html_all

def table_all_qaqc(sip_obj):
   
    html_all = table_1_qaqc(sip_obj)      
    html_all = html_all + table_2_qaqc(sip_obj)
    html_all = html_all + table_3_qaqc(sip_obj)

    return html_all


def table_1(sip_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(sip_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_1_qaqc(sip_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1dataqaqc(sip_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_2(sip_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>SIP Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Mammalian Results (%s kg)</H4>
                <div class="out_ container_output">
        """%(sip_obj.aw_mamm)
        #table 1
        # dose_mamm_out1 = sip_obj.dose_mamm(self)
        # dose_mamm_out2 = sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm)
        # at_mamm_out1 = sip_obj.at_mamm(ld50,aw_mamm,tw_mamm)
        # act_out1 = sip_obj.act(noael,tw_mamm,aw_mamm)
        # acute_mamm_out1 = sip_obj.acute_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.at_mamm(ld50,aw_mamm,tw_mamm))
        # chron_mamm_out1 = sip_obj.chron_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.act(noael,tw_mamm,aw_mamm))
        # acuconm_out1 = sip_obj.acuconm(sip_obj.acute_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.at_mamm(ld50,aw_mamm,tw_mamm)))
        # chronconm_out1 = sip_obj.chronconm(sip_obj.chron_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.act(noael,tw_mamm,aw_mamm)))
        # t2data = gett2data(dose_mamm_out1, dose_mamm_out2, at_mamm_out1,act_out1, acute_mamm_out1, chron_mamm_out1, acuconm_out1, chronconm_out1)
        t2data = gett2data(sip_obj)



        t2rows = gethtmlrowsfromcols(t2data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvrheadings)))
        html = html + """
                </div>
        """
        return html  

def table_2_qaqc(sip_obj):
        #pre-table 1
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>SIP Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>Mammalian Results (%s kg)</H4>
                <div class="out_ container_output">
        """%(sip_obj.aw_mamm)
        #table 1
        # dose_mamm_out1 = sip_obj.dose_mamm(self)
        # dose_mamm_out2 = sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm)
        # at_mamm_out1 = sip_obj.at_mamm(ld50,aw_mamm,tw_mamm)
        # act_out1 = sip_obj.act(noael,tw_mamm,aw_mamm)
        # acute_mamm_out1 = sip_obj.acute_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.at_mamm(ld50,aw_mamm,tw_mamm))
        # chron_mamm_out1 = sip_obj.chron_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.act(noael,tw_mamm,aw_mamm))
        # acuconm_out1 = sip_obj.acuconm(sip_obj.acute_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.at_mamm(ld50,aw_mamm,tw_mamm)))
        # chronconm_out1 = sip_obj.chronconm(sip_obj.chron_mamm(sip_obj.dose_mamm(sip_obj.fw_mamm(bw_mamm),sol,bw_mamm),sip_obj.act(noael,tw_mamm,aw_mamm)))
        # t2data = gett2data(dose_mamm_out1, dose_mamm_out2, at_mamm_out1,act_out1, acute_mamm_out1, chron_mamm_out1, acuconm_out1, chronconm_out1)
        t2data = gett2dataqaqc(sip_obj)



        t2rows = gethtmlrowsfromcols(t2data,pvrheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvrheadingsqaqc)))
        html = html + """
                </div>
        """
        return html  

def table_3(sip_obj):
        #pre-table 1
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Avian Results (%s kg)</H4>
                <div class="out_ container_output">
        """%(sip_obj.aw_bird)
        #table 1      
        # dose_bird_out1 = sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird), 
        # dose_bird_out2 = sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird), 
        # at_bird_out1 = sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau),
        # det_out1 = sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird),
        # acute_bird_out1 = sip_obj.acute_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau)),
        # chron_bird_out1 = sip_obj.chron_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird)),
        # acuonb_bird_out1 = sip_obj.acuconb(sip_obj.acute_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau))),             
        # chronconb_bird_out1 = sip_obj.chronconb(sip_obj.chron_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird)))
        t3data = gett3data(sip_obj)
        t3rows = gethtmlrowsfromcols(t3data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvrheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_3_qaqc(sip_obj):
        #pre-table 1
        html = """
            <H4 class="out_1 collapsible" id="section4"><span></span>Avian Results (%s kg)</H4>
                <div class="out_ container_output">
        """%(sip_obj.aw_bird)
        #table 1      
        # dose_bird_out1 = sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird), 
        # dose_bird_out2 = sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird), 
        # at_bird_out1 = sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau),
        # det_out1 = sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird),
        # acute_bird_out1 = sip_obj.acute_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau)),
        # chron_bird_out1 = sip_obj.chron_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird)),
        # acuonb_bird_out1 = sip_obj.acuconb(sip_obj.acute_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.at_bird(ld50,aw_bird,tw_bird,mineau))),             
        # chronconb_bird_out1 = sip_obj.chronconb(sip_obj.chron_bird(sip_obj.dose_bird(sip_obj.fw_bird(bw_bird),sol,bw_bird),sip_obj.det(noaec,sip_obj.fi_bird(bw_bird),bw_bird)))
        t3data = gett3dataqaqc(sip_obj)
        t3rows = gethtmlrowsfromcols(t3data,pvrheadingsqaqc)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvrheadingsqaqc)))
        html = html + """
                </div>
        </div>
        """
        return html


def table_all_sum(sumheadings, tmpl, bw_bird, bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, mineau,
                    aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael,
                    fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out):
    html_all_sum = table_sum_input(sumheadings, tmpl, bw_bird, bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, 
                    mineau, aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael)
    html_all_sum += table_sum_output(sumheadings, tmpl, fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out)
    return html_all_sum

def table_sum_input(sumheadings, tmpl, bw_bird, bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, mineau,
                    aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><td><H3>Summary Statistics</H3></td></tr>
        <tr></tr>
        </table>
        """
        #table sum_input
        tsuminputdata = gettsumdata(bw_bird, bw_mamm, avian_ld50, mammalian_ld50, sol, aw_bird, tw_bird, mineau,
                    aw_mamm, tw_mamm, avian_noaec, avian_noael, mammalian_noaec, mammalian_noael)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html

def table_sum_output(sumheadings, tmpl, fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out):

        #pre-table sum_input
        html = """
        <br>
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(fw_bird_out, fw_mamm_out, dose_bird_out, dose_mamm_out, at_bird_out, 
                    at_mamm_out, fi_bird_out, det_out, 
                    act_out, acute_bird_out, acute_mamm_out, 
                    chron_bird_out, chron_mamm_out)
        tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        return html