# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:55:40 2012

@author: jharston
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
import sys
sys.path.append('../CAS')
from CAS.CASGql import CASGql
from google.appengine.api import users
from google.appengine.ext import db
from use import Use
from pesticide_properties import PesticideProperties
from exposure_concentrations import ExposureConcentrations
from aquatic_toxicity import AquaticToxicity
from terrestrial_toxicity import TerrestrialToxicity
from ecosystem_inputs import EcosystemInputs
import logging


class RunUbertoolInp(forms.Form):
    logger = logging.getLogger("RunUbertoolInp")
    user = users.get_current_user()
    user_id = user.user_id()
    config_name = forms.CharField(label="Ubertool Configuration Name", initial="ubertool-config-%s"%user_id)
    q = db.Query(Use)
    q.filter('user =',user)
    uses = ()
#    uses += ((None,None),)
    for use in q:
        #logger.info(use.to_xml())
        uses += ((use.config_name,use.config_name),)
    use_configuration = forms.ChoiceField(required=True, choices=uses)
    q = db.Query(PesticideProperties)
    q.filter('user =',user)
    pests = ()
#    pests += ((None,None),)    
    for pest in q:
        #logger.info(use.to_xml())
        pests += ((pest.config_name,pest.config_name),)
    pest_configuration = forms.ChoiceField(required=True, choices=pests)
    q = db.Query(ExposureConcentrations)
    q.filter('user =',user)
    exposures = ()
#    exposures += ((None,None),)
    for exposure in q:
        #logger.info(use.to_xml())
        exposures += ((exposure.config_name,exposure.config_name),)
    exposures_configuration = forms.ChoiceField(required=True, choices=exposures)
    q = db.Query(AquaticToxicity)
    q.filter('user =',user)
    aquatics = ()
#    aquatics += ((None,None),)
    for aquatic in q:
        #logger.info(use.to_xml())
        aquatics += ((aquatic.config_name,aquatic.config_name),)
    aquatic_configuration = forms.ChoiceField(required=True, choices=aquatics)
    q = db.Query(TerrestrialToxicity)
    q.filter('user =',user)
    terrestrials = ()
#    terrestrials += ((None,None),)
    for terrestrial in q:
        #logger.info(use.to_xml())
        terrestrials += ((terrestrial.config_name,terrestrial.config_name),)
    terrestrial_configuration = forms.ChoiceField(required=True, choices=terrestrials)
    q = db.Query(EcosystemInputs)
    q.filter('user =',user)
    ecosystems = ()
#    ecosystems += ((None,None),)
    for ecosystem in q:
        #logger.info(use.to_xml())
        ecosystems += ((ecosystem.config_name,ecosystem.config_name),)
    ecosystems_configuration = forms.ChoiceField(required=True, choices=ecosystems)