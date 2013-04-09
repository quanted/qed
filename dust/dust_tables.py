import numpy as np
import django
from django.template import Context, Template

#table 1: chemical information
def ChemInfoTable(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res):
    ChemTable = ("Chemical Name", chemical_name, "",
    	 		 "Label EPA Reg No.", label_epa_reg_no, "",
    	 		 "Maximum single application rate", ar_lb, "lbs a.i/acre",
    	 		 "Fraction of pesticide assumed at surface", frac_pest_surface, "",
    	 		 "Dislodgeable foliar residue", dislodge_fol_res, "mg a.i./cm^2")
    ChemTable.shape(5,3)
    return ChemTable

def DefaultDicttoHTML():
    data = { 
        "heading1": ['h1-val1', 'h1-val2', 'h1-val3', ],
        "heading2": ['h2-val1', ],
        "heading3": ['h3-val1', 'h3-val2', 'h3-val3', 'h3-val4', ],
    }

    headings = ["heading1", "heading2", "heading3"]

    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]


    dj_template ="""
    <table>
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

    # return the template:
    tmpl = Template(dj_template)
    return tmpl
