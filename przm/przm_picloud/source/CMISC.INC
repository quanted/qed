! THIS IS INCLUDE FILE MISC.INC

      REAL SOL , THKns , CONst , OUTput , SPActs , OUTpuj , OUTpjj

      INTEGER ISDay , ISMon , ISTyr , IEDay , IEMon , IEYr , PCMc ,     &
     &        NHOriz ,  KDFlag , THFlag , HORizn , IARg , IARg2 ,       &
     &        NPLots , NDCnt , RZI ,  ILP , LFReq1 , LFReq2 , CFLag ,   &
     &        RETcod , BDFlag , IY , JULday ,  MONth , LFReq3 , LEAp ,  &
     &        IFIrst , SAVal , SAYr , SADay , DELt , DOM ,  SAMon ,     &
     &        SSFlag , NACts , PLTdsn , DAYcnt , HEAder , MWFlg
      INTEGER CNDmo , AOFf

      CHARACTER*1 PLTyp , INDx
      CHARACTER*4 CMOnth , ITEm1 , ITEm2 , ITEm3 , STEp1 ,  STEp2 ,     &
     &            STEp3 , MODe , PLName , STEp4
      CHARACTER*8 SPAct
      CHARACTER*20 PSTnam
      CHARACTER*78 TITle , PTItle , STItle , ATItle , HTItle , NTItle
      COMMON /MSCI  / ISDay , ISMon , ISTyr , IEDay , IEMon , IEYr ,    &
     &                PCMc , NACts ,  THFlag , KDFlag , RZI ,  NHOriz , &
     &                CFLag , ILP , NDCnt , NPLots , IY ,  LFReq1 ,     &
     &                DELt , BDFlag , LFReq2 , SAYr , SADay , SAMon ,   &
     &                SSFlag ,  LFReq3 , LEAp , DOM , MONth , JULday ,  &
     &                DAYcnt , SAVal , HEAder ,  RETcod , IFIrst , MWFlg
      COMMON /MSCI1 / HORizn(ncmpts) , IARg(12) , IARg2(12) , PLTdsn(12)&
     &                ,  AOFf(3)

      COMMON /MSCR41/ SOL(3) , THKns(ncmpts) , CONst(12) , OUTput(12) , &
     &                 SPActs(3) , OUTpuj(12) , OUTpjj(12)
      COMMON /CHAR1 / CMOnth(12) , PLTyp(12) , MODe(12) , PLName(12) ,  &
     &                 PSTnam(3) , INDx(12)
      COMMON /CHAR  / ITEm1 , ITEm2 , ITEm3 , STEp1 , STEp2 , STEp3 ,   &
     &                SPAct , STEp4 ,  TITle , HTItle , PTItle ,        &
     &                STItle , ATItle , NTItle
      COMMON /CNDF  / CNDmo(2,13)
