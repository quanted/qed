# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:34:41 2012

@author: msnyde02
"""
# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
import logging
import sys
import rest_funcs
import json
logger = logging.getLogger('Kabam Model')
import os
import keys_Picloud_S3
import base64
import urllib
from google.appengine.api import urlfetch


# Daily water intake rate for birds

############Provide the key and connect to EC2####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string, 'Content-Type' : 'application/json'}
url_part1 = os.environ['UBERTOOL_REST_SERVER']
###########################################################################

class kabam(object):
    def __init__(self, set_variables=True,run_methods=True, run_type='single',
            chemical_name='',l_kow=1,k_oc=1,c_wdp=1,water_column_EEC=1,c_wto=1,mineau_scaling_factor=1,x_poc=1,x_doc=1,c_ox=1,w_t=1,c_ss=1,oc=1,k_ow=1,
            Species_of_the_tested_bird='',bw_quail=1,bw_duck=1,bwb_other=1,avian_ld50=1,avian_lc50=1,avian_noaec=1,m_species='',bw_rat=1,bwm_other=1,mammalian_ld50=1,mammalian_lc50=1,mammalian_chronic_endpoint=1,
            lf_p_sediment=1,lf_p_phytoplankton=1,lf_p_zooplankton=1,lf_p_benthic_invertebrates=1,lf_p_filter_feeders=1,lf_p_small_fish=1,lf_p_medium_fish=1,
            mf_p_sediment=1,mf_p_phytoplankton=1,mf_p_zooplankton=1,mf_p_benthic_invertebrates=1,mf_p_filter_feeders=1,mf_p_small_fish=1,
            sf_p_sediment=1,sf_p_phytoplankton=1,sf_p_zooplankton=1,sf_p_benthic_invertebrates=1,sf_p_filter_feeders=1,
            ff_p_sediment=1,ff_p_phytoplankton=1,ff_p_zooplankton=1,ff_p_benthic_invertebrates=1,
            beninv_p_sediment=1,beninv_p_phytoplankton=1,beninv_p_zooplankton=1,
            zoo_p_sediment=1,zoo_p_phyto=1,
            s_lipid=1,s_NLOM=1,s_water=1,
            v_lb_phytoplankton=1,v_nb_phytoplankton=1,v_wb_phytoplankton=1,wb_zoo=1,v_lb_zoo=1,v_nb_zoo=1,v_wb_zoo=1,wb_beninv=1,v_lb_beninv=1,v_nb_beninv=1,v_wb_beninv=1,wb_ff=1,v_lb_ff=1,v_nb_ff=1,v_wb_ff=1,wb_sf=1,v_lb_sf=1,v_nb_sf=1,v_wb_sf=1,wb_mf=1,v_lb_mf=1,v_nb_mf=1,v_wb_mf=1,wb_lf=1,v_lb_lf=1,v_nb_lf=1,v_wb_lf=1,
            kg_phytoplankton=1,kd_phytoplankton=1,ke_phytoplankton=1,mo_phytoplankton=1,mp_phytoplankton=1,km_phytoplankton=1,km_zoo=1,
            k1_phytoplankton=1,k2_phytoplankton=1,
            k1_zoo=1,k2_zoo=1,kd_zoo=1,ke_zoo=1,k1_beninv=1,k2_beninv=1,kd_beninv=1,ke_beninv=1,km_beninv=1,
            k1_ff=1,k2_ff=1,kd_ff=1,ke_ff=1,km_ff=1,k1_sf=1,k2_sf=1,kd_sf=1,ke_sf=1,km_sf=1,k1_mf=1,k2_mf=1,kd_mf=1,ke_mf=1,km_mf=1,k1_lf=1,k2_lf=1,kd_lf=1,ke_lf=1,km_lf=1,
            rate_constants='',s_respire='',phyto_respire='',zoo_respire='',beninv_respire='',ff_respire='',sfish_respire='',mfish_respire='',lfish_respire='',
            vars_dict=None):

            # cb_phytoplankton_v=1,cb_zoo_v=1,cb_beninv_v=1,cb_ff_v=1,cb_sf_v=1,cb_mf_v=1,cb_lf_v=1,   ***These were removed from __init__***

        # self.set_default_variables()
        self.jid = rest_funcs.gen_jid()
        
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.run_type = run_type
                self.chemical_name = chemical_name
                self.l_kow=l_kow
                self.k_oc=k_oc
                self.c_wdp=c_wdp
                self.water_column_EEC=water_column_EEC
                self.c_wto=c_wto
                self.mineau_scaling_factor=mineau_scaling_factor
                self.x_poc=x_poc
                self.x_doc=x_doc
                self.c_ox=c_ox
                self.w_t=w_t
                self.c_ss=c_ss
                self.oc=oc
                self.k_ow=k_ow
                self.Species_of_the_tested_bird = Species_of_the_tested_bird
                self.bw_quail = bw_quail
                self.bw_duck = bw_duck
                self.bwb_other = bwb_other
                if Species_of_the_tested_bird =='178':
                    self.bw_bird = self.bw_quail
                elif Species_of_the_tested_bird =='1580':
                    self.bw_bird = self.bw_duck
                else:
                    self.bw_bird = self.bwb_other           
                self.avian_ld50=avian_ld50
                self.avian_lc50=avian_lc50
                self.avian_noaec=avian_noaec
                self.m_species = m_species
                self.bw_rat = bw_rat
                self.bwm_other = bwm_other
                if m_species =='350':
                    self.bw_mamm = self.bw_rat
                else:
                    self.bw_mamm = self.bwm_other
                self.mammalian_ld50=mammalian_ld50
                self.mammalian_lc50=mammalian_lc50
                self.mammalian_chronic_endpoint=mammalian_chronic_endpoint
                self.lf_p_sediment=lf_p_sediment
                self.lf_p_phytoplankton=lf_p_phytoplankton
                self.lf_p_zooplankton=lf_p_zooplankton
                self.lf_p_benthic_invertebrates=lf_p_benthic_invertebrates
                self.lf_p_filter_feeders=lf_p_filter_feeders
                self.lf_p_small_fish=lf_p_small_fish
                self.lf_p_medium_fish=lf_p_medium_fish
                self.mf_p_sediment=mf_p_sediment
                self.mf_p_phytoplankton=mf_p_phytoplankton
                self.mf_p_zooplankton=mf_p_zooplankton
                self.mf_p_benthic_invertebrates=mf_p_benthic_invertebrates
                self.mf_p_filter_feeders=mf_p_filter_feeders
                self.mf_p_small_fish=mf_p_small_fish
                self.sf_p_sediment=sf_p_sediment
                self.sf_p_phytoplankton=sf_p_phytoplankton
                self.sf_p_zooplankton=sf_p_zooplankton
                self.sf_p_benthic_invertebrates=sf_p_benthic_invertebrates
                self.sf_p_filter_feeders=sf_p_filter_feeders
                self.ff_p_sediment=ff_p_sediment
                self.ff_p_phytoplankton=ff_p_phytoplankton
                self.ff_p_zooplankton=ff_p_zooplankton
                self.ff_p_benthic_invertebrates=ff_p_benthic_invertebrates
                self.beninv_p_sediment=beninv_p_sediment
                self.beninv_p_phytoplankton=beninv_p_phytoplankton
                self.beninv_p_zooplankton=beninv_p_zooplankton
                self.zoo_p_sediment=zoo_p_sediment
                self.zoo_p_phyto=zoo_p_phyto
                self.s_lipid=s_lipid
                self.s_NLOM=s_NLOM
                self.s_water=s_water
                self.v_lb_phytoplankton=v_lb_phytoplankton
                self.v_nb_phytoplankton=v_nb_phytoplankton
                self.v_wb_phytoplankton=v_wb_phytoplankton
                self.wb_zoo=wb_zoo
                self.v_lb_zoo=v_lb_zoo
                self.v_nb_zoo=v_nb_zoo
                self.v_wb_zoo=v_wb_zoo
                self.wb_beninv=wb_beninv
                self.v_lb_beninv=v_lb_beninv
                self.v_nb_beninv=v_nb_beninv
                self.v_wb_beninv=v_wb_beninv
                self.wb_ff=wb_ff
                self.v_lb_ff=v_lb_ff
                self.v_nb_ff=v_nb_ff
                self.v_wb_ff=v_wb_ff
                self.wb_sf=wb_sf
                self.v_lb_sf=v_lb_sf
                self.v_nb_sf=v_nb_sf
                self.v_wb_sf=v_wb_sf
                self.wb_mf=wb_mf
                self.v_lb_mf=v_lb_mf
                self.v_nb_mf=v_nb_mf
                self.v_wb_mf=v_wb_mf
                self.wb_lf=wb_lf
                self.v_lb_lf=v_lb_lf
                self.v_nb_lf=v_nb_lf
                self.v_wb_lf=v_wb_lf
                self.kg_phytoplankton=kg_phytoplankton
                self.kd_phytoplankton=kd_phytoplankton
                self.ke_phytoplankton=ke_phytoplankton
                self.mo_phytoplankton=mo_phytoplankton
                self.mp_phytoplankton=mp_phytoplankton
                self.km_phytoplankton=km_phytoplankton
                self.km_zoo=km_zoo
                self.k1_phytoplankton=k1_phytoplankton
                self.k2_phytoplankton=k2_phytoplankton
                self.k1_zoo=k1_zoo
                self.k2_zoo=k2_zoo
                self.kd_zoo=kd_zoo
                self.ke_zoo=ke_zoo
                self.k1_beninv=k1_beninv
                self.k2_beninv=k2_beninv
                self.kd_beninv=kd_beninv
                self.ke_beninv=ke_beninv
                self.km_beninv=km_beninv
                self.k1_ff=k1_ff
                self.k2_ff=k2_ff
                self.kd_ff=kd_ff
                self.ke_ff=ke_ff
                self.km_ff=km_ff
                self.k1_sf=k1_sf
                self.k2_sf=k2_sf
                self.kd_sf=kd_sf
                self.ke_sf=ke_sf
                self.km_sf=km_sf
                self.k1_mf=k1_mf
                self.k2_mf=k2_mf
                self.kd_mf=kd_mf
                self.ke_mf=ke_mf
                self.km_mf=km_mf
                self.k1_lf=k1_lf
                self.k2_lf=k2_lf
                self.kd_lf=kd_lf
                self.ke_lf=ke_lf
                self.km_lf=km_lf
                # self.k_bw_phytoplankton=k_bw_phytoplankton
                # self.k_bw_zoo=k_bw_zoo
                # self.k_bw_beninv=k_bw_beninv
                # self.k_bw_ff=k_bw_ff
                # self.k_bw_sf=k_bw_sf
                # self.k_bw_mf=k_bw_mf
                # self.k_bw_lf=k_bw_lf
                self.rate_constants=rate_constants
                self.s_respire=s_respire
                self.phyto_respire=phyto_respire
                self.zoo_respire=zoo_respire
                self.beninv_respire=beninv_respire
                self.ff_respire=ff_respire
                self.sfish_respire=sfish_respire
                self.mfish_respire=mfish_respire
                self.lfish_respire=lfish_respire

                all_dic = {"chemical_name":chemical_name, "l_kow":l_kow, "k_oc":k_oc, "c_wdp":c_wdp, "water_column_EEC":water_column_EEC, "c_wto":c_wto, "mineau_scaling_factor":mineau_scaling_factor, "x_poc":x_poc, "x_doc":x_doc, "c_ox":c_ox, "w_t":w_t, "c_ss":c_ss, "oc":oc, "k_ow":k_ow, "Species_of_the_tested_bird":Species_of_the_tested_bird, "bw_quail":bw_quail, "bw_duck":bw_duck, "bwb_other":bwb_other, "avian_ld50":avian_ld50, "avian_lc50":avian_lc50, "avian_noaec":avian_noaec, "m_species":m_species, "bw_rat":bw_rat, "bwm_other":bwm_other, "mammalian_ld50":mammalian_ld50, "mammalian_lc50":mammalian_lc50, "mammalian_chronic_endpoint":mammalian_chronic_endpoint, "lf_p_sediment":lf_p_sediment, "lf_p_phytoplankton":lf_p_phytoplankton, "lf_p_zooplankton":lf_p_zooplankton, "lf_p_benthic_invertebrates":lf_p_benthic_invertebrates, "lf_p_filter_feeders":lf_p_filter_feeders, "lf_p_small_fish":lf_p_small_fish, "lf_p_medium_fish":lf_p_medium_fish, "mf_p_sediment":mf_p_sediment, "mf_p_phytoplankton":mf_p_phytoplankton, "mf_p_zooplankton":mf_p_zooplankton, "mf_p_benthic_invertebrates":mf_p_benthic_invertebrates, "mf_p_filter_feeders":mf_p_filter_feeders, "mf_p_small_fish":mf_p_small_fish, "sf_p_sediment":sf_p_sediment, "sf_p_phytoplankton":sf_p_phytoplankton, "sf_p_zooplankton":sf_p_zooplankton, "sf_p_benthic_invertebrates":sf_p_benthic_invertebrates, "sf_p_filter_feeders":sf_p_filter_feeders, "ff_p_sediment":ff_p_sediment, "ff_p_phytoplankton":ff_p_phytoplankton, "ff_p_zooplankton":ff_p_zooplankton, "ff_p_benthic_invertebrates":ff_p_benthic_invertebrates, "beninv_p_sediment":beninv_p_sediment, "beninv_p_phytoplankton":beninv_p_phytoplankton, "beninv_p_zooplankton":beninv_p_zooplankton, "zoo_p_sediment":zoo_p_sediment, "zoo_p_phyto":zoo_p_phyto, "s_lipid":s_lipid, "s_NLOM":s_NLOM, "s_water":s_water, "v_lb_phytoplankton":v_lb_phytoplankton, "v_nb_phytoplankton":v_nb_phytoplankton, "v_wb_phytoplankton":v_wb_phytoplankton, "wb_zoo":wb_zoo, "v_lb_zoo":v_lb_zoo, "v_nb_zoo":v_nb_zoo, "v_wb_zoo":v_wb_zoo, "wb_beninv":wb_beninv, "v_lb_beninv":v_lb_beninv, "v_nb_beninv":v_nb_beninv, "v_wb_beninv":v_wb_beninv, "wb_ff":wb_ff, "v_lb_ff":v_lb_ff, "v_nb_ff":v_nb_ff, "v_wb_ff":v_wb_ff, "wb_sf":wb_sf, "v_lb_sf":v_lb_sf, "v_nb_sf":v_nb_sf, "v_wb_sf":v_wb_sf, "wb_mf":wb_mf, "v_lb_mf":v_lb_mf, "v_nb_mf":v_nb_mf, "v_wb_mf":v_wb_mf, "wb_lf":wb_lf, "v_lb_lf":v_lb_lf, "v_nb_lf":v_nb_lf, "v_wb_lf":v_wb_lf, "kg_phytoplankton":kg_phytoplankton, "kd_phytoplankton":kd_phytoplankton, "ke_phytoplankton":ke_phytoplankton, "mo_phytoplankton":mo_phytoplankton, "mp_phytoplankton":mp_phytoplankton, "km_phytoplankton":km_phytoplankton, "km_zoo":km_zoo, "k1_phytoplankton":k1_phytoplankton, "k2_phytoplankton":k2_phytoplankton, "k1_zoo":k1_zoo, "k2_zoo":k2_zoo, "kd_zoo":kd_zoo, "ke_zoo":ke_zoo, "k1_beninv":k1_beninv, "k2_beninv":k2_beninv, "kd_beninv":kd_beninv, "ke_beninv":ke_beninv, "km_beninv":km_beninv, "k1_ff":k1_ff, "k2_ff":k2_ff, "kd_ff":kd_ff, "ke_ff":ke_ff, "km_ff":km_ff, "k1_sf":k1_sf, "k2_sf":k2_sf, "kd_sf":kd_sf, "ke_sf":ke_sf, "km_sf":km_sf, "k1_mf":k1_mf, "k2_mf":k2_mf, "kd_mf":kd_mf, "ke_mf":ke_mf, "km_mf":km_mf, "k1_lf":k1_lf, "k2_lf":k2_lf, "kd_lf":kd_lf, "ke_lf":ke_lf, "km_lf":km_lf, "rate_constants":rate_constants, "s_respire":s_respire, "phyto_respire":phyto_respire, "zoo_respire":zoo_respire, "beninv_respire":beninv_respire, "ff_respire":ff_respire, "sfish_respire":sfish_respire, "mfish_respire":mfish_respire, "lfish_respire":lfish_respire}
                data = json.dumps(all_dic)

                self.jid = rest_funcs.gen_jid()
                url=os.environ['UBERTOOL_REST_SERVER'] + '/kabam/' + self.jid 
                response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers, deadline=60)   
                output_val = json.loads(response.content, cls=rest_funcs.NumPyDecoder)['result']
                output_val_uni=json.loads(output_val, cls=rest_funcs.NumPyDecoder)
                for key, value in output_val_uni.items():
                    setattr(self, key, value)



