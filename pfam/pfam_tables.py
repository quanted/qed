
def table_all(pfam_obj):
    table1_out = table_1(pfam_obj)
    table2_out = table_2(pfam_obj)
    table3_out = table_3(pfam_obj)
    table4_out = table_4(pfam_obj)
    table5_out = table_5(pfam_obj)
    table6_out = table_6(pfam_obj)
    table7_out = table_7(pfam_obj)
    table8_out = table_8(pfam_obj)
    table9_out = table_9(pfam_obj)
    html_all = table1_out + table2_out + table3_out + table4_out + table5_out + table6_out + table7_out + table8_out + table9_out
    return html_all

def table_1(pfam_obj):
    html = """
        <table class="out_chemical" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Chemical Inputs</div></th>
                          </tr>        
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>           
                          <tr>
                            <td><div align="center">Water Column Half life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Benthic Compartment Half Life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>      
                          <tr>
                            <td><div align="center">Unflooded Soil Half Life @%s &#8451</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                
                          <tr>
                            <td><div align="center">Aqueous Near-Surface Photolysis Half Life @%s Degrees Latitude</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Hydrolysis Half Life</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Molecular Weight</div></td>
                            <td><div align="center">g/mol</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Vapor Pressure</div></td>
                            <td><div align="center">torr</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Solubility</div></td>
                            <td><div align="center">mg/l</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>      
                          <tr>
                            <td><div align="center">Koc</div></td>
                            <td><div align="center">ml/g</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Heat of Henry</div></td>
                            <td><div align="center">J/mol</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Henry Reference Temperature</div></td>
                            <td><div align="center">&#8451</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                                       
        </table><br>"""%(pfam_obj.wat_t, pfam_obj.wat_hl, pfam_obj.ben_t, pfam_obj.ben_hl, 
                         pfam_obj.unf_t, pfam_obj.unf_hl, pfam_obj.aqu_t, pfam_obj.aqu_hl, 
                         pfam_obj.hyd_hl, pfam_obj.mw, pfam_obj.vp, pfam_obj.sol, pfam_obj.koc, 
                         pfam_obj.hea_h, pfam_obj.hea_r_t)
    return html

def table_2(pfam_obj):
    html = """
        <table class="out_application_pre" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Application Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Applications</div></td>
                            <td><div align="center"></div></td>
                            <td id="noa_out"><div align="center">%s</div></td>
                          </tr></table>
        <table class="out_application" width="550" border="1">
                          <tr>
                            <th scope="col" width="50"><div align="center">App#</div></th>
                            <th scope="col" width="125"><div align="center">Month</div></th>                            
                            <th scope="col" width="125"><div align="center">Day</div></th>
                            <th scope="col" width="125"><div align="center">Mass Applied (kg/hA)</div></th>
                            <th scope="col" width="125"><div align="center">Slow Release (1/day)</div></th>
                          </tr>
                          <tr>          
                            <td id="mm_out" data-val='%s' style="display: none"></td>  
                            <td id="dd_out" data-val='%s' style="display: none"></td>  
                            <td id="ma_out" data-val='%s' style="display: none"></td>  
                            <td id="sr_out" data-val='%s' style="display: none"></td>  
                          </tr>                               
       </table><br>"""%(pfam_obj.noa, pfam_obj.mm_out, pfam_obj.dd_out, pfam_obj.ma_out, pfam_obj.sr_out)
    return html

def table_3(pfam_obj):
    html = """
        <table class="out_location" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Location Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Weather File</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Latitude (for Photolysis Calculations)</div></td>
                            <td><div align="center">degree</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                           
        </table><br>"""%(pfam_obj.weather, pfam_obj.wea_l)    
    return html

def table_4(pfam_obj):
    html = """
        <table class="out_floods_pre" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="5"><div align="center">Floods Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Number of Events</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Number of Events</div></td>
                            <td><div align="center"></div></td>
                            <td id="nof_out"><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Date for Event 1</div></td>
                            <td><div align="center"></div></td>
                            <td id="noa_out"><div align="center">%s</div></td>
                          </tr></table>
        <table class="out_floods" width="550" border="1">
                          <tr>
                            <th scope="col" width="50"><div align="center">Event#</div></th>
                            <th scope="col" width="100"><div align="center">Number of days</div></th>                            
                            <th scope="col" width="100"><div align="center">Fill Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Wier Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Min. Level (m)</div></th>
                            <th scope="col" width="100"><div align="center">Turn Over (1/day)</div></th>                            
                          </tr>
                          <tr>          
                            <td id="nod_out" data-val='%s' style="display: none"></td>  
                            <td id="fl_out" data-val='%s' style="display: none"></td>  
                            <td id="wl_out" data-val='%s' style="display: none"></td>  
                            <td id="ml_out" data-val='%s' style="display: none"></td>
                            <td id="to_out" data-val='%s' style="display: none"></td>  
                          </tr>                               
       </table><br>"""%(pfam_obj.nof, pfam_obj.date_f1, pfam_obj.nod_out, pfam_obj.fl_out, 
                        pfam_obj.wl_out, pfam_obj.ml_out, pfam_obj.to_out)
    return html

def table_5(pfam_obj):
    html = """<table class="out_location" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Crop Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Zero Height Reference</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Days from Zero Height to Full Height</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Days from Zero Height to Removal</div></td>
                            <td><div align="center">days</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Maximum Fractional Area Coverage</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                    
        </table><br>"""%(pfam_obj.zero_height_ref, pfam_obj.days_zero_full, pfam_obj.days_zero_removal, pfam_obj.max_frac_cov)       
    return html

def table_6(pfam_obj):
    html = """<table class="out_physical" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Physical Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>                            
                          <tr>
                            <td><div align="center">Mass Transfer Coefficient</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                          
                          <tr>
                            <td><div align="center">Leakage</div></td>
                            <td><div align="center">m/d</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Reference Depth</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Benthic Depth</div></td>
                            <td><div align="center">m</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Benthic Porosity</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>   
                          <tr>
                            <td><div align="center">Dry Bulk Density</div></td>
                            <td><div align="center">g/cm<sup>3</sup></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Foc Water Column on SS</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>  
                          <tr>
                            <td><div align="center">Foc Benthic</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">SS</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Water column DOC</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Chlorophyll, CHL</div></td>
                            <td><div align="center">mg/L</div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr> 
                          <tr>
                            <td><div align="center">Dfac</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>
                          <tr>
                            <td><div align="center">Q10</div></td>
                            <td><div align="center"></div></td>                            
                            <td><div align="center">%s</div></td>
                          </tr>                                                                                                                                                                                                                                                                                                                        
        </table><br>"""%(pfam_obj.mas_tras_cof, pfam_obj.leak, pfam_obj.ref_d, pfam_obj.ben_d, 
                         pfam_obj.ben_por, pfam_obj.dry_bkd, pfam_obj.foc_wat, pfam_obj.foc_ben, 
                         pfam_obj.ss, pfam_obj.wat_c_doc, pfam_obj.chl, pfam_obj.dfac, pfam_obj.q10)   
    return html

def table_7(pfam_obj):
    html = """
        <table class="out_output" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Output Inputs</div></th>
                          </tr>
                          <tr>
                            <th scope="col" width="250"><div align="center">Variable</div></th>
                            <th scope="col" width="150"><div align="center">Unit</div></th>                            
                            <th scope="col" width="150"><div align="center">Value</div></th>
                          </tr>
                          <tr>             
                            <th scope="col" width="250"><div align="center">Area of Application</div></th>
                            <th scope="col" width="150"><div align="center">m<sup>2</sup></div></th>                            
                            <th scope="col" width="150"><div align="center">%s</div></th>
                          </tr>
        </table><br>"""%(pfam_obj.area_app)   
    return html

def table_8(pfam_obj):
    html = """
        <table class="results" width="550" border="1">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">PFAM Results</div></th>
                          </tr>
                          <tr>
                            <th scope="col"><div align="center">Outputs</div></th>
                            <th scope="col"><div align="center">Value</div></th>                            
                          </tr>
                          <tr>
                            <td><div align="center">Simulation is finished. Please download your file from here</div></td>
                            <td><div align="center"><a href=%s>Link</a></div></td>
                          </tr>
                          <tr style="display: none">
                            <td id="x_date1" data-val='%s'></td>
                            <td id="x_re_v_f" data-val='%s'></td>
                            <td id="x_re_c_f" data-val='%s'></td>
                            <td id="x_date2" data-val='%s'></td>
                            <td id="x_water" data-val='%s'></td>
                            <td id="x_water_level" data-val='%s'></td>
                            <td id="x_ben_tot" data-val='%s'></td>
                            <td id="x_ben_por" data-val='%s'></td>
                          </tr>
        </table><br>"""%(pfam_obj.final_res[1][0], pfam_obj.x_date1, pfam_obj.x_re_v_f, pfam_obj.x_re_c_f, 
                         pfam_obj.x_date2, pfam_obj.x_water, pfam_obj.x_water_level, pfam_obj.x_ben_tot, pfam_obj.x_ben_por)  
    return html

def table_9(pfam_obj):
    html = """
        <table class="display" width="550" border="0">
                          <tr>
                            <th scope="col" colspan="3"><div align="center">Please select the display range</div></th>
                          </tr>
        </table><br>"""

    html = html +"""
        <div id="date_range_slider_1"></div>
        <div><button type="button" id="calc1">Generate</button></div>
        <div id="chart1" style="margin-top:20px; margin-left:90px; width:650px; height:400px;"></div>
        <div id="chart2" style="margin-top:20px; margin-left:90px; width:650px; height:400px;"></div>
        <div id="chart3" style="margin-top:20px; margin-left:90px; width:650px; height:400px;"></div>        
        """
    return html
