
class terrplant:
    #Currently used variables
    I = 1
    A = 1
    D = 1
    R = 1
    nms = 1
    nds = 1
    lms = 1
    lds = 1

    #Variables in the input page
    chemical_name = ''
    pc_code = ''
    use = ''
    application_method = ''
    application_form = ''
    solubility = 1
    nmv = 1
    ndv = 1
    lmv = 1
    ldv = 1

    #Result variables
    rundry_results = -1
    runsemi_results = -1
    totaldry_results = -1
    totalsemi_results = -1
    spray_results = -1
    nmsRQdry_results = -1
    LOCnmsdry_results = ''
    nmsRQsemi_results = -1
    LOCnmssemi_results = ''
    nmsRQspray_results = -1
    LOCnmsspray_results = ''
    lmsRQdry_results = -1
    LOClmsdry_results = ''
    lmsRQsemi_results = -1
    LOClmssemi_results = ''
    lmsRQspray_results = -1
    LOClmsspray_results = ''
    ndsRQdry_results = -1
    LOCndsdry_results = ''
    ndsRQsemi_results = -1
    LOCndssemi_results = ''
    ndsRQspray_results = -1
    LOCndsspray_results = ''
    ldsRQdry_results = -1
    LOCldsdry_results = ''
    ldsRQsemi_results = -1
    LOCldssemi_results = ''
    ldsRQspray_results = -1
    LOCldsspray_results = ''

    def __init__(self,A,I,R,D,nms,lms,nds,lds):
        self.A = A
        self.I = I
        self.R = R
        self.D = D
        self.nms = nms
        self.lms = lms
        self.nds = nds
        self.lds = lds

    # EEC for runoff for dry areas
    def rundry(self):
        try:
            self.A = float(self.A)
            self.I = float(self.I)
            self.R = float(self.R)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation, and/or runoff fraction must be a real number')
        if self.A < 0:
            raise ValueError\
            ('A must be positive.')
        if self.I == 0:
            raise ZeroDivisionError\
            ('I must not equal zero.')
        if self.I < 0:
            raise ValueError\
            ('I must be positive.')
        if self.R < 0:
            raise ValueError\
            ('R must be positive.')
        if self.rundry_results == -1:
            self.rundry_results = (self.A/self.I) * self.R
        return self.rundry_results

    # EEC for runoff to semi-aquatic areas
    def runsemi(self):
        try:
            self.A = float(self.A)
            self.I = float(self.I)
            self.R = float(self.R)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation, and/or runoff fraction must be a real number')
        if self.A < 0:
            raise ValueError\
            ('A must be positive.')
        if self.I == 0:
            raise ZeroDivisionError\
            ('I must not equal zero.')
        if self.I < 0:
            raise ValueError\
            ('I must be positive.')
        if self.R < 0:
            raise ValueError\
            ('R must be positive.')
        if self.runsemi_results == -1:
            self.runsemi_results = (self.A/self.I) * self.R * 10
        return self.runsemi_results

    # EEC for spray drift
    def spray(self):
        try:
            self.A = float(self.A)
            self.D = float(self.D)
        except ZeroDivisionError:
            raise ZeroDivisionError\
            ('The incorporation must be non-zero.')
        except IndexError:
            raise IndexError\
            ('The application rate, incorporation, and/or runoff fraction must be supplied on the command line. ')
        except ValueError:
            raise ValueError\
            ('The application rate, incorporation, and/or runoff fraction must be a real number')
        if self.A < 0:
            raise ValueError\
            ('A must be positive.')
        if self.D < 0:
            raise ValueError\
            ('D must be positive.')
        if self.spray_results == -1:
            self.spray_results = self.A * self.D
        return self.spray_results

    # EEC total for dry areas
    def totaldry(self):
        if self.totaldry_results == -1:
            try:
                if self.rundry_results == -1:
                    self.rundry()
                if self.spray_results == -1:
                    self.spray()
                if self.rundry_results == None or self.spray_results == None:
                    raise ValueError\
                    ('Either the rundry or spray variables equals None and therefor this function cannot be run.')
                self.totaldry_results = self.rundry_results * self.spray_results
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
        return self.totaldry_results


    # EEC total for semi-aquatic areas
    def totalsemi (self):
        if self.totalsemi_results == -1:
            try:
                if self.runsemi_results == -1:
                    self.runsemi()
                if self.spray_results == -1:
                    self.spray()
                if self.runsemi_results == None or self.spray_results == None:
                    raise ValueError\
                    ('Either the runsemi or spray variables equals None and therefor this function cannot be run.')
                self.totalsemi_results = self.runsemi_results * self.spray_results
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
        return self.totalsemi_results


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

    def nmsRQdry(self):
        if self.nmsRQdry_results == -1:
            try:
                self.nms = float(self.nms)
                self.totaldry_results = float(self.totaldry_results)
            except ValueError:
                raise ValueError\
                ('The application rate, incorporation, and/or runoff fraction must be a real number')
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nms < 0:
                raise ValueError\
                ('nms=%g is a non-physical value' %self.nms)
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('Either the totaldry_results variable equals None and therefor this function cannot be run.')
            self.nmsRQdry_results = self.totaldry_results/self.nms
        return self.nmsRQdry_results


    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area

    def LOCnmsdry(self):
        if self.LOCnmsdry_results == '':
            try:
                if self.nmsRQdry_results == -1:
                    try:
                        self.nmsRQdry()
                    except TypeError:
                        raise TypeError\
                        ('totaldry equals None and therefor this function cannot be run.')
                if self.nmsRQdry_results == None:
                    raise ValueError\
                    ('nmsRQdry variable equals None and therefor this function cannot be run.')
                elif self.nmsRQdry_results >= 1.0:
                    self.LOCnmsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
                    ' the pesticide via runoff to a dry area indicates a potential risk.')
                else:
                    self.LOCnmsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
                    ' the pesticide via runoff to a dry area indicates that potential risk is minimal.')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
        return self.LOCnmsdry_results

    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area

    def nmsRQsemi(self):
        if self.nmsRQsemi_results == -1:
            try:
                self.nms = float(self.nms)
                self.totalsemi_results = float(self.totalsemi_results)
            except ValueError:
                raise ValueError\
                ('The application rate, incorporation, and/or runoff fraction must be a real number')             
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nms < 0:
                raise ValueError\
                ('nms=%g is a non-physical value' %self.nms)   
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('Either the totaldry_results variable equals None and therefor this function cannot be run.')
            self.nmsRQsemi_results = self.totalsemi_results/self.nms
        return self.nmsRQsemi_results

    # Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
    def LOCnmssemi(self):
        if self.LOCnmssemi_results == '':
            if self.nmsRQsemi_results == -1:
                try:
                    self.nmsRQsemi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nmsRQsemi_results == None:
                raise ValueError\
                ('nmsRQsemi variable equals None and therefor this function cannot be run.')
            if self.nmsRQsemi_results >= 1.0:
                self.LOCnmssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
            else:
                self.LOCnmssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.LOCnmssemi_results


    # Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def nmsRQspray(self):
        if self.nmsRQspray_results == -1:
            try:
                self.nms = float(self.nms)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('EEC for spray drift equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The EEC for spray drift needs to be supplied on the command line. ')
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nms < 0:
                raise ValueError\
                ('nms=%g is a non-physical value' %self.nms)   
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('Either the spray_results variable equals None and therefor this function cannot be run.')
            self.nmsRQspray_results = self.spray_results/self.nms
        return self.nmsRQspray_results

    # Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
    def LOCnmsspray(self):
        if self.LOCnmsspray_results == '':
            if self.nmsRQspray_results == -1:
                try:
                    self.nmsRQspray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.nmsRQspray_results == None:
                raise ValueError\
                ('nmsRQspray_results variable equals None and therefor this function cannot be run.')
            if self.nmsRQspray_results >= 1.0:
                self.LOCnmsspray_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCnmsspray_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCnmsspray_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
    def lmsRQdry(self):
        if self.lmsRQdry_results == -1:
            try:
                self.lms = float(self.lms)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number,'\
                ' not "%lbs ai/A"' %self.totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lms < 0:
                raise ValueError\
                ('lms=%g is a non-physical value' %self.lms)   
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('Either the spray_results variable equals None and therefor this function cannot be run.')
            self.lmsRQdry_results = self.totaldry_results/self.lms
        return self.lmsRQdry_results

    # Level of concern for listed monocot seedlings exposed to pesticide
    #  via runoff in a dry area
    def LOClmsdry(self):
        if self.LOClmsdry_results == '':
            if self.lmsRQdry_results == -1:
                try:
                    self.lmsRQdry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lmsRQdry_results == None:
                raise ValueError\
                ('lmsRQdry_results variable equals None and therefor this function cannot be run.')
            if self.lmsRQdry_results >= 1.0:
                self.LOClmsdry_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a dry area indicates a potential risk.')
            else:
                self.LOClmsdry_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a dry area indicates that potential risk is minimal.')
        return self.LOClmsdry_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
    def lmsRQsemi(self):
        if self.lmsRQsemi_results == -1:
            try:
                self.lms = float(self.lms)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totaldry equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number,'\
                ' not "%lbs ai/A"' %self.totalsemi_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lms < 0:
                raise ValueError\
                ('nms=%g is a non-physical value' %self.lms)   
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('Either the totalsemi_results variable equals None and therefor this function cannot be run.')
            self.lmsRQsemi_results = self.totalsemi_results/self.lms
        return self.lmsRQsemi_results

    # Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
    def LOClmssemi(self):
        if self.LOClmssemi_results == '':
            if self.lmsRQsemi_results == -1:
                try:
                    self.lmsRQsemi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lmsRQsemi_results == None:
                raise ValueError\
                ('lmsRQsemi variable equals None and therefor this function cannot be run.')
            if self.lmsRQsemi_results >= 1.0:
                self.LOClmssemi_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
            else:
                self.LOClmssemi_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        return self.LOClmssemi_results


    # Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
    def lmsRQspray(self):
        if self.lmsRQspray_results == -1:
            try:
                self.lms = float(self.lms)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lms < 0:
                raise ValueError\
                ('nms=%g is a non-physical value' %self.lms)  
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.lmsRQspray_results = self.spray_results/self.lms
        return self.lmsRQspray_results

    # Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
    def LOClmsspray(self):
        if self.LOClmsspray_results == '':
            if self.lmsRQspray_results == -1:
                try:
                    self.lmsRQspray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.lmsRQspray_results == None:
                raise ValueError\
                ('lmsRQspray variable equals None and therefor this function cannot be run.')
            if self.lmsRQspray_results >= 1.0:
                self.LOClmsspray_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOClmsspray_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOClmsspray_results


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ndsRQdry(self):
        if self.ndsRQdry_results == -1:
            try:
                self.nds = float(self.nds)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nds < 0:
                raise ValueError\
                ('nds=%g is a non-physical value' %self.nds)  
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totaldry_results variable equals None and therefor this function cannot be run.')
            self.ndsRQdry_results = self.totaldry_results/self.nds
        return self.ndsRQdry_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
    def LOCndsdry(self):
        if self.LOCndsdry_results == '':
            if self.ndsRQdry_results == -1:
                try:
                    self.ndsRQdry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.ndsRQdry_results == None:
                raise ValueError\
                ('ndsRQdry_results variable equals None and therefor this function cannot be run.')
            if self.ndsRQdry_results >= 1.0:
                self.LOCndsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
            else:
                self.LOCndsdry_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.LOCndsdry_results


    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ndsRQsemi(self):
        if self.ndsRQsemi_results == -1:
            try:
                self.nds = float(self.nds)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totalsemi_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nds < 0:
                raise ValueError\
                ('nds=%g is a non-physical value' %self.nds)  
            if self.totaldry_results == -1:
                self.totalsemi()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totalsemi_results variable equals None and therefor this function cannot be run.')
            self.ndsRQsemi_results = self.totalsemi_results/self.nds
        return self.ndsRQsemi_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
    def LOCndssemi(self):
        if self.LOCndssemi_results == '':
            if self.ndsRQsemi_results == -1:
                try:
                    self.ndsRQsemi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.ndsRQsemi_results == None:
                raise ValueError\
                ('ndsRQsemi_results variable equals None and therefor this function cannot be run.')
            if self.ndsRQsemi_results >= 1.0:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
            else:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.LOCndssemi_results

    # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ndsRQspray(self):
        if self.ndsRQspray_results == -1:
            try:
                self.nds = float(self.nds)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The the amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The the amount of spray drift exposure areas must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.nds < 0:
                raise ValueError\
                ('nds=%g is a non-physical value' %self.nds)
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.ndsRQspray_results = self.spray_results/self.nds
        return self.ndsRQspray_results

    # Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
    def LOCndsspray(self):
        if self.LOCndssemi_results == '':
            if self.ndsRQspray_results == -1:
                try:
                    self.ndsRQspray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.ndsRQspray_results == None:
                raise ValueError\
                ('ndsRQspray_results variable equals None and therefor this function cannot be run.')
            if self.ndsRQspray_results >= 1.0:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCndssemi_results = ('The risk quotient for non-listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCndssemi_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
    def ldsRQdry(self):
        if self.ldsRQdry_results == -1:
            try:
                self.lds = float(self.lds)
                self.totaldry_results = float(self.totaldry_results)
            except TypeError:
                raise TypeError\
                ('totaldry_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to dry areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to dry areas must be a real number, not "%lbs ai/A"' %totaldry_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lds < 0:
                raise ValueError\
                ('lds=%g is a non-physical value' %self.lds)
            if self.totaldry_results == -1:
                self.totaldry()
            if self.totaldry_results == None:
                raise ValueError\
                ('The totaldry_results variable equals None and therefor this function cannot be run.')
            self.ldsRQdry_results = self.totaldry_results/self.lds
        return self.ldsRQdry_results

    # Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
    def LOCldsdry(self):
        if self.LOCldsdry_results == '':
            if self.ldsRQdry_results == -1:
                try:
                    self.ldsRQdry()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            print ("LOCldsdry calculated: %i") % (self.ldsRQdry_results)
            if self.ldsRQdry_results == None:
                raise ValueError\
                ('ldsRQdry_results variable equals None and therefor this function cannot be run.')
            if self.ldsRQdry_results >= 1.0:
                self.LOCldsdry_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to dry areas indicates a potential risk.')
            else:
                self.LOCldsdry_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.LOCldsdry_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
    def ldsRQsemi(self):
        if self.ldsRQsemi_results == -1:
            try:
                self.lds = float(self.lds)
                self.totalsemi_results = float(self.totalsemi_results)
            except TypeError:
                raise TypeError\
                ('totalsemi_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The total amount of runoff and spray to semi-aquatic areas needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The total amount of runoff and spray to semi-aquatic areas must be a real number, not "%lbs ai/A"' %totaldry)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lds < 0:
                raise ValueError\
                ('lds=%g is a non-physical value' %self.lds)
            if self.totalsemi_results == -1:
                self.totalsemi()
            if self.totalsemi_results == None:
                raise ValueError\
                ('The totalsemi_results variable equals None and therefor this function cannot be run.')
            self.ldsRQsemi_results = self.totalsemi_results/self.lds
        return self.ldsRQsemi_results

    # Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
    def LOCldssemi(self):
        if self.LOCldssemi_results == '':
            if self.ldsRQsemi_results == -1:
                try:
                    self.ldsRQsemi()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.ldsRQsemi_results == None:
                raise ValueError\
                ('ldsRQsemi_results variable equals None and therefor this function cannot be run.')
            if self.ldsRQsemi_results >= 1.0:
                self.LOCldssemi_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
            else:
                self.LOCldssemi_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.LOCldssemi_results

    # Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
    def ldsRQspray(self):
        if self.ldsRQspray_results == -1:
            try:
                self.lds = float(self.lds)
                self.spray_results = float(self.spray_results)
            except TypeError:
                raise TypeError\
                ('spray_results equals None and therefor this function cannot be run.')
            except IndexError:
                raise IndexError\
                ('The amount of spray drift exposure needs to be supplied on the command line. ')
            except ValueError:
                raise ValueError\
                ('The amount of spray drift exposure must be a real number, not "%lbs ai/A"' %spray_results)
            except ZeroDivisionError:
                raise ZeroDivisionError\
                ('The incorporation must be non-zero.')
            if self.lds < 0:
                raise ValueError\
                ('lds=%g is a non-physical value' %self.lds)
            if self.spray_results == -1:
                self.spray()
            if self.spray_results == None:
                raise ValueError\
                ('The spray_results variable equals None and therefor this function cannot be run.')
            self.ldsRQspray_results = self.spray_results/self.lds
        return self.ldsRQspray_results

    # Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
    def LOCldsspray(self):
        if self.LOCldsspray_results == '':
            if self.ldsRQspray_results == -1:
                try:
                    self.ldsRQspray()
                except TypeError:
                    raise TypeError\
                    ('totaldry equals None and therefor this function cannot be run.')
            if self.ldsRQspray_results == None:
                raise ValueError\
                ('ldsRQspray_results variable equals None and therefor this function cannot be run.')
            if self.ldsRQspray_results >= 1.0:
                self.LOCldsspray_results = ('The risk quotient for listed monocot seedlings exposed to'\
            ' the pesticide via spray drift indicates a potential risk.')
            else:
                self.LOCldsspray_results = ('The risk quotient for listed monocot seedlings exposed to the'\
            ' pesticide via spray drift indicates that potential risk is minimal.')
        return self.LOCldsspray_results
