import os
os.environ['DJANGO_SETTINGS_MODULE']= -1
import numpy as np
import math
import logging
from django.utils import simplejson

class fdadiet(object):
	def __init__(self,set_variables=True,run_methods=True,chemical_name='',trade_name='',run_use='',atuse_conc=1,residue=1,worst_case_est=1,vol=1,d=1,h=1,sa='',intake_avg=1,intake_90th=1,vars_dict=None):
		self.set_default_variables()
		if set_variables:
			if vars_dict != None:
				self.__dict__.update(vars_dict)
			else:
				self.chemical_name = chemical_name
				self.trade_name = trade_name
				self.run_use = run_use
				self.atuse_conc = atuse_conc
				self.residue = residue
				self.worst_case_est = worst_case_est
				self.vol = vol
				self.d = d
				self.h = h
				self.sa = sa
				self.intake_avg = intake_avg
				self.intake_90th = intake_90th
			if run_methods:
				self.run_methods()

	def set_default_variables(self):
		self.chemical_name = ''
		self.trade_name = ''
		self.run_use = ''
		self.atuse_conc = -1
		self.residue = -1
		self.worst_case_est = -1
		self.vol = -1
		self.d = -1
		self.h = -1
		self.sa = -1
		self.intake_avg = -1
		self.intake_90th = -1
		self.sa_cylinder = -1
		#outputs
		self.edi = -1

	def run_methods(self):
		if self.run_use == '0':
			self.edi_f()
		else:
			if self.sa > 0:
				try:
					self.sa = float(self.sa)
				except ValueError:
					raise ValueError\
					('Surface Area must be a real number')
				self.sa_cylinder = self.sa
			else:
				self.sa_cylinder_f()
			self.conc_f()
			self.edi_avg_vol_f()
			self.edi_90th_vol_f()

	def edi_f(self):
		if self.edi == -1:
			try:
				self.residue = float(self.residue)
				self.atuse_conc = float(self.atuse_conc)
				self.worst_case_est = float(self.worst_case_est)
			except IndexError:
				raise IndexError\
				('Sanitizer residue, "At-Use" Concentration and/or "Worst-Case" estimate of exposure must be supplied at the command line')
			except ValueError:
				raise ValueError\
				('Sanitizer residue, "At-Use" Concentration and/or "Worst-Case" estimate of exposure must be a real number')
			self.edi = self.residue * (self.atuse_conc / 1000) * self.worst_case_est
			return self.edi

	def sa_cylinder_f(self):
		if self.sa_cylinder == -1:
			try:
				self.d = float(self.d)
				self.h = float(self.h)
			except IndexError:
				raise IndexError\
				('Cross-sectional diameter and/or length of tank must be supplied at the command line')
			except ValueError:
				raise ValueError\
				('Cross-sectional diameter and/or length of tank must be a real number')
			self.r = self.d / 2
			self.sa_cylinder = (2 * math.pi * self.r**2) + (2 * math.pi * self.r * self.h)
			return self.sa_cylinder

	def conc_f(self):
		self.conc = (self.sa_cylinder * self.atuse_conc) / (self.vol * 1000)
		self.conc_unit_conv = self.conc * 929 * 0.264	# Unit conversion; ft2/gal to ug/L
		return self.conc_unit_conv

	def edi_avg_vol_f(self):
		self.edi_avg_vol = self.intake_avg * self.conc_unit_conv
		return self.edi_avg_vol

	def edi_90th_vol_f(self):
		self.edi_90th_vol = self.intake_90th * self.conc_unit_conv
		return self.edi_90th_vol