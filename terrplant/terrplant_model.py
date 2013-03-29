import numpy as np
import logging
import sys
sys.path.append("../utils")
import utils.json_utils

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
