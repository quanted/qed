import unittest
import pytest
import logging
import sys
import traceback
sys.path.append("utils")
sys.path.append("./")
from sip import sip_model
from CSVTestParamsLoader import CSVTestParamsLoader

logger = logging.getLogger("SipTest")

def pytest_generate_tests(metafunc):
    params_matrix = get_params_matrix()
    metafunc.parametrize("numiter", range(len(params_matrix.get('bw_bird'))))
    
def get_params_matrix():
    csvTestParamsLoader = CSVTestParamsLoader('test/eco/sip/sip_unittest_inputs.csv')
    csvTestParamsLoader.loadParamsMatrix()
    return csvTestParamsLoader.params_matrix

def test_fw_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.fw_bird(params_matrix.get('bw_bird')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("fw_bird", params_matrix.get('fw_bird_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['fw_bird_out'][numiter], 3) 
    except Exception:
        traceback.print_exc(file=sys.stdout)
        if params_matrix.get('fw_bird_out')[numiter] == None:
            assert True
        else:
            assert False

# Daily water intake rate for mammals

def test_fw_mamm(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.fw_mamm(params_matrix.get('bw_mamm')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("bw_mamm", params_matrix.get('fw_mamm_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['fw_mamm_out'][numiter], 3) 
    except Exception:
        if params_matrix.get('fw_mamm_out')[numiter] == None:
            assert True
        else:
            assert False


# Upper bound estimate of exposure for birds

def test_dose_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.dose_bird(params_matrix.get('fw_bird_out')[numiter], params_matrix.get('sol')[numiter], params_matrix.get('bw_bird')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("dose_bird", params_matrix.get('dose_bird_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['dose_bird_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('dose_bird_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('fw_bird_out')[numiter] < 0 or params_matrix.get('sol')[numiter] < 0 or params_matrix.get('bw_bird')[numiter] <= 0:
            assert True
        else:
            assert False

def test_dose_mamm(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.dose_mamm(params_matrix.get('fw_mamm_out')[numiter], params_matrix.get('sol')[numiter], params_matrix.get('bw_mamm')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("dose_mamm", params_matrix.get('dose_mamm_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['dose_mamm_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('dose_mamm_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('fw_mamm_out')[numiter] < 0 or params_matrix.get('sol')[numiter] < 0 or params_matrix.get('bw_mamm')[numiter] <= 0:
            assert True
        else:
            assert False

def test_at_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.at_bird(params_matrix.get('ld50')[numiter], params_matrix.get('aw_bird')[numiter], params_matrix.get('tw_bird')[numiter], params_matrix.get('mineau')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("at_bird", params_matrix.get('at_bird_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['at_bird_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('at_bird_out')[numiter] == None:
            assert True
        else:
            traceback.print_exc(file=sys.stdout)
            assert False
    except ValueError:
        if params_matrix.get('aw_bird')[numiter] < 0 or params_matrix.get('tw_bird')[numiter] <= 0 or params_matrix.get('ld50')[numiter] < 0 or params_matrix.get('mineau')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('at_bird_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False 

def test_at_mamm(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.at_mamm(params_matrix.get('ld50')[numiter], params_matrix.get('aw_mamm')[numiter], params_matrix.get('tw_mamm')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("at_mamm", params_matrix.get('at_mamm_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['at_mamm_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('at_mamm_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('ld50')[numiter] < 0 or params_matrix.get('aw_mamm')[numiter] < 0 or params_matrix.get('tw_mamm')[numiter] <= 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('at_mamm_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False 

def test_fi_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.fi_bird(params_matrix.get('bw_bird')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("fi_bird", params_matrix.get('fi_bird_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['fi_bird_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('fi_bird_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('bw_bird')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('fi_bird_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_det(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.det(params_matrix.get('noaec')[numiter],params_matrix.get('fi_bird_out')[numiter],params_matrix.get('bw_bird')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("det", params_matrix.get('det_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['det_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('det_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('noaec')[numiter] < 0 or params_matrix.get('fi_bird')[numiter] < 0 or params_matrix.get('bw_bird')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('det_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_act(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.act(params_matrix.get('noael')[numiter],params_matrix.get('tw_mamm')[numiter],params_matrix.get('aw_mamm')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("act", params_matrix.get('act_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['act_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('act_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('noael')[numiter] < 0 or params_matrix.get('tw_mamm')[numiter] < 0 or params_matrix.get('aw_mamm')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('act_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_acute_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.acute_bird(params_matrix.get('dose_bird_out')[numiter],params_matrix.get('at_bird_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("acute_bird", params_matrix.get('acute_bird_out')[numiter], output)
        assert round(output, 3) == round(params_matrix['acute_bird_out'][numiter], 3) 
    except ZeroDivisionError:
        if params_matrix.get('acute_bird_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('dose_bird_out')[numiter] < 0 or params_matrix.get('at_bird_out')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('acute_bird_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_acuconb(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.acuconb(params_matrix.get('acute_bird_out')[numiter])
        print "Test of function name: %s expected: %s != calculated: %s" % ("acuconb", params_matrix.get('acuconb_out')[numiter], output)
        assert output == params_matrix['acuconb_out'][numiter]
    except ValueError:
        if params_matrix.get('acuconb_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 

def test_acute_mamm(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.acute_mamm(params_matrix.get('dose_mamm_out')[numiter],params_matrix.get('at_mamm_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("acute_mamm", params_matrix.get('acute_mamm_out')[numiter], output)
        assert round(output, 6) == round(params_matrix['acute_mamm_out'][numiter], 6) 
    except ZeroDivisionError:
        if params_matrix.get('acute_mamm_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('dose_mamm_out')[numiter] < 0 or params_matrix.get('at_mamm_out')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('acute_mamm_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_acuconm(numiter):
    params_matrix = get_params_matrix()
    print params_matrix
    try:
        output = sip_model.acuconm(params_matrix.get('acute_mamm_out')[numiter])
        print "Test of function name: %s expected: %s != calculated: %s" % ("acuconm", params_matrix.get('acuconm_out')[numiter], output)
        assert output == params_matrix['acuconm_out'][numiter]
    except ValueError:
        if params_matrix.get('acuconm_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            traceback.print_exc(file=sys.stdout)
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 

def test_chron_bird(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.chron_bird(params_matrix.get('dose_bird_out')[numiter],params_matrix.get('det_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("chron_bird", params_matrix.get('chron_bird_out')[numiter], output)
        assert round(output, 6) == round(params_matrix['chron_bird_out'][numiter], 6) 
    except ZeroDivisionError:
        if params_matrix.get('chron_bird_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('dose_bird_out')[numiter] < 0 or params_matrix.get('det_out')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('chron_bird_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_chronconb(numiter):
    params_matrix = get_params_matrix()
    print params_matrix
    try:
        output = sip_model.chronconb(params_matrix.get('chron_bird_out')[numiter])
        print "Test of function name: %s expected: %s != calculated: %s" % ("chronconb", params_matrix.get('chronconb_out')[numiter], output)
        assert output == params_matrix['chronconb_out'][numiter]
    except ValueError:
        if params_matrix.get('chronconb_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            traceback.print_exc(file=sys.stdout)
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 

def test_chron_mamm(numiter):
    params_matrix = get_params_matrix()
    try:
        output = sip_model.chron_mamm(params_matrix.get('dose_mamm_out')[numiter],params_matrix.get('act_out')[numiter])
        print "Test of function name: %s expected: %i != calculated: %i" % ("chron_mamm", params_matrix.get('chron_mamm_out')[numiter], output)
        assert round(output, 6) == round(params_matrix['chron_mamm_out'][numiter], 6) 
    except ZeroDivisionError:
        if params_matrix.get('chron_mamm_out')[numiter] == None:
            assert True
        else:
            assert False
    except ValueError:
        if params_matrix.get('dose_mamm_out')[numiter] < 0 or params_matrix.get('act_out')[numiter] < 0:
            assert True
        else:
            assert False
    except Exception:
        if params_matrix.get('chron_mamm_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            print "Test threw unexpected Error"
            traceback.print_exc(file=sys.stdout)
            assert False

def test_chronconm(numiter):
    params_matrix = get_params_matrix()
    print params_matrix
    try:
        output = sip_model.chronconm(params_matrix.get('chron_mamm_out')[numiter])
        print "Test of function name: %s expected: %s != calculated: %s" % ("chronconm", params_matrix.get('chronconm_out')[numiter], output)
        assert output == params_matrix['chronconm_out'][numiter]
    except ValueError:
        if params_matrix.get('chronconm_out')[numiter] == None:
            print "Test threw expected Error"
            assert True
        else:
            traceback.print_exc(file=sys.stdout)
            assert False
    except Exception:
        print "Test threw unexpected Error"
        traceback.print_exc(file=sys.stdout)
        assert False 
