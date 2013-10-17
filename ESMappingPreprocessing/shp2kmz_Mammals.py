# import system modules
import arcpy
import os
import fnmatch

# Iterate the directory and sub-folders to find files with specific extension
#http://stackoverflow.com/questions/13299731/python-need-to-loop-through-directories-looking-for-txt-files
def findFiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)


# Name: LayerToKML 
for fc in findFiles(r'F:\EPA_ES_Mapper\NatureServe\Mammals\Mammals_3.0', '*.shp'):
    try:
        # Set local variables
        in_features = fc
        clip_features = "F:\EPA_ES_Mapper\Basemap\states_21basic\states.shp"
        out_feature_class = fc[:-4]+"_clip.shp"
        xy_tolerance = ""

        # Execute Clip to crop the glboal dataset of Mammals into within U.S.
        arcpy.Clip_analysis(in_features, clip_features, out_feature_class, xy_tolerance)

        if arcpy.management.GetCount(out_feature_class)[0] != "0":
            # Set Local Variables
            # composite = 'COMPOSITE'
            # COMPOSITE 
            # The output KML file will be a single composite image representing the raster/vector features.
            # The raster is draped over the terrain as a KML GroundOverlay. 
            # It reduces the size of the output KMZ file, but individual features in the KML are not selectable.
            pixels = 1024
            dpi = 96
            clamped = 'CLAMPED_TO_GROUND'
            scale = 1
            # 1 denotes there are no scale dependencies
            # Strips the '.shp' part of the name and appends '.kmz'
            lyr = out_feature_class[:-4]+".lyr"
            outKML = out_feature_class[:-4] + ".kmz"
            print fc
            print out_feature_class
            print lyr
            print outKML

            # Process: Make Feature Layer
            arcpy.MakeFeatureLayer_management(out_feature_class, lyr)
            
            #Execute LayerToKML
            arcpy.LayerToKML_conversion(lyr,outKML, scale, "TRUE",lyr, pixels, dpi, clamped)#TRUE denotes COMPOSITE

    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
        
    except Exception as ex:
        print(ex.args[0])

        
