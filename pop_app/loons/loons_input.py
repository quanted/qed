import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import django
from django import forms
from loons import loons_parameters

class loons_InputPage(webapp.RequestHandler):
    def get(self):       
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'loons','page':'input'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberinput_start.html', {
                'model':'loons', 
                'model_attributes':'Loons Population Model'})

        html = html + str(loons_parameters.loonsinp())

        html = html + """<table class="leslie" border="0">
                            <tr>
                                <th>Age Class</th>
                                <th colspan=4>Leslie matrix</th>
                                <th>Initial Population</th>
                            </tr>
                            <tr>
                                <td>Juvenile Year 1</td>
                                <td name="l11" id="l11" type="text">0</td>
                                <td name="l12" id="l12" type="text">0</td>
                                <td name="l13" id="l13" type="text">0</td>
                                <td name="l14" id="l14" type="text"></td>
                                <td> <input name="no1" id="no1" type="text" value="4"></td>
                            </tr>
                            <tr>
                                <td>Juvenile Year 2</td>
                                <td name="l21" id="l21" type="text"></td>
                                <td name="l22" id="l22" type="text">0</td>
                                <td name="l23" id="l23" type="text">0</td>
                                <td name="l24" id="l24" type="text">0</td>
                                <td> <input name="no2" id="no2" type="text" value="2"></td>
                            </tr>
                            <tr>
                                <td>Juvenile Year 3</td>
                                <td name="l31" id="l31" type="text">0</td>
                                <td name="l32" id="l32" type="text"></td>
                                <td name="l33" id="l33" type="text">0</td>
                                <td name="l34" id="l34" type="text">0</td>
                                <td> <input name="no3" id="no3" type="text" value="1"></td>
                            </tr>
                            <tr>
                                <td>Adult</td>
                                <td name="l41" id="l41" type="text">0</td>
                                <td name="l42" id="l42" type="text">0</td>
                                <td name="l43" id="l43" type="text"></td>
                                <td name="l44" id="l44" type="text"></td>
                                <td> <input name="no4" id="no4" type="text" value="3"></td>
                            </tr>
                        </table>"""



        # html = html + """<table class="life_cycle" border="0">
        #                     <tr>
        #                         <th>Age Class</th>
        #                         <th colspan=2>Annual transition matrix</th>
        #                     </tr>
        #                     <tr>
        #                         <td>Juvenile</td>
        #                         <td input name="a11" id="a11" type="text"></td>
        #                         <td input name="a12" id="a12" type="text"></td>
        #                     </tr>
        #                     <tr>
        #                         <td>Adult</td>
        #                         <td input name="a21" id="a21" type="text"></td>
        #                         <td input name="a22" id="a22" type="text"></td>
        #                     </tr>
        #                 </table>"""


        html = html + template.render(templatepath + 'loons_input_jquery.html', {})
        html = html + template.render(templatepath + '04uberinput_end.html', {'sub_title': 'Submit'})
        html = html + template.render(templatepath + '05pop_ubertext_tooltips_right.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', loons_InputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
