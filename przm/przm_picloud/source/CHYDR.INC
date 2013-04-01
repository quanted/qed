!     include file CHYDR.INC

      INTEGER :: CN(nc,32,3)
      REAL SW , WP , FC , ET , CINt , CEVap , AFIeld , USLek , USLels , &
     &      USLep , DELx , THEtn , INAbs , SMElt , BD , THEto , CINtb , &
     &     DIN ,  AINf , RUNof , THEtas , AD , VEL , THEfc , THEwp ,    &
     &     WBAl , CWBal ,  OSNow , CORed , THEth , SEDl , TDEt , SANd , &
     &     CLAy , SNOw ,  ADL , OUTflo , DPN , Z , ZC , DEN , TOP ,     &
     &     PFRac , PRDpth , DRI ,  ERSndp , ERSntt
      REAL USLec , HL , SLP , CFAc , N1 , MNGn , CVNum
      REAL TFCrnf , TWPrnf
      INTEGER NCOm1 , NCOm2  , NCOm0 , NCOm2m , ICNah , HSWzt ,         &
     &        ISCond ,  ERFlag , NUM , VLFlag , NPI , IRFlag , MCOflg , &
     &        RATio ,  PCOunt , ICRoss , STRyr , ENDyr , MOCflg ,       &
     &        FRMflg , RNCmpt ,  IREg , NUSlec , JUSlec , GDUslec ,     &
     &        GMUslec , MTR1 , NRZcomp
      COMMON /HYRI  / NCOm1 , NCOm2 , HSWzt , ISCond , NCOm0 , FRMflg , &
     &                NCOm2m ,  ERFlag , STRyr , ENDyr , IRFlag , NUM , &
     &                VLFlag , MCOflg ,  MOCflg , RNCmpt
      COMMON /HYRI  / IREg , MTR1 , NRZcomp
      COMMON /HYRI1 / ICNah(nc) , NPI(3) , ICRoss(3) , NUSlec(nc)
      COMMON /HYRI2 / RATio(3,ncmpts) , PCOunt(3,ncmpts) , JUSlec(nc,32)
      COMMON /HYRI3 / CN
      COMMON /HYRR4 / THEth , CINt , CEVap , AFIeld , INAbs , SEDl ,    &
     &                TDEt , CORed ,  SMElt , CINtb , DIN , RUNof ,     &
     &                WBAl , CWBal , SNOw , OSNow ,  USLek , USLels ,   &
     &                USLep , PFRac , PRDpth , ERSndp , ERSntt ,  HL ,  &
     &                SLP , CFAc , N1 , CVNum , TFCrnf , TWPrnf
      COMMON /HYRR41/ SW(ncmpts) , WP(ncmpts) , FC(ncmpts) , ET(ncmpts) &
     &                ,  CLAy(ncmpts) , THEtn(ncmpts) , BD(ncmpts) ,    &
     &                 THEto(ncmpts) , AINf(ncmpts) , THEtas(ncmpts) ,  &
     &                 AD(ncmpts) , SANd(ncmpts) , VEL(ncmpts) ,        &
     &                 THEfc(ncmpts) , THEwp(ncmpts) , ADL(ncmpts) ,    &
     &                 OUTflo(ncmpts) , DELx(ncmpts) , DPN(ncmpts) ,    &
     &                 ZC(ncmpts) , DRI(ncmpts)
      COMMON /HYRR42/ Z(3,npii) , DEN(3,ncmpts) , GDUslec(nc,32) ,      &
     &                 GMUslec(nc,32) ,  TOP(3,ncmpts-1) , USLec(nc,32) &
     &                , MNGn(nc,32)
