<<<<<<< HEAD
import sys
import unittest
sys.path.append("../../../rice")
from rice_test import RiceMSEDTest
from rice_test import RiceVWTest
from rice_test import RiceMAI1Test
from rice_test import RiceCWTest

class RiceSuite(unittest.TestSuite):
    
    def __init__(self):
        self.riceMsedTest = RiceMSEDTest()
        self.riceVwTest = RiceVWTest()
        self.riceMai1Test = RiceMAI1Test()
        self.riceCwTest = RiceCWTest()
        
    def suite(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(self.riceMsedTest)
        self.suite.addTest(self.riceVwTest)
        self.suite.addTest(self.riceMai1Test)
        self.suite.addTest(self.riceCwTest)
        return self.suite
    
    def runTests(self):
        self.riceMsedTest.runTest()
        self.riceVwTest.runTest()
        self.riceMai1Test.runTest()
        self.riceCwTest.runTest()    
    
    def runSuite(self):
        unittest.TextTestRunner(verbosity=2).run(self.suite())
    
if __name__ == '__main__':
    riceSuite = RiceSuite()
    unittest.TextTestRunner(verbosity=2).run(riceSuite.suite())
=======
import pytest

pytest.main("-s test")
>>>>>>> pascact1
