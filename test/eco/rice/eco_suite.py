import sys
import unittest
sys.path.append("rice")
from rice.rice_suite import RiceSuite

class EcoSuite(unittest.TestSuite):
    
    def __init__(self):
        self.riceSuite = RiceSuite()
        self.riceSuite.runSuite()
        pass
        
    def suite(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(self.riceSuite)
        return self.suite
    
if __name__ == '__main__':
    ecoSuite = EcoSuite()
    unittest.TextTestRunner(verbosity=2).run(ecoSuite.suite())