from django.template import Context, Template
from django.utils.safestring import mark_safe
from es_mapping_openlayer import es_mapping_openlayer_model
import time
import datetime
import os
from google.appengine.ext.webapp import template

def timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Endangered Species Mapper<br>
    """
    html = html + st
    html = html + " (UTC)</b>"
    html = html + """
    </div>"""
    return html


def table_all(es_obj):
    table1_out = table_1()
    table2_out = table_2()
    templatepath = os.path.dirname(__file__) + '/../templates/'
    html_plot = template.render(templatepath + 'ESMapper_OpenLayer.html', {
               'NSF': es_obj.NSF,
               'NSP': es_obj.NSP,
               'NSM': es_obj.NSM,
               'Crop': es_obj.Crop,
               'Pesticide': es_obj.Pesticide,
               'IUCN_Amphibians': es_obj.IUCN_Amphibians,
               'IUCN_Birds': es_obj.IUCN_Birds,
               'IUCN_Mammals': es_obj.IUCN_Mammals,
               'IUCN_Mammals_Marine': es_obj.IUCN_Mammals_Marine,
               'IUCN_Coral': es_obj.IUCN_Coral,
               'IUCN_Reptiles': es_obj.IUCN_Reptiles,
               'IUCN_Seagrasses': es_obj.IUCN_Seagrasses,
               'IUCN_SeaCucumbers': es_obj.IUCN_SeaCucumbers,
               'IUCN_Mangrove': es_obj.IUCN_Mangrove,
               'IUCN_MarineFish': es_obj.IUCN_MarineFish,
               'USFWS_p': es_obj.USFWS_p,
               'USFWS_l': es_obj.USFWS_l})


    html_all = timestamp() + table1_out + table2_out + html_plot
    return html_all


def table_1():
    html = """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                <div class="out_input_table out_">
                </div>"""
    return html

# def table_2():
#     html = """
#             <H3 class="out_3 collapsible" id="section1"><span></span>Endangered Species Mapper</H3>
#             <div class="out_3">
#                 <H4 class="out_4 collapsible" id="section1"><span></span></H4>
#                     <div id="map"></div>
#             </div>
#            """
def table_2():
    html = """
            <H3 class="out_3 collapsible" id="section1"><span></span>Endangered Species Mapper</H3>
                    <div id="map"></div>
           """

    return html