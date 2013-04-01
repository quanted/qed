C
C
      SUBROUTINE TRDIA1 (A,B,C,X,F,N,LPRZOT,MODID)
C
C     + + + PURPOSE + + +
C
C     Solves a system of equations with a tridiagonal coefficient matrix
C     Modification date: 2/14/92 JAM

      ! Solution of a tri-diagonal matrix solution (by Thomas algorithm).
      ! A: The lower diagonal elements
      ! B: The diagonal elements
      ! C: The upper diagonal element
      ! F: The vector of source terms

      !
      ! [lsr] Thu Oct 13 12:22:09 EDT 2005
      ! MAke sure sytem is diagonally dominant.
      ! See numerical mathematics and computing, Ward cheney & david kincaid
      ! pags 274-276

C
C     + + + DUMMY ARGUMENTS + + +
C
      INCLUDE 'PPARM.INC'
      INTEGER     N,LPRZOT
      REAL        A(NCMPTS),B(NCMPTS),C(NCMPTS),F(NCMPTS),X(NCMPTS)
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     LPRZOT....Fortran unit number for output file
C     MODID...character string for identification of output file LPRZOT
C
C     + + + PARAMETERS + + +
C
C      INCLUDE 'PPARM.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER   I,NM1
      REAL      U(NCMPTS),Y(NCMPTS),L(NCMPTS),DLIMIT
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
C
      INTRINSIC ABS
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,SUBOUT
C
C-----Data intializations
C
      DATA U,Y,L / NCMPTS*0.0, NCMPTS*0.0, NCMPTS*0.0 /
      DATA DLIMIT /1.0E-10/
C
C-----End specifications
C
      MESAGE = 'TRDIA1'
      CALL SUBIN(MESAGE)
C
C-----Factor matrix into upper and lower halves
C
      U(1)=B(1)
      DO 10 I=2,N
        IF(ABS(U(I-1)).LT.1.0E-5) GO TO 40
        L(I)=A(I)/U(I-1)
        U(I)=B(I)-L(I)*C(I-1)
10    CONTINUE
C
C-----Solve LUX=F
C
      Y(1)=F(1)
      DO 20 I=2,N
         Y(I)=F(I)-L(I)*Y(I-1)
20    CONTINUE
C
      IF(ABS(U(N)).LT.1.0E-5) GO TO 40
         X(N)=Y(N)/U(N)
      IF (X(N).LE.DLIMIT) X(N) = 0.0
         NM1=N-1
         DO 30 I=1,NM1
           X(N-I)=(Y(N-I)-C(N-I)*X(N+1-I))/U(N-I)
           IF (X(N-I).LE.DLIMIT) X(N-I) = 0.0
30       CONTINUE
         GO TO 800
40    CONTINUE
      WRITE(LPRZOT,2000) (MODID,I=1,11)
C
C-----FORMAT statements
C
2000  FORMAT (1X,A3,1X,110(1H*),/,1X,A3,1X,110(1H*),/,1X,A3,/,1X,A3,50X,
     1        'E R R O R',/,1X,A3,/,1X,A3,10X,'TRIDIAGONAL MATRIX IN ',
     2        'SUBROUTINE TRDIA COULD NOT BE SOLVED FOR THIS DAY. ',
     3        'PRZM WILL',/,1X,A3,10X,' USE VALUES FOR THE LAST TIME ',
     4        'STEP AND CONTINUE ON. YOU MAY WANT TO STOP AND CHECK',/,
     5        1X,A3,10X,'BOTH THE INPUT SEQUENCE AND THE CODE IN ',
     6        'SLPEST AND TRDIA',/,1X,A3,/,1X,A3,/,1X,A3,1X,110(1H*))
C
 800  CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE PESTAP (K)
C
C     + + + PURPOSE + + +
C     Computes amount and location of pesticide application
C     (foliage, soil surface, or soil layer)
C     Modification date: 2/18/92 JAM
C     Further modified by PV @ AQUA TERRA Consultants 9/93 to hardwire
C     the calculation of pesticide depth in runoff to 1 cm
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER   K
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     K  -  chemical being simulated (1-3)
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL         DMAX,APPAMT,SLOPE,BASE
      CHARACTER*80 MESAGE
      REAL*8       EXPCHK
C
C     + + + INTRINSICS + + +
C
      INTRINSIC REAL,DBLE
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,EXPCHK,SUBOUT,PDSTRB,PZDSPL
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'PESTAP'
      CALL SUBIN(MESAGE)
C
c Pesticide Application Models
C     Soil surface pesticide application
      IF (CAM(K,NAPPC) .EQ. 1) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        DMAX = 4.0
        BASE=2./DMAX
        SLOPE=(-BASE/DMAX)
C
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
C
C
C     Linear foliar pesticide application
      ELSEIF (CAM(K,NAPPC) .EQ. 2) THEN
        IF (DELX(1) .GE. 2.0) THEN
          PLNTAP(K)    = COVER * TAPP(K,NAPPC) * APPEFF(K,NAPPC)
          SOILAP(K,1)  = (1.0- COVER) * TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
          PLNTAP(K)    = COVER * TAPP(K,NAPPC) * APPEFF(K,NAPPC)
          APPAMT       = (1.0- COVER) * TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C         Solve for base of isosceles triangle given:
C         length of 1 leg and area = 1.0
             DMAX = 4.0
          BASE=2./DMAX
          SLOPE=(-BASE/DMAX)
C
          CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
C
        FOLPST(K)    = FOLPST(K)+ PLNTAP(K)
        IFSCND(K,NCROP)= 0
C
C
C     Exponential foliar pesticide application
      ELSEIF (CAM(K,NAPPC) .EQ. 3) THEN
        IF (DELX(1) .GE. 2.0) THEN
          PLNTAP(K)    = (1.0-REAL(EXPCHK(DBLE(-FILTRA*WEIGHT)))) *
     1                   (TAPP(K,NAPPC)*APPEFF(K,NAPPC))
          SOILAP(K,1)  = (TAPP(K,NAPPC)*APPEFF(K,NAPPC))- PLNTAP(K)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     *                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
          PLNTAP(K)=(1.0-REAL(EXPCHK(DBLE(-FILTRA*WEIGHT))))
     *              *(TAPP(K,NAPPC)*APPEFF(K,NAPPC))
          APPAMT  = (TAPP(K,NAPPC)*APPEFF(K,NAPPC))- PLNTAP(K)
C
C         Solve for base of isosceles triangle given:
C         length of 1 leg and area = 1.0
             DMAX = 4.0
          BASE=2./DMAX
          SLOPE=(-BASE/DMAX)
C
          CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
        FOLPST(K)    = FOLPST(K)+ PLNTAP(K)
        IFSCND(K,NCROP)= 0
C
C
C     Incorporated pesticide application method 1
      ELSEIF (CAM(K,NAPPC) .EQ. 4) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
        BASE=0.
        SLOPE=0.
C
        DMAX = DEPI(K,NAPPC)
C
        IF(DEPI(K,NAPPC).EQ.0.0)THEN
          SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
C     Incorporated pesticide application method 2
      ELSEIF (CAM(K,NAPPC) .EQ. 5) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        DMAX = DEPI(K,NAPPC)
        BASE=2./DMAX
        SLOPE=(-BASE/DMAX)
C
        IF(DEPI(K,NAPPC).EQ.0.0)THEN
          SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
C     Incorporated pesticide application method 3
      ELSEIF (CAM(K,NAPPC) .EQ. 6) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        DMAX = DEPI(K,NAPPC)
        BASE=2./DMAX
        SLOPE=(-BASE/DMAX)
C
        IF(DEPI(K,NAPPC).EQ.0.0)THEN
          SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
      ELSEIF (CAM(K,NAPPC) .EQ. 7) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        DMAX = DEPI(K,NAPPC)
C
        BASE=0.
        SLOPE=0.
        IF(DEPI(K,NAPPC).EQ.0.0)THEN
          SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
      ELSEIF (CAM(K,NAPPC) .EQ. 8) THEN
        PLNTAP(K)= 0.
        APPAMT = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        DMAX = DEPI(K,NAPPC)
        BASE=0.
        SLOPE=0.
C
        IF(DEPI(K,NAPPC).EQ.0.0)THEN
          SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
          CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
        ENDIF
      ELSEIF (CAM(K,NAPPC) .EQ. 9) THEN
        IF (DELX(1) .GE. 2.0) THEN
          PLNTAP(K)    = COVER * TAPP(K,NAPPC) * APPEFF(K,NAPPC)
          SOILAP(K,1)  = (1.0- COVER) * TAPP(K,NAPPC)*APPEFF(K,NAPPC)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
          PLNTAP(K)    = COVER * TAPP(K,NAPPC) * APPEFF(K,NAPPC)
          APPAMT       = (1.0- COVER) * TAPP(K,NAPPC)*APPEFF(K,NAPPC)
C
C         Solve for base of isosceles triangle given:
C         length of 1 leg and area = 1.0
          IF(DEPI(K,NAPPC).GT.0.0)THEN
             DMAX = DEPI(K,NAPPC)
          ELSE
             DMAX = 4.0
          ENDIF
          BASE=2./DMAX
          SLOPE=(-BASE/DMAX)
C
          IF(DEPI(K,NAPPC).EQ.0.0)THEN
            SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
            PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
            SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                     +(THETAS(1)-THETO(1))*KH(K,1))
          ELSE
            CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
          ENDIF
        ENDIF
C
        FOLPST(K)    = FOLPST(K)+ PLNTAP(K)
        IFSCND(K,NCROP)= 0
C
C
C     Exponential foliar pesticide application
      ELSEIF (CAM(K,NAPPC) .EQ. 10) THEN
        IF (DELX(1) .GE. 2.0) THEN
          PLNTAP(K)    = (1.0-REAL(EXPCHK(DBLE(-FILTRA*WEIGHT)))) *
     1                   (TAPP(K,NAPPC)*APPEFF(K,NAPPC))
          SOILAP(K,1)  = (TAPP(K,NAPPC)*APPEFF(K,NAPPC))- PLNTAP(K)
          PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
          SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     *                   +(THETAS(1)-THETO(1))*KH(K,1))
        ELSE
          PLNTAP(K)=(1.0-REAL(EXPCHK(DBLE(-FILTRA*WEIGHT))))
     *              *(TAPP(K,NAPPC)*APPEFF(K,NAPPC))
          APPAMT  = (TAPP(K,NAPPC)*APPEFF(K,NAPPC))- PLNTAP(K)
C
C         Solve for base of isosceles triangle given:
C         length of 1 leg and area = 1.0
          IF(DEPI(K,NAPPC).GT.0.0)THEN
             DMAX = DEPI(K,NAPPC)
          ELSE
             DMAX = 4.0
          ENDIF
          BASE=2./DMAX
          SLOPE=(-BASE/DMAX)
C
          IF(DEPI(K,NAPPC).EQ.0.0)THEN
            SOILAP(K,1)  = TAPP(K,NAPPC)*APPEFF(K,NAPPC)
            PESTR(K,1)   = PESTR(K,1)+ SOILAP(K,1)/(DELX(1)*THETO(1))
            SPESTR(K,1)  = PESTR(K,1)*THETO(1)/(THETO(1)+KD(K,1)*BD(1)
     1                   +(THETAS(1)-THETO(1))*KH(K,1))
          ELSE
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
          ENDIF
        ENDIF
        FOLPST(K)    = FOLPST(K)+ PLNTAP(K)
        IFSCND(K,NCROP)= 0
C
C
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE PLPEST (K)
C
C     + + + PURPOSE + + +
C
C     Determines amount of pesticide which disappears
C     from plant surface by first order decay.  The variable PLDKRT
C     is a pseudo first order decay rate which may include processes
C     of volatilization, oxidation, photolysis, etc.
C     also determines pesticide washed off during rainfall events.
C     Modification date: 2/18/92
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER   K
C
C     + + + ARGUMENTS DEFINITIONS + + +
C
C     K   -  pesticide index number
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'

!*****************************************************************************
      INCLUDE 'CIRGT.INC'  ! added by dfy to transfer really_not_thrufl*******
!*****************************************************************************
C
C     + + + LOCAL VARIABLES + + +
C
      REAL         WFRC(NCMPTS)
      REAL         APPAMT,DMAX,SLOPE,BASE,WFRCTT,FOLP1
      REAL         TERM,TERM1,TERM2,TERM3,TERM4,TERM5,
     *             FPWLOS,ALIMIT,
     *             PFRC1,PFRC2,PFRC3,PFRC4,PFRC5
      CHARACTER*80 MESAGE
      REAL*8       EXPCHK
      INTEGER      I
C
C     + + + INTRINSICS + + +
C
      INTRINSIC REAL,DBLE
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,EXPCHK,SUBOUT
C
C     + + + DATA STATEMENTS + + +
C
      DATA ALIMIT /1.0E-30/
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'PLPEST'
      CALL SUBIN(MESAGE)
C
      IF (IFSCND(K,NCROP) .GE. 4) THEN
C
C     Signal to bypass this routine
C
      ELSE IF (IFSCND(K,NCROP) .EQ. 0 .OR. IFSCND(K,NCROP) .EQ. 3) THEN
C
C       Before harvest or
C       after harvest under surface-residue condition
C
cjmc 1       TERM   = REAL(EXPCHK(DBLE(-(FEXTRC(K)*PRECIP))))
cjmc 2       IF (THRUFL .LE. 0.0) TERM= 1.0
cjmc 3       TERM1    = REAL(EXPCHK(DBLE(-PLDKRT(K)*DELT)))
cjmc 4       TERM2    = REAL(EXPCHK(DBLE(-PLVKRT(K)*DELT)))
cjmc 5       FOLP0(K) = FOLPST(K)
cjmc 6       FPWLOS   = FOLP0(K)*(1.0-TERM)
cjmc 7       FPDLOS(K)= FOLP0(K)*(1.0-TERM1)
cjmc 8       FPVLOS(K)= FOLP0(K)*(1.0-TERM2)
cjmc 9       FOLPST(K)= FOLP0(K) -FPDLOS(K) -FPWLOS -FPVLOS(K)
cjmc    the following changes were made to folp0 to correct for mass
cjmc    balance errors caused by double counting.
cjmc    following code added after line 6
cjmc    mass from washoff removed before degradation
cjmc    FOLP0(K) = FOLPST(K)-FPWLOS line added after 6
cjmc    to prevent combined degradation from being > 100%
cjmc    the following code was added
cjmc    IF((TERM1+TERM2).LE.1.)THEN
cjmc      PFRC1=(1-TERM1)/((1-TERM1)+(1-TERM2)
cjmc      PFRC2=(1-TERM2)/((1-TERM1)+(1-TERM2)
cjmc    ELSE
cjmc      PFRC1=1.
cjmc      PFRC2=1.
cjmc    ENDIF
cjmc    lines 7&8 changed to
cjmc    FPDLOS(K)= PFRC1*(FOLP0(K)*(1.0-TERM1))
cjmc    FPVLOS(K)= PFRC2*(FOLP0(K)*(1.0-TERM2))
cjmc    line 9 FOLP0(K) changed to FOLPST(K)
cjmc    FOLPST(K)= FOLPST(K) -FPDLOS(K) -FPWLOS -FPVLOS(K)
cjmc
        TERM   = REAL(EXPCHK(DBLE(-(FEXTRC(K)*PRECIP))))
        IF (THRUFL .LE. 0.0) TERM= 1.0

!**********************************************************************************
!***********************************************************************************
! line added by dfy, so that undercanopy irrigation (IRTYP =4) would not cause
! washoff of pesticide. In IRTYPE 4, irrigation water is included into the
! variable THRUFL in subroutine IRRIG. "really_not_thrufl" also added to common in cirgt.inc
        if (really_not_thrufl) term = 1.0
!***********************************************************************************
!********************************************************************************

        FOLP0(K) = FOLPST(K)
        FPWLOS   = FOLP0(K)*(1.0-TERM)
        FOLP1    = FOLPST(K)-FPWLOS
C
        ! PLDKRT: pesticide decay rate constant on plant foliage (days^-1).
        ! PLVKRT: pesticide volatilization decay rate constant on plant foliage (days^-1)
        IF(NCHEM.EQ.1)THEN
          TERM1    = REAL(EXPCHK(DBLE(-PLDKRT(K)*DELT)))
          TERM2    = REAL(EXPCHK(DBLE(-PLVKRT(K)*DELT)))
          IF(((1-TERM1)+(1-TERM2)).GE.1.)THEN
            PFRC1=(1.-TERM1)/((1.-TERM1)+(1.-TERM2))
            PFRC2=(1.-TERM2)/((1.-TERM1)+(1.-TERM2))
          ELSE
            PFRC1=1.
            PFRC2=1.
          ENDIF
        ELSEIF(NCHEM.GT.1)THEN
          TERM1    = REAL(EXPCHK(DBLE(-PLDKRT(K)*DELT)))
          TERM2    = REAL(EXPCHK(DBLE(-PLVKRT(K)*DELT)))
          TERM3    = REAL(EXPCHK(DBLE(-PTRN12*DELT)))
          TERM4    = REAL(EXPCHK(DBLE(-PTRN13*DELT)))
          TERM5    = REAL(EXPCHK(DBLE(-PTRN23*DELT)))
          IF(K.EQ.1)THEN
            IF(((1-TERM1)+(1-TERM2)+(1-TERM3)+(1-TERM4)).GE.1.)THEN
              PFRC1=(1.-TERM1)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM3)+(1.-TERM4))
              PFRC2=(1.-TERM2)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM3)+(1.-TERM4))
              PFRC3=(1.-TERM3)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM3)+(1.-TERM4))
              PFRC4=(1.-TERM4)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM3)+(1.-TERM4))
            ELSE
              PFRC1=1.
              PFRC2=1.
              PFRC3=1.
              PFRC4=1.
            ENDIF
            FPLOS12= PFRC3*(FOLP1*(1.0-TERM3))
            FPLOS13= PFRC4*(FOLP1*(1.0-TERM4))
          ELSEIF(K.EQ.2)THEN
            IF(((1-TERM1)+(1-TERM2)+(1-TERM5)).GE.1.)THEN
              PFRC1=(1.-TERM1)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM5))
              PFRC2=(1.-TERM2)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM5))
              PFRC5=(1.-TERM5)/((1.-TERM1)+(1.-TERM2)+
     *              (1.-TERM5))
            ELSE
              PFRC1=1.
              PFRC2=1.
              PFRC5=1.
            ENDIF
            FPLOS23= PFRC5*(FOLP1*(1.0-TERM5))
          ENDIF
        ENDIF
C
        ! FPDLOS: Current Daily Foliar	Pesticide Decay Loss	(g cm^-2)
        ! FPVLOS: Daily Foliage Pesticide	Volatilization Flux(g cm^-2)
        FPDLOS(K)= PFRC1*(FOLP1*(1.0-TERM1))
        FPVLOS(K)= PFRC2*(FOLP1*(1.0-TERM2))
C
        IF(NCHEM.EQ.1)THEN
          FOLPST(K)=FOLPST(K)-FPDLOS(K)-FPWLOS-FPVLOS(K)
        ELSEIF(NCHEM.GT.1)THEN
          IF(K.EQ.1)THEN
            FOLPST(K)=FOLPST(K)-FPDLOS(K)-FPWLOS-FPVLOS(K)-
     *                FPLOS12-FPLOS13
          ELSEIF(K.EQ.2)THEN
            FOLPST(K)=FOLPST(K)+FPLOS12-FPDLOS(K)-FPWLOS-
     *                FPVLOS(K)-FPLOS23
          ELSEIF(K.EQ.3)THEN
            FOLPST(K)=FOLPST(K)+FPLOS13+FPLOS23-FPDLOS(K)-
     *                FPWLOS-FPVLOS(K)
          ENDIF
        ENDIF
C
C
C       Check for underflow
C
        IF(FOLPST(K).LE.ALIMIT) FOLPST(K)=0.0
        DO 24 I=1,RNCMPT
          WTERM(K,I) = 0.0
  24    CONTINUE
cjmc   determine percent of pesticide washoff mass applied to each
cjmc   compartment in runoff zone.  Previously all mass applied to
cjmc   top compartment.
cjmc   IF (THRUFL .GT. 0.0) WTERM(K) = FPWLOS
cjmc   WTERM now is dimensioned by WTERM(CHEM,NCOM2)
        WFRCTT=0.0
        IF (THRUFL .GT. 0.0) THEN
          DO 26 I=1,RNCMPT
             WFRC(I)=(THETAS(I)-THETO(I))*DELX(I)
             WFRCTT=WFRCTT+WFRC(I)
  26      CONTINUE
          DO 27 I=1,RNCMPT
             WTERM(K,I) = (WFRC(I)/WFRCTT)*FPWLOS
  27      CONTINUE
        ENDIF
      ELSE IF (IFSCND(K,NCROP) .EQ. 1) THEN
C       Solve for base of isosceles triangle given:
C       length of 1 leg and area = 1.0
        CRPAPP(K)=1
        IF(DEPI(K,NAPPC).GT.0.0)THEN
           DMAX = DEPI(K,NAPPC)
        ELSE
           DMAX = 2.0
        ENDIF
        BASE=2./DMAX
        SLOPE=(-BASE/DMAX)
        APPAMT=FOLPST(K)
C
        CALL PDSTRB(APPAMT,DMAX,BASE,SLOPE,K)
C
        SOILAP(K,1)= FOLPST(K)
        IFSCND(K,NCROP) = 4
        FPVLOS(K)  = 0.0
        FPDLOS(K)  = 0.0
        FOLPST(K)  = 0.0
        FOLP0(K)   = 0.0
        DO 28 I=1,RNCMPT
          WTERM(K,I) = 0.0
  28    CONTINUE
      ELSE IF (IFSCND(K,NCROP) .EQ. 2) THEN
C
C       After harvest remove all pesticide from canopy
C
        FMRMVL(K) = FOLPST(K)
        IFSCND(K,NCROP) = 4
        FPVLOS(K) = 0.0
        FPDLOS(K) = 0.0
        FOLPST(K) = 0.0
        FOLP0(K)  = 0.0
        DO 29 I=1,RNCMPT
          WTERM(K,I) = 0.0
  29    CONTINUE
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END SUBROUTINE PLPEST
C
C
C
C
C
C
      SUBROUTINE SLPST0(
     I  LPRZOT, MODID, K, DKBIO)
C
C     + + + PURPOSE + + +
C
C     Sets up the coefficient matrix for the solution of the soil
C     pesticide transport equation. It then calls an equation
C     solver for the tridiagonal matrix and sets up pesticide
C     flux terms using the new concentrations.
C     Modification date: 2/18/92 JAM
C     Further modified at AQUA TERRA Consultants to hard code the
C     pesticide extraction depth to 1 cm. 9/93
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER     K,LPRZOT
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     LPRZOT - Fortran unit number for output file LPRZOT
C     MODID  - character string for output file identification
C     K      - chemical number being simulated (1-3)
C     DKBIO  - array containing rate of biodegradation
C     PRDPTH - runoff pesticide extraction depth
C     PFRAC  - pesticide to be distributed in the remaining depth
C              fraction
C     CMPT   - number of compartments which make up the pesticide
C              runoff extraction depth
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CACCUM.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER      I,J,KLIN,CMPT
      REAL         RTRWT,RTRST
      REAL         SRCWT,SRCST
      REAL         THAIR(NCMPTS),DGAIR(NCMPTS)
      REAL         VTERM,DDLN
      REAL*8       DKBIO(3,NCMPTS)
      CHARACTER*80 MESAGE
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,PSTLNK,TRDIAG,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'SLPST0'
      CALL SUBIN(MESAGE)
C
      DO 10 J=1,NCOM2
        SRCFLX(1,J)=0.0
        THAIR(J)=THETAS(J)-THETN(J)
        IF (THAIR(J) .LT. 0.0) THAIR(J) = 0.0
C       DGAIR now includes correction for air to bulk volume
        DGAIR(J)=(THAIR(J)**(10./3)/THETAS(J)**2)*DAIR(K) * THAIR(J)
10    CONTINUE
C
C     Set up coefficients for surface layer
      ! Set up tridiagonal system
      ! a(i) y(i-1)  +  b(i) y(i)  +  c(i) y(i+1) = f(i)
      ! a(1) = c(n) = 0
C
      J=1
C
      A(1)= 0.0
      B(1)= ((DISP(K,1)*THETN(1)+KH(K,1)*DGAIR(1))/(DELX(1)*
     1       DELX(1))
     1       +VEL(1)*THETN(1)/DELX(1)
     2       +(DWRATE(K,1)*THETN(1))+(DSRATE(K,1)*KD(K,1)*BD(1))
     3       +(DKBIO(K,1)*(THETN(1)+KD(K,1)*BD(1)))
     4       +(DGRATE(K,1)*THAIR(1)*KH(K,1))
     5       +ELTERM(K)) *FLOAT(DELT)
     6       +THETN(1) + KD(K,1)*BD(1) + THAIR(1)*KH(K,1)
     7       +CONDUC(K)*KH(K,1)*FLOAT(DELT)/DELX(1)
C
C     Add runoff term based on the number of compartments which
C     make up 1 cm depth.
C
      IF (RNCMPT .EQ. 1) THEN
        B(1) = B(1) + ((RUNOF*DRI(1))/DELX(1))
      ELSE
        B(1) = B(1) + ((RUNOF*DRI(1))/PRDPTH)
      ENDIF
C
      C(1)= -(DISP(K,2)*THETN(2)+KH(K,1)*DGAIR(2))*DELT/(DELX(1)*
     1       0.5*(DELX(1)+DELX(2)))
      F(1)= (THETO(1)+KD(K,1)*BD(1)
     *      +(THETAS(1)-THETO(1))*OKH(K,1))*SPESTR(K,1)
     *      +(WTERM(K,1)*DELT/DELX(1))
     *      +SRCFLX(K,1)/DELX(1)*DELT
C
C     Calculate coefficient of non-boundary soil layers
C
      DO 20 I=2,NCOM2M
        A(I)= (-(DISP(K,I-1)*THETN(I-1)+KH(K,I-1)*DGAIR(I-1))
     1          /(DELX(I)*0.5*(DELX(I-1)+DELX(I)))
     2          -VEL(I-1)*THETN(I-1)/DELX(I)) *DELT
        B(I)= ((DISP(K,I)*THETN(I)+KH(K,I)*DGAIR(I))
     1          /(DELX(I)*0.5*(DELX(I-1)+DELX(I)))
     2        + (DISP(K,I)*THETN(I)+KH(K,I)*DGAIR(I))
     3          /(DELX(I)*0.5*(DELX(I)+DELX(I+1)))
     4          +VEL(I)*THETN(I)/DELX(I)
     5          +(DWRATE(K,I)*THETN(I))+(DSRATE(K,I)*KD(K,I)*BD(I))
     6          +(DKBIO(K,I)*(THETN(I)+KD(K,I)*BD(I)))
     +          + (DGRATE(K,I)*THAIR(I)*KH(K,I))
     7          +GAMMA(K,I)*ET(I)*THETN(I)/SW(I)) *DELT
     8          +THETN(I)+KD(K,I)*BD(I)+THAIR(I)*KH(K,I)
C
C       Add runoff term if current compartment number is less than or
C       equal to the number of compartments which make up 1 cm depth.
C
        IF (I .LT. RNCMPT) THEN
          B(I) = B(I) + ((RUNOF*DRI(I))/PRDPTH)
        ELSE
          IF (I .EQ. RNCMPT)THEN
             B(I) = B(I) + ((RUNOF*DRI(I))/DELX(I))*(PFRAC/PRDPTH)
          ENDIF
        ENDIF
C
        C(I)= -(DISP(K,I+1)*THETN(I+1)+KH(K,I+1)*DGAIR(I+1))
     1         *DELT/(DELX(I)*0.5*(DELX(I)+DELX(I+1)))
        F(I)=  (THETO(I)+KD(K,I)*BD(I)
     *        +(THETAS(I)-THETO(I))*OKH(K,I))*SPESTR(K,I)
     *        +(WTERM(K,I)*DELT/DELX(I))
     *        +SRCFLX(K,I)/DELX(I)*DELT
C
20    CONTINUE
C
C     Calculate coefficients of bottom layer
C
C
      VTERM   = VEL(NCOM2) * THETN(NCOM2) / DELX(NCOM2)
C
      A(NCOM2)=(-(DISP(K,NCOM2M)*THETN(NCOM2M)
     1         +KH(K,NCOM2M)*DGAIR(NCOM2M))
     2         /(DELX(NCOM2)*0.5*(DELX(NCOM2M)+DELX(NCOM2)))
     3         -VEL(NCOM2M)*THETN(NCOM2M)/DELX(NCOM2))*DELT
      B(NCOM2)= ((DISP(K,NCOM2)*THETN(NCOM2)
     1         +KH(K,NCOM2)*DGAIR(NCOM2))/(DELX(NCOM2)*DELX(NCOM2))
     2         + VTERM
     3         +(DWRATE(K,NCOM2)*THETN(NCOM2))
     4         +(DKBIO(K,NCOM2)*(THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)))
     5         +(DSRATE(K,NCOM2)*KD(K,NCOM2)*BD(NCOM2))
     6         +DGRATE(K,NCOM2)*THAIR(NCOM2)*KH(K,NCOM2))*DELT
     7         +THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)
     8         +THAIR(NCOM2)*KH(K,NCOM2)
C
      C(NCOM2)= 0.0
      F(NCOM2)= (THETO(NCOM2)+KD(K,NCOM2)*BD(NCOM2)+(THETAS(NCOM2)-
     1           THETO(NCOM2))*OKH(K,NCOM2))*SPESTR(K,NCOM2)
     *          +(WTERM(K,NCOM2)*DELT/DELX(NCOM2))
     *          +SRCFLX(K,NCOM2)/DELX(NCOM2)*DELT
C
C     Call equation solver
C
      CALL TRDIAG (A,B,C,X,F,NCOM2,LPRZOT,MODID)
C
C     Calculate pesticide fluxes
C
      ! PVFLUX: Daily Soil Pesticide Volatilization Flux (g cm^-2 day^-1)
      PVFLUX(K,1) = -CONDUC(K)*X(1)*KH(K,1)
      IF(ABS(PVFLUX(K,1)).LT.1.E-34)PVFLUX(K,1)=0.0
      DFFLUX(K,1)=DISP(K,1)/(0.5*(DELX(1)+DELX(2)))*X(1)*THETN(1)
     1           -DISP(K,2)/(0.5*(DELX(1)+DELX(2)))*X(2)*THETN(2)
      ADFLUX(K,1)=VEL(1)*X(1)*THETN(1)
      LTFLUX(K,1)=0.0
      DKFLUX(K,1)=DELX(1)*X(1)*(DWRATE(K,1)*THETN(1)+DSRATE(K,1)
     1            *BD(1)*KD(K,1)+DGRATE(K,1)*THAIR(1)*KH(K,1)
     2            +DKBIO(K,1)*(THETN(1)+KD(K,1)*BD(1)))
      if(k.eq.1)then
        trflux(1,1)=(dkrw12(1)+dkrw13(1))*dkflux(1,1)
        srcflx(1,1)=0.0
        srcflx(2,1)=dkrw12(1)*dkflux(1,1)
        srcflx(3,1)=dkrw13(1)*dkflux(1,1)
        dkflux(1,1)=dkflux(1,1)-trflux(1,1)
      elseif(k.eq.2)then
        trflux(2,1)=dkrw23(1)*dkflux(2,1)
        srcflx(3,1)=srcflx(3,1)+trflux(2,1)
        dkflux(2,1)=dkflux(2,1)-trflux(2,1)
      endif
C
      IF (RNCMPT .EQ. 1) THEN
        RFFLUX(K,1) =RUNOF*DRI(1)*X(1)
      ELSE
        RFFLUX(K,1) =RUNOF*X(1)*DRI(1)*(DELX(1)/PRDPTH)
      ENDIF
      ERFLUX(K)   =ELTERM(K)*DELX(1)*X(1)
C
      DO 30 I=2,NCOM2M
        RFFLUX(K,I) = 0.0
        IF (I .LT. RNCMPT) THEN
          RFFLUX(K,I)=RUNOF*DRI(I)*X(I)*(DELX(I)/PRDPTH)
        ELSE
          IF (I.EQ.RNCMPT) RFFLUX(K,I)=RUNOF*DRI(I)*X(I)*(PFRAC/PRDPTH)
        ENDIF
        PVFLUX(K,I)=DGAIR(I)*KH(K,I)/(0.5*(DELX(I)+DELX(I+1)))*X(I)-
     1         DGAIR(I+1)*KH(K,I+1)/(0.5*(DELX(I)+DELX(I+1)))*X(I+1)
        IF(ABS(PVFLUX(K,I)).LT.1.E-34)PVFLUX(K,I)=0.0
        DFFLUX(K,I)=DISP(K,I)/(0.5*(DELX(I)+DELX(I+1)))*THETN(I)*X(I)-
     1         DISP(K,I+1)/(0.5*(DELX(I)+DELX(I+1)))*THETN(I+1)*X(I+1)
        ADFLUX(K,I)=VEL(I)*X(I)*THETN(I)
        LTFLUX(K,I)=OUTFLO(I)*X(I)
        DKFLUX(K,I)=DELX(I)*X(I)*(DWRATE(K,I)*THETN(I)+DSRATE(K,I)
     1             *BD(I)*KD(K,I)+DGRATE(K,I)*THAIR(I)*KH(K,I)
     2             +DKBIO(K,I)*(THETN(I)+KD(K,I)*BD(I)))
        UPFLUX(K,I)=GAMMA(K,I)*ET(I)*X(I)
      if(k.eq.1)then
        trflux(1,i)=(dkrw12(i)+dkrw13(i))*dkflux(1,i)
        srcflx(1,i)=0.0
        srcflx(2,i)=dkrw12(i)*dkflux(1,i)
        srcflx(3,i)=dkrw13(i)*dkflux(1,i)
        dkflux(1,i)=dkflux(1,i)-trflux(1,i)
      elseif(k.eq.2)then
        trflux(2,i)=dkrw23(i)*dkflux(2,i)
        srcflx(3,i)=srcflx(3,i)+trflux(2,i)
        dkflux(2,i)=dkflux(2,i)-trflux(2,i)
      endif
30    CONTINUE
C
      RZFLUX(K)= DISP(K,NCOMRZ)/(0.5*(DELX(NCOMRZ)+DELX(NCOMRZ+1)))
     1  *THETN(NCOMRZ)*X(NCOMRZ)-DISP(K,NCOMRZ+1)/(0.5*(DELX(NCOMRZ+1)
     2  +DELX(NCOMRZ)))*THETN(NCOMRZ+1)*X(NCOMRZ+1)
     3  +(VEL(NCOMRZ)*X(NCOMRZ)*THETN(NCOMRZ))
      RFFLUX(K,NCOM2)=0.
      DFFLUX(K,NCOM2)=0.
      PVFLUX(K,NCOM2)=0.
      UPFLUX(K,NCOM2)=0.
      ADFLUX(K,NCOM2) = VTERM * DELX(NCOM2) * X(NCOM2)
      LTFLUX(K,NCOM2)=OUTFLO(NCOM2)*X(NCOM2)
      DKFLUX(K,NCOM2)=DELX(NCOM2)*X(NCOM2)*(DWRATE(K,NCOM2)
     1            *THETN(NCOM2)+DSRATE(K,NCOM2)*BD(NCOM2)*KD(K,NCOM2)
     2            +DGRATE(K,NCOM2)*THAIR(NCOM2)*KH(K,NCOM2)
     3            +DKBIO(K,NCOM2)*(THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)))
      if(k.eq.1)then
        trflux(1,ncom2)=(dkrw12(ncom2)+dkrw13(ncom2))*dkflux(1,ncom2)
        srcflx(1,ncom2)=0.0
        srcflx(2,ncom2)=dkrw12(ncom2)*dkflux(1,ncom2)
        srcflx(3,ncom2)=dkrw13(ncom2)*dkflux(1,ncom2)
        dkflux(1,ncom2)=dkflux(1,ncom2)-trflux(1,ncom2)
      elseif(k.eq.2)then
        trflux(2,ncom2)=dkrw23(ncom2)*dkflux(2,ncom2)
        srcflx(3,ncom2)=srcflx(3,ncom2)+trflux(2,ncom2)
        dkflux(2,ncom2)=dkflux(2,ncom2)-trflux(2,ncom2)
      endif
C
C     Calculate core flux values.
C     Multiply internal units of GR/CM**2 by 10**5 so output
C     is expressed in units of KG/HA (as in the input).
C
      DCOFLX(K) = DISP(K,NCOM2)/DELX(NCOM2)*THETN(NCOM2)*X(NCOM2)
     1          - DISP(K,NCOM2)/DELX(NCOM2)*THETN(NCOM2)*X(NCOM2)
     2          + (VEL(NCOM2)*X(NCOM2)*THETN(NCOM2))
      DCOFLX(K) = DCOFLX(K) * 1.0E5
      MCOFLX(K) = MCOFLX(K) + DCOFLX(K)
      YCOFLX(K) = YCOFLX(K) + DCOFLX(K)
C
C     Accumulate fluxes from soil layers for output
C
      WOFLUX(K)= 0.0
      ROFLUX(K)= 0.0
      SUPFLX(K)= 0.0
      SDKFLX(K)= 0.0
      TTRFLX(K)= 0.0
      TSRCFX(K)= 0.0
      LATFLX(K)=0.0
      DO 40 I=1,NCOM2
         WOFLUX(K)= WOFLUX(K)+WTERM(K,I)
         ROFLUX(K)= ROFLUX(K)+RFFLUX(K,I)
         SDKFLX(K)= SDKFLX(K)+DKFLUX(K,I)
         SUPFLX(K)= SUPFLX(K)+UPFLUX(K,I)
         TTRFLX(K)= TTRFLX(K)+TRFLUX(K,I)
         TSRCFX(K)= TSRCFX(K)+SRCFLX(K,I)
         LATFLX(K)= LATFLX(K)+LTFLUX(K,I)
40    CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE SLPST1 (LPRZOT,MODID,K,DKBIO)
C
C     + + + PURPOSE + + +
C
C     Sets up the coefficient matrix for the solution
C     of the soil pesticide transport equation. It then calls an equa-
C     tion solver for the tridiagonal matrix and sets up pesticide
C     flux terms using the new concentrations
C     Modification date: 2/18/92 JAM
C     Further modified at AQUA TERRA Consultants to hard code the
C     pesticide extraction depth to 1 cm. 9/93
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER     LPRZOT,K
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     LPRZOT - Fortran unit number for output file LPRZOT
C     MODID  - character string for output file identification
C     K      - chemical number being simulated (1-3)
C     DKBIO  - biodegradation rate
C     PRDPTH - runoff pesticide extraction depth
C     PFRAC  - pesticide to be distributed in the remaining depth
C              fraction
C     CMPT   - number of compartments which make up the pesticide
C              runoff extraction depth
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CACCUM.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER      I,KK,KLIN,CMPT,J
      REAL         THAIR(NCMPTS),DGAIR(NCMPTS)
      REAL         DDLN
      REAL*8       DKBIO(3,NCMPTS)
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,PSTLNK,TRDIAG,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'SLPST1'
      CALL SUBIN(MESAGE)
C
      DO 10 KK=1,NCOM2
        SRCFLX(1,KK)=0.0
        THAIR(KK)=THETAS(KK)-THETN(KK)
        IF (THAIR(KK).LT.0.0) THAIR(KK) = 0.0
        DGAIR(KK)=(THAIR(KK)**(10./3)/THETAS(KK)**2)*DAIR(K)* THAIR(KK)
10    CONTINUE
C
      J=1
C
C     Set up coefficients for surface layer
C
      A(1)= 0.0
      B(1)= ((DISP(K,1)*THETN(1)+KH(K,1)*DGAIR(1))/(DELX(1)*
     1       DELX(1))
     2       +(DWRATE(K,1)*THETN(1))+(DSRATE(K,1)*KD(K,1)*BD(1))
     3       +(DKBIO(K,1)*(THETN(1)+KD(K,1)*BD(1)))
     4       +(DGRATE(K,1)*THAIR(1)*KH(K,1))
     5       +ELTERM(K)) *DELT
     6       +THETN(1) + KD(K,1)*BD(1) + THAIR(1)*KH(K,1)
     7       +CONDUC(K)*KH(K,1)*DELT/DELX(1)
C
      IF (RNCMPT .EQ. 1) THEN
        B(1) = B(1) + ((RUNOF*DRI(1))/DELX(1))
cjmc        B(1) = B(1) + (RUNOF/DELX(1))
      ELSE
        B(1) = B(1) + ((RUNOF*DRI(1))/PRDPTH)
cjmc        B(1) = B(1) + (RUNOF/PRDPTH)
      ENDIF
C
      C(1)= -(DISP(K,2)*THETN(2)+KH(K,1)*DGAIR(2))*DELT/(DELX(1)*
     1       0.5*(DELX(1)+DELX(2)))
      F(1)=  (THETO(1)+KD(K,1)*BD(1)
     *      +(THETAS(1)-THETO(1))*OKH(K,1))*SPESTR(K,1)
     *      +(WTERM(K,1)*DELT/DELX(1))
     *      +SRCFLX(K,1)/DELX(1)*DELT
Cjmc wterm now dimensioned by nchem,ncom2
cjmc     1      *SPESTR(K,1)+WTERM(K)*DELT/DELX(1)
C
C     Calculate coefficient of non-boundary soil layers
C
      DO 20 I=2,NCOM2M
        A(I)= (-(DISP(K,I-1)*THETN(I-1)+KH(K,I-1)*DGAIR(I-1))
     1          /(DELX(I)*0.5*(DELX(I-1)+DELX(I)))
     2          )*DELT
        B(I)= ((DISP(K,I)*THETN(I)+KH(K,I)*DGAIR(I))
     1          /(DELX(I)*0.5*(DELX(I-1)+DELX(I)))
     1        + (DISP(K,I)*THETN(I)+KH(K,I)*DGAIR(I))
     1          /(DELX(I)*0.5*(DELX(I)+DELX(I+1)))
     2          +(DWRATE(K,I)*THETN(I))+(DSRATE(K,I)*KD(K,I)*BD(I))
     3          +(DKBIO(K,I)*(THETN(I)+KD(K,I)*BD(I)))
     1          +(DGRATE(K,I)*THAIR(I)*KH(K,I))
     4          +GAMMA(K,I)*ET(I)*THETN(I)/SW(I)) *DELT
     5          +THETN(I)+KD(K,I)*BD(I)+THAIR(I)*KH(K,I)
C
C       Add runoff term if current compartment number is less than or
C       equal to the number of compartments which make up 1 cm depth.
C
        IF (I .LT. RNCMPT) THEN
          B(I) = B(I) + ((RUNOF*DRI(I))/PRDPTH)
cjmc          B(I) = B(I) + (RUNOF/PRDPTH)
        ELSE
          IF (I .EQ. RNCMPT)THEN
             B(I) = B(I) + ((RUNOF*DRI(I))/DELX(I))*(PFRAC/PRDPTH)
cjmc             B(I) = B(I) + (RUNOF/DELX(I))*(PFRAC/PRDPTH)
          ENDIF
        ENDIF
C
        C(I)= -(DISP(K,I+1)*THETN(I+1)+KH(K,I+1)*DGAIR(I+1))
     1         *DELT/(DELX(I)*0.5*(DELX(I)+DELX(I+1)))
        F(I)=  (THETO(I)+KD(K,I)*BD(I)
     *        +(THETAS(I)-THETO(I))*OKH(K,I))*SPESTR(K,I)
     *        +(WTERM(K,I)*DELT/DELX(I))
     *        +SRCFLX(K,I)/DELX(I)*DELT
20    CONTINUE
C
C     Calculate coefficients of bottom layer
C
      A(NCOM2)=(-(DISP(K,NCOM2M)*THETN(NCOM2M)+KH(K,NCOM2M)
     1         *DGAIR(NCOM2M))/(DELX(NCOM2)*0.5*
     2         (DELX(NCOM2M)+DELX(NCOM2))))*DELT
      B(NCOM2)= ((DISP(K,NCOM2)*THETN(NCOM2)+KH(K,NCOM2)*DGAIR(NCOM2))
     1         /(DELX(NCOM2)*DELX(NCOM2))
     2         +(DWRATE(K,NCOM2)*THETN(NCOM2))
     3         +(DKBIO(K,NCOM2)*(THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)))
     1         +(DSRATE(K,NCOM2)*KD(K,NCOM2)*BD(NCOM2))
     1         +DGRATE(K,NCOM2)*THAIR(NCOM2)*KH(K,NCOM2))*DELT
     1         +THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)
     6         +THAIR(NCOM2)*KH(K,NCOM2)
      C(NCOM2)= 0.0
      F(NCOM2)= (THETO(NCOM2)+KD(K,NCOM2)*BD(NCOM2)+(THETAS(NCOM2)-
     1           THETO(NCOM2))*OKH(K,NCOM2))*SPESTR(K,NCOM2)
     *          +(WTERM(K,NCOM2)*DELT/DELX(NCOM2))
     *          +SRCFLX(K,NCOM2)/DELX(NCOM2)*DELT
C
C     call solve equation
C
      CALL TRDIAG (A,B,C,X,F,NCOM2,LPRZOT,MODID)
C
C     Calculate pesticide fluxes
C
      PVFLUX(K,1)= -CONDUC(K)*X(1)*KH(K,1)
      UPFLUX(K,1)= 0.0
      DFFLUX(K,1)= DISP(K,1)/(0.5*(DELX(1)+DELX(2)))*X(1)*THETN(1)
     1            -DISP(K,2)/(0.5*(DELX(1)+DELX(2)))*X(2)*THETN(2)
      DKFLUX(K,1)= DELX(1)*X(1)*(DWRATE(K,1)*THETN(1)+DSRATE(K,1)
     1            *BD(1)*KD(K,1)+DGRATE(K,1)*THAIR(1)*KH(K,1)
     2            +DKBIO(K,1)*(THETN(1)+KD(K,1)*BD(1)))
      if(k.eq.1)then
        trflux(1,1)=(dkrw12(1)+dkrw13(1))*dkflux(1,1)
        srcflx(1,1)=0.0
        srcflx(2,1)=dkrw12(1)*dkflux(1,1)
        srcflx(3,1)=dkrw13(1)*dkflux(1,1)
        dkflux(1,1)=dkflux(1,1)-trflux(1,1)
      elseif(k.eq.2)then
        trflux(2,1)=dkrw23(1)*dkflux(2,1)
        srcflx(3,1)=srcflx(3,1)+trflux(2,1)
        dkflux(2,1)=dkflux(2,1)-trflux(2,1)
      endif
C
      IF (RNCMPT .EQ. 1) THEN
        RFFLUX(K,1) =RUNOF*DRI(1)*X(1)
      ELSE
        RFFLUX(K,1) =RUNOF*X(1)*DRI(1)*(DELX(1)/PRDPTH)
      ENDIF
      ERFLUX(K)  = ELTERM(K)*DELX(1)*X(1)
C
      DO 30 I=2,NCOM2M
        RFFLUX(K,I) = 0.0
        IF (I .LT. RNCMPT) THEN
          RFFLUX(K,I)=RUNOF*DRI(I)*X(I)*(DELX(I)/PRDPTH)
        ELSE
          IF (I.EQ.RNCMPT) RFFLUX(K,I)=RUNOF*DRI(I)*X(I)*(PFRAC/PRDPTH)
        ENDIF
        PVFLUX(K,I)=DGAIR(I)*KH(K,I)/(0.5*(DELX(I)+DELX(I+1)))*X(I)-
     1         DGAIR(I+1)*KH(K,I+1)/(0.5*(DELX(I)+DELX(I+1)))*X(I+1)
        DFFLUX(K,I)=DISP(K,I)/(0.5*(DELX(I)+DELX(I+1)))*THETN(I)*X(I)-
     1         DISP(K,I+1)/(0.5*(DELX(I)+DELX(I+1)))*THETN(I+1)*X(I+1)
        DKFLUX(K,I)=DELX(I)*X(I)*(DWRATE(K,I)*THETN(I)+DSRATE(K,I)
     1            *BD(I)*KD(K,I)+DGRATE(K,I)*THAIR(I)*KH(K,I)
     2            +DKBIO(K,I)*(THETN(I)+KD(K,I)*BD(I)))
        UPFLUX(K,I)=GAMMA(K,I)*ET(I)*X(I)
      if(k.eq.1)then
        trflux(1,i)=(dkrw12(i)+dkrw13(i))*dkflux(1,i)
        srcflx(1,i)=0.0
        srcflx(2,i)=dkrw12(i)*dkflux(1,i)
        srcflx(3,i)=dkrw13(i)*dkflux(1,i)
        dkflux(1,i)=dkflux(1,i)-trflux(1,i)
      elseif(k.eq.2)then
        trflux(2,i)=dkrw23(i)*dkflux(2,i)
        srcflx(3,i)=srcflx(3,i)+trflux(2,i)
        dkflux(2,i)=dkflux(2,i)-trflux(2,i)
      endif
30    CONTINUE
C
      RZFLUX(K)=DISP(K,NCOMRZ)/(0.5*(DELX(NCOMRZ)+DELX(NCOMRZ+1)))*
     1        THETN(NCOMRZ)*X(NCOMRZ)
     1  -DISP(K,NCOMRZ+1)/(0.5*(DELX(NCOMRZ+1)+DELX(NCOMRZ)))*
     1  THETN(NCOMRZ+1)*X(NCOMRZ+1)
     2  +(VEL(NCOMRZ)*X(NCOMRZ)*THETN(NCOMRZ))
      RFFLUX(K,NCOM2)=0.
      DFFLUX(K,NCOM2)=0.
      PVFLUX(K,NCOM2)=0.
      UPFLUX(K,NCOM2)=0.
      DKFLUX(K,NCOM2)=DELX(NCOM2)*X(NCOM2)*(DWRATE(K,NCOM2)*THETN(NCOM2)
     1           +DSRATE(K,NCOM2)*BD(NCOM2)*KD(K,NCOM2)
     2           +DGRATE(K,NCOM2)*THAIR(NCOM2)*KH(K,NCOM2)
     3           +DKBIO(K,NCOM2)*(THETN(NCOM2)+KD(K,NCOM2)*BD(NCOM2)))
      if(k.eq.1)then
        trflux(1,ncom2)=(dkrw12(ncom2)+dkrw13(ncom2))*dkflux(1,ncom2)
        srcflx(1,ncom2)=0.0
        srcflx(2,ncom2)=dkrw12(ncom2)*dkflux(1,ncom2)
        srcflx(3,ncom2)=dkrw13(ncom2)*dkflux(1,ncom2)
        dkflux(1,ncom2)=dkflux(1,ncom2)-trflux(1,ncom2)
      elseif(k.eq.2)then
        trflux(2,ncom2)=dkrw23(ncom2)*dkflux(2,ncom2)
        srcflx(3,ncom2)=srcflx(3,ncom2)+trflux(2,ncom2)
        dkflux(2,ncom2)=dkflux(2,ncom2)-trflux(2,ncom2)
      endif
C
C     Calculate core flux values.
C     Multiply internal units of GR/CM**2 by 10**5 so output
C     is expressed in units of KG/HA (as in the input).
C
      DCOFLX(K) = DISP(K,NCOM2)/DELX(NCOM2)*THETN(NCOM2)*X(NCOM2)
     1          - DISP(K,NCOM2)/DELX(NCOM2)*THETN(NCOM2)*X(NCOM2)
     2          + (VEL(NCOM2)*X(NCOM2)*THETN(NCOM2))
      DCOFLX(K) = DCOFLX(K) * 1.0E5
      MCOFLX(K) = MCOFLX(K) + DCOFLX(K)
      YCOFLX(K) = YCOFLX(K) + DCOFLX(K)
C
C     Accumulate fluxes from soil layers for output
C
      WOFLUX(K)= 0.0
      ROFLUX(K)= 0.0
      SUPFLX(K)= 0.0
      SDKFLX(K)= 0.0
      TTRFLX(K)= 0.0
      TSRCFX(K)= 0.0
      LATFLX(K)=0.0
C
      DO 40 I=1,NCOM2
         WOFLUX(K)= WOFLUX(K)+WTERM(K,I)
         ROFLUX(K)= ROFLUX(K)+RFFLUX(K,I)
         SDKFLX(K)= SDKFLX(K)+DKFLUX(K,I)
         SUPFLX(K)= SUPFLX(K)+UPFLUX(K,I)
         TTRFLX(K)= TTRFLX(K)+TRFLUX(K,I)
         TSRCFX(K)= TSRCFX(K)+SRCFLX(K,I)
40    CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE MOC(K)
C
C     + + + PURPOSE + + +
C
C     This subroutine solves the advection component of the soil
C     pesticide transport process.  SLPST1 is called next and uses
C     the advected concentrations to calculate the transport of
C     pesticide due to all other processes.  This algorithm is based
C     on one presented in Khaleel and Reddell (1986) in Groundwater
C     modified for use under variably saturated conditions, with
C     retardation and decay. To acomodate these changes the algorithm
C     operates on total pesticide mass in each call rather than conc.
C
C     This subroutine was added by Y.Meeks 4/87 to minimize numerical
C     dispersion in the solution of the transport equation.  To include
C     this subroutine, velocity calculations were deleted from SLPEST,
C     a call MOC1 toggle was added to the main program, and
C     initializations were added near the end of the subroutine
C     INITL.  See specific subroutines for more details.
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER  K
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     K   - chemical number being simulated (1-3)
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMISC.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL         CHANGE(NCMPTS),SUMC(NCMPTS),COUNT(NCMPTS),ZIN(250),
     1             TEND,TLEFT,MASS(NCMPTS),RVEL(NCMPTS),PTEMP(NCMPTS),
     2             NET(NCMPTS),DDLN,ZTOT,CTOT,ZCTOT,ZOLD,ZOLD1
      INTEGER      J,I,M,LL,NCELL,IOUT,NEW,ILIN,RTIOM1,IDEL,ICHECK,
     1             IFACE,FIRST,ISTART,IEND,MM,M3,NUMSUM
      CHARACTER*80 MESAGE
      INTEGER      IERROR
      LOGICAL      FATAL
      REAL         CCSUM
C
C     +  +  + INTRINSICS +  +  +
C
      INTRINSIC ABS,AMIN1,AMAX1,MIN0
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,ERRCHK,SUBOUT
C
C     + + + OUTPUT FORMATS + + +
C
 2090 FORMAT('NPI[',I4,'] + NEW[',I4,'] is greater than NPII[',I4,
     1       '] in subroutine MOC')
C
C     +  +  + END SPECIFICATIONS +  +  +
C
      MESAGE = 'MOC'
      CALL SUBIN(MESAGE)
C
C       Convert dissolved concentration to total mass in each cell
C
        DO 10  J=1,NCOM2
          PESTR(K,J)=SPESTR(K,J)*(THETO(J)+KD(K,J)*BD(J)+(THETAS(J)-
     1             THETO(J))*OKH(K,J))/THETO(J)
          MASS(J)=PESTR(K,J)*DELX(J)*THETO(J)
10      CONTINUE
C
C       Calculate the change in mass in each cell and increment each
C       point in the cell by the correct amount
C
        DO 20 J=1,NCOM2
          CHANGE(J)= MASS(J)-MASSO(K,J)
20      CONTINUE
C
C       Find out how many points are currently in each cell
C
        DO 30 J=1,NCOM2
          COUNT(J)=0.
          SUMC(J)=0.
30      CONTINUE
C
        DO 40 M=1,NPI(K)
          ILIN = 0
          DDLN = 0.0
33        ILIN = ILIN + 1
            DDLN = DDLN + DELX(ILIN)
            IF (Z(K,M) .GT. DDLN) GO TO 33
            NCELL = ILIN
          COUNT (NCELL) = COUNT(NCELL) + 1.0
40      CONTINUE
C
C       Increment the mass at each point. A positive change is added
C       equally to all points in the cell, and a negative vhange is
C       weighted by the actual mass at the point to avoid negative
C       mass values.
C
        DO 50 M=1,NPI(K)
          ILIN = 0
          DDLN = 0.0
43        ILIN = ILIN + 1
            DDLN = DDLN + DELX(ILIN)
            IF (Z(K,M) .GT. DDLN) GO TO 43
            NCELL = ILIN
          IF (ABS(COUNT(NCELL)-0.0).LT.1.0E-5)  COUNT(NCELL)=1.0
          IF (CHANGE(NCELL).GE.0.0) THEN
            CC(K,M) = CC(K,M)  + CHANGE(NCELL)/COUNT(NCELL)
          ELSE
            IF (MASSO(K,NCELL).LE.0) GO TO 50
            CC(K,M) = CC(K,M)+(CHANGE(NCELL))*(CC(K,M)/MASSO(K,NCELL))
          END IF
50      CONTINUE
C
C
C       Each point is advected to a new location according to the
C       local velocity. This is done in several steps for clarity.
C
C       Convert to retarded velocity
C
        DO 60 J=1,NCOM2
          RVEL(J)=VEL(J)/(1.0+KD(K,J)*BD(J)/THETO(J))
          IF(RVEL(J).GE.30.0) MOCFLG=1
60      CONTINUE
C
C       Move the points to their new locations.  If a point moves out
C       of one cell it will begin to move at the new local velocity.
C       if the velocity in a cell is zero, points do not move there.
C
        DO 70 M=1,NPI(K)
          ILIN = 0
          DDLN = 0.0
63        ILIN = ILIN + 1
            DDLN = DDLN + DELX(ILIN)
            IF (Z(K,M) .GT. DDLN) GO TO 63
            NCELL = ILIN
          IF(ABS(RVEL(NCELL)-0.0).LT.1.0E-5) GO TO 70
          TEND  = (ZC(NCELL) + DELX(NCELL)/2 - Z(K,M))/RVEL(NCELL)
          IF (TEND .GT. DELT) THEN
            ZOLD = Z(K,M)
            Z(K,M) = Z(K,M) + DELT*RVEL(NCELL)
            DO 75 IFACE=1,ICROSS(K)
              IF (Z(K,M).GE.TOP(K,IFACE).AND.ZOLD.LT.TOP(K,IFACE))
     1          PCOUNT(K,IFACE) = PCOUNT(K,IFACE) + 1
75          CONTINUE
          ELSE
            ZOLD = Z(K,M)
            Z(K,M) = ZC(NCELL) + DELX(NCELL)/2
            DO 76 IFACE=1,ICROSS(K)
              IF (Z(K,M).GE.TOP(K,IFACE).AND.ZOLD.LT.TOP(K,IFACE))
     1          PCOUNT(K,IFACE) = PCOUNT(K,IFACE) + 1
76          CONTINUE
            TLEFT = DELT - TEND
            DO 80 LL=1,40
              IF (TLEFT.GT.0.0) THEN
               IF ((NCELL+LL).GT.NCOM2) THEN
                 RVEL(NCELL+LL)=RVEL(NCOM2)
                 DELX(NCELL+LL)=DELX(NCOM2)
               ENDIF
               ZOLD1= Z(K,M)
               Z(K,M)=Z(K,M)+AMIN1(DELX(NCELL+LL),RVEL(NCELL+LL)*TLEFT)
               DO 85 IFACE=1,ICROSS(K)
C
C   The following if statements and the local variable ZOLD1 above
C   were introduced by ssh at aqua terra so that PCOUNT is incremented
C   for only the last point consolidation boundary that is crossed in
C   one time step
C
                 IF (IFACE.EQ.1) THEN
                   IF (Z(K,M).GE.TOP(K,IFACE).AND.ZOLD1.LT.TOP(K,IFACE))
     1               PCOUNT(K,IFACE) = PCOUNT(K,IFACE) + 1
                 ELSE
                   IF (Z(K,M).GE.TOP(K,IFACE).AND.ZOLD1.LT.
     1             TOP(K,IFACE))THEN
                     PCOUNT(K,IFACE) = PCOUNT(K,IFACE) + 1
                     IF (ZOLD.LT.TOP(K,IFACE-1))
     1                 PCOUNT(K,IFACE-1) = PCOUNT(K,IFACE-1) - 1
                   ENDIF
                 ENDIF
85             CONTINUE
               IF (ABS(RVEL(NCELL+LL)-0.0).LT.1.0E-5) THEN
                 TLEFT=0.0
               ELSE
                 TLEFT=AMAX1(TLEFT-DELX(NCELL+LL)/RVEL(NCELL+LL),0.0)
               END IF
              ELSE
                GO TO 70
              END IF
80          CONTINUE
          END IF
70      CONTINUE
C
C    The array indices are readjusted to keep track of points which
C    flow into and out of the soil column.  The advective flux out of
C    column is calculated as the sum of the mass carried by the
C    points which move out of the bottom.
C
        ADFLUX(K,NCOM2)=0.0
        CCSUM = 0.0
        IOUT=NPI(K) + 1
        DO 90 M=1,NPI(K)
          IF(Z(K,M).GT.CORED) THEN
C
C           IOUT is the lowest valued index no. of points below the core
C
            IOUT = MIN0(M,IOUT)
            CCSUM = CCSUM + CC(K,M)
          END IF
90      CONTINUE
        CC(K,IOUT) = CCSUM
C
C       Following code skips calculation of adflux if SAFTMOD is on but
C       VADOFT is not ???
C
        ADFLUX(K,NCOM2) = CCSUM / DELT
        NPI(K) = IOUT - 1
C
        NEW =  0
        DDLN = 0
        ILIN = 1
C
C    The following if statements and the local variable NUMSUM were
C    added by ssh at aqua terra, 1-89, so that only two new points
C    are placed in layers less than or equal to 2 cm thick.  Also, the
C    maximum number of new points was changed from 50 to 150 (see the
C    DO 100 statement) to prevent mass balance errors.
C
        IF(DELX(ILIN).LE.2.0) THEN
          NUM=2
          NUMSUM=2
        ELSE
          NUM=4
          NUMSUM=4
       ENDIF
        DO 100 I=1,150
C         IF (I-1 .EQ. ILIN*NUM) ILIN = ILIN + 1
          IF (I-1 .EQ. NUMSUM) THEN
            ILIN = ILIN + 1
            IF(DELX(ILIN).LE.2.0) THEN
              NUM=2
              NUMSUM=NUMSUM+NUM
            ELSE
              NUM=4
              NUMSUM=NUMSUM+NUM
            ENDIF
          ENDIF
          DDLN = DDLN + DELX(ILIN)/NUM
          IF ((Z(K,1)-DDLN).GT.0.0) THEN
C           ZIN(I) = Z(K,1)-DDLN
            ZIN(I) = DDLN
            NEW=NEW + 1
          ELSE
            GO TO 110
          END IF
100     CONTINUE
110     CONTINUE
C
        IF ((NPI(K)+NEW) .GT. NPII) THEN
          IERROR = 2040
          WRITE(MESAGE,2090) NPI(K), NEW, NPII
          FATAL  = .TRUE.
          CALL ERRCHK(IERROR,MESAGE,FATAL)
        ENDIF
C
        DO 120 M=NPI(K),1,-1
          Z(K,M+NEW) = Z(K,M)
          CC(K,M+NEW) = CC(K,M)
120     CONTINUE
C
C       The mass to assign to incoming points is based on the
C       concentration of incoming water.
C
        IDEL = 0
        IF (NEW.GT.0) THEN
          DO 130 M=1,NEW
            Z(K,M) = ZIN(M)
            CC(K,M)  = CNCPND*ZIN(1)/NEW
130       CONTINUE
          NPI(K) = NPI(K) + NEW
C
C         Consolidate points if necassary
C
          DO 190 M=1,ICROSS(K)
230         CONTINUE
              IF (PCOUNT(K,M) .GE. RATIO(K,M)) THEN
                IDEL = IDEL + RATIO(K,M) - 1
              DO 195 MM=1, NPI(K)
C
C               Find index of the first point under the interface
C
                IF (Z(K,MM) .GE. TOP(K,M)) THEN
                  FIRST = MM
                  GO TO 200
                ENDIF
195           CONTINUE
200         CONTINUE
C
C           Average points that need to be consolidated
C           distance is mass averaged, mass is summed
C
            ISTART = FIRST + PCOUNT(K,M) - RATIO(K,M)
            IEND   = FIRST + PCOUNT(K,M) - 1
            ZTOT   = 0.
            CTOT   = 0.
            ZCTOT  = 0.
            DO 210 M3=ISTART, IEND
              ZCTOT = ZCTOT + Z(K,M3)*CC(K,M3)
              CTOT  = CTOT + CC(K,M3)
              ZTOT  = ZTOT + Z(K,M3)
210         CONTINUE
            IF (CTOT.LE.1.0E-30) THEN
              Z(K,ISTART)= ZTOT/(IEND - ISTART + 1.)
            ELSE
              Z(K,ISTART) = ZCTOT/CTOT
            END IF
            CC(K,ISTART) = CTOT
C
C           Shift Z and CC arrays
C
            RTIOM1 = RATIO(K,M) - 1
            DO 220 M3=ISTART+1, NPI(K)-RTIOM1
              Z(K,M3) = Z(K,M3+RTIOM1)
              CC(K,M3) = CC(K,M3+RTIOM1)
220         CONTINUE
            PCOUNT(K,M) = PCOUNT(K,M) - RATIO(K,M)
            ICHECK = 1
          ELSE
            ICHECK = 0
C
C    The following line was added by ssh at aqua terra, 1-89, so
C    that the point consolidation counter is reset to zero after
C    each time step.
C
            PCOUNT(K,M) = 0
          ENDIF
          IF (ICHECK .EQ. 1) GO TO 230
190       CONTINUE
        END IF
        NPI(K) = NPI(K) - IDEL
C
C       Calculate the total mass and convert to dissolved concentration
C       in each cell.
C
        DO 140 M=1,NPI(K)
          ILIN = 0
          DDLN = 0.0
133       ILIN = ILIN + 1
            DDLN = DDLN + DELX(ILIN)
            IF (Z(K,M) .GT. DDLN) GO TO 133
            NCELL = ILIN
          SUMC (NCELL) =  SUMC(NCELL) + CC(K,M)
140     CONTINUE
C
        DO 150 J=1,NCOM2
          MASS(J)=SUMC(J)
          IF (ABS(THETO(J)-0.0).LT.1.0E-5) THEN
            PTEMP(J)=PESTR(K,J)
          ELSE
            PTEMP(J)=MASS(J)/THETO(J)/DELX(J)
            SPTEMP(K,J)=PTEMP(J)*THETO(J)/(THETO(J)+KD(K,J)*BD(J)+
     1                (THETAS(J)-THETO(J))*OKH(K,J))
          END IF
150     CONTINUE
C
C    Calculate the flux advected out of interior cells.  This is the
C    net flux in the next cell down (difference before and after the
C    advection step) minus the flux out of that lower cell.  This
C    difference gives the flux into the underlying cell which is
C    equal to the advective flux out of the cell of interest.
C
        DO 160 J=1,NCOM2
          NET(J)=(PESTR(K,J)-PTEMP(J))*DELX(J)*THETO(J)/DELT
160     CONTINUE
C
        DO 170 J=NCOM2-1,1,-1
          ADFLUX(K,J)=ADFLUX(K,J+1)-NET(J+1)
170     CONTINUE
C
C
C      Store the calculated concentrations
C
       DO 180 J=1,NCOM2
         MASSO(K,J)=MASS(J)
180    CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE TRDIAG (A,B,C,X,F,N,LPRZOT,MODID)
C
C     + + + PURPOSE + + +
C
C     Solves a system of equations with a tridiagonal coefficient matrix
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      INCLUDE 'PPARM.INC'
      REAL*8      A(NCMPTS),B(NCMPTS),C(NCMPTS),F(NCMPTS),
     1            X(NCMPTS)
      INTEGER     N,LPRZOT
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     A      - 1ST DIAGONAL VECTOR OF THE TRIDIAGONAL MATRIX
C     B      - 2ND DIAGONAL VECTOR OF THE TRIDIAGONAL MATRIX
C     C      - 3RD DIAGONAL VECTOR OF THE TRIDIAGONAL MATRIX
C     F      - RIGHT HAND SIDE VECTOR
C     X      - WORKING ARRRAY (SCRATCH ARRAY)
C     N      - TOTAL NUMBER OF COMPARTMENTS
C     LPRZOT - FILE OUTPUT UNIT NUMBER
C     MODID  - MODEL ID
C
C     + + + PARAMETERS + + +
C
C      INCLUDE 'PPARM.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL*8       U(NCMPTS),Y(NCMPTS),L(NCMPTS)
      INTEGER      I,NM1,IERROR,PREVFLG
      CHARACTER*80 MESAGE
      LOGICAL      FATAL
C
C     + + + FUNCTIONS + + +
C
      REAL*8       RELTST
C
C     + + + INTRINSICS + + +
C
      INTRINSIC ABS
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,ERRCHK,SUBOUT,RELTST
C
C     + + + DATA INITIALIZATIONS + + +
C
      DATA U,Y,L / NCMPTS*0.D0, NCMPTS*0.D0, NCMPTS*0.D0 /
C
C     + + + OUTPUT FORMATS + + +
C
2000  FORMAT (1X,A3,1X,110(1H*),/,1X,A3,1X,110(1H*),/,1X,A3,/,1X,A3,50X,
     1        'E R R O R',/,1X,A3,/,1X,A3,10X,'TRIDIAGONAL MATRIX IN ',
     2        'SUBROUTINE TRDIAG COULD NOT BE SOLVED ON THIS DAY. PRZM',
     3        ' WILL',/,1X,A3,10X,' USE VALUES FOR THE LAST TIME STEP ',
     4        'AND CONTINUE ON. YOU MAY WANT TO STOP AND CHECK',/,1X,A3,
     5       10X,'BOTH THE INPUT SEQUENCE AND THE CODE IN SLPST0, SLPS',
     6        'T1, OR TRDIA1',/,1X,A3,1X,A3,/,1X,A3,/,1X,A3,1X,110(1H*))
 2100 FORMAT('Solution for tridiagonal matrix not found, previous ',
     1       'days values used')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'TRDIAG'
      CALL SUBIN(MESAGE)
      PREVFLG=0
C
C     Factor matrix into upper and lower halves
C
      U(1)=B(1)
      DO 10 I=2,N
        IF(ABS(U(I-1)).LT.1.0E-5)THEN
          PREVFLG=1
          GO TO 400
        ENDIF
        L(I)=A(I)/U(I-1)
        U(I)=B(I)-L(I)*C(I-1)
10    CONTINUE
C
C     Solve LUX=F
C
      Y(1)=F(1)
      DO 20 I=2,N
         Y(I)=F(I)-L(I)*Y(I-1)
         Y(I)=RELTST(Y(I))
20    CONTINUE
C
      IF(ABS(U(N)).LT.1.0E-5)THEN
        PREVFLG=1
      ELSE
         X(N)=Y(N)/U(N)
         X(N)=RELTST(X(N))
         NM1=N-1
         DO 30 I=1,NM1
            X(N-I)=(Y(N-I)-C(N-I)*X(N+1-I))/U(N-I)
            X(N-I)=RELTST(X(N-I))
30      CONTINUE
      ENDIF
C
400   IF(PREVFLG.EQ.1)THEN
      IERROR = 2050
      WRITE(MESAGE,2100)
      FATAL  = .FALSE.
      CALL ERRCHK(IERROR,MESAGE,FATAL)
      WRITE(LPRZOT,2000) (MODID,I=1,11)
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE MASBAL (APDEP,K,IPRZM,IRTYPE,IRRR)
C
C     + + + PURPOSE + + +
C
C     Calculates mass balance error terms for both hydrology
C     and pesticide transport.
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER   K, IPRZM,IRTYPE
      REAL      APDEP,IRRR
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
      INCLUDE 'PMXZON.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CGLBPZ.INC'
      INCLUDE 'CSPTIC.INC'
C
C     + + + LOCAL VAIRIABLES + + +
C
      INTEGER      I
      REAL*8       XP(NCMPTS),XPB(NCMPTS),TERM1,TERM2
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,SUBOUT
C
C     + + + INTRINSICS + + +
C
      INTRINSIC FLOAT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'MASBAL'
      CALL SUBIN(MESAGE)
C
        WINPZ(IPRZM)  = 0.0
        WDSTPZ(IPRZM) = 0.0

        PDKPZ(IPRZM,1:K)  = 0.0
        PINPZ(IPRZM,1:K)  = 0.0
        PDSTPZ(IPRZM,1:K) = 0.0
        PTRPZ(IPRZM,1:K)  = 0.0
        PSRCFX(IPRZM,1:K) = 0.0
        IF (K .GT. 1) GO TO 15
C
C       First pest, need a water balance
C
        WBAL= 0.0
        IF((IRTYPE.NE.5).AND.(IRTYPE.NE.7))THEN
          WBAL= PRECIP+SNOWFL+APDEP-RUNOF-AINF(NCOM2+1)+OSNOW-SNOW
     1          +CINTB-CINT-CEVAP
        ELSE
          WBAL= PRECIP+IRRR+SNOWFL+APDEP-RUNOF-AINF(NCOM2+1)+OSNOW-SNOW
     1          +CINTB-CINT-CEVAP
        ENDIF
C
C       Store intermediate results for global mass balance
C
        WINPZ(IPRZM) = WBAL + AINF(NCOM2+1) + WINPZ(IPRZM)
C
        DO 10 I=1,NCOM2
          WBAL= WBAL+LINF(I)-ET(I)-OUTFLO(I)+(THETO(I)-THETN(I))*DELX(I)
C
C         store intermediate results for global mass balance
C
          WINPZ(IPRZM) = WINPZ(IPRZM)-ET(I)-OUTFLO(I)
          WDSTPZ(IPRZM) = WDSTPZ(IPRZM) + (THETN(I)-THETO(I))*DELX(I)
10      CONTINUE
        CWBAL= CWBAL+WBAL
15    CONTINUE
C
C     Pest balance
C
      PBAL(K)= 0.0
      IF(NCHEM.EQ.1)THEN
        PBAL(K)= FOLP0(K)-FOLPST(K)-FPDLOS(K)-FPVLOS(K)
      ELSEIF(NCHEM.GT.1)THEN
        IF(K.EQ.1)THEN
          PBAL(K)=FOLP0(K)-FOLPST(K)-FPDLOS(K)-FPVLOS(K)-FPLOS12-FPLOS13
        ELSEIF(K.EQ.2)THEN
          PBAL(K)=FOLP0(K)-FOLPST(K)-FPDLOS(K)-FPVLOS(K)-FPLOS23+FPLOS12
        ELSEIF(K.EQ.3)THEN
          PBAL(K)=FOLP0(K)-FOLPST(K)-FPDLOS(K)-FPVLOS(K)+FPLOS13+FPLOS23
        ENDIF
      ENDIF
C
      PBAL(K)= PBAL(K)-ROFLUX(K)-ERFLUX(K)-ADFLUX(K,NCOM2)
     1         -SDKFLX(K)-SUPFLX(K)
C**** ADD LATERAL OUTFLOW PESTICIDE FLUX ************************
     +         -LATFLX(K)
cjmc wterm(k) replace by woflux(k), woflux=total flux from soil cmprts.
cjmc      PINPZ(IPRZM,K) = PINPZ(IPRZM,K) + WTERM(K) -
cjmc     1               ROFLUX(K) - ERFLUX(K) - SUPFLX(K) +
cjmc     2               PVFLUX(K,1)
      PINPZ(IPRZM,K) = PINPZ(IPRZM,K) + WOFLUX(K) -
     1               ROFLUX(K) - ERFLUX(K) - SUPFLX(K) +
     2               PVFLUX(K,1)
C
      DO 20 I=1,NCOM2
        XP(I)= X(I)*(THETN(I)+KD(K,I)*BD(I)+(THETAS(I)-THETN(I))
     1         *KH(K,I))
C ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
C  Date: Wednesday, 17 June 1992.  Time: 10:41:10.
        TERM1=PESTR(K,I)*THETO(I)
        TERM2=TERM1-XP(I)
        XPB(I)=TERM2*DELX(I)/FLOAT(DELT)+(SRCFLX(K,I)-TRFLUX(K,I))
C        XPB(I)=(PESTR(K,I)*THETO(I)-XP(I))*DELX(I)/DELT+SRCFLX(K,I)
C     1         -TRFLUX(K,I)
        PBAL(K)=PBAL(K)+XPB(I)
C
        PDSTPZ(IPRZM,K) = PDSTPZ(IPRZM,K)-TERM2*DELX(I)/DELT
C        PDSTPZ(IPRZM,K) = PDSTPZ(IPRZM,K)+(XP(I)- PESTR(K,I)*THETO(I))*
C     1                  DELX(I)/DELT
C ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        PTRPZ(IPRZM,K) = PTRPZ(IPRZM,K) + TRFLUX(K,I)
        PSRCFX(IPRZM,K) = PSRCFX(IPRZM,K) + SRCFLX(K,I)
        PINPZ(IPRZM,K) = PINPZ(IPRZM,K) + SRCFLX(K,I)
20    CONTINUE
      PDKPZ(IPRZM,K) = PDKPZ(IPRZM,K) + SDKFLX(K)
      PBAL(K) =PBAL(K) + PVFLUX(K,1)
      CPBAL(K)=CPBAL(K)+PBAL(K)
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE PSTLNK(K,J)
C
C     + + + PURPOSE + + +
C
C     Provides linkage for transformation and source terms for
C     parent/daughter relationships
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      INTEGER   K,J
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     K   - chemical number
C     J   - daughter number
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CPEST.INC'
      INCLUDE 'CHYDR.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER  KK
C
C     + + + END SPECIFICATIONS + + +
C
      RTRW(1,J) = 0.0
      RTRS(1,J) = 0.0
      DO 10 KK = 1, NCHEM
        SRCW(KK,J) = 0.0
        SRCS(KK,J) = 0.0
10    CONTINUE
      IF (K.NE.1) GO TO 15
        RTRW(2,J) = DKRW12(J)
        RTRS(2,J) = DKRS12(J)
        RTRW(3,J) = DKRW13(J)
        RTRS(3,J) = DKRS13(J)
        GO TO 20
15    CONTINUE
      IF (K.NE.2) GO TO 16
        RTRW(2,J) = 0.0
        RTRS(2,J) = 0.0
        RTRW(3,J) = DKRW23(J)
        RTRS(3,J) = DKRS23(J)
        SRCW(1,J) =DKRW12(J)*(SPESTR(1,J)*THETN(J))
        SRCS(1,J) =DKRS12(J)*(SPESTR(1,J)*KD(1,J)*BD(J))
        GO TO 20
16    CONTINUE
      RTRW(2,J) = 0.0
      RTRS(2,J) = 0.0
      RTRW(3,J) = 0.0
      RTRS(3,J) = 0.0
      SRCW(1,J) = DKRW13(J)*(SPESTR(1,J)*THETN(J))
      SRCS(1,J) = DKRS13(J)*(SPESTR(1,J)*KD(1,J)*BD(J))
      SRCW(2,J) = DKRW23(J)*(SPESTR(2,J)*THETN(J))
      SRCS(2,J) = DKRS23(J)*(SPESTR(2,J)*KD(2,J)*BD(J))
C
20    CONTINUE
C
      RETURN
      END
C
C
C
      SUBROUTINE   NITRAP
     I                   (FECHO)
C
C     + + + PURPOSE + + +
C     Computes amount and location of nitrogen application.
C     Further modified by PV @ AQUA TERRA Consultants 9/93 to hardwire
C     the calculation of pesticide depth in runoff to 1 cm.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   FECHO
C
C     + + + ARGUMENT DEFINITIONS + + +
C     FECHO  - Fortran unit number for echo file
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CNITR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CHYDR.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      I,CMPT
      REAL         DEP,APPDEP
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
      INTRINSIC REAL,DBLE
C
C     + + + EXTERNALS + + +
      EXTERNAL SUBIN,SUBOUT,PZDSPL
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT(' Surface compartment > 1 cm: Nitrogen Distributed',
     $       ' to 1st compartment depth')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'NITRAP'
      CALL SUBIN(MESAGE)
C
      IF (DEPI(1,NAPPC) .GT. DELX(1)) THEN
C       the nitrogen is incorporated beyond the surface compartment
        IF (DEPI(1,NAPPC) .LT. 1.0) THEN
C         distribute the nitrogen to 1 cm depth
          APPDEP = 1.0
        ELSE
C         distribute the nitrogen down to the depth of incorporation
          APPDEP = DEPI(1,NAPPC)
        END IF
      ELSE
C       Hard-wiring the nitrogen distribution to 1 cm depth when-
C       ever it is surface applied.  Distribute the nitrogen in
C       either the first compartment thickness or 1 cm.
        IF (DELX(1) .GE. 1.0) THEN
C         nitrogen will be distributed through the first compartment
          APPDEP = 0.0
          IF (DELX(1) .GT. 1.0) THEN
C           warn user about distributing further than specified in input
            WRITE(MESAGE,2000)
            CALL PZDSPL(FECHO,MESAGE)
          END IF
        ELSE
C         nitrogen will be distributed in the 1 cm depth
          APPDEP = 1.0
        END IF
      END IF
C
C     determine how many compartments to distribute nitrogen in
      CMPT= 0
      DEP = 0.0
 10   CONTINUE
        CMPT= CMPT + 1
        DEP = DEP + DELX(CMPT)
      IF (DEP .LT. APPDEP) GO TO 10
C
      DO 20 I = 1,CMPT
C       add nitrogen application to appropriate compartments
        SOILAP(1,I) = (TAPP(1,NAPPC)*APPEFF(1,NAPPC))/CMPT
        SOILAP(2,I) = (TAPP(2,NAPPC)*APPEFF(1,NAPPC))/CMPT
        SOILAP(3,I) = (TAPP(3,NAPPC)*APPEFF(1,NAPPC))/CMPT
        NIT(1,I) = NIT(1,I) + SOILAP(3,I) * (1.0-NAPFRC(NAPPC))
        NIT(2,I) = NIT(2,I) + SOILAP(1,I)
        NIT(4,I) = NIT(4,I) + SOILAP(2,I)
        NIT(7,I) = NIT(7,I) + SOILAP(3,I) * NAPFRC(NAPPC)
 20   CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   NITBAL
     I                   (APDEP,IPRZM)
C
C     + + + PURPOSE + + +
C
C     Calculates mass balance error terms for both hydrology
C     and nitrogen transport.
C     Modification date: 9/26/95 PRH
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   IPRZM
      REAL      APDEP
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CNITR.INC'
      INCLUDE 'CSPTIC.INC'
C
C     + + + LOCAL VAIRIABLES + + +
      INTEGER      I
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'NITBAL'
      CALL SUBIN(MESAGE)
C
C     first do water balance
      WBAL= 0.0
      WBAL= PRECIP+SNOWFL+APDEP-RUNOF-AINF(NCOM2+1)+OSNOW-SNOW
     1      +CINTB-CINT-CEVAP
C
      DO 10 I=1,NCOM2
        WBAL= WBAL+LINF(I)-ET(I)-OUTFLO(I)+(THETO(I)-THETN(I))*DELX(I)
10    CONTINUE
      CWBAL= CWBAL+WBAL
C
C     nitrogen balance, start with change in storage
      PBAL(1) = TONIT0 - TOTNIT
C     add input fluxes
      DO 20 I = 1,3
C       three constituent depositions and septic inflows
        PBAL(1) = PBAL(1) + NIADDR(I) + NIADWT(I)
 20   CONTINUE
      DO 30 I = 1,NCOM2
C       three constituent soil applications
        PBAL(1) = PBAL(1) + SOILAP(1,I) + SOILAP(2,I) + SOILAP(3,I)
C       three constituent septic effluent inflows
        PBAL(1) = PBAL(1) + AMMINF(I) + NITINF(I) + ORGINF(I)
        IF (FIXNFG.EQ.1) THEN
C         include nitrogen fixation
          PBAL(1) = PBAL(1) + NCFX12(I,1)
        END IF
C       subtract lateral outflow from each compartment
        PBAL(1) = PBAL(1) - NCFX3(I,1) - NCFX5(I,1) -
     $            NCFX14(I,1) - NCFX16(I,1)
C       denitrification and volatilization
        PBAL(1) = PBAL(1) - NCFX6(I,1) - NCFX18(I,1)
 30   CONTINUE
C     subtract core outflow
      PBAL(1) = PBAL(1) - NCFX2(NCOM2,1) - NCFX4(NCOM2,1) -
     $          NCFX13(NCOM2,1) - NCFX15(NCOM2,1)
C
      CPBAL(1) = CPBAL(1) + PBAL(1)
C
C     update total nitrogen storage
      TONIT0 = TOTNIT
C
      CALL SUBOUT
C
      RETURN
      END
