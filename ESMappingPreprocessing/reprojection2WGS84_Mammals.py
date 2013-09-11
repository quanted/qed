# import system modules
import arcpy
import os, fnmatch


#http://stackoverflow.com/questions/13299731/python-need-to-loop-through-directories-looking-for-txt-files
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


for fc in findFiles(r'F:\EPA_ES_Mapper\NatureServe\Mammals\Mammals_3.0', '*.shp'):
    try:
    # set local variables
        in_dataset = fc
    # get the coordinate system by describing a feature class
        dsc = arcpy.Describe("F:\EPA_ES_Mapper\Basemap\gz_2010_us_outline_5m\gz_2010_us_outline_5m.shp")
        # Coordinate system reference can be also found below:
        # http://resources.arcgis.com/en/help/main/10.1/018z/pdf/geographic_coordinate_systems.pdf
        coord_sys = dsc.spatialReference
        
    # run the tool
        arcpy.DefineProjection_management(in_dataset, coord_sys)
        
    # print messages when the tool runs successfully
        print(arcpy.GetMessages(0))
        
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        
    except Exception as ex:
        print(ex.args[0])

