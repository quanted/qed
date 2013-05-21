# Screening Imbibiton Program v1.0 (SIP)

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import numpy as np

# Daily water intake rate for birds

class sip(object):
    def __init__(self, chemical_name, bw_bird, bw_mamm, sol, ld50_a, ld50_m, aw_bird, tw_bird, mineau, aw_mamm, tw_mamm, noaec, noael):
        self.chemical_name = chemical_name
       # self.select_receptor = select_receptor
        self.bw_bird = bw_bird
        self.bw_mamm = bw_mamm
        self.sol = sol
        self.ld50_a = ld50_a
        self.ld50_m = ld50_m
        self.aw_bird = aw_bird
        self.tw_bird = tw_bird
        self.mineau = mineau
        self.aw_mamm = aw_mamm
        self.tw_mamm = tw_mamm
        self.noaec = noaec
        self.noael = noael
        self.run_methods()

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
        try:
            self.bw_bird = float(self.bw_bird)
        except IndexError:
            raise IndexError\
            ('The body weight of the bird must be supplied on the command line.')
        except ValueError:
            raise ValueError\
            ('The body weight of the bird must be a real number, not "%g"' % self.bw_bird)
        if self.bw_bird < 0:
            raise ValueError\
            ('self.bw_bird=%g is a non-physical value.' % self.bw_bird)
        self.fw_bird = (1.180 * (self.bw_bird**0.874))/1000.0
        # return 


    # Daily water intake rate for mammals

    def fw_mamm(self):
       try:
            self.bw_mamm = float(self.bw_mamm)
       except IndexError:
            raise IndexError\
            ('The body weight of the mammal must be supplied on the command line.')
       except ValueError:
            raise ValueError\
            ('The body weight of the mammal must be a real number, not "%g"' % self.bw_mamm)
       if self.bw_mamm < 0:
            raise ValueError\
            ('self.bw_mamm=%g is a non-physical value.' % self.bw_mamm)
       self.fw_mamm = (0.708 * (self.bw_mamm**0.795))/1000.0


    # Upper bound estimate of exposure for birds

    def dose_bird(self):
        try:
            self.fw_bird = float(self.fw_bird)
            self.sol = float(self.sol)
            self.bw_bird = float(self.bw_bird)
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
            ('The body weight of the bird must be a real number, not "%g"' %self.bw_bird)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of the bird must non-zero.')
        if self.fw_bird < 0:
            raise ValueError\
            ('fw_bird=%g is a non-physical value.' % self.fw_bird)
        if self.sol < 0:
            raise ValueError\
            ('sol=%g is a non-physical value.' % self.sol)
        if self.bw_bird < 0:
            raise ValueError\
            ('self.bw_bird=%g is a non-physical value.' % self.bw_bird)
        self.dose_bird = (self.fw_bird * self.sol)/self.bw_bird


    # Upper bound estimate of exposure for mammals

    def dose_mamm(self):
        try:
            self.fw_mamm = float(self.fw_mamm)
            self.sol = float(self.sol)
            self.bw_mamm = float(self.bw_mamm)
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
            ('The body weight of the mammal must be a real number, not "%g"' %self.bw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of the mammal must non-zero.')
        if self.fw_bird < 0:
            raise ValueError\
            ('fw_mamm=%g is a non-physical value.' % self.fw_mamm)
        if self.sol < 0:
            raise ValueError\
            ('sol=%g is a non-physical value.' % self.sol)
        if self.bw_mamm < 0:
            raise ValueError\
            ('self.bw_mamm=%g is a non-physical value.' % self.bw_mamm)
        self.dose_mamm = (self.fw_mamm * self.sol)/self.bw_mamm


    # Acute adjusted toxicity value for birds

    def at_bird(self):
        try:
            self.ld50_a = float(self.ld50_a)
            self.aw_bird = float(self.aw_bird)
            self.tw_bird = float(self.tw_bird)
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
            ('The body weight of tested bird must be a real number, not "%g"' %self.tw_bird)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested bird must be non-zero.')
        if self.ld50_a < 0:
            raise ValueError\
            ('ld50_a=%g is a non-physical value.' % self.ld50_a)
        if self.aw_bird < 0:
            raise ValueError\
            ('aw_bird=%g is a non-physical value.' % self.aw_bird)
        if self.tw_bird < 0:
            raise ValueError\
            ('tw_bird=%g is a non-physical value.' % self.tw_bird)
        self.at_bird = (self.ld50_a) * ((self.aw_bird/self.tw_bird)**(self.mineau-1))




    # Acute adjusted toxicity value for mammals

    def at_mamm(self):
        try:
            self.ld50_m = float(self.ld50_m)
            self.aw_mamm = float(self.aw_mamm)
            self.tw_mamm = float(self.tw_mamm)
        except TypeError:
            raise TypeError\
            ('Either ld50_m, aw_mamm or tw_mamm equals None and therefor this function cannot be run.')
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
            ('The body weight of tested mammal must be a real number, not "%g"' %self.tw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of tested mammal must be non-zero.')
        if self.ld50_m < 0:
            raise ValueError\
            ('ld50_m=%g is a non-physical value.' % self.ld50_m)
        if self.aw_mamm < 0:
            raise ValueError\
            ('aw_mamm=%g is a non-physical value.' % self.aw_mamm)
        if self.tw_mamm < 0:
            raise ValueError\
            ('tw_mamm=%g is a non-physical value.' % self.tw_mamm)
        self.at_mamm = (self.ld50_m) * ((self.aw_mamm/self.tw_mamm)**0.25)


    # Adjusted chronic toxicity values for birds

    # FI = Food Intake Rate

    def fi_bird(self):
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
        self.fi_bird = 0.0582 * (self.bw_bird**0.651)


    # Dose-equivalent chronic toxicity value for birds

    def det(self):
        try:
            self.noaec = float(self.noaec)
            self.fi_bird = float(self.fi_bird)
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
            ' not "%kg"' % self.fi_bird)
        except ValueError:
            raise ValueError\
            ('The body weight of the bird must be a real number, not "%kg"' % self.bw_bird)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The body weight of the bird must be non-zero.')
        if self.noaec < 0:
            raise ValueError\
            ('noaec=%g is a non-physical value.' % self.noaec)
        if self.fi_bird < 0:
            raise ValueError\
            ('fi_bird=%g is a non-physical value.' % self.fi_bird)
        if self.bw_bird < 0:
            raise ValueError\
            ('self.bw_bird=%g is a non-physical value.' % self.bw_bird)
        self.det = (self.noaec * self.fi_bird)/self.bw_bird

    # Adjusted chronic toxicty value for mammals

    def act(self):
        try:
            self.noael = float(self.noael)
            self.tw_mamm = float(self.tw_mamm)
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
            ' not "%kg"' % self.tw_mamm)
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
        if self.tw_mamm < 0:
            raise ValueError\
            ('tw_mamm=%g is a non-physical value.' % self.tw_mamm)
        if self.aw_mamm < 0:
            raise ValueError\
            ('aw_mamm=%g is a non-physical value.' % self.aw_mamm)
        self.act = (self.noael) * ((self.tw_mamm/self.aw_mamm)**0.25)

    # ---- Is drinking water a concern?

    # Acute exposures for birds


    def acute_bird(self):
        try:
            self.dose_bird = float(self.dose_bird)
            self.at_bird = float(self.at_bird)
        except IndexError:
            raise IndexError\
            ('The upper bound estimate of exposure for birds, and/or the adjusted'\
            ' toxicity value for birds must be supplied the command line.')
        except ValueError:
            raise ValueError\
            ('The upper bound estimate of exposure for birds must be a real'\
            ' number, not "%mg/kg"' % self.dose_bird)
        except ValueError:
            raise ValueError\
            ('The adjusted toxicity value for birds must be a real number,'\
            ' not "%mg/kg"' % self.at_bird)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The adjusted toxicity value for birds must be non-zero.')
        if self.dose_bird < 0:
            raise ValueError\
            ('dose_bird=%g is a non-physical value.' % self.dose_bird)
        if self.at_bird < 0:
            raise ValueError\
            ('at_bird=%g is a non-physical value.' % self.at_bird)
        self.acute_bird = self.dose_bird/self.at_bird


    def acuconb(self):
        if self.acute_bird == None:
            raise ValueError\
            ('acute_bird variable equals None and therefor this function cannot be run.')
        if self.acute_bird < 0.1:
            return ('Drinking water exposure alone is NOT a potential concern for birds')
        else:
            return ('Exposure through drinking water alone is a potential concern for birds')

    # Acute exposures for mammals

    def acute_mamm(self):
        try:
            self.dose_mamm = float(self.dose_mamm)
            self.at_mamm = float(self.at_mamm)
        except IndexError:
            raise IndexError\
            ('The upper bound estimate of exposure for mammals, and/or the adjusted'\
            ' toxicity value for mammals must be supplied the command line.')
        except ValueError:
            raise ValueError\
            ('The upper bound estimate of exposure for mammals must be a real'\
            ' number, not "%mg/kg"' % self.dose_mamm)
        except ValueError:
            raise ValueError\
            ('The adjusted toxicity value for mammals must be a real number,'\
            ' not "%mg/kg"' % self.at_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The adjusted toxicity value for mammals must be non-zero.')
        if self.dose_mamm < 0:
            raise ValueError\
            ('dose_mamm=%g is a non-physical value.' % self.dose_mamm)
        if self.at_mamm < 0:
            raise ValueError\
            ('at_mamm=%g is a non-physical value.' % self.at_mamm)
        self.acute_mamm = self.dose_mamm/self.at_mamm


    def acuconm(self):
        if self.acute_mamm == None:
            raise ValueError\
            ('acute_mamm variable equals None and therefor this function cannot be run.')
        if self.acute_mamm < 0.1:
            return ('Drinking water exposure alone is NOT a potential concern for mammals')
        else:
            return ('Exposure through drinking water alone is a potential concern for mammals')


    # Chronic Exposures for birds

    def chron_bird(self):
        try:
            self.dose_bird = float(self.dose_bird)
            self.det = float(self.det)
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
            ' number, not "%mg/kg"' % self.dose_bird)
        except ValueError:
            raise ValueError\
            ('The dose-equivalent chronic toxicity value for birds must be a real'\
            ' number, not "%mg/kg"' % self.det)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The dose-equivalent chronic toxicity value for birds must be non-zero.')
        if self.dose_bird < 0:
            raise ValueError\
            ('dose_bird=%g is a non-physical value.' % self.dose_bird)
        if self.det < 0:
            raise ValueError\
            ('det=%g is a non-physical value.' % self.det)
        self.chron_bird = self.dose_bird/self.det


    def chronconb(self):
        if self.chron_bird == None:
            raise ValueError\
            ('chron_bird variable equals None and therefor this function cannot be run.')
        if self.chron_bird < 1:
            return ('Drinking water exposure alone is NOT a potential concern for birds')
        else:
            return ('Exposure through drinking water alone is a potential concern for birds')

    # Chronic exposures for mammals

    def chron_mamm(self):
        try:
            self.dose_mamm = float(self.dose_mamm)
            self.act = float(self.act)
        except IndexError:
            raise IndexError\
            ('The upper bound estimate of exposure for mammals, and/or the'\
            ' adjusted chronic toxicity value for mammals must be supplied the'\
            ' command line.')
        except ValueError:
            raise ValueError\
            ('The upper bound estimate of exposure for mammals must be a real'\
            ' number, not "%mg/kg"' % self.dose_mamm)
        except ValueError:
            raise ValueError\
            ('The adjusted chronic toxicity value for mammals must be a real'\
            ' number, not "%mg/kg"' % self.act)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The adjusted chronic toxicity value for mammals must be non-zero.')
        if self.dose_mamm < 0:
            raise ValueError\
            ('dose_mamm=%g is a non-physical value.' % self.dose_mamm)
        if self.act < 0:
            raise ValueError\
            ('act=%g is a non-physical value.' % self.act)
        self.chron_mamm = self.dose_mamm/self.act

    def chronconm(self):
        if self.chron_mamm == None:
            raise ValueError\
            ('chron_mamm variable equals None and therefor this function cannot be run.')
        if self.chron_mamm < 1:
            return ('Drinking water exposure alone is NOT a potential concern for mammals')
        else:
            return ('Exposure through drinking water alone is a potential concern for mammals')

