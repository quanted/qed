# -*- coding: utf-8 -*-

# TREX
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
#from trex import trex_input
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()

#food intake for birds

def fi_bird(aw_bird, mf_w_bird):
    try:
        aw_bird = float(aw_bird)
        mf_w_bird = float(mf_w_bird)           
    except IndexError:
        raise IndexError\
        ('The body weight of the assessed bird, and/or the mass fraction of '\
        'water in the food must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The body weight of the assessed bird must be a real number, not "%g"' % aw_bird)
    except ValueError:
        raise ValueError\
        ('The mass fraction of water in the food for bird must be a real number, not "%g"' % mf_w_bird)
    if aw_bird < 0:
        raise ValueError\
        ('The body weight of the assessed bird=%g is a non-physical value.' % aw_bird)
    if mf_w_bird < 0:
        raise ValueError\
        ('The fraction of water in the food for bird=%g is a non-physical value.' % mf_w_bird)        
    if mf_w_bird >= 1:
        raise ValueError\
        ('The fraction of water in the food for bird=%g must be less than 1.' % mf_w_bird)   
    return (0.648 * (aw_bird**0.651))/(1-mf_w_bird)

# food intake for mammals

def fi_mamm(aw_mamm, mf_w_mamm):
    try:
        aw_mamm = float(aw_mamm)
        mf_w_mamm = float(mf_w_mamm)           
    except IndexError:
        raise IndexError\
        ('The body weight of mammal, and/or the mass fraction of water in the '\
         'food must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The body weight of mammal must be a real number, not "%g"' % aw_mamm)
    except ValueError:
        raise ValueError\
        ('The mass fraction of water in the food for mammals must be a real number, not "%"' % mf_w_mamm)
    if aw_mamm < 0:
        raise ValueError\
        ('The body weight of mammal=%g is a non-physical value.' % aw_mamm)
    if mf_w_mamm < 0:
        raise ValueError\
        ('The fraction of water in the food for mammals=%g is a non-physical value.' % mf_w_mamm)        
    if mf_w_mamm >= 1:
        raise ValueError\
        ('The fraction of water in the food for mammals=%g must be less than 1.' % mf_w_mamm)  
    return (0.621 * (aw_mamm**0.564))/(1-mf_w_mamm)

#Acute adjusted toxicity value for birds

def at_bird(ld50_bird,aw_bird,tw_bird,x):
    try:
        ld50_bird = float(ld50_bird)
        aw_bird = float(aw_bird)
        tw_bird = float(tw_bird)
        x = float(x)
    except IndexError:
        raise IndexError\
        ('The lethal dose, body weight of assessed bird, body weight of tested'\
        ' bird, and/or Mineau scaling factor for birds must be supplied on'\
        ' the command line.')
    except ValueError:
        raise ValueError\
        ('The lethal dose must be a real number, not "%mg/kg"' %ld50_bird)
    except ValueError:
        raise ValueError\
        ('The body weight of assessed bird must be a real number, not "%g"' %aw_bird)
    except ValueError:
        raise ValueError\
        ('The body weight of tested bird must be a real number, not "%g"' %tw_bird)
    except ValueError:
        raise ValueError\
        ('The Mineau scaling factor for birds must be a real number' % x)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of tested bird must be non-zero.')
    if ld50_bird < 0:
        raise ValueError\
        ('ld50=%g is a non-physical value.' % ld50_bird)
    if aw_bird < 0:
        raise ValueError\
        ('aw_bird=%g is a non-physical value.' % aw_bird)
    if tw_bird < 0:
        raise ValueError\
        ('tw_bird=%g is a non-physical value.' % tw_bird)
    if x < 0:
        raise ValueError\
        ('x=%g is non-physical value.' %x)
    return (ld50_bird) * ((aw_bird/tw_bird)**(x-1))

# Acute adjusted toxicity value for mammals

def at_mamm(ld50_mamm,aw_mamm,tw_mamm):
    try:
        ld50_mamm = float(ld50_mamm)
        aw_mamm = float(aw_mamm)
        tw_mamm = float(tw_mamm)
    except IndexError:
        raise IndexError\
        ('The lethal dose, body weight of assessed mammal, and body weight of tested'\
        ' mammal must be supplied on'\
        ' the command line.')
    except ValueError:
        raise ValueError\
        ('The lethal dose must be a real number, not "%mg/kg"' %ld50_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of assessed mammals must be a real number, not "%g"' %aw_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of tested mammals must be a real number, not "%g"' %tw_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of tested mammals must be non-zero.')
    if ld50_mamm < 0:
        raise ValueError\
        ('ld50_mamm=%g is a non-physical value.' % ld50_mamm)
    if aw_mamm < 0:
        raise ValueError\
        ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    if tw_mamm < 0:
        raise ValueError\
        ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    return (ld50_mamm) * ((tw_mamm/aw_mamm)**(0.25))

# Adjusted chronic toxicity (NOAEL) value for mammals

def ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm):
    try:
        NOAEL_mamm = float(NOAEL_mamm)
        aw_mamm = float(aw_mamm)
        tw_mamm = float(tw_mamm)
    except IndexError:
        raise IndexError\
        ('The NOAEL, body weight of assessed mammal, and body weight of tested'\
        ' mammal must be supplied on'\
        ' the command line.')
    except ValueError:
        raise ValueError\
        ('The NOAEL must be a real number, not "%mg/kg"' %NOAEL_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of assessed mammals must be a real number, not "%g"' %aw_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of tested mammals must be a real number, not "%g"' %tw_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of tested mammals must be non-zero.')
    if NOAEL_mamm < 0:
        raise ValueError\
        ('NOAEL_mamm=%g is a non-physical value.' % NOAEL_mamm)
    if aw_mamm < 0:
        raise ValueError\
        ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    if tw_mamm < 0:
        raise ValueError\
        ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    return (NOAEL_mamm) * ((tw_mamm/aw_mamm)**(0.25))

#Dietary based EECs

#Initial concentration
 
def C_0(a_r, a_i, para):
    try:
        a_r = float(a_r)
        a_i = float(a_i)           
    except IndexError:
        raise IndexError\
        ('The application rate, and/or the percentage of active ingredient '\
         'must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The application rate must be a real number, not "%g"' % a_r)
    except ValueError:
        raise ValueError\
        ('The percentage of active ingredient must be a real number, not "%"' % a_i)
    if a_r < 0:
        raise ValueError\
        ('The application rate=%g is a non-physical value.' % a_r)
    if a_i < 0:
        raise ValueError\
        ('The percentage of active ingredient=%g is a non-physical value.' % a_i)        
    return (a_r*a_i*para)

#Concentration over time

def C_t(C_ini, h_l):    
    try:
        h_l = float(h_l)      
    except IndexError:
        raise IndexError\
        ('The initial concentration, and/or the foliar dissipation half life, '\
         'must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The foliar dissipation half life must be a real number, not "%g"' % h_l)      
    if h_l < 0:
        raise ValueError\
        ('The foliar dissipation half life=%g is a non-physical value.' % h_l)        
    return (C_ini*np.exp(-(np.log(2)/h_l)*1))
    
# concentration over time if application rate or time interval is variable

#Dietary based EECs

def EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out):

    C_temp = np.ones((365,1)) #empty array to hold the concentrations over days       
    a_p_temp = 0  #application period temp  
    n_a_temp = 0  #number of existing applications
    dayt = 0
#new in trex1.5.1
    if n_a == 1:
        C_temp = C_0(a_r[0], a_i, para)
        return C_temp
    
    else:
        for i in range (0,365):
            if i==0:  #first day of application
                a_p_temp = 0
                n_a_temp = n_a_temp + 1
                C_temp[i] = C_0(a_r[0], a_i, para)
                dayt = dayt + 1
            elif i==day_out[dayt] and n_a_temp<=n_a: # next application day
                n_a_temp = n_a_temp + 1
                C_temp[i] = C_t(C_temp[i-1], h_l) + C_0(a_r[dayt], a_i, para)
                dayt = dayt + 1        
        # elif a_p_temp<(i_a-1) and n_a_temp<=n_a: #
        #     a_p_temp=a_p_temp+1
        #     C_temp[i]=C_t(C_temp[i-1], h_l)        
            else : #not an application day just degredation of existing concentration
                C_temp[i]=C_t(C_temp[i-1], h_l) 
        return (max(C_temp))


# Dose based EECs for birds

def EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l, day_out):
    n_a = float(n_a)
 #   i_a = float(i_a)      
    aw_bird = float(aw_bird)
    mf_w_bird = float(mf_w_bird)
  #  a_r = float(a_r)
    a_i = float(a_i)
    para = float(para)
    h_l = float(h_l)
        
    fi_bird = fi_bird(aw_bird, mf_w_bird)
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)
    return (EEC_diet*fi_bird/aw_bird)

# Dose based EECs for granivores birds

# def EEC_dose_bird_g(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l):
#     if para==15:
#         n_a = float(n_a)
#       #  i_a = float(i_a)      
#         aw_bird = float(aw_bird)
#         mf_w_bird = float(mf_w_bird)
#         a_r = float(a_r)
#         a_i = float(a_i)
#         para = float(para)
#         h_l = float(h_l)        
#         fi_bird = fi_bird(aw_bird, mf_w_bird)
#         EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day)
#         return (EEC_diet*fi_bird/aw_bird)
#     else:
#         return(0)
        
# Dose based EECs for mammals

def EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l, day_out):
    aw_mamm = float(aw_mamm)
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)
    fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    return (EEC_diet*fi_mamm/aw_mamm)

# Dose based EECs for granivores mammals

# def EEC_dose_mamm_g(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l):
#     if para==15:    
#         aw_mamm = float(aw_mamm)
#         EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day)
#         fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
#         return (EEC_diet*fi_mamm/aw_mamm)
#     else:
#         return(0)
        
# Acute dose-based risk quotients for birds

def ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l, day_out):
    EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l, day_out)
    at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
    return (EEC_dose_bird/at_bird)

# Acute dose-based risk quotients for granivores birds

# def ARQ_dose_bird_g(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l):
#     if para==15:
#         EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, a_r, a_i, para, h_l)
#         at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
#         return (EEC_dose_bird/at_bird)
#     else:
#         return (0)
    
# Acute dose-based risk quotients for mammals

def ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l, day_out):
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l, day_out)
    at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    return (EEC_dose_mamm/at_mamm)

# Acute dose-based risk quotients for granivores mammals

# def ARQ_dose_mamm_g(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l):
#     if para==15:    
#         EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l)
#         at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
#         return (EEC_dose_mamm/at_mamm)
#     else:
#         return(0)
        
# Acute dietary-based risk quotients for birds

def ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, a_r, a_i, para, h_l, day_out):
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)    
    try:
        lc50_bird = float(lc50_bird)      
    except IndexError:
        raise IndexError\
        ('The Avian LC50 must be supplied on the command line.')
    if lc50_bird < 0:
        raise ValueError\
        ('The Avian LC50=%g is a non-physical value.' % lc50_bird)        
    return (EEC_diet/lc50_bird)


# Acute dietary-based risk quotients for mammals

def ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, a_r, a_i, para, h_l, day_out):
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)    
    return (EEC_diet/lc50_mamm)

# Chronic dietary-based risk quotients for birds

def CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, a_r, a_i, para, h_l, day_out):
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)    
    try:
        NOAEC_bird = float(NOAEC_bird)      
    except IndexError:
        raise IndexError\
        ('The avian NOAEC must be supplied on the command line.')
    if NOAEC_bird < 0:
        raise ValueError\
        ('The avian NOAEC=%g is a non-physical value.' % NOAEC_bird)        
    return (EEC_diet/NOAEC_bird)

# Chronic dietary-based risk quotients for mammals

def CRQ_diet_mamm(EEC_diet, NOAEC_mamm, C_0, n_a, a_r, a_i, para, h_l):
    EEC_diet=EEC_diet(C_0, n_a, a_r, a_i, para, h_l, day_out)
    try:
        NOAEC_mamm = float(NOAEC_mamm)      
    except IndexError:
        raise IndexError\
        ('The mammlian NOAEC must be supplied on the command line.')
    if NOAEC_mamm < 0:
        raise ValueError\
        ('The mammlian NOAEC=%g is a non-physical value.' % NOAEC_mamm)        
    return (EEC_diet/NOAEC_mamm)

# Chronic dose-based risk quotients for mammals

def CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, a_r, a_i, para, h_l, day_out):
    ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l, day_out)     
    return (EEC_dose_mamm/ANOAEL_mamm)

# Chronic dose-based risk quotients for granviores mammals

# def CRQ_dose_mamm_g(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, a_r, a_i, para, h_l):
#     if para==15:    
#         ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
#         EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, a_r, a_i, para, h_l)     
#         return (EEC_dose_mamm/ANOAEL_mamm)
#     else:
#         return (0)
        
# LD50ft-2 for row/band/in-furrow granular birds

def LD50_rg_bird(Application_type, a_r, a_i, p_i, r_s, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x): 
    if Application_type=='Row/Band/In-furrow-Granular':     
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        print 'r_s', r_s
        n_r=(43560**0.5)/(r_s)
        print 'n_r=', n_r
        print 'a_r=', a_r
        print 'b_w=', b_w
        print 'p_i=', p_i
        print 'a_i', a_i
        print 'class a_r', type(a_r)
        expo_rg_bird=(max(a_r)*a_i*453590.0)/(n_r*(43560.0**0.5)*b_w)*(1-p_i)
        return (expo_rg_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow liquid birds

def LD50_rl_bird(Application_type, a_r, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if Application_type=='Row/Band/In-furrow-Liquid':    
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
        expo_rl_bird=((max(a_r)*28349*a_i)/(1000*b_w))*(1-p_i)
        return (expo_rl_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow granular mammals

def LD50_rg_mamm(Application_type, a_r, a_i, p_i, r_s, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Row/Band/In-furrow-Granular':  
       # a_r = max(rate_out)  
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        n_r=(43560**0.5)/(r_s)
        expo_rg_mamm=(max(a_r)*a_i*453590)/(n_r*(43560**0.5)*b_w)*(1-p_i)
        return (expo_rg_mamm/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow liquid mammals

def LD50_rl_mamm(Application_type, a_r, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Row/Band/In-furrow-Liquid':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)    
        expo_rl_bird=((max(a_r)*28349*a_i)/(1000*b_w))*(1-p_i)
        return (expo_rl_bird/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast granular birds

def LD50_bg_bird(Application_type, a_r, a_i, p_i, aw_bird, at_bird, ld50_bird, tw_bird,x):
    if Application_type=='Broadcast-Granular':    
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        expo_bg_bird=((max(a_r)*a_i*453590)/43560)*(1-p_i)
        return (expo_bg_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast liquid birds

def LD50_bl_bird(Application_type, a_r, a_i, p_i, aw_bird, at_bird, ld50_bird, tw_bird,x):
    if Application_type=='Broadcast-Liquid':   
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        expo_bl_bird=((max(a_r)*28349*a_i)/43560)*(1-p_i)
        return (expo_bl_bird/(at_bird*(aw_bird/1000.0)))    
    else:
        return(0)
        
# LD50ft-2 for broadcast granular mammals

def LD50_bg_mamm(Application_type, a_r, a_i, p_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Broadcast-Granular':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm) 
        expo_bg_mamm=((max(a_r)*a_i*453590)/43560)*(1-p_i)
        return (expo_bg_mamm/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast liquid mammals

def LD50_bl_mamm(Application_type, a_r, a_i, p_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Broadcast-Liquid':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        expo_bl_mamm=((max(a_r)*28349*a_i)/43560)*(1-p_i)
        return (expo_bl_mamm/(at_mamm*(aw_mamm/1000.0)))     
    else:
        return(0)
        
# Seed treatment acute RQ for birds method 1

def sa_bird_1(a_r_p, a_i, den, at_bird,fi_bird, ld50_bird, aw_bird, tw_bird, x):
    at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
    fi_bird=fi_bird(20, 0.1)    
    m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
    nagy_bird=fi_bird*0.001*m_s_a_r/0.02
    return (nagy_bird/at_bird)      
    
# Seed treatment acute RQ for birds method 2

def sa_bird_2(a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird, tw_bird, x):
    at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
    m_a_r=((((a_r_p*a_i)/128)*den)*m_s_r_p)/100    #maximum application rate
    av_ai=m_a_r*1000000/(43560*2.2)
    return (av_ai/(at_bird*0.02))     
    
# Seed treatment chronic RQ for birds

def sc_bird(a_r_p, a_i, den, NOAEC_bird):    
    m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
    return (m_s_a_r/NOAEC_bird)       
    
# Seed treatment acute RQ for mammals method 1

def sa_mamm_1(a_r_p, a_i, den, at_mamm, fi_mamm, ld50_mamm, aw_mamm, tw_mamm):
    at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)     
    fi_mamm=fi_mamm(15, 0.1)    
    m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
    nagy_mamm=fi_mamm*0.001*m_s_a_r/0.015
    return (nagy_mamm/at_mamm)       
    
# Seed treatment acute RQ for mammals method 2

def sa_mamm_2(a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm, tw_mamm):
    at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    m_a_r=((((a_r_p*a_i)/128)*den)*m_s_r_p)/100    #maximum application rate
    av_ai=m_a_r*1000000/(43560*2.2)
    return (av_ai/(at_mamm*0.015))     
      
# Seed treatment chronic RQ for mammals

def sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm,tw_mamm,ANOAEL_mamm):
    ANOAEL_mamm = ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
    m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
    return (m_s_a_r/ANOAEL_mamm)          

    
class TRexOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()   
        chem_name = form.getvalue('chemical_name')
        use = form.getvalue('Use')
        formu_name = form.getvalue('Formulated_product_name')
        a_i = form.getvalue('percent_ai')
        a_i = float(a_i)/100
        Application_type = form.getvalue('Application_type')
        seed_crop = form.getvalue('seed_crop')
        p_i = form.getvalue('percent_incorporated')
        p_i = float(p_i)/100
      #  a_r = form.getvalue('application_rate')
     #   a_r = float(a_r)        
     #   a_r_l = form.getvalue('application_rate_l')
     #   a_r_l=float(a_r_l)        
        seed_treatment_formulation_name = form.getvalue('seed_treatment_formulation_name')
        den = form.getvalue('density_of_product')
        den = float(den)
        m_s_r_p = form.getvalue('maximum_seedling_rate_per_use')
        m_s_r_p = float(m_s_r_p)
        #a_r_p = form.getvalue('application_rate_per_use')
        #a_r_p = float(a_r_p)
        r_s = form.getvalue('row_sp') 
        r_s=float(r_s)
        b_w = form.getvalue('bandwidth')   #convert to ft
        b_w = float(b_w)/12
        n_a = float(form.getvalue('noa'))

        # rate_out = np.zeros(shape=(int(n_a),1))
        # day_out = np.zeros(shape=(int(n_a),1))
        

        # for i in range(int(n_a)):
        #     j=i+1
        #     rate_temp = form.getvalue('rate'+str(j))
        #     rate_out[i,] = int(rate_temp) 
        #     day_temp = form.getvalue('day'+str(j))
        #     day_out[i,] = int(day_temp)         
            
        rate_out = []
        day_out = []
        

        for i in range(int(n_a)):
            j=i+1
            rate_temp = form.getvalue('rate'+str(j))
            rate_out.append(float(rate_temp))
            day_temp = form.getvalue('day'+str(j))
            day_out.append(day_temp)  

        # a_t = form.getvalue('Application_target')
        # if a_t=='Short grass':
        #    para=240       #coefficient used to estimate initial conc.
        # elif a_t=='Tall grass':
        #    para=110
        # elif a_t=='Broad-leafed plants/small insects':
        #    para=135
        # elif a_t=='Fruits/pods/seeds/large insects':
        #    para=15
        # elif a_t=='Arthropods': #new coefficient for Arthropods
        #    para=94
        #i_a = form.getvalue('interval_between_applications')
        if Application_type=='Seed Treatment':
           a_r_p=rate_out[0]       #coefficient used to estimate initial conc.
        else:
           a_r_p=0
        print 'a_r_p', a_r_p
        h_l = form.getvalue('Foliar_dissipation_half_life')
        ld50_bird = form.getvalue('avian_ld50')
        lc50_bird = form.getvalue('avian_lc50')
        NOAEC_bird = form.getvalue('avian_NOAEC')
        NOAEC_bird = float(NOAEC_bird)
        NOAEL_bird = form.getvalue('avian_NOAEL')
        NOAEL_bird = float(NOAEL_bird)
        
#        bird_type = form.getvalue('Bird_type')    
        Species_of_the_tested_bird = form.getvalue('Species_of_the_tested_bird')
        aw_bird_sm = form.getvalue('body_weight_of_the_assessed_bird_small')
        aw_bird_sm = float(aw_bird_sm)  
        aw_bird_md = form.getvalue('body_weight_of_the_assessed_bird_medium')
        aw_bird_md = float(aw_bird_md) 
        aw_bird_lg = form.getvalue('body_weight_of_the_assessed_bird_large')
        aw_bird_lg = float(aw_bird_lg)       
        if Species_of_the_tested_bird == 'Bobwhite quail':
            tw_bird = form.getvalue('bw_quail')
        elif  Species_of_the_tested_bird == 'Mallard duck':
            tw_bird = form.getvalue('bw_duck')  
        else:
            tw_bird = form.getvalue('bwb_other')      

        #tw_bird = form.getvalue('body_weight_of_the_tested_bird')
        tw_bird = float(tw_bird)        
        x = form.getvalue('mineau_scaling_factor')
        ld50_mamm = form.getvalue('mammalian_ld50')
        lc50_mamm = form.getvalue('mammalian_lc50')
        lc50_mamm=float(lc50_mamm)        
        NOAEC_mamm = form.getvalue('mammalian_NOAEC')
        NOAEC_mamm = float(NOAEC_mamm)
        NOAEL_mamm = form.getvalue('mammalian_NOAEL')
#        mammal_type = form.getvalue('Mammal_type')                
#        if mammal_type =='Herbivores and insectivores':
#           mf_w_mamm=0.8       #coefficient used to estimate initial conc.
#        elif mammal_type=='Granivores':
#           mf_w_mamm=0.1 
#        if bird_type =='Herbivores and insectivores':
#           mf_w_bird=0.8       #coefficient used to estimate initial conc.
#        elif bird_type=='Granivores':
#           mf_w_bird=0.1            
        aw_mamm_sm = form.getvalue('body_weight_of_the_assessed_mammal_small')
        aw_mamm_sm = float(aw_mamm_sm)  
        aw_mamm_md = form.getvalue('body_weight_of_the_assessed_mammal_medium')
        aw_mamm_md = float(aw_mamm_md) 
        aw_mamm_lg = form.getvalue('body_weight_of_the_assessed_mammal_large')
        aw_mamm_lg = float(aw_mamm_lg)               
        tw_mamm = form.getvalue('body_weight_of_the_tested_mammal')
        tw_mamm = float(tw_mamm) 
        
        #mf_w_mamm = form.getvalue('mass_fraction_of_water_in_the_mammal_food')
        #mf_w_bird = form.getvalue('mass_fraction_of_water_in_the_bird_food')
        
        text_file = open('trex2/trex2_description.txt','r')
        x1 = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})        
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html',  {'model':'trex2','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                               
        html = html + template.render(templatepath + '04uberoutput_start.html', {
                'model':'trex2', 
                'model_attributes':'T-Rex 1.5.1 Output'})

        html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Inputs</div></th>
                            <th scope="col">Value</div></th>
                            <th scope="col">Inputs</div></th>
                            <th scope="col">Value</div></th>                            
                          </tr>
                          <tr>
                            <td>Chemical name</td>
                            <td>%s</td>
                            <td>Use</td>
                            <td>%s</td>                          
                          </tr>
                          <tr>
                            <td>Formulated product name</td>
                            <td>%s</td>
                            <td>Percentage active ingredient</td>
                            <td>%s%%</td>  
                          </tr>
                          <tr>
                            <td>Application type</td>
                            <td>%s</td>
                            <td>Percentage incorporated</td>
                            <td>%s%%</td>
                          </tr>
                          <tr>
                            <td>Density of product (lbs/gal)</td>
                            <td>%s</td>
                          </tr>                                                    
                          <tr>
                            <td>Number of applications</td>
                            <td>%s</td>
                          </tr>                              
                          <tr>                            
                            <td>Foliar dissipation half-life (days)</td>
                            <td>%s</td>
                          </tr>                              
                          <tr>                            
                            <td>Avian LD50 (mg/kg-bw)</td>
                            <td>%s</td>
                            <td>Avian LC50 (mg/kg-diet)</td>
                            <td>%s</td>
                          </tr>    
                          <tr>                            
                            <td>Avian NOAEC (mg/kg-diet)</td>
                            <td>%s</td>
                            <td>Avian NOAEL (mg/kg-bw)</td>
                            <td>%s</td>
                          </tr>    
                          <tr>                            
                            <td>Body weight of assessed bird (g)</td>
                            <td>%s</td>
                            <td>Body weight of tested bird (g)</td>
                            <td>%s</td>                                                   
                          </tr>    
                          <tr>
                            <td>Mineau scaling factor</td>
                            <td>%s</td>
                            <td>Mammalian LD50 (mg/kg-bw)</td>
                            <td>%s</td>                                                    
                          </tr>    
                          <tr>                            
                            <td>Mammalian LC50 (mg/kg-diet)</td>
                            <td>%s</td>
                            <td>Mammalian NOAEC (mg/kg-diet)</td>
                            <td>%s</td>                                                                             
                          </tr>    
                          <tr>
                            <td>Mammalian NOAEL (mg/kg-bw)</td>
                            <td>%s</td>
                            <td>Body weight of assessed mammal (g)</td>
                            <td>%s</td>
                          </tr>                           
                          <tr>
                            <td>Body weight of tested mammal (g)</td>
                            <td>%s</td>
                            <td>&nbsp;</td>
                            <td>&nbsp;</td>                            
                          </tr>                                                              
                        </table>
                        #<p>&nbsp;</p>                     
                        """%(chem_name, use, formu_name, 100*a_i, Application_type, 100*p_i, den, 
                            n_a, h_l, ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, tw_bird, x, ld50_mamm, 
                               lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm)         
        if Application_type == 'Seed Treatment':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Size</div></th>
                            <th scope="col">Acute #1</div></th> 
                            <th scope="col">Acute #2</div></th>                          
                            <th scope="col">Chronic</div></th>
                            <th scope="col">Acute #1</div></th> 
                            <th scope="col">Acute #2</div></th>                          
                            <th scope="col">Chronic</div></th>  
                          </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          """%(sa_bird_1(a_r_p, a_i, den, at_bird,fi_bird, ld50_bird, aw_bird_sm, tw_bird, x), 
                               sa_bird_2(a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird_sm, tw_bird, x), 
                               sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               sa_mamm_1(a_r_p, a_i, den, at_mamm, fi_mamm, ld50_mamm, aw_mamm_sm, tw_mamm),
                               sa_mamm_2(a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm_sm, tw_mamm),
                               sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_sm,tw_mamm, ANOAEL_mamm),
                               sa_bird_1(a_r_p, a_i, den, at_bird,fi_bird, ld50_bird, aw_bird_md, tw_bird, x), 
                               sa_bird_2(a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird_md, tw_bird, x), 
                               sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               sa_mamm_1(a_r_p, a_i, den, at_mamm, fi_mamm, ld50_mamm, aw_mamm_md, tw_mamm),
                               sa_mamm_2(a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm_md, tw_mamm),
                               sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_md,tw_mamm, ANOAEL_mamm),
                               sa_bird_1(a_r_p, a_i, den, at_bird,fi_bird, ld50_bird, aw_bird_lg, tw_bird, x), 
                               sa_bird_2(a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird_lg, tw_bird, x), 
                               sc_bird(a_r_p, a_i, den, NOAEC_bird),
                               sa_mamm_1(a_r_p, a_i, den, at_mamm, fi_mamm, ld50_mamm, aw_mamm_lg, tw_mamm),
                               sa_mamm_2(a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm_lg, tw_mamm),
                               sc_mamm(a_r_p, a_i, den, NOAEL_mamm,aw_mamm_lg,tw_mamm, ANOAEL_mamm)) 
        else:    
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Dietary based EECs (ppm)</div></th>
                            <th scope="col">Value</div></th>                          
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                          </tr>                           
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>   
                          </tr>                           
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>                        
                          </tr>
                        """%(EEC_diet(C_0, n_a, rate_out, a_i, 240, h_l, day_out),EEC_diet(C_0, n_a, rate_out, a_i, 110, h_l, day_out),EEC_diet(C_0, n_a, rate_out, a_i, 135, h_l, day_out),EEC_diet(C_0, n_a, rate_out, a_i, 15, h_l, day_out),EEC_diet(C_0, n_a, rate_out, a_i, 94, h_l, day_out))                        
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Dosed Based EECs</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Mid</div></th> 
                            <th scope="col">Large</div></th>                    
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                            <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                           <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                           <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                            <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                        """%(EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out), EEC_dose_bird(EEC_diet, aw_bird_sm, fi_bird, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out),EEC_dose_bird(EEC_diet, aw_bird_md, fi_bird, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out),EEC_dose_bird(EEC_diet, aw_bird_lg, fi_bird, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out))                      
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Dosed Based RQs</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Mid</div></th> 
                            <th scope="col">Large</div></th>                    
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>   
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.9, C_0, n_a, rate_out, a_i, 94, h_l, day_out),
                            ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_sm, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_md, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out),ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird_lg, fi_bird, at_bird, ld50_bird, tw_bird, x, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Avian Diet Based RQs</div></th>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th>                  
                          </tr>
                           <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                           <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 240, h_l,day_out),
                            ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, rate_out, a_i, 110, h_l,day_out),
                            CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 110, h_l,day_out),
                            ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, rate_out, a_i, 15, h_l, day_out) ,
                            CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, rate_out, a_i, 94, h_l, day_out) ,
                            CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 94, h_l, day_out)) 
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Mammalian Dose Based EECs (mg/kg-bw)</div></th>
                            <th scope="col">Small</div></th>       
                            <th scope="col">Medium</div></th> 
                            <th scope="col">Large</div></th>                  
                          </tr>
                           <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out),
                            EEC_dose_mamm(EEC_diet, aw_mamm_sm, fi_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_md, fi_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out), EEC_dose_mamm(EEC_diet, aw_mamm_lg, fi_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th rowspan="2">Mammalian Dose Based EECs (mg/kg-bw)</div></th>
                            <td colspan="2">Small</td>
                            <td colspan="2">Medium</td>
                            <td colspan="2">Large</td>
                            </tr>
                            <tr>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th> 
                            <th scope="col">Acute</div></th> 
                            <th scope="col">Chronic</div></th>  
                            <th scope="col">Acute</div></th> 
                            <th scope="col">Chronic</div></th>                  
                          </tr>
                          <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 240, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 240, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 110, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 110, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 135, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.8, C_0, n_a, rate_out, a_i, 94, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.8, n_a, rate_out, a_i, 94, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_sm, ld50_mamm, tw_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_sm, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_md, ld50_mamm, tw_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_md, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm_lg, ld50_mamm, tw_mamm, 0.1, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm_lg, tw_mamm, 0.1, n_a, rate_out, a_i, 15, h_l, day_out))
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">Mammalian Dietary Based RQs (mg/kg-bw)</div></th>
                            <th scope="col">Acute</div></th>       
                            <th scope="col">Chronic</div></th>               
                          </tr>
                            <tr>
                            <td>Short Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Tall Grass</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Broadleaf Plants</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Fruits/Pods/Seeds</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                          <tr>
                            <td>Arthropods</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>
                        """%(ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, rate_out, a_i, 240, h_l, day_out), CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 240, h_l, day_out),
                            ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, rate_out, a_i, 110, h_l, day_out), CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 110, h_l, day_out),
                            ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, rate_out, a_i, 135, h_l, day_out), CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 135, h_l, day_out),
                            ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, rate_out, a_i, 15, h_l, day_out), CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 15, h_l, day_out),
                            ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, rate_out, a_i, 94, h_l, day_out), CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, rate_out, a_i, 94, h_l, day_out))
        if Application_type == 'Row/Band/In-furrow-Granular':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>            
                          """%(LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_sm, at_bird, ld50_bird, tw_bird, x), LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),
                                  LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_md, at_bird, ld50_bird, tw_bird, x), LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),
                                  LD50_rg_bird(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_bird_lg, at_bird, ld50_bird, tw_bird, x), LD50_rg_mamm(Application_type, rate_out, a_i, p_i, r_s, b_w, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))
        elif Application_type == 'Row/Band/In-furrow-Liquid':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                      
                          """%(LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_sm, at_bird, ld50_bird, tw_bird, x), LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),     
                               LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_md, at_bird, ld50_bird, tw_bird, x), LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),     
                               LD50_rl_bird(Application_type, rate_out, a_i, p_i, b_w, aw_bird_lg, at_bird, ld50_bird, tw_bird, x), LD50_rl_mamm(Application_type, rate_out, a_i, p_i, b_w, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))     

        elif Application_type == 'Broadcast-Granular':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                       
                          """%(LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, at_bird, ld50_bird, tw_bird,x), LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),
                              LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, at_bird, ld50_bird, tw_bird,x), LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),
                              LD50_bg_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, at_bird, ld50_bird, tw_bird,x), LD50_bg_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))
        elif Application_type == 'Broadcast-Liquid':
            html = html + """<table width="600" border="1">
                          <tr>
                            <th scope="col">LD50ft-2(mg/kg-bw)</div></th>
                            <th scope="col">Avian</div></th>       
                            <th scope="col">Mammal</div></th>    
                            </tr>
                          <tr>
                            <td>Small</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>  
                          <tr>
                            <td>Medium</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr> 
                          <tr>
                            <td>Large</td>
                            <td>%.2f</td>
                            <td>%.2f</td>
                          </tr>                      
                          """%(LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_sm, at_bird, ld50_bird, tw_bird,x), LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_sm, at_mamm, ld50_mamm, tw_mamm),
                               LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_md, at_bird, ld50_bird, tw_bird,x), LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_md, at_mamm, ld50_mamm, tw_mamm),
                               LD50_bl_bird(Application_type, rate_out, a_i, p_i, aw_bird_lg, at_bird, ld50_bird, tw_bird,x), LD50_bl_mamm(Application_type, rate_out, a_i, p_i, aw_mamm_lg, at_mamm, ld50_mamm, tw_mamm))
        
        html = html + template.render(templatepath + '04uberoutput_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TRexOutputPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

 

    