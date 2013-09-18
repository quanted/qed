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
from geneec import geneec_model
from geneec import geneec_tables
import base64
import urllib
from google.appengine.api import urlfetch
import sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)
import keys_Picloud_S3

############Provide the key and connect to the picloud####################
api_key=keys_Picloud_S3.picloud_api_key
api_secretkey=keys_Picloud_S3.picloud_api_secretkey
base64string = base64.encodestring('%s:%s' % (api_key, api_secretkey))[:-1]
http_headers = {'Authorization' : 'Basic %s' % base64string}
###########################################################################

########call the function################# 
def get_jid(geneec_obj):

    url='https://api.picloud.com/r/3303/geneec_fortran_s1' 

    APPRAT = geneec_obj.application_rate
    APPNUM = geneec_obj.number_of_applications
    APSPAC = geneec_obj.interval_between_applications
    KOC = geneec_obj.Koc
    METHAF = geneec_obj.aerobic_soil_metabolism
    WETTED = json.dumps(geneec_obj.wet_in)
    METHOD = json.dumps(geneec_obj.application_method)
    AIRFLG = json.dumps(geneec_obj.aerial_size_dist)
    YLOCEN = geneec_obj.no_spray_drift
    GRNFLG = json.dumps(geneec_obj.ground_spray_type)
    GRSIZE = json.dumps(geneec_obj.spray_quality)
    ORCFLG = json.dumps(geneec_obj.airblast_type)
    INCORP = geneec_obj.incorporation_depth
    SOL = geneec_obj.solubility
    METHAP = geneec_obj.aerobic_aquatic_metabolism
    HYDHAP = geneec_obj.hydrolysis
    FOTHAP = geneec_obj.photolysis_aquatic_half_life

    data = urllib.urlencode({"APPRAT":APPRAT, "APPNUM":APPNUM, "APSPAC":APSPAC, "KOC":KOC, "METHAF":METHAF, "WETTED":WETTED,
                             "METHOD":METHOD, "AIRFLG":AIRFLG, "YLOCEN":YLOCEN, "GRNFLG":GRNFLG, "GRSIZE":GRSIZE,
                             "ORCFLG":ORCFLG, "INCORP":INCORP, "SOL":SOL, "METHAP":METHAP, "HYDHAP":HYDHAP, "FOTHAP":FOTHAP})
    
    response = urlfetch.fetch(url=url, payload=data, method=urlfetch.POST, headers=http_headers)    
    jid= json.loads(response.content)['jid']
    output_st = ''
    
    while output_st!="done":
        response_st = urlfetch.fetch(url='https://api.picloud.com/job/?jids=%s&field=status' %jid, headers=http_headers)
        output_st = json.loads(response_st.content)['info']['%s' %jid]['status']

    url_val = 'https://api.picloud.com/job/result/?jid='+str(jid)
    response_val = urlfetch.fetch(url=url_val, method=urlfetch.GET, headers=http_headers)
    output_val = json.loads(response_val.content)['result']
    return(jid, output_st, output_val)

#############################################

class GENEECOutputPage(webapp.RequestHandler):
    def post(self):     
        form = cgi.FieldStorage() 
        chem_name = form.getvalue('chemical_name')
        application_target = form.getvalue('application_target')
        application_rate = form.getvalue('application_rate')
        number_of_applications = form.getvalue('number_of_applications')
        interval_between_applications = form.getvalue('interval_between_applications')
        Koc = form.getvalue('Koc')  
        aerobic_soil_metabolism = form.getvalue('aerobic_soil_metabolism')   
        wet_in = form.getvalue('wet_in')              
        application_method = form.getvalue('application_method')
        #A1
        aerial_size_dist = form.getvalue('aerial_size_dist')
        #B1
        ground_spray_type = form.getvalue('ground_spray_type')                                          
        #C1
        airblast_type = form.getvalue('airblast_type')  
        #B2    
        spray_quality = form.getvalue('spray_quality')
        
        no_spray_drift = form.getvalue('no_spray_drift')    
        incorporation_depth = form.getvalue('incorporation_depth')   
        solubility = form.getvalue('solubility')
        aerobic_aquatic_metabolism = form.getvalue('aerobic_aquatic_metabolism')
        hydrolysis = form.getvalue('hydrolysis')
        photolysis_aquatic_half_life = form.getvalue('photolysis_aquatic_half_life')
        
        if (application_method=='a' or application_method=='c'):
            incorporation_depth=0
        if (application_method=='d'):
            no_spray_drift=0     
        if  aerobic_aquatic_metabolism>0:
            hydrolysis_label='NA'
        else:
            hydrolysis_label=hydrolysis
               
################label selection###################################                    
        if application_method=='a':
            application_method_label='Aerial Spray'
            if aerial_size_dist=='a':
               aerial_size_dist_label='Very Fine to Fine'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA' 
            elif aerial_size_dist=='b':
               aerial_size_dist_label='Fine to Medium (EFED Default)'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
            elif aerial_size_dist=='c':
               aerial_size_dist_label='Medium to Coarse'
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
            else:
               aerial_size_dist_label='Coarse to Very Coarse' 
               ground_spray_type_label='NA'
               spray_quality_label='NA'
               airblast_type_label='NA'
              
        elif application_method=='b':        
            application_method_label='Ground Spray'
            if ground_spray_type=='a':
                if spray_quality=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='Low Boom Ground Spray (20" or less)'
                    spray_quality_label='Fine (EFED Default)'
                    airblast_type_label='NA'
                else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='Low Boom Ground Spray (20" or less)'
                    spray_quality_label='Medium-Coarse'
                    airblast_type_label='NA'
            else:
                if spray_quality=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='High Boom Ground Spray (20-50"; EFED Default)'
                    spray_quality_label='Fine (EFED Default)'
                    airblast_type_label='NA'
                else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='High Boom Ground Spray (20-50"; EFED Default)'
                    spray_quality_label='Medium-Coarse'
                    airblast_type_label='NA'
        elif application_method=='c':
            application_method_label='Airblast Spray (Orchard & Vineyard)'
            if airblast_type=='a':
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='NA'
                    spray_quality_label='NA'
                    airblast_type_label='Orchards and Dormant Vineyards'
            else:
                    aerial_size_dist_label='NA' 
                    ground_spray_type_label='NA'
                    spray_quality_label='NA'
                    airblast_type_label='Foliated Vineyards'
        else:
            application_method_label='NA'
            aerial_size_dist_label='NA' 
            ground_spray_type_label='NA'
            spray_quality_label='NA'
            airblast_type_label='NA'
##########################################################################################                                        

        geneec_obj = geneec_model.geneec(chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life)
        
        # application_rate, number_of_applications, interval_between_applications, 
        #                   Koc, aerobic_soil_metabolism, wet_in, application_method, 
        #                   aerial_size_dist, no_spray_drift, ground_spray_type, spray_quality, airblast_type,
        #                   incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life


        final_res=get_jid(geneec_obj)

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'geneec','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'geneec', 
                'model_attributes':'GENEEC Output'})
        html = html + geneec_tables.timestamp()
        html = html + geneec_tables.table_all(geneec_obj, final_res)
        # html = html + """<table width="500" border="1">
        #                   <tr>
        #                     <th scope="col" width="200">Inputs</div></th>
        #                     <th scope="col" width="150">Unit</div></th>                            
        #                     <th scope="col" width="150">Value</div></th>
        #                   <tr>
        #                     <td>Chemical name</td>
        #                     <td>&nbsp</td>                            
        #                     <td>%s</td>
        #                   </tr>                            
        #                   <tr>                            
        #                     <td>Application Target</td>
        #                     <td>&nbsp</td>                                                        
        #                     <td>%s</td>                          
        #                   </tr>                            
        #                   <tr>
        #                     <td>Application rate</td>
        #                     <td>lbs a.i./A</td>                                                        
        #                     <td>%s</td>
        #                   </tr>                            
        #                   <tr>                            
        #                     <td>Number of applications</td>
        #                     <td>&nbsp</td>                                                                                    
        #                     <td>%s</td>                          
        #                   </tr>                             
        #                   <tr>
        #                     <td>Interval between applications</td>
        #                     <td>days</td>                                                                                                                
        #                     <td>%s</td>
        #                   </tr>                             
        #                   <tr>                            
        #                     <td>Koc</td>
        #                     <td>K<sub>OC</sub> (mL/g OC)</td>                                                                                                                                            
        #                     <td>%s</td>                          
        #                   </tr>                               
        #                   <tr>
        #                     <td>Aerobic soil metabolism</td>
        #                     <td>K<sub>OC</sub> (mL/g OC)</td>                                                                                                                                                                        
        #                     <td>%s</td>
        #                   </tr>                               
        #                   <tr>                            
        #                     <td>Wet in</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                    
        #                     <td>%s</td>                          
        #                   </tr>                              
        #                   <tr>
        #                     <td>Application method</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                
        #                     <td>%s</td>
        #                   </tr>                              
        #                   <tr>                                                        
        #                     <td>Aerial size distribution</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                
        #                     <td>%s</td>                          
        #                   </tr>                              
        #                   <tr>
        #                     <td>Ground spray type</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                
        #                     <td>%s</td>
        #                   </tr>                                                        
        #                   <tr>                            
        #                     <td>Airblast type</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                
        #                     <td>%s</td>                          
        #                   </tr>                                                        
        #                   <tr>
        #                     <td>Spray quality</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                                            
        #                     <td>%s</td>
        #                   </tr> 
        #                   <tr>                            
        #                     <td>No spray drift</td>
        #                     <td>&nbsp</td>                                                                                                                                                                                                                                                                                        
        #                     <td>%s</td>                          
        #                   </tr> 
        #                   <tr>
        #                     <td>Incorporation depth</td>
        #                     <td>feet</td>                                                                                                                                                                                                                                                                                                                    
        #                     <td>%s</td>
        #                   </tr> 
        #                   <tr>                            
        #                     <td>Solubility</td>
        #                     <td>mg/L</td>                                                                                                                                                                                                                                                                                                                                                
        #                     <td>%s</td>                          
        #                   </tr>                           
        #                   <tr>
        #                     <td>Aerobic aquatic metabolism</td>
        #                     <td>days</td>                                                                                                                                                                                                                                                                                                                                                                            
        #                     <td>%s</td>
        #                   </tr>                           
        #                   <tr>                            
        #                     <td>hydrolysis</td>
        #                     <td>days</td>                                                                                                                                                                                                                                                                                                                                                                                                        
        #                     <td>%s</td>                          
        #                   </tr>                           
        #                   <tr>
        #                     <td>Photolysis aquatic half life</td>
        #                     <td>days</td>                                                                                                                                                                                                                                                                                                                                                                                                                                    
        #                     <td>%s</td>
        #                   </tr>                           
        #                   </table>
        #                   <p>&nbsp;</p>""" %(chem_name,application_target,application_rate,number_of_applications,interval_between_applications,
        #                              Koc,aerobic_soil_metabolism,wet_in,application_method_label,aerial_size_dist_label,ground_spray_type_label,airblast_type_label,
        #                              spray_quality_label,no_spray_drift,incorporation_depth,solubility,aerobic_aquatic_metabolism,hydrolysis_label,photolysis_aquatic_half_life)

        # html = html +  """<table width="700" border="1">
        #                   <tr>
        #                     <th scope="col">Outputs</div></th>
        #                     <th scope="col">Value</div></th>                            
        #                   </tr>
        #                   <tr>
        #                     <td>Peak Generic Expected Environmental Concentration (GEEC) (PPB)</td>
        #                     <td>%0.3E</td>
        #                   </tr>
        #                   <tr>
        #                     <td>Max 4 Day Average GEEC (PPB)</td>
        #                     <td>%0.3E</td>
        #                   </tr>
        #                   <tr>
        #                     <td>Max 21 Day Average GEEC (PPB)</td>
        #                     <td>%0.3E</td>
        #                   </tr>
        #                   <tr>
        #                     <td>Max 60 Day Average GEEC (PPB)</td>
        #                     <td>%0.3E</td>
        #                   </tr>
        #                   <tr>
        #                     <td>Max 90 Day Average GEEC (PPB)</td>
        #                     <td>%0.3E</td>
        #                   </tr>                      
        #                   </table>""" %(final_res[2][0],final_res[2][1],final_res[2][2],final_res[2][3],final_res[2][4])
#    "\"a\""                        
#        html = html + str(GENEECdb.GENEECInp())

#$(document).ready(function() {
# $("label[for='id_solubility']").remove()
#     });
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', GENEECOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
