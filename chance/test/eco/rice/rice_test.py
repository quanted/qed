import unittest
import pytest
import logging
import sys
sys.path.append("utils")
sys.path.append("./")
from rice import rice_model
from CSVTestParamsLoader import CSVTestParamsLoader

logger = logging.getLogger("RiceTest")

def pytest_generate_tests(metafunc):
    params_matrix = get_params_matrix()
    metafunc.parametrize("numiter", range(len(params_matrix.get('a'))))

def testMsed(numiter):
    params_matrix = get_params_matrix()
    output = rice_model.msed(params_matrix.get('dsed')[numiter], params_matrix.get('a')[numiter], params_matrix.get('pb')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("msed", params_matrix.get('msed_out')[numiter], output)
    assert round(output, 3) == round(params_matrix['msed_out'][numiter], 3) 
    # assert numiter == numiter  

def testVW(numiter):
    params_matrix = get_params_matrix()
    output = rice_model.vw(params_matrix.get('dw')[numiter], params_matrix.get('a')[numiter], params_matrix.get('dsed')[numiter], params_matrix.get('osed')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("vw", params_matrix.get('vw_out')[numiter], output)
    assert round(output, 3) == round(params_matrix['vw_out'][numiter], 3) 
    
def testMAI1(numiter):
    params_matrix = get_params_matrix()
    output = rice_model.mai1(params_matrix.get('mai')[numiter], params_matrix.get('a')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("mai1", params_matrix.get('mai1_out')[numiter], output)
    assert round(output, 3) == round(params_matrix['mai1_out'][numiter], 3) 
        
def testCW(numiter):
    params_matrix = get_params_matrix()
    output = rice_model.cw(rice_model.mai1(params_matrix.get('mai')[numiter], params_matrix.get('a')[numiter]), params_matrix.get('dw')[numiter], params_matrix.get('dsed')[numiter], params_matrix.get('osed')[numiter], params_matrix.get('pb')[numiter], params_matrix.get('kd')[numiter])
    print "Test of function name: %s expected: %i != calculated: %i" % ("cw", params_matrix.get('cw_out')[numiter], output)
    assert round(output, 3) == round(params_matrix['cw_out'][numiter], 3) 
    
def get_params_matrix():
    csvTestParamsLoader = CSVTestParamsLoader('test/eco/rice/rice_unittest_inputs.csv')
    csvTestParamsLoader.loadParamsMatrix()
    return csvTestParamsLoader.params_matrix
        