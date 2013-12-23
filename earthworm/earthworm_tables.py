import numpy
from django.template import Context, Template
from django.utils.safestring import mark_safe
from earthworm import earthworm_model,earthworm_parameters
import logging
import time
import datetime
import os
from google.appengine.ext.webapp import template

logger = logging.getLogger("earthwormTables")


def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Earthworm Fugacity Modeling<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html

def table_all(earthworm_obj):
    table1_out = table_1()
    table2_out = table_2(earthworm_obj)
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_all = table1_out + table2_out 
    return html_all

# def getheaderpvu():
#     headings = ["Parameter", "Value", "Units"]
#     return headings    

# def gethtmlrowsfromcols(data, headings):
#     columns = [data[heading] for heading in headings]

#     # get the length of the longest column
#     max_len = len(max(columns, key=len))

#     for col in columns:
#         # padding the short columns with None
#         col += [None,] * (max_len - len(col))

#     # Then rotate the structure...
#     rows = [[col[i] for col in columns] for i in range(max_len)]
#     return rows

# def getdjtemplate():
#     dj_template ="""
#     <table class="out_">
#     {# headings #}
#         <tr>
#         {% for heading in headings %}
#             <th>{{ heading }}</th>
#         {% endfor %}
#         </tr>
#     {# data #}
#     {% for row in data %}
#     <tr>
#         {% for val in row %}
#         <td>{{ val|default:'' }}</td>
#         {% endfor %}
#     </tr>
#     {% endfor %}
#     </table>
#     """
#     return dj_template


# def earthwormoutput(earthworm_obj):
#     data = { 
#         "Parameter": ['Chemical concentration in earthworm tissue',],
#         "Value": ['%.5e' % %earthworm_obj.earthworm_fugacity_out,],
        
#         "Units": ['g/kg',],
#     }
#     return data

def table_1():
    html = """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                <div class="out_input_table out_">
                </div>
                
                <script type="text/javascript">
                    $(document).ready(function(){

                    // Initialize output page//

                    //$('#export_menu').hide()

                    $(".out_input_table").append(localStorage.html_input);
                    $(".out_input_table :input").attr('disabled', true);

                    element_all = localStorage.html_new.split("&")
                    // console.log(element_all)
                    element1 = localStorage.html_new.split("&")[0].split("=")
                    // console.log(element_all.length)
                    for (i=0; i<element_all.length; i++) {
                        element_name_t = element_all[i].split("=")[0]
                        element_val_t = element_all[i].split("=")[1]
                        $('[name="'+element_name_t+'"]').val(element_val_t)
                    }
                    $(".input_button").hide()
                    })
                </script>"""
    return html


def table_2(earthworm_obj):
    html = """
            <H3 class="out_3 collapsible" id="section1"><span></span>Earthworm Fugacity Modeling Output</H3>
            <div class="out_3">
                <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                    <div id="map">%s</div>
            </div>
           """%earthworm_obj.earthworm_fugacity_out
    return html


