# -*- coding: utf-8 -*-
"""
@author: 
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from google.appengine.api import users
from google.appengine.ext import db
import sys
sys.path.append("../ubertool")
from ubertool.use import Use
from ubertool.pesticide_properties import PesticideProperties
from ubertool.exposure_concentrations import ExposureConcentrations
from ubertool.aquatic_toxicity import AquaticToxicity
from ubertool.terrestrial_toxicity import TerrestrialToxicity
from ubertool.ecosystem_inputs import EcosystemInputs
from ubertool.ubertool import Ubertool


class UserInp(forms.Form):
    user = users.get_current_user()
    user_id = user.user_id()
    q = db.Query(PesticideProperties)
    q.filter('user =',user)
    pests = ()
    pests += ((None,None),)
    for pest in q:
        #logger.info(use.to_xml())
        pests += ((pest.config_name,pest.config_name),)
    pest_configuration = forms.ChoiceField(required=True, choices=pests)
    q = db.Query(ExposureConcentrations)
    q.filter('user =',user)
    exposures = ()
    exposures += ((None,None),)
    for exposure in q:
        #logger.info(use.to_xml())
        exposures += ((exposure.config_name,exposure.config_name),)
    exposures_configuration = forms.ChoiceField(required=True, choices=exposures)
    q = db.Query(AquaticToxicity)
    q.filter('user =',user)
    aquatics = ()
    aquatics += ((None,None),)
    for aquatic in q:
        #logger.info(use.to_xml())
        aquatics += ((aquatic.config_name,aquatic.config_name),)
    aquatic_configuration = forms.ChoiceField(required=True, choices=aquatics)
    q = db.Query(TerrestrialToxicity)
    q.filter('user =',user)
    terrestrials = ()
    terrestrials += ((None,None),)
    for terrestrial in q:
        #logger.info(use.to_xml())
        terrestrials += ((terrestrial.config_name,terrestrial.config_name),)
    terrestrial_configuration = forms.ChoiceField(required=True, choices=terrestrials)
    q = db.Query(EcosystemInputs)
    q.filter('user =',user)
    ecosystems = ()
    ecosystems += ((None,None),)
    for ecosystem in q:
        #logger.info(use.to_xml())
        ecosystems += ((ecosystem.config_name,ecosystem.config_name),)
    ecosystems_configuration = forms.ChoiceField(required=True, choices=ecosystems)
    q = db.Query(Ubertool)
    q.filter('user =',user)
    ubertools = ()
    ubertools += ((None,None),)
    for ubertool in q:
        #logger.info(use.to_xml())
        ubertools += ((ubertool.config_name,ubertool.config_name),)
    ubertools_configuration = forms.ChoiceField(required=True, choices=ubertools)

    