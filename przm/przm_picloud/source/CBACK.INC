!     common block CBACK.INC

      REAL*8 TMHv , HVTm , QVTm
      INTEGER*4 NTSndh , ITSth
      COMMON /BACKUP/ NTSndh(2) , TMHv(2,mxtmv) , HVTm(2,mxtmv) ,       &
     &                QVTm(2,mxtmv) , ITSth(2)
