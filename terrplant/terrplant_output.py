# TerrPlant Version 1.2.2


import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import numpy as np
import cgi
import cgitb
cgitb.enable()
import logging
import sys
sys.path.append("../utils")
import utils.json_utils



#import csv as TerrPlant
#import numpy as N
#
#PyPestDir = str()
##PyPestDir = 'C:\\Documents and Settings\\jharston\\Desktop\\jharston_dropbox\\Dropbox\\pypest'
#PyPestDir = 'C:\\Dropbox\\Dropbox\\pypest'
#
#TerrPlantReader = TerrPlant.reader(open(PyPestDir+'\\TerrPlant\\TerrPlant.input.csv')
#    ,delimiter=',')
#arr = N.loadtxt(PyPestDir+'\\TerrPlant\TerrPlant.input.csv',dtype={'names': ('parameter', 'value', 'units'),'formats': ('c', 'f', 'c')},delimiter=',')
#
#A = arr[0,][1]
#I = arr[1,][1]
#R = arr[2,][1]
#D = arr[3,][1]
#nms = arr[4,][1]
#lms = arr[5,][1]
#nds = arr[6,][1]
#lds = arr[7,][1]
#
#TerrPlantDict = dict()
#
#TerrPlantDict['A'] = arr[0,][1]
#TerrPlantDict['I'] = arr[1,][1]
#TerrPlantDict['R'] = arr[2,][1]
#TerrPlantDict['D'] = arr[3,][1]
#TerrPlantDict['nms'] = arr[4,][1]
#TerrPlantDict['lms'] = arr[5,][1]
#TerrPlantDict['nds'] = arr[6,][1]
#TerrPlantDict['lds'] = arr[7,][1]

# EEC = Estimated Environmental Concentration

# EEC for runoff to dry areas

def rundry(A,I,R):
    try:
        A = float(A)
        I = float(I)
        R = float(R)
    except ZeroDivisionError:
        raise ZeroDivisionError
        print('The incorporation must be non-zero.')
        raise IndexError 
        print('The application rate, incorporation, and runoff fraction must all be supplied.')
    if A < 0:
        raise ValueError
        print('A must be positive.')
    if I < 0:
        raise ValueError
        print('I must be positive.')
    if R < 0:
        raise ValueError
        print('R must be positive.')
    return (A/I) * R


# EEC for runoff to semi-aquatic areas

def runsemi(A,I,R):
    try:
        A = float(A)
        I = float(I)
        R = float(R)
    except IndexError:
        raise IndexError\
        ('The application rate, incorporation, and/or runoff fraction must be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The application rate must be a real number, not "%lbs ai/A"' % A)
    except ValueError:
        raise ValueError\
        ('The incorporation must be a real number.' %I)
    except ValueError:
        raise ValueError\
        ('The runoff fraction must be a real number.' %R)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The incorporation must be non-zero.')
    if A < 0:
        raise ValueError\
        ('A=%g is a non-physical value.' %A)
    if I < 0:
        raise ValueError\
        ('I=%g is a non-physical value' %I)
    if R < 0:
        raise ValueError\
        ('R=%g is a non-physical value' %R)
    return (A/I) * R * 10


# EEC for spray drift

def spray(A,D):
    try:
        A = float(A)
        D = float(D)
    except IndexError:
        raise IndexError\
        ('The application rate, and/or drift fraction must'\
        ' be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The application rate must be a real number, not "%lbs ai/A"' %A)
    except ValueError:
        raise ValueError\
        ('The drift fraction must be a real number.' %D)
    if A < 0:
        raise ValueError\
        ('A=%g is a non-physical value.' %A)
    if D < 0:
        raise ValueError\
        ('D=%g is a non-physical value' %D)
    return A * D


# EEC total for dry areas

def totaldry(rundry,spray):
    return rundry + spray


# EEC total for semi-aquatic areas

def totalsemi (runsemi,spray):
    return runsemi + spray


# EC25 --> non-listed species
# NOAEC --> listed species

# ALL USER INPUTS

# EC25 (Non-listed) Monocot Seedling (nms)
# NOAEC (Listed) Monocot Seedling (lms)
# EC25 (Non-listed) Dicot Seedling (nds)
# NOAEC (Listed) Dicot Seedling (lds)
# EC25 (Non-listed) Monocot Vegetative (nmv)
# NOAEC (Listed) Monocot Vegetative (lmv)
# EC25 (Non-listed) Dicot Vegetative (ndv)
# NOAEC (Listed) Dicot Vegetative (ldv)


# Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a DRY area

def nmsRQdry(totaldry,nms):
    try:
        totaldry = float(totaldry)
        nms = float(nms)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to dry areas and/or EC25 for monocot'\
        ' seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to dry areas must be a real number,'\
        ' not "%lbs ai/A"' %totaldry)
    except ValueError:
        raise ValueError\
        ('The EC25 for monocot seedlings must be a real number.' %nms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for monocot seedlings must be non-zero.')
    if totaldry < 0:
        raise ValueError\
        ('totaldry=%g is a non-physical value.' %totaldry)
    if nms < 0:
        raise ValueError\
        ('nms=%g is a non-physical value' %nms)
    return totaldry/nms



# Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area

def LOCnmsdry(nmsRQdry):
    if nmsRQdry >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via runoff to a dry area indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via runoff to a dry area indicates that potential risk is minimal.')


# Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area

def nmsRQsemi(totalsemi,nms):
    try:
        totalsemi = float(totalsemi)
        nms = float(nms)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to semi-aquatic areas and/or'\
        ' EC25 for monocot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to semi-aquatic areas must be a'\
        ' real number, not "%lbs ai/A"' %totalsemi)
    except ValueError:
        raise ValueError\
        ('The EC25 for monocot seedlings must be a real number.' %nms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for monocot seedlings must be non-zero.')
    if totalsemi < 0:
        raise ValueError\
        ('totalsemi=%g is a non-physical value.' %totalsemi)
    if nms < 0:
        raise ValueError\
        ('nms=%g is a non-physical value' %nms)
    return totalsemi/nms

# Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area

def LOCnmssemi(nmsRQsemi):
    if nmsRQdry >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to the'\
    ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')


# Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift

def nmsRQspray(spray,nms):
    try:
        spray = float(spray)
        nms = float(nms)
    except IndexError:
        raise IndexError\
        ('The the amount of spray drift exposure and/or EC25 for monocot'\
        ' seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The amount of spray drift exposure must be a real number,'\
        ' not "%lbs ai/A"' %spray)
    except ValueError:
        raise ValueError\
        ('The EC25 for monocot seedlings must be a real number.' %nms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for monocot seedlings must be non-zero.')
    if spray < 0:
        raise ValueError\
        ('spray=%g is a non-physical value.' %spray)
    if nms < 0:
        raise ValueError\
        ('nms=%g is a non-physical value' %nms)
    return spray/nms

# Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift

def LOCnmsspray(nmsRQspray):
    if nmsRQspray >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via spray drift indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to the'\
    ' pesticide via spray drift indicates that potential risk is minimal.')


# Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas

def lmsRQdry(totaldry,lms):
    try:
        totaldry = float(totaldry)
        lms = float(lms)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to dry areas and/or NOAEC for'\
        ' monocot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to dry areas must be a real number,'\
        ' not "%lbs ai/A"' %totaldry)
    except ValueError:
        raise ValueError\
        ('The NOAEC for monocot seedlings must be a real number.' %lms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for monocot seedlings must be non-zero.')
    if totaldry < 0:
        raise ValueError\
        ('totaldry=%g is a non-physical value.' %totaldry)
    if lms < 0:
        raise ValueError\
        ('lms=%g is a non-physical value' %lms)
    return totaldry/lms

# Level of concern for listed monocot seedlings exposed to pesticide
#  via runoff in a dry area

def LOClmsdry(lmsRQdry):
    if lmsRQdry >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via runoff to a dry area indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via runoff to a dry area indicates that potential risk is minimal.')


# Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area

def lmsRQsemi(totalsemi,lms):
    try:
        totalsemi = float(totalsemi)
        lms = float(lms)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to semi-aquatic areas and/or'\
        ' NOAEC for monocot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to semi-aquatic areas must be a'\
        ' real number, not "%lbs ai/A"' %totalsemi)
    except ValueError:
        raise ValueError\
        ('The NOAEC for monocot seedlings must be a real number.' %lms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for monocot seedlings must be non-zero.')
    if totalsemi < 0:
        raise ValueError\
        ('totalsemi=%g is a non-physical value.' %totalsemi)
    if lms < 0:
        raise ValueError\
        ('lms=%g is a non-physical value' %lms)
    return totalsemi/lms

# Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas

def LOClmssemi(lmsRQsemi):
    if lmsRQsemi >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')


# Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift

def lmsRQspray(spray,lms):
    try:
        spray = float(spray)
        lms = float(lms)
    except IndexError:
        raise IndexError\
        ('The the amount of spray drift exposure and/or NOAEC for monocot'\
        ' seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The amount of spray drift exposure must be a real number,'\
        ' not "%lbs ai/A"' %spray)
    except ValueError:
        raise ValueError\
        ('The NOAEC for monocot seedlings must be a real number.' %lms)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for monocot seedlings must be non-zero.')
    if spray < 0:
        raise ValueError\
        ('spray=%g is a non-physical value.' %spray)
    if lms < 0:
        raise ValueError\
        ('lms=%g is a non-physical value' %lms)
    return spray/lms

# Level of concern for listed monocot seedlings exposed to pesticide X via spray drift

def LOClmsspray(lmsRQspray):
    if lmsRQspray >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via spray drift indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via spray drift indicates that potential risk is minimal.')


# Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas

def ndsRQdry(totaldry,nds):
    try:
        totaldry = float(totaldry)
        nds = float(nds)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to dry areas and/or EC25 for dicot'\
        ' seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to dry areas must be a real number,'\
        ' not "%lbs ai/A"' %totaldry)
    except ValueError:
        raise ValueError\
        ('The EC25 for dicot seedlings must be a real number.' %nds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for dicot seedlings must be non-zero.')
    if totaldry < 0:
        raise ValueError\
        ('totaldry=%g is a non-physical value.' %totaldry)
    if nds < 0:
        raise ValueError\
        ('nds=%g is a non-physical value' %nds)
    return totaldry/nds

# Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas

def LOCndsdry(ndsRQdry):
    if ndsRQdry >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via runoff to dry areas indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to the'\
    ' pesticide via runoff to dry areas indicates that potential risk is minimal.')


# Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas

def ndsRQsemi(totalsemi,nds):
    try:
        totalsemi = float(totalsemi)
        nds = float(nds)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to semi-aquatic areas and/or'\
        ' EC25 for dicot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to semi-aquatic areas must be a'\
        ' real number, not "%lbs ai/A"' %totalsemi)
    except ValueError:
        raise ValueError\
        ('The EC25 for dicot seedlings must be a real number.' %nds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for dicot seedlings must be non-zero.')
    if totalsemi < 0:
        raise ValueError\
        ('totalsemi=%g is a non-physical value.' %totalsemi)
    if nds < 0:
        raise ValueError\
        ('nds=%g is a non-physical value' %nds)
    return totalsemi/nds

# Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas

def LOCndssemi(ndsRQsemi):
    if ndsRQsemi >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to the'\
    ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')

# Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift

def ndsRQspray(spray,nds):
    try:
        spray = float(spray)
        nds = float(nds)
    except IndexError:
        raise IndexError\
        ('The the amount of spray drift exposure and/or EC25 for dicot'\
        ' seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The amount of spray drift exposure must be a real number,'\
        ' not "%lbs ai/A"' %spray)
    except ValueError:
        raise ValueError\
        ('The EC25 for dicot seedlings must be a real number.' %nds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The EC25 for dicot seedlings must be non-zero.')
    if spray < 0:
        raise ValueError\
        ('spray=%g is a non-physical value.' %spray)
    if nds < 0:
        raise ValueError\
        ('nds=%g is a non-physical value' %nds)
    return spray/nds

# Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift

def LOCndsspray(ndsRQspray):
    if ndsRQspray >= 1.0:
        return ('The risk quotient for non-listed monocot seedlings exposed to'\
    ' the pesticide via spray drift indicates a potential risk.')
    else:
        return ('The risk quotient for non-listed monocot seedlings exposed to the'\
    ' pesticide via spray drift indicates that potential risk is minimal.')

# Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas

def ldsRQdry(totaldry,lds):
    try:
        totaldry = float(totaldry)
        lds = float(lds)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to dry areas and/or NOAEC for'\
        ' dicot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to dry areas must be a real number,'\
        ' not "%lbs ai/A"' %totaldry)
    except ValueError:
        raise ValueError\
        ('The NOAEC for dicot seedlings must be a real number.' %lds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for dicot seedlings must be non-zero.')
    if totaldry < 0:
        raise ValueError\
        ('totaldry=%g is a non-physical value.' %totaldry)
    if lds < 0:
        raise ValueError\
        ('lds=%g is a non-physical value' %lds)
    return totaldry/lds

# Level of concern for listed dicot seedlings exposed to pesticideX in dry areas

def LOCldsdry(ldsRQdry):
    if ldsRQdry >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via runoff to dry areas indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via runoff to dry areas indicates that potential risk is minimal.')

# Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas

def ldsRQsemi(totalsemi,lds):
    try:
        totalsemi = float(totalsemi)
        lds = float(lds)
    except IndexError:
        raise IndexError\
        ('The total amount of runoff and spray to semi-aquatic areas and/or'\
        ' NOAEC for dicot seedlings be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The total amount of runoff and spray to semi-aquatic areas must be a'\
        ' real number, not "%lbs ai/A"' %totalsemi)
    except ValueError:
        raise ValueError\
        ('The NOAEC for dicot seedlings must be a real number.' %lds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for dicot seedlings must be non-zero.')
    if totalsemi < 0:
        raise ValueError\
        ('totalsemi=%g is a non-physical value.' %totalsemi)
    if lds < 0:
        raise ValueError\
        ('lds=%g is a non-physical value' %lds)
    return totalsemi/lds

# Level of concern for listed dicot seedlings exposed to pesticide X in dry areas

def LOCldssemi(ldsRQsemi):
    if ldsRQsemi >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')

# Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift

def ldsRQspray(spray,lds):
    try:
        spray = float(spray)
        lds = float(lds)
    except IndexError:
        raise IndexError\
        ('The amount of spray drift exposure and/or NOAEC for dicot'\
        ' seedlings must be supplied on the command line. ')
    except ValueError:
        raise ValueError\
        ('The amount of spray drift exposure must be a real number,'\
        ' not "%lbs ai/A"' %spray)
    except ValueError:
        raise ValueError\
        ('The NOAEC for dicot seedlings must be a real number.' %lds)
    except ZeroDivisionError:
        raise ZeroDivisionError\
        ('The NOAEC for dicot seedlings must be non-zero.')
    if spray < 0:
        raise ValueError\
        ('spray=%g is a non-physical value.' %spray)
    if lds < 0:
        raise ValueError\
        ('lds=%g is a non-physical value' %lds)
    return spray/lds

# Level of concern for listed dicot seedlings exposed to pesticide X via spray drift

def LOCldsspray(ldsRQspray):
    if ldsRQspray >= 1.0:
        return ('The risk quotient for listed monocot seedlings exposed to'\
    ' the pesticide via spray drift indicates a potential risk.')
    else:
        return ('The risk quotient for listed monocot seedlings exposed to the'\
    ' pesticide via spray drift indicates that potential risk is minimal.')


#f = open(PyPestDir+'\TerrPlant\TerrPlant.output.csv', 'wt')
#
#try:
#    writer = TerrPlant.writer(f)
#    writer.writerow( ('Parameter', 'Value', 'Units') )
#    writer.writerow( ('EEC for Runoff to Dry Areas', rundry(A,I,R), 'lbs ai/A') )
#    writer.writerow( ('EEC for Runoff to Semi Aquatic Area', runsemi(A,I,R), 'lbs ai/A') )
#    writer.writerow( ('EEC for Spray Drift', spray(A,D), 'lbs ai/A') )
#    writer.writerow( ('EEC Total for Dry Areas', totaldry(rundry(A,I,R),spray(A,D)), 'lbs ai/A') )
#    writer.writerow( ('EEC Total for Semi-aquatic Areas', totalsemi(runsemi(A,I,R),spray(A,D)), 'lbs ai/A') )
#    writer.writerow( ('Risk Quotient for non-listed monocot seedlings exposed to a pesticide in dry areas', nmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nms), '') )
#    writer.writerow( ('Level of concern for non-listed monocot seedlings exposed to pesticide in a dry area', LOCnmsdry(nmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nms)), '') )
#    writer.writerow( ('Risk Quotient for non-listed monocot seedlings exposed to a pesticide in semi-aquatic areas', nmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nms), '') )
#    writer.writerow( ('Level of concern for non-listed monocot seedlings exposed to pesticide in a semi-aquatic area', LOCnmssemi(nmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nms)), '') )
#    writer.writerow( ('Risk Quotient for non-listed monocot seedlings exposed to pesticide via spray drift', nmsRQspray(spray(A,D),nms), '') )
#    writer.writerow( ('Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift', LOCnmsspray(nmsRQspray(spray(A,D),nms)), '') )
#    writer.writerow( ('Risk Quotient for listed monocot seedlings exposed to a pesticide in dry areas', lmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lms), '') )
#    writer.writerow( ('Level of concern for listed monocot seedlings exposed to pesticide in a dry area', LOClmsdry(lmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lms)), '') )
#    writer.writerow( ('Risk Quotient for listed monocot seedlings exposed to a pesticide in semi-aquatic areas', lmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lms), '') )
#    writer.writerow( ('Level of concern for listed monocot seedlings exposed to pesticide in a semi-aquatic area', LOClmssemi(lmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lms)), '') )
#    writer.writerow( ('Risk Quotient for listed monocot seedlings exposed to pesticide via spray drift', lmsRQspray(spray(A,D),lms), '') )
#    writer.writerow( ('Level of concern for listed monocot seedlings exposed to pesticide via spray drift', LOClmsspray(lmsRQspray(spray(A,D),lms)), '') )
#    writer.writerow( ('Risk Quotient for non-listed dicot seedlings exposed to a pesticide in dry areas', ndsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nds), '') )
#    writer.writerow( ('Level of concern for non-listed dicot seedlings exposed to pesticide in a dry area', LOCndsdry(ndsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nds)), '') )
#    writer.writerow( ('Risk Quotient for non-listed dicot seedlings exposed to a pesticide in semi-aquatic areas', ndsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nds), '') )
#    writer.writerow( ('Level of concern for non-listed dicot seedlings exposed to pesticide in a semi-aquatic area', LOCndssemi(ndsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nds)), '') )
#    writer.writerow( ('Risk Quotient for non-listed dicot seedlings exposed to pesticide via spray drift', ndsRQspray(spray(A,D),nds), '') )
#    writer.writerow( ('Level of concern for non-listed dicot seedlings exposed to pesticide via spray drift', LOCndsspray(ndsRQspray(spray(A,D),nds)), '') )
#    writer.writerow( ('Risk Quotient for listed dicot seedlings exposed to a pesticide in dry areas', ldsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lds), '') )
#    writer.writerow( ('Level of concern for listed dicot seedlings exposed to pesticide in a dry area', LOCldsdry(ldsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lds)), '') )
#    writer.writerow( ('Risk Quotient for listed dicot seedlings exposed to a pesticide in semi-aquatic areas', ldsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lds), '') )
#    writer.writerow( ('Level of concern for listed dicot seedlings exposed to pesticide in a semi-aquatic area', LOCldssemi(ldsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lds)), '') )
#    writer.writerow( ('Risk Quotient for listed dicot seedlings exposed to pesticide via spray drift', ldsRQspray(spray(A,D),lds), '') )
#    writer.writerow( ('Level of concern for listed dicot seedlings exposed to pesticide via spray drift', LOCldsspray(ldsRQspray(spray(A,D),lds)), '') )
#
#finally:
#    f.close()
#
#print open(PyPestDir+'\TerrPlant\TerrPlant.output.csv', 'rt').read()

class TerrPlantBatchRunner():
    
    def runTerrPlantModel(self,config_properties,results_dict):
        results_dict = {}
        #this is where properties are searched, converted as needed, and any available methods are called
        A = None
        if 'application_lbs_rate' in config_properties:
            A = config_properties['application_lbs_rate']
        I = None
        if 'incorporation_depth' in config_properties:
            I = config_properties['incorporation_depth']
        R = None
        if 'runoff' in config_properties:
            R = config_properties['runoff']
        if A and I and R:
            results_dict['EEC-dry'] = rundry(A,I,R)
            results_dict['EEC-semi-aquatic'] = runsemi(A, I, R)
            D = None
            if 'spray_drift' in config_properties:
                D = config_properties['spray_drift']
            if D:
                results_dict['EEC-spray-drift'] = spray(A,D)
        if results_dict['EEC-dry'] and results_dict['EEC-spray-drift']:
            results_dict['EEC-total-dry'] = totaldry(results_dict['EEC-dry'],results_dict['EEC-spray-drift'])
        if results_dict['EEC-semi-aquatic'] and results_dict['EEC-spray-drift']:
            results_dict['EEC-total-semi-aquatic'] = totalsemi(results_dict['EEC-semi-aquatic'],results_dict['EEC-spray-drift'])
        nms = None
        if 'EC25_for_nonlisted_seedling_emergence_monocot' in config_properties:
            nms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        if results_dict['EEC-total-dry'] and nms:
            results_dict['nmsRQdry'] = nmsRQdry(results_dict['EEC-total-dry'],nms)
        if results_dict['EEC-total-semi-aquatic'] and nms:    
            results_dict['nmsRQsemi'] = nmsRQsemi(results_dict['EEC-total-semi-aquatic'],nms)
            results_dict['nmsRQspray'] = nmsRQspray(results_dict['EEC-spray-drift'],nms)
        lms = None
        if 'NOAEC_for_listed_seedling_emergence_monocot' in config_properties:
            lms = config_properties['NOAEC_for_listed_seedling_emergence_monocot']
        if results_dict['EEC-total-dry'] and lms:
            results_dict['lmsRQdry'] = lmsRQdry(results_dict['EEC-total-dry'],lms)
        if results_dict['EEC-total-semi-aquatic'] and lms:
            results_dict['lmsRQsemi'] = lmsRQsemi(results_dict['EEC-total-semi-aquatic'],lms)
            results_dict['lmsRQspray'] = lmsRQspray(results_dict['EEC-spray-drift'],lms)
        nds = None
        if 'EC25_for_nonlisted_seedling_emergence_dicot' in config_properties:
            nds = config_properties['EC25_for_nonlisted_seedling_emergence_dicot']
        if results_dict['EEC-total-dry'] and nds:
            results_dict['ndsRQdry'] = ndsRQdry(results_dict['EEC-total-dry'],nds)
        if results_dict['EEC-total-semi-aquatic'] and nds:    
            results_dict['ndsRQsemi'] = ndsRQsemi(results_dict['EEC-total-semi-aquatic'],nds)
            results_dict['ndsRQspray'] = ndsRQspray(results_dict['EEC-spray-drift'],nds)
        lds = None
        if 'NOAEC_for_listed_vegetative_vigor_dicot' in config_properties:
            lds = config_properties['NOAEC_for_listed_vegetative_vigor_dicot']
        if results_dict['EEC-total-dry'] and lds:
            results_dict['ldsRQdry'] = ldsRQdry(results_dict['EEC-total-dry'],lds)
        if results_dict['EEC-total-semi-aquatic'] and lds:
            results_dict['ldsRQsemi'] = ldsRQsemi(results_dict['EEC-total-semi-aquatic'],lds)
            results_dict['ldsRQspray'] = ldsRQspray(results_dict['EEC-spray-drift'],lds)            
        return results_dict


class TerrPlantExecutePage(webapp.RequestHandler):
    def post(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
        pc_code = form.getvalue('pc_code')
        use = form.getvalue('use')
        application_method = form.getvalue('application_method')
        application_form = form.getvalue('application_form')
        solubility = form.getvalue('solubility')
        I = form.getvalue('incorporation')
        A = form.getvalue('application_rate')
        D = form.getvalue('drift_fraction')
        R = form.getvalue('runoff_fraction')
        nms = form.getvalue('EC25_for_nonlisted_seedling_emergence_monocot')
        nds = form.getvalue('EC25_for_nonlisted_seedling_emergence_dicot')
        lms = form.getvalue('NOAEC_for_listed_seedling_emergence_monocot')
        lds = form.getvalue('NOAEC_for_listed_seedling_emergence_dicot')
        nmv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_monocot')
        ndv = form.getvalue('EC25_for_nonlisted_vegetative_vigor_dicot')
        lmv = form.getvalue('NOAEC_for_listed_vegetative_vigor_monocot')
        ldv = form.getvalue('NOAEC_for_listed_vegetative_vigor_dicot')
        text_file = open('terrplant/terrplant_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock_wmodellinks.html', {'model':'terrplant','page':'output'})
        html = html + template.render (templatepath + '03ubertext_links_left.html', {})                                
        html = html + template.render(templatepath + '04uberoutput_start.html',{'model':'terrplant', 'model_attributes':'TerrPlant Output'})   
        html = html + """
        <table border="1">
        <tr><H3>User Inputs: Chemical Identity</H3></tr>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>PC Code</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Use</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Method</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Form</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Solubility in Water (ppm)</td>
        <td>%s</td>
        <tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>User Inputs: Input Parameters Used to Derive EECs</H3></tr><br>
        <tr>
        <td>Incorporation</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Application Rate</td>
        <td>%s</td>
        <td>lbs ai/A</td>
        </tr>
        <tr>
        <td>Drift Fraction</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Runoff Fraction</td>
        <td>%s</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>EECs - Units in (lbs a.i./A)</H3></tr><br>
        <tr>
        <th colspan="1">Description</th>
        <th colspan="1">EEC</th>
        </tr>
        <tr>
        <td>Runoff to Dry Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Runoff to Semi-Aquatic Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Spray Drift</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Total for Dry Areas</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Total for Semi-Aquatic Areas</td>
        <td>%0.2E</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>User Inputs: Plant Survival and Growth Data Used for RQ Derivation - Units in (lbs a.i./A)</H3></tr><br>
        <tr><th> </th>
        <th colspan="2">Seedling Emergence</th>
        <th colspan="2">Vegetative Vigor</th>
        </tr>
        <tr><td>Plant Type</td>
        <td>EC<sub>25</sub></td>
        <td>NOAEC</td>
        <td>EC<sub>25</sub></td>
        <td>NOAEC</td>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        </table>
        <br></br>
        
        <table border="1">
        <tr><H3>RQ Values for Plants in Dry and Semi-aquatic Areas Exposed to Through Runoff and/or Spray Drift *</H3></tr>
        <tr>
        <th colspan="1">Plant Type</th>
        <th colspan="1">Listed Status</th>
        <th colspan="1">Dry</th>
        <th colspan="1">Semi-Aquatic</th>
        <th colspan="1">Spray Drift</th>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>non-listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Monocot</td>
        <td>listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>non-listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        <tr>
        <td>Dicot</td>
        <td>listed</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        <td>%0.2E</td>
        </tr>
        </table>
        <H4>* If RQ > 1.0, the Level of Concern is exceeded, resulting in potential risk to that plant group.</H4>
        """ % (chemical_name, pc_code, use, application_method, application_form, solubility,
               I, A, D, R, 
               rundry(A,I,R), runsemi(A,I,R), spray(A,D), totaldry(rundry(A,I,R),spray(A,D)), totalsemi(runsemi(A,I,R),spray(A,D)),
               nms, lms, nmv, lmv, nds, lds, ndv, ldv,
               nmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nms), 
nmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nms), 
nmsRQspray(spray(A,D),nms), 
lmsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lms), 
lmsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lms), 
lmsRQspray(spray(A,D),lms),
ndsRQdry(totaldry(rundry(A,I,R),spray(A,D)),nds), 
ndsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),nds), 
ndsRQspray(spray(A,D),nds), 
ldsRQdry(totaldry(rundry(A,I,R),spray(A,D)),lds), 
ldsRQsemi(totalsemi(runsemi(A,I,R),spray(A,D)),lds), 
ldsRQspray(spray(A,D),lds)
)
        html = html + template.render(templatepath + '04uberoutput_end.html', {})
        html = html + template.render(templatepath + '05ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

