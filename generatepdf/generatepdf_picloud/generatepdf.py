'''
Created on Mar 25, 2013

@author: th
'''

import os
import stat
import shutil
import subprocess
import zipfile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string
import random
import time
import sys
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

name_temp=id_generator()

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
key = keys_Picloud_S3.amazon_s3_key
secretkey = keys_Picloud_S3.amazon_s3_secretkey
##########################################################################################

html_str="""
<table border="1" class="out_1">
        <tbody><tr><th colspan="2">Inputs</th></tr>
        <tr>
            <td>Application method</td>
            <td id="app_method_val">Aerial</td>
        </tr>
        <tr id="Orc_type" style="display: none;">
            <td>Orchard type</td>
            <td>None</td>
        </tr>
        <tr>
            <td>Drop size</td>
            <td>Fine</td>
        </tr>
        <tr>
            <td>Ecosystem type</td>
            <td>EPA Pond</td>
        </tr>
        </tbody></table><br>
"""

html_str= html_str + """<table border="1" class="out_1">
            <tbody><tr><th colspan="2">Inputs: Chemical Identity</th></tr>
            <tr>
                <td>Chemical Name</td>
                <td>Alachlor</td>
            </tr>
            <tr>
                <td>PC Code</td>
                <td>90501</td>
            </tr>
            <tr>
                <td>Use</td>
                <td>Corn</td>
            </tr>
            <tr>
                <td>Application Method</td>
                <td>Ground</td>
            </tr>
            <tr>
                <td>Application Form</td>
                <td>Spray</td>
            </tr>
            <tr>
                <td>Solubility in Water (ppm)</td>
                <td>240</td>
            </tr><tr>
        </tr></tbody></table><table border="1" class="out_2">
            <tbody><tr>
                <th colspan="3">Inputs: Input Parameters Used to Derive EECs</th>
            </tr>
            <tr>
                <td>Incorporation</td>
                <td>1</td>
                <td></td>
            </tr>
            <tr>
                <td>Application Rate</td>
                <td>4</td>
                <td>lbs ai/A</td>
            </tr>
            <tr>
                <td>Drift Fraction</td>
                <td>0.01</td>
                <td></td>
            </tr>
            <tr>
                <td>Runoff Fraction</td>
                <td>0.05</td>
                <td></td>
            </tr>
        </tbody></table><table border="1" class="out_3">
            <tbody><tr><th colspan="2">EECs - Units in (lbs a.i./A)</th></tr>
            <tr>
                <th colspan="1">Description</th>
                <th colspan="1">EEC</th>
            </tr>
            <tr>
                <td>Runoff to Dry Areas</td>
                <td>2.00E-01</td>
            </tr>
            <tr>
                <td>Runoff to Semi-Aquatic Areas</td>
                <td>2.00E+00</td>
            </tr>
            <tr>
                <td>Spray Drift</td>
                <td>4.00E-02</td>
            </tr>
            <tr>
                <td>Total for Dry Areas</td>
                <td>2.40E-01</td>
            </tr>
            <tr>
                <td>Total for Semi-Aquatic Areas</td>
                <td>2.04E+00</td>
            </tr>
        </tbody></table><table border="1" class="out_4">
            <tbody><tr>
                <th colspan="5">Inputs: Plant Survival and Growth Data Used for RQ Derivation - Units in (lbs a.i./A)</th>
            </tr>
            <tr>
                <th></th>
                <th colspan="2">Seedling Emergence</th>
                <th colspan="2">Vegetative Vigor</th>
            </tr>
            <tr>
                <td>Plant Type</td>
                <td>EC<sub>25</sub></td>
                <td>NOAEC</td>
                <td>EC<sub>25</sub></td>
                <td>NOAEC</td>
            </tr>
            <tr>
                <td>Monocot</td>
                <td>0.0067</td>
                <td>0.0023</td>
                <td>0.068</td>
                <td>0.037</td>
            </tr>
            <tr>
                <td>Dicot</td>
                <td>0.034</td>
                <td>0.019</td>
                <td>1.4</td>
                <td>0.67</td>
            </tr>
        </tbody></table><table border="1" class="out_4">
            <tbody><tr>
                <th colspan="5">RQ Values for Plants in Dry and Semi-aquatic Areas Exposed to Through Runoff and/or Spray Drift *</th>
            </tr>
            <tr>
                <th colspan="1">Plant Type</th>
                <th colspan="1">Listed Status</th>
                <th colspan="1">Dry</th>
                <th colspan="1">Semi-Aquatic</th>
                <th colspan="1">Spray Drift</th>
            </tr>
            <tr>
                <td>Monocot</td>
                <td>non-listed</td>
                <td>3.58E+01</td>
                <td>3.04E+02</td>
                <td>5.97E+00</td>
            </tr>
            <tr>
                <td>Monocot</td>
                <td>listed</td>
                <td>1.04E+02</td>
                <td>8.87E+02</td>
                <td>1.74E+01</td>
            </tr>
            <tr>
                <td>Dicot</td>
                <td>non-listed</td>
                <td>7.06E+00</td>
                <td>6.00E+01</td>
                <td>1.18E+00</td>
            </tr>
            <tr>
                <td>Dicot</td>
                <td>listed</td>
                <td>1.26E+01</td>
                <td>1.07E+02</td>
                <td>2.11E+00</td>
            </tr>
            <tr>
                <td colspan="5">* If RQ &gt; 1.0, the Level of Concern is exceeded, resulting in potential risk to that plant group.</td><td>
        </td></tr></tbody></table>"""

html_css="""
<style>
table {margin-bottom:16px;}
th {text-align:center; padding:2px; font-size:12px;}
td {text-align:center; padding:2px; font-size:11px;}
</style>
"""

# extract1 = "data:image/png;base64,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"
# html_str = html_str + """<br>"""
# html_str = html_str + """<img id="imgChart1" src="%s" />"""%(extract1)

#text_file = open("Output.txt", "w")
#text_file.write(html_str)
#text_file.close()

# import sys
# import xhtml2pdf

import xhtml2pdf


from xhtml2pdf import pisa                         

cwd=os.getcwd()
os.chdir(cwd)

# print xhtml2pdf.__file__
# print sys.modules

filename = "model.pdf"
pdf = pisa.CreatePDF(html_css+html_str, file(filename, "wb"))
pdf.dest.close()

conn = S3Connection(key, secretkey)
bucket = Bucket(conn, 'ubertool_pdfs')
k=Key(bucket)
name1=name_temp+".pdf"
k.key=name1
k.set_contents_from_filename(filename)
link='https://s3.amazonaws.com/ubertool_pdfs/'+name1
k.set_acl('public-read-write')

print (link)

