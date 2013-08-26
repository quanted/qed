# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import math 
import cgi
import cgitb
cgitb.enable()
from resexposure import resexposure_model
from resexposure import resexposure_tables


class resexposureOutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage()
        model = form.getvalue('model')
        all_obj = {}

        if 'tab_hdflr' in model:
            ar_hd = float(form.getvalue('ar_hd'))
            ai_hd = float(form.getvalue('ai_hd'))/100
            den_hd = float(form.getvalue('den_hd'))
            cf1_hd = float(form.getvalue('cf1_hd'))
            cf2_hd = float(form.getvalue('cf2_hd'))
            fr_hd = float(form.getvalue('fr_hd'))
            tf_hd = float(form.getvalue('tf_hd'))
            sa_hd = float(form.getvalue('sa_hd'))
            da_hd = float(form.getvalue('da_hd'))/100
            bw_hd = float(form.getvalue('bw_hd'))
            sa_h_hd = float(form.getvalue('sa_h_hd'))
            fq_hd = float(form.getvalue('fq_hd'))
            et_hd = float(form.getvalue('et_hd'))
            se_hd = float(form.getvalue('se_hd'))/100
            hd_obj = resexposure_model.resexposure_hd(ar_hd, ai_hd, den_hd, cf1_hd, cf2_hd, fr_hd, tf_hd, sa_hd, da_hd, bw_hd, sa_h_hd, fq_hd, et_hd, se_hd)
            all_obj['tab_hdflr'] = hd_obj

        if 'tab_vlflr' in model:
            wf_vl = float(form.getvalue('wf_vl'))/100
            den_vl = float(form.getvalue('den_vl'))
            vt_vl = float(form.getvalue('vt_vl'))
            cf1_vl = float(form.getvalue('cf1_vl'))
            af_vl = float(form.getvalue('af_vl'))/100
            tf_vl = float(form.getvalue('tf_vl'))/100
            cf2_vl = float(form.getvalue('cf2_vl'))
            bw_vl = float(form.getvalue('bw_vl'))
            sa_vl = float(form.getvalue('sa_vl'))
            da_vl = float(form.getvalue('da_vl'))/100
            sa_h_vl = float(form.getvalue('sa_h_vl'))
            fq_vl = float(form.getvalue('fq_vl'))
            et_vl = float(form.getvalue('et_vl'))
            se_vl = float(form.getvalue('se_vl'))/100
            vl_obj = resexposure_model.resexposure_vl(wf_vl, den_vl, vt_vl, cf1_vl, af_vl, tf_vl, cf2_vl, bw_vl, sa_vl, da_vl, sa_h_vl, fq_vl, et_vl, se_vl)
            all_obj['tab_vlflr'] = vl_obj

        if 'tab_cpcln' in model:
            ar_cc = float(form.getvalue('ar_cc'))
            ai_cc = float(form.getvalue('ai_cc'))/100
            den_cc = float(form.getvalue('den_cc'))
            cf1_cc = float(form.getvalue('cf1_cc'))
            cf2_cc = float(form.getvalue('cf2_cc'))
            fr_cc = float(form.getvalue('fr_cc'))
            tf_cc = float(form.getvalue('tf_cc'))
            bw_cc = float(form.getvalue('bw_cc'))
            sa_cc = float(form.getvalue('sa_cc'))
            da_cc = float(form.getvalue('da_cc'))/100
            sa_h_cc = float(form.getvalue('sa_h_cc'))
            fq_cc = float(form.getvalue('fq_cc'))
            et_cc = float(form.getvalue('et_cc'))
            se_cc = float(form.getvalue('se_cc'))/100
            cc_obj = resexposure_model.resexposure_cc(ar_cc, ai_cc, den_cc, cf1_cc, cf2_cc, fr_cc, tf_cc, sa_cc, da_cc, bw_cc, sa_h_cc, fq_cc, et_cc, se_cc)
            all_obj['tab_cpcln'] = cc_obj

        if 'tab_ipcap' in model:
            den_ic = float(form.getvalue('den_ic'))
            wf_ic = float(form.getvalue('wf_ic'))
            tf_ic = float(form.getvalue('tf_ic'))
            bw_ic = float(form.getvalue('bw_ic'))
            sa_ic = float(form.getvalue('sa_ic'))
            da_ic = float(form.getvalue('da_ic'))/100
            sa_h_ic = float(form.getvalue('sa_h_ic'))
            fq_ic = float(form.getvalue('fq_ic'))
            et_ic = float(form.getvalue('et_ic'))
            se_ic = float(form.getvalue('se_ic'))/100
            ic_obj = resexposure_model.resexposure_ic(den_ic, wf_ic, tf_ic, bw_ic, sa_ic, da_ic, sa_h_ic, fq_ic, et_ic, se_ic)
            all_obj['tab_ipcap'] = ic_obj

        if 'tab_mactk' in model:
            wf_mt = float(form.getvalue('wf_mt'))/100
            den_mt = float(form.getvalue('den_mt'))
            tf_mt = float(form.getvalue('tf_mt'))/100
            bw_mt = float(form.getvalue('bw_mt'))
            pf_mt = float(form.getvalue('pf_mt'))/100
            sa_mt = float(form.getvalue('sa_mt'))
            da_mt = float(form.getvalue('da_mt'))/100
            mt_obj = resexposure_model.resexposure_mt(wf_mt, den_mt, tf_mt, bw_mt, pf_mt, sa_mt, da_mt)
            all_obj['tab_mactk'] = mt_obj

        if 'tab_ccpst' in model:
            wa_ct = float(form.getvalue('wa_ct'))
            wf_ct = float(form.getvalue('wf_ct'))/100
            bw_ct = float(form.getvalue('bw_ct'))
            tf_ct = float(form.getvalue('tf_ct'))/100
            sa_ct = float(form.getvalue('sa_ct'))
            da_ct = float(form.getvalue('da_ct'))/100
            sa_m_ct = float(form.getvalue('sa_m_ct'))
            se_ct = float(form.getvalue('se_ct'))/100
            ct_obj = resexposure_model.resexposure_ct(wa_ct, wf_ct, bw_ct, tf_ct, sa_ct, da_ct, sa_m_ct, se_ct)
            all_obj['tab_ccpst'] = ct_obj

        if 'tab_ldtpr' in model:
            ap_lp = float(form.getvalue('ap_lp'))
            wf_lp = float(form.getvalue('wf_lp'))/100
            den_lp = float(form.getvalue('den_lp'))
            wfd_lp = float(form.getvalue('wfd_lp'))/100
            tw_lp = float(form.getvalue('tw_lp'))
            bw_lp = float(form.getvalue('bw_lp'))
            sa_lp = float(form.getvalue('sa_lp'))
            tf_cs_lp = float(form.getvalue('tf_cs_lp'))/100
            tf_r_lp = float(form.getvalue('tf_r_lp'))/100
            da_lp = float(form.getvalue('da_lp'))/100
            sa_m_lp = float(form.getvalue('sa_m_lp'))
            se_lp = float(form.getvalue('se_lp'))/100
            lp_obj = resexposure_model.resexposure_lp(ap_lp, wf_lp, den_lp, wfd_lp, tw_lp, bw_lp, sa_lp, tf_cs_lp, tf_r_lp, da_lp, sa_m_lp, se_lp)
            all_obj['tab_ldtpr'] = lp_obj

        if 'tab_clopr' in model:
            den_cp = float(form.getvalue('den_cp'))
            wf_cp = float(form.getvalue('wf_cp'))/100
            bw_cp = float(form.getvalue('bw_cp'))
            tf_cs_cp = float(form.getvalue('tf_cs_cp'))/100
            sa_cp = float(form.getvalue('sa_cp'))
            da_cp = float(form.getvalue('da_cp'))/100
            sa_m_cp = float(form.getvalue('sa_m_cp'))
            se_cp = float(form.getvalue('se_cp'))/100
            cp_obj = resexposure_model.resexposure_cp(den_cp, wf_cp, bw_cp, tf_cs_cp, sa_cp, da_cp, sa_m_cp, se_cp)
            all_obj['tab_clopr'] = cp_obj

        if 'tab_impdp' in model:
            am_id = float(form.getvalue('am_id'))
            wf_id = float(form.getvalue('wf_id'))/100
            tf_id = float(form.getvalue('tf_id'))/100
            fq_id = float(form.getvalue('fq_id'))
            da_id = float(form.getvalue('da_id'))/100
            bw_id = float(form.getvalue('bw_id'))
            id_obj = resexposure_model.resexposure_id(am_id, wf_id, tf_id, fq_id, da_id, bw_id)
            all_obj['tab_impdp'] = id_obj

        if 'tab_cldst' in model:
            ar_sd = float(form.getvalue('ar_sd'))
            wf_sd = float(form.getvalue('wf_sd'))/100
            tf_sd = float(form.getvalue('tf_sd'))/100
            sa_sd = float(form.getvalue('sa_sd'))
            fq_sd = float(form.getvalue('fq_sd'))
            da_sd = float(form.getvalue('da_sd'))/100
            bw_sd = float(form.getvalue('bw_sd'))
            sd_obj = resexposure_model.resexposure_sd(ar_sd, wf_sd, tf_sd, sa_sd, fq_sd, da_sd, bw_sd)
            all_obj['tab_cldst'] = sd_obj

        if 'tab_impty' in model:
            wf_ip = float(form.getvalue('wf_ip'))/100
            wt_ip = float(form.getvalue('wt_ip'))
            fr_sa_ip = float(form.getvalue('fr_sa_ip'))/100
            sa_ip = float(form.getvalue('sa_ip'))
            sa_m_ip  = float(form.getvalue('sa_m_ip'))
            se_ip = float(form.getvalue('se_ip'))/100
            bw_ip = float(form.getvalue('bw_ip'))
            ip_obj = resexposure_model.resexposure_ip(wf_ip, wt_ip, fr_sa_ip, sa_ip, sa_m_ip, se_ip, bw_ip)
            all_obj['tab_impty'] = ip_obj




        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02hh_uberintroblock_wmodellinks.html',  {'model':'resexposure','page':'output'})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'resexposure', 
                'model_attributes':'Residential Exposure Model Output'})

        html = html + resexposure_tables.table_all(model, all_obj)

        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', resexposureOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    