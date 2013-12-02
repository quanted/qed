import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from uber import uber_lib
from przm5 import przm5_parameters
import logging
logger = logging.getLogger('PRZM5 Model')

class przm5InputPage(webapp.RequestHandler):
    def get(self):
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)
        html = html + template.render (templatepath + 'przm5-jquery.html', {})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'przm5','page':'input'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start_tabbed.html', {
                'model':'przm5', 
                'model_attributes':'PRZM 5 Inputs'})
        html = html + """
        <div class="input_nav">
            <ul>
                <li class="Chemical tabSel">Chemical </li>
                |<li class="Applications tabUnsel"> Applications </li>
                |<li class="CropLand tabUnsel"> Crop/Land </li>
                |<li class="Runoff tabUnsel"> Runoff </li>
            </ul>
        </div>
        """
        html = html + """<br><table class="tab tab_Chemical" border="0">"""
        html = html + str(przm5_parameters.przm5Inp_chem())
        html = html + """</table><table class="tab tab_Chemical deg" border="0" style="display:none">
                                    <tr class="deg1"><th><label for="id_Koc_1">Sorption Coefficient 1 (mL/g):</label></th><td><input type="text" name="Koc_1" value="200" id="id_Koc_1" /></td></tr>
                                    <tr class="deg1"><th><label for="id_soilHalfLife_1">Soil Halflife 1 (day):</label></th><td><input type="text" name="soilHalfLife_1" value="100" id="id_soilHalfLife_1" /></td></tr>
                                    <tr class="deg1"><th><label for="id_foliarHalfLife_1">Foliar Halflife 1 (day):</label></th><td><input type="text" name="foliarHalfLife_1" value="44" id="id_foliarHalfLife_1" /></td></tr>
                                    <tr class="deg1"><th><label for="id_convert_Foliar1">Foliar Molar Conversion Factor:</label></th><td><input type="text" name="convert_Foliar1" value="0.82" id="id_convert_Foliar1" /></td></tr>
                                    <tr class="deg1"><th><label for="id_convertSoil1">Soil Molar Conversion Factor:</label></th><td><input type="text" name="convertSoil1" value="0.70" id="id_convertSoil1" /></td></tr>
                                    <tr class="deg2"><th><label for="id_Koc_2">Sorption Coefficient 2 (mL/g):</label></th><td><input type="text" name="Koc_2" value="200" id="id_Koc_2" /></td></tr>
                                    <tr class="deg2"><th><label for="id_soilHalfLife_2">Soil Halflife 2 (day):</label></th><td><input type="text" name="soilHalfLife_2" value="100" id="id_soilHalfLife_2" /></td></tr>
                                    <tr class="deg2"><th><label for="id_foliarHalfLife_2">Foliar Halflife 2 (day):</label></th><td><input type="text" name="foliarHalfLife_2" value="44" id="id_foliarHalfLife_2" /></td></tr>
                                    <tr class="deg2"><th><label for="id_deg2_source">Source of Degradate 2:</label></th><td><select name="deg2_source" id="id_deg2_source"><option value="0">Degradate 1</option><option value="1">Parent</option></select></td></tr>
                                    <tr class="deg2"><th><label for="id_convertSoil2">Soil Molar Conversion Factor (Degradate 2):</label></th><td><input type="text" name="convertSoil2" value="0.80" id="id_convertSoil2" /></td></tr>
                                </table>"""

        html = html + """</table><table class="tab tab_Applications" border="0" style="display:none">"""
        html = html + str(przm5_parameters.przm5Inp_appl())
        html = html + """</table><table class="tab tab_Applications tab_noa" border="0" style="display:none">
                                    <tr><th colspan="5" scope="col"><label for="id_noa">No. of Applications:</label></th>
                                        <td colspan="1" scope="col"><select name="noa" id="id_noa">
                                            <option value="1">1</option><option value="2" selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26">26</option><option value="27">27</option><option value="28">28</option><option value="29">29</option><option value="30">30</option></select>
                                        </td>
                                    </tr>
                                    <tr id="not_header">
                                        <th width="18%" id="rela_a_head" class="rela">Days Since Emergence</th>
                                        <th width="18%" id="day_head" class="abs">Day</th>
                                        <th width="18%" id="mon_head" class="abs">Month</th>
                                        <th width="18%" id="a_head">Amount (kg/hA)</th>
                                        <th width="18%" id="cam_head">Application method</th>
                                        <th width="18%" id="d_head">Depth</th>
                                        <th width="18%" id="e_head">Eff.</th>
                                        <th width="18%" id="d_head">Drift/T</th>
                                    </tr>""" 

        html = html + """</table><table class="tab tab_CropLand" border="0" style="display:none">"""
        html = html + str(przm5_parameters.przm5Inp_cropland())
        html = html + """</table><table class="tab tab_CropLand tab_noh" border="0" style="display:none">
                                    <tr><th colspan="2" scope="col"><label for="id_noh">No. of Horizons:</label></th>
                                        <td colspan="1" scope="col"><select name="noh" id="id_noh">
                                            <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5" selected>5</option><option value="6">6</option><option value="7">7</option>
                                        </td>
                                        <th colspan="3"><label><input type="checkbox" name="tempflag_check" id="id_tempflag_check", value=1> Simulate Temperature</label></th>
                                    </tr>
                                    <tr class="tempflag">
                                        <th colspan="4"><label for="id_bcTemp">Lower BC Temperature:</label></th>
                                        <td colspan="3"><input type="text" name="bcTemp" value="23" id="id_bcTemp" /></td>
                                    </tr>
                                    <tr class="tempflag">
                                        <th colspan="4"><label for="id_albedo">Albedo:</label></th>
                                        <td colspan="3"><input type="text" name="albedo" value="0.4" id="id_albedo" /></td>
                                    </tr>
                                    <tr id="not_header">
                                        <th width="18%" id="thick_head">Thick</th>
                                        <th width="18%" id="rho_head">&#961;</th>
                                        <th width="18%" id="max_head">Max. Cap.</th>
                                        <th width="18%" id="min_head">Min. Cap.</th>
                                        <th width="18%" id="oc_head">O.C.</th>
                                        <th width="18%" id="n_head">N</th>
                                        <th width="18%" id="s_head" class="tempflag">Sand</th>
                                        <th width="18%" id="c_head" class="tempflag">Clay</th>
                                    </tr>""" 

        html = html + """</table><table class="tab tab_Runoff" border="0" style="display:none">"""
        html = html + str(przm5_parameters.przm5Inp_runoff())
        html = html + """</table><table class="tab tab_Runoff tab_nott" border="0" style="display:none">
                                    <tr><th colspan="3" scope="col"><label for="id_nott">No. of Time-Varing Factors:</label></th>
                                        <td colspan="1" scope="col"><select name="nott" id="id_nott">
                                            <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option><option value="23">23</option><option value="24">24</option><option value="25">25</option><option value="26" selected>26</option><option value="27">27</option><option value="28">28</option><option value="29">29</option><option value="30">30</option></select>
                                        </td>
                                        <th colspan="2"><label><input type="checkbox" name="sp_year" id="id_sp_year", value=1> Specify year</label></th>
                                    </tr>
                                    <tr id="not_header">
                                        <th style="width:6px;" >No.</th>
                                        <th style="width:6px;" id="day_head">Day</th>
                                        <th style="width:6px;" id="mon_head">Month</th>
                                        <th style="width:6px;" id="CN_head">CN</th>
                                        <th style="width:6px;" id="C_head">C</th>
                                        <th style="width:6px;" id="N_head">N</th>
                                        <th style="width:6px;" id="year_head" class="year_not">Year</th>
                                    </tr>""" 

        html = html + template.render(templatepath + '04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przm5InputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
