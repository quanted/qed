import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from sip import sip_model
from sip import sip_parameters

def getheaderpvu():
	headings = ["Parameter", "Value", "Units"]
	return headings

def getheaderpvr():
	headings = ["Parameter", "Acute", "Chronic","Units"]
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

def gett1data(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael):
    data = { 
        "Parameter": ['Chemical Name', 'Receptor Selected', 'Body Weight of Bird', 'Body Weight of Mammal','Solubility', 'LD<sub>50', 'Body Weight of Assessed Bird','Body Weight of Tested Bird','Body Weight of Assessed Mammal','Body Weight of Tested Mammal','Mineau Scaling Factor','NOAEC','NOAEL',],
        "Value": [chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael,],
        "Units": ['', '', 'kg', 'kg','mg/L', 'mg/kg','kg','kg','kg','kg','','mg/kg','mg/kg'],
    }
    return data


def gett2data(dose_mamm_out1, at_mamm_out1, acute_mamm_out1, acuconm_out1, dose_mamm_out2, act_out1,chron_mamm_out1, chronconm_out1):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % dose_mamm_out1, '%.2e' % at_mamm_out1, '%.2e' % acute_mamm_out1, '%s' % acuconm_out1,],
        "Chronic": ['%.2e' % dose_mamm_out2, '%.2e' % act_out1, '%.2e' % chron_mamm_out1, '%s' % chronconm_out1,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gett3data(dose_bird_out1, dose_bird_out2, at_bird_out1, det_out1, acute_bird_out1, chron_bird_out1, acuonb_bird_out1, chronconb_bird_out1):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % dose_bird_out1, '%.2e' % at_bird_out1,'%.2e' % acute_bird_out1, '%s' % acuonb_bird_out1,],
        "Chronic": ['%.2e' % dose_bird_out2, '%.2e' % det_out1,'%.2e' % chron_bird_out1, '%s' % chronconb_bird_out1,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data






pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael):
   
    html_all = table_1(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)      
    html_all = html_all + table_2(aw_mamm, bw_mamm, sol, ld50, tw_mamm, noael)
    html_all = html_all + table_3(aw_bird, bw_bird, sol, ld50, tw_bird, mineau, noaec)


    return html_all


def table_1(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael):
        #pre-table 1
        html = """
            <div class="out_1">
              <H3>User Inputs: Chemical Identity</H3>
              <H4>Application and Chemical Information</H4>
            </div>
        """
        #table 1
        t1data = gett1data(chemical_name, select_receptor, bw_bird, bw_mamm, sol, ld50, aw_bird, tw_bird, aw_mamm, tw_mamm, mineau, noaec, noael)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        return html

def table_2(aw_mamm, bw_mamm, sol, ld50, tw_mamm, noael):
        #pre-table 1
        html = """
            <div class="out_1">
              <H3>User Inputs: Chemical Identity</H3>
              <H4>Mammalian Results (%s kg)</H4>
            </div>
        """%(aw_mamm)
        #table 1        
        dose_mamm_out1 = sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm)
        dose_mamm_out2 = sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm)
        at_mamm_out1 = sip_model.at_mamm(ld50,aw_mamm,tw_mamm)
        act_out1 = sip_model.act(noael,tw_mamm,aw_mamm)
        acute_mamm_out1 = sip_model.acute_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.at_mamm(ld50,aw_mamm,tw_mamm))
        chron_mamm_out1 = sip_model.chron_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.act(noael,tw_mamm,aw_mamm))
        acuconm_out1 = sip_model.acuconm(sip_model.acute_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.at_mamm(ld50,aw_mamm,tw_mamm)))
        chronconm_out1 = sip_model.chronconm(sip_model.chron_mamm(sip_model.dose_mamm(sip_model.fw_mamm(bw_mamm),sol,bw_mamm),sip_model.act(noael,tw_mamm,aw_mamm)))
        # t2data = gett2data(dose_mamm_out1, dose_mamm_out2, at_mamm_out1,act_out1, acute_mamm_out1, chron_mamm_out1, acuconm_out1, chronconm_out1)
        t2data = gett2data(dose_mamm_out1, at_mamm_out1, acute_mamm_out1, acuconm_out1, dose_mamm_out2, act_out1,chron_mamm_out1, chronconm_out1)



        t2rows = gethtmlrowsfromcols(t2data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvrheadings)))
        return html               
def table_3(aw_bird, bw_bird, sol, ld50, tw_bird, mineau, noaec):
        #pre-table 1
        html = """
            <div class="out_1">
              <H3>User Inputs: Chemical Identity</H3>
              <H4>Mammalian Results (%s kg)</H4>
            </div>
        """%(aw_bird)
        #table 1      
        dose_bird_out1 = sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird), 
        dose_bird_out2 = sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird), 
        at_bird_out1 = sip_model.at_bird(ld50,aw_bird,tw_bird,mineau),
        det_out1 = sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird),
        acute_bird_out1 = sip_model.acute_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.at_bird(ld50,aw_bird,tw_bird,mineau)),
        chron_bird_out1 = sip_model.chron_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird)),
        acuonb_bird_out1 = sip_model.acuconb(sip_model.acute_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.at_bird(ld50,aw_bird,tw_bird,mineau))),             
        chronconb_bird_out1 = sip_model.chronconb(sip_model.chron_bird(sip_model.dose_bird(sip_model.fw_bird(bw_bird),sol,bw_bird),sip_model.det(noaec,sip_model.fi_bird(bw_bird),bw_bird)))             
        t3data = gett3data(dose_bird_out1,dose_bird_out2, at_bird_out1, det_out1, acute_bird_out1, chron_bird_out1, acuonb_bird_out1, chronconb_bird_out1)
        t3rows = gethtmlrowsfromcols(t3data,pvrheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvrheadings)))
        return html