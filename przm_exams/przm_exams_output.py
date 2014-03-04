# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
cgitb.enable()
import json
from przm_exams import przm_exams_model, przm_exams_tables
from uber import uber_lib
import base64
import urllib
from google.appengine.api import urlfetch
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3
import rest_funcs

###########################################################################               
station_pool={'NC Sweet Potato MLRA-133': 'Raleigh/Durham, NC', 'ID Potato   MLRA-11B': 'Pocatello, ID', 'NY Grape   MLRA-100/101': 'Binghamton, NY', 'CA Citrus   MLRA-17': 'Bakersfield, CA', 'OR Hops   MLRA-2': 'Salem, OR', 'FL Sugarcane   MLRA-156A': 'W Palm Beach, FL', 'OR Mint   MLRA-2': 'Salem, OR', 'FL Citrus   MLRA-156A': 'W Palm Beach, FL', 'CA Almonds MLRA-17': 'Sacramento, CA', 'ND Canola   MLRA-55A': 'Minot, ND', 'MI Asparagus MLRA-96': 'Muskegon, MI', 'PR Coffee MLRA-270': 'San Juan, PR', 'FL Avocado MLRA-156A': 'Miami, FL', 'NC Tobacco   MLRA-133A': 'Raleigh/Durham, NC', 'CA Grape  MLRA-17': 'Fresno, CA', 'FL Cucumber   MLRA-156A': 'W Palm Beach, FL', 'OH Corn   MLRA-111': 'Dayton, OH', 'NC Apple   MLRA-130': 'Asheville, NC', 'CA Onions MLRA-17': 'Bakersfield, CA', 'PA Turf  MLRA-148': 'Harrisburg, PA', 'MI Beans MLRA-99': 'Flint, MI', 'GA Onions MLRA-153A/133A': 'Savannah, GA', 'LA Sugarcane   MLRA-131': 'Baton Rouge, LA', 'NC Corn - E   MLRA-153A': 'Raleigh/Durham, NC', 'OR Christmas Trees  MLRA-2': 'Salem, OR', 'MN Sugarbeet   MLRA-56': 'Fargo, ND', 'FL Turf  MLRA-155': 'Daytona Beach, FL', 'MS Cotton   MLRA-134': 'Jackson, MS', 'MS Soybean   MLRA-134': 'Jackson, MS', 'GA Pecan   MLRA-133A': 'Tallahassee, FL', 'OR Filberts   MLRA-2': 'Salem, OR', 'OR Grass Seed   MLRA-2': 'Salem, OR', 'GA Peach   MLRA-133A': 'Macon, GA', 'FL Carrots MLRA-156B': 'W Palm Beach, FL', 'NC Cotton   MLRA-133A': 'Raleigh/Durham, NC', 'CA Lettuce  MLRA-14': 'Santa Maria, CA', 'FL Tomato   MLRA-155': 'W Palm Beach, FL', 'OR Apple   MLRA-2': 'Salem, OR', 'ND Wheat   MLRA-56': 'Fargo, ND', 'CA Tomato MLRA-17': 'Fresno, CA', 'PA Corn   MLRA-148': 'Harrisburg, PA', 'FL Peppers MLRA-156A': 'W Palm Beach, FL', 'MS Corn   MLRA-134': 'Jackson, MS', 'MI Cherry   MLRA-96': 'Traverse City, MI', 'IL Corn   MLRA-108': 'Peoria, IL', 'ME Potato   MLRA-146': 'Caribou, ME', 'FL Strawberry   MLRA-155': 'Tampa, FL', 'KS Sorghum   MLRA-112': 'Topeka, KS', 'PA Apple   MLRA-148': 'Harrisburg, PA', 'CA Cotton   MLRA-17': 'Fresno, CA', 'NC Peanut   MLRA-153A': 'Raleigh/Durham, NC', 'FL Cabbage   MLRA-155': 'Tampa, FL'}
met_pool={'NC Sweet Potato MLRA-133': 'W13722.DVF', 'ID Potato   MLRA-11B': 'W24156.DVF', 'NY Grape   MLRA-100/101': 'W04725.DVF', 'CA Citrus   MLRA-17': 'W23155.DVF', 'OR Hops   MLRA-2': 'W24232.DVF', 'FL Sugarcane   MLRA-156A': 'W12844.DVF', 'OR Mint   MLRA-2': 'W24232.DVF', 'FL Citrus   MLRA-156A': 'W12844.DVF', 'CA Almonds MLRA-17': 'W23232.DVF', 'ND Canola   MLRA-55A': 'W24013.DVF', 'MI Asparagus MLRA-96': 'w14840.DVF', 'PR Coffee MLRA-270': 'W11641.DVF', 'FL Avocado MLRA-156A': 'W12839.DVF', 'NC Tobacco   MLRA-133A': 'W13722.DVF', 'CA Grape  MLRA-17': 'W93193.DVF', 'FL Cucumber   MLRA-156A': 'W12844.DVF', 'OH Corn   MLRA-111': 'W93815.DVF', 'NC Apple   MLRA-130': 'W03812.DVF', 'CA Onions MLRA-17': 'W23155.DVF', 'PA Turf  MLRA-148': 'W14751.DVF', 'MI Beans MLRA-99': 'W14826.DVF', 'GA Onions MLRA-153A/133A': 'W03822.DVF', 'LA Sugarcane   MLRA-131': 'W13970.DVF', 'NC Corn - E   MLRA-153A': 'W13722.DVF', 'OR Christmas Trees  MLRA-2': 'W24232.DVF', 'MN Sugarbeet   MLRA-56': 'W14914.DVF', 'FL Turf  MLRA-155': 'W12834.DVF', 'MS Cotton   MLRA-134': 'W03940.DVF', 'MS Soybean   MLRA-134': 'W03940.DVF', 'GA Pecan   MLRA-133A': 'W93805.DVF', 'OR Filberts   MLRA-2': 'W24232.DVF', 'OR Grass Seed   MLRA-2': 'W24232.DVF', 'GA Peach   MLRA-133A': 'W03813.DVF', 'FL Carrots MLRA-156B': 'W12844.DVF', 'NC Cotton   MLRA-133A': 'W13722.DVF', 'CA Lettuce  MLRA-14': 'W93193.DVF', 'FL Tomato   MLRA-155': 'W12844.DVF', 'OR Apple   MLRA-2': 'W24232.DVF', 'ND Wheat   MLRA-56': 'W14914.DVF', 'CA Tomato MLRA-17': 'W93193.DVF', 'PA Corn   MLRA-148': 'W14751.DVF', 'FL Peppers MLRA-156A': 'W12844.DVF', 'MS Corn   MLRA-134': 'W03940.DVF', 'MI Cherry   MLRA-96': 'W14850.DVF', 'IL Corn   MLRA-108': 'W14842.DVF', 'ME Potato   MLRA-146': 'W14607.DVF', 'FL Strawberry   MLRA-155': 'W12842.DVF', 'KS Sorghum   MLRA-112': 'W13996.DVF', 'PA Apple   MLRA-148': 'W14751.DVF', 'CA Cotton   MLRA-17': 'W93193.DVF', 'NC Peanut   MLRA-153A': 'W13722.DVF', 'FL Cabbage   MLRA-155': 'W12842.DVF'}
inp_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.INP', 'ID Potato   MLRA-11B': 'ID1Pot-P.INP', 'NY Grape   MLRA-100/101': 'NY2Gra-P.INP', 'CA Citrus   MLRA-17': 'CA1Cit-P.INP', 'OR Hops   MLRA-2': 'OR1Hop-P.INP', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.INP', 'OR Mint   MLRA-2': 'OR1Min-P.INP', 'FL Citrus   MLRA-156A': 'FL1Cit-P.INP', 'CA Almonds MLRA-17': 'CA1Wal-P.INP', 'ND Canola   MLRA-55A': 'ND1Cno-P.INP', 'MI Asparagus MLRA-96': 'MI1Asp-P.INP', 'PR Coffee MLRA-270': 'PR1Cof-P.INP', 'FL Avocado MLRA-156A': 'FL1Avo-P.INP', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.INP', 'CA Grape  MLRA-17': 'CA1Gra-P.INP', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.INP', 'OH Corn   MLRA-111': 'OH1Cor-P.INP', 'NC Apple   MLRA-130': 'NC1App-P.INP', 'CA Onions MLRA-17': 'CA1Oni-P.INP', 'PA Turf  MLRA-148': 'PA1Tur-P.INP', 'MI Beans MLRA-99': 'MI1Bea-P.INP', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.INP', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.INP', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.INP', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.INP', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.INP', 'FL Turf  MLRA-155': 'FL1Tur-P.INP', 'MS Cotton   MLRA-134': 'MS1Ctt-P.INP', 'MS Soybean   MLRA-134': 'MS1Syb-P.INP', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.INP', 'OR Filberts   MLRA-2': 'OR1Fil-P.INP', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.INP', 'GA Peach   MLRA-133A': 'GA1Pch-P.INP', 'FL Carrots MLRA-156B': 'FL1Car-P.INP', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.INP', 'CA Lettuce  MLRA-14': 'CA1Let-P.INP', 'FL Tomato   MLRA-155': 'FL1Tma-P.INP', 'OR Apple   MLRA-2': 'OR1App-P.INP', 'ND Wheat   MLRA-56': 'ND1Whe-P.INP', 'CA Tomato MLRA-17': 'CA1Tma-P.INP', 'PA Corn   MLRA-148': 'PA1Cor-P.INP', 'FL Peppers MLRA-156A': 'FL1Pep-P.INP', 'MS Corn   MLRA-134': 'MS1Cor-P.INP', 'MI Cherry   MLRA-96': 'MI1Che-P.INP', 'IL Corn   MLRA-108': 'IL1Cor-P.INP', 'ME Potato   MLRA-146': 'ME1Pot-P.INP', 'FL Strawberry   MLRA-155': 'FL1Str-P.INP', 'KS Sorghum   MLRA-112': 'KS2Srg-P.INP', 'PA Apple   MLRA-148': 'PA1App-P.INP', 'CA Cotton   MLRA-17': 'CA1Ctt-P.INP', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.INP', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.INP'}
run_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.RUN', 'ID Potato   MLRA-11B': 'ID1Pot-P.RUN', 'NY Grape   MLRA-100/101': 'NY2Gra-P.RUN', 'CA Citrus   MLRA-17': 'CA1Cit-P.RUN', 'OR Hops   MLRA-2': 'OR1Hop-P.RUN', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.RUN', 'OR Mint   MLRA-2': 'OR1Min-P.RUN', 'FL Citrus   MLRA-156A': 'FL1Cit-P.RUN', 'CA Almonds MLRA-17': 'CA1Wal-P.RUN', 'ND Canola   MLRA-55A': 'ND1Cno-P.RUN', 'MI Asparagus MLRA-96': 'MI1Asp-P.RUN', 'PR Coffee MLRA-270': 'PR1Cof-P.RUN', 'FL Avocado MLRA-156A': 'FL1Avo-P.RUN', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.RUN', 'CA Grape  MLRA-17': 'CA1Gra-P.RUN', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.RUN', 'OH Corn   MLRA-111': 'OH1Cor-P.RUN', 'NC Apple   MLRA-130': 'NC1App-P.RUN', 'CA Onions MLRA-17': 'CA1Oni-P.RUN', 'PA Turf  MLRA-148': 'PA1Tur-P.RUN', 'MI Beans MLRA-99': 'MI1Bea-P.RUN', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.RUN', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.RUN', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.RUN', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.RUN', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.RUN', 'FL Turf  MLRA-155': 'FL1Tur-P.RUN', 'MS Cotton   MLRA-134': 'MS1Ctt-P.RUN', 'MS Soybean   MLRA-134': 'MS1Syb-P.RUN', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.RUN', 'OR Filberts   MLRA-2': 'OR1Fil-P.RUN', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.RUN', 'GA Peach   MLRA-133A': 'GA1Pch-P.RUN', 'FL Carrots MLRA-156B': 'FL1Car-P.RUN', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.RUN', 'CA Lettuce  MLRA-14': 'CA1Let-P.RUN', 'FL Tomato   MLRA-155': 'FL1Tma-P.RUN', 'OR Apple   MLRA-2': 'OR1App-P.RUN', 'ND Wheat   MLRA-56': 'ND1Whe-P.RUN', 'CA Tomato MLRA-17': 'CA1Tma-P.RUN', 'PA Corn   MLRA-148': 'PA1Cor-P.RUN', 'FL Peppers MLRA-156A': 'FL1Pep-P.RUN', 'MS Corn   MLRA-134': 'MS1Cor-P.RUN', 'MI Cherry   MLRA-96': 'MI1Che-P.RUN', 'IL Corn   MLRA-108': 'IL1Cor-P.RUN', 'ME Potato   MLRA-146': 'ME1Pot-P.RUN', 'FL Strawberry   MLRA-155': 'FL1Str-P.RUN', 'KS Sorghum   MLRA-112': 'KS2Srg-P.RUN', 'PA Apple   MLRA-148': 'PA1App-P.RUN', 'CA Cotton   MLRA-17': 'CA1Ctt-P.RUN', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.RUN', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.RUN'}
exam_pool={'NC Sweet Potato MLRA-133': 'NC1SWE-P.EXA', 'ID Potato   MLRA-11B': 'ID1Pot-P.EXA', 'NY Grape   MLRA-100/101': 'NY2Gra-P.EXA', 'CA Citrus   MLRA-17': 'CA1Cit-P.EXA', 'OR Hops   MLRA-2': 'OR1Hop-P.EXA', 'FL Sugarcane   MLRA-156A': 'FL1Sgc-P.EXA', 'OR Mint   MLRA-2': 'OR1Min-P.EXA', 'FL Citrus   MLRA-156A': 'FL1Cit-P.EXA', 'CA Almonds MLRA-17': 'CA1Wal-P.EXA', 'ND Canola   MLRA-55A': 'ND1Cno-P.EXA', 'MI Asparagus MLRA-96': 'MI1Asp-P.EXA', 'PR Coffee MLRA-270': 'PR1Cof-P.EXA', 'FL Avocado MLRA-156A': 'FL1Avo-P.EXA', 'NC Tobacco   MLRA-133A': 'NC1Tba-P.EXA', 'CA Grape  MLRA-17': 'CA1Gra-P.EXA', 'FL Cucumber   MLRA-156A': 'FL1Cuc-P.EXA', 'OH Corn   MLRA-111': 'OH1Cor-P.EXA', 'NC Apple   MLRA-130': 'NC1App-P.EXA', 'CA Onions MLRA-17': 'CA1Oni-P.EXA', 'PA Turf  MLRA-148': 'PA1Tur-P.EXA', 'MI Beans MLRA-99': 'MI1Bea-P.EXA', 'GA Onions MLRA-153A/133A': 'GA1Oni-P.EXA', 'LA Sugarcane   MLRA-131': 'LA1Sgc-P.EXA', 'NC Corn - E   MLRA-153A': 'NC1Cor-P.EXA', 'OR Christmas Trees  MLRA-2': 'OR1Xma-P.EXA', 'MN Sugarbeet   MLRA-56': 'MN1Sbe-P.EXA', 'FL Turf  MLRA-155': 'FL1Tur-P.EXA', 'MS Cotton   MLRA-134': 'MS1Ctt-P.EXA', 'MS Soybean   MLRA-134': 'MS1Syb-P.EXA', 'GA Pecan   MLRA-133A': 'GA1Pcn-P.EXA', 'OR Filberts   MLRA-2': 'OR1Fil-P.EXA', 'OR Grass Seed   MLRA-2': 'OR1Gra-P.EXA', 'GA Peach   MLRA-133A': 'GA1Pch-P.EXA', 'FL Carrots MLRA-156B': 'FL1Car-P.EXA', 'NC Cotton   MLRA-133A': 'NC1Ctt-P.EXA', 'CA Lettuce  MLRA-14': 'CA1Let-P.EXA', 'FL Tomato   MLRA-155': 'FL1Tma-P.EXA', 'OR Apple   MLRA-2': 'OR1App-P.EXA', 'ND Wheat   MLRA-56': 'ND1Whe-P.EXA', 'CA Tomato MLRA-17': 'CA1Tma-P.EXA', 'PA Corn   MLRA-148': 'PA1Cor-P.EXA', 'FL Peppers MLRA-156A': 'FL1Pep-P.EXA', 'MS Corn   MLRA-134': 'MS1Cor-P.EXA', 'MI Cherry   MLRA-96': 'MI1Che-P.EXA', 'IL Corn   MLRA-108': 'IL1Cor-P.EXA', 'ME Potato   MLRA-146': 'ME1Pot-P.EXA', 'FL Strawberry   MLRA-155': 'FL1Str-P.EXA', 'KS Sorghum   MLRA-112': 'KS2Srg-P.EXA', 'PA Apple   MLRA-148': 'PA1App-P.EXA', 'CA Cotton   MLRA-17': 'CA1Ctt-P.EXA', 'NC Peanut   MLRA-153A': 'NC1Pnt-P.EXA', 'FL Cabbage   MLRA-155': 'FL1Cbb-P.EXA'}
###########################################################################               


class PRZMEXAMSOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        scenarios =form.getvalue('Scenarios')
        chem_name = form.getvalue('chemical_name')
        noa = int(form.getvalue('NOA'))
        unit = form.getvalue('Unit')

        station = station_pool[scenarios]
        met_o = met_pool[scenarios]
        inp_o = inp_pool[scenarios]
        run_o = run_pool[scenarios]
        exam_o = exam_pool[scenarios]

        met_o=str(met_o)
        inp_o=str(inp_o)
        run_o=str(run_o)
        exam_o=str(exam_o)

####################################################        
######inputs related to different applications#####
####################################################
        Apt = []        #Application timings (indicators)
        Apt_p = []      #Application timings (words)
        DayRe = []      #Days relevant to the application
        Ap_mp = []      #Application methods (words)
        Ar = []         #Application rates
        CAM_f_p = []    #Chemical application Methods (words)
        CAM_f = []      #Chemical application Methods (indicators)
        EFF_p = []      #EFF (words)
        EFF = []        #EFF (numbers)
        Drft_p = []     #Drft (words)
        Drft = []       #Drft (numbers)
        DEPI_p = []     #DEPI (numbers)
        Date_inp = []   #Date 
        
        for i in range(noa):
            if i<1:    
                Apt_temp = form.getvalue('Apt')
                Apt.append(Apt_temp)
                Date_inp_temp=form.getvalue('Date_apt')
                Date_inp.append(Date_inp_temp)
                DayRe_temp = form.getvalue('DayRe')
                DayRe.append(DayRe_temp)
                
                CAM_1 = form.getvalue('CAM_1')
                CAM_2 = form.getvalue('CAM_2')
                CAM_3 = form.getvalue('CAM_3')
                CAM_4 = form.getvalue('CAM_4')  
                DEPI = form.getvalue('DEPI')
                
                Ap_m_temp = form.getvalue('Ap_m')
                Ap_mp.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[0])
                Ar_temp = form.getvalue('Ar')
                Ar.append(float(Ar_temp))
              
                CAM_f_p.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[0])   #CAM_f_p
                DEPI_p.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[1])   #DEPI                
                CAM_f.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[2])   #CAM_f
                EFF_p.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[2])
                Drft_p.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[3])
                EFF.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[4])
                Drft.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[5])

                if Apt_temp=='1':
                    Apt_p.append('Relative to planting')
                elif Apt_temp=='2':
                    Apt_p.append('Relative to emergence')
                elif Apt_temp=='3':
                    Apt_p.append('Relative to maturity')             
                elif Apt_temp=='4':
                    Apt_p.append('Relative to harvest')
                elif Apt_temp=='5':
                    Apt_p.append('Enter your own dates')                    
                    
            else:
                j=i+1
                Apt_temp = form.getvalue('Apt'+str(j))
                Apt.append(Apt_temp)
                Date_inp_temp=form.getvalue('Date_apt'+str(j))
                Date_inp.append(Date_inp_temp)             
                DayRe_temp = form.getvalue('DayRe'+str(j))
                DayRe.append(DayRe_temp)
                
                CAM_1 = form.getvalue('CAM_1_'+str(j))
                CAM_2 = form.getvalue('CAM_2_'+str(j))
                CAM_3 = form.getvalue('CAM_3_'+str(j))
                CAM_4 = form.getvalue('CAM_4_'+str(j)) 
                DEPI = form.getvalue('DEPI_'+str(j))
                
                Ap_m_temp = form.getvalue('Ap_m'+str(j))
                Ap_mp.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[0])
                Ar_temp = form.getvalue('Ar'+str(j))
                Ar.append(float(Ar_temp))
                
                CAM_f_p.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[0])   #CAM_f_p
                DEPI_p.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[1])   #DEPI                
                CAM_f.append(przm_exams_model.CAM_select(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[1], DEPI)[2])   #CAM_f
                EFF_p.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[2])
                Drft_p.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[3])
                EFF.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[4])
                Drft.append(przm_exams_model.Ap_m_select(Ap_m_temp, CAM_1, CAM_2, CAM_3, CAM_4)[5])
                
                if Apt_temp=='1':
                    Apt_p.append('Relative to planting')
                elif Apt_temp=='2':
                    Apt_p.append('Relative to emergence')
                elif Apt_temp=='3':
                    Apt_p.append('Relative to maturity')             
                elif Apt_temp=='4':
                    Apt_p.append('Relative to harvest') 
                elif Apt_temp=='5':
                    Apt_p.append('Enter your own dates') 
                                                        
        MM=przm_exams_model.es_date(noa, scenarios, Apt, DayRe, Date_inp)[0]
        DD=przm_exams_model.es_date(noa, scenarios, Apt, DayRe, Date_inp)[1]
        YY='61'
        
        if unit=='2':
            Ar=[1.12*kk for kk in Ar]
        else:
            Ar=Ar

        Ar_text=['%.4f' %i for i in Ar]
        CAM_f_f = [float(i) for i in CAM_f]
        CAM_text=['%.2f' %i for i in CAM_f_f]
        DEPI_f = [float(i) for i in DEPI_p]
        DEPI_text=['%.2f' %i for i in DEPI_f]

###################################################
#################EXAMS Inputs######################
###################################################

        farm =form.getvalue('farm_pond')
        mw = form.getvalue('molecular_weight')
        sol = form.getvalue('solubility')
        koc = form.getvalue('Koc')
        vp = form.getvalue('vapor_pressure')
        aem = form.getvalue('aerobic_aquatic_metabolism')
        anm = form.getvalue('anaerobic_aquatic_metabolism')
        aqp = form.getvalue('aquatic_direct_photolysis')
        tmper = form.getvalue('temperature')

        n_ph = float(form.getvalue('n_ph'))
        ph_out = []
        hl_out = []
        for i in range(int(n_ph)):
            j=i+1
            ph_temp = form.getvalue('ph'+str(j))
            ph_out.append(float(ph_temp))
            hl_temp = float(form.getvalue('hl'+str(j)))
            hl_out.append(hl_temp)  

        przm_exams_obj = przm_exams_model.przm_exams(chem_name, noa, scenarios, unit, met_o, inp_o, run_o, exam_o, 
                                                     MM, DD, YY, CAM_f, DEPI_text, Ar_text, EFF, Drft, 
                                                     Apt_p, DayRe, Ap_mp, Ar, CAM_f_p, EFF_p, Drft_p, DEPI_f,
                                                     farm, mw, sol, koc, vp, aem, anm, aqp, tmper, n_ph, ph_out, hl_out)


        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "PRZM EXAMS Output")     
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'przm_exams','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'express', 
                'model_attributes':'PRZM-EXAMS Output'})
        html = html + przm_exams_tables.timestamp(przm_exams_obj)
        html = html + przm_exams_tables.table_all(przm_exams_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        rest_funcs.save_dic(html, przm_exams_obj.__dict__, 'przm_exams', 'single')

        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', PRZMEXAMSOutputPage)], debug=True)
 
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
