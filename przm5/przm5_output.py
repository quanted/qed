# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from uber import uber_lib
import cgi
import cgitb
from przm5 import przm5_model

import logging
logger = logging.getLogger('PRZM5 Model')


class przm5OutputPage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        args={}
        for key in form:
            args[key] = form.getvalue(key)
        przm5_obj = przm5_model.przm5(args)
        logger.info(vars(przm5_obj))
        templatepath = os.path.dirname(__file__) + '/../templates/'
        ChkCookie = self.request.cookies.get("ubercookie")
        html = uber_lib.SkinChk(ChkCookie)    
        html = html + template.render (templatepath + 'przm5-output-jqplot.html', {})                               
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'przm5','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'przm5', 
                'model_attributes':'PRZM 5 Output'})
        html = html + template.render (templatepath + 'przm5-jquery-output.html', {})
        html = html + """<H3 class="out_3 collapsible" id="section1"><span></span>User Inputs</H3>
                            <div class="out_input_table">"""


        html = html + """
                        <H3 class="out_3 collapsible" id="section1"><span></span>User Outputs</H3>
                        <div class="out_3">
                            <H4 class="out_1 collapsible" id="section1"><span></span>Download</H4>
                                <div class="out_ container_output">
                                    <table class="out_">
                                        <tr>
                                            <th scope="col">Outputs</div></th>
                                            <th scope="col">Value</div></th>                            
                                        </tr>
                                        <tr>
                                            <td>Simulation is finished. Please download your file from here</td>
                                            <td><a href=%s>Link</a></td>
                                        </tr>
                                    </table>
                                </div>
                        </div>
                            """%(przm5_obj.link)
        html = html + """
                        <H4 class="out_4 collapsible" id="section1" style="display: none"><span></span>Plot</H4>
                            <div class="out_4 container_output">
                                <table class="out_" style="display: none">
                                    <tr>
                                        <td id="x_pre_irr">pre+irr</td>
                                        <td id="x_pre_irr_val_%s">%s</td>
                                    </tr>
                                    <tr>
                                        <td id="x_et">et</td>
                                        <td id="x_et_val_%s">%s</td>
                                    </tr>
                                    <tr>
                                        <td id="x_runoff">runoff</td>
                                        <td id="x_runoff_val_%s">%s</td>
                                    </tr>                          
                                </table>
                            </div>"""%(1, przm5_obj.PRCP_IRRG_sum, 1, przm5_obj.CEVP_TETD_sum, 1, przm5_obj.RUNF_sum)
        html = html + """
                        <H3 class="out_3 collapsible" id="section1"><span></span>Plots</H3>
                            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                                <div id="chart1" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
                            <H4 class="out_4 collapsible" id="section1"><span></span></H4>
                                <div id="chart2" style="margin-top:20px; margin-left:20px; width:600px; height:400px;"></div>
                        """

        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', przm5OutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    

