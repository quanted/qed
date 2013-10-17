import os
os.environ['DJANGO_SETTINGS_MODULE']= -1
import numpy as np
import math
import logging
from django.utils import simplejson



class hedgas(object):
	def __init__(self, set_variables=True,run_methods=True,
				run_acuteNonOcc='',mw_acuteNonOcc=1,noael_acuteNonOcc=1,hrs_animal_acuteNonOcc=1,hrs_human_acuteNonOcc=1,dow_animal_acuteNonOcc=1,dow_human_acuteNonOcc=1,b0_acuteNonOcc=1,b1_acuteNonOcc=1,SAa_acuteNonOcc=1,tb_acuteNonOcc=1,pu_acuteNonOcc=1,
				run_stitNonOcc='',mw_stitNonOcc=1,noael_stitNonOcc=1,hrs_animal_stitNonOcc=1,hrs_human_stitNonOcc=1,BWa_stitNonOcc=1,dow_animal_stitNonOcc=1,dow_human_stitNonOcc=1,b0_stitNonOcc=1,b1_stitNonOcc=1,SAa_stitNonOcc=1,tb_stitNonOcc=1,pu_stitNonOcc=1,
				run_ltNonOcc='',mw_ltNonOcc=1,noael_ltNonOcc=1,hrs_animal_ltNonOcc=1,hrs_human_ltNonOcc=1,BWa_ltNonOcc=1,dow_animal_ltNonOcc=1,dow_human_ltNonOcc=1,b0_ltNonOcc=1,b1_ltNonOcc=1,SAa_ltNonOcc=1,tb_ltNonOcc=1,pu_ltNonOcc=1,
				run_acuteOcc='',mw_acuteOcc=1,noael_acuteOcc=1,hrs_animal_acuteOcc=1,hrs_human_acuteOcc=1,BWa_acuteOcc=1,dow_animal_acuteOcc=1,dow_human_acuteOcc=1,b0_acuteOcc=1,b1_acuteOcc=1,SAa_acuteOcc=1,tb_acuteOcc=1,pu_acuteOcc=1,
				run_stitOcc='',mw_stitOcc=1,noael_stitOcc=1,hrs_animal_stitOcc=1,hrs_human_stitOcc=1,BWa_stitOcc=1,dow_animal_stitOcc=1,dow_human_stitOcc=1,b0_stitOcc=1,b1_stitOcc=1,SAa_stitOcc=1,tb_stitOcc=1,pu_stitOcc=1,
				run_ltOcc='',mw_ltOcc=1,noael_ltOcc=1,hrs_animal_ltOcc=1,hrs_human_ltOcc=1,BWa_ltOcc=1,dow_animal_ltOcc=1,dow_human_ltOcc=1,b0_ltOcc=1,b1_ltOcc=1,SAa_ltOcc=1,tb_ltOcc=1,pu_ltOcc=1,
				vars_dict=None):
		self.set_default_variables()
		if set_variables:
			if vars_dict != None:
				self.__dict__.update(vars_dict)
			else:
				self.run_acuteNonOcc = run_acuteNonOcc
				self.mw_acuteNonOcc = mw_acuteNonOcc
				self.noael_acuteNonOcc = noael_acuteNonOcc
				self.hrs_animal_acuteNonOcc = hrs_animal_acuteNonOcc
				self.hrs_human_acuteNonOcc = hrs_human_acuteNonOcc
				self.dow_animal_acuteNonOcc = dow_animal_acuteNonOcc
				self.dow_human_acuteNonOcc = dow_human_acuteNonOcc
				self.b0_acuteNonOcc = b0_acuteNonOcc
				self.b1_acuteNonOcc = b1_acuteNonOcc
				self.SAa_acuteNonOcc = SAa_acuteNonOcc
				self.tb_acuteNonOcc = tb_acuteNonOcc
				self.pu_acuteNonOcc = pu_acuteNonOcc
				self.run_stitNonOcc = run_stitNonOcc
				self.mw_stitNonOcc = mw_stitNonOcc
				self.noael_stitNonOcc = noael_stitNonOcc
				self.hrs_animal_stitNonOcc = hrs_animal_stitNonOcc
				self.hrs_human_stitNonOcc = hrs_human_stitNonOcc
				self.BWa_stitNonOcc = BWa_stitNonOcc
				self.dow_animal_stitNonOcc = dow_animal_stitNonOcc
				self.dow_human_stitNonOcc = dow_human_stitNonOcc
				self.b0_stitNonOcc = b0_stitNonOcc
				self.b1_stitNonOcc = b1_stitNonOcc
				self.SAa_stitNonOcc = SAa_stitNonOcc
				self.tb_stitNonOcc = tb_stitNonOcc
				self.pu_stitNonOcc = pu_stitNonOcc
				self.run_ltNonOcc = run_ltNonOcc
				self.mw_ltNonOcc = mw_ltNonOcc
				self.noael_ltNonOcc = noael_ltNonOcc
				self.hrs_animal_ltNonOcc = hrs_animal_ltNonOcc
				self.hrs_human_ltNonOcc = hrs_human_ltNonOcc
				self.BWa_ltNonOcc = BWa_ltNonOcc
				self.dow_animal_ltNonOcc = dow_animal_ltNonOcc
				self.dow_human_ltNonOcc = dow_human_ltNonOcc
				self.b0_ltNonOcc = b0_ltNonOcc
				self.b1_ltNonOcc = b1_ltNonOcc
				self.SAa_ltNonOcc = SAa_ltNonOcc
				self.tb_ltNonOcc = tb_ltNonOcc
				self.pu_ltNonOcc = pu_ltNonOcc
				self.run_acuteOcc = run_acuteOcc
				self.mw_acuteOcc = mw_acuteOcc
				self.noael_acuteOcc = noael_acuteOcc
				self.hrs_animal_acuteOcc = hrs_animal_acuteOcc
				self.hrs_human_acuteOcc = hrs_human_acuteOcc
				self.BWa_acuteOcc = BWa_acuteOcc
				self.dow_animal_acuteOcc = dow_animal_acuteOcc
				self.dow_human_acuteOcc = dow_human_acuteOcc
				self.b0_acuteOcc = b0_acuteOcc
				self.b1_acuteOcc = b1_acuteOcc
				self.SAa_acuteOcc = SAa_acuteOcc
				self.tb_acuteOcc = tb_acuteOcc
				self.pu_acuteOcc = pu_acuteOcc
				self.run_stitOcc = run_stitOcc
				self.mw_stitOcc = mw_stitOcc
				self.noael_stitOcc = noael_stitOcc
				self.hrs_animal_stitOcc = hrs_animal_stitOcc
				self.hrs_human_stitOcc = hrs_human_stitOcc
				self.BWa_stitOcc = BWa_stitOcc
				self.dow_animal_stitOcc = dow_animal_stitOcc
				self.dow_human_stitOcc = dow_human_stitOcc
				self.b0_stitOcc = b0_stitOcc
				self.b1_stitOcc = b1_stitOcc
				self.SAa_stitOcc = SAa_stitOcc
				self.tb_stitOcc = tb_stitOcc
				self.pu_stitOcc = pu_stitOcc
				self.run_ltOcc = run_ltOcc
				self.mw_ltOcc = mw_ltOcc
				self.noael_ltOcc = noael_ltOcc
				self.hrs_animal_ltOcc = hrs_animal_ltOcc
				self.hrs_human_ltOcc = hrs_human_ltOcc
				self.BWa_ltOcc = BWa_ltOcc
				self.dow_animal_ltOcc = dow_animal_ltOcc
				self.dow_human_ltOcc = dow_human_ltOcc
				self.b0_ltOcc = b0_ltOcc
				self.b1_ltOcc = b1_ltOcc
				self.SAa_ltOcc = SAa_ltOcc
				self.tb_ltOcc = tb_ltOcc
				self.pu_ltOcc = pu_ltOcc
			if run_methods:
				self.run_methods()

   	def set_default_variables(self):
		#inputs
		self.mw_acuteNonOcc = -1
		self.noael_acuteNonOcc = -1
		self.hrs_animal_acuteNonOcc = -1
		self.hrs_human_acuteNonOcc = -1
		self.dow_animal_acuteNonOcc = -1
		self.dow_human_acuteNonOcc = -1
		self.b0_acuteNonOcc = -1
		self.b1_acuteNonOcc = -1
		self.SAa_acuteNonOcc = -1
		self.tb_acuteNonOcc = -1
		self.pu_acuteNonOcc = -1
		self.mw_stitNonOcc = -1
		self.noael_stitNonOcc = -1
		self.hrs_animal_stitNonOcc = -1
		self.hrs_human_stitNonOcc = -1
		self.BWa_stitNonOcc = -1
		self.dow_animal_stitNonOcc = -1
		self.dow_human_stitNonOcc = -1
		self.b0_stitNonOcc = -1
		self.b1_stitNonOcc = -1
		self.SAa_stitNonOcc = -1
		self.tb_stitNonOcc = -1
		self.pu_stitNonOcc = -1
		self.mw_ltNonOcc = -1
		self.noael_ltNonOcc = -1
		self.hrs_animal_ltNonOcc = -1
		self.hrs_human_ltNonOcc = -1
		self.BWa_ltNonOcc = -1
		self.dow_animal_ltNonOcc = -1
		self.dow_human_ltNonOcc = -1
		self.b0_ltNonOcc = -1
		self.b1_ltNonOcc = -1
		self.SAa_ltNonOcc = -1
		self.tb_ltNonOcc = -1
		self.pu_ltNonOcc = -1
		self.run_acuteOcc = -1
		self.mw_acuteOcc = -1
		self.noael_acuteOcc = -1
		self.hrs_animal_acuteOcc = -1
		self.hrs_human_acuteOcc = -1
		self.BWa_acuteOcc = -1
		self.dow_animal_acuteOcc = -1
		self.dow_human_acuteOcc = -1
		self.b0_acuteOcc = -1
		self.b1_acuteOcc = -1
		self.SAa_acuteOcc = -1
		self.tb_acuteOcc = -1
		self.pu_acuteOcc = -1
		self.run_stitOcc = -1
		self.mw_stitOcc = -1
		self.noael_stitOcc = -1
		self.hrs_animal_stitOcc = -1
		self.hrs_human_stitOcc = -1
		self.BWa_stitOcc = -1
		self.dow_animal_stitOcc = -1
		self.dow_human_stitOcc = -1
		self.b0_stitOcc = -1
		self.b1_stitOcc = -1
		self.SAa_stitOcc = -1
		self.tb_stitOcc = -1
		self.pu_stitOcc = -1
		self.run_ltOcc = -1
		self.mw_ltOcc = -1
		self.noael_ltOcc = -1
		self.hrs_animal_ltOcc = -1
		self.hrs_human_ltOcc = -1
		self.BWa_ltOcc = -1
		self.dow_animal_ltOcc = -1
		self.dow_human_ltOcc = -1
		self.b0_ltOcc = -1
		self.b1_ltOcc = -1
		self.SAa_ltOcc = -1
		self.tb_ltOcc = -1
		self.pu_ltOcc = -1
		#ouputs
		self.noael_adj = -1
		self.mv_a = -1
		self.rgdr_ET = -1
		self.hec_ET = -1
		self.hec_ET_ppm = -1
		self.rgdr_TB = -1
		self.hec_TB = -1
		self.hec_TB_ppm = -1
		self.rgdr_PU = -1
		self.hec_PU = -1
		self.hec_PU_ppm = -1
		self.hec_SYS = -1
		self.hec_SYS_ppm = -1

    # def set_unit_testing_variables(self):

	def run_methods(self):
		if self.run_acuteNonOcc == '1':
			self.noael_adj_acuteNonOccET = self.noael_adj_f(self.hrs_animal_acuteNonOcc,self.hrs_human_acuteNonOcc,self.dow_animal_acuteNonOcc,self.dow_human_acuteNonOcc,self.noael_acuteNonOcc)
			self.mv_a_acuteNonOccET = self.mv_a_f(self.hrs_human_acuteNonOcc,self.b0_acuteNonOcc,self.b1_acuteNonOcc)
			self.rgdr_acuteNonOccET = self.rgdr_ET_f(self.mv_a_acuteNonOccET,self.SAa_acuteNonOcc)
			self.hec_acuteNonOccET = self.hec_ET_f(self.noael_adj_acuteNonOccET,self.rgdr_acuteNonOccET)
			self.hec_acuteNonOccET_ppm = self.hec_ET_ppm_f(self.mw_acuteNonOcc,self.hec_acuteNonOccET)
			self.rgdr_acuteNonOccTB = self.rgdr_TB_f(self.mv_a_acuteNonOccET,self.tb_acuteNonOcc)
			self.hec_acuteNonOccTB = self.hec_TB_f(self.noael_adj_acuteNonOccET,self.rgdr_acuteNonOccTB)
			self.hec_acuteNonOccTB_ppm = self.hec_TB_ppm_f(self.mw_acuteNonOcc,self.hec_acuteNonOccTB)
			self.rgdr_acuteNonOccPU = self.rgdr_PU_f(self.mv_a_acuteNonOccET,self.pu_acuteNonOcc)
			self.hec_acuteNonOccPU = self.hec_PU_f(self.noael_adj_acuteNonOccET,self.rgdr_acuteNonOccPU)
			self.hec_acuteNonOccPU_ppm = self.hec_PU_ppm_f(self.mw_acuteNonOcc,self.hec_acuteNonOccPU)
			self.hec_acuteNonOccSYS = self.noael_adj_acuteNonOccET
			self.hec_acuteNonOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_acuteNonOcc,self.noael_adj_acuteNonOccET)
			
		if self.run_stitNonOcc == '1':
			self.noael_adj_stitNonOccET = self.noael_adj_f(self.hrs_animal_stitNonOcc,self.hrs_human_stitNonOcc,self.dow_animal_stitNonOcc,self.dow_human_stitNonOcc,self.noael_stitNonOcc)
			self.mv_a_stitNonOccET = self.mv_a_f(self.BWa_stitNonOcc,self.b0_stitNonOcc,self.b1_stitNonOcc)
			self.rgdr_stitNonOccET = self.rgdr_ET_f(self.mv_a_stitNonOccET,self.SAa_stitNonOcc)
			self.hec_stitNonOccET = self.hec_ET_f(self.noael_adj_stitNonOccET,self.rgdr_stitNonOccET)
			self.hec_stitNonOccET_ppm = self.hec_ET_ppm_f(self.mw_stitNonOcc,self.hec_stitNonOccET)
			self.rgdr_stitNonOccTB = self.rgdr_TB_f(self.mv_a_stitNonOccET,self.tb_stitNonOcc)
			self.hec_stitNonOccTB = self.hec_TB_f(self.noael_adj_stitNonOccET,self.rgdr_stitNonOccTB)
			self.hec_stitNonOccTB_ppm = self.hec_TB_ppm_f(self.mw_stitNonOcc,self.hec_stitNonOccTB)
			self.rgdr_stitNonOccPU = self.rgdr_PU_f(self.mv_a_stitNonOccET,self.pu_stitNonOcc)
			self.hec_stitNonOccPU = self.hec_PU_f(self.noael_adj_stitNonOccET,self.rgdr_stitNonOccPU)
			self.hec_stitNonOccPU_ppm = self.hec_PU_ppm_f(self.mw_stitNonOcc,self.hec_stitNonOccPU)
			self.hec_stitNonOccSYS = self.noael_adj_stitNonOccET
			self.hec_stitNonOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_stitNonOcc,self.noael_adj_stitNonOccET)
			
		if self.run_ltNonOcc == '1':
			self.noael_adj_ltNonOccET = self.noael_adj_f(self.hrs_animal_ltNonOcc,self.hrs_human_ltNonOcc,self.dow_animal_ltNonOcc,self.dow_human_ltNonOcc,self.noael_ltNonOcc)
			self.mv_a_ltNonOccET = self.mv_a_f(self.BWa_ltNonOcc,self.b0_ltNonOcc,self.b1_ltNonOcc)
			self.rgdr_ltNonOccET = self.rgdr_ET_f(self.mv_a_ltNonOccET,self.SAa_ltNonOcc)
			self.hec_ltNonOccET = self.hec_ET_f(self.noael_adj_ltNonOccET,self.rgdr_ltNonOccET)
			self.hec_ltNonOccET_ppm = self.hec_ET_ppm_f(self.mw_ltNonOcc,self.hec_ltNonOccET)
			self.rgdr_ltNonOccTB = self.rgdr_TB_f(self.mv_a_ltNonOccET,self.tb_ltNonOcc)
			self.hec_ltNonOccTB = self.hec_TB_f(self.noael_adj_ltNonOccET,self.rgdr_ltNonOccTB)
			self.hec_ltNonOccTB_ppm = self.hec_TB_ppm_f(self.mw_ltNonOcc,self.hec_ltNonOccTB)
			self.rgdr_ltNonOccPU = self.rgdr_PU_f(self.mv_a_ltNonOccET,self.pu_ltNonOcc)
			self.hec_ltNonOccPU = self.hec_PU_f(self.noael_adj_ltNonOccET,self.rgdr_ltNonOccPU)
			self.hec_ltNonOccPU_ppm = self.hec_PU_ppm_f(self.mw_ltNonOcc,self.hec_ltNonOccPU)
			self.hec_ltNonOccSYS = self.noael_adj_ltNonOccET
			self.hec_ltNonOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_ltNonOcc,self.noael_adj_ltNonOccET)

		if self.run_acuteOcc == '1':
			self.noael_adj_acuteOccET = self.noael_adj_f(self.hrs_animal_acuteOcc,self.hrs_human_acuteOcc,self.dow_animal_acuteOcc,self.dow_human_acuteOcc,self.noael_acuteOcc)
			self.mv_a_acuteOccET = self.mv_a_f(self.BWa_acuteOcc,self.b0_acuteOcc,self.b1_acuteOcc)
			self.rgdr_acuteOccET = self.rgdr_ET_f(self.mv_a_acuteOccET,self.SAa_acuteOcc)
			self.hec_acuteOccET = self.hec_ET_f(self.noael_adj_acuteOccET,self.rgdr_acuteOccET)
			self.hec_acuteOccET_ppm = self.hec_ET_ppm_f(self.mw_acuteOcc,self.hec_acuteOccET)
			self.rgdr_acuteOccTB = self.rgdr_TB_f(self.mv_a_acuteOccET,self.tb_acuteOcc)
			self.hec_acuteOccTB = self.hec_TB_f(self.noael_adj_acuteOccET,self.rgdr_acuteOccTB)
			self.hec_acuteOccTB_ppm = self.hec_TB_ppm_f(self.mw_acuteOcc,self.hec_acuteOccTB)
			self.rgdr_acuteOccPU = self.rgdr_PU_f(self.mv_a_acuteOccET,self.pu_acuteOcc)
			self.hec_acuteOccPU = self.hec_PU_f(self.noael_adj_acuteOccET,self.rgdr_acuteOccPU)
			self.hec_acuteOccPU_ppm = self.hec_PU_ppm_f(self.mw_acuteOcc,self.hec_acuteOccPU)
			self.hec_acuteOccSYS = self.noael_adj_acuteOccET
			self.hec_acuteOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_acuteOcc,self.noael_adj_acuteOccET)
			
		if self.run_stitOcc == '1':
			self.noael_adj_stitOccET = self.noael_adj_f(self.hrs_animal_stitOcc,self.hrs_human_stitOcc,self.dow_animal_stitOcc,self.dow_human_stitOcc,self.noael_stitOcc)
			self.mv_a_stitOccET = self.mv_a_f(self.BWa_stitOcc,self.b0_stitOcc,self.b1_stitOcc)
			self.rgdr_stitOccET = self.rgdr_ET_f(self.mv_a_stitOccET,self.SAa_stitOcc)
			self.hec_stitOccET = self.hec_ET_f(self.noael_adj_stitOccET,self.rgdr_stitOccET)
			self.hec_stitOccET_ppm = self.hec_ET_ppm_f(self.mw_stitOcc,self.hec_stitOccET)
			self.rgdr_stitOccTB = self.rgdr_TB_f(self.mv_a_stitOccET,self.tb_stitOcc)
			self.hec_stitOccTB = self.hec_TB_f(self.noael_adj_stitOccET,self.rgdr_stitOccTB)
			self.hec_stitOccTB_ppm = self.hec_TB_ppm_f(self.mw_stitOcc,self.hec_stitOccTB)
			self.rgdr_stitOccPU = self.rgdr_PU_f(self.mv_a_stitOccET,self.pu_stitOcc)
			self.hec_stitOccPU = self.hec_PU_f(self.noael_adj_stitOccET,self.rgdr_stitOccPU)
			self.hec_stitOccPU_ppm = self.hec_PU_ppm_f(self.mw_stitOcc,self.hec_stitOccPU)
			self.hec_stitOccSYS = self.noael_adj_stitOccET
			self.hec_stitOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_stitOcc,self.noael_adj_stitOccET)
			
		if self.run_ltOcc == '1':
			self.noael_adj_ltOccET = self.noael_adj_f(self.hrs_animal_ltOcc,self.hrs_human_ltOcc,self.dow_animal_ltOcc,self.dow_human_ltOcc,self.noael_ltOcc)
			self.mv_a_ltOccET = self.mv_a_f(self.BWa_ltOcc,self.b0_ltOcc,self.b1_ltOcc)
			self.rgdr_ltOccET = self.rgdr_ET_f(self.mv_a_ltOccET,self.SAa_ltOcc)
			self.hec_ltOccET = self.hec_ET_f(self.noael_adj_ltOccET,self.rgdr_ltOccET)
			self.hec_ltOccET_ppm = self.hec_ET_ppm_f(self.mw_ltOcc,self.hec_ltOccET)
			self.rgdr_ltOccTB = self.rgdr_TB_f(self.mv_a_ltOccET,self.tb_ltOcc)
			self.hec_ltOccTB = self.hec_TB_f(self.noael_adj_ltOccET,self.rgdr_ltOccTB)
			self.hec_ltOccTB_ppm = self.hec_TB_ppm_f(self.mw_ltOcc,self.hec_ltOccTB)
			self.rgdr_ltOccPU = self.rgdr_PU_f(self.mv_a_ltOccET,self.pu_ltOcc)
			self.hec_ltOccPU = self.hec_PU_f(self.noael_adj_ltOccET,self.rgdr_ltOccPU)
			self.hec_ltOccPU_ppm = self.hec_PU_ppm_f(self.mw_ltOcc,self.hec_ltOccPU)
			self.hec_ltOccSYS = self.noael_adj_ltOccET
			self.hec_ltOccSYS_ppm = self.hec_SYS_ppm_f(self.mw_ltOcc,self.noael_adj_ltOccET)



	def noael_adj_f(self,hrs_animal,hrs_human,dow_animal,dow_human,noael):
		# if self.noael_adj == -1:
			# try:
			# 	self.hrs_animal_acuteNonOcc = float(self.hrs_animal_acuteNonOcc)
			# 	self.hrs_human_acuteNonOcc = float(self.hrs_human_acuteNonOcc)
			# 	self.dow_animal_acuteNonOcc = float(self.dow_animal_acuteNonOcc)
			# 	self.dow_human_acuteNonOcc = float(self.dow_human_acuteNonOcc)
			# 	self.noael_acuteNonOcc = float(self.noael_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The hours animal study, hours human, days of week animal, days of week human, and/or NOAEL must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The hours animal study must be a real number, not "%L"' %self.hrs_animal_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The hours human must be a real number, not "%L"' %self.hrs_human_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The days of week animal must be a real number, not "%L"' %self.dow_animal_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The days of week human must be a real number, not "%L"' %self.dow_human_acuteNonOcc)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The hours human, days of week human, and/or NOAEL must be non-zero')
			# if self.hrs_animal_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('hrs_animal_acuteNonOcc=%g is a non-physical value' %self.hrs_animal_acuteNonOcc)
			# if self.hrs_human_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('hrs_human_acuteNonOcc=%g is a non-physical value' %self.hrs_human_acuteNonOcc)
			# if self.dow_animal_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('dow_animal_acuteNonOcc=%g is a non-physical value' %self.dow_animal_acuteNonOcc)
			# if self.dow_human_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('dow_human_acuteNonOcc=%g is a non-physical value' %self.dow_human_acuteNonOcc)
			# if self.noael_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('noael_acuteNonOcc=%g is a non-physical value' %self.noael_acuteNonOcc)
		self.noael_adj = (hrs_animal / hrs_human) * (dow_animal / dow_human) * noael
		return self.noael_adj

	def mv_a_acuteNonOcc_f(self,exp_n,b0,b1):
		# if self.mv_a == -1:
			# try:
			# 	self.hrs_human_acuteNonOcc = float(self.hrs_human_acuteNonOcc)
			# 	self.b1_acuteNonOcc = float(self.b1_acuteNonOcc)
			# 	self.b0_acuteNonOcc = float(self.b0_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The hours human, b01, and/or b1 must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The hours human must be a real number, not "%L"' %self.hrs_human_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The b0 must be a real number, not "%L"' %self.b0_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The b1 must be a real number, not "%L"' %self.b1_acuteNonOcc)
			# if self.hrs_human_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('hrs_human_acuteNonOcc=%g is a non-physical value' %self.hrs_human_acuteNonOcc)
			# if self.b0_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('b0_acuteNonOcc=%g is a non-physical value' %self.b0_acuteNonOcc)
			# if self.b1_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('b1_acuteNonOcc=%g is a non-physical value' %self.b1_acuteNonOcc)
		self.mv_a = math.exp(math.log(exp_n) * b1 + b0)
		return self.mv_a

	def mv_a_f(self,hrs_human,b0,b1):
		# if self.mv_a == -1:
			# try:
			# 	self.hrs_human_acuteNonOcc = float(self.hrs_human_acuteNonOcc)
			# 	self.b1_acuteNonOcc = float(self.b1_acuteNonOcc)
			# 	self.b0_acuteNonOcc = float(self.b0_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The hours human, b01, and/or b1 must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The hours human must be a real number, not "%L"' %self.hrs_human_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The b0 must be a real number, not "%L"' %self.b0_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The b1 must be a real number, not "%L"' %self.b1_acuteNonOcc)
			# if self.hrs_human_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('hrs_human_acuteNonOcc=%g is a non-physical value' %self.hrs_human_acuteNonOcc)
			# if self.b0_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('b0_acuteNonOcc=%g is a non-physical value' %self.b0_acuteNonOcc)
			# if self.b1_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('b1_acuteNonOcc=%g is a non-physical value' %self.b1_acuteNonOcc)
		self.mv_a = math.exp(math.log(hrs_human) * b1 + b0)
		return self.mv_a

	def rgdr_ET_f(self,mv_a,SAa):
		# if self.rgdr_ET == -1:
			# try:
			# 	self.mv_a = float(self.mv_a)
			# 	self.SAa_acuteNonOcc = float(self.SAa_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The mv_a and/or SAa must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The SAa must be a real number, not "%L"' %self.SAa_acuteNonOcc)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The SAa must be non-zero')
			# if self.mv_a < 0:
			# 	raise ValueError\
			# 	('mv_a=%g is a non-physical value' %self.mv_a)
			# if self.SAa_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('SAa_acuteNonOcc=%g is a non-physical value' %self.SAa_acuteNonOcc)
		self.rgdr_ET = (mv_a / SAa) / 0.069
		return self.rgdr_ET

	def hec_ET_f(self,noael_adj,rgdr_ET):
		# if self.hec_ET == -1:
			# try:
			# 	self.noael_adj = float(self.noael_adj)
			# 	self.rgdr_ET = float(self.rgdr_ET)
			# except ValueError:
			# 	raise ValueError\
			# 	('The noael_adj must be a real number, not "%L"' %self.noael_adj)
			# except ValueError:
			# 	raise ValueError\
			# 	('The rgdr_ET must be a real number, not "%L"' %self.rgdr_ET)
			# if self.noael_adj < 0:
			# 	raise ValueError\
			# 	('noael_adj=%g is a non-physical value' %self.noael_adj)
			# if self.rgdr_ET < 0:
			# 	raise ValueError\
			# 	('rgdr_ET=%g is a non-physical value' %self.rgdr_ET)
		self.hec_ET = noael_adj * rgdr_ET
		return self.hec_ET

	def hec_ET_ppm_f(self,mw,hec_ET):
		# if self.hec_ET_ppm == -1:
			# try:
			# 	self.mw_acuteNonOcc = float(self.mw_acuteNonOcc)
			# 	self.hec_ET = float(self.hec_ET)
			# except ValueError:
			# 	raise ValueError\
			# 	('The mw must be a real number, not "%L"' %self.mw_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The hec_ET must be a real number, not "%L"' %self.hec_ET)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The molecular weight (mw) must be non-zero')
			# if self.mw_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('mw_acuteNonOcc=%g is a non-physical value' %self.mw_acuteNonOcc)
			# if self.hec_ET < 0:
			# 	raise ValueError\
			# 	('hec_ET=%g is a non-physical value' %self.hec_ET)
		self.hec_ET_ppm = (24.45 / mw) * hec_ET
		return self.hec_ET_ppm

	def rgdr_TB_f(self,mv_a,tb):
		# if self.rgdr_TB == -1:
			# try:
			# 	self.mv_a = float(self.mv_a)
			# 	self.tb_acuteNonOcc = float(self.tb_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The mv_a and/or tb must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The tb must be a real number, not "%L"' %self.tb_acuteNonOcc)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The tb must be non-zero')
			# if self.mv_a < 0:
			# 	raise ValueError\
			# 	('mv_a=%g is a non-physical value' %self.mv_a)
			# if self.tb_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('tb_acuteNonOcc=%g is a non-physical value' %self.tb_acuteNonOcc)
		self.rgdr_TB = (mv_a / tb) / (13.8 / 3200)
		return self.rgdr_TB

	def hec_TB_f(self,noael_adj,rgdr_TB):
		# if self.hec_TB == -1:
			# try:
			# 	self.noael_adj = float(self.noael_adj)
			# 	self.rgdr_TB = float(self.rgdr_TB)
			# except ValueError:
			# 	raise ValueError\
			# 	('The noael_adj must be a real number, not "%L"' %self.noael_adj)
			# except ValueError:
			# 	raise ValueError\
			# 	('The rgdr_TB must be a real number, not "%L"' %self.rgdr_TB)
			# if self.noael_adj < 0:
			# 	raise ValueError\
			# 	('noael_adj=%g is a non-physical value' %self.noael_adj)
			# if self.rgdr_TB < 0:
			# 	raise ValueError\
			# 	('rgdr_TB=%g is a non-physical value' %self.rgdr_TB)
		self.hec_TB = noael_adj * rgdr_TB
		return self.hec_TB

	def hec_TB_ppm_f(self,mw,hec_TB):
		# if self.hec_TB_ppm == -1:
			# try:
			# 	self.mw_acuteNonOcc = float(self.mw_acuteNonOcc)
			# 	self.hec_TB = float(self.hec_TB)
			# except ValueError:
			# 	raise ValueError\
			# 	('The mw must be a real number, not "%L"' %self.mw_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The hec_TB must be a real number, not "%L"' %self.hec_TB)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The molecular weight (mw) must be non-zero')
			# if self.mw_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('mw_acuteNonOcc=%g is a non-physical value' %self.mw_acuteNonOcc)
			# if self.hec_TB < 0:
			# 	raise ValueError\
			# 	('hec_TB=%g is a non-physical value' %self.hec_TB)
		self.hec_TB_ppm = (24.45 / mw) * hec_TB
		return self.hec_TB_ppm

	def rgdr_PU_f(self,mv_a,pu):
		# if self.rgdr_PU == -1:
			# try:
			# 	self.mv_a = float(self.mv_a)
			# 	self.pu_acuteNonOcc = float(self.pu_acuteNonOcc)
			# except IndexError:
			# 	raise IndexError\
			# 	('The mv_a and/or pu must be supplied')
			# except ValueError:
			# 	raise ValueError\
			# 	('The pu must be a real number, not "%L"' %self.pu_acuteNonOcc)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The pu must be non-zero')
			# if self.mv_a < 0:
			# 	raise ValueError\
			# 	('mv_a=%g is a non-physical value' %self.mv_a)
			# if self.pu_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('pu=%g is a non-physical value' %self.pu_acuteNonOcc)
		self.rgdr_PU = (mv_a / pu) / (13.8 / 54)
		return self.rgdr_PU

	def hec_PU_f(self,noael_adj,rgdr_PU):
		# if self.hec_PU == -1:
			# try:
			# 	self.noael_adj = float(self.noael_adj)
			# 	self.rgdr_PU = float(self.rgdr_PU)
			# except ValueError:
			# 	raise ValueError\
			# 	('The noael_adj must be a real number, not "%L"' %self.noael_adj)
			# except ValueError:
			# 	raise ValueError\
			# 	('The rgdr_PU must be a real number, not "%L"' %self.rgdr_PU)
			# if self.noael_adj < 0:
			# 	raise ValueError\
			# 	('noael_adj=%g is a non-physical value' %self.noael_adj)
			# if self.rgdr_PU < 0:
			# 	raise ValueError\
			# 	('rgdr_PU=%g is a non-physical value' %self.rgdr_PU)
		self.hec_PU = noael_adj * rgdr_PU
		return self.hec_PU

	def hec_PU_ppm_f(self,mw,hec_PU):
		# if self.hec_PU_ppm == -1:
			# try:
			# 	self.mw_acuteNonOcc = float(self.mw_acuteNonOcc)
			# 	self.hec_PU = float(self.hec_PU)
			# except ValueError:
			# 	raise ValueError\
			# 	('The mw must be a real number, not "%L"' %self.mw_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The hec_PU must be a real number, not "%L"' %self.hec_PU)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The molecular weight (mw) must be non-zero')
			# if self.mw_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('mw_acuteNonOcc=%g is a non-physical value' %self.mw_acuteNonOcc)
			# if self.hec_PU < 0:
			# 	raise ValueError\
			# 	('hec_PU=%g is a non-physical value' %self.hec_PU)
		self.hec_PU_ppm = (24.45 / mw) * hec_PU
		return self.hec_PU_ppm

	# def hec_SYS_f(self,noael_adj):
	# 	if self.hec_SYS == -1:
	# 		# try:
	# 		# 	self.noael_adj = float(self.noael_adj)
	# 		# except ValueError:
	# 		# 	raise ValueError\
	# 		# 	('NOAEL_adj must be a real number, not "%L"' %self.noael_adj)
	# 		# if self.noael_adj < 0:
	# 		# 	raise ValueError\
	# 		# 	('NOAEL_adj=%g is a non-physical value' %self.noael_adj)
	# 		self.hec_SYS = noael_adj
	# 	return self.hec_SYS

	def hec_SYS_ppm_f(self,mw,noael_adj):
		# if self.hec_SYS_ppm == -1:
			# try:
			# 	self.mw_acuteNonOcc = float(self.mw_acuteNonOcc)
			# 	self.hec_SYS = float(self.hec_SYS)
			# except ValueError:
			# 	raise ValueError\
			# 	('The mw must be a real number, not "%L"' %self.mw_acuteNonOcc)
			# except ValueError:
			# 	raise ValueError\
			# 	('The hec_SYS must be a real number, not "%L"' %self.hec_SYS)
			# except ZeroDivisionError:
			# 	raise ZeroDivisionError\
			# 	('The molecular weight (mw) must be non-zero')
			# if self.mw_acuteNonOcc < 0:
			# 	raise ValueError\
			# 	('mw_acuteNonOcc=%g is a non-physical value' %self.mw_acuteNonOcc)
			# if self.hec_SYS < 0:
			# 	raise ValueError\
			# 	('hec_SYS=%g is a non-physical value' %self.hec_SYS)
		self.hec_SYS_ppm = (24.45 / mw) * noael_adj
		return self.hec_SYS_ppm