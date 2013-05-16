import numpy
#import django
from django.template import Context, Template
from django.utils.safestring import mark_safe
from dust import dust_model
from dust import dust_parameters

def getheaderpv():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvu():
    headings = ["Parameter", "Value", "Units"]
    return headings

def getheaderde():
    headings = ["Description", "EEC"]
    return headings

def getheaderplantec25noaec():
    headings = ["Plant Type", "EC25", "NOAEC", "EC25", "NOAEC"]
    return headings

def getheaderplantecdrysemispray():
    headings = ["Plant Type", "Listed Status", "Dry", "Semi-Aquatic", "Spray Drift"]
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

def gett1data(terrplant_obj):
    data = { 
        "Parameter": ['Chemical Name', 'PC Code', 'Use', 'Application Method','Application Form',],
        "Value": [terrplant_obj.chemical_name, terrplant_obj.pc_code, terrplant_obj.use, terrplant_obj.application_method,terrplant_obj.application_form,],
    }
    return data

def gett2data(terrplant_obj):
    data = { 
        "Parameter": ['Incorporation', 'Application Rate', 'Drift Fraction', 'Runoff Fraction',],
        "Value": [terrplant_obj.I, terrplant_obj.A, terrplant_obj.D, terrplant_obj.R,],
        "Units": ['', 'lbs ai/A', '','', ],
    }
    return data

def gett3data(terrplant_obj):
    data = { 
        "Description": ['Runoff to Dry Areas', 'Runoff to Semi-Aquatic Areas', 'Spray Drift','Total to Dry Areas', 'Total to Semi-Aquatic Areas',],
        "EEC": ['%.2e' % terrplant_obj.rundry_results,'%.2e' % terrplant_obj.runsemi_results,'%.2e' % terrplant_obj.spray_results,
                '%.2e' % terrplant_obj.totaldry_results,'%.2e' % terrplant_obj.totalsemi_results, ],
    }
    return data

def gett4data(terrplant_obj):
    data = { 
        "Plant Type": ['Monocot', 'Dicot',],
        "EC25": [terrplant_obj.nms,terrplant_obj.nds,],
        "NOAEC": [terrplant_obj.lms,terrplant_obj.lds,],
        "EC25": [terrplant_obj.nmv,terrplant_obj.ndv,],
        "NOAEC":[terrplant_obj.lmv,terrplant_obj.ldv,],
    }
    return data

def gett5data(terrplant_obj):
    data = { 
        "Plant Type": ['Monocot', 'Monocot', 'Dicot', 'Dicot',],
        "Listed Status": ['non-listed','listed','non-listed','listed',],
        "Dry": ['%.2e' % terrplant_obj.nmsRQdry_results,'%.2e' % terrplant_obj.lmsRQdry_results,'%.2e' % terrplant_obj.ndsRQdry_results,'%.2e' % terrplant_obj.ldsRQdry_results,],
        "Semi-Aquatic": ['%.2e' % terrplant_obj.nmsRQsemi_results,'%.2e' % terrplant_obj.lmsRQsemi_results,'%.2e' % terrplant_obj.ndsRQsemi_results,'%.2e' % terrplant_obj.ldsRQsemi_results,],
        "Spray Drift":['%.2e' % terrplant_obj.nmsRQspray_results,'%.2e' % terrplant_obj.lmsRQspray_results,'%.2e' % terrplant_obj.ndsRQspray_results,'%.2e' % terrplant_obj.ldsRQspray_results,],
    }
    return data

def gettsumdata(A, I, R, D, nms, lms, nds, lds):
    data = { 
        "Parameter": ['Incorporation', 'Application Rate', 'Drift Fraction', 'Runoff Fraction','Runoff to Dry Areas',],
        "Mean": ['%.2e' % numpy.mean(A),'%.2e' % numpy.mean(I),'%.2e' % numpy.mean(R), '%.2e' % numpy.mean(D), 
                 '%.2e' % numpy.mean(nms), '%.2e' % numpy.mean(lms), '%.2e' % numpy.mean(nds), '%.2e' % numpy.mean(lds),],
        "Std": ['%.2e' % numpy.std(A),'%.2e' % numpy.std(I),'%.2e' % numpy.std(R), '%.2e' % numpy.std(D), 
                '%.2e' % numpy.std(nms), '%.2e' % numpy.std(lms), '%.2e' % numpy.std(nds), '%.2e' % numpy.std(lds),],
        "Min": ['%.2e' % numpy.min(A),'%.2e' % numpy.min(I),'%.2e' % numpy.min(R), '%.2e' % numpy.min(D), 
                '%.2e' % numpy.min(nms), '%.2e' % numpy.min(lms), '%.2e' % numpy.min(nds), '%.2e' % numpy.min(lds),],
         "Max": ['%.2e' % numpy.max(A),'%.2e' % numpy.max(I),'%.2e' % numpy.max(R), '%.2e' % numpy.max(D), 
                '%.2e' % numpy.max(nms), '%.2e' % numpy.max(lms), '%.2e' % numpy.max(nds), '%.2e' % numpy.max(lds),],
        "Unit": ['', '', '', '', '','', '', '',],
    }
    return data

def gettsumdata_out(rundry_out, runsemi_out, spray_out, totaldry_out, totalsemi_out, 
                    nmsRQdry_out, nmsRQsemi_out, nmsRQspray_out, 
                    lmsRQdry_out, lmsRQsemi_out, lmsRQspray_out, 
                    ndsRQdry_out, ndsRQsemi_out, ndsRQspray_out, 
                    ldsRQdry_out, ldsRQsemi_out, ldsRQspray_out):
    data = { 
        "Parameter": ['Runoff to Semi-Aquatic Areas', 'Spray Drift','Total to Dry Areas', 'Total to Semi-Aquatic Areas',
                    'EEC for runoff to dry areas','EEC for runoff to semi-aquatic areas','EEC for spray drift',
                    'EEC total for dry areas','EEC total for semi-aquatic areas',
                    'Risk Quotient for non-listed monocot seedlings exposed to pesticide X in a dry area'
                    'Risk Quotient for non-listed monocot seedlings exposed to Pesticide X in a semi-aquatic area'
                    'Risk Quotient for non-listed monocot seedlings exposed to Pesticide X via spray drift'
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X in a dry areas'
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X in a semi-aquatic area'
                    'Risk Quotient for listed monocot seedlings exposed to Pesticide X via spray drift'
                    'Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas'
                    'Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in semi-aquatic areas'
                    'Risk Quotient for non-listed dicot seedlings exposed to Pesticide X in dry areas'
                    'Risk Quotient for listed dicot seedlings exposed to Pesticide X in dry areas'
                    'Risk Quotient for listed dicot seedlings exposed to Pesticide X in semi-aquatic areas'
                    'Risk Quotient for listed dicot seedlings exposed to Pesticide X via spray drift',],

        "Mean": [
                 '%.2e' % numpy.mean(rundry_out), '%.2e' % numpy.mean(runsemi_out), '%.2e' % numpy.mean(spray_out), '%.2e' % numpy.mean(totaldry_out), '%.2e' % numpy.mean(totaldry_out),
                 '%.2e' % numpy.mean(nmsRQdry_out), '%.2e' % numpy.mean(nmsRQsemi_out), '%.2e' % numpy.mean(nmsRQspray_out),
                 '%.2e' % numpy.mean(lmsRQdry_out), '%.2e' % numpy.mean(lmsRQsemi_out), '%.2e' % numpy.mean(lmsRQspray_out),
                 '%.2e' % numpy.mean(ndsRQdry_out), '%.2e' % numpy.mean(ndsRQsemi_out), '%.2e' % numpy.mean(ndsRQspray_out),
                 '%.2e' % numpy.mean(ldsRQdry_out), '%.2e' % numpy.mean(ldsRQsemi_out), '%.2e' % numpy.mean(ldsRQspray_out),],

        "Std": ['%.2e' % numpy.std(rundry_out), '%.2e' % numpy.std(runsemi_out), '%.2e' % numpy.std(spray_out), '%.2e' % numpy.std(totaldry_out), '%.2e' % numpy.std(totaldry_out),
                '%.2e' % numpy.std(nmsRQdry_out), '%.2e' % numpy.std(nmsRQsemi_out), '%.2e' % numpy.std(nmsRQspray_out),
                '%.2e' % numpy.std(lmsRQdry_out), '%.2e' % numpy.std(lmsRQsemi_out), '%.2e' % numpy.std(lmsRQspray_out),
                '%.2e' % numpy.std(ndsRQdry_out), '%.2e' % numpy.std(ndsRQsemi_out), '%.2e' % numpy.std(ndsRQspray_out),
                '%.2e' % numpy.std(ldsRQdry_out), '%.2e' % numpy.std(ldsRQsemi_out), '%.2e' % numpy.std(ldsRQspray_out),],

        "Min": ['%.2e' % numpy.min(rundry_out), '%.2e' % numpy.min(runsemi_out), '%.2e' % numpy.min(spray_out), '%.2e' % numpy.min(totaldry_out), '%.2e' % numpy.min(totaldry_out),
                '%.2e' % numpy.min(nmsRQdry_out), '%.2e' % numpy.min(nmsRQsemi_out), '%.2e' % numpy.min(nmsRQspray_out),
                '%.2e' % numpy.min(lmsRQdry_out), '%.2e' % numpy.min(lmsRQsemi_out), '%.2e' % numpy.min(lmsRQspray_out),
                '%.2e' % numpy.min(ndsRQdry_out), '%.2e' % numpy.min(ndsRQsemi_out), '%.2e' % numpy.min(ndsRQspray_out),
                '%.2e' % numpy.min(ldsRQdry_out), '%.2e' % numpy.min(ldsRQsemi_out), '%.2e' % numpy.min(ldsRQspray_out),],

         "Max": ['%.2e' % numpy.max(rundry_out), '%.2e' % numpy.max(runsemi_out), '%.2e' % numpy.max(spray_out), '%.2e' % numpy.min(totaldry_out), '%.2e' % numpy.min(totaldry_out),
                '%.2e' % numpy.max(nmsRQdry_out), '%.2e' % numpy.max(nmsRQsemi_out), '%.2e' % numpy.min(nmsRQspray_out),
                '%.2e' % numpy.max(lmsRQdry_out), '%.2e' % numpy.max(lmsRQsemi_out), '%.2e' % numpy.min(lmsRQspray_out),
                '%.2e' % numpy.max(ndsRQdry_out), '%.2e' % numpy.max(ndsRQsemi_out), '%.2e' % numpy.min(ndsRQspray_out),
                '%.2e' % numpy.max(ldsRQdry_out), '%.2e' % numpy.max(ldsRQsemi_out), '%.2e' % numpy.min(ldsRQspray_out),],

        "Unit": ['', '','', '', '', '', '','', '', '', '', '','', '', '', '', '',],
    }
    return data

pvheadings = getheaderpv()
pvuheadings = getheaderpvu()
deheadings = getheaderde()
plantec25noaecheadings = getheaderplantec25noaec()
plantecdrysemisprayheadings = getheaderplantecdrysemispray()
sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(pvheadings, pvuheadings, deheadings, plantec25noaecheadings, plantecdrysemisprayheadings, sumheadings, tmpl,terrplant_obj):
    html_all = table_1(pvheadings, tmpl, terrplant_obj)
    html_all = html_all + table_2(pvuheadings, tmpl, terrplant_obj)
    html_all = html_all + table_3(deheadings, tmpl, terrplant_obj)
    html_all = html_all + table_4(plantec25noaecheadings, tmpl, terrplant_obj)
    html_all = html_all + table_5(plantecdrysemisprayheadings, tmpl, terrplant_obj)
    return html_all

def table_sum_input(sumheadings, tmpl, A, I, R, D, nms, lms, nds, lds):
        #pre-table sum_input
        html = """
        <table border="1" border="1" class="out_1">
        <tr><td><H3>Summary Statistics (Iterations=%s)</H3></td></tr>
        <tr></tr>
        </table>
        """%(i-1)
        #table sum_input
        tsuminputdata = gettsumdata(A, I, R, D, nms, lms, nds, lds)
        tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
        html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
        return html

def table_sum_output(rundry_out, runsemi_out, spray_out, totaldry_out, totalsemi_out, 
                    nmsRQdry_out, nmsRQsemi_out, nmsRQspray_out, 
                    lmsRQdry_out, lmsRQsemi_out, lmsRQspray_out, 
                    ndsRQdry_out, ndsRQsemi_out, ndsRQspray_out, 
                    ldsRQdry_out, ldsRQsemi_out, ldsRQspray_out):

        #pre-table sum_input
        html = """
        <br>
        """
        #table sum_input
        tsumoutputdata = gettsumdata_out(rundry_out, runsemi_out, spray_out, totaldry_out, totalsemi_out, 
                    nmsRQdry_out, nmsRQsemi_out, nmsRQspray_out, 
                    lmsRQdry_out, lmsRQsemi_out, lmsRQspray_out, 
                    ndsRQdry_out, ndsRQsemi_out, ndsRQspray_out, 
                    ldsRQdry_out, ldsRQsemi_out, ldsRQspray_out)
        html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
        return html

def table_1(pvheadings, tmpl, terrplant_obj):
        #pre-table 1
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs: Chemical Identity</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        #table 1
        t1data = gett1data(terrplant_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html

def table_2(pvuheadings, tmpl, terrplant_obj):
        # #pre-table 2
        html = """
            <H4 class="out_2 collapsible" id="section3"><span></span>Toxicity Properties</H4>
                <div class="out_ container_output">
        """
        #table 2
        t2data = gett2data(terrplant_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

def table_3(deheadings, tmpl, terrplant_obj):
        #pre-table 3
        html = """
        <br>
        <H3 class="out_3 collapsible" id="section4"><span></span>Exposure Estimates</H3>
        <div class="out_">
            <H4 class="out_3 collapsible" id="section5"><span></span>Granular Application</H4>
                <div class="out_ container_output">
        """
        #table 3
        t3data = gett3data(terrplant_obj)
        t3rows = gethtmlrowsfromcols(t3data,deheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=deheadings)))
        html = html + """
                </div>
        """
        return html

def table_4(plantec25noaecheadings, tmpl, terrplant_obj):
        #pre-table 4
        html = """     
            <H4 class="out_4 collapsible" id="section6"><span></span>Foliar Spray Application (contact with foliar residues and directly applied spray)</H4>
                <div class="out_ container_output">
        """
        #table 4
        t4data = gett4data(terrplant_obj)
        t4rows = gethtmlrowsfromcols(t4data,plantec25noaecheadings)
        html = html + tmpl.render(Context(dict(data=t4rows, headings=plantec25noaecheadings)))
        html = html + """
                </div>
        """
        return html

def table_5(plantecdrysemisprayheadings, tmpl, terrplant_obj):
        #pre-table 5
        html = """         
            <H4 class="out_5 collapsible" id="section7"><span></span>Bare Ground Spray Application (contact with soil residues and directly applied spray)</H4>
                <div class="out_ container_output">
        """
        #table 5
        t5data = gett5data(terrplant_obj)
        t5rows = gethtmlrowsfromcols(t5data,plantecdrysemisprayheadings)
        html = html + tmpl.render(Context(dict(data=t5rows, headings=plantecdrysemisprayheadings)))
        html = html + """
                </div>
        </div>
        """
        return html
