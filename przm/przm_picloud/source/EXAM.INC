!        Include file EXAM.INC

! +++ Date: Wednesday, 7 October 1992.  Time: 10:48:25.

!     Change all INTEGER*2 to *4 - D. Disney
      CHARACTER*16 CASsno(3)
      REAL*4 YIEld(3)
      INTEGER*2 EXMflg , IYOld , CNAp2 , OFFst
      INTEGER*4 EXMenv
      INTEGER*4 APDex(napp) , APMex(napp) , EXMchm(3) , NPRoc(3) ,      &
     &          RFOrm(3) , EXPrnt(3)

!         INTEGER*2  EXMFLG,IYOLD,APDEX(NAPP),APMEX(NAPP),CNAP2,OFFST
! +++
      COMMON /EXMSI / EXMflg , IYOld , CNAp2 , OFFst , EXMenv
      COMMON /EXMSI1/ APDex , APMex , EXMchm , NPRoc , RFOrm , EXPrnt
      COMMON /EXMSR / YIEld
      COMMON /EXMSC / CASsno
