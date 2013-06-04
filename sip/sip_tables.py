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

def gett1data(sip_obj):
    data = { 
        "Parameter": ['Chemical Name', 'Body Weight of Bird', 'Body Weight of Mammal','Solubility', 'LD<sub>50 avian', 'LD<sub>50 mammal','Body Weight of Assessed Bird','Body Weight of Assessed Mammal','Mineau Scaling Factor','NOAEC','NOAEL',],
        "Value": [sip_obj.chemical_name,  sip_obj.bw_bird, sip_obj.bw_mamm, sip_obj.sol, sip_obj.ld50_a, sip_obj.ld50_m, sip_obj.aw_bird,  sip_obj.aw_mamm, sip_obj.mineau, sip_obj.noaec, sip_obj.noael,],
        "Units": ['', 'kg', 'kg','mg/L', 'mg/kg','mg/kg','kg','kg','', 'mg/kg','mg/kg'],
    }
    return data


def gett2data(sip_obj):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.acute_mamm, '%.2e' % sip_obj.at_mamm, '%.2e' % sip_obj.acute_mamm, '%s' % sip_obj.acuconm,],
        "Chronic": ['%.2e' % sip_obj.dose_mamm, '%.2e' % sip_obj.act, '%.2e' % sip_obj.chron_mamm, '%s' % sip_obj.chronconm,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data

def gett3data(sip_obj):
    data = { 
        "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
        "Acute": ['%.2e' % sip_obj.dose_bird, '%.2e' % sip_obj.at_bird,'%.2e' % sip_obj.acute_bird, '%s' % sip_obj.acuconb,],
        "Chronic": ['%.2e' % sip_obj.dose_bird, '%.2e' % sip_obj.det,'%.2e' % sip_obj.chron_bird, '%s' % sip_obj.chronconb,],
        "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
    }
    return data






pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(sip_obj):
   
    html_all = table_1(sip_obj)      
    html_all = html_all + table_2(sip_obj)
    html_all = html_all + table_3(sip_obj)


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