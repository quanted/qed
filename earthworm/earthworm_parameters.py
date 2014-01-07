import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class earthwormInp(forms.Form):
	# chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
	# body_weight_of_bird = forms.FloatField(required=True,label='NEED TO GET INPUTS.')
	k_ow = forms.FloatField(required = True, label = mark_safe('Octanol to water partition coefficient K<sub>OW</sub>'),initial = 57544)
	l_f_e = forms.FloatField(required = True, label = 'Lipid fraction of earthworm L', initial = 0.01)
	c_s = forms.FloatField(required = True, label = mark_safe('Chemical concentration in soil C<sub>S</sub> (mol/m<sup>3</sup>)'),initial = 0.055)
	k_d = forms.FloatField(required = True, label = mark_safe('Soil partitioning coefficient K<sub>d</sub> (cm<sup>3</sup>/g)'), initial = 69)
	p_s = forms.FloatField(required = True, label = mark_safe('Bulk density of soil &#961;<sub>s</sub> (g/cm<sup>3</sup>)'), initial = 1.7)
	c_w = forms.FloatField(required = True, label = mark_safe('Chemical concentration in pore water of soil C<sub>W</sub> (mol/m<sup>3</sup>)'), initial = 0.000447)
	m_w = forms.FloatField(required = True, label = mark_safe('Molecular weight of chemical MW (g/mol)'), initial = 406.9)
	p_e = forms.FloatField(required = True, label = mark_safe('Density of earthworm &#961;<sub>E</sub> (kg/m<sup>3</sup>)'), initial = 1000)
	

	

