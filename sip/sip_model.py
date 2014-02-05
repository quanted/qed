# Screening Imbibiton Program v1.0 (SIP)
import logging
from django.utils import simplejson
import time, datetime
logger = logging.getLogger('SIP Model')
# Daily water intake rate for birds

def toJSON(sip_object):
    sip_vars = vars(sip_object)
    sip_json = simplejson.dumps(sip_vars)
    return sip_json

def fromJSON(json_string):
    sip_vars = simplejson.loads(json_string)
    sip_object = terrplant(True,False,vars_dict=sip_vars)
    return sip_object

class sip(object):
    def __init__(self, set_variables=True,run_methods=True,run_type = "single",chemical_name='', b_species='', m_species='', bw_quail=1, bw_duck=1, bwb_other=1, bw_rat=1, bwm_other=1, sol=1, ld50_a=1, ld50_m=1, aw_bird=1, mineau=1, aw_mamm=1, noaec_d=1, noaec_q=1, noaec_o=1, Species_of_the_bird_NOAEC_CHOICES=1, noael=1,vars_dict=None):
        self.set_default_variables()
        ts = datetime.datetime.now()
        if(time.daylight):
            ts1 = datetime.timedelta(hours=-4)+ts
        else:
            ts1 = datetime.timedelta(hours=-5)+ts
        self.jid = ts1.strftime('%Y%m%d%H%M%S%f')
        if set_variables:
            if vars_dict != None:
                self.__dict__.update(vars_dict)
            else:
                self.run_type = run_type
                self.chemical_name = chemical_name
                self.bw_quail = bw_quail
                self.bw_duck = bw_duck
                self.bwb_other = bwb_other
                self.bw_rat = bw_rat
                self.bwm_other = bwm_other
                self.b_species = b_species
                self.m_species = m_species
                if b_species =='178':
                    self.bw_bird = self.bw_quail
                elif b_species =='1580':
                    self.bw_bird = self.bw_duck
                else:
                    self.bw_bird = self.bwb_other
                if m_species =='350':
                    self.bw_mamm = self.bw_rat
                else:
                    self.bw_mamm = self.bwm_other
                self.sol = sol
                self.ld50_a = ld50_a
                self.ld50_m = ld50_m
                self.aw_bird = aw_bird
                self.mineau = mineau
                self.aw_mamm = aw_mamm
                self.noaec_d = noaec_d
                self.noaec_q = noaec_q
                self.noaec_o = noaec_o
                if Species_of_the_bird_NOAEC_CHOICES == '1':
                    self.noaec = self.noaec_q
                elif Species_of_the_bird_NOAEC_CHOICES == '2':
                    self.noaec = self.noaec_d
                elif Species_of_the_bird_NOAEC_CHOICES == '3':
                    self.noaec = self.noaec_o
                # else:
                #     try:
                #         self.noaec = noaec
                #     except ValueError:
                #         raise ValueError\
                #         ('self.noaec=%g is a non-physical value.' % self.aw_bird)
                self.noael = noael
                # logger.info(vars(self))
            if run_methods:
                self.run_methods()

    def set_default_variables(self):
        self.run_type = "single"
        self.chemical_name = ''
       # self.select_receptor()
        self.bw_bird = -1
        self.bw_mamm = -1
        self.sol = -1
        self.ld50_a = -1
        self.ld50_m = -1
        self.aw_bird = -1
        self.mineau = -1
        self.aw_mamm = -1
        self.noaec = -1
        self.noael = -1
        self.fw_bird_out = -1
        self.fw_mamm_out = -1
        self.dose_bird_out = -1
        self.dose_mamm_out = -1
        self.at_bird_out = -1
        self.at_mamm_out = -1
        self.fi_bird_out = -1
        self.det_out = -1
        self.act_out = -1
        self.acute_bird_out = -1
        self.acuconb_out = -1
        self.acute_mamm_out = -1
        self.acuconm_out = -1
        self.chron_bird_out = -1
        self.chronconb_out = -1
        self.chron_mamm_out = -1
        self.chronconm_out = -1
        self.bw_quail = -1
        self.bw_duck = -1
        self.bwb_other = -1
        self.bw_rat = -1
        self.bwm_other = -1
        self.b_species = None
        self.m_species = None

    def set_unit_testing_variables(self):
        self.fw_bird_out_expected = None
        self.fw_mamm_out_expected = None
        self.dose_bird_out_expected = None
        self.dose_mamm_out_expected = None
        self.at_bird_out_expected = None
        self.at_mamm_out_expected = None
        self.fi_bird_out_expected = None
        self.det_out_expected = None
        self.act_out_expected = None
        self.acute_bird_out_expected = None
        self.acuconb_out_expected = None
        self.acute_mamm_out_expected = None
        self.acuconm_out_expected = None
        self.chron_bird_out_expected = None
        self.chronconb_out_expected = None
        self.chron_mamm_out_expected = None
        self.chronconm_out_expected = None

    def run_methods(self):
        self.fw_bird()
        self.fw_mamm()
        self.dose_bird()
        self.dose_mamm()
        self.at_bird()
        self.at_mamm()
        self.fi_bird()
        self.det()
        self.act()
        self.acute_bird()
        self.acuconb()
        self.acute_mamm()
        self.acuconm()
        self.chron_bird()
        self.chronconb()
        self.chron_mamm()
        self.chronconm()

    def fw_bird(self):
        if self.fw_bird_out == -1:
            try:
                self.aw_bird = float(self.aw_bird)
            except IndexError:
                raise IndexError\
                ('The body weight of the bird must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%g"' % self.aw_bird)
            if self.aw_bird < 0:
                raise ValueError\
                ('self.aw_bird=%g is a non-physical value.' % self.aw_bird)
            self.fw_bird_out = (1.180 * (self.aw_bird**0.874))/1000.0
        return self.fw_bird_out

    # Daily water intake rate for mammals

    def fw_mamm(self):
        if self.fw_mamm_out == -1:
            try:
                self.aw_mamm = float(self.aw_mamm)
            except IndexError:
                raise IndexError\
                ('The body weight of the mammal must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight of the mammal must be a real number, not "%g"' % self.aw_mamm)
            if self.aw_mamm < 0:
                raise ValueError\
                ('self.aw_mamm=%g is a non-physical value.' % self.aw_mamm)
            self.fw_mamm_out = (0.708 * (self.aw_mamm**0.795))/1000.0
        return self.fw_mamm_out

    # Upper bound estimate of exposure for birds

    def dose_bird(self):
        if self.dose_bird_out == -1:
            try:
                self.fw_bird_out = float(self.fw_bird_out)
                self.sol = float(self.sol)
                self.aw_bird = float(self.aw_bird)
            except IndexError:
                raise IndexError\
                ('The daily water intake for birds, chemical solubility, and/or'\
                ' the body weight of the bird must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The daily water intake for birds must be a real number, '\
                'not "%L"' %self.fw_bird)
            except ValueError:
                raise ValueError\
                ('The chemical solubility must be a real number, not "%mg/L"' %self.sol)
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%g"' %self.aw_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the bird must non-zero.')
            if self.fw_bird_out < 0:
                raise ValueError\
                ('fw_bird=%g is a non-physical value.' % self.fw_bird_out)
            if self.sol < 0:
                raise ValueError\
                ('sol=%g is a non-physical value.' % self.sol)
            if self.aw_bird < 0:
                raise ValueError\
                ('self.aw_bird=%g is a non-physical value.' % self.aw_bird)
            self.dose_bird_out = (self.fw_bird_out * self.sol)/(self.aw_bird / 1000)
        return self.dose_bird_out


    # Upper bound estimate of exposure for mammals

    def dose_mamm(self):
        if self.dose_mamm_out == -1:
            try:
                self.fw_mamm_out = float(self.fw_mamm_out)
                self.sol = float(self.sol)
                self.aw_mamm = float(self.aw_mamm)
            except IndexError:
                raise IndexError\
                ('The daily water intake for mammals, chemical solubility, and/or'\
                ' the body weight of the mammal must be supplied on the command line.')
            except ValueError:
                raise ValueError\
                ('The daily water intake for mammals must be a real number, '\
                'not "%L"' %self.fw_mamm)
            except ValueError:
                raise ValueError\
                ('The chemical solubility must be a real number, not "%mg/L"' %self.sol)
            except ValueError:
                raise ValueError\
                ('The body weight of the mammal must be a real number, not "%g"' %self.aw_mamm)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the mammal must non-zero.')
            if self.fw_bird_out < 0:
                raise ValueError\
                ('fw_mamm=%g is a non-physical value.' % self.fw_mamm_out)
            if self.sol < 0:
                raise ValueError\
                ('sol=%g is a non-physical value.' % self.sol)
            if self.aw_mamm < 0:
                raise ValueError\
                ('self.aw_mamm=%g is a non-physical value.' % self.aw_mamm)
            self.dose_mamm_out = (self.fw_mamm_out * self.sol)/(self.aw_mamm / 1000)
        return self.dose_mamm_out

    # Acute adjusted toxicity value for birds

    def at_bird(self):
        if self.at_bird_out == -1:
            try:
                self.ld50_a = float(self.ld50_a)
                self.aw_bird = float(self.aw_bird)
                self.bw_bird = float(self.bw_bird)
                self.mineau = float(self.mineau)
            except IndexError:
                raise IndexError\
                ('The lethal dose, body weight of assessed bird, body weight'\
                ' of tested bird, and/or the mineau scaling factor must be'\
                'supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The mineau scaling factor must be a real number' %self.mineau)
            except ValueError:
                raise ValueError\
                ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_a)
            except ValueError:
                raise ValueError\
                ('The body weight of assessed bird must be a real number, not "%g"' %self.aw_bird)
            except ValueError:
                raise ValueError\
                ('The body weight of tested bird must be a real number, not "%g"' %self.bw_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of tested bird must be non-zero.')
            if self.ld50_a < 0:
                raise ValueError\
                ('ld50_a=%g is a non-physical value.' % self.ld50_a)
            if self.aw_bird < 0:
                raise ValueError\
                ('aw_bird=%g is a non-physical value.' % self.aw_bird)
            if self.bw_bird < 0:
                raise ValueError\
                ('bw_bird=%g is a non-physical value.' % self.bw_bird)
            self.at_bird_out = (self.ld50_a) * ((self.aw_bird/self.bw_bird)**(self.mineau-1))
        return self.at_bird_out

    # Acute adjusted toxicity value for mammals

    def at_mamm(self):
        if self.at_mamm_out == -1:
            try:
                self.ld50_m = float(self.ld50_m)
                self.aw_mamm = float(self.aw_mamm)
                self.bw_mamm = float(self.bw_mamm)
            except TypeError:
                raise TypeError\
                ('Either ld50_m, aw_mamm or bw_mamm equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The lethal dose, body weight of assessed mammal, and/or body weight'\
                ' of tested mammal, must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The lethal dose must be a real number, not "%mg/kg"' %self.ld50_m)
            except ValueError:
                raise ValueError\
                ('The body weight of assessed mammal must be a real number, not "%g"' %self.aw_mamm)
            except ValueError:
                raise ValueError\
                ('The body weight of tested mammal must be a real number, not "%g"' %self.bw_mamm)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of tested mammal must be non-zero.')
            if self.ld50_m < 0:
                raise ValueError\
                ('ld50_m=%g is a non-physical value.' % self.ld50_m)
            if self.aw_mamm < 0:
                raise ValueError\
                ('aw_mamm=%g is a non-physical value.' % self.aw_mamm)
            if self.bw_mamm < 0:
                raise ValueError\
                ('bw_mamm=%g is a non-physical value.' % self.bw_mamm)
            self.at_mamm_out = (self.ld50_m) * ((self.bw_mamm/self.aw_mamm)**0.25)
        return self.at_mamm_out


    # Adjusted chronic toxicity values for birds

    # FI = Food Intake Rate

    def fi_bird(self):
        if self.fi_bird_out == -1:
            try:
                self.bw_bird = float(self.bw_bird)
            except IndexError:
                raise IndexError\
                ('The body weight of the bird must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The body weight must be a real number, not "%kg"' %self.bw_bird)
            if self.bw_bird < 0:
                raise ValueError\
                ('self.bw_bird=%g is a non-physical value.' % self.bw_bird)
            self.fi_bird_out = 0.0582 * ((self.bw_bird / 1000)**0.651)
        return self.fi_bird_out

    # Dose-equivalent chronic toxicity value for birds

    def det(self):
        if self.det_out == -1:
            try:
                self.noaec = float(self.noaec)
                self.fi_bird_out = float(self.fi_bird_out)
                self.bw_bird = float(self.bw_bird)
            except IndexError:
                raise IndexError\
                ('The no observed adverse effects concentration, daily food intake'\
                ' rate for birds, and/or body weight of the bird must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The NOAEC must be a real number, not "%mg/kg"' % self.noaec)
            except ValueError:
                raise ValueError\
                ('The dialy food intake rate for birds must be a real number,'\
                ' not "%kg"' % self.fi_bird_out)
            except ValueError:
                raise ValueError\
                ('The body weight of the bird must be a real number, not "%kg"' % self.bw_bird)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the bird must be non-zero.')
            if self.noaec < 0:
                raise ValueError\
                ('noaec=%g is a non-physical value.' % self.noaec)
            if self.fi_bird_out < 0:
                raise ValueError\
                ('fi_bird=%g is a non-physical value.' % self.fi_bird_out)
            if self.bw_bird < 0:
                raise ValueError\
                ('self.bw_bird=%g is a non-physical value.' % self.bw_bird)
            self.det_out = (self.noaec * self.fi_bird_out) / (self.bw_bird / 1000)
        return self.det_out

    # Adjusted chronic toxicty value for mammals

    def act(self):
        if self.act_out == -1:
            try:
                self.noael = float(self.noael)
                self.bw_mamm = float(self.bw_mamm)
                self.aw_mamm = float(self.aw_mamm)
            except IndexError:
                raise IndexError\
                ('The no observed adverse effects level, body weight of the tested'\
                ' mammal, and/or body weight of assessed mammal must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The NOAEL must be a real number, not "%mg/kg"' % self.noael)
            except ValueError:
                raise ValueError\
                ('The body weight of the tested mammal must be a real number,'\
                ' not "%kg"' % self.bw_mamm)
            except ValueError:
                raise ValueError\
                ('The body weight of the assessed mammal must be a real number,'\
                ' not "%kg"' % self.aw_mamm)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The body weight of the assessed mammal must be non-zero.')
            if self.noael < 0:
                raise ValueError\
                ('noael=%g is a non-physical value.' % self.noael)
            if self.bw_mamm < 0:
                raise ValueError\
                ('bw_mamm=%g is a non-physical value.' % self.bw_mamm)
            if self.aw_mamm < 0:
                raise ValueError\
                ('aw_mamm=%g is a non-physical value.' % self.aw_mamm)
            self.act_out = (self.noael) * ((self.bw_mamm/self.aw_mamm)**0.25)
        return self.act_out
        #   MAMMILIAN:  If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC by 20 to determine the equivalent chronic daily dose (NOAEL)
    # ---- Is drinking water a concern?

    # Acute exposures for birds


    def acute_bird(self):
        if self.acute_bird_out == -1:
            try:
                self.dose_bird_out = float(self.dose_bird_out)
                self.at_bird_out = float(self.at_bird_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for birds, and/or the adjusted'\
                ' toxicity value for birds must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for birds must be a real'\
                ' number, not "%mg/kg"' % self.dose_bird_out)
            except ValueError:
                raise ValueError\
                ('The adjusted toxicity value for birds must be a real number,'\
                ' not "%mg/kg"' % self.at_bird_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted toxicity value for birds must be non-zero.')
            if self.dose_bird_out < 0:
                raise ValueError\
                ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
            if self.at_bird_out < 0:
                raise ValueError\
                ('at_bird=%g is a non-physical value.' % self.at_bird_out)
            self.acute_bird_out = self.dose_bird_out/self.at_bird_out
        return self.acute_bird_out


    def acuconb(self):
        if self.acuconb_out == -1:
            if self.acute_bird_out == None:
                raise ValueError\
                ('acute_bird variable equals None and therefor this function cannot be run.')
            if self.acute_bird_out < 0.1:
                self.acuconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
            else:
                self.acuconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        return self.acuconb_out

    # Acute exposures for mammals

    def acute_mamm(self):
        if self.acute_mamm_out == -1:
            try:
                self.dose_mamm_out = float(self.dose_mamm_out)
                self.at_mamm_out = float(self.at_mamm_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for mammals, and/or the adjusted'\
                ' toxicity value for mammals must be supplied the command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for mammals must be a real'\
                ' number, not "%mg/kg"' % self.dose_mamm_out)
            except ValueError:
                raise ValueError\
                ('The adjusted toxicity value for mammals must be a real number,'\
                ' not "%mg/kg"' % self.at_mamm_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted toxicity value for mammals must be non-zero.')
            if self.dose_mamm_out < 0:
                raise ValueError\
                ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
            if self.at_mamm_out < 0:
                raise ValueError\
                ('at_mamm=%g is a non-physical value.' % self.at_mamm_out)
            self.acute_mamm_out = self.dose_mamm_out/self.at_mamm_out
        return self.acute_mamm_out

    def acuconm(self):
        if self.acuconm_out == -1:
            if self.acute_mamm_out == None:
                raise ValueError\
                ('acute_mamm variable equals None and therefor this function cannot be run.')
            if self.acute_mamm_out < 0.1:
                self.acuconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
            else:
                self.acuconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
            return self.acuconm_out
        return self.acuconm_out

    # Chronic Exposures for birds

    def chron_bird(self):
        if self.chron_bird_out == -1:
            try:
                self.dose_bird_out = float(self.dose_bird_out)
                self.det_out = float(self.det_out)
            except TypeError:
                raise TypeError\
                ('Either dose_bird or det equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for birds, and/or the dose-'\
                'equivalent chronic toxicity value for birds must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for birds must be a real'\
                ' number, not "%mg/kg"' % self.dose_bird_out)
            except ValueError:
                raise ValueError\
                ('The dose-equivalent chronic toxicity value for birds must be a real'\
                ' number, not "%mg/kg"' % self.det_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The dose-equivalent chronic toxicity value for birds must be non-zero.')
            if self.dose_bird_out < 0:
                raise ValueError\
                ('dose_bird=%g is a non-physical value.' % self.dose_bird_out)
            if self.det_out < 0:
                raise ValueError\
                ('det=%g is a non-physical value.' % self.det_out)
            self.chron_bird_out = self.dose_bird_out/self.det_out
        return self.chron_bird_out


    def chronconb(self):
        if self.chronconb_out == -1:
            if self.chron_bird_out == None:
                raise ValueError\
                ('chron_bird variable equals None and therefor this function cannot be run.')
            if self.chron_bird_out < 1:
                self.chronconb_out = ('Drinking water exposure alone is NOT a potential concern for birds')
            else:
                self.chronconb_out = ('Exposure through drinking water alone is a potential concern for birds')
        return self.chronconb_out

    # Chronic exposures for mammals

    def chron_mamm(self):
        if self.chron_mamm_out == -1:
            try:
                self.dose_mamm_out = float(self.dose_mamm_out)
                self.act_out = float(self.act_out)
            except IndexError:
                raise IndexError\
                ('The upper bound estimate of exposure for mammals, and/or the'\
                ' adjusted chronic toxicity value for mammals must be supplied the'\
                ' command line.')
            except ValueError:
                raise ValueError\
                ('The upper bound estimate of exposure for mammals must be a real'\
                ' number, not "%mg/kg"' % self.dose_mamm_out)
            except ValueError:
                raise ValueError\
                ('The adjusted chronic toxicity value for mammals must be a real'\
                ' number, not "%mg/kg"' % self.act_out)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The adjusted chronic toxicity value for mammals must be non-zero.')
            if self.dose_mamm_out < 0:
                raise ValueError\
                ('dose_mamm=%g is a non-physical value.' % self.dose_mamm_out)
            if self.act_out < 0:
                raise ValueError\
                ('act=%g is a non-physical value.' % self.act_out)
            self.chron_mamm_out = self.dose_mamm_out/self.act_out
        return self.chron_mamm_out

    def chronconm(self):
        if self.chronconm_out == -1:
            if self.chron_mamm_out == None:
                raise ValueError\
                ('chron_mamm variable equals None and therefor this function cannot be run.')
            if self.chron_mamm_out < 1:
                self.chronconm_out = ('Drinking water exposure alone is NOT a potential concern for mammals')
            else:
                self.chronconm_out = ('Exposure through drinking water alone is a potential concern for mammals')
        return self.chronconm_out

