# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
from StringIO import StringIO
import csv
import sys
sys.path.append("../resexposure")
from resexposure import resexposure_model, resexposure_tables
import logging

logger = logging.getLogger('resexposureBatchPage')


#inputs
run_hd = []
ar_hd = []
ai_hd = []
den_hd = []
cf1_hd = []
cf2_hd = []
fr_hd = []
tf_hd = []
sa_hd = []
da_hd = []
bw_hd = []
sa_h_hd = []
fq_hd = []
et_hd = []
se_hd = []

run_vl = []
wf_vl = []
den_vl = []
vt_vl = []
cf1_vl = []
af_vl = []
tf_vl = []
cf2_vl = []
bw_vl = []
sa_vl = []
da_vl = []
sa_h_vl = []
fq_vl = []
et_vl = []
se_vl = []

run_cc = []
ar_cc = []
ai_cc = []
den_cc = []
cf1_cc = []
cf2_cc = []
fr_cc = []
tf_cc = []
bw_cc = []
sa_cc = []
da_cc = []
sa_h_cc = []
fq_cc = []
et_cc = []
se_cc = []

run_ic = []
den_ic = []
wf_ic = []
tf_ic = []
bw_ic = []
sa_ic = []
da_ic = []
sa_h_ic = []
fq_ic = []
et_ic = []
se_ic = []

run_mt = []
wf_mt = []
den_mt = []
tf_mt = []
bw_mt = []
pf_mt = []
sa_mt = []
da_mt = []

run_ct = []
wa_ct = []
wf_ct = []
bw_ct = []
tf_ct = []
sa_ct = []
da_ct = []
sa_m_ct = []
se_ct = []

run_lp = []
ap_lp = []
wf_lp = []
den_lp = []
wfd_lp = []
tw_lp = []
bw_lp = []
sa_lp = []
tf_cs_lp = []
tf_r_lp = []
da_lp = []
sa_m_lp = []
se_lp = []

run_cp = []
den_cp = []
wf_cp = []
bw_cp = []
tf_cs_cp = []
sa_cp = []
da_cp = []
sa_m_cp = []
se_cp = []

run_id = []
am_id = []
wf_id = []
tf_id = []
fq_id = []
da_id = []
bw_id = []

run_sd = []
ar_sd = []
wf_sd = []
tf_sd = []
sa_sd = []
fq_sd = []
da_sd = []
bw_sd = []

run_ip = []
wf_ip = []
wt_ip = []
fr_sa_ip = []
sa_ip = []
sa_m_ip = []
se_ip = []
bw_ip = []

#outputs

def html_table(row, iter):
    all_obj_temp = {}
    model_temp = []
    run_hd_temp = float(row[0])
    run_hd.append(run_hd_temp)
    if run_hd_temp == 1:
        model_temp.append('tab_hdflr')
        ar_hd_temp = float(row[1])
        ar_hd.append(ar_hd_temp)
        ai_hd_temp = float(row[2])/100
        ai_hd.append(ai_hd_temp)
        den_hd_temp = float(row[3])
        den_hd.append(den_hd_temp)
        cf1_hd_temp = float(row[4])
        cf1_hd.append(cf1_hd_temp)
        cf2_hd_temp = float(row[5])
        cf2_hd.append(cf2_hd_temp)
        fr_hd_temp = float(row[6])
        fr_hd.append(fr_hd_temp)
        tf_hd_temp = float(row[7])
        tf_hd.append(tf_hd_temp)
        sa_hd_temp = float(row[8])
        sa_hd.append(sa_hd_temp)
        da_hd_temp = float(row[9])/100
        da_hd.append(da_hd_temp)
        bw_hd_temp = float(row[10])
        bw_hd.append(bw_hd_temp)
        sa_h_hd_temp = float(row[11])
        sa_h_hd.append(sa_h_hd_temp)
        fq_hd_temp = float(row[12])
        fq_hd.append(fq_hd_temp)
        et_hd_temp = float(row[13])
        et_hd.append(et_hd_temp)
        se_hd_temp = float(row[14])/100
        se_hd.append(se_hd_temp)
        hd_obj_temp = resexposure_model.resexposure_hd(ar_hd_temp, ai_hd_temp, den_hd_temp, cf1_hd_temp, cf2_hd_temp, fr_hd_temp, tf_hd_temp, sa_hd_temp, da_hd_temp, bw_hd_temp, sa_h_hd_temp, fq_hd_temp, et_hd_temp, se_hd_temp)
        all_obj_temp['tab_hdflr'] = hd_obj_temp

    run_vl_temp = float(row[15])
    run_vl.append(run_vl_temp)
    if run_vl_temp == 1:
        model_temp.append('tab_vlflr')
        wf_vl_temp = float(row[16])/100
        wf_vl.append(wf_vl_temp)
        den_vl_temp = float(row[17])
        den_vl.append(den_vl_temp)
        vt_vl_temp = float(row[18])
        vt_vl.append(vt_vl_temp)
        cf1_vl_temp = float(row[19])
        cf1_vl.append(cf1_vl_temp)
        af_vl_temp = float(row[20])/100
        af_vl.append(af_vl_temp)
        tf_vl_temp = float(row[21])/100
        tf_vl.append(tf_vl_temp)
        cf2_vl_temp = float(row[22])
        cf2_vl.append(cf2_vl_temp)
        bw_vl_temp = float(row[23])
        bw_vl.append(bw_vl_temp)
        sa_vl_temp = float(row[24])
        sa_vl.append(sa_vl_temp)
        da_vl_temp = float(row[25])/100
        da_vl.append(da_vl_temp)
        sa_h_vl_temp = float(row[26])
        sa_h_vl.append(sa_h_vl_temp)
        fq_vl_temp = float(row[27])
        fq_vl.append(fq_vl_temp)
        et_vl_temp = float(row[28])
        et_vl.append(et_vl_temp)
        se_vl_temp = float(row[29])/100
        se_vl.append(se_vl_temp)
        vl_obj_temp = resexposure_model.resexposure_vl(wf_vl_temp, den_vl_temp, vt_vl_temp, cf1_vl_temp, af_vl_temp, tf_vl_temp, cf2_vl_temp, bw_vl_temp, sa_vl_temp, da_vl_temp, sa_h_vl_temp, fq_vl_temp, et_vl_temp, se_vl_temp)
        all_obj_temp['tab_vlflr'] = vl_obj_temp

    run_cc_temp = float(row[30])
    run_cc.append(run_cc_temp)
    if run_cc_temp == 1:
        model_temp.append('tab_cpcln')
        ar_cc_temp = float(row[31])
        ar_cc.append(ar_cc_temp)
        ai_cc_temp = float(row[32])/100
        ai_cc.append(ai_cc_temp)
        den_cc_temp = float(row[33])
        den_cc.append(den_cc_temp)
        cf1_cc_temp = float(row[34])
        cf1_cc.append(cf1_cc_temp)
        cf2_cc_temp = float(row[35])
        cf2_cc.append(cf2_cc_temp)
        fr_cc_temp = float(row[36])
        fr_cc.append(fr_cc_temp)
        tf_cc_temp = float(row[37])
        tf_cc.append(tf_cc_temp)
        bw_cc_temp = float(row[38])
        bw_cc.append(bw_cc_temp)
        sa_cc_temp = float(row[39])
        sa_cc.append(sa_cc_temp)
        da_cc_temp = float(row[40])/100
        da_cc.append(da_cc_temp)
        sa_h_cc_temp = float(row[41])
        sa_h_cc.append(sa_h_cc_temp)
        fq_cc_temp = float(row[42])
        fq_cc.append(fq_cc_temp)
        et_cc_temp = float(row[43])
        et_cc.append(et_cc_temp)
        se_cc_temp = float(row[44])/100
        se_cc.append(se_cc_temp)
        cc_obj_temp = resexposure_model.resexposure_cc(ar_cc_temp, ai_cc_temp, den_cc_temp, cf1_cc_temp, cf2_cc_temp, fr_cc_temp, tf_cc_temp, sa_cc_temp, da_cc_temp, bw_cc_temp, sa_h_cc_temp, fq_cc_temp, et_cc_temp, se_cc_temp)
        all_obj_temp['tab_cpcln'] = cc_obj_temp

    run_ic_temp = float(row[45])
    run_ic.append(run_ic_temp)
    if run_ic_temp == 1:
        model_temp.append('tab_ipcap')
        den_ic_temp = float(row[46])
        den_ic.append(den_ic_temp)
        wf_ic_temp = float(row[47])
        wf_ic.append(wf_ic_temp)
        tf_ic_temp = float(row[48])
        tf_ic.append(tf_ic_temp)
        bw_ic_temp = float(row[49])
        bw_ic.append(bw_ic_temp)
        sa_ic_temp = float(row[50])
        sa_ic.append(sa_ic_temp)
        da_ic_temp = float(row[51])/100
        da_ic.append(da_ic_temp)
        sa_h_ic_temp = float(row[52])
        sa_h_ic.append(sa_h_ic_temp)
        fq_ic_temp = float(row[53])
        fq_ic.append(fq_ic_temp)
        et_ic_temp = float(row[54])
        et_ic.append(et_ic_temp)
        se_ic_temp = float(row[55])/100
        se_ic.append(se_ic_temp)
        ic_obj_temp = resexposure_model.resexposure_ic(den_ic_temp, wf_ic_temp, tf_ic_temp, bw_ic_temp, sa_ic_temp, da_ic_temp, sa_h_ic_temp, fq_ic_temp, et_ic_temp, se_ic_temp)
        all_obj_temp['tab_ipcap'] = ic_obj_temp

    run_mt_temp = float(row[56])
    run_mt.append(run_mt_temp)
    if run_mt_temp == 1:
        model_temp.append('tab_mactk')
        wf_mt_temp = float(row[57])/100
        wf_mt.append(wf_mt_temp)
        den_mt_temp = float(row[58])
        den_mt.append(den_mt_temp)
        tf_mt_temp = float(row[59])/100
        tf_mt.append(tf_mt_temp)
        bw_mt_temp = float(row[60])
        bw_mt.append(bw_mt_temp)
        pf_mt_temp = float(row[61])/100
        pf_mt.append(pf_mt_temp)
        sa_mt_temp = float(row[62])
        sa_mt.append(sa_mt_temp)
        da_mt_temp = float(row[63])/100
        da_mt.append(da_mt_temp)
        mt_obj_temp = resexposure_model.resexposure_mt(wf_mt_temp, den_mt_temp, tf_mt_temp, bw_mt_temp, pf_mt_temp, sa_mt_temp, da_mt_temp)
        all_obj_temp['tab_mactk'] = mt_obj_temp

    run_ct_temp = float(row[64])
    run_ct.append(run_ct_temp)
    if run_ct_temp == 1:
        model_temp.append('tab_ccpst')
        wa_ct_temp = float(row[65])
        wa_ct.append(wa_ct_temp)
        wf_ct_temp = float(row[66])/100
        wf_ct.append(wf_ct_temp)
        bw_ct_temp = float(row[67])
        bw_ct.append(bw_ct_temp)
        tf_ct_temp = float(row[68])/100
        tf_ct.append(tf_ct_temp)
        sa_ct_temp = float(row[69])
        sa_ct.append(sa_ct_temp)
        da_ct_temp = float(row[70])/100
        da_ct.append(da_ct_temp)
        sa_m_ct_temp = float(row[71])
        sa_m_ct.append(sa_m_ct_temp)
        se_ct_temp = float(row[72])/100
        se_ct.append(se_ct_temp)
        ct_obj_temp = resexposure_model.resexposure_ct(wa_ct_temp, wf_ct_temp, bw_ct_temp, tf_ct_temp, sa_ct_temp, da_ct_temp, sa_m_ct_temp, se_ct_temp)
        all_obj_temp['tab_ccpst'] = ct_obj_temp

    run_lp_temp = float(row[73])
    run_lp.append(run_lp_temp)
    if run_lp_temp == 1:
        model_temp.append('tab_ldtpr')
        ap_lp_temp = float(row[74])
        ap_lp.append(ap_lp_temp)
        wf_lp_temp = float(row[75])/100
        wf_lp.append(wf_lp_temp)
        den_lp_temp = float(row[76])
        den_lp.append(den_lp_temp)
        wfd_lp_temp = float(row[77])/100
        wfd_lp.append(wfd_lp_temp)
        tw_lp_temp = float(row[78])
        tw_lp.append(tw_lp_temp)
        bw_lp_temp = float(row[79])
        bw_lp.append(bw_lp_temp)
        sa_lp_temp = float(row[80])
        sa_lp.append(sa_lp_temp)
        tf_cs_lp_temp = float(row[81])/100
        tf_cs_lp.append(tf_cs_lp_temp)
        tf_r_lp_temp = float(row[82])/100
        tf_r_lp.append(tf_r_lp_temp)
        da_lp_temp = float(row[83])/100
        da_lp.append(da_lp_temp)
        sa_m_lp_temp = float(row[84])
        sa_m_lp.append(sa_m_lp_temp)
        se_lp_temp = float(row[85])/100
        se_lp.append(se_lp_temp)
        lp_obj_temp = resexposure_model.resexposure_lp(ap_lp_temp, wf_lp_temp, den_lp_temp, wfd_lp_temp, tw_lp_temp, bw_lp_temp, sa_lp_temp, tf_cs_lp_temp, tf_r_lp_temp, da_lp_temp, sa_m_lp_temp, se_lp_temp)
        all_obj_temp['tab_ldtpr'] = lp_obj_temp

    run_cp_temp = float(row[86])
    run_cp.append(run_cp_temp)
    if run_cp_temp == 1:
        model_temp.append('tab_clopr')
        den_cp_temp = float(row[87])
        den_cp.append(den_cp_temp)
        wf_cp_temp = float(row[88])/100
        wf_cp.append(wf_cp_temp)
        bw_cp_temp = float(row[89])
        bw_cp.append(bw_cp_temp)
        tf_cs_cp_temp = float(row[90])/100
        tf_cs_cp.append(tf_cs_cp_temp)
        sa_cp_temp = float(row[91])
        sa_cp.append(sa_cp_temp)
        da_cp_temp = float(row[92])/100
        da_cp.append(da_cp_temp)
        sa_m_cp_temp = float(row[93])
        sa_m_cp.append(sa_m_cp_temp)
        se_cp_temp = float(row[94])/100
        se_cp.append(se_cp_temp)
        cp_obj_temp = resexposure_model.resexposure_cp(den_cp_temp, wf_cp_temp, bw_cp_temp, tf_cs_cp_temp, sa_cp_temp, da_cp_temp, sa_m_cp_temp, se_cp_temp)
        all_obj_temp['tab_clopr'] = cp_obj_temp

    run_id_temp = float(row[95])
    run_id.append(run_id_temp)
    if run_id_temp == 1:
        model_temp.append('tab_impdp')
        am_id_temp = float(row[96])
        am_id.append(am_id_temp)
        wf_id_temp = float(row[97])/100
        wf_id.append(wf_id_temp)
        tf_id_temp = float(row[98])/100
        tf_id.append(tf_id_temp)
        fq_id_temp = float(row[99])
        fq_id.append(fq_id_temp)
        da_id_temp = float(row[100])/100
        da_id.append(da_id_temp)
        bw_id_temp = float(row[101])
        bw_id.append(bw_id_temp)
        id_obj_temp = resexposure_model.resexposure_id(am_id_temp, wf_id_temp, tf_id_temp, fq_id_temp, da_id_temp, bw_id_temp)
        all_obj_temp['tab_impdp'] = id_obj_temp

    run_sd_temp = float(row[102])
    run_sd.append(run_sd_temp)
    if run_sd_temp == 1:
        model_temp.append('tab_cldst')
        ar_sd_temp = float(row[103])
        ar_sd.append(ar_sd_temp)
        wf_sd_temp = float(row[104])/100
        wf_sd.append(wf_sd_temp)
        tf_sd_temp = float(row[105])/100
        tf_sd.append(tf_sd_temp)
        sa_sd_temp = float(row[106])
        sa_sd.append(sa_sd_temp)
        fq_sd_temp = float(row[107])
        fq_sd.append(fq_sd_temp)
        da_sd_temp = float(row[108])/100
        da_sd.append(da_sd_temp)
        bw_sd_temp = float(row[109])
        bw_sd.append(bw_sd_temp)
        sd_obj_temp = resexposure_model.resexposure_sd(ar_sd_temp, wf_sd_temp, tf_sd_temp, sa_sd_temp, fq_sd_temp, da_sd_temp, bw_sd_temp)
        all_obj_temp['tab_cldst'] = sd_obj_temp

    run_ip_temp = float(row[110])
    run_ip.append(run_ip_temp)
    if run_ip_temp == 1:
        model_temp.append('tab_impty')
        wf_ip_temp = float(row[111])/100
        wf_ip.append(wf_ip_temp)
        wt_ip_temp = float(row[112])
        wt_ip.append(wt_ip_temp)
        fr_sa_ip_temp = float(row[113])/100
        fr_sa_ip.append(fr_sa_ip_temp)
        sa_ip_temp = float(row[114])
        sa_ip.append(sa_ip_temp)
        sa_m_ip_temp = float(row[115])
        sa_m_ip.append(sa_m_ip_temp)
        se_ip_temp = float(row[116])/100
        se_ip.append(se_ip_temp)
        bw_ip_temp = float(row[117])
        bw_ip.append(bw_ip_temp)
        ip_obj_temp = resexposure_model.resexposure_ip(wf_ip_temp, wt_ip_temp, fr_sa_ip_temp, sa_ip_temp, sa_m_ip_temp, se_ip_temp, bw_ip_temp)
        all_obj_temp['tab_impty'] = ip_obj_temp


    Input_header="""<H3 class="out_0 collapsible" id="section0"><span></span>Batch Calculation of Iteration %s</H3>
                    <div class="out_">
                    """%(iter)
    table_all_out = resexposure_tables.table_all(model_temp, all_obj_temp)
    html_table_temp = Input_header + table_all_out + "</div><br>"

    return html_table_temp           
    
def loop_html(thefile):
    reader = csv.reader(thefile.file.read().splitlines())
    reader.next()
    reader.next()
    reader.next()
    i=1

    iter_html=""
    for row in reader:
        iter_html = iter_html +html_table(row,i)
        i=i+1


    return iter_html


              
class resexposureBatchOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        logger.info(form) 
        thefile = form['upfile']
        iter_html=loop_html(thefile)
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', 'title')
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html', {'model':'resexposure','page':'batchinput'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberbatch_start.html', {
                'model':'resexposure',
                'model_attributes':'Residential Exposure Batch Output'})
        # html = html + resexposure_tables.timestamp()
        html = html + iter_html
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', resexposureBatchOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
    

