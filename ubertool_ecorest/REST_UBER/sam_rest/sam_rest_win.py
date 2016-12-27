#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import zipfile
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string
import random
import keys_Picloud_S3


# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def sam():
    ##########################################################################################
    #####AMAZON KEY, store output files. You might have to write your own import approach#####
    ##########################################################################################
    key = keys_Picloud_S3.amazon_s3_key
    secretkey = keys_Picloud_S3.amazon_s3_secretkey
    ##########################################################################################
    ##########################################################################################
    ##########################################################################################

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    exe = "SuperPRZMpesticide_win.exe"
    sam_path = os.path.join(curr_dir, 'bin', 'ubertool_superprzm_src', 'Debug', exe)
    print sam_path
    sam_args = os.path.join(curr_dir, 'bin')
    a = subprocess.Popen(sam_path + " " + sam_args, shell=1)
    a.wait()
    print "Done"

    name_temp = id_generator()
    print name_temp

    ##zip the output files
    zout = zipfile.ZipFile("temp.zip", "w", zipfile.ZIP_DEFLATED)
    # for name in fname:
    #     if name !='przm5.exe' and name !='test.dvf':
    #         zout.write(name)
    superPRZM_ouput = os.path.join(curr_dir, 'bin', 'dwPestOut_all', 'dwPestOut_SoilGrps', 'Reservoirs',
                                   '1838_pestAvgConc_distrib.out')
    print superPRZM_ouput
    zout.write(superPRZM_ouput, os.path.basename(superPRZM_ouput))
    zout.close()

    ##Create connection to S3
    conn = S3Connection(key, secretkey)
    bucket = Bucket(conn, 'super_przm')
    k = Key(bucket)

    ##Generate link to zip file
    name1 = 'SAM_' + name_temp + '.zip'
    k.key = name1
    link = 'https://s3.amazonaws.com/super_przm/' + name1
    print link

    ##Upload zip file to S3
    k.set_contents_from_filename('temp.zip')
    k.set_acl('public-read-write')
    print 'upload finished'

    return link, "Done!"
