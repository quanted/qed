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
    pest_configuration = forms.ChoiceField(required=True)
    exposures_configuration = forms.ChoiceField(required=True)
    aquatic_configuration = forms.ChoiceField(required=True)
    terrestrial_configuration = forms.ChoiceField(required=True)
    ecosystems_configuration = forms.ChoiceField(required=True)
    ubertools_configuration = forms.ChoiceField(required=True)

    