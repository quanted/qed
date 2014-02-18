import time, threading
from boto import sqs
import ast
import os
import urllib
import sys
import csv
import przm_batchmodel
sys.path.append("../")
import keys_Picloud_S3


# import keys_Picloud_S3
# from boto.s3.connection import S3Connection
# from boto.s3.key import Key
# from boto.s3.bucket import Bucket

# ##########################AMAZON KEY###################################################
# key = keys_Picloud_S3.amazon_s3_key
# secretkey = keys_Picloud_S3.amazon_s3_secretkey
# ##########################################################################################


##########################connect to sqs###################################################
conn = sqs.connect_to_region("us-east-1",
                             aws_access_key_id=keys_Picloud_S3.aws_access_key_id,
                             aws_secret_access_key=keys_Picloud_S3.aws_secret_access_key)
my_queue = conn.get_queue('uber_batch')
##########################connect to sqs###################################################

# print os.getcwd()
# przm_batchmodel.loop_html(os.getcwd()+'/batch_temp.csv')


def foo():
    print(time.ctime())
    pointer = my_queue.read()
    if pointer:
        a = pointer.get_body()
        a_dict = ast.literal_eval(a)
        batch_temp_link = a_dict['link']
        batch_jid = a_dict['batch_jid']
        print 'print0= work', a
        urllib.urlretrieve(batch_temp_link, os.getcwd()+'/batch_temp.csv')
        przm_batchmodel.loop_html(os.getcwd()+'/batch_temp.csv', batch_jid)
    else:
        print 'No New Messages'

foo()

# def foo_target():
#   while True:
#     foo()
#     time.sleep(10)


# if __name__ == '__main__':
#     foo_target()
