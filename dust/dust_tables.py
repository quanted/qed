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

def gett1data(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res):
    data = { 
        "Parameter": ['Chemical Name', 'Label EPA Reg. No.', 'Maximum Single Application Rate', 
            'Fraction of Pesticide Assumed at the Surface','Dislodgeable Foliar Residue',],
        "Value": [chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res,],
        "Units": ['', '', 'lbs a.i./A', '','mg a.i./cm^2', ],
    }
    return data

def gett2data(bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study,
               mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw):
    data = { 
        "Parameter": ['Bird Acute Oral Study (OCSPP 850.2100) MRID#', 'Additional Comments About the Study (if any)', 
            mark_safe('Lowest Bird Acute Oral LD<sub>50</sub> &asymp; Amphibian Dermal LD<sub>50</sub>'), 
            'Tested Bird Body Weight','Mineau Scaling Factor for Birds',
            mark_safe('Mammal Acute Dermal (OCSPP 870.1200) MRID#'),'Additional Comments About Study (if any)',
            mark_safe('Mammal Acute Dermal LD<sub>50</sub>'),'Tested Mammal Body Weight',],
        "Value": [bird_acute_oral_study, bird_study_add_comm,low_bird_acute_ld50, test_bird_bw, mineau, mamm_acute_derm_study,
               mamm_study_add_comm, mam_acute_derm_ld50, test_mam_bw,],
        "Units": ['', '', 'mg a.i./kg-bw', 'g','','','','mg a.i./kg-bw','g', ],
    }
    return data

def gett3data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett4data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett5data(birdderm,herpderm,mammderm):
    data = { 
        "Parameter": ['Bird External Dermal Dose', 'Reptile/Amphibian External Dermal Dose', 'Mammal External Dermal Dose',],
        "Value": ['%.2e' % birdderm,'%.2e' % herpderm,'%.2e' % mammderm, ],
        "Units": ['mg a.i./kg-bw', 'mg a.i./kg-bw', 'mg a.i./kg-bw', ],
    }
    return data

def gett6data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data

def gett7data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data

def gett8data(birdrisk,birdmess,reprisk,repmess,amphibrisk,amphibmess,mammrisk,mammmess):
    data = { 
        "Parameter": ['Bird', 'Reptile', 'Amphibian', 'Mammal',],
        "Value": ['%.2e' % birdrisk,'%.2e' % reprisk,'%.2e' % amphibrisk, '%.2e' % mammrisk, ],
        "Results": [birdmess, repmess, amphibmess, mammmess, ],
    }
    return data