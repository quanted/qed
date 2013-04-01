!     common block CBIO.INC

      REAL*8 AM , AC , AS , AR , KE , KSM , KCM
      REAL*8 KC , MKS , KR , KIN , KSK , KLDm , KLDc , KLDs , KLDr , KL1
      REAL*8 KL2 , USM , UCM , MUC , US , UR , Q , CM
      REAL*8 Y , YSM , YCM , YC , YS , YR , C12
      INTEGER*4 BIOflg
      COMMON /BIDGI / BIOflg
      COMMON /BIDGR / AM , AC , AS , AR , KE , KSM , KCM , KC , MKS ,   &
     &                KR , KIN , KSK , KLDm , KLDc , KLDs , KLDr , KL1 ,&
     &                KL2 , USM , UCM , MUC , US , UR , YSM , YCM , YC ,&
     &                YS , YR
      COMMON /BIDGR1/ Q(ncmpts) , CM(ncmpts)
      COMMON /BIDGR2/ Y(6,3,ncmpts) , C12(3,ncmpts)
