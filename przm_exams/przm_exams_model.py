import numpy as np
import logging
import sys



class przm_exams(object):

    def __init__(self, chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
                 MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                 Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
                 farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out):

        self.chem_name=chem_name
        self.noa=int(noa)
        self.scenarios=scenarios
        self.unit=unit

        self.met_o=met_o
        self.inp_o=inp_o
        self.run_o=run_o
        self.exam_o=exam_o

        self.MM=MM
        self.DD=DD
        self.YY=YY
        self.CAM_f=CAM_f
        self.DEPI_text=DEPI_text
        self.Ar_text=Ar_text
        self.EFF=EFF
        self.Drft=Drft

        self.Apt_p=Apt_p
        self.DayRe=DayRe
        self.Ap_mp=Ap_mp
        self.Ar=Ar
        self.CAM_f_p=CAM_f_p
        self.EFF_p=EFF_p
        self.Drft_p=Drft_p
        self.DEPI_f=DEPI_f


        if self.unit=='1':
            self.unit_p='kg/ha'
        elif self.unit=='2':
            self.unit_p='lb/acre'

        self.farm=farm
        self.mw=mw
        self.sol=sol
        self.koc=koc
        self.vp=vp
        self.aem=aem
        self.anm=anm
        self.aqp=aqp
        self.tmper=tmper
        self.n_ph=n_ph
        self.ph_out=ph_out
        self.hl_out=hl_out

        # self.met = met_pool[scenarios] 







# exams_obj = exams('chem_name_1', 'CA Almonds MLRA-17', 'Yes', 70, 71, 72, 73, 24, 25, 26, 27, 3, [5.0, 7.0, 11.0], [11.0, 12.0, 10.0])
# import json
# import simplejson
# input_list=json.dumps(exams_obj.__dict__)
# print input_list
# input_list1= simplejson.loads(input_list)
# print input_list1['hl_out'][0]
# import urllib
# data = urllib.urlencode({"input_list":input_list})
# print data
