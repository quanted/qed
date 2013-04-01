!     VADOFT storage variables
!-----Next 2 arrays for storing VADOFT values between VADOFT runs
      REAL SAVhed(mxnszo,mxnod)
      REAL SAVcnc(mxnszo,mxnod,3)

!-----Array for storing VADOFT corrected values of head and conc.
      REAL PINt(mxnod)

!-----VARS. TO PASS FLUX TO VADOFT
      REAL TOPflx(mxvdt) , TOWflx(mxvdt)
      COMMON /VADSTR41/ PINt , TOPflx , TOWflx
      COMMON /VADSTR42/ SAVhed
      COMMON /VADSTR43/ SAVcnc
