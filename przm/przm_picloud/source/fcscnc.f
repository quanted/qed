
      SUBROUTINE FCSCNC(K)
C
C     + + + PARAMETERS + + +
C
      Use IO_LUNS
C     Use Inf_NaN_Detection
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CPEST.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER    I,K
C
C
2000  FORMAT(6Es12.5)
      IF(MWFLG.EQ.0)THEN
        YRINF1(K) = (YRINF1(K)+ AINF(NCOM2))
        YRFLX1(K) = YRFLX1(K)+ (ADFLUX(K,NCOM2)+DFFLUX(K,NCOM2))
        YRINF2(K) = (YRINF2(K)+ AINF(MTR1))
        YRFLX2(K) = YRFLX2(K)+ (ADFLUX(K,MTR1)+DFFLUX(K,MTR1))
      ENDIF
C
      IF(JULDAY.EQ.CNDMO(LEAP,13))THEN

        YRCNC1 = 0.0
        IF (YRINF1(K)>0.0) YRCNC1=((YRFLX1(K)*1.E14)/(YRINF1(K)*1.E5))
        YRCNC2 = 0.0
        IF (YRINF2(K)>0.0) YRCNC2=((YRFLX2(K)*1.E14)/(YRINF2(K)*1.E5))

        ! 156 -> 1.cnc
        WRITE(lun_cnc(k),2000)YRCNC1,YRFLX1(K)*1.E8,YRINF1(K)*1.E5,
     *                  YRCNC2,YRFLX2(K)*1.E8,YRINF2(K)*1.E5
          YRCNC1=0.0
          YRFLX1(K)=0.0
          YRINF1(K)=0.0
          YRCNC2=0.0
          YRFLX2(K)=0.0
          YRINF2(K)=0.0

      ENDIF
C
      RETURN
C
      END
C
C*********************************************
      SUBROUTINE FCSMSB(K)
C
C     + + + PARAMETERS + + +
C
      Use IO_LUNS
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CPEST.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL       YRDKM1(3),YRRNM1(3),YRVLM1(3),YRLCM1(3),YRUPM1(3),
     *           YRCRM1,XP9(500),XSOIL(500),YRERM1(3)
      REAL       YRDKM2(3),YRVLM2(3),YRLCM2(3),YRUPM2(3),YRFRM1(3),
     *           TOTAPP(3)
      REAL       YRCRM2
      INTEGER    I,II,K
C
      SAVE  YRDKM1,YRRNM1,YRVLM1,YRCRM1,YRLCM1,YRUPM1,YRERM1,
     *      YRDKM2,YRVLM2,YRCRM2,YRLCM2,YRUPM2,XSOIL,YRFRM1,TOTAPP
C
2000  FORMAT(13Es12.5)
C
      IF (JULDAY.EQ.IAPDY(NAPPC) .AND. IY.EQ.IAPYR(NAPPC))THEN
        XSOIL(K) = 0.00
        DO 4 I = 1, NCOM2
          XSOIL(K) = XSOIL(K) + SOILAP(K,I)*1.E5
4       CONTINUE
        TOTAPP(K) = TOTAPP(K)+ XSOIL(K) + plntap(K)*1.E5
      ENDIF
C
C
! PVFLUX - Soil pesticide volatilization flux [g cm-2 day-1]
! FPVLOS - Foliar pesticide volatilization flux Soil Temperature [g cm-2 day-1]
! ROFLUX - ROFLUX Surface runoff flux, g/cm2/day
! ERFLUX - Erosion flux of pesticide, g/cm2/day
! ADFLUX - Pesticide advective flux from each soil compartment
! DFFLUX - [g cm-2 day-1] Array Diffusive/Dispersive Flux of Pesticide Leaving Each Soil Compartment
! PVFLUX - [g cm-2 day-1] Array Daily Soil Pesticide Volatilization Flux
! FPVLOS - [g cm-2 day-1] Array Daily Foliage Pesticide Volatilization Flux
! TSRCFX - [g cm-2 day-1] Array Sum of the Source Flux from All Compartments in Soil Profile
! TRFLUX - [g cm-2 day-1] Array Transformation Flux of Pesticide from Each Soil Compartment
! UPFLUX - [g cm-2] Array Uptake Flux of Pesticide From Each Soil Compartment
      YRRNM1(K) = YRRNM1(K)+ ROFLUX(K)* 1.E5
      YRERM1(K) = YRERM1(K)+ ERFLUX(K)* 1.E5
      YRLCM1(K) = YRLCM1(K)+ (ADFLUX(K,NCOM2)+DFFLUX(K,NCOM2))* 1.E5
      YRLCM2(K) = YRLCM2(K)+ (ADFLUX(K,MTR1)+DFFLUX(K,MTR1))* 1.E5
      YRVLM1(K) = YRVLM1(K)+ PVFLUX(K,1)* 1.E5 !+ FPVLOS(K)* 1.E5 !debug
      YRVLM2(K) = YRVLM2(K)+ PVFLUX(K,1)* 1.E5 !+ FPVLOS(K)* 1.E5	!debug
      IF(K.GT.1)THEN
        YRFRM1(K) = YRFRM1(K)+ TSRCFX(K)*1.E5
      ENDIF
C
      DO 80 I=1,NCOM2
          YRDKM1(K) = YRDKM1(K)+ DKFLUX(K,I)* 1.E5+ TRFLUX(K,I)*1.E5
          YRUPM1(K) = YRUPM1(K)+ UPFLUX(K,I)* 1.E5
          IF(I.LE.MTR1)THEN
            YRDKM2(K) = YRDKM2(K)+ DKFLUX(K,I)* 1.E5+ TRFLUX(K,I)*1.E5
            YRUPM2(K) = YRUPM2(K)+ UPFLUX(K,I)* 1.E5
          ENDIF
80    CONTINUE
      YRDKM1(K)=YRDKM1(K)+FPDLOS(K)*1.0E+05
      YRDKM2(K)=YRDKM2(K)+FPDLOS(K)*1.0E+05
C
      IF(JULDAY.EQ.CNDMO(LEAP,13))THEN
        IF(K.EQ.1)THEN
          DO 240 II=1,NCOM2
            XP9(II)= X(II)*DELX(II)*(THETN(II)+KD(K,II)*BD(II)
     1              +(THETAS(II)-THETN(II))*KH(K,II))* 1.E5
            YRCRM1 = YRCRM1+ XP9(II)
          IF(II.LE.MTR1)THEN
            YRCRM2 = YRCRM2+ XP9(II)
          ENDIF
240       CONTINUE
          ! 159 -> 1.msb
          WRITE(lun_msb(k),2000)YRRNM1(K),-YRVLM1(K),YRDKM1(K),
     *                  YRUPM1(K),YRLCM1(K),YRCRM1,
     *                  -YRVLM2(K),YRDKM2(K),
     *                  YRUPM2(K),YRLCM2(K),YRCRM2,TOTAPP(K),YRERM1(K)
          YRDKM1(K)=0.0
          YRVLM1(K)=0.0
          YRRNM1(K)=0.0
          YRERM1(K)=0.0
          YRUPM1(K)=0.0
          YRLCM1(K)=0.0
          XSOIL(K)=0.0
          YRCRM1=0.0
          YRDKM2(K)=0.0
          YRVLM2(K)=0.0
          YRUPM2(K)=0.0
          YRLCM2(K)=0.0
          YRCRM2=0.0
          TOTAPP(K)=0.0
        ELSEIF(K.EQ.2)THEN
          DO 250 II=1,NCOM2
            XP9(II)= X(II)*DELX(II)*(THETN(II)+KD(K,II)*BD(II)
     1              +(THETAS(II)-THETN(II))*KH(K,II))* 1.E5
            IF(MWFLG.EQ.0)THEN
              YRCRM1 = YRCRM1+ XP9(II)
            ELSEIF(MWFLG.EQ.1)THEN
              YRCRM1 = YRCRM1+ XP9(II)*MW21
            ENDIF
250       CONTINUE
          ! 160 -> 2.msb
          WRITE(lun_msb(k),2000)YRRNM1(K),-YRVLM1(K),YRDKM1(K),
     *                  YRUPM1(K),YRLCM1(K),YRCRM1,
     *                  -YRVLM2(K),YRDKM2(K),
     *                  YRUPM2(K),YRLCM2(K),YRCRM2,YRFRM1(K),YRERM1(K)
          YRDKM1(K)=0.0
          YRVLM1(K)=0.0
          YRRNM1(K)=0.0
          YRERM1(K)=0.0
          YRUPM1(K)=0.0
          YRLCM1(K)=0.0
          XSOIL(K)=0.0
          YRCRM1=0.0
          YRDKM2(K)=0.0
          YRVLM2(K)=0.0
          YRUPM2(K)=0.0
          YRLCM2(K)=0.0
          YRCRM2=0.0
          YRFRM1(K)=0.0
          TOTAPP(K)=0.0
        ELSEIF(K.EQ.3)THEN
          DO 260 II=1,NCOM2
            XP9(II)= X(II)*DELX(II)*(THETN(II)+KD(K,II)*BD(II)
     1              +(THETAS(II)-THETN(II))*KH(K,II))* 1.E5
            IF(MWFLG.EQ.0)THEN
              YRCRM1 = YRCRM1+ XP9(II)
            ELSEIF(MWFLG.EQ.1)THEN
              YRCRM1 = YRCRM1+ (XP9(II)*MW31)+(XP9(II)*MW32)
            ENDIF
260       CONTINUE
          ! 161 -> 3.msb
          WRITE(lun_msb(k),2000)YRRNM1(K),-YRVLM1(K),YRDKM1(K),
     *                  YRUPM1(K),YRLCM1(K),YRCRM1,
     *                  -YRVLM2(K),YRDKM2(K),
     *                  YRUPM2(K),YRLCM2(K),YRCRM2,YRFRM1(K),YRERM1(K)
          YRDKM1(K)=0.0
          YRVLM1(K)=0.0
          YRRNM1(K)=0.0
          YRERM1(K)=0.0
          YRUPM1(K)=0.0
          YRLCM1(K)=0.0
          XSOIL(K)=0.0
          YRCRM1=0.0
          YRDKM2(K)=0.0
          YRVLM2(K)=0.0
          YRUPM2(K)=0.0
          YRLCM2(K)=0.0
          YRCRM2=0.0
          YRFRM1(K)=0.0
          TOTAPP(K)=0.0
        ENDIF
      ENDIF
C
      RETURN
C
      END

C*********************************************
      SUBROUTINE FCSHYD(K)
C
C     + + + PARAMETERS + + +
C
      Use IO_LUNS
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CMET.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL       YRTDET,YRRNOF,YRPRCP,YRSEDL,YRAINF,YRIRRR
      INTEGER    K
C
      SAVE  YRTDET,YRRNOF,YRPRCP,YRSEDL,YRAINF,YRIRRR
C
2000  FORMAT(6Es12.5)
C
      IF(K.EQ.1)THEN
        YRPRCP = YRPRCP+ PRECIP+SNOWFL
        YRRNOF = YRRNOF+ RUNOF
        YRSEDL = YRSEDL+ SEDL
        YRTDET = YRTDET+ TDET + CEVAP ! adding canopy evaporation (cevap)
        YRAINF = YRAINF+ AINF(1)
        YRIRRR = YRIRRR+ IRRR
        IF(JULDAY.EQ.CNDMO(LEAP,13))THEN
c          IF((IRTYPE.NE.5).AND.(IRTYPE.NE.7).AND.
c     *       (IRTYPE.NE.1).AND.(IRTYPE.NE.2))THEN
c            ! 162 -> 1.hyd
c            WRITE(lun_hyd(k),2000)YRPRCP-YRIRRR,YRRNOF,YRTDET,
c     *                     YRSEDL,YRAINF,YRIRRR
c          ELSE
c            WRITE(lun_hyd(k),2000)YRPRCP,YRRNOF,YRTDET,
c     *                     YRSEDL,YRAINF,YRIRRR
c          ENDIF

          Select Case(IRTYPE)
             Case(1, 2, 5, 7)
               ! 162 -> 1.hyd
               WRITE(lun_hyd(k),2000)YRPRCP,YRRNOF,YRTDET,
     *                        YRSEDL,YRAINF,YRIRRR
             Case Default
               ! 162 -> 1.hyd
               WRITE(lun_hyd(k),2000)YRPRCP-YRIRRR,YRRNOF,YRTDET,
     *                        YRSEDL,YRAINF,YRIRRR
          End Select

          YRPRCP=0.0
          YRRNOF=0.0
          YRTDET=0.0
          YRSEDL=0.0
          YRAINF=0.0
          YRIRRR=0.0
        ENDIF
      ENDIF
C
      RETURN
C
      END
