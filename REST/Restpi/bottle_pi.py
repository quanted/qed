from bottle import route, run, post, request, auth_basic, abort
import keys_Picloud_S3
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import os

##########################################################################################
#####KEY, store output files. You might have to write your own import approach#####
##########################################################################################
s3_key = keys_Picloud_S3.amazon_s3_key
s3_secretkey = keys_Picloud_S3.amazon_s3_secretkey
rest_key = keys_Picloud_S3.picloud_api_key
rest_secretkey = keys_Picloud_S3.picloud_api_secretkey
###########################################################################################

host_ip='10.122.46.109'

from pymongo import Connection
connection = Connection(host_ip, 27017)
db = connection.ubertool

def check(user, passwd):
    if user == rest_key and passwd == rest_secretkey:
        return True
    return False

###############geneec####################
@route('/geneec/', method='POST') # or @route('/login', method='POST')
@auth_basic(check)
def myroute():
    print 'auth=', request.auth
    print 'remote_addr=', request.remote_addr
    print 'request=', request

    for k, v in request.json.iteritems():
        exec '%s = v' % k

    import gfix
    result = gfix.geneec2(APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,FOTHAP)
    print result
    return {'result': result}
all_result = {}

@route('/geneec1/<jid>', method='POST') # or @route('/login', method='POST')
@auth_basic(check)
def myroute(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k

    all_result.setdefault(jid,{}).setdefault('status','none')

    import gfix
    print request.json
    result = gfix.geneec2(APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,FOTHAP)
    # print result
    # print 'jid=', jid

    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    element={"_id":jid, "output":all_result[jid]['result'], "input":all_result[jid]['input']}
    db['geneec'].save(element)
    print element 
    return {'result': result, '_id':jid, 'jid':jid}

###############przm5####################
@route('/przm5/<jid>', method='POST') 
@auth_basic(check)
def przm5_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')

    from przm5_rest_pi import PRZM5_pi_new
    result = PRZM5_pi_new.PRZM5_pi(pfac, snowmelt, evapDepth, 
                                 uslek, uslels, uslep, fieldSize, ireg, slope, hydlength,
                                 canopyHoldup, rootDepth, canopyCover, canopyHeight,
                                 NumberOfFactors, useYears,
                                 USLE_day, USLE_mon, USLE_year, USLE_c, USLE_n, USLE_cn,
                                 firstyear, lastyear,
                                 dayEmerge_text, monthEmerge_text, dayMature_text, monthMature_text, dayHarvest_text, monthHarvest_text, addYearM, addYearH,
                                 irflag, tempflag,
                                 fleach, depletion, rateIrrig,
                                 albedo, bcTemp, Q10Box, soilTempBox1,
                                 numHoriz,
                                 SoilProperty_thick, SoilProperty_compartment, SoilProperty_bulkden, SoilProperty_maxcap, SoilProperty_mincap, SoilProperty_oc, SoilProperty_sand, SoilProperty_clay,
                                 rDepthBox, rDeclineBox, rBypassBox,
                                 eDepthBox, eDeclineBox,
                                 appNumber_year, totalApp,
                                 SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, Rela_a, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
                                 PestDispHarvest,
                                 nchem, convert_Foliar1, parentTo3, deg1To2, foliarHalfLifeBox,
                                 koc_check, Koc,
                                 soilHalfLifeBox,
                                 convertSoil1, convert1to3, convert2to3)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    element={"_id":jid, "output_link":all_result[jid]['result'][0], "output_val":all_result[jid]['result'][1:4], "input":all_result[jid]['input']}
    db['przm5'].save(element)

    # print request.json
    # print all_result
    # print list(ff)[0][0]
    return {'result': result, '_id':jid, 'jid':jid}

# ###############File upload####################
@route('/file_upload', method='POST') 
@auth_basic(check)
def file_upload():
    import shutil
    for k, v in request.json.iteritems():
        exec '%s = v' % k

    ##upload file to S3
    conn = S3Connection(s3_key, s3_secretkey)
    bucket = Bucket(conn, model_name)
    k=Key(bucket)

    os.chdir(src1)
    k.key=name1
    link='https://s3.amazonaws.com/'+model_name+'/'+name1

    print 'begin upload'
    k.set_contents_from_filename('test.zip')
    k.set_acl('public-read-write')
    print 'end upload'
    src1_up=os.path.abspath(os.path.join(src1, '..'))
    os.chdir(src1_up)
    shutil.rmtree(src1)

###############Check History####################
# @route('/geneec1/job/<jid>') 
# @auth_basic(check)
# def show_res(jid):
#     import json
#     print all_result
#     return all_result[jid]

@route('/ubertool_history/<model_name>/<jid>')
@auth_basic(check)
def get_document(model_name, jid):
    entity = db[model_name].find_one({'_id':jid})
    if not entity:
        abort(404, 'No document with jid %s' % jid)
    return entity

run(host=host_ip, port=7777, debug=True)




