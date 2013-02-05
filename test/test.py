import unittest
import sys
sys.path.append("../eco/rice")
from rice_suite import RiceSuite

class Test(unittest.TestSuite):
    
    def test(self):
        rice_suite = RiceSuite()
        suite = rice_suite.suite()
        suite.run()
        
def main():
    test = Test()
    test.test()

if __name__ == '__main__':
    main()       

        