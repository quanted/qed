import cloud
import os
import sys 
lib_path = os.path.abspath('../../..')
sys.path.append(lib_path)
from ubertool_src import keys_Picloud_S3

cloud.setkey(keys_Picloud_S3.picloud_api_key, keys_Picloud_S3.picloud_api_secretkey)    


def geneec2(APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,FOTHAP): 
    cwd=os.getcwd()
    print "CWD=",cwd
    print(os.listdir(cwd))   #check what files are copied
    
    import g1
    ff=g1.geneec2(APPRAT,APPNUM,APSPAC,KOC,METHAF,WETTED,METHOD,AIRFLG,YLOCEN,GRNFLG,GRSIZE,ORCFLG,INCORP,SOL,METHAP,HYDHAP,FOTHAP)    
    return ff
cloud.rest.publish(func=geneec2, label='GENEEC_FORTRAN', _env='t-fortran77-test', _type='c1', _profile=True )
cloud.rest.publish(func=geneec2, label='GENEEC_FORTRAN_s1', _env='t-fortran77-test', _type='s1', _profile=True )
print 'Done'
