# Screening Imbibiton Program v1.0 (SIP)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import numpy as np

# Daily water intake rate for birds

def fw_bird(bw_bird):
    try:
        bw_bird = float(bw_bird)
    except IndexError:
        raise IndexError\
        ('The body weight of the bird must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The body weight of the bird must be a real number, not "%g"' % bw_bird)
    if bw_bird < 0:
        raise ValueError\
        ('bw_bird=%g is a non-physical value.' % bw_bird)
    return (1.180 * (bw_bird**0.874))/1000.0


# Daily water intake rate for mammals

def fw_mamm(bw_mamm):
   try:
        bw_mamm = float(bw_mamm)
   except IndexError:
        raise IndexError\
        ('The body weight of the mammal must be supplied on the command line.')
   except ValueError:
        raise ValueError\
        ('The body weight of the mammal must be a real number, not "%g"' % bw_mamm)
   if bw_mamm < 0:
        raise ValueError\
        ('bw_mamm=%g is a non-physical value.' % bw_mamm)
   return (0.708 * (bw_mamm**0.795))/1000.0


# Upper bound estimate of exposure for birds

def dose_bird(fw_bird,sol,bw_bird):
    try:
        fw_bird = float(fw_bird)
        sol = float(sol)
        bw_bird = float(bw_bird)
    except IndexError:
        raise IndexError\
        ('The daily water intake for birds, chemical solubility, and/or'\
        ' the body weight of the bird must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The daily water intake for birds must be a real number, '\
        'not "%L"' %fw_bird)
    except ValueError:
        raise ValueError\
        ('The chemical solubility must be a real number, not "%mg/L"' %sol)
    except ValueError:
        raise ValueError\
        ('The body weight of the bird must be a real number, not "%g"' %bw_bird)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of the bird must non-zero.')
    if fw_bird < 0:
        raise ValueError\
        ('fw_bird=%g is a non-physical value.' % fw_bird)
    if sol < 0:
        raise ValueError\
        ('sol=%g is a non-physical value.' % sol)
    if bw_bird < 0:
        raise ValueError\
        ('bw_bird=%g is a non-physical value.' % bw_bird)
    return (fw_bird * sol)/bw_bird


# Upper bound estimate of exposure for mammals

def dose_mamm(fw_mamm,sol,bw_mamm):
    try:
        fw_mamm = float(fw_mamm)
        sol = float(sol)
        bw_mamm = float(bw_mamm)
    except IndexError:
        raise IndexError\
        ('The daily water intake for mammals, chemical solubility, and/or'\
        ' the body weight of the mammal must be supplied on the command line.')
    except ValueError:
        raise ValueError\
        ('The daily water intake for mammals must be a real number, '\
        'not "%L"' %fw_mamm)
    except ValueError:
        raise ValueError\
        ('The chemical solubility must be a real number, not "%mg/L"' %sol)
    except ValueError:
        raise ValueError\
        ('The body weight of the mammal must be a real number, not "%g"' %bw_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of the mammal must non-zero.')
    if fw_bird < 0:
        raise ValueError\
        ('fw_mamm=%g is a non-physical value.' % fw_mamm)
    if sol < 0:
        raise ValueError\
        ('sol=%g is a non-physical value.' % sol)
    if bw_mamm < 0:
        raise ValueError\
        ('bw_mamm=%g is a non-physical value.' % bw_mamm)
    return (fw_mamm * sol)/bw_mamm


# Acute adjusted toxicity value for birds

def at_bird(ld50,aw_bird,tw_bird,mineau):
    try:
        ld50 = float(ld50)
        aw_bird = float(aw_bird)
        tw_bird = float(tw_bird)
        mineau = float(mineau)
    except IndexError:
        raise IndexError\
        ('The lethal dose, body weight of assessed bird, body weight'\
        ' of tested bird, and/or the mineau scaling factor must be'\
        'supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The mineau scaling factor must be a real number' %mineau)
    except ValueError:
        raise ValueError\
        ('The lethal dose must be a real number, not "%mg/kg"' %ld50)
    except ValueError:
        raise ValueError\
        ('The body weight of assessed bird must be a real number, not "%g"' %aw_bird)
    except ValueError:
        raise ValueError\
        ('The body weight of tested bird must be a real number, not "%g"' %tw_bird)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of tested bird must be non-zero.')
    if ld50 < 0:
        raise ValueError\
        ('ld50=%g is a non-physical value.' % ld50)
    if aw_bird < 0:
        raise ValueError\
        ('aw_bird=%g is a non-physical value.' % aw_bird)
    if tw_bird < 0:
        raise ValueError\
        ('tw_bird=%g is a non-physical value.' % tw_bird)
    return (ld50) * ((aw_bird/tw_bird)**(mineau-1))




# Acute adjusted toxicity value for mammals

def at_mamm(ld50,aw_mamm,tw_mamm):
    try:
        ld50 = float(ld50)
        aw_mamm = float(aw_mamm)
        tw_mamm = float(tw_mamm)
    except IndexError:
        raise IndexError\
        ('The lethal dose, body weight of assessed mammal, and/or body weight'\
        ' of tested mammal, must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The lethal dose must be a real number, not "%mg/kg"' %ld50)
    except ValueError:
        raise ValueError\
        ('The body weight of assessed mammal must be a real number, not "%g"' %aw_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of tested mammal must be a real number, not "%g"' %tw_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of tested mammal must be non-zero.')
    if ld50 < 0:
        raise ValueError\
        ('ld50=%g is a non-physical value.' % ld50)
    if aw_mamm < 0:
        raise ValueError\
        ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    if tw_mamm < 0:
        raise ValueError\
        ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    return (ld50) * ((aw_mamm/tw_mamm)**0.25)


# Adjusted chronic toxicity values for birds

# FI = Food Intake Rate

def fi_bird(bw_bird):
    try:
        bw_bird = float(bw_bird)
    except IndexError:
        raise IndexError\
        ('The body weight of the bird must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The body weight must be a real number, not "%kg"' %bw_bird)
    if bw_bird < 0:
        raise ValueError\
        ('bw_bird=%g is a non-physical value.' % bw_bird)
    return 0.0582 * (bw_bird**0.651)


# Dose-equivalent chronic toxicity value for birds

def det(noaec,fi_bird,bw_bird):
    try:
        noaec = float(noaec)
        fi_bird = float(fi_bird)
        bw_bird = float(bw_bird)
    except IndexError:
        raise IndexError\
        ('The no observed adverse effects concentration, daily food intake'\
        ' rate for birds, and/or body weight of the bird must be supplied the'\
        ' command line.')
    except ValueError:
        raise ValueError\
        ('The NOAEC must be a real number, not "%mg/kg"' % noaec)
    except ValueError:
        raise ValueError\
        ('The dialy food intake rate for birds must be a real number,'\
        ' not "%kg"' % fi_bird)
    except ValueError:
        raise ValueError\
        ('The body weight of the bird must be a real number, not "%kg"' % bw_bird)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of the bird must be non-zero.')
    if noaec < 0:
        raise ValueError\
        ('noaec=%g is a non-physical value.' % noaec)
    if fi_bird < 0:
        raise ValueError\
        ('fi_bird=%g is a non-physical value.' % fi_bird)
    if bw_bird < 0:
        raise ValueError\
        ('bw_bird=%g is a non-physical value.' % bw_bird)
    return (noaec * fi_bird)/bw_bird

# Adjusted chronic toxicty value for mammals

def act(noael,tw_mamm,aw_mamm):
    try:
        noael = float(noael)
        tw_mamm = float(tw_mamm)
        aw_mamm = float(aw_mamm)
    except IndexError:
        raise IndexError\
        ('The no observed adverse effects level, body weight of the tested'\
        ' mammal, and/or body weight of assessed mammal must be supplied the'\
        ' command line.')
    except ValueError:
        raise ValueError\
        ('The NOAEL must be a real number, not "%mg/kg"' % noael)
    except ValueError:
        raise ValueError\
        ('The body weight of the tested mammal must be a real number,'\
        ' not "%kg"' % tw_mamm)
    except ValueError:
        raise ValueError\
        ('The body weight of the assessed mammal must be a real number,'\
        ' not "%kg"' % aw_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The body weight of the assessed mammal must be non-zero.')
    if noael < 0:
        raise ValueError\
        ('noael=%g is a non-physical value.' % noael)
    if tw_mamm < 0:
        raise ValueError\
        ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    if aw_mamm < 0:
        raise ValueError\
        ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    return (noael) * ((tw_mamm/aw_mamm)**0.25)

# ---- Is drinking water a concern?

# Acute exposures for birds


def acute_bird(dose_bird,at_bird):
    try:
        dose_bird = float(dose_bird)
        at_bird = float(at_bird)
    except IndexError:
        raise IndexError\
        ('The upper bound estimate of exposure for birds, and/or the adjusted'\
        ' toxicity value for birds must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The upper bound estimate of exposure for birds must be a real'\
        ' number, not "%mg/kg"' % dose_bird)
    except ValueError:
        raise ValueError\
        ('The adjusted toxicity value for birds must be a real number,'\
        ' not "%mg/kg"' % at_bird)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The adjusted toxicity value for birds must be non-zero.')
    if dose_bird < 0:
        raise ValueError\
        ('dose_bird=%g is a non-physical value.' % dose_bird)
    if at_bird < 0:
        raise ValueError\
        ('at_bird=%g is a non-physical value.' % at_bird)
    return dose_bird/at_bird


def acuconb(acute_bird):
    if acute_bird < 0.1:
        return ('Drinking water exposure alone is NOT a potential concern for birds')
    else:
        return ('Exposure through drinking water alone is a potential concern for birds')

# Acute exposures for mammals

def acute_mamm(dose_mamm,at_mamm):
    try:
        dose_mamm = float(dose_mamm)
        at_mamm = float(at_mamm)
    except IndexError:
        raise IndexError\
        ('The upper bound estimate of exposure for mammals, and/or the adjusted'\
        ' toxicity value for mammals must be supplied the command line.')
    except ValueError:
        raise ValueError\
        ('The upper bound estimate of exposure for mammals must be a real'\
        ' number, not "%mg/kg"' % dose_mamm)
    except ValueError:
        raise ValueError\
        ('The adjusted toxicity value for mammals must be a real number,'\
        ' not "%mg/kg"' % at_mamm)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The adjusted toxicity value for mammals must be non-zero.')
    if dose_mamm < 0:
        raise ValueError\
        ('dose_mamm=%g is a non-physical value.' % dose_mamm)
    if at_mamm < 0:
        raise ValueError\
        ('at_mamm=%g is a non-physical value.' % at_mamm)
    return dose_mamm/at_mamm


def acuconm(acute_mamm):
    if acute_mamm < 0.1:
        return ('Drinking water exposure alone is NOT a potential concern for mammals')
    else:
        return ('Exposure through drinking water alone is a potential concern for mammals')


# Chronic Exposures for birds

def chron_bird(dose_bird,det):
    try:
        dose_bird = float(dose_bird)
        det = float(det)
    except IndexError:
        raise IndexError\
        ('The upper bound estimate of exposure for birds, and/or the dose-'\
        'equivalent chronic toxicity value for birds must be supplied the'\
        ' command line.')
    except ValueError:
        raise ValueError\
        ('The upper bound estimate of exposure for birds must be a real'\
        ' number, not "%mg/kg"' % dose_bird)
    except ValueError:
        raise ValueError\
        ('The dose-equivalent chronic toxicity value for birds must be a real'\
        ' number, not "%mg/kg"' % det)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The dose-equivalent chronic toxicity value for birds must be non-zero.')
    if dose_bird < 0:
        raise ValueError\
        ('dose_bird=%g is a non-physical value.' % dose_bird)
    if det < 0:
        raise ValueError\
        ('det=%g is a non-physical value.' % det)
    return dose_bird/det


def chronconb(chron_bird):
    if chron_bird < 1:
        return ('Drinking water exposure alone is NOT a potential concern for birds')
    else:
        return ('Exposure through drinking water alone is a potential concern for birds')

# Chronic exposures for mammals

def chron_mamm(dose_mamm,act):
    try:
        dose_mamm = float(dose_mamm)
        act = float(act)
    except IndexError:
        raise IndexError\
        ('The upper bound estimate of exposure for mammals, and/or the'\
        ' adjusted chronic toxicity value for mammals must be supplied the'\
        ' command line.')
    except ValueError:
        raise ValueError\
        ('The upper bound estimate of exposure for mammals must be a real'\
        ' number, not "%mg/kg"' % dose_mamm)
    except ValueError:
        raise ValueError\
        ('The adjusted chronic toxicity value for mammals must be a real'\
        ' number, not "%mg/kg"' % act)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The adjusted chronic toxicity value for mammals must be non-zero.')
    if dose_mamm < 0:
        raise ValueError\
        ('dose_mamm=%g is a non-physical value.' % dose_mamm)
    if act < 0:
        raise ValueError\
        ('act=%g is a non-physical value.' % act)
    return dose_mamm/act

def chronconm(chron_mamm):
    if chron_mamm < 1:
        return ('Drinking water exposure alone is NOT a potential concern for mammals')
    else:
        return ('Exposure through drinking water alone is a potential concern for mammals')

