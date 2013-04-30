#!/usr/bin/python
#
def generatepdf_pi(input_str):
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
    import operator
    import re
    import sys
    from ubertool_src import keys_Picloud_S3

    # Generate a random ID for file save
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    from xhtml2pdf import pisa        
    name_temp=id_generator()

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey

##################################################################################
######Create a folder if it does not existed, where holds calculations' output.#####
##################################################################################
    cwd=os.getcwd()+'/generatepdf'
    print("cwd="+cwd)

    src=cwd
    src1=cwd+'/'+name_temp
    if not os.path.exists(src1):
        os.makedirs(src1)
    else:
        shutil.rmtree(src1)
        os.makedirs(src1)
    os.chdir(src1) 

    input_css="""
            <style>
            table {margin-bottom:16px;}
            th {text-align:center; padding:2px; font-size:12px;}
            td {text-align:center; padding:2px; font-size:11px;}
            </style>
            """

    input_str = input_css + input_str
    filename = "model.pdf"
    pdf = pisa.CreatePDF(input_str, file(filename, "wb"))
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

    return link

