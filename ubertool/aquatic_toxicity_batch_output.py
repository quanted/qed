import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import urllib
from google.appengine.api import urlfetch
import logging
from django.utils import simplejson

logger = logging.getLogger("AquaToxicityBatchOutput")

ubertool_config_service_base_url = os.environ['UBERTOOL_MONGO_SERVER']

def batchLoadAquaticToxicityConfigs(params_matrix,config_index,ubertool_configuration_properties):
    config_params = {}
    config_name = None
    logger.info("Config Index: %d Type: %s" %(config_index,type(config_index)))
    logger.info("params_matrix:")
    logger.info(params_matrix)
    config_name = params_matrix.get("aquatic_toxicity_config_name")[config_index]
    config_params['acute_toxicity_target_concentration_for_freshwater_fish'] = params_matrix.get("acute_toxicity_target_concentration_for_freshwater_fish")[config_index]            
    config_params['duckweed'] = params_matrix.get("duckweed")[config_index]
    config_params['mai'] = params_matrix.get("mai")[config_index]
    config_params['a'] = params_matrix.get("a")[config_index]
    config_params['dsed'] = params_matrix.get("dsed")[config_index]
    config_params['pb'] = params_matrix.get("pb")[config_index]
    config_params['dw'] = params_matrix.get("dw")[config_index]
    config_params['osed'] = params_matrix.get("osed")[config_index]
    config_params['kd'] = params_matrix.get("kd")[config_index]
    config_params['msed'] = params_matrix.get("msed")[config_index]
    config_params['vw'] = params_matrix.get("vw")[config_index]
    config_params['mai1'] = params_matrix.get("mai1")[config_index]
    config_params['cw'] = params_matrix.get("cw")[config_index]
    config_params['lf_p_sediment'] = params_matrix.get("lf_p_sediment")[config_index]
    config_params['lf_p_phytoplankton'] = params_matrix.get("lf_p_phytoplankton")[config_index]
    config_params['lf_p_zooplankton'] = params_matrix.get("lf_p_zooplankton")[config_index]
    config_params['lf_p_benthic_invertebrates'] = params_matrix.get("lf_p_benthic_invertebrates")[config_index]
    config_params['lf_p_filter_feeders'] = params_matrix.get("lf_p_filter_feeders")[config_index]
    config_params['lf_p_small_fish'] = params_matrix.get("lf_p_small_fish")[config_index]
    config_params['lf_p_medium_fish'] = params_matrix.get("lf_p_medium_fish")[config_index]
    config_params['mf_p_sediment'] = params_matrix.get("mf_p_sediment")[config_index]
    config_params['mf_p_phytoplankton'] = params_matrix.get("mf_p_phytoplankton")[config_index]
    config_params['mf_p_zooplankton'] = params_matrix.get("mf_p_zooplankton")[config_index]
    config_params['mf_p_benthic_invertebrates'] = params_matrix.get("mf_p_benthic_invertebrates")[config_index]
    config_params['mf_p_filter_feeders'] = params_matrix.get("mf_p_filter_feeders")[config_index]
    config_params['mf_p_small_fish'] = params_matrix.get("mf_p_small_fish")[config_index]
    config_params['sf_p_sediment'] = params_matrix.get("sf_p_sediment")[config_index]
    config_params['sf_p_phytoplankton'] = params_matrix.get("sf_p_phytoplankton")[config_index]
    config_params['sf_p_zooplankton'] = params_matrix.get("sf_p_zooplankton")[config_index]
    config_params['sf_p_benthic_invertebrates'] = params_matrix.get("sf_p_benthic_invertebrates")[config_index]
    config_params['sf_p_filter_feeders'] = params_matrix.get("sf_p_filter_feeders")[config_index]
    config_params['ff_p_sediment'] = params_matrix.get("ff_p_sediment")[config_index]
    config_params['ff_p_phytoplankton'] = params_matrix.get("ff_p_phytoplankton")[config_index]
    config_params['ff_p_zooplankton'] = params_matrix.get("ff_p_zooplankton")[config_index]
    config_params['ff_p_benthic_invertebrates'] = params_matrix.get("ff_p_benthic_invertebrates")[config_index]
    config_params['beninv_p_sediment'] = params_matrix.get("beninv_p_sediment")[config_index]
    config_params['beninv_p_phytoplankton'] = params_matrix.get("beninv_p_phytoplankton")[config_index]
    config_params['beninv_p_zooplankton'] = params_matrix.get("beninv_p_zooplankton")[config_index]
    config_params['zoo_p_sediment'] = params_matrix.get("zoo_p_sediment")[config_index]
    config_params['zoo_p_phytoplankton'] = params_matrix.get("zoo_p_phytoplankton")[config_index]
    config_params['s_lipid'] = params_matrix.get("s_lipid")[config_index]
    config_params['s_NLOM'] = params_matrix.get("s_NLOM")[config_index]
    config_params['s_water'] = params_matrix.get("s_water")[config_index]
    config_params['v_lb_phytoplankton'] = params_matrix.get("v_lb_phytoplankton")[config_index]
    config_params['v_nb_phytoplankton'] = params_matrix.get("v_nb_phytoplankton")[config_index]
    config_params['v_wb_phytoplankton'] = params_matrix.get("v_wb_phytoplankton")[config_index]
    config_params['v_lb_zoo'] = params_matrix.get("v_lb_zoo")[config_index]
    config_params['v_nb_zoo'] = params_matrix.get("v_nb_zoo")[config_index]
    config_params['v_wb_zoo'] = params_matrix.get("v_wb_zoo")[config_index]
    config_params['v_lb_beninv'] = params_matrix.get("v_lb_beninv")[config_index]
    config_params['v_nb_beninv'] = params_matrix.get("v_nb_beninv")[config_index]
    config_params['v_wb_beninv'] = params_matrix.get("v_wb_beninv")[config_index]
    config_params['v_lb_ff'] = params_matrix.get("v_lb_ff")[config_index]
    config_params['v_nb_ff'] = params_matrix.get("v_nb_ff")[config_index]
    config_params['v_wb_ff'] = params_matrix.get("v_wb_ff")[config_index]
    config_params['v_lb_sf'] = params_matrix.get("v_lb_sf")[config_index]
    config_params['v_nb_sf'] = params_matrix.get("v_nb_sf")[config_index]
    config_params['v_wb_sf'] = params_matrix.get("v_wb_sf")[config_index]
    config_params['v_lb_mf'] = params_matrix.get("v_lb_mf")[config_index]
    config_params['v_nb_mf'] = params_matrix.get("v_nb_mf")[config_index]
    config_params['v_wb_mf'] = params_matrix.get("v_wb_mf")[config_index]
    config_params['v_lb_lf'] = params_matrix.get("v_lb_lf")[config_index]
    config_params['v_nb_lf'] = params_matrix.get("v_nb_lf")[config_index]
    config_params['v_wb_lf'] = params_matrix.get("v_wb_lf")[config_index]
    config_params['k1_phytoplankton'] = params_matrix.get("k1_phytoplankton")[config_index]
    config_params['k2_phytoplankton'] = params_matrix.get("k2_phytoplankton")[config_index]
    config_params['ke_phytoplankton'] = params_matrix.get("ke_phytoplankton")[config_index]
    config_params['kd_phytoplankton'] = params_matrix.get("kd_phytoplankton")[config_index]
    config_params['km_phytoplankton'] = params_matrix.get("km_phytoplankton")[config_index]
    config_params['k1_zoo'] = params_matrix.get("k1_zoo")[config_index]
    config_params['k2_zoo'] = params_matrix.get("k2_zoo")[config_index]
    config_params['ke_zoo'] = params_matrix.get("ke_zoo")[config_index]
    config_params['kd_zoo'] = params_matrix.get("kd_zoo")[config_index]
    config_params['km_zoo'] = params_matrix.get("km_zoo")[config_index]
    config_params['k1_beninv'] = params_matrix.get("k1_beninv")[config_index]
    config_params['k2_beninv'] = params_matrix.get("k2_beninv")[config_index]
    config_params['ke_beninv'] = params_matrix.get("ke_beninv")[config_index]
    config_params['kd_beninv'] = params_matrix.get("kd_beninv")[config_index]
    config_params['km_beninv'] = params_matrix.get("km_beninv")[config_index]
    config_params['k1_ff'] = params_matrix.get("k1_ff")[config_index]
    config_params['k2_ff'] = params_matrix.get("k2_ff")[config_index]
    config_params['ke_ff'] = params_matrix.get("ke_ff")[config_index]
    config_params['kd_ff'] = params_matrix.get("kd_ff")[config_index]
    config_params['km_ff'] = params_matrix.get("km_ff")[config_index]
    config_params['k1_sf'] = params_matrix.get("k1_sf")[config_index]
    config_params['k2_sf'] = params_matrix.get("k2_sf")[config_index]
    config_params['ke_sf'] = params_matrix.get("ke_sf")[config_index]
    config_params['kd_sf'] = params_matrix.get("kd_sf")[config_index]
    config_params['km_sf'] = params_matrix.get("km_sf")[config_index]
    config_params['k1_mf'] = params_matrix.get("k1_mf")[config_index]
    config_params['k2_mf'] = params_matrix.get("k2_mf")[config_index]
    config_params['ke_mf'] = params_matrix.get("ke_mf")[config_index]
    config_params['kd_mf'] = params_matrix.get("kd_mf")[config_index]
    config_params['km_mf'] = params_matrix.get("km_mf")[config_index]
    config_params['k1_lf'] = params_matrix.get("k1_lf")[config_index]
    config_params['k2_lf'] = params_matrix.get("k2_lf")[config_index]
    config_params['ke_lf'] = params_matrix.get("ke_lf")[config_index]
    config_params['kd_lf'] = params_matrix.get("kd_lf")[config_index]
    config_params['km_lf'] = params_matrix.get("km_lf")[config_index]
    config_params['s_respire'] = params_matrix.get("s_respire")[config_index]
    config_params['phyto_respire'] = params_matrix.get("phyto_respire")[config_index]
    config_params['zoo_respire'] = params_matrix.get("zoo_respire")[config_index]
    config_params['beninv_respire'] = params_matrix.get("beninv_respire")[config_index]
    config_params['ff_respire'] = params_matrix.get("ff_respire")[config_index]
    config_params['sfish_respire'] = params_matrix.get("sfish_respire")[config_index]
    config_params['mfish_respire'] = params_matrix.get("mfish_respire")[config_index]
    config_params['lfish_respire'] = params_matrix.get("lfish_respire")[config_index]
    config_params['kg_phytoplankton'] = params_matrix.get("kg_phytoplankton")[config_index]
    config_params['mp_phytoplankton'] = params_matrix.get("mp_phytoplankton")[config_index]
    config_params['mo_phytoplankton'] = params_matrix.get("mo_phytoplankton")[config_index]
>>>>>>> chance
    config_params['aquatic_configuration'] = config_name
    ubertool_configuration_properties.update(config_params)
    config_params['config_name'] = config_name
    logger.info("config_params:")
    logger.info(config_params)
    form_data = simplejson.dumps(config_params)
    url = ubertool_config_service_base_url+"/ubertool/aqua/"+config_name
    result = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
    return ubertool_configuration_properties