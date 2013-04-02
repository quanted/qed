import unittest
import pytest
import logging
import sys
sys.path.append("utils")
sys.path.append("./")
from terrplant import terrplant_model
from CSVTestParamsLoader import CSVTestParamsLoader

logger = logging.getLogger("RiceTest")

def pytest_generate_tests(metafunc):
    params_matrix = get_params_matrix()
    metafunc.parametrize("numiter", range(len(params_matrix.get('a'))))
    
def get_params_matrix():
    csvTestParamsLoader = CSVTestParamsLoader('test/eco/terrplant/terrplant_unittest_inputs.csv')
    csvTestParamsLoader.loadParamsMatrix()
    return csvTestParamsLoader.params_matrix

def testRundry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.rundry(params_matrix.get('A')[numiter], params_matrix.get('I')[numiter], params_matrix.get('R')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("rundry", params_matrix.get('rundry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['runDry_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('rundry_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('I')[numiter] == 0:
            assert True
        else:
            assert False

def testRunSemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.runsemi(params_matrix.get('A')[numiter], params_matrix.get('I')[numiter], params_matrix.get('R')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("runsemi", params_matrix.get('runsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['runsemi_out'][numiter], 3) 
    except Error:
        if params_matrix.get('runsemi_out')[numiter] == None:
            assert True
        else:
            assert False

def testSpray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.spray(params_matrix.get('A')[numiter], params_matrix.get('D')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("spray", params_matrix.get('spray_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['spray_out'][numiter], 3) 
    except Error:
        if params_matrix.get('spray_out')[numiter] == None:
            assert True
        else:
            assert False

def testTotaldry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.totaldry(params_matrix.get('rundry_out')[numiter], params_matrix.get('spray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("totaldry", params_matrix.get('totaldry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['totaldry_out'][numiter], 3) 
    except ValueError:
        if params_matrix.get('totaldry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testTotalsemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.totalsemi(params_matrix.get('runsemi_out')[numiter], params_matrix.get('spray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("totalsemi", params_matrix.get('totalsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['totalsemi_out'][numiter], 3) 
    except ValueError:
        if params_matrix.get('totalsemi_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testNmsRQdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.nmsRQdry(params_matrix.get('totaldry_out')[numiter], params_matrix.get('nms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQdry", params_matrix.get('nmsRQdry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['nmsRQdry_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('nmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('nmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('nmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testLOCnmsdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCnmsdry(params_matrix.get('nmsRQdry_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCnmsdry", params_matrix.get('LOCnmsdry_out')[numiter], output)
        assert output == params_matrix['LOCnmsdry_out'][numiter]
    except ValueError:
        if params_matrix.get('LOCnmsdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('LOCnmsdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('LOCnmsdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False 


def testNmsRQsemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.nmsRQsemi(params_matrix.get('totalsemi_out')[numiter],params_matrix.get('nms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQsemi", params_matrix.get('nmsRQsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['nmsRQsemi_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('nmsRQsemi_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('nmsRQsemi_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('nmsRQsemi_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testLOCnmssemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCnmssemi(params_matrix.get('nmsRQsemi_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCnmssemi", params_matrix.get('LOCnmssemi_out')[numiter], output)
        assert output == params_matrix['LOCnmssemi_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testNmsRQspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.nmsRQspray(params_matrix.get('spray_out')[numiter],params_matrix.get('nms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQspray", params_matrix.get('nmsRQspray_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['nmsRQspray_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('nmsRQspray_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('nmsRQspray_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('nmsRQspray_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False


def testLOCnmsspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCnmsspray(params_matrix.get('nmsRQspray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCnmsspray", params_matrix.get('LOCnmsspray_out')[numiter], output)
        assert output, 3 == params_matrix['LOCnmsspray_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testLmsRQdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.lmsRQdry(params_matrix.get('totaldry_out')[numiter],params_matrix.get('lms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQdry", params_matrix.get('lmsRQdry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['lmsRQdry_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLOClmsdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOClmsdry(params_matrix.get('lmsRQdry_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOClmsdry", params_matrix.get('LOClmsdry_out')[numiter], output)
        assert output, 3 == params_matrix['LOClmsdry_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testLmsRQsemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.lmsRQsemi(params_matrix.get('totalsemi_out')[numiter],params_matrix.get('lms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQsemi", params_matrix.get('lmsRQsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['lmsRQsemi_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLOClmssemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOClmssemi(params_matrix.get('lmsRQsemi_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOClmssemi", params_matrix.get('LOClmssemi_out')[numiter], output)
        assert output == params_matrix['LOClmssemi_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testLmsRQspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOClmssemi(params_matrix.get('spray_out')[numiter],params_matrix.get('lms')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQspray", params_matrix.get('lmsRQspray_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['lmsRQspray_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLOClmsspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOClmsspray(params_matrix.get('lmsRQspray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOClmsspray", params_matrix.get('LOClmsspray_out')[numiter], output)
        assert output == params_matrix['LOClmsspray_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False 

def testNdsRQdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ndsRQdry(params_matrix.get('totaldry_out')[numiter],params_matrix.get('nds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQdry", params_matrix.get('ndsRQdry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['LOClmsspray_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False


def testLOCndsdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCndsdry(params_matrix.get('ndsRQdry_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCndsdry", params_matrix.get('LOCndsdry_out')[numiter], output)
        assert output == params_matrix['LOCndsdry_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False

def testNdsRQsemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ndsRQsemi(params_matrix.get('totalsemi_out')[numiter],params_matrix.get('nds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQsemi", params_matrix.get('ndsRQsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['ndsRQsemi_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLOCndssemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCndsRQsemi(params_matrix.get('ndsRQsemi_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCndssemi", params_matrix.get('LOCndssemi_out')[numiter], output)
        assert output == params_matrix['LOCndssemi_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False

def testNdsRQspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ndsRQspray(params_matrix.get('spray_out')[numiter],params_matrix.get('nds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQspray", params_matrix.get('ndsRQspray_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['ndsRQspray_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False
    
def testLOCndsspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCndsspray(params_matrix.get('ndsRQspray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCndsspray", params_matrix.get('LOCndsspray_out')[numiter], output)
        assert output == params_matrix['LOCndsspray_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False    

def testLdsRQdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ldsRQdry(params_matrix.get('totaldry_out')[numiter],params_matrix.get('lds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQdry", params_matrix.get('ldsRQdry_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['ldsRQdry_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLOCldsdry(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCldsRQdry(params_matrix.get('ldsRQdry_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCldsdry", params_matrix.get('LOCldsdry_out')[numiter], output)
        assert output == params_matrix['LOCldsdry_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLdsRQsemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ldsRQsemi(params_matrix.get('totalsemi_out')[numiter],params_matrix.get('lds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQsemi", params_matrix.get('ldsRQsemi_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['ldsRQsemi_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False
     

def testLOCldssemi(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCldssemi(params_matrix.get('ldsRQsemi_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCldssemi", params_matrix.get('LOCldssemi_out')[numiter], output)
        assert output == params_matrix['LOCldssemi_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False

def testLdsRQspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.ldsRQspray(params_matrix.get('spray_out')[numiter],params_matrix.get('lds')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQspray", params_matrix.get('ldsRQspray_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['ldsRQspray_out'][numiter], 3)
    except ValueError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if params_matrix.get('lmsRQdry_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Error:
        print "Test threw unexpected Error"
        assert False


def testLOCldsspray(numiter):
    params_matrix = get_params_matrix()
    try:
        output = terrplant_model.LOCldsspray(params_matrix.get('ldsRQspray_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("LOCldsspray", params_matrix.get('LOCldsspray_out')[numiter], output)
        assert output == params_matrix['LOCldsspray_out'][numiter]
    except Error:
        print "Test threw unexpected Error"
        assert False
