# Earthworm Fugacity Modeling (earthworm)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import numpy as np
import logging
from django.utils import simplejson

logger = logging.getLogger('earthworm Model')


def toJSON(earthworm_object):
    earthworm_vars = vars(earthworm_object)
    earthworm_json = simplejson.dumps(earthworm_vars)
    return earthworm_json

def fromJSON(json_string):
    earthworm_vars = simplejson.loads(json_string)
    earthworm_object = terrplant(True,False,vars_dict=earthworm_vars)
    return earthworm_object

class earthworm(object):
    def __init__(self, set_variables=True,run_methods=True,k_ow=1,l_f_e=1,c_s=1,k_d=1,p_s=1,c_w=1,m_w=1,p_e=1,vars_dict=None):
        self.set_default_variables()
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.k_ow = k_ow
                self.l_f_e = l_f_e
                self.c_s = c_s
                self.k_d = k_d
                self.p_s = p_s
                self.c_w = c_w
                self.m_w = m_w
                self.p_e = p_e
                logger.info(vars(self))
            if run_methods:
                self.run_methods()

    def set_default_variables(self):
        self.k_ow = -1
        self.l_f_e = -1
        self.c_s = -1
        self.k_d = -1
        self.p_s = -1
        self.c_w = -1
        self.m_w = -1
        self.p_e = -1
        self.earthworm_fugacity_out = -1


    def run_methods(self):
        self.earthworm_fugacity()


    def earthworm_fugacity(self):
        if self.earthworm_fugacity_out == -1:
            try:
                self.k_ow = float(self.k_ow)
                self.l_f_e = float(self.l_f_e)
                self.c_s = float(self.c_s)
                self.k_d = float(self.k_d)
                self.p_s = float(self.p_s)
                self.c_w = float(self.c_w)
                self.m_w = float(self.m_w)
                self.p_e = float(self.p_e)
            except ValueError:
                raise ValueError\
                ('The octanol to water partition coefficient must be a real number, not "%g"' % self.k_ow)
            except ValueError:
                raise ValueError\
                ('The lipid fraction of earthworm must be a real number, not "%g"' % self.l_f_e)
            except ValueError:
                raise ValueError\
                ('The chemical concentration in soil must be a real number, not "%g"' % self.c_s)
            except ValueError:
                raise ValueError\
                ('The soil partitioning coefficient must be a real number, not "%g"' % self.k_d)
            except ValueError:
                raise ValueError\
                ('The bulk density of soil must be a real number, not "%g"' % self.p_s)
            except ValueError:
                raise ValueError\
                ('The chemical concentration in pore water of soil must be a real number, not "%g"' % self.c_w)
            except ValueError:
                raise ValueError\
                ('The molecular weight of chemical must be a real number, not "%g"' % self.m_w)
            except ValueError:
                raise ValueError\
                ('The density of earthworm must be a real number, not "%g"' % self.p_e)
            if self.k_ow < 0:
                raise ValueError\
                ('self.k_ow=%g is a non-physical value.' % self.k_ow)
            if self.l_f_e < 0:
                raise ValueError\
                ('self.l_f_e=%g is a non-physical value.' % self.l_f_e)
            if self.l_f_e > 1:
                raise ValueError\
                ('self.l_f_e=%g is a non-physical value.' % self.l_f_e)
            if self.c_s < 0:
                raise ValueError\
                ('self.c_s=%g is a non-physical value.' % self.c_s)
            if self.k_d < 0:
                raise ValueError\
                ('self.k_d=%g is a non-physical value.' % self.k_d)
            if self.p_s < 0:
                raise ValueError\
                ('self.p_s=%g is a non-physical value.' % self.p_s)
            if self.c_w < 0:
                raise ValueError\
                ('self.c_w=%g is a non-physical value.' % self.c_w)
            if self.m_w < 0:
                raise ValueError\
                ('self.m_w=%g is a non-physical value.' % self.m_w)
            if self.p_e < 0:
                raise ValueError\
                ('self.p_e=%g is a non-physical value.' % self.p_e)

            self.earthworm_fugacity_out = self.k_ow*self.l_f_e*(self.c_s/(self.k_d*self.p_s)+self.c_w)*self.m_w/self.p_e
        return self.earthworm_fugacity_out