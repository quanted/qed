import os
import keys_Picloud_S3
import base64
import urllib
import json
from google.appengine.api import urlfetch
import numpy as np
import ast
import logging
from datetime import datetime, timedelta
import time
#############################Provide the key and connect to the picloud#####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}

###########################A class helps dictionary to be converted to JSON when it contains numpy element################################ 
class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)

###########################A function to generate JID################################ 
def gen_jid():
    ts = datetime.now()
    if(time.daylight):
        ts1 = timedelta(hours=-4)+ts
    else:
        ts1 = timedelta(hours=-5)+ts
    jid = ts1.strftime('%Y%m%d%H%M%S%f')
    return jid

###########################function to save a single run to MongoDB################################ 
def save_dic(output_html, model_object_dict, model_name, run_type):
    all_dic = {"model_name":model_name, "_id":model_object_dict['jid'], "run_type":run_type, "output_html":output_html, "model_object_dict":model_object_dict}
    data = json.dumps(all_dic, cls=NumPyArangeEncoder)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/save_history'
    try:
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    except:
        pass

###########################function to save batch runs to MongoDB################################ 
def batch_save_dic(output_html, model_object_dict, model_name, run_type, jid_batch, ChkCookie, templatepath):
    from uber import uber_lib
    from google.appengine.ext.webapp import template

    html_save = uber_lib.SkinChk(ChkCookie, "Batch")
    html_save = html_save + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':model_name,'page':'output'})
    html_save = html_save + template.render (templatepath + '03ubertext_links_left.html', {})                
    html_save = html_save + output_html
    html_save = html_save + template.render(templatepath + '06uberfooter.html', {'links': ''})
    
    all_dic = {"model_name":model_name, "_id":jid_batch, "run_type":run_type, "output_html":html_save, "model_object_dict":model_object_dict}
    data = json.dumps(all_dic, cls=NumPyArangeEncoder)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/save_history'
    try:
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    except:
        pass
###########################function to update html saved in MongoDB################################ 
def update_html(output_html, jid, model_name):
    all_dic = {"model_name":model_name, "_id":jid, "output_html":output_html}
    data = json.dumps(all_dic)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/update_html'
    try:
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    except:
        pass
###########################function to retrive html from MongoDB################################ 
def get_output_html(jid, model_name):
    all_dic = {"jid":jid, "model_name":model_name}
    data = json.dumps(all_dic)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/get_html_output'
    try:
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    except:
        pass
    if response:
        html_output = json.loads(response.content)['html_output']
    else:
        html_output =""
    return html_output

###########################function to retrive html from MongoDB################################ 
def create_batchoutput_html(jid, model_name):
    all_dic = {"jid":jid, "model_name":model_name}
    data = json.dumps(all_dic)
    url=os.environ['UBERTOOL_REST_SERVER'] + '/get_przm_batch_output'
    try:
        response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
    except:
        pass
    if response:
        result = response.content
        result_dict = ast.literal_eval(result)['result']
        result_obj_all = []
        for i in result_dict:
            result_obj_temp = Struct(**i)
            result_obj_all.append(result_obj_temp)
    else:
        result_obj_all =[]
    return result_obj_all

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

###########################creat an object to display history runs################################ 
class user_hist(object):
    def __init__(self, user_id, model_name):
        import datetime
        self.user_id = user_id
        self.model_name = model_name
    ########call the function################# 
        self.all_dic = {"user_id": user_id, "model_name":model_name}
        self.data = json.dumps(self.all_dic)
        self.url=os.environ['UBERTOOL_REST_SERVER']+'/user_history'
        self.user_id = []
        self.time_id = []
        self.jid = []
        self.run_type = []
        self.model_name = model_name

        try:
            self.response = urlfetch.fetch(url=self.url, payload=self.data, method=urlfetch.POST, headers=http_headers, deadline=60)
        # logger.info(self.response.content)
        except:
            self.response = None
        if self.response:
            self.output_val = json.loads(self.response.content)['hist_all']
            self.total_num = len(self.output_val)

            for element in self.output_val:
                self.user_id.append(element['user_id'])
                self.jid.append(element['_id'])
                self.time_id.append(datetime.datetime.strptime(element['_id'], '%Y%m%d%H%M%S%f').strftime('%Y-%m-%d %H:%M:%S'))
                self.run_type.append(element['run_type'])
        else:
            self.total_num = 0

