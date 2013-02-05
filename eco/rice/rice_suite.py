import sys
import unittest
sys.path.append("../rice")
from rice_test import RiceTest

class RiceSuite(unittest.TestSuite):
    
    def addTests(self):
        this.addTest(RiceTest.test_msed())
        this.addTest(RiceTest.test_vw())
        this.addTest(RiceTest.test_mai1())
        this.addTest(RiceTest.test_cw())
        return this
    
    def suite(self):
        return addTests()