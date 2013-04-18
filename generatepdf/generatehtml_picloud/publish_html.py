import cloud
import sys 
import os
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

cloud.setkey(keys_Picloud_S3.picloud_api_key, keys_Picloud_S3.picloud_api_secretkey)   

def generatehtml_pi(input_str): 
    import os, sys
    lib_path = os.path.abspath('/home/picloud/generatehtml')
    sys.path.append(lib_path)

    table_str = input_str[0]
    nop = int(input_str[1])
    jq_str = input_str[2]

    final_str = table_str
    final_str = final_str + """<br>"""
    if (nop>0):
        for i in range(nop):
            final_str = final_str + """<img id="imgChart1" src="%s" />"""%(jq_str[i])
            final_str = final_str + """<br>"""

    import generatehtml_pi
    ff=generatehtml_pi.generatehtml_pi(final_str)
    return ff
 
cloud.rest.publish(func=generatehtml_pi, label='generatehtml_pi_s1', _env='t-fortran77-test', _type='s1', _profile=True )
print 'Done gen_html'


# def generatepdf_pi_iec(input_str): 
#     import os, sys
#     lib_path = os.path.abspath('/home/picloud/generatepdf')
#     sys.path.append(lib_path)
#     import generatepdf_pi_iec
#     ff=generatepdf_pi_iec.generatepdf_pi_iec(input_str)
#     return ff
 
# cloud.rest.publish(func=generatepdf_pi_iec, label='generatepdf_pi_iec_s1', _env='t-fortran77-test', _type='s1', _profile=True )
# print 'Done gen_pdf_iec'

# def gen_pdf_exp(input_str): 
#     import os, sys
#     lib_path = os.path.abspath('/home/picloud/generatepdf')
#     sys.path.append(lib_path)
    
#     table_str=input_str[0]
#     jq_str=input_str[1]

#     final_str = table_str
#     final_str = final_str + """<br>"""
#     final_str = final_str + """<img id="imgChart1" src="%s" />"""%(jq_str)

#     import generatepdf_pi_exp
#     ff=generatepdf_pi_exp.generatepdf_pi_exp(final_str)
#     return ff
 
# cloud.rest.publish(func=gen_pdf_exp, label='generatepdf_pi_exp_s1', _env='t-fortran77-test', _type='s1', _profile=True )
# print 'Done gen_pdf_exp'
