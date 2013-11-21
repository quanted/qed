# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:18:30 2013

@author: Jon F
"""

#Chemical Tab
working_dir = "Test/"
sorp_K_unit = 'Koc'        #Remove this line after done testing
chem_deg = '1'
if chem_deg == '3':
	nchem = '3'
elif chem_deg == '2':
	nchem = '2'
else:
	nchem = '1'
if sorp_K_unit == 'Koc':
	K_unit = 'True'
else:
	K_unit = 'False'

# Make sure default value for *2 and *3 are blank
sorp_K1 = "200"
sorp_K2 = ""
sorp_K3 = ""
sorp_K = [sorp_K1,sorp_K2,sorp_K3]
wc_hl1 = "21"
wc_hl2 = ""
wc_hl3 = ""
wc_hl = [wc_hl1,wc_hl2,wc_hl3]
w_temp1 = "25"
w_temp2 = ""
w_temp3 = ""
w_temp = [w_temp1,w_temp2,w_temp3]
bm_hl1 = "75"
bm_hl2 = ""
bm_hl3 = ""
bm_hl = [bm_hl1,bm_hl2,bm_hl3]
ben_temp1 = "25"
ben_temp2 = ""
ben_temp3 = ""
ben_temp = [ben_temp1,ben_temp2,ben_temp3]
ap_hl1 = "2.0"
ap_hl2 = ""
ap_hl3 = ""
ap_hl = [ap_hl1,ap_hl2,ap_hl3]
p_ref1 = "40"
p_ref2 = ""
p_ref3 = ""
p_ref = [p_ref1,p_ref2,p_ref3]
h_hl1 = ""
h_hl2 = ""
h_hl3 = ""
h_hl = [h_hl1,h_hl2,h_hl3]
s_hl1 = "100"
s_hl2 = ""
s_hl3 = ""
s_hl = [s_hl1,s_hl2,s_hl3]
s_ref1 = "25"
s_ref2 = ""
s_ref3 = ""
s_ref = [s_ref1,s_ref2,s_ref3]
f_hl1 = ""
f_hl2 = ""
f_hl3 = ""
f_hl = [f_hl1,f_hl2,f_hl3]
mwt1 = "311"
mwt2 = ""
mwt3 = ""
mwt = [mwt1,mwt2,mwt3]
vp1 = "8e-8"
vp2 = ""
vp3 = ""
vp = [vp1,vp2,vp3]
sol1 = "3.3"
sol2 = ""
sol3 = ""
sol = [sol1,sol2,sol3]

wc_mcf1 = "0"
wc_mcf2 = "0"
wc_mcf = [wc_mcf1,wc_mcf2]
ben_mcf1 = "0"
ben_mcf2 = "0"
ben_mcf = [ben_mcf1,ben_mcf2]
p_mcf1 = "0"
p_mcf2 = "0"
p_mcf = [p_mcf1,p_mcf2]
h_mcf1 = "0"
h_mcf2 = "0"
h_mcf = [h_mcf1,h_mcf2]
s_mcf1 = "0"
s_mcf2 = "0"
s_mcf = [s_mcf1,s_mcf2]
f_mcf1 = "0"
f_mcf2 = "0"
f_mcf = [f_mcf1,f_mcf2]

QT = "2"


#Crop/Land Tab
scenID = "CAlettuceSTD"
dvf_path = "test.dvf"


# Water Body Tab
burial = ""
if burial == 1:
	buried = "1"
else:
	buried = ""
buried = ""
D_over_dx = "1e-8"
PRBEN = "0.5"
benthic_depth = "0.05"
porosity = "0.5"
bulk_density = "1.35"
FROC2 = "0.04"
DOC2 = "5"
BNMAS = "0.006"
DFAC = "1.19"
SUSED = "30"
CHL = "0.005"
FROC1 = "0.04"
DOC1 = "5"
PLMAS = "0.4"
