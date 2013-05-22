# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:29:49 2012

@author: msnyde02
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from beepop import beepopdb
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
import math
import csv

cgitb.enable()

# read in weather data
path0 = os.path.dirname(__file__)

data = csv.reader(open(path0+'/athens_weather.csv'))
#data = csv.reader(open('C:/temp/athens_weather.csv'))
jday = []
precip = []
temp = []
wspeed = []
day_light = []
for row in data:
    jday.append(float(row[0]))
    precip.append(float(row[1]))  
    temp.append(float(row[2]))
    wspeed.append(float(row[3]))
    day_light.append(float(row[4]))
# number of eggs layed on a day by the queen
def Et_f(winter_kill, kill_percent,swarm, swarm_date, adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size):
    p_t = 0
    Et = 0
    eu = 0
    ed = 0
    Wt = 0 # workers produced per day
    eggs_laid = []
    eggs_used = []
    drone_eggs_list = []
    worker_eggs = []
    total_workers_day = []
    total_foragers_day = []
    number_drones_day = [] 
    n_f = 0    
    n_a = 0  
    n_d = 0  
      #create matrices
    Ndays = 365  
    eggs = np.zeros((days_to_adult_worker-1,Ndays+1)) #creates an array value x 365 columns
    drone_eggs = np.zeros((days_to_adult_drones, Ndays+1))    
    adults = np.zeros((days_from_adult_to_forager-1, Ndays+1)) #creates an array value x 365 columns
    forager = np.zeros((number_of_forages-1, Ndays+1))
    drones = np.zeros((days_to_adult_drones-1, Ndays+1))
    drones_outside = np.zeros((number_of_forages-1,Ndays+1))
    forager[0, 0] = initial_colony_size * (1.0/3)
    total_foragers_day.append(initial_colony_size * (1.0/3))
#    print 'total_foragers_day', total_foragers_day
   # print forager[0,0]
   # print forager
    adults[0,0] = initial_colony_size - forager[0,0] 
#    be_verbose = 1  
  #  print forager[0,0]
    for i in range(1,Ndays,1):
 #       if be_verbose==1:
 #           print '--------------------------------------------------------------------<br>'
 #           print 'i=', i, '<br>'
        day = i-1
        DD = (-.0006*(wspeed[day]**2)) + (.05 * wspeed[day]) + 0.021 #temperature factor calculation
        LT = (-.00743*(day_light[day]**3)) + (0.312 * (day_light[day]**2)) - (4.04 * day_light[day]) + 16.58 #sunlight factor calculation 
        nt = total_foragers_day[i-1]
        #print 'total_foragers_day', total_foragers_day[i-1]
        #print 'nt=', nt
        if nt > 0:
            N = (math.log((nt * .001) + 1)) * 0.672    #foraging population size factor calculation for number of eggs laid
            Ft = (math.log(nt * .0006))*0.797 #foraging population size factor for calculation of number of drones vs. worker eggs laid
        else:
            N= 0.1
            Ft = 0.1
        p_t = e_max + ((-.0027 * (i**2)) + (0.395 * i)) #egg laying factor depending on day of laying
#        print 'foragers=', total_foragers_day[i-1]
#        print 'workers=', total_workers_day[i-1]
#        print 'eggs=', eggs_laid[i-1]
        #print 'n_a', n_a
        if ( i >1 and ((n_a + n_f) / Et) > 3 and (n_a + n_f / Et > adult_brood_ratio) ):         
            Et = DD * LT * N * p_t #Et number of eggs laid per day
            Et = round(Et)
            if Et < 0: 
                Et = 0
            else:
                Et = Et
       #     print 'ratio', ((n_a + n_f) / Et), '<br>'
        else:
            Et = 0
        eggs_laid.append(Et) #list of eggs laid on each day
        st = Wt / sperm_obtained #proportion of available sperm used
        if st > 0.6:
            St = 1 - ((-6.355 * (st**3)) + (7.657 * (st**2)) + 1.002) #proportion of sperm used factor
        else:
            St = 0
       # Ft = (math.log(nt * .0006))*0.797 #foraging population size factor for calculation of number of drones vs. worker eggs laid
        Light = (math.log(day_light[day] * 0.1))*0.284 #hours of sunlight factor for calculation of number of drones vs. worker eggs laid
        Zt = St + (Light * Ft) # proportion of eggs unfertilized
        Vt = round(Zt * Et) # number of drone eggs produced per day
        if Vt < 0:
            Vt = 0
        else:
            Vt = Vt
   #     print 'Vt=', Vt, '<br>'
        Wt = Et - Vt # number of worker eggs produced per day
   #     print 'Wt=', Wt, '<br>'        
        eu = eu + Wt
        ed = ed + Vt
        
        drone_eggs[0,i] = Vt
        #drone_eggs = np.roll(drone_eggs, 1, axis = 0) # shifts values one cell down and one to the right
        #drone_eggs = np.roll(drone_eggs, 1, axis = 1)
        drone_eggs[1:days_to_adult_drones-1, i] = drone_eggs[0:days_to_adult_drones-2, i-1]
        eggs[0, i] = Wt #puts number of eggs laid into first row at i place in the matrix
        #eggs = np.roll(eggs, 1, axis = 0) # shifts values one cell down         
        #eggs = np.roll(eggs, 1, axis = 1)  # shifts values one cell to the right  
        eggs[1:days_to_adult_worker-1, i] = eggs[0:days_to_adult_worker-2, i-1]
       # print 'eggs=', eggs[0:days_to_adult_worker+2, i], '<br>'
        eggs_used.append(eu)   
        #print 'eggs_used', eggs_used[i-1], '<br>'
        drone_eggs_list.append(Vt)
        worker_eggs.append(Wt)
        # life cycle for fertilized eggs that develop into worker bees and foragers
        #print forager        
#        if i == 1:
#            adults = adults
        #if i < days_to_adult_worker:   
            ##print 'e'                   
            #adults_t = np.roll(adults, 1, axis = 0) 
            #adults_t = np.roll(adults_t, 1, axis = 1)
            #adults_t[:,0]=0
            #adults_t[0,:]=0
            #adults = adults_t
            #print adults[:,i]            
            #adults[1:365, 1:365] = adults[0:364, 0:364]            
            # 0.85 is the survival rate of eggs into adults
            #print adults[:,i]
        #else:
        #forager[1:364, i] = forager[0:363, i-1]    
        adults[1:days_from_adult_to_forager-1, i] = adults[0:days_from_adult_to_forager-2, i-1]        
        adults[0, i] = round((eggs[days_to_adult_worker-2,i-1])*egg_mortality)         
         # put eggs developed into adult bees into adult matrix
        #print 'new eggs=', (eggs[days_to_adult_worker-2,i])*.85
        #print 'new adults=', round((eggs[days_to_adult_worker-2,i-1])*.85), '<br>'
            #adults_t = np.roll(adults, 1, axis = 0) 
            #adults_t = np.roll(adults_t, 1, axis = 1)
            #adults_t[:,0]=0
            #adults_t[0,:]=0            
        #adults[0, i-1] = (eggs[days_to_adult_worker-2,i])*.85 # put eggs developed into adult bees into adult matrix
        #forager matrix update per time step depending on weather and time step   
#        if i == Ndays-1:
#            for j in range(0,i,1):
#                print 'adults', adults[0:days_from_adult_to_forager+1,j], '<br>'
#        else:
#                print 'adult age structure  for day', i, ' =', adults[0:Ndays,i], '<br>'
#        if i == 1:
#            forager = forager
#            print 'i=1 forager=', forager[0:34, 0:34]
        if i >59 and i <305 and (temp[day] > 12 and wspeed[day] < 34 and precip[day] < 0.5):
 #           print i, 'was a good day', '<br>'            
#            forager_t = np.roll(forager, 1, axis = 1)
#            forager_t = np.roll(forager_t, 1, axis = 0)
#            forager_t[:,0]=0
#            forager_t[0,:]=0  
            forager[1:number_of_forages-1, i] = forager[0:number_of_forages-2, i-1]
            forager[0,i] = adults[days_from_adult_to_forager-2, i-1] 
          #  print 'adults=', adults[days_from_adult_to_forager-2, i], '<br>'
       # for j in range (0,i,1):
        #    print 'forager', forager[j,0:i+1], '<br>'
          #  print 'i>1 forager=', forager[0:34, 0:34]  
           # print forager[:,i]
#        elif (i > days_to_adult_worker + days_from_adult_to_forager) and temp[day] > 12 and wspeed[day] < 34 and precip[day] < 0.5:       
#            #print 'b'            
#            forager_t = np.roll(forager, 1, axis = 1)
#            forager_t = np.roll(forager_t, 1, axis = 0)
#            forager_t[:,0]=0
#            forager_t[0,:]=0  
#            forager_t[0,i] = adults[days_from_adult_to_forager-1, i]
#            forager = forager_t
#        elif (i >1 and i < days_to_adult_worker + days_from_adult_to_forager): #bad day    
#            #print 'c'            
#            forager = np.roll(forager, 1, axis = 1)            
            #forager[1:365, 1:365] = forager[0:364, 0:364]      
        else: # > days_to_adult_worker + days_from_adult_to_forager and a bad day
#            print i, 'was a bad day', '<br>'
           # print 'forager', forager[0:9,0:i], '<br>'
#            forager_t = np.roll(forager, 1, axis = 1)
            forager[:, i] = forager[:, i-1]
            forager[0,i] = forager[0,i] + adults[days_from_adult_to_forager-2, i-1]                        
          #  print 'adults=', adults[days_from_adult_to_forager-2, i], '<br>'            
            #for j in range (0,i,1):
                #print 'forager', forager[j,0:i+1], '<br>'            
           # print 'forager=', forager[0:9,0:i], '<br>'
           # print 'i>1 forager=', forager[0:34, 0:34], '<br>'
#        print 'forager=', forager[0:number_of_forages,i], '<br>' 
        # update of list tracking total workers a day from matrix                              
#        n_a = 0         
#        for p in range(0,days_from_adult_to_forager,1):
#            #print 'i=', i             
#            #print 'p=', p            
#            #print 'n_a=', n_a
#            n_a = n_a + adults[p,i] #calculates number of workers per day and adds to a list        
        n_a =sum(adults[0:days_from_adult_to_forager-2, i])        
        total_workers_day.append(n_a)
#        print 'workers_day', total_workers_day[i-1], '<br>'
        #print total_workers_day        
        # update of list tracking total foragers a day from matrix                 
        #n_f = 0         
        #for p in range(0,number_of_forages,1):
        
          #  print i
         #   print p
        #    print n_f
        #print n_f
#        print 'forager', forager, '<br>'        
        n_f=sum(forager[0:number_of_forages,i]) 
       # print 'n_f (number of foragers)', n_f, '<br>' #calculates number of foragers per day and adds to a list 
        total_foragers_day.append(n_f)
#        print 'total_foragers=', total_foragers_day, '<br>'
        #print total_foragers_day
        #print total_foragers_day 
     #life cycle for unfertilized eggs that develop into drones   
       # if i > days_to_adult_drones:   
             #drones = np.roll(drones, 1, axis = 0)      
             #drones = np.roll(drones, 1, axis = 1)    
        drones[1:days_to_adult_drones-1, i] = drones[0:days_to_adult_drones-2, i-1]
        drones[0, i] = (drone_eggs[days_to_adult_drones-2,i])*egg_mortality # put eggs developed into adult bees into drone matrix         
        if temp[day] > 12 and wspeed[day] < 34 and precip[day] < 0.5:
            drones_outside[1:number_of_forages-1, i] = drones_outside[0:number_of_forages-2, i-1]
            #drones_outside = np.roll(drones_outside, 1, axis = 0)
            #drones_outside = np.roll(drones_outside, 1, axis = 1)                               
        else: # put eggs developed into drone matrix matrix
            drones_outside[0,i] = drones_outside[0,i] + drones[days_from_adult_to_forager-2, i]
        #update of list tracking total drones outside a day from matrix                                       
#        n_d = 0          
#        for p in range(0,number_of_forages,1):
#            n_d = n_d + drones_outside[p,i]   
        n_d =sum(drones_outside[0:number_of_forages-1, i])  #calculates number of drones per day and adds to a list       
        #print n_d
        number_drones_day.append(n_d)
 #       print 'drones=', number_drones_day
        if swarm == 'Yes' and i == swarm_date:
            forager[0:number_of_forages,i] = 0.75 * (forager[0:number_of_forages,i])
            adults[0:days_from_adult_to_forager-2, i] = 0.30 * (adults[0:days_from_adult_to_forager-2, i])
            drones[1:days_to_adult_drones-1, i] = 0.95 * (drones[1:days_to_adult_drones-1, i])
            for i in range(swarm_date+5,258,1):
                adult_brood_ratio = 2  
        else:
            forager[0:number_of_forages,i] = (forager[0:number_of_forages,i])
            adults[0:days_from_adult_to_forager-2, i] = (adults[0:days_from_adult_to_forager-2, i])
            drones[1:days_to_adult_drones-1, i] = (drones[1:days_to_adult_drones-1, i])
#implementing winter kill equation                
        if winter_kill == 'Yes' and i > 1 and i < 30:
            kill_per_day = float(kill_percent) / 29            
            per_remain_day= 1.0 - (kill_per_day / 100 ) 
            forager[0:number_of_forages,i] = per_remain_day * (forager[0:number_of_forages,i])
            adults[0:days_from_adult_to_forager-2, i] = per_remain_day * (adults[0:days_from_adult_to_forager-2, i])
            drones[1:days_to_adult_drones-1, i] = per_remain_day * (drones[1:days_to_adult_drones-1, i])    
        else:
            forager[0:number_of_forages,i] = (forager[0:number_of_forages,i])
            adults[0:days_from_adult_to_forager-2, i] = (adults[0:days_from_adult_to_forager-2, i])
            drones[1:days_to_adult_drones-1, i] = (drones[1:days_to_adult_drones-1, i]) 
    return eggs_laid, drone_eggs, worker_eggs, eggs, n_a, n_f, n_d, number_drones_day, total_foragers_day, total_workers_day    
class beepopOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        initial_colony_size = float(form.getvalue('initial_colony_size'))
        sperm_obtained = float(form.getvalue('sperm_obtained'))
        egg_mortality = float(form.getvalue('egg_mortality'))
        e_max = float(form.getvalue('potential_eggs_laid'))
        adult_brood_ratio = float(form.getvalue('adult_brood_ratio'))
      #  no_foraging_days = int(form.getvalue('no_foraging_days'))
        brood_cycles = float(form.getvalue('brood_cycles'))
        days_to_adult_worker = int(form.getvalue('days_to_adult_worker'))
        days_to_adult_drones = int(form.getvalue('days_to_adult_drones'))
        days_from_adult_to_forager = int(form.getvalue('days_from_adult_to_forager'))
        number_of_forages = int(form.getvalue('number_of_forages'))
        swarm = (form.getvalue('swarm'))
        stop_lay = int(form.getvalue('stop_lay'))
        start_lay = int(form.getvalue('start_lay'))
        lay_maximum = int(form.getvalue('lay_maximum'))
        swarm_date = int(form.getvalue('swarm_date'))
        kill_percent = float(form.getvalue('kill_percent'))
        winter_kill = (form.getvalue('winter_kill'))
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'beepop','page':'output'})
        html = html + template.render (templatepath + '03pop_ubertext_links_left.html', {})                
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'beepop', 
                'model_attributes':'BEEPOP Output'})
        html = html + """
        <div class="out_">
            <H3>User Inputs</H3>
            <table>
                <tr>
                    <td>Initial colony size</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Sperm obtained</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Potential eggs laid</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Number of foraging days</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Brood cycles</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Days for eggs to develop into adult worker</td>
                    <td>%s</td>
                </tr>
                 <tr>
                    <td>Days for eggs to develop into adult drones</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Days for inside worker bees to develop into foragers</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Number of foragers until death</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Percentage of eggs surviving to adults</td>
                    <td>%s</td>
                </tr>
            </table>
        </div>
        """ % (initial_colony_size, sperm_obtained, e_max, number_of_forages, brood_cycles, days_to_adult_worker, days_to_adult_drones, days_from_adult_to_forager, number_of_forages, egg_mortality)
        html = html + """
        <div class="out_">
            <H3>Outputs for the last day of the model run</H3>
            <table>
                <tr>
                    <td>Worker bees</td>
                    <td>%.2f</td>
                </tr>
                <tr>
                    <td>Forager bees</td>
                    <td>%.2f</td>
                </tr>
                <tr>
                    <td>Drones bees</td>
                    <td>%.2f</td>
                </tr>
            </table>
        </div>
        """ % (Et_f(winter_kill, kill_percent,swarm, swarm_date,adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[4], Et_f(winter_kill, kill_percent,swarm, swarm_date,adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[5], Et_f(winter_kill, kill_percent,swarm, swarm_date,adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[6])
        html = html +  """
        <table width="400" border="1", style="display:none">
            <tr>
                <td>hive_val_1</td>
                <td id="Eggs_laid">%s</td>
            </tr>
            <tr>
                <td>hive_val_2</td>
                <td id="Adult_workers">%s</td>
            </tr>
            <tr>
                <td>hive_val_3</td>
                <td id="Foragers">%s</td>
            </tr>
            <tr>
                <td>hive_val_3</td>
                <td id="Drones">%s</td>
            </tr>                                                     
      </table>
        """%(Et_f(winter_kill, kill_percent,swarm, swarm_date, adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[0],Et_f(winter_kill, kill_percent,swarm, swarm_date, adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[9],Et_f(winter_kill, kill_percent,swarm, swarm_date, adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[8],Et_f(winter_kill, kill_percent,swarm, swarm_date, adult_brood_ratio, egg_mortality, e_max, days_to_adult_drones, sperm_obtained, days_to_adult_worker, days_from_adult_to_forager, number_of_forages, initial_colony_size)[7])        
        html = html + template.render(templatepath + 'beepop-outputjqplot.html', {})         
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + 'export.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
          
       
        self.response.out.write(html)
          
app = webapp.WSGIApplication([('/.*', beepopOutputPage)], debug=True)
        
      
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()