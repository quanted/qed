
import cloud
import os

api_key='3355'
api_secretkey='212ed160e3f416fdac8a3b71c90f3016722856b9'
cloud.setkey(api_key, api_secretkey)    


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
