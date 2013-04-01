
      REAL*8 TIN , TIMa , UWF , DLAmda , FLX1 , FLXn , HTOl , TMAccw ,  &
     &       TMDcyv , TIMakp , TMAccp , TMDcys , TMAtmw , TMAtmp
      INTEGER NP , NE , ITRans , NITmax , NUMkm , NUMkpm , NSTep ,      &
     &        NVPr , INEwt , MARk , KPRop , IMOdl , IMBal , NTS , NMAt ,&
     &        ITMark , NOWrit , IOBsnd , NOBsnd , NTOmt , IREsol ,      &
     &        IFReun , ITEr , NOBswd , NODe(mxowd) , VADdsn(mxowd)
      CHARACTER*4 OUTf , OUTt
      CHARACTER*1 COD(mxowd)
      COMMON /CNTRI / NP , NE , ITRans , NITmax , NUMkm , NUMkpm ,      &
     &                NSTep , NVPr , INEwt , MARk , KPRop , IMOdl ,     &
     &                IMBal , NTS , NMAt , ITMark , NOWrit , IOBsnd ,   &
     &                NOBsnd , NTOmt , IREsol , IFReun , ITEr , NOBswd ,&
     &                VADdsn , NODe
      COMMON /CNTRR8/ TIN , TIMa , UWF , DLAmda , FLX1 , FLXn , HTOl ,  &
     &                TMAccw , TMDcyv , TIMakp , TMAccp , TMDcys ,      &
     &                TMAtmw , TMAtmp
      COMMON /CCONT / COD , OUTf , OUTt
