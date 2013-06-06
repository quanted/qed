import unittest
import pytest
import logging
import sys
sys.path.append("utils")
sys.path.append("./")
from iec import iec_output
from CSVTestParamsLoader import CSVTestParamsLoader

logger = logging.getLogger("IECTest")

def pytest_generate_tests(metafunc):
    params_matrix = get_params_matrix()
    metafunc.parametrize("numiter",range(len(params_matrix.get('LC50'))))

def testZScoreF(numiter):
    params_matrix = get_params_matrix()
    output = iec_output.z_score_f(params_matrix.get('dose_response')[numiter],params_matrix.get('LC50')[numiter],params_matrix.get('threshold')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("Z Score F",params_matrix.get('z_score_f_out')[numiter],output)
    assert round(output,3) == round(params_matrix['z_score_f_out'][numiter],3) 

def testF8f(numiter):
    params_matrix = get_params_matrix()
    output = iec_output.F8_f(params_matrix.get('dose_response')[numiter],params_matrix.get('LC50')[numiter],params_matrix.get('threshold')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("F8 f",params_matrix.get('F8_f_out')[numiter],output)
    assert round(output,3) == round(params_matrix['F8_f_out'][numiter],3) 
    
def testChancef(numiter):
    params_matrix = get_params_matrix()
    output = iec_output.chance_f(params_matrix.get('dose_response')[numiter],params_matrix.get('LC50')[numiter],params_matrix.get('threshold')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("Chance f",params_matrix.get('chance_f_out')[numiter],output)
    assert round(output,3) == round(params_matrix['chance_f_out'][numiter],3) 
    
def get_params_matrix():
    csvTestParamsLoader = CSVTestParamsLoader('test/eco/iec/iec_unittest_inputs.csv')
    csvTestParamsLoader.loadParamsMatrix()
    return csvTestParamsLoader.params_matrix
        