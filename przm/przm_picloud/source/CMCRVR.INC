!     common block include file CMCRVR.INC

!     + + + PARAMETERS + + +
      INTEGER MCMAX , NMAX , NCMAX , NRMAX , NEMP , MCSUM , NPMAX
      PARAMETER (MCMAX=150,NMAX=50,NCMAX=50,NRMAX=1000,NEMP=20)
!     MCMAX - ???
!     NMAX  - ???
!     NCMAX - ???
!     NRMAX - ???
!     NEMP  - ???
      PARAMETER (MCSUM=MCMAX+NMAX,NPMAX=5)
!     MCSUM - ???
!     NPMAX - ???

!     common block for Monte Carlo variables:
      COMMON /MCRI  / NRUns , MCVar , NVAr
      COMMON /MCRI1 / LARr , INDz , NDAt , IND1 , NAVg
      COMMON /MCRR4 / PALph
      COMMON /MCRR41/ RMC , XMC , XCDf , VAR , CNMc
      COMMON /MCRR42/ STOr
      COMMON /MCRR43/ DISt
      COMMON /MCRR82/ STAt , CORr , BBTrns , DECom
      COMMON /MCCHAR/ PNAme , SNAme

      INTEGER NRUns , MCVar , NVAr , LARr(MCSUM) , INDz(NMAX,2) ,       &
     &        NDAt(MCMAX) , IND1(NMAX,2) , NAVg(NMAX)
      REAL RMC(MCMAX) , VAR(MCMAX,5) , DISt(NEMP,2,MCMAX) , PALph ,     &
     &     CNMc(MCMAX)
      REAL*8 STAt(NMAX,6) , CORr(NMAX,NMAX) , STOr(NPMAX,NMAX) ,        &
     &       BBTrns(MCMAX,MCMAX) , DECom(MCMAX,MCMAX) , XMC(NMAX) ,     &
     &       XCDf(NCMAX,NRMAX)
      CHARACTER*20 PNAme(MCMAX) , SNAme(NMAX,3)
