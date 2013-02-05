# -*- coding: utf-8 -*-
import os
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb

import json
import base64
import urllib
from google.appengine.api import urlfetch
from datetime import  datetime,timedelta


############Provide the key and connect to the picloud####################
api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################

#######call the function################# 
def get_jid(met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft):

    url='https://api.picloud.com/r/3303/przm_s1_new' 
    met=json.dumps(met)
    inp=json.dumps(inp)
    run=json.dumps(run)
    MM=json.dumps(str(MM))
    DD=json.dumps(str(DD))
    YY=json.dumps(str(YY))    
    CAM_f=json.dumps(CAM_f)    
    DEPI_text=json.dumps(DEPI_text)    
    Ar_text=json.dumps(Ar_text)    
    EFF=json.dumps(EFF)    
    Drft=json.dumps(Drft)    
    
    
    data = urllib.urlencode({"met":met,"inp":inp,"run":run,"MM":MM,"DD":DD,"YY":YY,"CAM_f":CAM_f,
                             "DEPI_text":DEPI_text,"Ar_text":Ar_text,"EFF":EFF,"Drft":Drft})

#    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers) 
#    jid= json.loads(response.content)['jid']
#    output_st = ''
#        
#    while output_st!="done":
#        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
#        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']
#
#    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
#    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
#    output_val = json.loads(response_val.content)['result']
#    return(jid, output_st, output_val)
    return(data)
    

                                               
final_res=get_jid("W23232.DVF", "CA1Wal-P.INP", "CA1Wal-P.RUN","04", "25", "61", "2", "4.000", "1.000", ".9500", "0.0500")
print final_res







CAM_f=%222%22
&run=%22CA1Wal-P.RUN%22&DD=%2225%22&inp=%22CA1Wal-P.INP%22&YY=%2261%22&met=%22W23232.DVF%22&EFF=%22.9500%22&DEPI_text=%224.000%22&Drft=%220.0500%22&Ar_text=%221.000%22&MM=%2204%22





















    