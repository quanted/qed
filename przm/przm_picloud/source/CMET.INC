      ! this is the include file cmet.inc

      REAL TEMp , PEVp , PFAc , DT , PREcip , TR , SFAc , THRufl ,      &
     &     SNOwfl ,  SOLrad , WINd , SPT , ALBedo , EMMiss , BBT ,      &
     &      THCond , VHTcap , STTdet , UBT , DBUff
      INTEGER IPEind , ITFlag , IDFlag , METdsn
      COMMON /METI  / IPEind , ITFlag , IDFlag
      COMMON /METI1 / METdsn(5)
      COMMON /METR4 / TEMp , PEVp , PFAc , PREcip , TR , SFAc , SNOwfl ,&
     &                THRufl ,  SOLrad , WINd , EMMiss , STTdet , UBT
      COMMON /METR41/ DT(12) , SPT(ncmpts) , ALBedo(13) , BBT(13) ,     &
     &                 THCond(ncmpts) , VHTcap(ncmpts)
      COMMON /METR42/ DBUff(366,5)
