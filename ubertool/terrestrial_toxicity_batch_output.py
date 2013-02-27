import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from ubertool import run_ubertool_db
from StringIO import StringIO
import cStringIO
import csv
import sys
sys.path.append("utils")
sys.path.append("./")
from CSVTestParamsLoader import CSVTestParamsLoader
from terrestrial_toxicity import TerrestrialToxicity

class TerrestrialToxicityBatchLoader:
    
    def batchLoadTerrestrialToxicityConfigs(self,params_matrix):
        params_matrix["TerrestrialToxicity"]=[]
        for terr_config_index in range(len(params_matrix.get('avian_ld50'))):
            terrestrial_toxicity_config_name = None
            if "terrestrial_toxicity_config_name" in params_matrix:
                terrestrial_toxicity_config_name = params_matrix.get("terrestrial_toxicity_config_name")[terr_config_index]
            avian_ld50 = None
            if "avian_ld50" in params_matrix:
                avian_ld50 = params_matrix.get("avian_ld50")[terr_config_index]            
            avian_lc50 = None
            if "avian_lc50" in params_matrix:
                avian_lc50 = params_matrix.get("avian_lc50")[terr_config_index]            
            avian_NOAEC = None
            if "avian_NOAEC" in params_matrix:
                avian_NOAEC = params_matrix.get("avian_NOAEC")[terr_config_index]            
            avian_NOAEL = None
            if "avian_NOAEL" in params_matrix:
                avian_NOAEL = params_matrix.get("avian_NOAEL")[terr_config_index]  
            body_weight_of_the_assessed_bird = None
            if "body_weight_of_the_assessed_bird" in params_matrix:
                body_weight_of_the_assessed_bird = params_matrix.get("body_weight_of_the_assessed_bird")[terr_config_index]  
            mineau_scaling_factor = None
            if "mineau_scaling_factor" in params_matrix:
                mineau_scaling_factor = params_matrix.get("mineau_scaling_factor")[terr_config_index]              
            mammalian_ld50 = None
            if "mammalian_ld50" in params_matrix:
                mammalian_ld50 = params_matrix.get("mammalian_ld50")[terr_config_index]
            mammalian_lc50 = None
            if "mammalian_lc50" in params_matrix:
                mammalian_lc50 = params_matrix.get("mammalian_lc50")[terr_config_index]            
            mammalian_inhalation_lc50 = None
            if "mammalian_inhalation_lc50" in params_matrix:
                mammalian_inhalation_lc50 = params_matrix.get("mammalian_inhalation_lc50")[terr_config_index]            
            duration_of_rat_study = None
            if "duration_of_rat_study" in params_matrix:
                duration_of_rat_study = params_matrix.get("duration_of_rat_study")[terr_config_index]            
            mammalian_NOAEC = None
            if "mammalian_NOAEC" in params_matrix:
                mammalian_NOAEC = params_matrix.get("mammalian_NOAEC")[terr_config_index]  
            mammalian_NOAEL = None
            if "mammalian_NOAEL" in params_matrix:
                mammalian_NOAEL = params_matrix.get("mammalian_NOAEL")[terr_config_index]  
            amphibian_bw = None
            if "amphibian_bw" in params_matrix:
                amphibian_bw = params_matrix.get("amphibian_bw")[terr_config_index]              
            terrestrial_phase_amphibian_ld50 = None
            if "terrestrial_phase_amphibian_ld50" in params_matrix:
                terrestrial_phase_amphibian_ld50 = params_matrix.get("terrestrial_phase_amphibian_ld50")[terr_config_index]
            terrestrial_phase_amphibian_lc50 = None
            if "terrestrial_phase_amphibian_lc50" in params_matrix:
                terrestrial_phase_amphibian_lc50 = params_matrix.get("terrestrial_phase_amphibian_lc50")[terr_config_index]            
            terrestrial_phase_amphibian_NOAEC = None
            if "terrestrial_phase_amphibian_NOAEC" in params_matrix:
                terrestrial_phase_amphibian_NOAEC = params_matrix.get("terrestrial_phase_amphibian_NOAEC")[terr_config_index]            
            terrestrial_phase_amphibian_NOAEL = None
            if "terrestrial_phase_amphibian_NOAEL" in params_matrix:
                terrestrial_phase_amphibian_NOAEL = params_matrix.get("terrestrial_phase_amphibian_NOAEL")[terr_config_index]            
            reptile_bw = None
            if "reptile_bw" in params_matrix:
                reptile_bw = params_matrix.get("reptile_bw")[terr_config_index]  
            terrestrial_phase_reptile_ld50 = None
            if "terrestrial_phase_reptile_ld50" in params_matrix:
                terrestrial_phase_reptile_ld50 = params_matrix.get("terrestrial_phase_reptile_ld50")[terr_config_index]  
            terrestrial_phase_reptile_lc50 = None
            if "terrestrial_phase_reptile_lc50" in params_matrix:
                terrestrial_phase_reptile_lc50 = params_matrix.get("terrestrial_phase_reptile_lc50")[terr_config_index]              
            terrestrial_phase_reptile_NOAEC = None
            if "terrestrial_phase_reptile_NOAEC" in params_matrix:
                terrestrial_phase_reptile_NOAEC = params_matrix.get("terrestrial_phase_reptile_NOAEC")[terr_config_index]
            terrestrial_phase_reptile_NOAEL = None
            if "terrestrial_phase_reptile_NOAEL" in params_matrix:
                terrestrial_phase_reptile_NOAEL = params_matrix.get("terrestrial_phase_reptile_NOAEL")[terr_config_index]            
            EC25_for_nonlisted_seedling_emergence_monocot = None
            if "EC25_for_nonlisted_seedling_emergence_monocot" in params_matrix:
                EC25_for_nonlisted_seedling_emergence_monocot = params_matrix.get("EC25_for_nonlisted_seedling_emergence_monocot")[terr_config_index]            
            EC25_for_nonlisted_seedling_emergence_dicot = None
            if "EC25_for_nonlisted_seedling_emergence_dicot" in params_matrix:
                EC25_for_nonlisted_seedling_emergence_dicot = params_matrix.get("EC25_for_nonlisted_seedling_emergence_dicot")[terr_config_index]            
            NOAEC_for_listed_seedling_emergence_monocot = None
            if "NOAEC_for_listed_seedling_emergence_monocot" in params_matrix:
                NOAEC_for_listed_seedling_emergence_monocot = params_matrix.get("NOAEC_for_listed_seedling_emergence_monocot")[terr_config_index]  
            NOAEC_for_listed_seedling_emergence_dicot = None
            if "NOAEC_for_listed_seedling_emergence_dicot" in params_matrix:
                NOAEC_for_listed_seedling_emergence_dicot = params_matrix.get("NOAEC_for_listed_seedling_emergence_dicot")[terr_config_index]  
            EC25_for_nonlisted_vegetative_vigor_monocot = None
            if "EC25_for_nonlisted_vegetative_vigor_monocot" in params_matrix:
                EC25_for_nonlisted_vegetative_vigor_monocot = params_matrix.get("EC25_for_nonlisted_vegetative_vigor_monocot")[terr_config_index]              
            EC25_for_nonlisted_vegetative_vigor_dicot = None
            if "EC25_for_nonlisted_vegetative_vigor_dicot" in params_matrix:
                EC25_for_nonlisted_vegetative_vigor_dicot = params_matrix.get("EC25_for_nonlisted_vegetative_vigor_dicot")[terr_config_index]
            NOAEC_for_listed_vegetative_vigor_monocot = None
            if "NOAEC_for_listed_vegetative_vigor_monocot" in params_matrix:
                NOAEC_for_listed_vegetative_vigor_monocot = params_matrix.get("NOAEC_for_listed_vegetative_vigor_monocot")[terr_config_index]            
            NOAEC_for_listed_vegetative_vigor_dicot = None
            if "NOAEC_for_listed_vegetative_vigor_dicot" in params_matrix:
                NOAEC_for_listed_vegetative_vigor_dicot = params_matrix.get("NOAEC_for_listed_vegetative_vigor_dicot")[terr_config_index]            
            Small_medium_and_large_BW_of_assessed_herptile_listed_species = None
            if "Small_medium_and_large_BW_of_assessed_herptile_listed_species" in params_matrix:
                Small_medium_and_large_BW_of_assessed_herptile_listed_species = params_matrix.get("Small_medium_and_large_BW_of_assessed_herptile_listed_species")[terr_config_index]            
            percent_water_content_of_small_med_large_herptile_species_diet = None
            if "percent_water_content_of_small_med_large_herptile_species_diet" in params_matrix:
                percent_water_content_of_small_med_large_herptile_species_diet = params_matrix.get("percent_water_content_of_small_med_large_herptile_species_diet")[terr_config_index]  
            taxonomic_group = None
            if "taxonomic_group" in params_matrix:
                taxonomic_group = params_matrix.get("taxonomic_group")[terr_config_index]  
            toxicity_target_concentration_for_nonlisted_vascular_plants = None
            if "eat_mammals" in params_matrix:
                eat_mammals = params_matrix.get("eat_mammals")[terr_config_index]              
            eat_amphibians_reptiles = None
            if "eat_amphibians_reptiles" in params_matrix:
                eat_amphibians_reptiles = params_matrix.get("eat_amphibians_reptiles")[terr_config_index]
            user = users.get_current_user()
            q = db.Query(TerrestrialToxicity)
            if user:
                q.filter('user =',user)
            if terrestrial_toxicity_config_name:
                q.filter("config_name =", terrestrial_toxicity_config_name)
            terr_tox = q.get()
            if terr_tox is None:
                terr_tox = TerrestrialToxicity()
            if user:
                terr_tox.user = user
            terr_tox.config_name = terrestrial_toxicity_config_name
            terr_tox.avian_ld50 = avian_ld50
            terr_tox.avian_lc50 = avian_lc50
            terr_tox.avian_NOAEC = avian_NOAEC
            terr_tox.avian_NOAEL = avian_NOAEL   
            terr_tox.body_weight_of_the_assessed_bird = body_weight_of_the_assessed_bird
            terr_tox.mineau_scaling_factor = mineau_scaling_factor
            terr_tox.mammalian_ld50 = mammalian_ld50
            terr_tox.mammalian_lc50 = mammalian_lc50
            terr_tox.mammalian_inhalation_lc50 = mammalian_inhalation_lc50
            terr_tox.duration_of_rat_study = duration_of_rat_study   
            terr_tox.mammalian_NOAEC = mammalian_NOAEC
            terr_tox.mammalian_NOAEL = mammalian_NOAEL
            terr_tox.amphibian_bw = amphibian_bw
            terr_tox.terrestrial_phase_amphibian_ld50 = terrestrial_phase_amphibian_ld50
            terr_tox.terrestrial_phase_amphibian_lc50 = terrestrial_phase_amphibian_lc50
            terr_tox.terrestrial_phase_amphibian_NOAEC = terrestrial_phase_amphibian_NOAEC   
            terr_tox.terrestrial_phase_amphibian_NOAEL = terrestrial_phase_amphibian_NOAEL
            terr_tox.reptile_bw = reptile_bw            
            terr_tox.terrestrial_phase_reptile_ld50 = terrestrial_phase_reptile_ld50
            terr_tox.terrestrial_phase_reptile_lc50 = terrestrial_phase_reptile_lc50
            terr_tox.terrestrial_phase_reptile_NOAEC = terrestrial_phase_reptile_NOAEC
            terr_tox.terrestrial_phase_reptile_NOAEL = terrestrial_phase_reptile_NOAEL   
            terr_tox.EC25_for_nonlisted_seedling_emergence_monocot = EC25_for_nonlisted_seedling_emergence_monocot
            terr_tox.EC25_for_nonlisted_seedling_emergence_dicot = EC25_for_nonlisted_seedling_emergence_dicot            
            terr_tox.NOAEC_for_listed_seedling_emergence_monocot = NOAEC_for_listed_seedling_emergence_monocot
            terr_tox.NOAEC_for_listed_seedling_emergence_dicot = NOAEC_for_listed_seedling_emergence_dicot
            terr_tox.EC25_for_nonlisted_vegetative_vigor_monocot = EC25_for_nonlisted_vegetative_vigor_monocot
            terr_tox.EC25_for_nonlisted_vegetative_vigor_dicot = EC25_for_nonlisted_vegetative_vigor_dicot   
            terr_tox.NOAEC_for_listed_vegetative_vigor_monocot = NOAEC_for_listed_vegetative_vigor_dicot
            terr_tox.Small_medium_and_large_BW_of_assessed_herptile_listed_species = Small_medium_and_large_BW_of_assessed_herptile_listed_species
            terr_tox.percent_water_content_of_small_med_large_herptile_species_diet = percent_water_content_of_small_med_large_herptile_species_diet            
            terr_tox.taxonomic_group = taxonomic_group
            terr_tox.eat_mammals = eat_mammals
            terr_tox.eat_amphibians_reptiles = eat_amphibians_reptiles
            terr_tox.put()
            params_matrix["TerrestrialToxicity"].append(terr_tox)
        return params_matrix
                
                      