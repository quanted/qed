# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:16:54 2012

@author: msnyde02
"""

#diet = np.array([[1,1,1,], [2,2,2], [3,3,3]])
#water = np.array([[0.5, 0.1, 0.75]])
#multiply = (diet * water)
#dietwater = np.cumsum(multiply, axis=1)
#dietwater.ndim # dimension
#dietwater.shape # shape
#dietwater2 = 1 - dietwater
#
##dietwater3 = np.sum(denom2, axis = 1)
#dietwater4 =dietwater3[2]
import numpy as np
v_wb_a=np.array([[ 0.9, 0.85, 0.76, 0.85, 0.73, 0.73, 0.73]])
diet_mammal = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0,0,0,0,0,1,0], [0,0,0,0,1,0,0], [0,0,0,0,0,0,1]])
print diet_mammal.shape
#denom1=np.ones((1,1))
denom1 = v_wb_a * diet_mammal
    
print denom1