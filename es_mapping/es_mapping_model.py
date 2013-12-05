# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from collections import OrderedDict

import logging
logger = logging.getLogger('ES Model')


class es_mapping(object):
     def __init__(self, dictionary):
        self.ES_source = ''
        self.NSF = ''
        self.NSP = ''
        self.NSM = ''
        self.Crop = ''
        self.Pesticide = ''
        self.IUCN_Amphibians = ''
        self.IUCN_Birds = ''
        self.IUCN_Mammals = ''
        self.IUCN_Mammals_Marine = ''
        self.IUCN_Coral = ''
        self.IUCN_Reptiles = ''
        self.IUCN_Seagrasses = ''
        self.IUCN_SeaCucumbers = ''
        self.IUCN_Mangrove = ''
        self.IUCN_MarineFish = ''
        self.USFWS_p = ''
        self.USFWS_l = ''


        dictionary = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
        logger.info('===================')
        dictionary = OrderedDict(dictionary)
        for k, v in dictionary.items():
            setattr(self, k, v)
