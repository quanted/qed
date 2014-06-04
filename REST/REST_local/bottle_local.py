import bottle
from bottle import route, run, post, request, auth_basic, abort
import keys_Picloud_S3
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import os
import json


#####The folloing two lines could let the REST servers to handle multiple requests##
########################(not necessary for local dev. env.)#########################
# from gevent import monkey
# monkey.patch_all()

##########################################################################################
#####AMAZON KEY, store output files. You might have to write your own import approach#####
##########################################################################################
s3_key = keys_Picloud_S3.amazon_s3_key
s3_secretkey = keys_Picloud_S3.amazon_s3_secretkey
rest_key = keys_Picloud_S3.picloud_api_key
rest_secretkey = keys_Picloud_S3.picloud_api_secretkey
###########################################################################################
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # (or whatever you want)

class NumPyArangeEncoder(json.JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist() # or map(int, obj)
        return json.JSONEncoder.default(self, obj)

import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.ubertool

def check(user, passwd):
    if user == keys_Picloud_S3.picloud_api_key and passwd == keys_Picloud_S3.picloud_api_secretkey:
        return True
    return False

all_result = {}



##################################terrplant#############################################
@route('/terrplant/<jid>', method='POST') 
@auth_basic(check)
def terrplant_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
        # print k, v
    all_result.setdefault(jid,{}).setdefault('status','none')

    from terrplant_rest import terrplant_model_rest
    result = terrplant_model_rest.terrplant(version_terrplant,run_type,A,I,R,D,nms,lms,nds,lds,chemical_name,pc_code,use,application_method,application_form,solubility)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result

    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################terrplant#############################################

##################################sip#############################################
@route('/sip/<jid>', method='POST') 
@auth_basic(check)
def sip_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from sip_rest import sip_model_rest
    result = sip_model_rest.sip(chemical_name, bw_bird, bw_quail, bw_duck, bwb_other, bw_rat, bwm_other, b_species, m_species, bw_mamm, sol, ld50_a, ld50_m, aw_bird, mineau, aw_mamm, noaec, noael)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################sip#############################################

##################################stir#############################################
@route('/stir/<jid>', method='POST') 
@auth_basic(check)
def stir_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from stir_rest import stir_model_rest
    result = stir_model_rest.stir(run_type,chemical_name,application_rate,column_height,spray_drift_fraction,direct_spray_duration, 
                                  molecular_weight,vapor_pressure,avian_oral_ld50,body_weight_assessed_bird,body_weight_tested_bird,mineau_scaling_factor, 
                                  mammal_inhalation_lc50,duration_mammal_inhalation_study,body_weight_assessed_mammal,body_weight_tested_mammal, 
                                  mammal_oral_ld50)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################sip#############################################

##################################dust#############################################
@route('/dust/<jid>', method='POST') 
@auth_basic(check)
def dust_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from dust_rest import dust_model_rest
    result = dust_model_rest.dust(chemical_name, label_epa_reg_no, ar_lb, frac_pest_surface, dislodge_fol_res, bird_acute_oral_study, bird_study_add_comm,
                                  low_bird_acute_ld50, test_bird_bw, mineau_scaling_factor, mamm_acute_derm_study, mamm_study_add_comm, mam_acute_derm_ld50, mam_acute_oral_ld50, test_mam_bw)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################sip#############################################

##################################trex2#############################################
@route('/trex2/<jid>', method='POST') 
@auth_basic(check)
def trex2_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from trex2_rest import trex2_model_rest
    result = trex2_model_rest.trex2(chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, ar_lb, day_out,
                                    ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
                                    Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL, 
                                    tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
                                    m_s_r_p)
    if (result):
        result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result':result_json, '_id':jid}
##################################trex2#############################################

##################################therps#############################################
@route('/therps/<jid>', method='POST') 
@auth_basic(check)
def therps_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from therps_rest import therps_model_rest
    result = therps_model_rest.therps(chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50, avian_NOAEC, avian_NOAEL, 
                                      Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
                                      bw_avian_ld50, bw_avian_lc50, bw_avian_NOAEC, bw_avian_NOAEL,
                                      mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md, 
                                      wp_herp_a_lg, c_mamm_a, c_herp_a)
    if (result):
        result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result':result_json, '_id':jid}
##################################therps#############################################

##################################iec#############################################
@route('/iec/<jid>', method='POST') 
@auth_basic(check)
def iec_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from iec_rest import iec_model_rest
    result = iec_model_rest.iec(dose_response, LC50, threshold)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################iec#############################################

##################################agdrift#############################################
@route('/agdrift/<jid>', method='POST') 
@auth_basic(check)
def agdrift_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from agdrift_rest import agdrift_model_rest
    result = agdrift_model_rest.agdrift(drop_size, ecosystem_type, application_method, boom_height, orchard_type, application_rate, distance, aquatic_type, calculation_input, init_avg_dep_foa, avg_depo_gha, avg_depo_lbac, deposition_ngL, deposition_mgcm, nasae, y, x, express_y)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################agdrift#############################################















##################################earthworm#############################################
@route('/earthworm/<jid>', method='POST') 
@auth_basic(check)
def earthworm_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from earthworm_rest import earthworm_model_rest
    result = earthworm_model_rest.earthworm(k_ow, l_f_e, c_s, k_d, p_s, c_w, m_w, p_e)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################earthworm#############################################

##################################rice#############################################
@route('/rice/<jid>', method='POST') 
@auth_basic(check)
def rice_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from rice_rest import rice_model_rest
    result = rice_model_rest.rice(chemical_name, mai, dsed, a, pb, dw, osed, kd)
    if (result):
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result': result.__dict__, '_id':jid}
##################################rice#############################################

##################################kabam#############################################
@route('/kabam/<jid>', method='POST') 
@auth_basic(check)
def kabam_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from kabam_rest import kabam_model_rest
    result = kabam_model_rest.kabam(chemical_name, l_kow, k_oc, c_wdp, water_column_EEC, c_wto, mineau_scaling_factor, x_poc, x_doc, c_ox, w_t, c_ss, oc, k_ow, Species_of_the_tested_bird, bw_quail, bw_duck, bwb_other, avian_ld50, avian_lc50, avian_noaec, m_species, bw_rat, bwm_other, mammalian_ld50, mammalian_lc50, mammalian_chronic_endpoint, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton, lf_p_benthic_invertebrates, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_sediment, mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish, sf_p_sediment, sf_p_phytoplankton, sf_p_zooplankton, sf_p_benthic_invertebrates, sf_p_filter_feeders, ff_p_sediment, ff_p_phytoplankton, ff_p_zooplankton, ff_p_benthic_invertebrates, beninv_p_sediment, beninv_p_phytoplankton, beninv_p_zooplankton, zoo_p_sediment, zoo_p_phyto, s_lipid, s_NLOM, s_water, v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, wb_zoo, v_lb_zoo, v_nb_zoo, v_wb_zoo, wb_beninv, v_lb_beninv, v_nb_beninv, v_wb_beninv, wb_ff, v_lb_ff, v_nb_ff, v_wb_ff, wb_sf, v_lb_sf, v_nb_sf, v_wb_sf, wb_mf, v_lb_mf, v_nb_mf, v_wb_mf, wb_lf, v_lb_lf, v_nb_lf, v_wb_lf, kg_phytoplankton, kd_phytoplankton, ke_phytoplankton, mo_phytoplankton, mp_phytoplankton, km_phytoplankton, km_zoo, k1_phytoplankton, k2_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv, kd_beninv, ke_beninv, km_beninv, k1_ff, k2_ff, kd_ff, ke_ff, km_ff, k1_sf, k2_sf, kd_sf, ke_sf, km_sf, k1_mf, k2_mf, kd_mf, ke_mf, km_mf, k1_lf, k2_lf, kd_lf, ke_lf, km_lf, rate_constants, s_respire, phyto_respire, zoo_respire, beninv_respire, ff_respire, sfish_respire, mfish_respire, lfish_respire)
    if (result):
        result_json = json.dumps(result.__dict__, cls=NumPyArangeEncoder)
        all_result[jid]['status']='done'
        all_result[jid]['input']=request.json
        all_result[jid]['result']=result
    return {'user_id':'admin', 'result':result_json, '_id':jid}
##################################kabam#############################################



##################################geneec#############################################
@route('/geneec/<jid>', method='POST') 
@auth_basic(check)
def geneec_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')
    from geneec_rest import gfix
    # print request.json
    result = gfix.geneec2(APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,FOTHAP)

    # if (result):
    all_result[jid]['status']='done'
    all_result[jid]['input']=request.json
    all_result[jid]['result']=result

    return {'user_id':'admin', 'result': result, '_id':jid}
##################################geneec#############################################


##################################przm5#############################################
@route('/przm5/<jid>', method='POST') 
@auth_basic(check)
def przm5_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')

    from przm5_rest import PRZM5_pi_new
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
    # if (result):
    all_result[jid]['status']='done'
    all_result[jid]['input']=request.json
    all_result[jid]['result']=result

    # print request.json
    # print all_result
    # print list(ff)[0][0]

    return {'user_id':'admin', 'result': result, '_id':jid}

##################################przm5#############################################


################################# VVWM #############################################
@route('/vvwm/<jid>', method='POST') 
@auth_basic(check)
def vvwm_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')

    from vvwm_rest import VVWM_pi_new
    result = VVWM_pi_new.VVWM_pi(working_dir,
                                koc_check, Koc, soilHalfLifeBox, soilTempBox1, foliarHalfLifeBox,
                                wc_hl, w_temp, bm_hl, ben_temp, ap_hl, p_ref, h_hl, mwt, vp, sol, Q10Box,
                                convertSoil, convert_Foliar, convertWC, convertBen, convertAP, convertH,
                                deg_check, totalApp,
                                SpecifyYears, ApplicationTypes, PestAppyDay, PestAppyMon, appNumber_year, app_date_type, DepthIncorp, PestAppyRate, localEff, localSpray,
                                scenID,
                                buried, D_over_dx, PRBEN, benthic_depth, porosity, bulk_density, FROC2, DOC2, BNMAS,
                                DFAC, SUSED, CHL, FROC1, DOC1, PLMAS,
                                firstYear, lastyear, vvwmSimType,
                                afield, area, depth_0, depth_max,
                                ReservoirFlowAvgDays)

    all_result[jid]['status']='done'
    all_result[jid]['input']=request.json
    all_result[jid]['result']=result

    return {'user_id':'admin', 'result': result, '_id':jid}

################################# VVWM #############################################

##################################przm##############################################
@route('/przm/<jid>', method='POST') 
@auth_basic(check)

def przm_rest(jid):
    import time
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')

    from przm_rest import PRZM_pi_new
    result = PRZM_pi_new.PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)
    return {'user_id':'admin', 'result': result, '_id':jid}
    
##################################przm##############################################

# ##################################przm_batch##############################################
# result_all=[]
# @route('/przm_batch/<jid>', method='POST') 
# @auth_basic(check)
# def przm_rest(jid):
#     from przm_rest import PRZM_pi_new
#     for k, v in request.json.iteritems():
#         exec '%s = v' % k
#     zz=0
#     for przm_obs_temp in przm_objs:
#         print zz
#         # przm_obs_temp = przm_objs[index]
#         result_temp = PRZM_pi_new.PRZM_pi(przm_obs_temp['NOA'], przm_obs_temp['met_o'], przm_obs_temp['inp_o'], przm_obs_temp['run_o'], przm_obs_temp['MM'], przm_obs_temp['DD'], przm_obs_temp['YY'], przm_obs_temp['CAM_f'], przm_obs_temp['DEPI_text'], przm_obs_temp['Ar_text'], przm_obs_temp['EFF'], przm_obs_temp['Drft'])
#         result_all.append(result_temp)
#         zz=zz+1
#     # element = {"user_id":"admin", "_id":jid, "run_type":'batch', "output_html": 'output_html', "model_object_dict":result_all}
#     # print element
#     # from przm_rest import PRZM_batch_control
#     # result = PRZM_pi_new.PRZM_pi(noa, met, inp, run, MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft)

#     return {"user_id":"admin", "result": result_all, "_id":jid}
    
# ##################################przm_batch##############################################


##################################przm_batch##############################################
result_all=[]
@route('/przm_batch/<jid>', method='POST') 
@auth_basic(check)
def przm_rest(jid):
    from przm_rest import PRZM_pi_new
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    zz=0
    for przm_obs_temp in przm_objs:
        print zz
        # przm_obs_temp = przm_objs[index]
        result_temp = PRZM_pi_new.PRZM_pi(przm_obs_temp['NOA'], przm_obs_temp['met_o'], przm_obs_temp['inp_o'], przm_obs_temp['run_o'], przm_obs_temp['MM'], przm_obs_temp['DD'], przm_obs_temp['YY'], przm_obs_temp['CAM_f'], przm_obs_temp['DEPI_text'], przm_obs_temp['Ar_text'], przm_obs_temp['EFF'], przm_obs_temp['Drft'])
        przm_obs_temp['link'] = result_temp[0]
        przm_obs_temp['x_precip'] = [float(i) for i in result_temp[1]]
        przm_obs_temp['x_runoff'] = [float(i) for i in result_temp[2]]
        przm_obs_temp['x_et'] = [float(i) for i in result_temp[3]]
        przm_obs_temp['x_irr'] = [float(i) for i in result_temp[4]]
        przm_obs_temp['x_leachate'] = [float(i)/100000 for i in result_temp[5]]
        przm_obs_temp['x_pre_irr'] = [i+j for i,j in zip(przm_obs_temp['x_precip'], przm_obs_temp['x_irr'])]
        result_all.append(przm_obs_temp)
        zz=zz+1
    element={"user_id":"admin", "_id":jid, "run_type":'batch', "output_html": "", "model_object_dict":result_all}
    db['przm'].save(element)

    # return {"user_id":"admin", "result": result_all, "_id":jid}
    
##################################przm_batch##############################################


##################################exams##############################################
@route('/exams/<jid>', method='POST') 
@auth_basic(check)
def exams_rest(jid):
    import time
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    all_result.setdefault(jid,{}).setdefault('status','none')

    from exams_rest import exams_pi
    result = exams_pi.exams_pi(chem_name, scenarios, met, farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
    return {'user_id':'admin', 'result': result, '_id':jid}
    
##################################exams##############################################

##################################pfam##############################################
@route('/pfam/<jid>', method='POST') 
@auth_basic(check)

def pfam_rest(jid):
    import time
    for k, v in request.json.iteritems():
        exec '%s = v' % k
        # print k,'=',v
    # all_result.setdefault(jid,{}).setdefault('status','none')

    from pfam_rest import pfam_pi
    result = pfam_pi.pfam_pi(wat_hl,wat_t,ben_hl,ben_t,unf_hl,unf_t,aqu_hl,aqu_t,hyd_hl,mw,vp,sol,koc,hea_h,hea_r_t,
           noa,dd_out,mm_out,ma_out,sr_out,weather,wea_l,nof,date_f1,nod_out,fl_out,wl_out,ml_out,to_out,
           zero_height_ref,days_zero_full,days_zero_removal,max_frac_cov,mas_tras_cof,leak,ref_d,ben_d,
           ben_por,dry_bkd,foc_wat,foc_ben,ss,wat_c_doc,chl,dfac,q10,area_app)
    return {'user_id':'admin', 'result': result, '_id':jid}
    
##################################pfam##############################################

##################################przm_exams##############################################
@route('/przm_exams/<jid>', method='POST') 
@auth_basic(check)
def przm_exams_rest(jid):
    for k, v in request.json.iteritems():
        exec '%s = v' % k
        # print k, '=', v
    # all_result.setdefault(jid,{}).setdefault('status','none')

    from przm_exams_rest import PRZM_EXAMS_pi
    result = PRZM_EXAMS_pi.PRZM_EXAMS_pi(chem_name, noa, scenarios, unit, met, inp, run, exam, MM, DD, YY, CAM_f, DEPI, Ar, EFF, Drft, 
                                         farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)
    return {'user_id':'admin', 'result': result, '_id':jid}
##################################przm_exams##############################################

##################File upload####################
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
    print src1
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


##########insert results into mongodb#########################
@route('/save_history', method='POST') 
@auth_basic(check)
def insert_output_html():
    for k, v in request.json.iteritems():
        exec "%s = v" % k
    element={"user_id":"admin", "_id":_id, "run_type":run_type, "output_html": output_html, "model_object_dict":model_object_dict}
    db[model_name].save(element)
    print _id

@route('/update_html', method='POST') 
@auth_basic(check)
def update_output_html():
    for k, v in request.json.iteritems():
        exec "%s = v" % k
    # print request.json
    db[model_name].update({"_id" :_id}, {'$set': {"output_html": output_html}})




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
    # print entity
    if not entity:
        abort(404, 'No document with jid %s' % jid)
    return entity


@route('/user_history', method='POST')
@auth_basic(check)
def get_user_model_hist():
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    hist_all = []
    entity = db[model_name].find({'user_id':user_id}).sort("_id", 1)
    for i in entity:
        hist_all.append(i)
    if not entity:
        abort(404, 'No document with jid %s' % jid)
    return {"hist_all":hist_all}

@route('/get_html_output', method='POST')
@auth_basic(check)
def get_html_output():
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    html_output_c = db[model_name].find({"_id" :jid}, {"output_html":1, "_id":0})
    for i in html_output_c:
        # print i
        html_output = i['output_html']
    return {"html_output":html_output}

@route('/get_przm_batch_output', method='POST')
@auth_basic(check)
def get_przm_batch_output():
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    result_output_c = db[model_name].find({"_id" :jid}, {"model_object_dict":1, "_id":0})
    for i in result_output_c:
        # print i
        result = i['model_object_dict']
    return {"result":result}

@route('/get_pdf', method='POST')
@auth_basic(check)
def get_pdf():
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    final_str = pdf_t
    final_str = final_str + """<br>"""
    if (int(pdf_nop)>0):
        for i in range(int(pdf_nop)):
            final_str = final_str + """<img id="imgChart1" src="%s" />"""%(pdf_p[i])
            final_str = final_str + """<br>"""

    from generate_doc import generatepdf_pi
    result=generatepdf_pi.generatepdf_pi(final_str)
    return {"result":result}

@route('/get_html', method='POST')
@auth_basic(check)
def get_html():
    for k, v in request.json.iteritems():
        exec '%s = v' % k
    final_str = pdf_t
    final_str = final_str + """<br>"""
    if (int(pdf_nop)>0):
        for i in range(int(pdf_nop)):
            final_str = final_str + """<img id="imgChart1" src="%s" />"""%(pdf_p[i])
            final_str = final_str + """<br>"""

    from generate_doc import generatehtml_pi
    result=generatehtml_pi.generatehtml_pi(final_str)
    return {"result":result}

run(host='localhost', port=80, debug=True)

# run(host='localhost', port=7777, server='gevent', debug=True)




