import unittest
import pytest
import logging
import sys
import traceback
sys.path.append("utils")
sys.path.append("./")
from terrplant import terrplant_model
from CSVTestParamsLoader import CSVTestParamsLoader

logger = logging.getLogger("TerrPlantTest")

def pytest_generate_tests(metafunc):
    params_matrix = get_params_matrix()
    metafunc.parametrize("numiter", range(len(params_matrix.get('A'))))
    
def get_params_matrix():
    csvTestParamsLoader = CSVTestParamsLoader('test/eco/terrplant/terrplant_unittest_inputs.csv')
    csvTestParamsLoader.loadParamsMatrix()
    return csvTestParamsLoader.params_matrix

def get_terrplant_data(numiter):
    params_matrix = get_params_matrix()
    A = params_matrix.get('A')[numiter]
    I =  params_matrix.get('I')[numiter]
    R =  params_matrix.get('R')[numiter]
    D =  params_matrix.get('D')[numiter]
    nms = params_matrix.get('nms')[numiter]
    lms =  params_matrix.get('lms')[numiter]
    nds =  params_matrix.get('nds')[numiter]
    lds =  params_matrix.get('D')[numiter]
    terr = terrplant_model.terrplant(True,False,A,I,R,D,nms,lms,nds,lds)
    terrplant_expected_results = {}
    terrplant_expected_results['rundry_out'] = params_matrix.get('rundry_out')[numiter]
    terrplant_expected_results['runsemi_out'] = params_matrix.get('runsemi_out')[numiter]
    terrplant_expected_results['spray_out'] = params_matrix.get('spray_out')[numiter]
    terrplant_expected_results['totaldry_out'] = params_matrix.get('totaldry_out')[numiter]
    terrplant_expected_results['totalsemi_out'] = params_matrix.get('totalsemi_out')[numiter]
    terrplant_expected_results['nmsRQdry_out'] = params_matrix.get('nmsRQdry_out')[numiter]
    terrplant_expected_results['LOCnmsdry_out'] = params_matrix.get('LOCnmsdry_out')[numiter]
    terrplant_expected_results['nmsRQsemi_out'] = params_matrix.get('nmsRQsemi_out')[numiter]
    terrplant_expected_results['LOCnmssemi_out'] = params_matrix.get('LOCnmssemi_out')[numiter]
    terrplant_expected_results['nmsRQspray_out'] = params_matrix.get('nmsRQspray_out')[numiter]
    terrplant_expected_results['LOCnmsspray_out'] = params_matrix.get('LOCnmsspray_out')[numiter]
    terrplant_expected_results['lmsRQdry_out'] = params_matrix.get('lmsRQdry_out')[numiter]
    terrplant_expected_results['LOClmsdry_out'] = params_matrix.get('LOClmsdry_out')[numiter]
    terrplant_expected_results['lmsRQsemi_out'] = params_matrix.get('lmsRQsemi_out')[numiter]
    terrplant_expected_results['LOClmssemi_out'] = params_matrix.get('LOClmssemi_out')[numiter]
    terrplant_expected_results['lmsRQspray_out'] = params_matrix.get('lmsRQspray_out')[numiter]
    terrplant_expected_results['LOClmsspray_out'] = params_matrix.get('LOClmsspray_out')[numiter]

    terrplant_expected_results['ndsRQdry_out'] = params_matrix.get('ndsRQdry_out')[numiter]
    terrplant_expected_results['LOCndsdry_out'] = params_matrix.get('LOCndsdry_out')[numiter]
    terrplant_expected_results['ndsRQsemi_out'] = params_matrix.get('ndsRQsemi_out')[numiter]
    terrplant_expected_results['LOCndssemi_out'] = params_matrix.get('LOCndssemi_out')[numiter]
    terrplant_expected_results['ndsRQspray_out'] = params_matrix.get('ndsRQspray_out')[numiter]
    terrplant_expected_results['LOCndsspray_out'] = params_matrix.get('LOCndsspray_out')[numiter]
    terrplant_expected_results['ldsRQdry_out'] = params_matrix.get('ldsRQdry_out')[numiter]
    terrplant_expected_results['LOCldsdry_out'] = params_matrix.get('LOCldsdry_out')[numiter]
    terrplant_expected_results['ldsRQsemi_out'] = params_matrix.get('ldsRQsemi_out')[numiter]
    terrplant_expected_results['LOCldssemi_out'] = params_matrix.get('LOCldssemi_out')[numiter]
    terrplant_expected_results['ldsRQspray_out'] = params_matrix.get('ldsRQspray_out')[numiter]
    terrplant_expected_results['LOCldsspray_out'] = params_matrix.get('LOCldsspray_out')[numiter]
    return (terr,terrplant_expected_results)

def testRundry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.rundry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("rundry", terrplant_expected_results['rundry_out'], output)
        assert round(output , 3) == round(terrplant_expected_results['rundry_out'], 3) 
    except ZeroDivisionError:
        if terrplant_expected_results['rundry_out'] == None:
            assert True
        else:
            assert False
    except ValueError:
        if terrplant.A < 0 or terrplant.I <= 0 or terrplant.R:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testRunSemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.runsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("runsemi", terrplant_expected_results['runsemi_out'], output)
        assert round( output, 3) == round(terrplant_expected_results['runsemi_out'], 3) 
    except ZeroDivisionError:
        if terrplant_expected_results['runsemi_out'] == None:
            assert True
        else:
            assert False
    except ValueError:
        if terrplant.A < 0 or terrplant.I <= 0 or terrplant.R:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testSpray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.spray()
        print "Test of function name: %s expected: %i != calculated: %i" % ("spray", terrplant_expected_results['spray_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['spray_out'], 3) 
    except ZeroDivisionError:
        if terrplant_expected_results['spray_out'] == None:
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['spray_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testTotaldry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.totaldry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("totaldry", terrplant_expected_results['totaldry_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['totaldry_out'], 3)
    except ZeroDivisionError:
        if terrplant_expected_results['totaldry_out'] == None:
            assert True
        else:
            assert False
    except ValueError:
        if terrplant_expected_results['totaldry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testTotalsemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.totalsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("totalsemi", terrplant_expected_results['totalsemi_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['totalsemi_out'], 3)
    except ZeroDivisionError:
        if terrplant_expected_results['totalsemi_out'] == None:
            assert True
        else:
            assert False
    except ValueError:
        if terrplant_expected_results['totalsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNmsRQdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.nmsRQdry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQdry", terrplant_expected_results['nmsRQdry_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['nmsRQdry_out'], 3)
    except TypeError:
        if terrplant_expected_results['nmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['nmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['nmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testLOCnmsdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCnmsdry()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCnmsdry", terrplant_expected_results['LOCnmsdry_out'], output)
        assert output == terrplant_expected_results['LOCnmsdry_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCnmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCnmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCnmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNmsRQsemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.nmsRQsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQsemi", terrplant_expected_results['nmsRQsemi_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['nmsRQsemi_out'], 3)
    except TypeError:
        if terrplant_expected_results['nmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['nmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['nmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['nmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['nmsRQsemi_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testLOCnmssemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCnmssemi()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCnmssemi", terrplant_expected_results['LOCnmssemi_out'], output)
        assert output == terrplant_expected_results['LOCnmssemi_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCnmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCnmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCnmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNmsRQspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.nmsRQspray()
        print "Test of function name: %s expected: %i != calculated: %i" % ("nmsRQspray", terrplant_expected_results['nmsRQspray_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['nmsRQspray_out'], 3)
    except TypeError:
        if terrplant_expected_results['nmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['nmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['nmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['nmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['nmsRQspray_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False   

def testLOCnmsspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCnmsspray()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCnmsspray", terrplant_expected_results['LOCnmsspray_out'], output)
        assert output == terrplant_expected_results['LOCnmsspray_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCnmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCnmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCnmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testLmsRQdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.lmsRQdry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQdry", terrplant_expected_results['lmsRQdry_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['lmsRQdry_out'], 3)
    except TypeError:
        if terrplant_expected_results['lmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['lmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['lmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['lmsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['lmsRQdry_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False  

def testLOClmsdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOClmsdry()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOClmsdry", terrplant_expected_results['LOClmsdry_out'], output)
        assert output == terrplant_expected_results['LOClmsdry_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOClmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOClmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOClmsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testLmsRQsemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.lmsRQsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQsemi", terrplant_expected_results['lmsRQsemi_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['lmsRQsemi_out'], 3)
    except TypeError:
        if terrplant_expected_results['lmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['lmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['lmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['lmsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['lmsRQsemi_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False  

def testLOClmssemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOClmssemi()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOClmssemi", terrplant_expected_results['LOClmssemi_out'], output)
        assert output == terrplant_expected_results['LOClmssemi_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOClmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOClmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOClmssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testLmsRQspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.lmsRQspray()
        print "Test of function name: %s expected: %i != calculated: %i" % ("lmsRQspray", terrplant_expected_results['lmsRQspray_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['lmsRQspray_out'], 3)
    except TypeError:
        if terrplant_expected_results['lmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['lmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['lmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['lmsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['lmsRQspray_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False 

def testLOClmsspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOClmsspray()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOClmsspray_out", terrplant_expected_results['lmsRQspray_out'], output)
        assert output == terrplant_expected_results['LOClmsspray_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOClmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOClmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOClmsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNdsRQdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ndsRQdry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQdry", terrplant_expected_results['ndsRQdry_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ndsRQdry_out'], 3)
    except TypeError:
        if terrplant_expected_results['ndsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ndsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ndsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ndsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ndsRQdry_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False 

def testLOCndsdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCndsdry()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCndsdry", terrplant_expected_results['LOCndsdry_out'], output)
        assert output == terrplant_expected_results['LOCndsdry_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCndsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCndsdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCndsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNdsRQsemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ndsRQsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQsemi", terrplant_expected_results['ndsRQsemi_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ndsRQsemi_out'], 3)
    except TypeError:
        if terrplant_expected_results['ndsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ndsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ndsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ndsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ndsRQsemi_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False  

def testLOCndssemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCndssemi()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCndssemi", terrplant_expected_results['LOCndssemi_out'], output)
        assert output == terrplant_expected_results['LOCndssemi_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCndssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCndssemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCndssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testNdsRQspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ndsRQspray()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ndsRQspray", terrplant_expected_results['ndsRQspray_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ndsRQspray_out'], 3)
    except TypeError:
        if terrplant_expected_results['ndsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ndsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ndsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ndsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ndsRQspray_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testLOCndsspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCndsspray()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCndsspray", terrplant_expected_results['LOCndsspray_out'], output)
        assert output == terrplant_expected_results['LOCndsspray_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCndsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCndsspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCndsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 

def testLdsRQdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ldsRQdry()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQdry", terrplant_expected_results['ldsRQdry_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ldsRQdry_out'], 3)
    except TypeError:
        if terrplant_expected_results['ldsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ldsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ldsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ldsRQdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ldsRQdry_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testLOCldsdry(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCldsdry()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCldsdry", terrplant_expected_results['LOCldsdry_out'], output)
        assert output == terrplant_expected_results['LOCldsdry_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCldsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCldsdry_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCldsdry_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 

def testLdsRQsemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ldsRQsemi()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQsemi", terrplant_expected_results['ldsRQsemi_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ldsRQsemi_out'], 3)
    except TypeError:
        if terrplant_expected_results['ldsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ldsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ldsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ldsRQsemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ldsRQsemi_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False
    
def testLOCldssemi(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCldssemi()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCldssemi", terrplant_expected_results['LOCldssemi_out'], output)
        assert output == terrplant_expected_results['LOCldssemi_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCldssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCldssemi_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCldssemi_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False

def testLdsRQspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.ldsRQspray()
        print "Test of function name: %s expected: %i != calculated: %i" % ("ldsRQspray", terrplant_expected_results['ldsRQspray_out'], output)
        assert round(output, 3) == round(terrplant_expected_results['ldsRQspray_out'], 3)
    except TypeError:
        if terrplant_expected_results['ldsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['ldsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except ZeroDivisionError:
        if terrplant_expected_results['ldsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except IndexError:
        if terrplant_expected_results['ldsRQspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        if terrplant_expected_results['ldsRQspray_out'] == None:
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def testLOCldsspray(numiter):
    terrplant_data = get_terrplant_data(numiter)
    terrplant = terrplant_data[0]
    terrplant_expected_results = terrplant_data[1]
    try:
        output = terrplant.LOCldsspray()
        print "Test of function name: %s expected: %s != calculated: %s" % ("LOCldsspray", terrplant_expected_results['LOCldsspray_out'], output)
        assert output == terrplant_expected_results['LOCldsspray_out']
    except ZeroDivisionError:
        if terrplant_expected_results['LOCldsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except TypeError:
        if terrplant_expected_results['LOCldsspray_out'] == None:
            print "Test threw expected Error"
            assert True
    except ValueError:
        if terrplant_expected_results['LOCldsspray_out'] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False