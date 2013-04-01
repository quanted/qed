!...  THIS IS INCLUDE FILE TABLE.INC

      REAL RAIn , SURf , IFLo , BFLo , TFLo , EVPo , SEDi , ROPst ,     &
     &     ERPst , LPSt , BPSt
      INTEGER STArtyr , ENDyear

      COMMON /OUTSUMS/ RAIn(12,mxyrs) , SURf(12,mxyrs) , IFLo(12,mxyrs) &
     &                 , BFLo(12,mxyrs) , TFLo(12,mxyrs) ,              &
     &                 EVPo(12,mxyrs) , SEDi(12,mxyrs) ,                &
     &                 ROPst(12,mxyrs,3) , ERPst(12,mxyrs,3) ,          &
     &                 LPSt(12,mxyrs,3) , BPSt(12,mxyrs,3)
      COMMON /YEARS / STArtyr , ENDyear
