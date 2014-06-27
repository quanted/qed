'''
Created on Jan 17, 2013

@author: chance
'''
from StringIO import StringIO
import csv
import logging
import datetime

logger = logging.getLogger("CSVTestParamsLoader")

class CSVTestParamsLoader(object):
    '''
    classdocs
    '''

    def __init__(self,csv_params_file):
        '''
        Constructor
        '''
        self.csv_params_file = csv_params_file
        print self.csv_params_file
        self.params_matrix = {}
        
    def __str__(self):
        string_rep = "Params from csv file: " + self.csv_params_file + "\n"
        param_names = self.params_matrix.keys()
        for param_name in param_names:
            string_rep += "param name: " + param_name + " values: "
            param_values = self.params_matrix[param_name]
            for param_value in param_values:
                string_rep += str(param_value) + " "
            string_rep += "\n"
        return string_rep
    
    def loadParamsMatrixFromUpFile(self,thefile):
        params_data_rows = csv.reader(thefile.file.read().splitlines())
        self.loadParamsMatrixFromReader(params_data_rows)
             
    def loadParamsMatrix(self):
        params_data_rows = csv.reader(open(self.csv_params_file))
        self.loadParamsMatrixFromReader(params_data_rows)         
       
    def loadParamsMatrixFromReader(self, params_data_rows):
        param_names = params_data_rows.next()
        param_name_order = []
        for param_name in param_names:
            param_name_order.append(param_name);
            self.params_matrix[param_name] = []
        param_types = params_data_rows.next()
        param_name_type_dict = {}
        temp_order = list(param_name_order.__reversed__())
        for param_type in param_types:
            param_name = temp_order.pop()
            #logger.info(param_name + ":" + param_type)
            param_name_type_dict[param_name]=param_type
        for params_data_row in params_data_rows:
            temp_order = list(param_name_order.__reversed__())
            for param_data in params_data_row:
                param_name = temp_order.pop()
                if str(param_data) == "None":
                    self.params_matrix[param_name].append(None)
                elif("float" in param_name_type_dict[param_name]):
                    self.params_matrix[param_name].append(float(param_data))
                elif("string" in param_name_type_dict[param_name]):
                    self.params_matrix[param_name].append(str(param_data))
                    #print "String as input %s" % str(param_data)
                elif("boolean" in param_name_type_dict[param_name]):
                    if param_data == "yes" or param_data == "true":
                        self.params_matrix[param_name].append(True)
                    else:
                        self.params_matrix[param_name].append(False)
                elif("date" in param_name_type_dict[param_name]):
                    app_data_parts = param_data.split("-")
                    self.params_matrix[param_name].append(datetime.date(int(app_data_parts[0]),int(app_data_parts[1]),int(app_data_parts[2])))
        logger.info(self.params_matrix)
    
    def getTestValuesForParam(self,paramName):
        return self.params_matrix[paramName]
    
def main():
    csvTestParamLoader = CSVTestParamsLoader("../Rice/rice_unittest_inputs.csv")
    csvTestParamLoader.loadParamsMatrix()
    print csvTestParamLoader

if __name__ == '__main__':
    main()