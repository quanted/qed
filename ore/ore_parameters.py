# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 2014

@author: J. Flaishans
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.template import Context, Template
from django.utils.safestring import mark_safe


# Define Custom Templates
def tmpl_ChemicalInp():
	tmpl_ChemicalInp = """
	<br>
	<table class="input_table tab tab_ToxInp">
	{% for field in form %}
		<tr><th>{{ field.label_tag }}</th><td>{{ field }}</td></tr>
	{% endfor %}
	</table>
	"""
	return tmpl_ChemicalInp

def tmpl_ToxInp():
	tmpl_ToxInp = """
	{% if header %}
		<table class="input_table tab {{ tab_name }}">
		<tr><th colspan="3">Exposure Duration: {{header}}</th></tr>
	{% endif %}
	{% if expMethod %}
		<tr><th colspan="2">{{ expMethod }}</th></tr>
	{% endif %}
		<tr><th rowspan="{{ noOfItems }}">{{ label }}</th>
	{% for field in form %}
			<th>{{ field.label_tag }}</th><td>{{ field }}</td></tr>
	{% endfor %}
		</tr>
	"""
	return tmpl_ToxInp

def tmpl_CropTargetSel():
	tmpl_CropTargetSel = """
		</table>
		<table class="input_table tab tab_CropTargetSel">
		{% for field in form %}
			<tr><th>Pick me:</th><td>{{ field }}</td></tr>
		{% endfor %}
		</table>
	"""
	return tmpl_CropTargetSel

def tmpl_OccHandler():
	tmpl_OccHandler = """
		</table>
		<table class="input_table tab tab_OccHandler">
		{% for field in form %}
			<tr><th>Exposure:</th><td>{{ field }}</td></tr>
		{% endfor %}
		</table>
	"""
	return tmpl_OccHandler

tmpl_ChemicalInp = Template(tmpl_ChemicalInp())
tmpl_ToxInp = Template(tmpl_ToxInp())
tmpl_CropTargetSel = Template(tmpl_CropTargetSel())
tmpl_OccHandler = Template(tmpl_OccHandler())

# Method(s) called from *_inputs.py
def form():
	# Chemical and Exposure Duration
	form_ChemicalInp = ore_ChemicalInp()
	html = tmpl_ChemicalInp.render(Context(dict(form=form_ChemicalInp)))
	# Dermal Short Term
	form_ToxInpDermal_NC_st = ore_ToxInpDermal_NC_st()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_NC_st, tab_name="tab_tox_st", header="Short-Term", expMethod="Dermal", label="Non-Cancer", noOfItems="4")))
	form_ToxInpDermal_abs_st = ore_ToxInpDermal_abs_st()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_abs_st, label="Absorption", noOfItems="2")))
	# Inhalation Short Term
	form_ToxInpInhalation_NC_st = ore_ToxInpInhalation_NC_st()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_NC_st, expMethod="Inhalation", label="Non-Cancer", noOfItems="6")))
	form_ToxInpInhalation_abs_st = ore_ToxInpInhalation_abs_st()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_abs_st, label="Absorption", noOfItems="2")))
	
	# Dermal Intermediate Term
	form_ToxInpDermal_NC_it = ore_ToxInpDermal_NC_it()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_NC_it, tab_name="tab_tox_it", header="Intermediate-Term", expMethod="Dermal", label="Non-Cancer", noOfItems="4")))
	form_ToxInpDermal_abs_it = ore_ToxInpDermal_abs_it()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_abs_it, label="Absorption", noOfItems="2")))
	# Inhalation Intermediate Term
	form_ToxInpInhalation_NC_it = ore_ToxInpInhalation_NC_it()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_NC_it, expMethod="Inhalation", label="Non-Cancer", noOfItems="6")))
	form_ToxInpInhalation_abs_it = ore_ToxInpInhalation_abs_it()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_abs_it, label="Absorption", noOfItems="2")))
	
	# Dermal Long Term
	form_ToxInpDermal_NC_lt = ore_ToxInpDermal_NC_lt()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_NC_lt, tab_name="tab_tox_lt", header="Long-Term", expMethod="Dermal", label="Non-Cancer", noOfItems="4")))
	form_ToxInpDermal_abs_lt = ore_ToxInpDermal_abs_lt()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpDermal_abs_lt, label="Absorption", noOfItems="2")))
	# Inhalation Long Term
	form_ToxInpInhalation_NC_lt = ore_ToxInpInhalation_NC_lt()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_NC_lt, expMethod="Inhalation", label="Non-Cancer", noOfItems="6")))
	form_ToxInpInhalation_abs_lt = ore_ToxInpInhalation_abs_lt()
	html = html + tmpl_ToxInp.render(Context(dict(form=ore_ToxInpInhalation_abs_lt, label="Absorption", noOfItems="2")))

	
	# Crop Target Category Lookup
	html = html + tmpl_CropTargetSel.render(Context(dict(form=ore_CropTargetSel)))


	# Crop Target Category Lookup
	html = html + tmpl_OccHandler.render(Context(dict(form=ore_OccHandler)))

	return html


# Begin parameters declaration
# Chemical and Exposure Duration
class ore_ChemicalInp(forms.Form):
	activeIngredient = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 1}), label='Active Ingredient')
	# expDuration_CHOICES=((0,'Short-Term'),(1,'Intermediate-Term'),(2,'Long-Term'))
	# expDuration = forms.ChoiceField(required=True, label='Exposure Duration', choices=expDuration_CHOICES, initial='Intermediate-Term')
	expDuration_CHOICES = (('st','Short-Term'), ('it','Intermediate-Term'), ('lt','Long-Term'))
	expDurationType = forms.MultipleChoiceField(label='Exposure Duration', choices=expDuration_CHOICES, widget=forms.CheckboxSelectMultiple())

# These ChoiceField Options are used across multiple classes
dermal_NC_POD_source_CHOICES = (('Oral','Oral'), ('Route-specific','Route-specific'))
abs_source_CHOICES = 	(('Human study','Human study'), ('Animal study','Animal study'), ('Estimated by POD or LOAEL/NOAEL comparison','Estimated by POD or LOAEL/NOAEL comparison'),
						('In vitro study','In vitro study'), ('Other','Other'))
bw_CHOICES = (('80','80'), ('69','69'), ('86','86'))
yesNo_CHOICES = (('No', 'No'), ('Yes', 'Yes'))

# Dermal Short Term Non-Cancer
class ore_ToxInpDermal_NC_st(forms.Form):
	dermal_NC_POD_st = forms.FloatField(required=True, label='POD (mg/kg/day)', initial=50)
	dermal_NC_POD_source_st = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='Route-specific')
	dermal_NC_endpoint_st = forms.ChoiceField(required=True, choices=yesNo_CHOICES, label='Enpoint based on fetal effects?')
	dermal_NC_LOC_st = forms.FloatField(required=True, label='LOC', initial=100)
# Dermal Short Term Inhalation
class ore_ToxInpDermal_abs_st(forms.Form):
	dermal_abs_frac_st = forms.FloatField(required=True, label='Absorption (0-1)', initial=0.25)
	dermal_abs_source_st = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
# Inhalation Short Term Non-Cancer
class ore_ToxInpInhalation_NC_st(forms.Form):
	inhalation_NC_POD_st = forms.FloatField(required=True, label='POD (mg/kg/day) Oral Study', initial=25)
	inhalation_NC_POD_HEC83_st = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (8.3 L/min)")
	inhalation_NC_POD_HEC167_st = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (16.7 L/min)")
	inhalation_NC_POD_HEC29_st = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (29 L/min)")
	inhalation_NC_POD_source_st = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='POD source/study', initial='Oral')
	inhalation_NC_LOC_st = forms.FloatField(required=True, label='LOC', initial=100)
# Inhalation Short Term Absorption
class ore_ToxInpInhalation_abs_st(forms.Form):
	inhalation_abs_frac_st = forms.FloatField(required=True, label='Absorption Fraction (0-1)', initial=1)
	inhalation_abs_source_st = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
	
	# bw_dermal_NC_st = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (dermal kg)')
	# bw_inhalation_NC_st = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (inhalation kg)')
	
	# lifetimeExp_jobTenure_st = forms.FloatField(required=True, label='Handler Job Tenure (years)', initial=35)
	# lifetimeExp_lifeExpectancy_st = forms.FloatField(required=True, label='Life Expectancy (years)', initial=78)

# Dermal Intermediate Term Non-Cancer
class ore_ToxInpDermal_NC_it(forms.Form):
	dermal_NC_POD_it = forms.FloatField(required=True, label='POD (mg/kg/day)', initial=50)
	dermal_NC_POD_source_it = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='Route-specific')
	dermal_NC_endpoint_it = forms.ChoiceField(required=True, choices=yesNo_CHOICES, label='Enpoint based on fetal effects?')
	dermal_NC_LOC_it = forms.FloatField(required=True, label='LOC', initial=100)
# Dermal Intermediate Term Inhalation
class ore_ToxInpDermal_abs_it(forms.Form):
	dermal_abs_frac_it = forms.FloatField(required=True, label='Absorption (0-1)', initial=0.25)
	dermal_abs_source_it = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
# Inhalation Intermediate Term Non-Cancer
class ore_ToxInpInhalation_NC_it(forms.Form):
	inhalation_NC_POD_it = forms.FloatField(required=True, label='POD (mg/kg/day) Oral Study', initial=25)
	inhalation_NC_POD_HEC83_it = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (8.3 L/min)")
	inhalation_NC_POD_HEC167_it = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (16.7 L/min)")
	inhalation_NC_POD_HEC29_it = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (29 L/min)")
	inhalation_NC_POD_source_it = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='POD source/study', initial='Oral')
	inhalation_NC_LOC_it = forms.FloatField(required=True, label='LOC', initial=100)
# Inhalation Intermediate Term Absorption
class ore_ToxInpInhalation_abs_it(forms.Form):
	inhalation_abs_frac_it = forms.FloatField(required=True, label='Absorption Fraction (0-1)', initial=1)
	inhalation_abs_source_it = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
	
	# bw_dermal_NC_it = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (dermal kg)')
	# bw_inhalation_NC_it = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (inhalation kg)')
	
	# lifetimeExp_jobTenure_it = forms.FloatField(required=True, label='Handler Job Tenure (years)', initial=35)
	# lifetimeExp_lifeExpectancy_it = forms.FloatField(required=True, label='Life Expectancy (years)', initial=78)

# Dermal Long Term Non-Cancer
class ore_ToxInpDermal_NC_lt(forms.Form):
	dermal_NC_POD_lt = forms.FloatField(required=True, label='POD (mg/kg/day)', initial=50)
	dermal_NC_POD_source_lt = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='Route-specific')
	dermal_NC_endpoint_lt = forms.ChoiceField(required=True, choices=yesNo_CHOICES, label='Enpoint based on fetal effects?')
	dermal_NC_LOC_lt = forms.FloatField(required=True, label='LOC', initial=100)
# Dermal Long Term Inhalation
class ore_ToxInpDermal_abs_lt(forms.Form):
	dermal_abs_frac_lt = forms.FloatField(required=True, label='Absorption (0-1)', initial=0.25)
	dermal_abs_source_lt = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
# Inhalation Long Term Non-Cancer
class ore_ToxInpInhalation_NC_lt(forms.Form):
	inhalation_NC_POD_lt = forms.FloatField(required=True, label='POD (mg/kg/day) Oral Study', initial=25)
	inhalation_NC_POD_HEC83_lt = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (8.3 L/min)")
	inhalation_NC_POD_HEC167_lt = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (16.7 L/min)")
	inhalation_NC_POD_HEC29_lt = forms.FloatField(required=True, label="POD (mg/kg/day) HEC (29 L/min)")
	inhalation_NC_POD_source_lt = forms.ChoiceField(required=True, choices=dermal_NC_POD_source_CHOICES, label='POD source/study', initial='Oral')
	inhalation_NC_LOC_lt = forms.FloatField(required=True, label='LOC', initial=100)
# Inhalation Long Term Absorption
class ore_ToxInpInhalation_abs_lt(forms.Form):
	inhalation_abs_frac_lt = forms.FloatField(required=True, label='Absorption Fraction (0-1)', initial=1)
	inhalation_abs_source_lt = forms.ChoiceField(required=True, choices=abs_source_CHOICES, label='Animal study')
	
	# bw_dermal_NC_lt = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (dermal kg)')
	# bw_inhalation_NC_lt = forms.ChoiceField(required=True, choices=bw_CHOICES, label='Adult weights (inhalation kg)')
	
	# lifetimeExp_jobTenure_lt = forms.FloatField(required=True, label='Handler Job Tenure (years)', initial=35)
	# lifetimeExp_lifeExpectancy_lt = forms.FloatField(required=True, label='Life Expectancy (years)', initial=78)


# Crop-Target Category Lookup Tab
class ore_CropTargetSel(forms.Form):
	crop_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 1}), label='Crop Name', initial="Corn")


# Occupational Handler Exposure Tab
class ore_OccHandler(forms.Form):
	exp_conc = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 1}), label='Exposure', initial="A lot :-(")