import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import unittest
from StringIO import StringIO
# from iec import iec_output
from pprint import pprint
import csv
import sys
sys.path.append("../kabam")
from kabam import kabam_model,kabam_tables
import logging
from uber import uber_lib
import rest_funcs

logger = logging.getLogger('KabamQaqcPage')

cwd= os.getcwd()
data = csv.reader(open(cwd+'/kabam/kabam_qaqc.csv'))

# Inputs
chemical_name=[]
l_kow=[]
k_oc=[]
c_wdp=[]
water_column_EEC=[]
c_wto=[]
mineau_scaling_factor=[]
x_poc=[]
x_doc=[]
c_ox=[]
w_t=[]
c_ss=[]
oc=[]
k_ow=[]
Species_of_the_tested_bird =[]
bw_quail =[]
bw_duck =[]
bwb_other =[]
avian_ld50=[]
avian_lc50=[]
avian_noaec=[]
m_species =[]
bw_rat =[]
bwm_other =[]
mammalian_ld50=[]
mammalian_lc50=[]
mammalian_chronic_endpoint=[]
lf_p_sediment=[]
lf_p_phytoplankton=[]
lf_p_zooplankton=[]
lf_p_benthic_invertebrates=[]
lf_p_filter_feeders=[]
lf_p_small_fish=[]
lf_p_medium_fish=[]
mf_p_sediment=[]
mf_p_phytoplankton=[]
mf_p_zooplankton=[]
mf_p_benthic_invertebrates=[]
mf_p_filter_feeders=[]
mf_p_small_fish=[]
sf_p_sediment=[]
sf_p_phytoplankton=[]
sf_p_zooplankton=[]
sf_p_benthic_invertebrates=[]
sf_p_filter_feeders=[]
ff_p_sediment=[]
ff_p_phytoplankton=[]
ff_p_zooplankton=[]
ff_p_benthic_invertebrates=[]
beninv_p_sediment=[]
beninv_p_phytoplankton=[]
beninv_p_zooplankton=[]
zoo_p_sediment=[]
zoo_p_phyto=[]
s_lipid=[]
s_NLOM=[]
s_water=[]
v_lb_phytoplankton=[]
v_nb_phytoplankton=[]
v_wb_phytoplankton=[]
wb_zoo=[]
v_lb_zoo=[]
v_nb_zoo=[]
v_wb_zoo=[]
wb_beninv=[]
v_lb_beninv=[]
v_nb_beninv=[]
v_wb_beninv=[]
wb_ff=[]
v_lb_ff=[]
v_nb_ff=[]
v_wb_ff=[]
wb_sf=[]
v_lb_sf=[]
v_nb_sf=[]
v_wb_sf=[]
wb_mf=[]
v_lb_mf=[]
v_nb_mf=[]
v_wb_mf=[]
wb_lf=[]
v_lb_lf=[]
v_nb_lf=[]
v_wb_lf=[]
kg_phytoplankton=[]
kd_phytoplankton=[]
ke_phytoplankton=[]
mo_phytoplankton=[]
mp_phytoplankton=[]
km_phytoplankton=[]
km_zoo=[]
k1_phytoplankton=[]
k2_phytoplankton=[]
k1_zoo=[]
k2_zoo=[]
kd_zoo=[]
ke_zoo=[]
k1_beninv=[]
k2_beninv=[]
kd_beninv=[]
ke_beninv=[]
km_beninv=[]
k1_ff=[]
k2_ff=[]
kd_ff=[]
ke_ff=[]
km_ff=[]
k1_sf=[]
k2_sf=[]
kd_sf=[]
ke_sf=[]
km_sf=[]
k1_mf=[]
k2_mf=[]
kd_mf=[]
ke_mf=[]
km_mf=[]
k1_lf=[]
k2_lf=[]
kd_lf=[]
ke_lf=[]
km_lf=[]
rate_constants=[]
s_respire=[]
phyto_respire=[]
zoo_respire=[]
beninv_respire=[]
ff_respire=[]
sfish_respire=[]
mfish_respire=[]
lfish_respire=[]

# Outputs
cb_phytoplankton=[]
cb_zoo=[]
cb_beninv=[]
cb_ff=[]
cb_sf=[]
cb_mf=[]
cb_lf=[]
cbl_phytoplankton=[]
cbl_zoo=[]
cbl_beninv=[]
cbl_ff=[]
cbl_sf=[]
cbl_mf=[]
cbl_lf=[]
cbd_zoo=[]
cbd_beninv=[]
cbd_ff=[]
cbd_sf=[]
cbd_mf=[]
cbd_lf=[]
cbr_phytoplankton=[]
cbr_zoo=[]
cbr_beninv=[]
cbr_ff=[]
cbr_sf=[]
cbr_mf=[]
cbr_lf=[]
cbf_phytoplankton=[]
cbf_zoo=[]
cbf_beninv=[]
cbf_ff=[]
cbf_sf=[]
cbf_mf=[]
cbf_lf=[]
cbaf_phytoplankton=[]
cbaf_zoo=[]
cbaf_beninv=[]
cbaf_ff=[]
cbaf_sf=[]
cbaf_mf=[]
cbaf_lf=[]
cbfl_phytoplankton=[]
cbfl_zoo=[]
cbfl_beninv=[]
cbfl_ff=[]
cbfl_sf=[]
cbfl_mf=[]
cbfl_lf=[]
cbafl_phytoplankton=[]
cbafl_zoo=[]
cbafl_beninv=[]
cbafl_ff=[]
cbafl_sf=[]
cbafl_mf=[]
cbafl_lf=[]
bmf_zoo=[]
bmf_beninv=[]
bmf_ff=[]
bmf_sf=[]
cbmf_mf=[]
cbmf_lf=[]
cbsafl_phytoplankton=[]
cbsafl_zoo=[]
cbsafl_beninv=[]
cbsafl_ff=[]
cbsafl_sf=[]
cbsafl_mf=[]
cbsafl_lf=[]
mweight0=[]
mweight1=[]
mweight2=[]
mweight3=[]
mweight4=[]
mweight5=[]
aweight0=[]
aweight1=[]
aweight2=[]
aweight3=[]
aweight4=[]
aweight5=[]
dfir0=[]
dfir1=[]
dfir2=[]
dfir3=[]
dfir4=[]
dfir5=[]
dfira0=[]
dfira1=[]
dfira2=[]
dfira3=[]
dfira4=[]
dfira5=[]
wet_food_ingestion_m0=[]
wet_food_ingestion_m1=[]
wet_food_ingestion_m2=[]
wet_food_ingestion_m3=[]
wet_food_ingestion_m4=[]
wet_food_ingestion_m5=[]
wet_food_ingestion_a0=[]
wet_food_ingestion_a1=[]
wet_food_ingestion_a2=[]
wet_food_ingestion_a3=[]
wet_food_ingestion_a4=[]
wet_food_ingestion_a5=[]
drinking_water_intake_m0=[]
drinking_water_intake_m1=[]
drinking_water_intake_m2=[]
drinking_water_intake_m3=[]
drinking_water_intake_m4=[]
drinking_water_intake_m5=[]
drinking_water_intake_a0=[]
drinking_water_intake_a1=[]
drinking_water_intake_a2=[]
drinking_water_intake_a3=[]
drinking_water_intake_a4=[]
drinking_water_intake_a5=[]
db40=[]
db41=[]
db42=[]
db43=[]
db44=[]
db45=[]
db4a0=[]
db4a1=[]
db4a2=[]
db4a3=[]
db4a4=[]
db4a5=[]
db50=[]
db51=[]
db52=[]
db53=[]
db54=[]
db55=[]
db5a0=[]
db5a1=[]
db5a2=[]
db5a3=[]
db5a4=[]
db5a5=[]
acute_dose_based_m0=[]
acute_dose_based_m1=[]
acute_dose_based_m2=[]
acute_dose_based_m3=[]
acute_dose_based_m4=[]
acute_dose_based_m5=[]
acute_dose_based_a0=[]
acute_dose_based_a1=[]
acute_dose_based_a2=[]
acute_dose_based_a3=[]
acute_dose_based_a4=[]
acute_dose_based_a5=[]
avian_lc50=[]
chronic_dose_based_m0=[]
chronic_dose_based_m1=[]
chronic_dose_based_m2=[]
chronic_dose_based_m3=[]
chronic_dose_based_m4=[]
chronic_dose_based_m5=[]
mammalian_chronic_endpoint_exp=[]
avian_noaec=[]
acute_rq_dose_m0=[]
acute_rq_dose_m1=[]
acute_rq_dose_m2=[]
acute_rq_dose_m3=[]
acute_rq_dose_m4=[]
acute_rq_dose_m5=[]
acute_rq_dose_a0=[]
acute_rq_dose_a1=[]
acute_rq_dose_a2=[]
acute_rq_dose_a3=[]
acute_rq_dose_a4=[]
acute_rq_dose_a5=[]
acute_rq_diet_a0=[]
acute_rq_diet_a1=[]
acute_rq_diet_a2=[]
acute_rq_diet_a3=[]
acute_rq_diet_a4=[]
acute_rq_diet_a5=[]
chronic_rq_dose_m0=[]
chronic_rq_dose_m1=[]
chronic_rq_dose_m2=[]
chronic_rq_dose_m3=[]
chronic_rq_dose_m4=[]
chronic_rq_dose_m5=[]
chronic_rq_diet_m0=[]
chronic_rq_diet_m1=[]
chronic_rq_diet_m2=[]
chronic_rq_diet_m3=[]
chronic_rq_diet_m4=[]
chronic_rq_diet_m5=[]
chronic_rq_diet_a0=[]
chronic_rq_diet_a1=[]
chronic_rq_diet_a2=[]
chronic_rq_diet_a3=[]
chronic_rq_diet_a4=[]
chronic_rq_diet_a5=[]


data.next()
for row in data:
    chemical_name.append(row[0])
    l_kow.append(float(row[1]))
    k_oc.append(float(row[2]))
    c_wdp.append(float(row[3]) / 1000000)
    water_column_EEC.append(float(row[4]))
    c_wto.append(float(row[4]) / 1000000)
    mineau_scaling_factor.append(float(row[5]))
    x_poc.append(float(row[6]))
    x_doc.append(float(row[7]))
    c_ox.append(float(row[8]))
    w_t.append(float(row[9]))
    c_ss.append(float(row[10]))
    oc.append(float(row[11]) / 100)
    k_ow.append(10**(float(row[1])))
    Species_of_the_tested_bird.append(row[12])
    bw_quail.append(row[13])
    bw_duck.append(row[14])
    bwb_other.append(row[15])
    avian_ld50.append(float(row[16]))
    avian_lc50.append(float(row[17]))
    avian_noaec.append(float(row[18]))
    m_species.append(row[19])
    bw_rat.append(row[20])
    bwm_other.append(row[21])
    mammalian_ld50.append(float(row[22]))
    mammalian_lc50.append(float(row[23]))
    mammalian_chronic_endpoint.append(float(row[24]))
    lf_p_sediment.append(float(row[25]) / 100)
    lf_p_phytoplankton.append(float(row[26]) / 100)
    lf_p_zooplankton.append(float(row[27]) / 100)
    lf_p_benthic_invertebrates.append(float(row[28]) / 100)
    lf_p_filter_feeders.append(float(row[29]) / 100)
    lf_p_small_fish.append(float(row[30]) / 100)
    lf_p_medium_fish.append(float(row[31]) / 100)
    mf_p_sediment.append(float(row[32]))
    mf_p_phytoplankton.append(float(row[33]))
    mf_p_zooplankton.append(float(row[34]))
    mf_p_benthic_invertebrates.append(float(row[35]) / 100)
    mf_p_filter_feeders.append(float(row[36]))
    mf_p_small_fish.append(float(row[37]) / 100)
    sf_p_sediment.append(float(row[38]))
    sf_p_phytoplankton.append(float(row[39]))
    sf_p_zooplankton.append(float(row[40]) / 100)
    sf_p_benthic_invertebrates.append(float(row[41]) / 100)
    sf_p_filter_feeders.append(float(row[42]))
    ff_p_sediment.append(float(row[43]) / 100)
    ff_p_phytoplankton.append(float(row[44]) / 100)
    ff_p_zooplankton.append(float(row[45]) / 100)
    ff_p_benthic_invertebrates.append(float(row[46]))
    beninv_p_sediment.append(float(row[47]) / 100)
    beninv_p_phytoplankton.append(float(row[48]) / 100)
    beninv_p_zooplankton.append(float(row[49]) / 100)
    zoo_p_sediment.append(float(row[50]))
    zoo_p_phyto.append(float(row[51]) / 100)
    s_lipid.append(float(row[52]) / 100)
    s_NLOM.append(float(row[53]) / 100)
    s_water.append(float(row[54]) / 100)
    v_lb_phytoplankton.append(float(row[55]) / 100)
    v_nb_phytoplankton.append(float(row[56]) / 100)
    v_wb_phytoplankton.append(float(row[57]) / 100)
    wb_zoo.append(float(row[58]))
    v_lb_zoo.append(float(row[59]) / 100)
    v_nb_zoo.append(float(row[60]) / 100)
    v_wb_zoo.append(float(row[61]) / 100)
    wb_beninv.append(float(row[62]))
    v_lb_beninv.append(float(row[63]) / 100)
    v_nb_beninv.append(float(row[64]) / 100)
    v_wb_beninv.append(float(row[65]) / 100)
    wb_ff.append(float(row[66]))
    v_lb_ff.append(float(row[67]) / 100)
    v_nb_ff.append(float(row[68]) / 100)
    v_wb_ff.append(float(row[69]) / 100)
    wb_sf.append(float(row[70]))
    v_lb_sf.append(float(row[71]) / 100)
    v_nb_sf.append(float(row[72]) / 100)
    v_wb_sf.append(float(row[73]) / 100)
    wb_mf.append(float(row[74]))
    v_lb_mf.append(float(row[75]) / 100)
    v_nb_mf.append(float(row[76]) / 100)
    v_wb_mf.append(float(row[77]) / 100)
    wb_lf.append(float(row[78]))
    v_lb_lf.append(float(row[79]) / 100)
    v_nb_lf.append(float(row[80]) / 100)
    v_wb_lf.append(float(row[81]) / 100)
    kg_phytoplankton.append(float(row[82]))
    kd_phytoplankton.append(float(row[83]))
    ke_phytoplankton.append(float(row[84]))
    mo_phytoplankton.append(float(row[85]))
    mp_phytoplankton.append(float(row[86]))
    km_phytoplankton.append(float(row[87]))
    km_zoo.append(float(row[88]))
    k1_phytoplankton.append(float(row[89]))
    k2_phytoplankton.append(float(row[90]))
    k1_zoo.append(float(row[91]))
    k2_zoo.append(float(row[92]))
    kd_zoo.append(float(row[93]))
    ke_zoo.append(float(row[94]))
    k1_beninv.append(float(row[95]))
    k2_beninv.append(float(row[96]))
    kd_beninv.append(float(row[97]))
    ke_beninv.append(float(row[98]))
    km_beninv.append(float(row[99]))
    k1_ff.append(float(row[100]))
    k2_ff.append(float(row[101]))
    kd_ff.append(float(row[102]))
    ke_ff.append(float(row[103]))
    km_ff.append(float(row[104]))
    k1_sf.append(float(row[105]))
    k2_sf.append(float(row[106]))
    kd_sf.append(float(row[107]))
    ke_sf.append(float(row[108]))
    km_sf.append(float(row[109]))
    k1_mf.append(float(row[110]))
    k2_mf.append(float(row[111]))
    kd_mf.append(float(row[112]))
    ke_mf.append(float(row[113]))
    km_mf.append(float(row[114]))
    k1_lf.append(float(row[115]))
    k2_lf.append(float(row[116]))
    kd_lf.append(float(row[117]))
    ke_lf.append(float(row[118]))
    km_lf.append(float(row[119]))
    rate_constants.append(row[120])
    s_respire.append(row[121])
    phyto_respire.append(row[122])
    zoo_respire.append(row[123])
    beninv_respire.append(row[124])
    ff_respire.append(row[125])
    sfish_respire.append(row[126])
    mfish_respire.append(row[127])
    lfish_respire.append(row[128])

    #outputs
    cb_phytoplankton.append(float(row[129]))
    cb_zoo.append(float(row[130]))
    cb_beninv.append(float(row[131]))
    cb_ff.append(float(row[132]))
    cb_sf.append(float(row[133]))
    cb_mf.append(float(row[134]))
    cb_lf.append(float(row[135]))
    cbl_phytoplankton.append(float(row[136]))
    cbl_zoo.append(float(row[137]))
    cbl_beninv.append(float(row[138]))
    cbl_ff.append(float(row[139]))
    cbl_sf.append(float(row[140]))
    cbl_mf.append(float(row[141]))
    cbl_lf.append(float(row[142]))
    cbd_zoo.append(float(row[143]))
    cbd_beninv.append(float(row[144]))
    cbd_ff.append(float(row[145]))
    cbd_sf.append(float(row[146]))
    cbd_mf.append(float(row[147]))
    cbd_lf.append(float(row[148]))
    cbr_phytoplankton.append(float(row[149]))
    cbr_zoo.append(float(row[150]))
    cbr_beninv.append(float(row[151]))
    cbr_ff.append(float(row[152]))
    cbr_sf.append(float(row[153]))
    cbr_mf.append(float(row[154]))
    cbr_lf.append(float(row[155]))
    cbf_phytoplankton.append(float(row[156]))
    cbf_zoo.append(float(row[157]))
    cbf_beninv.append(float(row[158]))
    cbf_ff.append(float(row[159]))
    cbf_sf.append(float(row[160]))
    cbf_mf.append(float(row[161]))
    cbf_lf.append(float(row[162]))
    cbaf_phytoplankton.append(float(row[163]))
    cbaf_zoo.append(float(row[164]))
    cbaf_beninv.append(float(row[165]))
    cbaf_ff.append(float(row[166]))
    cbaf_sf.append(float(row[167]))
    cbaf_mf.append(float(row[168]))
    cbaf_lf.append(float(row[169]))
    cbfl_phytoplankton.append(float(row[170]))
    cbfl_zoo.append(float(row[171]))
    cbfl_beninv.append(float(row[172]))
    cbfl_ff.append(float(row[173]))
    cbfl_sf.append(float(row[174]))
    cbfl_mf.append(float(row[175]))
    cbfl_lf.append(float(row[176]))
    cbafl_phytoplankton.append(float(row[177]))
    cbafl_zoo.append(float(row[178]))
    cbafl_beninv.append(float(row[179]))
    cbafl_ff.append(float(row[180]))
    cbafl_sf.append(float(row[181]))
    cbafl_mf.append(float(row[182]))
    cbafl_lf.append(float(row[183]))
    bmf_zoo.append(float(row[184]))
    bmf_beninv.append(float(row[185]))
    bmf_ff.append(float(row[186]))
    bmf_sf.append(float(row[187]))
    cbmf_mf.append(float(row[188]))
    cbmf_lf.append(float(row[189]))
    cbsafl_phytoplankton.append(float(row[190]))
    cbsafl_zoo.append(float(row[191]))
    cbsafl_beninv.append(float(row[192]))
    cbsafl_ff.append(float(row[193]))
    cbsafl_sf.append(float(row[194]))
    cbsafl_mf.append(float(row[195]))
    cbsafl_lf.append(float(row[196]))
    mweight0.append(float(row[197]))
    mweight1.append(float(row[198]))
    mweight2.append(float(row[199]))
    mweight3.append(float(row[200]))
    mweight4.append(float(row[201]))
    mweight5.append(float(row[202]))
    aweight0.append(float(row[203]))
    aweight1.append(float(row[204]))
    aweight2.append(float(row[205]))
    aweight3.append(float(row[206]))
    aweight4.append(float(row[207]))
    aweight5.append(float(row[208]))
    dfir0.append(float(row[209]))
    dfir1.append(float(row[210]))
    dfir2.append(float(row[211]))
    dfir3.append(float(row[212]))
    dfir4.append(float(row[213]))
    dfir5.append(float(row[214]))
    dfira0.append(float(row[215]))
    dfira1.append(float(row[216]))
    dfira2.append(float(row[217]))
    dfira3.append(float(row[218]))
    dfira4.append(float(row[219]))
    dfira5.append(float(row[220]))
    wet_food_ingestion_m0.append(float(row[221]))
    wet_food_ingestion_m1.append(float(row[222]))
    wet_food_ingestion_m2.append(float(row[223]))
    wet_food_ingestion_m3.append(float(row[224]))
    wet_food_ingestion_m4.append(float(row[225]))
    wet_food_ingestion_m5.append(float(row[226]))
    wet_food_ingestion_a0.append(float(row[227]))
    wet_food_ingestion_a1.append(float(row[228]))
    wet_food_ingestion_a2.append(float(row[229]))
    wet_food_ingestion_a3.append(float(row[230]))
    wet_food_ingestion_a4.append(float(row[231]))
    wet_food_ingestion_a5.append(float(row[232]))
    drinking_water_intake_m0.append(float(row[233]))
    drinking_water_intake_m1.append(float(row[234]))
    drinking_water_intake_m2.append(float(row[235]))
    drinking_water_intake_m3.append(float(row[236]))
    drinking_water_intake_m4.append(float(row[237]))
    drinking_water_intake_m5.append(float(row[238]))
    drinking_water_intake_a0.append(float(row[239]))
    drinking_water_intake_a1.append(float(row[240]))
    drinking_water_intake_a2.append(float(row[241]))
    drinking_water_intake_a3.append(float(row[242]))
    drinking_water_intake_a4.append(float(row[243]))
    drinking_water_intake_a5.append(float(row[244]))
    db40.append(float(row[245]))
    db41.append(float(row[246]))
    db42.append(float(row[247]))
    db43.append(float(row[248]))
    db44.append(float(row[249]))
    db45.append(float(row[250]))
    db4a0.append(float(row[251]))
    db4a1.append(float(row[252]))
    db4a2.append(float(row[253]))
    db4a3.append(float(row[254]))
    db4a4.append(float(row[255]))
    db4a5.append(float(row[256]))
    db50.append(float(row[257]))
    db51.append(float(row[258]))
    db52.append(float(row[259]))
    db53.append(float(row[260]))
    db54.append(float(row[261]))
    db55.append(float(row[262]))
    db5a0.append(float(row[263]))
    db5a1.append(float(row[264]))
    db5a2.append(float(row[265]))
    db5a3.append(float(row[266]))
    db5a4.append(float(row[267]))
    db5a5.append(float(row[268]))
    acute_dose_based_m0.append(float(row[269]))
    acute_dose_based_m1.append(float(row[270]))
    acute_dose_based_m2.append(float(row[271]))
    acute_dose_based_m3.append(float(row[272]))
    acute_dose_based_m4.append(float(row[273]))
    acute_dose_based_m5.append(float(row[274]))
    acute_dose_based_a0.append(float(row[275]))
    acute_dose_based_a1.append(float(row[276]))
    acute_dose_based_a2.append(float(row[277]))
    acute_dose_based_a3.append(float(row[278]))
    acute_dose_based_a4.append(float(row[279]))
    acute_dose_based_a5.append(float(row[280]))
    avian_lc50.append(float(row[281]))
    chronic_dose_based_m0.append(float(row[282]))
    chronic_dose_based_m1.append(float(row[283]))
    chronic_dose_based_m2.append(float(row[284]))
    chronic_dose_based_m3.append(float(row[285]))
    chronic_dose_based_m4.append(float(row[286]))
    chronic_dose_based_m5.append(float(row[287]))
    avian_noaec.append(float(row[288]))
    acute_rq_dose_m0.append(float(row[289]))
    acute_rq_dose_m1.append(float(row[290]))
    acute_rq_dose_m2.append(float(row[291]))
    acute_rq_dose_m3.append(float(row[292]))
    acute_rq_dose_m4.append(float(row[293]))
    acute_rq_dose_m5.append(float(row[294]))
    acute_rq_dose_a0.append(float(row[295]))
    acute_rq_dose_a1.append(float(row[296]))
    acute_rq_dose_a2.append(float(row[297]))
    acute_rq_dose_a3.append(float(row[298]))
    acute_rq_dose_a4.append(float(row[299]))
    acute_rq_dose_a5.append(float(row[300]))
    acute_rq_diet_a0.append(float(row[301]))
    acute_rq_diet_a1.append(float(row[302]))
    acute_rq_diet_a2.append(float(row[303]))
    acute_rq_diet_a3.append(float(row[304]))
    acute_rq_diet_a4.append(float(row[305]))
    acute_rq_diet_a5.append(float(row[306]))
    chronic_rq_dose_m0.append(float(row[307]))
    chronic_rq_dose_m1.append(float(row[308]))
    chronic_rq_dose_m2.append(float(row[309]))
    chronic_rq_dose_m3.append(float(row[310]))
    chronic_rq_dose_m4.append(float(row[311]))
    chronic_rq_dose_m5.append(float(row[312]))
    chronic_rq_diet_m0.append(float(row[313]))
    chronic_rq_diet_m1.append(float(row[314]))
    chronic_rq_diet_m2.append(float(row[315]))
    chronic_rq_diet_m3.append(float(row[316]))
    chronic_rq_diet_m4.append(float(row[317]))
    chronic_rq_diet_m5.append(float(row[318]))
    chronic_rq_diet_a0.append(float(row[319]))
    chronic_rq_diet_a1.append(float(row[320]))
    chronic_rq_diet_a2.append(float(row[321]))
    chronic_rq_diet_a3.append(float(row[322]))
    chronic_rq_diet_a4.append(float(row[323]))
    chronic_rq_diet_a5.append(float(row[324]))


kabam_obj = kabam_model.kabam(
            True,True,chemical_name[0],l_kow[0],k_oc[0],c_wdp[0],water_column_EEC[0],c_wto[0],mineau_scaling_factor[0],x_poc[0],x_doc[0],c_ox[0],w_t[0],c_ss[0],oc[0],k_ow[0],
            Species_of_the_tested_bird[0],bw_quail[0],bw_duck[0],bwb_other[0],avian_ld50[0],avian_lc50[0],avian_noaec[0],m_species[0],bw_rat[0],bwm_other[0],mammalian_ld50[0],mammalian_lc50[0],mammalian_chronic_endpoint[0],
            lf_p_sediment[0],lf_p_phytoplankton[0],lf_p_zooplankton[0],lf_p_benthic_invertebrates[0],lf_p_filter_feeders[0],lf_p_small_fish[0],lf_p_medium_fish[0],
            mf_p_sediment[0],mf_p_phytoplankton[0],mf_p_zooplankton[0],mf_p_benthic_invertebrates[0],mf_p_filter_feeders[0],mf_p_small_fish[0],
            sf_p_sediment[0],sf_p_phytoplankton[0],sf_p_zooplankton[0],sf_p_benthic_invertebrates[0],sf_p_filter_feeders[0],
            ff_p_sediment[0],ff_p_phytoplankton[0],ff_p_zooplankton[0],ff_p_benthic_invertebrates[0],
            beninv_p_sediment[0],beninv_p_phytoplankton[0],beninv_p_zooplankton[0],
            zoo_p_sediment[0],zoo_p_phyto[0],
            s_lipid[0],s_NLOM[0],s_water[0],
            v_lb_phytoplankton[0],v_nb_phytoplankton[0],v_wb_phytoplankton[0],wb_zoo[0],v_lb_zoo[0],v_nb_zoo[0],v_wb_zoo[0],wb_beninv[0],v_lb_beninv[0],v_nb_beninv[0],v_wb_beninv[0],wb_ff[0],v_lb_ff[0],v_nb_ff[0],v_wb_ff[0],wb_sf[0],v_lb_sf[0],v_nb_sf[0],v_wb_sf[0],wb_mf[0],v_lb_mf[0],v_nb_mf[0],v_wb_mf[0],wb_lf[0],v_lb_lf[0],v_nb_lf[0],v_wb_lf[0],
            kg_phytoplankton[0],kd_phytoplankton[0],ke_phytoplankton[0],mo_phytoplankton[0],mp_phytoplankton[0],km_phytoplankton[0],km_zoo[0],
            k1_phytoplankton[0],k2_phytoplankton[0],
            k1_zoo[0],k2_zoo[0],kd_zoo[0],ke_zoo[0],k1_beninv[0],k2_beninv[0],kd_beninv[0],ke_beninv[0],km_beninv[0],
            k1_ff[0],k2_ff[0],kd_ff[0],ke_ff[0],km_ff[0],k1_sf[0],k2_sf[0],kd_sf[0],ke_sf[0],km_sf[0],k1_mf[0],k2_mf[0],kd_mf[0],ke_mf[0],km_mf[0],k1_lf[0],k2_lf[0],kd_lf[0],ke_lf[0],km_lf[0],
            rate_constants[0],s_respire[0],phyto_respire[0],zoo_respire[0],beninv_respire[0],ff_respire[0],sfish_respire[0],mfish_respire[0],lfish_respire[0]
            )

kabam_obj.chemical_name_exp=chemical_name[0]
kabam_obj.cb_phytoplankton_exp=cb_phytoplankton[0]
kabam_obj.cb_zoo_exp=cb_zoo[0]
kabam_obj.cb_beninv_exp=cb_beninv[0]
kabam_obj.cb_ff_exp=cb_ff[0]
kabam_obj.cb_sf_exp=cb_sf[0]
kabam_obj.cb_mf_exp=cb_mf[0]
kabam_obj.cb_lf_exp=cb_lf[0]
kabam_obj.cbl_phytoplankton_exp=cbl_phytoplankton[0]
kabam_obj.cbl_zoo_exp=cbl_zoo[0]
kabam_obj.cbl_beninv_exp=cbl_beninv[0]
kabam_obj.cbl_ff_exp=cbl_ff[0]
kabam_obj.cbl_sf_exp=cbl_sf[0]
kabam_obj.cbl_mf_exp=cbl_mf[0]
kabam_obj.cbl_lf_exp=cbl_lf[0]
kabam_obj.cbd_zoo_exp=cbd_zoo[0]
kabam_obj.cbd_beninv_exp=cbd_beninv[0]
kabam_obj.cbd_ff_exp=cbd_ff[0]
kabam_obj.cbd_sf_exp=cbd_sf[0]
kabam_obj.cbd_mf_exp=cbd_mf[0]
kabam_obj.cbd_lf_exp=cbd_lf[0]
kabam_obj.cbr_phytoplankton_exp=cbr_phytoplankton[0]
kabam_obj.cbr_zoo_exp=cbr_zoo[0]
kabam_obj.cbr_beninv_exp=cbr_beninv[0]
kabam_obj.cbr_ff_exp=cbr_ff[0]
kabam_obj.cbr_sf_exp=cbr_sf[0]
kabam_obj.cbr_mf_exp=cbr_mf[0]
kabam_obj.cbr_lf_exp=cbr_lf[0]
kabam_obj.cbf_phytoplankton_exp=cbf_phytoplankton[0]
kabam_obj.cbf_zoo_exp=cbf_zoo[0]
kabam_obj.cbf_beninv_exp=cbf_beninv[0]
kabam_obj.cbf_ff_exp=cbf_ff[0]
kabam_obj.cbf_sf_exp=cbf_sf[0]
kabam_obj.cbf_mf_exp=cbf_mf[0]
kabam_obj.cbf_lf_exp=cbf_lf[0]
kabam_obj.cbaf_phytoplankton_exp=cbaf_phytoplankton[0]
kabam_obj.cbaf_zoo_exp=cbaf_zoo[0]
kabam_obj.cbaf_beninv_exp=cbaf_beninv[0]
kabam_obj.cbaf_ff_exp=cbaf_ff[0]
kabam_obj.cbaf_sf_exp=cbaf_sf[0]
kabam_obj.cbaf_mf_exp=cbaf_mf[0]
kabam_obj.cbaf_lf_exp=cbaf_lf[0]
kabam_obj.cbfl_phytoplankton_exp=cbfl_phytoplankton[0]
kabam_obj.cbfl_zoo_exp=cbfl_zoo[0]
kabam_obj.cbfl_beninv_exp=cbfl_beninv[0]
kabam_obj.cbfl_ff_exp=cbfl_ff[0]
kabam_obj.cbfl_sf_exp=cbfl_sf[0]
kabam_obj.cbfl_mf_exp=cbfl_mf[0]
kabam_obj.cbfl_lf_exp=cbfl_lf[0]
kabam_obj.cbafl_phytoplankton_exp=cbafl_phytoplankton[0]
kabam_obj.cbafl_zoo_exp=cbafl_zoo[0]
kabam_obj.cbafl_beninv_exp=cbafl_beninv[0]
kabam_obj.cbafl_ff_exp=cbafl_ff[0]
kabam_obj.cbafl_sf_exp=cbafl_sf[0]
kabam_obj.cbafl_mf_exp=cbafl_mf[0]
kabam_obj.cbafl_lf_exp=cbafl_lf[0]
kabam_obj.bmf_zoo_exp=bmf_zoo[0]
kabam_obj.bmf_beninv_exp=bmf_beninv[0]
kabam_obj.bmf_ff_exp=bmf_ff[0]
kabam_obj.bmf_sf_exp=bmf_sf[0]
kabam_obj.cbmf_mf_exp=cbmf_mf[0]
kabam_obj.cbmf_lf_exp=cbmf_lf[0]
kabam_obj.cbsafl_phytoplankton_exp=cbsafl_phytoplankton[0]
kabam_obj.cbsafl_zoo_exp=cbsafl_zoo[0]
kabam_obj.cbsafl_beninv_exp=cbsafl_beninv[0]
kabam_obj.cbsafl_ff_exp=cbsafl_ff[0]
kabam_obj.cbsafl_sf_exp=cbsafl_sf[0]
kabam_obj.cbsafl_mf_exp=cbsafl_mf[0]
kabam_obj.cbsafl_lf_exp=cbsafl_lf[0]
kabam_obj.mweight0_exp=mweight0[0]
kabam_obj.mweight1_exp=mweight1[0]
kabam_obj.mweight2_exp=mweight2[0]
kabam_obj.mweight3_exp=mweight3[0]
kabam_obj.mweight4_exp=mweight4[0]
kabam_obj.mweight5_exp=mweight5[0]
kabam_obj.aweight0_exp=aweight0[0]
kabam_obj.aweight1_exp=aweight1[0]
kabam_obj.aweight2_exp=aweight2[0]
kabam_obj.aweight3_exp=aweight3[0]
kabam_obj.aweight4_exp=aweight4[0]
kabam_obj.aweight5_exp=aweight5[0]
kabam_obj.dfir0_exp=dfir0[0]
kabam_obj.dfir1_exp=dfir1[0]
kabam_obj.dfir2_exp=dfir2[0]
kabam_obj.dfir3_exp=dfir3[0]
kabam_obj.dfir4_exp=dfir4[0]
kabam_obj.dfir5_exp=dfir5[0]
kabam_obj.dfira0_exp=dfira0[0]
kabam_obj.dfira1_exp=dfira1[0]
kabam_obj.dfira2_exp=dfira2[0]
kabam_obj.dfira3_exp=dfira3[0]
kabam_obj.dfira4_exp=dfira4[0]
kabam_obj.dfira5_exp=dfira5[0]
kabam_obj.wet_food_ingestion_m0_exp=wet_food_ingestion_m0[0]
kabam_obj.wet_food_ingestion_m1_exp=wet_food_ingestion_m1[0]
kabam_obj.wet_food_ingestion_m2_exp=wet_food_ingestion_m2[0]
kabam_obj.wet_food_ingestion_m3_exp=wet_food_ingestion_m3[0]
kabam_obj.wet_food_ingestion_m4_exp=wet_food_ingestion_m4[0]
kabam_obj.wet_food_ingestion_m5_exp=wet_food_ingestion_m5[0]
kabam_obj.wet_food_ingestion_a0_exp=wet_food_ingestion_a0[0]
kabam_obj.wet_food_ingestion_a1_exp=wet_food_ingestion_a1[0]
kabam_obj.wet_food_ingestion_a2_exp=wet_food_ingestion_a2[0]
kabam_obj.wet_food_ingestion_a3_exp=wet_food_ingestion_a3[0]
kabam_obj.wet_food_ingestion_a4_exp=wet_food_ingestion_a4[0]
kabam_obj.wet_food_ingestion_a5_exp=wet_food_ingestion_a5[0]
kabam_obj.drinking_water_intake_m0_exp=drinking_water_intake_m0[0]
kabam_obj.drinking_water_intake_m1_exp=drinking_water_intake_m1[0]
kabam_obj.drinking_water_intake_m2_exp=drinking_water_intake_m2[0]
kabam_obj.drinking_water_intake_m3_exp=drinking_water_intake_m3[0]
kabam_obj.drinking_water_intake_m4_exp=drinking_water_intake_m4[0]
kabam_obj.drinking_water_intake_m5_exp=drinking_water_intake_m5[0]
kabam_obj.drinking_water_intake_a0_exp=drinking_water_intake_a0[0]
kabam_obj.drinking_water_intake_a1_exp=drinking_water_intake_a1[0]
kabam_obj.drinking_water_intake_a2_exp=drinking_water_intake_a2[0]
kabam_obj.drinking_water_intake_a3_exp=drinking_water_intake_a3[0]
kabam_obj.drinking_water_intake_a4_exp=drinking_water_intake_a4[0]
kabam_obj.drinking_water_intake_a5_exp=drinking_water_intake_a5[0]
kabam_obj.db40_exp=db40[0]
kabam_obj.db41_exp=db41[0]
kabam_obj.db42_exp=db42[0]
kabam_obj.db43_exp=db43[0]
kabam_obj.db44_exp=db44[0]
kabam_obj.db45_exp=db45[0]
kabam_obj.db4a0_exp=db4a0[0]
kabam_obj.db4a1_exp=db4a1[0]
kabam_obj.db4a2_exp=db4a2[0]
kabam_obj.db4a3_exp=db4a3[0]
kabam_obj.db4a4_exp=db4a4[0]
kabam_obj.db4a5_exp=db4a5[0]
kabam_obj.db50_exp=db50[0]
kabam_obj.db51_exp=db51[0]
kabam_obj.db52_exp=db52[0]
kabam_obj.db53_exp=db53[0]
kabam_obj.db54_exp=db54[0]
kabam_obj.db55_exp=db55[0]
kabam_obj.db5a0_exp=db5a0[0]
kabam_obj.db5a1_exp=db5a1[0]
kabam_obj.db5a2_exp=db5a2[0]
kabam_obj.db5a3_exp=db5a3[0]
kabam_obj.db5a4_exp=db5a4[0]
kabam_obj.db5a5_exp=db5a5[0]
kabam_obj.acute_dose_based_m0_exp=acute_dose_based_m0[0]
kabam_obj.acute_dose_based_m1_exp=acute_dose_based_m1[0]
kabam_obj.acute_dose_based_m2_exp=acute_dose_based_m2[0]
kabam_obj.acute_dose_based_m3_exp=acute_dose_based_m3[0]
kabam_obj.acute_dose_based_m4_exp=acute_dose_based_m4[0]
kabam_obj.acute_dose_based_m5_exp=acute_dose_based_m5[0]
kabam_obj.acute_dose_based_a0_exp=acute_dose_based_a0[0]
kabam_obj.acute_dose_based_a1_exp=acute_dose_based_a1[0]
kabam_obj.acute_dose_based_a2_exp=acute_dose_based_a2[0]
kabam_obj.acute_dose_based_a3_exp=acute_dose_based_a3[0]
kabam_obj.acute_dose_based_a4_exp=acute_dose_based_a4[0]
kabam_obj.acute_dose_based_a5_exp=acute_dose_based_a5[0]
kabam_obj.avian_lc50_exp=avian_lc50[0]
kabam_obj.chronic_dose_based_m0_exp=chronic_dose_based_m0[0]
kabam_obj.chronic_dose_based_m1_exp=chronic_dose_based_m1[0]
kabam_obj.chronic_dose_based_m2_exp=chronic_dose_based_m2[0]
kabam_obj.chronic_dose_based_m3_exp=chronic_dose_based_m3[0]
kabam_obj.chronic_dose_based_m4_exp=chronic_dose_based_m4[0]
kabam_obj.chronic_dose_based_m5_exp=chronic_dose_based_m5[0]
kabam_obj.mammalian_chronic_endpoint_exp=mammalian_chronic_endpoint[0]
kabam_obj.avian_noaec_exp=avian_noaec[0]
kabam_obj.acute_rq_dose_m0_exp=acute_rq_dose_m0[0]
kabam_obj.acute_rq_dose_m1_exp=acute_rq_dose_m1[0]
kabam_obj.acute_rq_dose_m2_exp=acute_rq_dose_m2[0]
kabam_obj.acute_rq_dose_m3_exp=acute_rq_dose_m3[0]
kabam_obj.acute_rq_dose_m4_exp=acute_rq_dose_m4[0]
kabam_obj.acute_rq_dose_m5_exp=acute_rq_dose_m5[0]
kabam_obj.acute_rq_dose_a0_exp=acute_rq_dose_a0[0]
kabam_obj.acute_rq_dose_a1_exp=acute_rq_dose_a1[0]
kabam_obj.acute_rq_dose_a2_exp=acute_rq_dose_a2[0]
kabam_obj.acute_rq_dose_a3_exp=acute_rq_dose_a3[0]
kabam_obj.acute_rq_dose_a4_exp=acute_rq_dose_a4[0]
kabam_obj.acute_rq_dose_a5_exp=acute_rq_dose_a5[0]
kabam_obj.acute_rq_diet_a0_exp=acute_rq_diet_a0[0]
kabam_obj.acute_rq_diet_a1_exp=acute_rq_diet_a1[0]
kabam_obj.acute_rq_diet_a2_exp=acute_rq_diet_a2[0]
kabam_obj.acute_rq_diet_a3_exp=acute_rq_diet_a3[0]
kabam_obj.acute_rq_diet_a4_exp=acute_rq_diet_a4[0]
kabam_obj.acute_rq_diet_a5_exp=acute_rq_diet_a5[0]
kabam_obj.chronic_rq_dose_m0_exp=chronic_rq_dose_m0[0]
kabam_obj.chronic_rq_dose_m1_exp=chronic_rq_dose_m1[0]
kabam_obj.chronic_rq_dose_m2_exp=chronic_rq_dose_m2[0]
kabam_obj.chronic_rq_dose_m3_exp=chronic_rq_dose_m3[0]
kabam_obj.chronic_rq_dose_m4_exp=chronic_rq_dose_m4[0]
kabam_obj.chronic_rq_dose_m5_exp=chronic_rq_dose_m5[0]
kabam_obj.chronic_rq_diet_m0_exp=chronic_rq_diet_m0[0]
kabam_obj.chronic_rq_diet_m1_exp=chronic_rq_diet_m1[0]
kabam_obj.chronic_rq_diet_m2_exp=chronic_rq_diet_m2[0]
kabam_obj.chronic_rq_diet_m3_exp=chronic_rq_diet_m3[0]
kabam_obj.chronic_rq_diet_m4_exp=chronic_rq_diet_m4[0]
kabam_obj.chronic_rq_diet_m5_exp=chronic_rq_diet_m5[0]
kabam_obj.chronic_rq_diet_a0_exp=chronic_rq_diet_a0[0]
kabam_obj.chronic_rq_diet_a1_exp=chronic_rq_diet_a1[0]
kabam_obj.chronic_rq_diet_a2_exp=chronic_rq_diet_a2[0]
kabam_obj.chronic_rq_diet_a3_exp=chronic_rq_diet_a3[0]
kabam_obj.chronic_rq_diet_a4_exp=chronic_rq_diet_a4[0]
kabam_obj.chronic_rq_diet_a5_exp=chronic_rq_diet_a5[0]

class kabamQaqcPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie, "Kabam QA/QC")
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'kabam','page':'qaqc'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'kabam',
                'model_attributes':'Kabam QAQC'})
        #html = html + kabam_tables.timestamp()
        html = html + kabam_tables.table_all_qaqc(kabam_obj)
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', kabamQaqcPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
