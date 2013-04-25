import numpy as np
import logging
import sys

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
    
#Dietary based EECs

def EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l):
    C_0=C_0(a_r, a_i, para)
    try:
        n_a = float(n_a)
        i_a = float(i_a)        
    except IndexError:
        raise IndexError\
        ('The number of applications, and/or the interval between applications '\
         'must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The number of applications must be a real number, not "%g"' % n_a)        
    except ValueError:
        raise ValueError\
        ('The interval between applications must be a real number, not "%g"' % i_a)                
    if n_a < 0:
        raise ValueError\
        ('The number of applications=%g is a non-physical value.' % n_a)    
    if i_a < 0:
        raise ValueError\
        ('The interval between applications=%g is a non-physical value.' % i_a)      
    if a_i*n_a > 365:
        raise ValueError\
        ('The schduled application=%g is over the modeling period (1 year).' % i_a*n_a)     

    #C_temp=[1.0]*365 #empty array to hold the concentrations over days   
    C_temp=np.ones((365,1)) #empty array to hold the concentrations over days       
    a_p_temp=0  #application period temp  
    n_a_temp=0  #number of existed applications
    
    for i in range (0,365):
        if i==0: 
            a_p_temp=0
            n_a_temp=n_a_temp+1
            C_temp[i]=C_0
        elif a_p_temp==(i_a-1) and n_a_temp<n_a:
            a_p_temp=0
            n_a_temp=n_a_temp+1
            C_temp[i]=C_t(C_temp[i-1], h_l)+C_0        
        elif a_p_temp<(i_a-1) and n_a_temp<=n_a:
            a_p_temp=a_p_temp+1
            C_temp[i]=C_t(C_temp[i-1], h_l)        
        else :
            C_temp[i]=C_t(C_temp[i-1], h_l) 
    return (max(C_temp))

# Dose based EECs for birds

def EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    n_a = float(n_a)
    i_a = float(i_a)      
    aw_bird = float(aw_bird)
    mf_w_bird = float(mf_w_bird)
    a_r = float(a_r)
    a_i = float(a_i)
    para = float(para)
    h_l = float(h_l)
        
    fi_bird = fi_bird(aw_bird, mf_w_bird)
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)
    return (EEC_diet*fi_bird/aw_bird)

# Dose based EECs for granivores birds

def EEC_dose_bird_g(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    if para==15:
        n_a = float(n_a)
        i_a = float(i_a)      
        aw_bird = float(aw_bird)
        mf_w_bird = float(mf_w_bird)
        a_r = float(a_r)
        a_i = float(a_i)
        para = float(para)
        h_l = float(h_l)        
        fi_bird = fi_bird(aw_bird, mf_w_bird)
        EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)
        return (EEC_diet*fi_bird/aw_bird)
    else:
        return(0)
        
# Dose based EECs for mammals

def EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    aw_mamm = float(aw_mamm)
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)
    fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    return (EEC_diet*fi_mamm/aw_mamm)

# Dose based EECs for granivores mammals

def EEC_dose_mamm_g(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    if para==15:    
        aw_mamm = float(aw_mamm)
        EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)
        fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
        return (EEC_diet*fi_mamm/aw_mamm)
    else:
        return(0)
        
# Acute dose-based risk quotients for birds

def ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l)
    at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
    return (EEC_dose_bird/at_bird)

# Acute dose-based risk quotients for granivores birds

def ARQ_dose_bird_g(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    if para==15:
        EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, n_a, i_a, a_r, a_i, para, h_l)
        at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
        return (EEC_dose_bird/at_bird)
    else:
        return (0)
    
# Acute dose-based risk quotients for mammals

def ARQ_dose_mamm(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l)
    at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    return (EEC_dose_mamm/at_mamm)

# Acute dose-based risk quotients for granivores mammals

def ARQ_dose_mamm_g(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    if para==15:    
        EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l)
        at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        return (EEC_dose_mamm/at_mamm)
    else:
        return(0)
        
# Acute dietary-based risk quotients for birds

def ARQ_diet_bird(EEC_diet, lc50_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)    
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

def ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)    
    return (EEC_diet/lc50_mamm)

# Chronic dietary-based risk quotients for birds

def CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)    
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

def CRQ_diet_mamm(EEC_diet, NOAEC_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l):
    EEC_diet=EEC_diet(C_0, n_a, i_a, a_r, a_i, para, h_l)
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

def CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, i_a, a_r, a_i, para, h_l):
    ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l)     
    return (EEC_dose_mamm/ANOAEL_mamm)

# Chronic dose-based risk quotients for granviores mammals

def CRQ_dose_mamm_g(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, i_a, a_r, a_i, para, h_l):
    if para==15:    
        ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
        EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, n_a, i_a, a_r, a_i, para, h_l)     
        return (EEC_dose_mamm/ANOAEL_mamm)
    else:
        return (0)
        
# LD50ft-2 for row/band/in-furrow granular birds

def LD50_rg_bird(Application_type, a_r, a_i, p_i, r_s, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x): 
    if Application_type=='Row/Band/In-furrow-Granular':     
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        n_r=(43560**0.5)/(r_s)
        expo_rg_bird=(a_r*a_i*453590)/(n_r*(43560**0.5)*b_w)*(1-p_i)
        return (expo_rg_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow liquid birds

def LD50_rl_bird(Application_type, a_r_l, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if Application_type=='Row/Band/In-furrow-Liquid':    
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)    
        expo_rl_bird=((a_r_l*28349*a_i)/(1000*b_w))*(1-p_i)
        return (expo_rl_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow granular mammals

def LD50_rg_mamm(Application_type, a_r, a_i, p_i, r_s, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Row/Band/In-furrow-Granular':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        n_r=(43560**0.5)/(r_s)
        expo_rg_mamm=(a_r*a_i*453590)/(n_r*(43560**0.5)*b_w)*(1-p_i)
        return (expo_rg_mamm/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for row/band/in-furrow liquid mammals

def LD50_rl_mamm(Application_type, a_r_l, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Row/Band/In-furrow-Liquid':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)    
        expo_rl_bird=((a_r_l*28349*a_i)/(1000*b_w))*(1-p_i)
        return (expo_rl_bird/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast granular birds

def LD50_bg_bird(Application_type, a_r, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird,x):
    if Application_type=='Broadcast-Granular':    
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        expo_bg_bird=((a_r*a_i*453590)/43560)*(1-p_i)
        return (expo_bg_bird/(at_bird*(aw_bird/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast liquid birds

def LD50_bl_bird(Application_type, a_r_l, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird,x):
    if Application_type=='Broadcast-Liquid':   
        at_bird=at_bird(ld50_bird,aw_bird,tw_bird,x)
        expo_bl_bird=((a_r_l*28349*a_i)/43560)*(1-p_i)
        return (expo_bl_bird/(at_bird*(aw_bird/1000.0)))    
    else:
        return(0)
        
# LD50ft-2 for broadcast granular mammals

def LD50_bg_mamm(Application_type, a_r, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Broadcast-Granular':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm) 
        expo_bg_mamm=((a_r*a_i*453590)/43560)*(1-p_i)
        return (expo_bg_mamm/(at_mamm*(aw_mamm/1000.0)))
    else:
        return(0)
        
# LD50ft-2 for broadcast liquid mammals

def LD50_bl_mamm(Application_type, a_r_l, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if Application_type=='Broadcast-Liquid':    
        at_mamm=at_mamm(ld50_mamm,aw_mamm,tw_mamm)
        expo_bl_mamm=((a_r_l*28349*a_i)/43560)*(1-p_i)
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

def sc_mamm(a_r_p, a_i, den, NOAEC_mamm):
    m_s_a_r=((a_r_p*a_i)/128)*den*10000    #maximum seed application rate=application rate*10000
    return (m_s_a_r/NOAEC_mamm)          
    