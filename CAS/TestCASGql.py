import unittest
import sys
sys.path.append('./')
from CASGql import CASGql

class TestCASGql:
    def setUp(self):
        pass
    
    def suite(self):
        pass


class TestCloseDbConnection(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testCloseDbConnection(self):
        self.fail("Expected Failure - create test")


class TestGetAllChemicalNames(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testGetAllChemicalNames(self):
        self.fail("Expected Failure - create test")


class TestGetAllChemicalNamesCASNumbers(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testGetAllChemicalNamesCASNumbers(self):
        self.fail("Expected Failure - create test")        


class TestGetAllChemNamesCASNumsUTF8(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testGetAllChemNamesCASNumsUTF8(self):
        self.fail("Expected Failure - create test")        


class TestGetCASNumberFromChemicalName(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testGetCASNumberFromChemicalName(self):
        self.fail("Expected Failure - create test")


class TestGetChemicalNameFromCASNumber(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testGetChemicalNameFromCASNumber(self):
        self.fail("Expected Failure - create test")


class TestMakeListUTF8(unittest.TestCase):

    def setUp(self):
        self.CASGqlLocalNoParams = CASGql()
        self.CASGqlLocalParams = CASGql("localhost","ubertool","ubertool","ubertool")
    
    def testMakeListUTF8(self):
        self.fail("Expected Failure - create test")


