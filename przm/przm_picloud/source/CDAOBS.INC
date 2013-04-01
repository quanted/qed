!     common block CDAOBS.INC

      REAL*8 HDObs
      INTEGER*4 NDObs
      COMMON /DAOBS / NDObs(mxprt) , HDObs(mxtim,mxprt)
