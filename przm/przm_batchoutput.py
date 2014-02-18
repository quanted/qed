import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from przm import przm_batchmodel, przm_tables
import json
import base64
import urllib
import logging
logger = logging.getLogger('PRZM Batch Model')
from uber import uber_lib
from datetime import datetime,timedelta
import time

# from threading import Thread
# import Queue
# import multiprocessing
# from collections import OrderedDict
# import rest_funcs

from boto import sqs
import keys_Picloud_S3
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import string, random

conn = sqs.connect_to_region("us-east-1",
                             aws_access_key_id='AKIAJZZHOBNJDUE6CWBQ',
                             aws_secret_access_key='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')
my_queue = conn.get_queue('uber_batch')

# Generate a random ID for file save
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

name_temp=id_generator()

##########################AMAZON KEY###################################################
key = keys_Picloud_S3.amazon_s3_key
secretkey = keys_Picloud_S3.amazon_s3_secretkey
##########################################################################################
ts = datetime.now()
if(time.daylight):
    ts1 = timedelta(hours=-4)+ts
else:
    ts1 = timedelta(hours=-5)+ts
batch_jid = ts1.strftime('%Y%m%d%H%M%S%f')

class przmBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        thefile = form['file-0']
        thefile_str = thefile.file.getvalue()



        # iter_html = przm_batchmodel.loop_html(thefile)
        # iter_html=loop_html(thefile)

        # q = taskqueue.Queue('pull-queue')
        # tasks = []
        # # payload_str = 'hello world'
        # tasks.append(taskqueue.Task(payload=thefile, method='PULL'))
        # q.add(tasks)
        # print q

        conn_S3 = S3Connection(key, secretkey)
        bucket = Bucket(conn_S3, 'przm_batch')
        k=Key(bucket)
        name1='PRZM_batch_'+name_temp+'.csv'
        k.key=name1
        k.set_contents_from_string(thefile_str)
        link='https://s3.amazonaws.com/przm_batch/'+name1
        k.set_acl('public-read-write')

        m = sqs.message.Message()
        m.set_body( json.dumps({'link': link, 'batch_jid':batch_jid}))
        my_queue.write(m)

        # msg = {'properties': {'content_type': 'application/json', 
        #                       'content_encoding': 'utf-8', 
        #                       'body_encoding':'base64', 
        #                       'delivery_tag':None, 
        #                       'delivery_info': {'exchange':None, 'routing_key':None}},}
        # body = {'id':'theid',
        #         'task':'VTOServer.apps.vto.tasks.begin_processing',
        #         'url':['s3.abc.com']}
        # msg.update({'body':base64.encodestring(json.dumps(body))})
        # my_queue.write(my_queue.new_message(json.dumps(msg)))


        # Give the job an hour to run, plenty of time to avoid double-runs
        # pointer = my_queue.read()

        # pointer = my_queue.get_messages(num_messages=10, visibility_timeout=None, attributes=None, wait_time_seconds=3)
        # # pointer = conn.receive_message('uber_batch', number_messages=10, visibility_timeout=None, attributes=None, wait_time_seconds=None)
        # print len(pointer)
        # for i in pointer:
        #     print i.get_body()



        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm',
                'model_attributes':'PRZM Batch Output'})
        # html = html + przm_tables.timestamp()
        # logger.info(iter_html)
        # html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przmBatchOutputPage)], debug=True)


def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
