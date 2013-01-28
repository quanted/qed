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



class TerrPlantExecutePage(webapp.RequestHandler):
    def get(self):
        form = cgi.FieldStorage() 
        chemical_name = form.getvalue('chemical_name')
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
        text_file = open('stir/stir_description.txt','r')
        x = text_file.read()
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02uberintroblock.html', {'title2':'STIR Output', 'title3':x})
        html = html + template.render(templatepath + '02modellinkblock.html', {'model':'stir'})
        html = html + template.render(templatepath + '03euberinput_start.html', {})
        html = html + template.render(templatepath + '06uber_break.html', {})     
        html = html + """
        <table border="1">
        <tr><H3>User Inputs</H3></tr><br>
        <tr>
        <td>Chemical Name</td>
        <td>%s</td>
        </tr>
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
        
        <table border="1">
        <caption><b>User Inputs: Plant Survival and Growth Data Used for RQ Derivation</b></caption><br>
        <tr>Units in (lbs a.i./A)</tr>
        <tr><th> </th>
        <th colspan="2">Seedling Emergence</th>
        <th colspan="2">Vegetative Vigor</th>
        </tr>
        
        
        <tr>
        <td>EC25 for Non-listed Seedling Emergence Monocot</td>
        <td>%s</td>
        <td>lbs a.i./A</td>
        </tr>
        <tr>
        <td>EC25 for Non-listed Seedling Emergence Dicot</td>
        <td>%s</td>
        <td>lbs a.i./A</td>
        </tr>
        <tr>
        <td>NOAEC for Listed Seedling Emergence Monocot</td>
        <td>%s</td>
        <td>lbs a.i./A</td>
        </tr>
        <tr>
        <td>NOAEC for Listed Seedling Emergence Dicot</td>
        <td>%s</td>
        <td>lbs a.i./A</td>
        </tr>
        <tr>
        <td>EC25 for Non-listed Vegetative Vigor Monocot</td>
        <td>%s</td>
        <td>kg</td>
        </tr>
        <tr>
        <td>Chemical Specific Mineau Scaling Factor</td>
        <td>%s</td>
        </tr>
        <tr>
        <td>Mammalian LC<sub>50</sub></td>
        <td>%s</td>
        <td>mg/kg-bw</td>
        </tr>
        <tr>
        <td>Duration of Rat Inhalation Study</td>
        <td>%s</td>
        <td>hrs</td>
        </tr>
        <tr>
        <td>Body Weight of Assessed Mammal</td>
        <td>%s</td>
        <td>kg</td>
        </tr>
        <tr>
        <td>Rat Inhalation LD<sub>50</sub></td>
        <td>%s</td>
        <td>mg/kg-bw</td>
        </tr>
        <tr>
        <td>Rat Oral LD<sub>50</sub></td>
        <td>%s</td>
        <td>mg/kg-bw</td>
        </tr>
        </table>
        """ % (chemical_name, I, A, D, R, nms, nds, lms, lds, nmv, ndv, lmv, ldv)
#        html = html + template.render(templatepath + '06uber_break.html', {})
#        html = html + """
#       <table border="1">
#        <tr><H3>STIR Outputs</H3></tr><br>
#        <tr>
#        <H4>Results Avian (%s kg)</H4>
#        </tr>
#        <tr>
#        <td>Saturated Air Concentration of Pesticide</td>
#        <td>%0.2E</td>
#        <td>mg/m<sup>3</sup></td>
#        </tr>
#        <tr>
#        <td>Avian Inhalation Rate</td>
#        <td>%0.2E</td>
#        <td>cm<sup>3</sup>/hr</td>
#        </tr>
#        <tr>
#        <td>Maximum 1-hour Avian Vapor Inhalation Dose</td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <td>Estimated Avian Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Adjusted Avian Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td><H5><font color="red">%s</font></H5></td>
#        </tr>
#        <tr>
#        <td>Spray Droplet Inhalation Dose of Assessed Bird</td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td><H5><font color="red">%s</font></H5></td>
#        </tr>
#        </table>
#        <br></br>
#        <table border="1">
#        <tr>
#        <H4>Results Mammalian (%s kg)</H4>
#        </tr>
#        <tr>
#        <td>Saturated Air Concentration of Pesticide</td>
#        <td>%0.2E</td>
#        <td>mg/m<sup>3</sup></td>
#        </tr>
#        <tr>
#        <td>Mammalian Inhalation Rate</td>
#        <td>%0.2E</td>
#        <td>cm<sup>3</sup>/hr</td>
#        </tr>
#        <tr>
#        <td>Maximum 1-hour Mammalian Vapor Inhalation Dose</td> 
#        <td>%0.2E</td>
#        <td>mg/kg</td>
#        </tr>
#        <tr>
#        <td>Conversion of Mammalian Inhalation LC<sub>50</sub> to LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Adjusted Mammalian Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Ratio of Vapor Dose to Adjusted Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td><H5><font color="red">%s</font></H5></td>
#        </tr>
#        <tr>
#        <td>Spray Droplet Inhalation Dose of Assessed Mammal</td>
#        <td>%0.2E</td>
#        <td>mg/kg-bw</td>
#        </tr>
#        <tr>
#        <td>Ratio of Droplet Inhalation Dose to Adjusted Inhalation LD<sub>50</sub></td>
#        <td>%0.2E</td>
#        <td><H5><font color="red">%s</font></H5></td>
#        </tr>
#        </table>
#        """ % (aw_avian, 
#               cs(vp,mw), 
#ir_avian(aw_avian), 
#vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian), 
#ld50est(ld50ao,ld50ri,ld50ro), 
#ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau), 
#ratio_vd_avian(vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau)), 
#LOC_vd_avian(ratio_vd_avian(vid_avian(cs(vp,mw),ir_avian(aw_avian),aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau))), 
#sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian), 
#ratio_sid_avian(sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau)), 
#LOC_sid_avian(ratio_sid_avian(sid_avian(c_air(ar2,h),ir_avian(aw_avian),ddsi,f_inhaled,aw_avian),ld50adj_avian(ld50est(ld50ao,ld50ri,ld50ro),aw_avian,tw_avian,mineau))), 
#               aw_mammal, 
#               cs(vp,mw), 
#ir_mammal(aw_mammal), 
#vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal), 
#ld50(lc50,cf(ir_mammal, aw_mammal),dur), 
#ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal), 
#ratio_vd_mammal(vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal)), 
#LOC_vd_mammal(ratio_vd_mammal(vid_mammal(cs(vp,mw),ir_mammal(aw_mammal),aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal))), 
#sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),
#ratio_sid_mammal(sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal)),
#LOC_sid_mammal(ratio_sid_mammal(sid_mammal(c_air(ar2,h),ir_mammal(aw_mammal),ddsi,f_inhaled,aw_mammal),ld50adj_mammal(ld50(lc50,cf(ir_mammal, aw_mammal),dur),tw_mammal,aw_mammal))))              
        html = html + template.render(templatepath + '03dubertext_end.html', {})
        html = html + template.render(templatepath + '03cubertext_links.html', {})
        html = html + template.render(templatepath + '04uberform_end.html', {})
        html = html + template.render(templatepath + '05uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', TerrPlantExecutePage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

