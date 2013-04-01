C
C
C
      SUBROUTINE   PRZM
     I                 (RSTFG, NUMFIL, MCARLO, SEPTON, NITRON,
     I                  MODID, RSDAT, REDAT, LPRZRS,
     I                  LPRZOT, LPRZIN, LWDMS,
     I                  LMETEO, LSPTIC, LNITAD,
     I                  LTMSRS, SRNFG, BASEND, IPRZM, ITSAFT, NLDLT)
C
C     +  +  + PURPOSE +  +  +
C     called by EXESUP to execute PRZM
C     Modification date: 2/18/92 JAM
C
      Use m_Wind
      Use m_Crop_Dates
      Use m_Canopy
      Use debug
      Use Date_Module
      Use m_chem
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     SRNFG,BASEND,RSTFG,NUMFIL,IPRZM,ITSAFT,NLDLT
      INTEGER     RSDAT(3),REDAT(3),LPRZRS,LPRZOT,
     1            LPRZIN,LMETEO,LSPTIC,LNITAD,LTMSRS,LWDMS
      LOGICAL     MCARLO,SEPTON,NITRON,APPLY
      CHARACTER*3 MODID(NUMFIL)
      REAL        CURVN
      INTEGER*4   RODPTH
      Integer ::  jd_today  ! today's Julian day
C
C     +  +  + ARGUMENT DEFINITIONS +  +  +
C     RSTFG  - restart starting flag
C     NUMFIL - max. number of open files
C     MCARLO - flag for Monte Carlo on
C     SEPTON - septic effluent on flag
C     NITRON - nitrogen modeling on flag
C     MODID  - model id (pest,conc,water)
C     RSDAT  - restart starting date
C     REDAT  - restart ending date
C     LPRZRS - unit number for przm restart file
C     LPRZOT - unit number for przm output file
C     LPRZIN - unit number for przm input file
C     LMETEO - unit number for meteorlogical file
C     LSPTIC - unit number for septic effluent file
C     LNITAD - unit number for nitrogen atmospheric deposition
C     LTMSRS - unit number for time series file
C     LWDMS  - unit number for WDM file
C     SRNFG  - starting run flag
C     BASEND - base node for PRZM
C     IPRZM  - current przm zone
C     ITSAFT - current time step
C     NLDLT  - maximum days in a time step (31)
C
C     +  +  + PARAMETERS +  +  +
C
      INCLUDE 'PPARM.INC'
      INCLUDE 'PMXPDT.INC'
      INCLUDE 'PMXNSZ.INC'
      INCLUDE 'PMXZON.INC'
C
C     +  +  + COMMON BLOCKS +  +  +
C
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CPRZST.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CECHOT.INC'
      INCLUDE 'CPTAP.INC'
      INCLUDE 'CFILEX.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'EXAM.INC'
      INCLUDE 'CNITR.INC'
C
C     +  +  + LOCAL VARIABLES +  +  +
C
      INTEGER      J,I,LDAY,FDAY,JP1,MNTHP1,EYRFG,
     1             K, NMCDAY,LPAD
      INTEGER      FLPS,FLCN
      REAL         ATEMP(2),PWIND(2),R0,
     1             OLDKH(NCMPTS),ZCH,TOTCR
      Real         z0, d, urh, uch
      REAL*8       DKBIO(3,NCMPTS)
      CHARACTER*4  YEAR,MNTH,DAY,CONC
      INTEGER      ILDLT,IERROR
      LOGICAL      MCTFLG,IRDAY,FATAL
      CHARACTER*80 MESAGE
C
C     +  +  + INTRINSICS  +  +  +
C
      INTRINSIC MOD
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,RSTGET,RSTGT1,KHCORR,ACTION,GETMET,PLGROW
      EXTERNAL IRRIG,HYDROL,EVPOTR,HYDR1,HYDR2,EROSN,SLTEMP,FARM
      EXTERNAL PZSCRN,PESTAP,PLPEST,BIODEG,SLPST0,SLPST1
      EXTERNAL MOC,MASBAL,OUTCNC,OUTRPT,OUTPST,OUTHYD,OUTTSR
      EXTERNAL MCPRZ,RSTPUT,RSTPT1,SUBOUT,PRZEXM,ERRCHK
      EXTERNAL SEPTIN,NITR,NITRAP,NITBAL,OUTCNI,OUTNIT,ZIPR
C
C     +  +  + DATA INITIALIZATIONS +  +  +
C
      DATA YEAR /'YEAR'/
      DATA MNTH /'MNTH'/
      DATA DAY  /' DAY'/
      DATA CONC /'CONC'/
C
C     +  +  + OUTPUT FORMATS +  +  +
2000  FORMAT('Application [',I3,'] chem [',I1,
     1      '] on julday [',I3,'] year [',I2,'] zone [',I2,']')
2001  FORMAT('Application [',I3,'] chem [',I1,
     1      '] on julday [',I3,'] year [',I2,'] zone [',I2,']')
2002  FORMAT('ERROR, Application [',I3,'] failed ideal soil conditions')
2010  FORMAT('Nitrogen application [',I3,'] on julday [',I3,'] year [',
     $       I2,'] zone [',I2,']')
2020  FORMAT('ERROR, Nitrogen application [',I3,'] failed ideal soil ',
     $       'conditions')
C
C     +  +  + END SPECIFICATIONS +  +  +
C
      R0 = 0.0
      APPLY = .FALSE.
      MESAGE = 'PRZM'
      CALL SUBIN(MESAGE)
C     get unit numbers used for input and output
      FLPS= LPRZOT
      FLCN= LPRZOT
C
C     in restart mode
      IF(IPRZM.NE.1)THEN
        CALL RSTGET (LPRZRS,IPRZM)
        CALL RSTGT1 (RSTFG,LPRZRS,IPRZM)
      ENDIF
C
C     use dates passed as input rather than on input file
      ISTYR = RSDAT(1)
      ISMON = RSDAT(2)
      ISDAY = RSDAT(3)
      IEYR  = REDAT(1)
      IEMON = REDAT(2)
      IEDAY = REDAT(3)
      !jd_today = Jd(yyyy=ISTYR+iybase, mm=ISMON, dd=ISDAY) ! m_debug
C
C     check temperature simulation flag
      IF (ITFLAG .EQ. 1) THEN
        DO 178 K=1,NCHEM
          CALL KHCORR(SPT,HENRYK(K),ENPY(K),NCOM2,OLDKH)
          DO 177 I=1,NCOM2
            OKH(K,I) = OLDKH(I)
177       CONTINUE
178     CONTINUE
      ELSE
        DO 189 K=1,NCHEM
          DO 188 I=1,NCOM2
            OKH(K,I)   = HENRYK(K)
            KH(K,I)    = HENRYK(K)
188       CONTINUE
189     CONTINUE
      ENDIF
C
      NMCDAY = (ITSAFT-1)*NLDLT
      DO 200 IY=ISTYR,IEYR
        IF (MOD(IY,4) .NE. 0 .OR. MOD(IY,100) .EQ. 0) THEN
          LEAP=1
          LDAY=365
        ELSE
          LEAP=2
          LDAY=366
        ENDIF
        IF (IY .EQ. IEYR) LDAY=IEDAY+CNDMO(LEAP,IEMON)
C
        FDAY=1
        IF (IY .EQ. ISTYR)THEN
          FDAY=ISDAY+CNDMO(LEAP,ISMON)
        ENDIF
C
        EYRFG = 0
C
C       counter for VADOFT link
        ILDLT = 0
C       set input accumulator for GLOMAS
CJMC determine time period for each decay rate if DK2FLG=1
        DO 39 K = 1,NCHEM
          IF(DK2FLG.EQ.1)THEN
            DKSTRT(K)=DKDAY(K)+CNDMO(LEAP,DKMNTH(K))
            DKEND(K)=DKSTRT(K)+DKNUM(K)
            IF(DKEND(K).GT.365)DKEND(K)=DKEND(K)-LDAY
          ENDIF
          PTAP(K) = 0.
  39    CONTINUE
C
C       begin daily loop
        DO 100 JULDAY=FDAY,LDAY
!          Write (802, *) 'DO 100 JULDAY, FDAY,LDAY = ',  ! m_debug
!     &                   JULDAY, FDAY,LDAY ! m_debug
          NMCDAY = NMCDAY + 1
          ILDLT = ILDLT + 1
          IF (JULDAY .EQ. LDAY) THEN
            EYRFG = 1
          ENDIF
          IF (LEAP .EQ. 2 .AND. DAYCNT .EQ. 366) DAYCNT = 0
          IF (LEAP .EQ. 1 .AND. DAYCNT .EQ. 365) DAYCNT = 0
          DAYCNT = DAYCNT + 1
C
          DO 40 J=1,12
            JP1= J+ 1
            IF (JULDAY.GT.CNDMO(LEAP,J) .AND.
     1         JULDAY.LE.CNDMO(LEAP,JP1)) MONTH = J
40        CONTINUE
          DOM=JULDAY-CNDMO(LEAP,MONTH)
          MNTHP1 = MONTH + 1
          SSFLAG = 0
          IF (IY.EQ.SAYR .AND. JULDAY.EQ.SAVAL) THEN
C           time for a special action
            CALL ACTION (LPRZIN,LPRZOT,MODID(3))
          END IF
C         get met data
          CALL GETMET(
     I      IY,JULDAY,MONTH,DOM,LMETEO,LSPTIC,LNITAD,FWDMS,
     I      LDAY,RSTFG,NITRON,SEPTON,
     O      RETCOD)
!          Write (802, *) '   Met data for IY,JULDAY,MONTH,DOM,LDAY = ',
!     &                   IY,JULDAY,MONTH,DOM,LDAY ! m_debug

C         grow some crops
          CALL PLGROW(IRDAY)
!          Write (802, *) '   Call PLGROW(IRDAY), IRDAY = ', IRDAY  ! m_debug
C
          APDEP  = 0.0
          AINF(1)= 0.0
          THRUFL = 0.0
          really_not_thrufl = .FALSE.
          IRRR = 0.0
          IF (IRTYPE .GT. 0 .AND. IRNONE .NE. 4 .AND. RZI .EQ. 1) THEN
C           need to do irrigation
            CALL IRRIG
          ELSE
            IF (IRNONE .EQ. 4) THEN
              IF (IRDAY) THEN
                CALL IRRIG
              ELSE
                GOTO 555
              ENDIF
            ENDIF
          ENDIF
C
C         calculate surface hydrology factors
c ! m_debug -- IUSLEC
555   CONTINUE
          IF(ERFLAG.GT.0)THEN
            IF(LEAP.EQ.1)THEN
              IF(UCFLG.EQ.0)THEN
                CFAC=USLEC(NCROP,IUSLEC)
                N1=MNGN(NCROP,IUSLEC)
                ISCOND=IUSLEC
                IF(JULDAY.EQ.JUSLEC(NCROP,IUSLEC))THEN
                  UCFLG=2
                  IUSLEC=IUSLEC+1
                ENDIF
              ELSEIF(UCFLG.EQ.1)THEN
                CFAC=USLEC(NCROP,IUSLEC)
                N1=MNGN(NCROP,IUSLEC)
                ISCOND=IUSLEC
                IF(JULDAY.EQ.JUSLEC(NCROP,IUSLEC))THEN
                  UCFLG=2
                  IUSLEC=IUSLEC+1
                ENDIF
              ELSE
                IF(JULDAY.EQ.(JUSLEC(NCROP,IUSLEC)))THEN
                  CFAC=USLEC(NCROP,IUSLEC)
                  N1=MNGN(NCROP,IUSLEC)
                  ISCOND=IUSLEC
                  IUSLEC=IUSLEC+1
                  IF(IUSLEC.GT.NUSLEC(NCROP))IUSLEC=1
                ENDIF
              ENDIF
            ELSE
              LPAD=0
              IF(UCFLG.EQ.0)THEN
                CFAC=USLEC(NCROP,IUSLEC)
                N1=MNGN(NCROP,IUSLEC)
                IF(JULDAY.GT.59)LPAD=1
                ISCOND=IUSLEC
                IF(JULDAY.EQ.JUSLEC(NCROP,IUSLEC)+LPAD)THEN
                  UCFLG=2
                  IUSLEC=IUSLEC+1
                ENDIF
              ELSEIF(UCFLG.EQ.1)THEN
                CFAC=USLEC(NCROP,IUSLEC)
                N1=MNGN(NCROP,IUSLEC)
                IF(JULDAY.GT.59)LPAD=1
                ISCOND=IUSLEC+1
                IF(JULDAY.EQ.JUSLEC(NCROP,IUSLEC)+LPAD)THEN
                  UCFLG=2
                  IUSLEC=IUSLEC+1
                ENDIF
              ELSE
                IF(JULDAY.GT.59)LPAD=1
                IF(JULDAY.EQ.(JUSLEC(NCROP,IUSLEC))+LPAD)THEN
                  CFAC=USLEC(NCROP,IUSLEC)
                  N1=MNGN(NCROP,IUSLEC)
                  ISCOND=IUSLEC
                  IUSLEC=IUSLEC+1
                  IF(IUSLEC.GT.NUSLEC(NCROP))IUSLEC=1
                ENDIF
              ENDIF
            ENDIF
          ENDIF
          CALL HYDROL (LPRZOT,MODID(3),RODPTH,CURVN)
C
C         calculate et
          CALL EVPOTR
C
          IF (SEPTON) THEN
C           introduce septic effluent into soil column
            CALL SEPTIN
          END IF
C
          IF (HSWZT .EQ. 0) THEN
C           hydraulics with unrestricted drainage
            CALL HYDR1
          ELSEIF (HSWZT .EQ. 1) THEN
C           hydraulics with restricted drainage
            CALL HYDR2
          ENDIF
C
c
          SEDL= 0.0
          ELTT= 0.0
          IF (RUNOF .GT. 0.0 .AND. ERFLAG .GE. 1) THEN
C           calc loss of chem due to erosion
            CALL EROSN
          END IF
C
CJMC
          IF(DK2FLG.EQ.1)THEN
            CALL DKINIT
          ENDIF
CJMC
          IF (NITRON) THEN
C           perform nitrogen simulation
            CALL SLTEMP (LPRZOT,MODID(3))
            CALL ZIPR (3*NCOM2,R0,SOILAP)
            IF (JULDAY.EQ.IAPDY(NAPPC) .AND. IY.EQ.IAPYR(NAPPC)) THEN
C             need to perform ag nitrogen application
              IF ((FRMFLG .GE. 1).AND.(FRMFLG.LE.3)) THEN
C               check for appropriate soil moisture
                CALL FARM (RODPTH,APPLY,CURVN)
                IF (APPLY) THEN
C                 make ag nitrogen application
                  WRITE(MESAGE,2010) NAPPC,IAPDY(NAPPC),
     $                               IAPYR(NAPPC),IPRZM
                  CALL PZSCRN(1,MESAGE)
                  CALL NITRAP (FECHO)
                  NAPPC= NAPPC+ 1
                  WIN  = 0
                ELSE
C                 soil moisture not right for application, try again tomorrow
                  WIN = WIN + 1
                  IF (WIN .GT. WINDAY(NAPPC)) THEN
C                   beyond window of opportunity
                    WRITE(MESAGE,2020) NAPPC
                    IERROR= 2150
                    FATAL = .TRUE.
                    CALL ERRCHK(IERROR,MESAGE,FATAL)
                  ELSE
C                   try to apply tomorrow
                    IAPDY(NAPPC) = IAPDY(NAPPC) + 1
                  ENDIF
                ENDIF
              ELSE
                WRITE(MESAGE,2010) NAPPC,IAPDY(NAPPC),
     $                             IAPYR(NAPPC),IPRZM
                CALL PZSCRN(1,MESAGE)
                CALL NITRAP (FECHO)
                NAPPC= NAPPC+ 1
              ENDIF
            ENDIF
            IF (MCARLO) THEN
              CALL NITR (IY,MONTH,DOM,FECHO,IPRZM,MODID(13))
            ELSE
              CALL NITR (IY,MONTH,DOM,LPRZOT,IPRZM,MODID(13))
            END IF
C           perform mass balance for nitrogen constituents
            CALL NITBAL (APDEP,IPRZM)
            IF (ECHOLV .GE. 3) THEN
              CALL OUTHYD (LPRZOT,LTMSRS,MODID(3),MODID(5),SEPTON)
              IF (ITEM3 .EQ. CONC .AND. (STEP3 .EQ. DAY .OR. (STEP3
     1          .EQ. MNTH .AND. JULDAY .EQ. CNDMO(LEAP,MNTHP1)) .OR.
     2          (STEP3 .EQ. YEAR .AND. JULDAY .EQ. CNDMO(LEAP,13)))
     3          .AND. FLCN.GT.0) CALL OUTCNI (LPRZOT,MODID(6))
              CALL OUTNIT (FLPS,MODID(13),SEPTON)
              IF (NPLOTS .GT. 0) THEN
C               output time-series
                HEADER = HEADER + 1
                IF (HEADER .EQ. 1) SRNFG = 1
                CALL OUTTSR (SRNFG,EYRFG,LPRZOT,LTMSRS,LWDMS,
     I                       MODID(3),MODID(5),HEIGHT)
              ENDIF
            ENDIF
C           store PRZM nitrogen fluxes for vadoft, start w/ammonia
            PRZMPF(IPRZM,ILDLT,1) = PRZMPF(IPRZM,ILDLT,1) +
     $                              NCFX2(BASEND,1)/1.0E5
C           nitrate
            PRZMPF(IPRZM,ILDLT,2) = PRZMPF(IPRZM,ILDLT,2) +
     $                              NCFX4(BASEND,1)/1.0E5
C           combine the two organic species
            PRZMPF(IPRZM,ILDLT,3) = PRZMPF(IPRZM,ILDLT,3) +
     $                              (NCFX13(BASEND,1) +
     $                               NCFX15(BASEND,1))/1.0E5
          ELSE
C           perform pesticide simulation
            DO 95 K=1, NCHEM
              ELTERM(K) = ELTT*KD(K,1)
              DO 74 I=1,NCOM2
                SOILAP(K,I) = 0.0
                DKBIO(K,I)  = 0.0
74            CONTINUE
C
              Select Case(ITFLAG)
              Case(1, 2)
                  IF (K == 1) Then
                     CALL SLTEMP (LPRZOT,MODID(3))
                     IF (QFAC(K) > 0.0) Then
                        CALL Q10DK
                     Else
                        If (DK2FLG == 1) Call DKINIT
                     End If
                  End If
                  CALL KHCORR (SPT,HENRYK(K),ENPY(K),NCOM2,OLDKH)
                  KH(K,1:NCOM2) = OLDKH(1:NCOM2)

              Case Default
                  If ((K == 1) .And. (DK2FLG == 1)) Call DKINIT
              End Select
C
              PLNTAP(K) = 0.0
C
              IF (JULDAY.EQ.IAPDY(NAPPC) .AND. IY.EQ.IAPYR(NAPPC))THEN
                IF ((FRMFLG .GE. 1).AND.(FRMFLG.LE.3)) THEN
C                 added new statement for farm option -jam 4/24/91
                  CALL FARM (RODPTH,APPLY,CURVN)
                  IF (APPLY) THEN
                    WRITE(MESAGE,2000) NAPPC,K,IAPDY(NAPPC),
     $                                 IAPYR(NAPPC),IPRZM
                    CALL PZSCRN(1,MESAGE)
                    CALL PESTAP(K)
                    PTAP(K) = PTAP(K) +
     *                        (TAPP(K,NAPPC)*APPEFF(K,NAPPC))-PLNTAP(K)
                  ENDIF
                ELSE
                  WRITE(MESAGE,2001) NAPPC,K,IAPDY(NAPPC),
     $                               IAPYR(NAPPC),IPRZM
                  CALL PZSCRN(1,MESAGE)
                  CALL PESTAP(K)
C                 global mass balance
                  PTAP(K) = PTAP(K) +
     *                      (TAPP(K,NAPPC)*APPEFF(K,NAPPC))-PLNTAP(K)
                ENDIF
              ENDIF
C
c jmc 6/17/96 fam=2 signifies that some applications were foliar
              IF (FAM.EQ.2)CALL PLPEST(K)
C
              ! CNDBDY: Boundary Layer's Conductance (cm day^-1) = 1/Rdb
              ! Rdb:    Boundary layer resistance (day/cm) = d / Dair,
              ! d:      Height of the stagnant air layer above the soil
              ! Dair:   Molecular Diffusivity in air (cm^2 day^-1)
              CNDBDY(K) = DAIR(K) / Height_stagnant_air_layer_cm

              ! CONDUC: Canopy Conductance Including Boundary Layer's Conductance (cm day^-1)
              CONDUC(K) = CNDBDY(K)
C
C             When canopy develops, resistance type approach is used
C             to estimate the volatilization flux and concentration
C             retains in the canopy
C
c HEIGHT: Canopy height (cm)

              IF (HEIGHT .GT. Minimum_Canopy_Height_cm) THEN
                ZCH = HEIGHT/100.0     ! convert to meter
                IF (ITFLAG .EQ. 0) THEN
                  ATEMP(1)= 15.0
                ELSE
                  ATEMP(1)= UBT
                ENDIF
                ATEMP(2)= TEMP

               ! Let u_2 and u_1 be wind speeds measured at
               ! heights z_2 and z_1 respectively. Then
               !
               !        u_2                    u_1
               ! ------------------  =  ------------------
               ! Ln((z_2-d_2)/z0_2)     Ln((z_1-d_1)/z0_1)
               !
               ! where
               !     u_i : wind speed at height z_i
               !     z_i : height at which the measurement was taken (m)
               !     d_i : zero plane displacement (m)
               !     z0_i: surface roughness length or roughness height (m)
               !
               ! This equation assumes the atmosphere is neutrally stable,
               ! i.e., phi_m = 1, which implies psi_m = 0.
               !
               ! Given the wind speed at reference conditions (urh), compute
               ! the wind speed at the top of the canopy (uch). Assume the
               ! atmosphere is neutrally stable.
               !
               ! The wind speed at reference conditions (urh) is retrieved from the
               ! metereological file. The aerodynamic parameters for wind speed
               ! computations are set by the subroutine Get_Aerodynamic_Parameters.
               ! In the absence of przm input file values, the routine assumes
               ! the conditions of the meteorological Daily Values File (*.dvf),
               ! i.e., Open Flat Terrain (used for Metereological Stations), and
               ! wind measurements normalized to 10 meters.
               ! See subroutines IniVar and Get_Aerodynamic_Parameters.
               !   Wind_Reference_Height = 10.0
               !   Wind_z0 = 0.03
               !   Wind_D  = 0.0

               ! Computes zero displacement height, D (meter)
               ! and the roughness length, Z0 (meter)
               Call Get_Crop_Params (zch, z0, d)

                ! urh: wind speed (meter/day) at reference height.
                !      units of WIND are cm/sec.
                !      1 cm/sec is equivalent to 864.0 meter/day
                !      subroutine canopy expects wind speed in meter/day
                ! uch: wind speed at the top of the canopy (zch)

                urh = WIND * 864.0
                uch = urh * Log((zch-d)/z0) /
     &                Log((uWind_Reference_Height-uWind_D)/uWind_z0)

                PWIND(1)= 0.0
                PWIND(2)= uch

C
C               CONDUC was being calculated after the following
C               if then statement.  It should be calculated right
C               after the call CANOPY statement.  Change made by
C               PV @ AQUA TERRA Consultants, 10/93
C
                IF(HENRYK(K).GT.0.0.AND.URH.GT.0.0)THEN
                  CALL Canopy(ATEMP,PWIND,ZCH,TOTCR,CRCNC)
                  ! CNDBDY: Boundary Layer's Conductance (cm/day)
                  ! CONDUC: Canopy Conductance Including Boundary Layer's Conductance (cm/day)
                  ! TOTCR:  Total canopy resistance (cm/day)
                  CONDUC(K) = 1.0 / (1.0/CNDBDY(K) + TOTCR)
                ELSE
                  TOTCR=0.0
                ENDIF
C                CONDUC(K) = 1.0 / (1.0/CNDBDY(K) + TOTCR)
              ENDIF
C
C             Include calls to biodegradation subroutines here
C
              IF (BIOFLG .EQ. 1) THEN
                CALL BIODEG(K,DKBIO)
              ENDIF
C
C             end of biodegradation
C
              IF (MCFLAG.EQ.0 .OR. VLFLAG.EQ.0) THEN
                CALL SLPST0 (LPRZOT, MODID(3), K, DKBIO)
              ELSE
                CALL MOC(K)
                CALL SLPST1 (LPRZOT,MODID(3),K, DKBIO)
              END IF
C
C             calculate correction for dissolved to total solute conc.
              CALL MASBAL (APDEP,K,IPRZM,IRTYPE,IRRR)
C
              CALL FCSCNC(K)
              CALL FCSMSB(K)
              CALL FCSHYD(K)
C
              IF (MCOFLG .EQ. 0 .AND. ECHOLV .GE.3) THEN
C
                IF (ITEM3 .EQ. CONC .AND. (STEP3 .EQ. DAY .OR. (STEP3
     1            .EQ. MNTH .AND. JULDAY .EQ. CNDMO(LEAP,MNTHP1)) .OR.
     2            (STEP3 .EQ. YEAR .AND. JULDAY .EQ. CNDMO(LEAP,13)))
     3            .AND. FLCN.GT.0) CALL OUTCNC (LPRZOT,MODID(6),K)
C
C               Determine if a write to files MODOUT.DAT or SNAPSHOT.DAT
C               is required
                CALL OUTRPT (LPRZOT,MODID(7),MODID(8),K)
              ENDIF
C
              IF (ECHOLV .GE. 3) THEN
                IF (K .EQ. 1) CALL OUTHYD (
     I                           LPRZOT,LTMSRS,MODID(3),MODID(5),SEPTON)
                CALL OUTPST (
     I                       FLPS,MODID(4),K)
              ENDIF
              PRZMPF(IPRZM,ILDLT,K) = PRZMPF(IPRZM,ILDLT,K) +
     1          DFFLUX(K,BASEND) + ADFLUX(K,BASEND)
CPRH              DAFLUX(IPRZM,1,ILDLT,K) = DFFLUX(K,1) + ADFLUX(K,1) +
CPRH   1            PVFLUX(K,1)
C
              DO 90 I=1,NCOM2
CPRH                DAFLUX(IPRZM,I+1,ILDLT,K) = DFFLUX(K,I) + ADFLUX(K,I) +
CPRH   1              PVFLUX(K,I)
                SPESTR(K,I)=X(I)
C
C               store SPESTR for this zone (for use w/ MASCOR)
                PESTR(K,I)=SPESTR(K,I)*(THETN(I)+KD(K,I)*BD(I)+
     1                   (THETAS(I)-THETN(I))*KH(K,I))/THETN(I)
90            CONTINUE
C
C             last value of DAFLUX and ZPESTR is same as
C             in last compartment
CPRH              DAFLUX(IPRZM,NCOM2+2,ILDLT,K) = DFFLUX(K,NCOM2) +
CPRH   1            ADFLUX(K,NCOM2) + PVFLUX(K,NCOM2)
C
              IF (NPLOTS .GT. 0 .AND. K .EQ. NCHEM) THEN
                 HEADER = HEADER + 1
                 IF (HEADER .EQ. 1) SRNFG = 1
                 IF(ECHOLV .GE.3)CALL OUTTSR
     1             (SRNFG,EYRFG,LPRZOT,LTMSRS,LWDMS,MODID(3),MODID(5),
     2              HEIGHT)
              ENDIF
C
C             new code added for EXAMS
              IF (ERFLAG.GT.0 .AND. IPRZM.EQ.1) THEN
                IF ((EXMFLG.GT.0) .AND. (K.EQ.NCHEM)) CALL PRZEXM(K)
              ENDIF
C             end of code added for EXAMS
C
              SRNFG = 0
              IF (ITFLAG .EQ. 1) THEN
                DO 92 I=1,NCOM2
                  OKH(K,I) = KH(K,I)
92              CONTINUE
              ENDIF
95          CONTINUE
            IF ((FRMFLG .GE. 1).AND.(FRMFLG.LE.3)) THEN
              IF (APPLY) THEN
                IF (JULDAY.EQ.IAPDY(NAPPC) .AND.
     $                  IY.EQ.IAPYR(NAPPC)) THEN
                  NAPPC= NAPPC+ 1
                  WIN = 0
                ENDIF
              ELSE
                IF (JULDAY.EQ.IAPDY(NAPPC) .AND.
     $                  IY.EQ.IAPYR(NAPPC)) THEN
                  WIN = WIN + 1
                  IF (WIN .GT. WINDAY(NAPPC)) THEN
                    WRITE(MESAGE,2002)NAPPC
                    IERROR = 2150
                    FATAL = .TRUE.
                    CALL ERRCHK(IERROR,MESAGE,FATAL)
                  ELSE
                    IAPDY(NAPPC) = IAPDY(NAPPC) + 1
                  ENDIF
                ENDIF
              ENDIF
            ELSE
              IF (JULDAY.EQ.IAPDY(NAPPC) .AND. IY.EQ.IAPYR(NAPPC))THEN
                NAPPC= NAPPC+ 1
              ENDIF
            ENDIF
          END IF
C
C         water flux to EXESUP
          PRZMWF(IPRZM,ILDLT) = PRZMWF(IPRZM,ILDLT) + AINF(BASEND)
C
C         transfer results to Monte Carlo arrays
          IF(MCARLO) THEN
            MCTFLG = .TRUE.
            CALL MCPRZ(
     I        MCTFLG,IPRZM,NMCDAY)
          ENDIF
C
100     CONTINUE
200   CONTINUE
      IF(IPRZM.NE.1)THEN
        IF (RSTFG .EQ. 1 .OR. RSTFG .EQ. 2) THEN
C
C         Save state of system for next execution
          CALL RSTPUT (LPRZRS,IPRZM)
          CALL RSTPT1 (LPRZRS,IPRZM)
        ENDIF
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   KHCORR
     I                   (STEMP,HENRY,ENP,NUMB,
     O                    NEWK)
C
C     + + + PURPOSE + + +
C     to correct Henry's constant using Clausius-Clapeyron equation
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   NUMB
      REAL      STEMP(NUMB),NEWK(NUMB)
      REAL      HENRY,ENP
C
C     + + + ARGUMENT DEFINITIONS + + +
C     NUMB  - ???
C     STEMP - ???
C     NEWK  - ???
C     HENRY - ???
C     ENP   - ???
C
C     + + + LOCAL VARIABLES + + +
      REAL      TMPK,TCORR,HENRY2
      INTEGER   I
C
C     + + + INTRINSICS + + +
      INTRINSIC LOG10
C
C     + + + END SPECIFICATIONS + + +
C
      IF (HENRY .GT. 0.0) THEN
C       perform corrections
        DO 10 I=1, NUMB
          TMPK=273.16+STEMP(I)
          TCORR=(298.16-TMPK)/(298.16*TMPK)/(2.302585*1.98718)
          HENRY2=LOG10(HENRY)
          NEWK(I)=HENRY2-1000.0*ENP*TCORR
          NEWK(I)=10**NEWK(I)
 10     CONTINUE
      ELSE
C       not a valid Henry's value, don't correct
        DO 20 I = 1,NUMB
          NEWK(I) = 0.0
 20     CONTINUE
      END IF
C
      RETURN
      END
C
C
C
C
      SUBROUTINE   ACTION (LPRZIN,LPRZOT,MODID)
C
C     + + + PURPOSE + + +
C     identifies any special actions requested in the przm input file
C     Modification date: 2/14/92 JAM
C
      Use m_CN_functions
      Use m_Debug   ! m_debug

C     + + + DUMMY ARGUMENTS + + +
      INTEGER     LPRZIN,LPRZOT
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZIN - ???
C     LPRZOT - ???
C     MODID  - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
C
C     + + + LOCAL VARIABLES + + +
      DIMENSION    ACTS(7)
      INTEGER      MATCH,I,J,JP1,FLAG,SALEAP,JCOM
      CHARACTER*8  ACTS
      CHARACTER*80 MESAGE
C
C     +  +  + INTRINSICS +  +  +
C
      INTRINSIC NINT,MOD
C
C     +  +  + EXTERANLS +  +  +
C
      EXTERNAL SUBIN,SUBOUT
C
C     +  +  + DATA INITIALIZATIONS +  +  +
C
      DATA  ACTS / 'BD      ','CN      ','DSRATE  ','DWRATE  ',
     1       'KD      ','SNAPSHOT','USLEC   ' /
C
C     + + + OUTPUT FORMATS + + +
1000  FORMAT (1X,A3,/,1X,A3,1X,100(1H*),/,1X,A3,/,1X,A3,10X,
     1        'THE SPECIAL ACTION CALLED ''',A8,
     2        ''' DOES NOT EXIST FOR JULIAN DATE ',I3,',',I4,
     2          '.',/,1X,A3,/,1X,A3,1X,100(1H*))
1010  FORMAT (2X,3I2,1X,A8,1X,I3,3F8.0)
1020  FORMAT (1X,A3,/,1X,A3,1X,100(1H*),/,1X,A3,/,1X,A3,10X,
     1        'ERROR UPON A SPECIAL ACTION READ, VALUES DISPLAYED ',
     2        'BELOW:',/,1X,A3,/,1X,A3,10X,3I2,4X,A8,4X,I4,3G10.4,
     3        /,1X,A3,/,1X,A3,1X,100(1H*))
1030  FORMAT (1X,A3,/,1X,A3,1X,100(1H*),/,1X,A3,/,1X,A3,10X,
     1        'A SPECIAL ACTION READ FOUND DATES OUT OF ORDER, ',
     2        'VALUES DISPLAYED BELOW:',/,1X,A3,/,1X,A3,10X,3I2,4X,
     3        A8,4X,I4,3G10.4,/,1X,A3,/,1X,A3,10X,
     4        'CURRENT YEAR/JULIAN DATE: ',I2,'/',I3,
     4          '   NOT JULIAN DATE: ',I3,/,1X,A3,/,1X,A3,1X,100(1H*))
1040  FORMAT (1X,A3,/,1X,A3,1X,100(1H*),/,1X,A3,/,1X,A3,10X,3I2,4X,
     1        'THE VARIABLE ',A8,' CAN NOT USE A DIMENSION OF ',I4,
     2        /,1X,A3,/,1X,A3,1X,100(1H*))
1050  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,1X,20A4,/)
1060  FORMAT (1X,A3,/,1X,A3,4X,3I2,'  VARIABLE ',A8,' FOR HORIZON #',
     1          I3,' NOW HAS A VALUE OF ',G10.4)
1061  FORMAT (1X,A3,/,1X,A3,4X,3I2,'  VARIABLE ',A8,' FOR HORIZON #',
     1          I3,' NOW HAS VALUES OF ',3G10.4)
1070  FORMAT (1X,A3,/,1X,A3,4X,3I2,'  VARIABLE ',A8,' FOR CROP #',I3,
     1          ' NOW HAS VALUES OF ',3I8)
1080  FORMAT (1X,A3,/,1X,A3,4X,3I2,'  VARIABLE ',A8,' FOR CROP #',I3,
     1          ' NOW HAS VALUES OF ',3G10.4)
1090  FORMAT (1X,A3,/,1X,A3,4X,3I2,'  SNAPSHOT REQUESTED')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'ACTION'
      CALL SUBIN(MESAGE)
C     assign values in temporary locations
      FLAG   = 0
   4  IF  (SAYR - IY)     820, 6,900
   6  IF (SAVAL - JULDAY) 820,10,900
C
  10  CONTINUE
C     determine which special action was requested
      DO 200 MATCH = 1, 7
        IF (ACTS(MATCH) .EQ. SPACT) THEN
C
C         we have a match for a variable
          IF (MATCH .EQ. 1) THEN
C
C           match for the variable BD
            IF (NACTS .LT. 1 .OR. NACTS .GT. NHORIZ) GO TO 260
            DO 113 JCOM = NCOMBE(NACTS),NCOMEN(NACTS)
              BD(JCOM) = SPACTS(1)
  113       CONTINUE
            I = MATCH
            GO TO 210
          ELSEIF (MATCH .EQ. 2) THEN
C
C           match for the variable CN
            IF (NACTS .LT. 1 .OR. NACTS .GT. NDC) GO TO 260
            call Fill_CN_Array()
            DO I = 1, 3
               CN(NACTS,I,2) = NINT(SPACTS(I))
               CN(NACTS,I,1) = cn_1_func(CN(NACTS,I,2))
               CN(NACTS,I,3) = cn_3_func(CN(NACTS,I,2))
            End Do
            I = MATCH
            GO TO 210
C
          ELSEIF (MATCH .EQ. 3) THEN
C           match for the variable DSRATE
            IF (NACTS .LT. 1 .OR. NACTS .GT. NHORIZ) GO TO 260
            DO 114 JCOM = NCOMBE(NACTS),NCOMEN(NACTS)
              DO 51 I = 1, NCHEM
                DSRATE(I,JCOM) = SPACTS(I)
   51         CONTINUE
  114       CONTINUE
            I = MATCH
            GO TO 210
C
          ELSEIF (MATCH .EQ. 4) THEN
C           match for the variable DWRATE
            IF (NACTS .LT. 1 .OR. NACTS .GT. NHORIZ) GO TO 260
            DO 116 JCOM = NCOMBE(NACTS),NCOMEN(NACTS)
              DO 52 I = 1, NCHEM
                DWRATE(I,JCOM) = SPACTS(I)
  52          CONTINUE
  116       CONTINUE
            I = MATCH
            GO TO 210
C
          ELSEIF (MATCH .EQ. 5) THEN
C           match for the variable KD
            IF (NACTS .LT. 1 .OR. NACTS .GT. NHORIZ) GO TO 260
            DO 117 JCOM = NCOMBE(NACTS),NCOMEN(NACTS)
              DO 47 I= 1, NCHEM
                KD(I,JCOM) = SPACTS(I)
  47          CONTINUE
  117       CONTINUE
            I = MATCH
            GO TO 210
C
          ELSEIF (MATCH .EQ. 6) THEN
C           match for the variable SNAPSHOT
            SSFLAG = 1
            I = MATCH
            GO TO 210
C
          ENDIF
        ENDIF
 200  CONTINUE
      IF (MCOFLG .EQ. 0) THEN
        WRITE(LPRZOT,1000) (MODID,J=1,4),SPACT,SAVAL,SAYR,
     1                   (MODID,J=1,2)
      ENDIF
      GO TO 220
C
C     write a summary of changes made
 210  CONTINUE
      IF (MCOFLG .EQ. 0) THEN
        IF (FLAG .EQ. 0) WRITE(LPRZOT,1050) (MODID,J=1,5),ATITLE
      ENDIF
      FLAG = 1
      IF (MCOFLG .EQ. 0) THEN
        IF (I .EQ. 2) THEN
          WRITE(LPRZOT,1070) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,NACTS,
     1                     (CN(NACTS,JP1,2),JP1=1,3)
C          WRITE(LPRZOT,1075) ((MODID,CN(NACTS,JP1,J),J=1,3),JP1=1,3)
        ELSEIF (I .EQ. 7) THEN
          WRITE(LPRZOT,1080) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,
     1                      NACTS,(SPACTS(I),I=1,3)
        ELSEIF (I .EQ. 3) THEN
          WRITE(LPRZOT,1061) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,
     1                      NACTS,(SPACTS(I),I=1,3)
        ELSEIF (I .EQ. 4) THEN
          WRITE(LPRZOT,1061) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,
     1                      NACTS,(SPACTS(I),I=1,3)
        ELSEIF (I .EQ. 5) THEN
          WRITE(LPRZOT,1061) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,
     1                      NACTS,(SPACTS(I),I=1,3)
        ELSEIF (I .EQ. 6) THEN
          WRITE(LPRZOT,1090) (MODID,J=1,2),SADAY,SAMON,SAYR
        ELSE
          WRITE(LPRZOT,1060) (MODID,J=1,2),SADAY,SAMON,SAYR,SPACT,
     1                      NACTS,SPACTS(1)
        ENDIF
      ENDIF
C
C     read the next special action in
 220  CONTINUE
      READ(LPRZIN,1010,END=240,ERR=800)
     1        SADAY,SAMON,SAYR,SPACT,NACTS,(SPACTS(I),I=1,3)
C
C     modification to correct for leap year
      SALEAP=1
      IF(MOD(SAYR,4).EQ.0) SALEAP=2
      SAVAL=SADAY+CNDMO(SALEAP,SAMON)
C
C     end change
      GO TO 4
C
C     end of file encountered,
C     set special action's date artificially high
 240  SAVAL = 9999
      SAYR  = 9999
      GO TO 900
C
C     the variable NACTS contains an unacceptable range
 260  IF (MCOFLG .EQ. 0) THEN
        WRITE(LPRZOT,1040) (MODID,J=1,4),SADAY,SAMON,SAYR,SPACT,NACTS,
     1                   (MODID,J=1,2)
      ENDIF
      GO TO 220
C
C     error reading data in
C     display error message and read next value in
 800  IF (MCOFLG .EQ. 0) THEN
        WRITE(LPRZOT,1020) (MODID,J=1,6),SADAY,SAMON,SAYR,SPACT,
     1                    NACTS,SPACTS,(MODID,J=1,2)
      ENDIF
      GO TO 220
C
 820  IF (MCOFLG .EQ. 0) THEN
        WRITE(LPRZOT,1030) (MODID,J=1,6),SADAY,SAMON,SAYR,SPACT,
     1                    NACTS,SPACTS,(MODID,J=1,2),IY,JULDAY,SAVAL,
     2                    (MODID,J=1,2)
      ENDIF
      GO TO 220
C
C     return to calling program
 900  CONTINUE
      CALL SUBOUT
      RETURN
C
      END
C
C
C
      SUBROUTINE   GETMET
     I                   (IY,JULDAY,MONTH,DOM,LMETEO,LSPTIC,LNITAD,
     I                    LWDMS,LDAY,RSTFG,NITRON,SEPTON,
     O                    RETCOD)
C
C     + + + PURPOSE + + +
C     gets met data for the specified day from old met file or wdmsfl
C     Modification date: 2/14/92 JAM
C     Further modifications were made at AQUA TERRA Consultants 9/93
C     in two areas:
C       Increased the size of the buffer used to read precipitation data,
C     from a WDM file, to store a whole year of data.  This eliminates
C     the need to perform a WDM read from disk for every month being
C     simulated. Reads from disk are now performed only once per year.
C       Also, the capability to read average monthly evaporation values
C     stored as attributes on the same WDM dataset as the precipitation
C     data has been added. These monthly values are then divided by the
C     number of days in the month to generate daily values to be used
C     in the simulation for the appropriate month.
C
C     + + + DUMMY ARGUMENTS + + +
      Use m_debug
      Use Date_Module
      Implicit None
      INTEGER     IY,MONTH,DOM,LMETEO,LSPTIC,LNITAD,RETCOD,
     1            RSTFG,LWDMS,JULDAY,LDAY
      LOGICAL     NITRON,SEPTON
C
C     + + + ARGUMENT DEFINITIONS + + +
C     IY     - ???
C     MONTH  - ???
C     DOM    - ???
C     JULDAY - ???
C     LDAY   - ???
C     LMETEO - unit number for meteorologic file
C     LSPTIC - unit number for septic effluent file
C     LNITAD - unit number for nitrogen atmospheric deposition file
C     LWDMS  - unit number of wdms file
C     RSTFG  - restart flag 1-first time thru, 2-later times thru
C     NITRON - nitrogen simulation on flag
C     SEPTON - septic effluent on flag
C     RETCOD - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMET.INC'
      INCLUDE 'CSPTIC.INC'
      INCLUDE 'CNITR.INC'
C
C     + + + SAVES + + +
      INTEGER      DELT,DTRAN(15),QUALFG,TUNITS,CURYR,CMTDSN(5),
     $             CSPDSN(4),CNDDSN(6),READFG
      SAVE         DELT,DTRAN,QUALFG,TUNITS,CURYR,CMTDSN,
     $             CSPDSN,CNDDSN
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      I,MM,MD,MY,DATES(6),NVAL,IDY,IMO,
     1             IERROR,SAIND(12),SALEN,NDAYS,NXTMON
      REAL         R0,RSAVAL
      LOGICAL      FATAL
      CHARACTER*60 CADBUF
      CHARACTER*80 MESAGE
      CHARACTER*2  CDSN
      CHARACTER*4  CRCODE
C
C     + + + FUNCTIONS + + +
      REAL         DAYVAL

      Integer, Save :: itimes = 0  ! m_debug
      Integer, Dimension(:), Pointer :: Days_in_Month
C
C     + + + EXTERNALS + + +
      EXTERNAL SUBIN,ERRCHK,WDTGET,SUBOUT,WDBSGR,ZIPR,DAYVAL
C
C     + + + DATA INITIALIZATIONS + + +
      DATA SAIND /135,136,137,138,139,140,141,142,143,132,133,134/
      DATA DELT,DTRAN,QUALFG,TUNITS /1,1,1,0,0,1,10*0,30,4/
      DATA CURYR,CMTDSN,CSPDSN,CNDDSN/0,5*0,4*0,6*0/
C
C     + + + INPUT FORMATS + + +
 1000 FORMAT(1X,3(I2),5F10.0)
 1010 FORMAT(1X,3I2,A60)
 1020 FORMAT(F10.0)
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT('Simulation date (',I2,2('/',I2),
     1       ') ,meteorological date (',I2,2('/',I2),') do not match')
 2010 FORMAT(I2)
 2020 FORMAT(I4)
C
C     + + + END SPECIFICATIONS + + +
C
      itimes = itimes + 1  ! m_debug
      R0 = 0.0
      SALEN  = 1
      MESAGE = 'GETMET'
      CALL SUBIN(MESAGE)

      !! "DATES" array below is not initialized. PRZM
      !! aborts when compiled with "debugging" options.
      !
      ! DATES(1) = 4-digit Year
      ! DATES(2) = Month, 1 .. 2
      ! DATES(3) = Day of the Month, 1 .. 28, 29, 30, 31
      ! DATES(4) = 0 ! Hours ?
      ! DATES(5) = 0 ! Minutes ?
      ! DATES(6) = 0 ! Seconds
      DATES = (/ IY + iybase, MONTH, DOM, 0, 0, 0 /)

      Days_in_Month => Number_of_Days_in_Month(Iyear=DATES(1))
      ! NDAYS = Days_in_Month(mon)     ! Mon May 02 15:01:38 EDT 2005

      RETCOD= 0
      IMO= 2

      NVAL = 365
      If (IsLeapYear(Iyear=DATES(1))) NVAL = 366

      ! NDAYS is always the number of days in February   ! m_debug
      ! Is this correct ?  Given the context, should DAYMON_new
      ! be called with MONTH (or even NXTMON) ?
      !
      ! Mon May 02 15:05:51 EDT 2005
      ! From the usage of NDAYS in the code, it appears that
      ! NDAYS should be set to the number of days in "MONTH" (input)
      ! or IMO (Do loop index). I am commenting the old code, in case
      ! the decision needs to ve revisited. Also, the new code makes
      ! DAYMON superfluous.
      !old! NDAYS = DAYMON_new(DATES(1),IMO)

      IF (MONTH.LT.12) THEN
        NXTMON= MONTH + 1
      ELSE
        NXTMON= 1
      END IF
C
      IF (METDSN(1).EQ.0) THEN
C       read from old meteorological file
        IF (RSTFG.EQ.1) THEN
C         first read from met file, skip as needed
10        CONTINUE
            READ(LMETEO,1000,END=20) MM,MD,MY,PRECIP,PEVP,TEMP,
     1                               WIND,SOLRAD
          IF (MY.LT.IY.OR.MM.LT.MONTH.OR.MD.LT.DOM) GO TO 10
        ELSE
C         further read and check of meteorlogical data
          READ(LMETEO,1000,END=20) MM,MD,MY,PRECIP,PEVP,TEMP,
     1                             WIND,SOLRAD
          IF (MY.NE.IY.OR.MM.NE.MONTH.OR.MD.NE.DOM) THEN
            IERROR = 2000
            FATAL = .TRUE.
            WRITE(MESAGE,2000) DOM,MONTH,IY,MD,MM,MY
            CALL ERRCHK(
     I                  IERROR, MESAGE, FATAL)
            RETCOD= 1
          END IF
        END IF
        GO TO 30
20      CONTINUE
C
C         end of file reading metdata
          RETCOD= 2
30      CONTINUE
      ELSE
C       read from wdms file
        DATES(1)= IY + 1900
        DATES(2)= MONTH
        DATES(3)= DOM
        DATES(4)= 0
        DATES(5)= 0
        DATES(6)= 0
        DO 40 I = 1,5
          IF (CMTDSN(I).NE.METDSN(I) .OR. CURYR.NE.DATES(1)) THEN
C           time to read another year of data
            IF (METDSN(I).GT.0) THEN
C             retrieve time-series data from wdm file
              CALL WDTGET (LWDMS,METDSN(I),DELT,DATES,NVAL,
     I                     DTRAN(I),QUALFG,TUNITS,
     O                     DBUFF(1,I),RETCOD)
            ELSE IF (METDSN(I).EQ.-1) THEN
C             retrieve attribute values for evap from dataset
              IDY= 1
              DO 35 IMO= 1,12
C               get average monthly values for each month of year
                CALL WDBSGR (LWDMS,METDSN(1),SAIND(IMO),SALEN,
     O                       RSAVAL,RETCOD)
C               daily value is monthly average divided by days in month
C               also convert from inches to cms
                NDAYS = Days_in_Month(IMO)
                RSAVAL= RSAVAL/NDAYS
C               fill daily buffer with value
                CALL ZIPR (NDAYS,RSAVAL,DBUFF(IDY,I))
                IDY= IDY+ NDAYS
 35           CONTINUE
            ELSE IF (METDSN(I).EQ.0) THEN
C             this process not being modeled, no need to retrieve values
              CALL ZIPR (NVAL,R0,DBUFF(1,I))
            END IF
            IF (RETCOD .NE. 0) THEN
C             problem reading wdmsfl
              FATAL = .TRUE.
              WRITE(CDSN,2010)   METDSN(I)
              WRITE(CRCODE,2020) RETCOD
              MESAGE = 'Error reading WDMS file, data set number ['//
     1          CDSN//'] , return code ['//CRCODE//']'
              IERROR = 1295
              CALL ERRCHK(IERROR,MESAGE,FATAL)
            ENDIF
C           save current data-set number
            CMTDSN(I)= METDSN(I)
          END IF
  40    CONTINUE
C       get the current day's value
        PRECIP= DBUFF(JULDAY,1)
        PEVP  = DBUFF(JULDAY,2)
        TEMP  = DBUFF(JULDAY,3)
        WIND  = DBUFF(JULDAY,4)
        SOLRAD= DBUFF(JULDAY,5)
      END IF
C
      IF (SEPTON .AND. SEPDSN(1).EQ.0) THEN
C       read septic effluent from flat file
        IF (RSTFG.EQ.1) THEN
C         first read from flat file, skip as needed
50        CONTINUE
            READ(LSPTIC,1000,END=60) MM,MD,MY,INFLOW,AMMON,NITR,ORGN
          IF (MY.LT.IY.OR.MM.LT.MONTH.OR.MD.LT.DOM) GO TO 50
        ELSE
C         further read and check of meteorlogical data
          READ(LSPTIC,1000,END=60) MM,MD,MY,INFLOW,AMMON,NITR,ORGN
          IF (MY.NE.IY.OR.MM.NE.MONTH.OR.MD.NE.DOM) THEN
            IERROR = 2000
            FATAL = .TRUE.
            WRITE(MESAGE,2000) DOM,MONTH,IY,MD,MM,MY
            CALL ERRCHK(
     I                  IERROR, MESAGE, FATAL)
            RETCOD= 1
          END IF
        END IF
        GO TO 70
60      CONTINUE
C
C         end of file reading metdata
          RETCOD= 2
70      CONTINUE
      ELSE IF (SEPTON) THEN
C       read septic effluent from wdms file
        DATES(1)= IY + 1900
        DATES(2)= MONTH
        DATES(3)= DOM
        DATES(4)= 0
        DATES(5)= 0
        DATES(6)= 0
        DO 80 I = 1,4
          IF (CSPDSN(I).NE.SEPDSN(I) .OR. CURYR.NE.DATES(1)) THEN
C           time to read another year of data
            IF (SEPDSN(I).GT.0) THEN
C             retrieve time-series data from wdm file
              CALL WDTGET (LWDMS,SEPDSN(I),DELT,DATES,NVAL,
     I                     DTRAN(I+5),QUALFG,TUNITS,
     O                     SBUFF(1,I),RETCOD)
            ELSE
C             this process not being modeled, no need to retrieve values
              CALL ZIPR (NVAL,R0,SBUFF(1,I))
            END IF
            IF (RETCOD .NE. 0) THEN
C             problem reading wdmsfl
              FATAL = .TRUE.
              WRITE(CDSN,2010)   SEPDSN(I)
              WRITE(CRCODE,2020) RETCOD
              MESAGE = 'Error reading WDMS file, data set number ['//
     1          CDSN//'] , return code ['//CRCODE//']'
              IERROR = 1295
              CALL ERRCHK(IERROR,MESAGE,FATAL)
            ENDIF
C           save current data-set number
            CSPDSN(I)= SEPDSN(I)
          END IF
80      CONTINUE
C       get the current day's values
        INFLOW= SBUFF(JULDAY,1)
        AMMON = SBUFF(JULDAY,2)
        NITR  = SBUFF(JULDAY,3)
        ORGN  = SBUFF(JULDAY,4)
      END IF
C
      IF (NITRON) THEN
C       get any needed nitrogen atmospheric deposition values
        READFG = 0
        DO 200 I = 1,6
           NDAYS = Days_in_Month(MONTH)
C         check next flag
          IF (NIADFG(I).EQ.-2) THEN
C           atmospheric deposition values input as monthly
            IF (I.LE.3) THEN
C             dry monthly value
              NIADDR(I)= DAYVAL(NIAFXM(MONTH,I),
     I                          NIAFXM(NXTMON,I),DOM,NDAYS)
            ELSE
C             generate wet value from input concentration and current precip
              NIADWT(I)= PRECIP*DAYVAL(NIACNM(MONTH,I),
     I                                 NIACNM(NXTMON,I),DOM,NDAYS)
            END IF
          ELSE IF (NIADFG(I).EQ.-1) THEN
C           read this atmospheric deposition value from flat file
            IF (RSTFG.EQ.1 .AND. READFG.EQ.0) THEN
C             first read from flat file, skip as needed
 150          CONTINUE
                READ(LNITAD,1010,END=160) MM,MD,MY,CADBUF
              IF (MY.LT.IY.OR.MM.LT.MONTH.OR.MD.LT.DOM) GO TO 150
              READFG = 1
            ELSE IF (READFG.EQ.0) THEN
C             further read and check of nitrogaen atmospheric deposition data
              READ(LNITAD,1010,END=160) MM,MD,MY,CADBUF
              IF (MY.NE.IY.OR.MM.NE.MONTH.OR.MD.NE.DOM) THEN
                IERROR = 2000
                FATAL = .TRUE.
                WRITE(MESAGE,2000) DOM,MONTH,IY,MD,MM,MY
                CALL ERRCHK(
     I                      IERROR, MESAGE, FATAL)
                RETCOD= 1
              END IF
              READFG = 1
            END IF
C           read atmospheric deposition value from text buffer
            IF (I.LE.3) THEN
C             read dry deposition value
              READ(CADBUF,1020) NIADDR(I)
            ELSE
C             read concentration value, generate deposition using precip
              READ(CADBUF,1020) NIADWT(I-3)
              NIADWT(I-3) = NIADWT(I-3) * PRECIP
            END IF
            CADBUF = CADBUF(11:60)
            GO TO 170
 160        CONTINUE
C
C             end of file reading metdata
              RETCOD= 2
 170        CONTINUE
          ELSE IF (NIADFG(I).GT.0) THEN
C           read septic effluent from wdms file
            DATES(1)= IY + 1900
            DATES(2)= MONTH
            DATES(3)= DOM
            DATES(4)= 0
            DATES(5)= 0
            DATES(6)= 0
            IF (CNDDSN(I).NE.NIADFG(I) .OR. CURYR.NE.DATES(1)) THEN
C             time to retrieve another year of time-series data from wdm file
              CALL WDTGET (LWDMS,NIADFG(I),DELT,DATES,NVAL,
     I                     DTRAN(I+9),QUALFG,TUNITS,
     O                     NBUFF(1,I),RETCOD)
              IF (RETCOD .NE. 0) THEN
C               problem reading wdmsfl
                FATAL = .TRUE.
                WRITE(CDSN,2010)   NIADFG(I)
                WRITE(CRCODE,2020) RETCOD
                MESAGE = 'Error reading WDMS file, data set number ['//
     1            CDSN//'] , return code ['//CRCODE//']'
                IERROR = 1295
                CALL ERRCHK(IERROR,MESAGE,FATAL)
              ENDIF
C             save current data-set number
              CNDDSN(I)= NIADFG(I)
            END IF
C           get the current day's values
            IF (I.LE.3) THEN
              NIADDR(I) = NBUFF(JULDAY,I)
            ELSE
              NIADWT(I-3) = NBUFF(JULDAY,I) * PRECIP
            END IF
          END IF
 200    CONTINUE
      END IF
C     save current year
      CURYR= DATES(1)
C
      CALL SUBOUT
C
      RETURN
      END SUBROUTINE GETMET
C
C
C
      SUBROUTINE   PLGROW(IRDAY)
C
C     + + + PURPOSE + + +
C     determines plant growth parameters for use in other routines
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      LOGICAL      IRDAY
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     IRDAY   - determines if today is an irrigation day
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
C
C     + + + LOCAL VARIABLES + + +
      REAL         FRAC,DDLN
      INTEGER      I,IEXDAY,NEXDAY,NBYR,NEYR,J,NDYRS,NRZCOM,ILIN,K
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
C
      INTRINSIC MOD,FLOAT,AMIN1,AMAX1
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
C     determine which crop is in season. if a new crop is beginning,
C     determine the crop type and the length of the growing season.
C
      MESAGE = 'PLGROW'
      CALL SUBIN(MESAGE)
C
! m_debug ! date manipulation
      DO 60 I= 1, NCPDS
        IF (JULDAY .EQ. IEMER(I) .AND. IY .EQ. IYREM(I)) THEN
          IRDAY = .TRUE.
          IF(ERFLAG.EQ.0)ISCOND=2
          RZI = 1
          NDCNT=0
          DO 10 J= 1, NDC
            IF (INCROP(I) .EQ. ICNCN(J))THEN
              NCROP=J
              IUSLEC=1
              IF(ERFLAG.EQ.0)ISCOND=IUSLEC
            ENDIF
10        CONTINUE
          NCP  = I
          NDYRS= IYRMAT(I)- IYREM(I)
          IF (NDYRS .LE. 0) THEN
            TNDGS(I)= MAT(I)- IEMER(I)
          ELSE
            NEXDAY = 0
            IF (MOD(IYRMAT(I),4) .EQ. 0) NEXDAY= NEXDAY+1
            IF (MOD(IYREM(I),4) .EQ. 0)  NEXDAY= NEXDAY+1
            IF (NDYRS .LE. 1) THEN
              TNDGS(I)= 365- IEMER(I)+ MAT(I)+ NEXDAY
            ELSE
              NBYR  = IYREM(I)+1
              NEYR  = IYRMAT(I)-1
              IEXDAY= 0
              DO 40 J=NBYR, NEYR
                IF (MOD(J,4) .EQ. 0) IEXDAY= IEXDAY+1
40            CONTINUE
              TNDGS(I)= MAT(I)- IEMER(I)+(365*NDYRS)+ IEXDAY+ NEXDAY
            ENDIF
          ENDIF
        ENDIF
60    CONTINUE
C
C     determine fraction of time elapsed between crop emergence and
C     maturation and compute crop growth parameters
      FRAC  = 0.
      COVER = 0.
      WEIGHT= 0.
      HEIGHT= 0.
      NCOM1 = NCOM0
      DIN   = 0.
      IF (NCP .NE. 0 .AND. RZI .NE. 0) THEN
        NDCNT = NDCNT+1
        FRAC  = AMIN1(1.0,FLOAT(NDCNT)/FLOAT(TNDGS(NCP)))
        COVER = COVMAX(NCROP)*FRAC
        WEIGHT= WFMAX(NCROP)*FRAC
        HEIGHT= HTMAX(NCROP)*FRAC
C
c AMXDR:	maximum rooting depth of the crop (cm).

        ILIN = 0
        DDLN = 0.0
70      CONTINUE
          ILIN = ILIN + 1
          DDLN = DDLN + DELX(ILIN)
        IF (AMXDR(NCROP)*FRAC .GT. DDLN) GO TO 70
        NRZCOM = ILIN
        NRZCOMP = ILIN
        NCOM1 = AMAX1 (FLOAT(NRZCOM),FLOAT(NCOM0))+ 0.5
        DIN   = CINTCP(NCROP)*COVER
C
C       set soil surface condition after harvest and
C       turn off root zone flag
        IF (IY .EQ. IYRHAR(NCP) .AND. JULDAY .EQ. IHAR(NCP)) THEN
          IRDAY = .FALSE.
          If (ErFlag == 0) Then
             ISCOND = ICNAH(NCROP)
          End If
          RZI   = 0 ! set root zone flag
          DO 38 K=1,NCHEM
            IFSCND(K,NCROP) = IPSCND(K)
  38      CONTINUE
          COVER  = 0.0
          HEIGHT = 0.0
          WEIGHT = 0.0
          DIN    = 0.0 ! reset to eliminate crop interception
        ENDIF
C
C       set uptake flags if crop is growing
        IF (RZI .NE. 0) THEN
          DO 119 K=1,NCHEM
            DO 120 I=1,NRZCOM
              GAMMA(K,I)= UPTKF(K)
120         CONTINUE
119       CONTINUE
        ENDIF
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END Subroutine PLGROW
C
C
C
      SUBROUTINE IRRIG
C
C     + + + PURPOSE + + +
C     determines soil moisture deficit, decides
C     if irrigation is needed, and calculates irrigation
C     depths.
C     Modification date: 2/14/92 JAM
C
      Use m_furrow
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CMET.INC'
C
C     + + + LOCAL VARIABLES + + +
      REAL         SMCRIT,SMAVG,FCAVG,XLOC,SLOPE,DDLN
      INTEGER      I,ILIN
      CHARACTER*80 MESAGE
C
C local variable definitions:
C      XLOC.....location in furrow (fraction of length)
C      SLOPE....slope in infiltration - distance curve for furrow
C
C     + + + INTRINSICS + + +
C
      INTRINSIC MIN
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'IRRIG'
      CALL SUBIN(MESAGE)
C
C     initialization
      APDEP = 0.0
      SMDEF = 0.0


      really_not_thrufl = .FALSE.


C     compute average soil moisture and porosity for root zone

! SMCRIT -- soil moisture level where irrigation begins (fraction).
! SMCRIT -- soil moisture level where irrigation begins (fraction).
! SMAVG  -- average root zone soil moisture level (fraction).
! FCAVG  -- average root zone field capacity (fraction).
!
! PCDEPL -- fraction of available water capacity at which irrigation is applied.
!           Usually ~0.45 – 0.55; PRZM accepts values between 0.0 and 0.9
!
! THEFC --  field capacity in the horizon (cm3 cm^-3).
! THEWP --  wilting point in the horizon (cm3 cm^-3).
! THETN --  (cm3 cm^-3) soil water content at the end of the current day for
!           each soil compartment. Note: the water content above the wilting
!           point (ThetN - TheWP) represents the water available to the crop.
!
! NCOMRZ	-- Number of Compartments in the Root Zone
!
! Maximum available soil water:  TheFC - TheWP
! Critical Water Fraction, below which irrigation occurs:  PCDEPL*(TheFC - TheWP)
! Today's available water: Thetn - TheWP
! Therefore, irrigate if: Thetn - TheWP < PCDEPL*(TheFC - TheWP)
!                   i.e., Thetn < PCDEPL*(TheFC - TheWP) + TheWP
!
! From Dirk Young/DC/USEPA/US 10/20/04 12:08 PM
! THETN is actually the begining day water content at this point
! in the program because the call to IRRIG occurs before the
! hydrologic updates in HYDR1. Thus in the IRRIG routine, the
! definition of THETN is contrary to the manual's definition.
!
! See also comments in subroutine iniacc.

      DW = 0.0
      SMCRIT = 0.0
      SMAVG = 0.0
      FCAVG = 0.0
      DO I=1,NRZCOMP
         SMCRIT = SMCRIT + (PCDEPL*(THEFC(i)-THEWP(I))+THEWP(I))*delx(i)
         SMDEF = SMDEF+(THEFC(i)-THETN(I))*(1.0 + FLEACH)*DELX(I)

! dfy note SMDEF is not the soil moisture deficit, but deficit + salt leaching requirements
! not as defined in equation 6-89

C        SMCRIT = SMCRIT + (PCDEPL*(THEFC(I)-THEWP(I))+THEWP(I))/NCOM1
C        SMAVG = SMAVG + THETO(I)/NCOM1
C        FCAVG = FCAVG + THEFC(I)/NCOM1
         DW = DW + (THETAS(I)-THETO(I))/NCOM1
      ENDDO
C


C



      IF((Sum(Thetn(1:NRZCOMP)*delx(1:NRZCOMP)) > SMCRIT) .OR.
     *          PRECIP > 0.0) THEN
C     no irrigation needed
C
      ELSEIF(IRTYPE .EQ. 1)THEN
C     flood irrigation
        APDEP   = SMDEF
        AINF(1) = APDEP
        IRRR=AINF(1)
C
      ELSE IF(IRTYPE .EQ. 2)THEN
C     furrow irrigation
C
C       compute infiltration down the furrow
        CALL FURROW
C
C       use infiltration at a specific location in furrow
C       (XFRAC greater than 0.0)
C
        IF(XFRAC .GE. 0.0)THEN
C
C         find infiltration at location XFRAC in the furrow
          XLOC = 0.0
          DO 20 I=2,NSPACE
            XLOC = XLOC + DX/XL
            IF(XLOC .GE. XFRAC)THEN
              SLOPE = (FS(I)-FS(I-1))/DX
              APDEP = 100.*(FS(I) - SLOPE*XL*(XLOC - XFRAC))
              AINF(1) = APDEP
              GO TO 800
            END IF
   20     CONTINUE
C
C       use average furrow infiltration depth (XFRAC less than 0.0)
        ELSE
          DO 30 I=1,NSPACE
             APDEP = APDEP + 100.*FS(I)/NSPACE
   30     CONTINUE
          AINF(1) = APDEP
        END IF
        IRRR=AINF(1)
C
C     Over-Canopy Sprinkler Irrigation;  irrigation applied above
C     the canopy as precipitation
      ELSE IF(IRTYPE .EQ. 3)THEN
         PRECIP = MIN(RATEAP*24.0 , SMDEF+DIN-CINT)
         IRRR=PRECIP
C
C     Under-Canopy Sprinkler Irrigation; irrigation applied as
C     under-canopy throughfall
      ELSE IF(IRTYPE .EQ. 4)THEN
        THRUFL = MIN(RATEAP*24.0 , SMDEF)

!****************************************************************
!***************************************************************
! line added by dfy because this water did not flow through the canopy
! and should not wash off pesticide , this flag is used in PLPEST routine
! to prevent canopy washoff during under canopy irrigation
        really_not_thrufl = .TRUE.
!*****************************************************************
!******************************************************************

        IRRR=THRUFL
C       for sprinkler M-C, generate value of THRUFL here
C       from normal distribution, mean = APMEAN, std. dev. = APSTD
C
C     Over-Canopy Sprinkler Irrigation;  irrigation applied above
C     the canopy as precipitation, no runoff
      ELSE IF(IRTYPE .EQ. 5)THEN
         THRUFL = MIN(RATEAP*24.0 , SMDEF+DIN-CINT)
         IRRR=THRUFL
C
C     Over-Canopy Sprinkler Irrigation;  irrigation applied above
C     the canopy as precipitation (user defined amount)
      ELSE IF(IRTYPE .EQ. 6)THEN
         PRECIP = RATEAP*24.0
         IRRR=PRECIP
C     Over-Canopy Sprinkler Irrigation;  irrigation applied above
C     the canopy as precipitation, no runoff  (user defined amount)
      ELSE IF(IRTYPE .EQ. 7)THEN
         THRUFL = RATEAP*24.0
         IRRR=THRUFL
C
      END IF
C
800   CONTINUE
      CALL SUBOUT
C
      RETURN
      END SUBROUTINE IRRIG


      SUBROUTINE HYDROL (LPRZOT,MODID,RODPTH,CURVN)
C     Last change:  JMC  12 Apr 2004    4:49 pm
C
C     This subroutine calculates snowmelt, crop interception,
C     runoff, and infiltration from the soil surface
C     Modification date: 2/7/92 JAM
C     Further modified by PV @ AQUA TERRA Consultants 9/93 to
C     hard-wire the depth of runoff calculation to 10 cm
C
C     +  +  + DUMMY ARGUMENTS +  +  +
C
      Use Date_Module
      INTEGER     LPRZOT
      CHARACTER*3 MODID
C
C     +  +  + ARGUMENT DEFINITIONS +  +  +
C
C     LPRZOT  - Fortran unit number for output file LPRZOT
C     MODID - character string for output file identification
C
C     +  +  + PARAMETERS +  +  +
C
      INCLUDE 'PPARM.INC'
C
C     +  +  + COMMON BLOCKS +  +  +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CMISC.INC'
C
C     +  +  + LOCAL VARIABLES +  +  +
C
      REAL         TWLVL,CURVN,WLVL,AAA,DDLNJ,TTLNJ,TTT,SPTTOT,SPTAVE,
     *             TTFCRNF,TTWPRNF,CNFRAC
      INTEGER      I,RODPTH,MLIN,TLIN
      Logical      Issue_Error
      CHARACTER*80 MESAGE
      integer      :: itimes = 0
C
C     +  +  + INTRINSICS +  +  +
C
      INTRINSIC AMIN1,AMAX1
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,SUBOUT
C
C     +  +  + OUTPUT FORMATS +  +  +
C
2000  FORMAT (1X,A3,1X,110(1H*),/,1X,A3,1X,110(1H*),/,1X,A3,/,1X,A3,50X,
     1        'E R R O R',/,1X,A3,/,1X,A3,10X,'YOU ARE FORCING MORE ',
     2        'RUNOFF TO OCCUR THAN THE AMOUNT OF THROUGH FALL ',
     3        'AVAILABLE - THE',/,1X,A3,10X,'CANOPY COVERAGE AND THE ',
     4        'RUNOFF CURVE NUMBER INPUT VALUES ARE PROBABLY ',
     5        'INCONSISTENT',/,1X,A3,/,1X,A3,/,1X,A3,1X,110(1H*))
C
C     +  +  + END SPECIFICATIONS +  +  +
C
      MESAGE = 'HYDROL'
      CALL SUBIN(MESAGE)
C
      RUNOF = 0.0
      SMELT = 0.0
      SNOWFL= 0.0
      CINTB = CINT
      OSNOW = SNOW
      IF (SFAC .GT. 0.0) THEN
C
C       Compute snowmelt and accumulation
C
        IF (TEMP .LE. 0.0) THEN
          SNOWFL= PRECIP
          PRECIP= 0.0
          SNOW  = SNOW+ SNOWFL
        ELSE
          SMELT = AMIN1(SFAC*TEMP,SNOW)
          SNOW  = SNOW- SMELT
        ENDIF
      ENDIF
C
C     Compute interception
C     throughfall due to under-canopy sprinkler irrigation
C
      IF((IRTYPE.NE.5).AND.(IRTYPE.NE.7))THEN
        IF (THRUFL .GT. 0.0 .AND. PRECIP .LE. 0.0) THEN
          PRECIP = THRUFL
        ELSE
          THRUFL= AMAX1(0.0,PRECIP-(DIN-CINT))
          IF (PRECIP .GT. DIN-CINT) CINT = DIN
          IF (PRECIP .LE. DIN-CINT) CINT = CINT + PRECIP
        ENDIF
      ELSE
        IF (PRECIP .GT. 0.0) THEN
          THRUFL= AMAX1(0.0,PRECIP-(DIN-CINT))
          IF (PRECIP .GT. DIN-CINT) CINT = DIN
          IF (PRECIP .LE. DIN-CINT) CINT = CINT + PRECIP
        ENDIF
      ENDIF
C
C     Compute runoff
C     hard-wiring the depth of runoff calculation to 10 cm or the
C     surface compartment thickness, whichever is greater
C      AAA   = AMAX1(THKNS(1),10.)
      AAA   = AMAX1(DELX(1),10.0)
      MLIN  = 0
      DDLNJ = 0.0
10    CONTINUE
        MLIN  = MLIN + 1
        DDLNJ = DDLNJ + DELX(MLIN)
      IF (AAA .GT. DDLNJ) GO TO 10
      RODPTH= MLIN
      WLVL  = 0.0
C
      SPTAVE=0.0
      SPTTOT=0.0
      IF(ITFLAG.GT.0)THEN
        TLIN  = 0
        TTLNJ = 0.0
        TTT=15.0
15      CONTINUE
          TLIN  = TLIN + 1
          SPTTOT=SPTTOT+SPT(TLIN)*DELX(TLIN)
          TTLNJ = TTLNJ + DELX(MLIN)
        IF (TTT .GT. TTLNJ) GO TO 15
        SPTAVE=SPTTOT/TTLNJ
      ENDIF
C
      DO 30 I= 1, RODPTH
          WLVL= WLVL+ SW(I)
30    CONTINUE
C
      TWLVL = WLVL/ DDLNJ
      TTFCRNF=TFCRNF/DDLNJ
      TTWPRNF=TWPRNF/DDLNJ
C
c Formats (e.g., 2000) are not shared between subroutines.
c Rather than duplicating the format statement, Curve_Number_Internal
c will set Issue_Error if an error is detected and the calling
c routine takes care of issuing the error message.
      Issue_Error = .False.   ! Modified by Curve_Number_Internal

      IF (ITFLAG.EQ.0) THEN
         Call Curve_Number_Internal()
         If (Issue_Error) WRITE (LPRZOT,2000) (MODID,I=1,10)

      ELSE IF((ITFLAG.GT.0).AND.(SPTAVE.GT.0.0))THEN
         Call Curve_Number_Internal()
         If (Issue_Error) WRITE (LPRZOT,2000) (MODID,I=1,10)

      ELSE IF((ITFLAG.GT.0).AND.(SPTAVE.LE.0.0))THEN
         CURVN = 100.0
         RUNOF = THRUFL+SMELT
         WRITE (LPRZOT,2000) (MODID,I=1,10)
      ENDIF
C
C     Compute infiltration for first soil compartment
C
      CVNUM = CURVN
      AINF(1) = AINF(1) + THRUFL + SMELT- RUNOF

!      ! we are in SUBROUTINE HYDROL
      itimes = itimes + 1 ! m_debug
      Call i_to_ISO(MESAGE, iYear=1961, doy=itimes)
!      write (800, *) 'date, cn(ncrop,iscond,2): ',   ! m_debug
!     &       Trim(Mesage), ' ', cn(ncrop,iscond,2)   ! m_debug
C
      CALL SUBOUT
C
      RETURN

      Contains

      Subroutine Curve_Number_Internal()

            ! The code in this internal procedure is used twice in
            ! subroutine HYDROL. The code is complex enough
            ! that warrants efforts to prevent duplication.
            ! Keywords: Curve Number, CN
            Implicit None

!jmc,cn_new>c new cn calc begin
!jmc,cn_new>c Last change:  JMC  12 Apr 2004    4:49 pm
!jmc,cn_new>        IF(TWLVL .GT. THETH)THEN
!jmc,cn_new>          CNFRAC= ((TTFCRNF-(TWLVL-THETH))/TTFCRNF)
!jmc,cn_new>          CURVN = CN(NCROP,ISCOND,2)+ CNFRAC*
!jmc,cn_new>     1             (CN(NCROP,ISCOND,3)-CN(NCROP,ISCOND,2))
!jmc,cn_new>          IF (CURVN .GT. CN(NCROP,ISCOND,3)) CURVN = CN(NCROP,ISCOND,3)
!jmc,cn_new>        ELSEIF(TWLVL .EQ. THETH)THEN
!jmc,cn_new>          CURVN = CN(NCROP,ISCOND,2)
!jmc,cn_new>        ELSEIF (TWLVL .LT. THETH)THEN
!jmc,cn_new>          CNFRAC=1.0-(((THETH-(THETH-TWLVL))/THETH))
!jmc,cn_new>          CURVN = CN(NCROP,ISCOND,2)- CNFRAC*
!jmc,cn_new>     1             (CN(NCROP,ISCOND,2)-CN(NCROP,ISCOND,1))
!jmc,cn_new>          IF (CURVN .LT. CN(NCROP,ISCOND,1)) CURVN = CN(NCROP,ISCOND,1)
!jmc,cn_new>        ENDIF
!jmc,cn_new>c new cn calc end

        CURVN = CN(NCROP,ISCOND,2)+ (TWLVL-THETH)* (CN(NCROP,ISCOND,3)-
     1        CN(NCROP,ISCOND,2))/ THETH
        IF (CURVN .GT. CN(NCROP,ISCOND,3)) CURVN = CN(NCROP,ISCOND,3)
        IF (TWLVL .LT. THETH) CURVN= CN(NCROP,ISCOND,1)+ TWLVL*
     1        (CN(NCROP,ISCOND,2)- CN(NCROP,ISCOND,1))/ THETH

C       the constant 0.508 is derived from 0.2 * 2.54 cm/in
C       and 0.2 is from INABS = 0.2 * S, where S is (1000./CURVN-10.) below.
c       INABS: Initial Abstraction of Water from Potential Surface Runoff
c
        INABS = AMAX1(0.508* (1000./CURVN-10.),PRECIP-THRUFL)
        IF (PRECIP+SMELT .GT. 0.0) THEN
          IF (PRECIP+SMELT .GT. INABS) RUNOF= (PRECIP+SMELT-INABS)**2/
     1                                      (PRECIP+ SMELT+ (4* INABS))
          IF (THRUFL+SMELT .LT. RUNOF) THEN
            RUNOF = THRUFL+SMELT
            Issue_Error = .True.
            ! WRITE(LPRZOT,2000) (MODID,I=1,10)
          ENDIF
        ENDIF

      End Subroutine Curve_Number_Internal
      END SUBROUTINE HYDROL



      SUBROUTINE EVPOTR
C
C     Computes daily potential evapotranspiration,
C     canopy evaporation, and actual evapotranspiration from each
C     soil layer
C     Modification date: 2/14/92 JAM
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL         PET,ES(40),PETP,ANUM,DENOM,AW,FRAC(NCMPTS),TSW,
     1             TWP,TFRAC,RNSUM,STDELX,EDEPTH
      INTEGER      ITEMP,I,NSUM
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
C
      INTRINSIC INT,FLOAT,AMAX1,AMIN1
C
C     + + + EXTERNALS + + +
C
      EXTERNAL SUBIN,SUBOUT
C
C     + + + DATA INITIALIZTIONS + + +
C
      DATA ES/ 4.926, 5.294, 5.685, 6.101, 6.543, 7.013, 7.513, 8.015,
     1         8.609, 9.209, 9.844,10.518,11.231,11.987,12.788,13.634,
     2        14.530,15.477,16.477,17.535,18.650,19.827,21.068,22.377,
     3        23.756,25.209,26.739,28.349,30.043,31.824,33.695,35.663,
     4        37.729,39.898,42.175,44.453,47.067,49.692,52.442,55.324/
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'EVPOTR'
      CALL SUBIN(MESAGE)
C
C     Compute potential evapotranspiration
C
      ITEMP= INT(TEMP)
      IF (ITEMP.LT.1)  ITEMP= 1
      IF (ITEMP.GT.40) ITEMP= 40
      IF (IPEIND .EQ. 0) THEN
        PET= PEVP*PFAC
      ELSEIF (IPEIND .EQ. 1) THEN
        PET= 0.021*ES(ITEMP)*DT(MONTH)**2.0/(FLOAT(ITEMP)+273.)
      ELSEIF (IPEIND .EQ. 2) THEN
        IF (PEVP .GT. 0.0) THEN
          PET= PEVP*PFAC
        ELSEIF (TEMP .GT. -99.) THEN
          PET= 0.021*ES(ITEMP)*DT(MONTH)**2.0/(FLOAT(ITEMP)+273.)
        ELSE
          PET= 0.0
        ENDIF
      ENDIF
C
C     Subtract canopy evaporation from potential evapotranspiration
C
      PETP= AMAX1(0.0,PET-CINT)
      IF (PET .GT. CINT) THEN
        CEVAP= CINT
      ELSE
        CEVAP= PET
      ENDIF
      CINT= CINT-CEVAP
C
C     Compute evapotranspiration from each soil layer
C
      EDEPTH = 5.0
      STDELX = DELX(1)
      STTDET = 0.0
C
C     End of modification
C
      TDET = 0.0
      DO 10 I= 1, NCOM2
        ET(I)= 0.0
10    CONTINUE
      ANUM = 0.0
      DENOM= 0.0
      DO 20 I= 1, NCOM1
        ANUM = ANUM + AMAX1(0.0,SW(I)- WP(I))
        DENOM= DENOM+ AMAX1(0.0,FC(I)- WP(I))
20    CONTINUE
      AW   = ANUM/DENOM
      IF (AW.LT.0.6) PETP= AW*PETP/0.6
      NSUM = 0
      TSW  = 0.0
      TWP  = 0.0
      DO 30 I= 1, NCOM1
        NSUM = NSUM + I
        TSW  = TSW + SW(I)
        TWP  = TWP + WP(I)
30    CONTINUE
      RNSUM= FLOAT(NSUM)
      IF (RNSUM .GT. 0.00 .AND. TSW .GT. TWP) THEN
        TFRAC= 0.0
        DO 40 I= 1, NCOM1
          FRAC(I)=FLOAT(NCOM1-I+1)*(SW(I)-WP(I))/(RNSUM*(TSW-TWP))
          TFRAC  =TFRAC + FRAC(I)
40      CONTINUE
        DO 50 I = 1, NCOM1
          ET(I) = AMIN1((SW(I)-WP(I)),PETP*FRAC(I)/TFRAC)
          ET(I) = AMAX1(ET(I),0.0)
          TDET  = TDET + ET(I)
C
C         This code is added by C.S.Raju to estimate the evaporation
C         through the top 5cm depth of soil.
C
          IF (STDELX .LE. EDEPTH)THEN
            STTDET = STTDET + ET(I)
            STDELX = STDELX + DELX(I)
          END IF
C
C
50      CONTINUE
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
      SUBROUTINE HYDR1
C
C     Performs hydraulic calculations assuming a uniform soil
C     profile with unrestricted drainage
C     (drainage occurs instantaneously)
C     Modification date: 2/18/92 JAM
C
C     +  +  + PARAMETERS +  +  +
C
      INCLUDE 'PPARM.INC'
C
C     +  +  + COMMON BLOCKS +  +  +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CSPTIC.INC'
C
C     +  +  + LOCAL VARIABLES +  +  +
C
      REAL         R(3,NCMPTS)
      INTEGER      I,K
      CHARACTER*80 MESAGE
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,SUBOUT
C
C     +  +  + END SPECIFICATIONS +  +  +
C
      MESAGE = 'HYDR1'
      CALL SUBIN(MESAGE)
C
      DO 20 I=1,NCOM2
        THETO(I) = SW(I)/DELX(I)
        THETN(I) = (SW(I)+ AINF(I)+ LINF(I)- ET(I))/ DELX(I)
        AINF(I+1)= 0.0
        IF (THETN(I) .GT. THEFC(I)) THEN
          AINF(I+1)= (THETN(I)- THEFC(I))* DELX(I)
          THETN(I) = THEFC(I)
        ENDIF
        VEL(I)= AINF(I+1)/THETN(I)
        IF (MCFLAG.EQ.1) THEN
          DO 21 K = 1,3
            R(K,I) = 1 + (BD(I)*KD(K,I)/THETN(I))
C            VM(K,I) = VEL(I)/R(K,I)
21        CONTINUE
        ENDIF
        SW(I) = THETN(I)*DELX(I)
20    CONTINUE
C
      VLFLAG = 0
      DO 30 I = 1, NCOM2
        IF (VEL(I) .GT. 0.0) VLFLAG = 1
30    CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE HYDR2
C
C     Performs soil hydraulic calculations. Incoming water
C     fills successive soil compartments to field capacity during infil-
C     tration events until incoming water is depleted. Percolation continues
C     according to assigned drainage parameters (AD) until redistribution
C     is complete. Allows for the presence of restrictive layers in soil
C     profile.
C     Modification date: 2/7/92 JAM
C
C     +  +  + PARAMETERS +  +  +
C
      INCLUDE 'PPARM.INC'
C
C     +  +  + COMMON BLOCKS +  +  +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CSPTIC.INC'
C
C     +  +  + LOCAL VARIABLES +  +  +
C
      REAL         R(3,NCMPTS)
      REAL         TS(NCMPTS),AVSTOR,EXTRA,F1,F2,F3,T,LNCHK
      INTEGER      I,K,IB,NDEX,NDEXM1
      CHARACTER*80 MESAGE
      REAL*8       EXPCHK
C
C     +  +  + INTRINSICS +  +  +
C
      INTRINSIC AMAX1,AMIN1,DBLE,REAL
C
C     +  +  + EXTERNALS +  +  +
C
      EXTERNAL SUBIN,SUBOUT,LNCHK,EXPCHK
C
C     +  +  + END SPECIFICATIONS +  +  +
C
      MESAGE = 'HYDR2'
      CALL SUBIN(MESAGE)
C
C     Subtract evapotranspired water from soil profile
C
      DO 10 I=1,NCOM2
        OUTFLO(I) = 0.0
        THETO(I)=SW(I)/DELX(I)
        TS(I)   =THETO(I)+ (LINF(I)-ET(I))*DELT/DELX(I)
10    CONTINUE
C
      IF (AINF(1) .GT. 0.0) THEN
C
C       Route water during infiltration event
C
        DO 20 I=1, NCOM2
          AVSTOR   = (THETAS(I)- TS(I))* DELX(I)/DELT
          THETN(I) = AMIN1(AINF(I),AVSTOR)* DELT/DELX(I)+ TS(I)
          AINF(I+1)= AINF(I)- (THETN(I)-TS(I))* DELX(I)/DELT
          IF (AINF(I+1).LE.0.0) AINF(I+1)= 0.0
20      CONTINUE
C
C       If there is an infiltration event on the current dat, then water
C       movement calculations are finished - jump to end of routine
C
      ELSE
C
C       If there is no infiltration event on current, then water
C       movement calculations are made here
C
        AINF(1) = 0.0
        DO 40 I=1,NCOM2
          TS(I)   = TS(I)+ AINF(I)/DELX(I)* DELT
          AINF(I+1) = 0.0
          IF (TS(I) .GT. THETAS(I)) THEN
            F1 = THETAS(I) - THEFC(I)
            F2 = TS(I) - THEFC(I)
            F3 = LNCHK(F1/F2) / (-AD(I)-ADL(I))
            T  = AMIN1(1.0,F3)
            TS(I) = THEFC(I) + F2 *
     1                  REAL(EXPCHK(DBLE((-AD(I)-ADL(I))*T)))
            AINF(I+1) = AD(I) * F2 * DELX(I) / (ADL(I) + AD(I)) *
     1              (1.0 - REAL(EXPCHK(DBLE((-AD(I)-ADL(I))*T))))
            OUTFLO(I) = ADL(I) * F2 * DELX(I) / (ADL(I) + AD(I)) *
     1             (1.0 - REAL(EXPCHK(DBLE((-AD(I)-ADL(I))*T))))
            IF (T .LT. 1.0) THEN
              F1 = REAL(EXPCHK(DBLE(-AD(I)*(1.0-T))))
              F2 = TS(I) - THEFC(I)
              TS(I) = THEFC(I) + F2 * F1
              AINF(I+1) = AINF(I+1) + F2 * DELX(I) * (1.0 - F1)
            ENDIF
          ELSEIF (TS(I) .GT. THEFC(I)) THEN
            F1 = REAL(EXPCHK(DBLE(-AD(I) * DELT)))
            F2 = TS(I) - THEFC(I)
            TS(I) = THEFC(I) + F2 * F1
            AINF(I+1) = F2 * DELX(I) * (1.0 - F1)
          ENDIF
          THETN(I)= TS(I)
40      CONTINUE
C
50      CONTINUE
          NDEX= 0
          I   = NCOM2
60        CONTINUE
            IF (THETN(I).GT.THETAS(I)) NDEX= I
            I = I- 1
          IF (I.GE.1.AND.NDEX.EQ.0) GO TO 60
C
          IF (NDEX .GT. 1) THEN
C
C           Redistribute water into overlying compartments
            NDEXM1     = NDEX- 1
            EXTRA      = THETN(NDEX)- THETAS(NDEX)
            THETN(NDEX)= THETAS(NDEX)
            IB= NDEXM1
70          CONTINUE
              AVSTOR    = AMAX1(0.0,THETAS(IB)-THETN(IB))
              THETN(IB) = AMIN1(EXTRA,AVSTOR)+ THETN(IB)
              AINF(IB+1)= AINF(IB+1)- EXTRA * DELX(IB)/DELT
              EXTRA     = EXTRA- AMIN1(EXTRA,AVSTOR)
              IB= IB- 1
            IF (EXTRA .GT. 0.0 .AND. IB .GE. 1) GO TO 70
C
C           Look for oversaturation again
          ENDIF
        IF (NDEX .NE. 0) GO TO 50
      ENDIF
C
      DO 120 I=1,NCOM2
        VEL(I)= AINF(I+1)/THETN(I)
        IF (MCFLAG.EQ.1) THEN
          DO 22 K = 1,3
            R(K,I) = 1 + (BD(I)*KD(K,I)/THETN(I))
C            VM(K,I) = VEL(I)/R(K,I)
22        CONTINUE
        ENDIF
        SW(I) = THETN(I)*DELX(I)
120   CONTINUE
C
      VLFLAG = 0
      DO 130 I = 1, NCOM2
        IF (VEL(I) .GT. 0.0) VLFLAG = 1
130   CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE EROSN
C
C     + + + PURPOSE + + +
C     Determines loss of pesticide due to erosion by the MUSLE method
C     and an enrichment ratio.  It sets up a sink term (ELTERM) for
C     the pesticide balance in the surface layer.
C     Modification date: 2/14/92 JAM
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMET.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      REAL         Q,RNUM,DENOM,QQP,SLKGHA,ENRICH,LNCHK
      REAL         EC0,EC1,EC2,TC,QP,QU
      CHARACTER*80 MESAGE
      REAL*8       EXPCHK
      INTEGER      SPTFLG
C
C     + + + INTRINSICS + + +
C
      INTRINSIC REAL,DBLE
C
C     + + + EXTERNAL + + +
C
      EXTERNAL SUBIN,LNCHK,EXPCHK,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'EROSN'
      CALL SUBIN(MESAGE)
C
C     Determine runoff energy factor
C
      IF(ERFLAG.EQ.1)THEN
        Q=RUNOF*AFIELD*100.
        RNUM = AFIELD* (PRECIP+SMELT)* RUNOF
        DENOM= TR* (PRECIP+SMELT-INABS)
        QQP  = RNUM/DENOM* Q* 0.0278
        SEDL  = 11.8* QQP**0.56
      ELSEIF(ERFLAG.GT.1)THEN
        CALL TMCOEF(EC0,EC1,EC2)
        CALL TMCONC(TC)
        QU=EC0+EC1*ALOG10(TC)+EC2*(ALOG10(TC))**2.
        QU=10.0**QU
        QP=(QU*(AFIELD*.00386)*(RUNOF*.3937))*0.02832
        QP=(QP/AFIELD)*360
        Q=RUNOF*10.
        QQP=Q*QP
      ENDIF
C check to see if first compartment frozen
      SPTFLG=0
      IF((ITFLAG.EQ.1).AND.(SPT(1).LE.0.0))THEN
        SPTFLG=1
      ENDIF
C
C     ERFLAG=2: MUSLE
C     ERFLAG=3: MUST
C     ERFLAG=4: MUSS
      IF(SPTFLG.EQ.1)THEN
        ELTT=0.0
      ELSE
        IF(ERFLAG.EQ.2)THEN
          SEDL=1.586*(QQP**0.56)*(AFIELD**0.12)
        ELSEIF(ERFLAG.EQ.3)THEN
          SEDL=2.5*(QQP**0.5)
        ELSEIF(ERFLAG.EQ.4)THEN
          SEDL=0.79*(QQP**0.65)*(AFIELD**0.009)
        ENDIF

C
C       Compute enrichment ratio
C
        IF(ERFLAG.EQ.1)THEN
          SEDL  = SEDL* USLEK* USLELS* CFAC* USLEP
          SLKGHA= SEDL* 1000./AFIELD
        ELSEIF(ERFLAG.GT.1)THEN
          SEDL  = (SEDL* USLEK* USLELS* CFAC* USLEP)*AFIELD
          SLKGHA= (SEDL* 1000.)/AFIELD
        ENDIF
C
        IF(SLKGHA.EQ.0.0)THEN
          ENRICH=1.0
        ELSE
          ENRICH= 2.0- (0.2* LNCHK(SLKGHA))
          ENRICH= REAL(EXPCHK(DBLE(ENRICH)))
        ENDIF
C
C       Compute loss term for pesticide balance
C
        ELTT=  (SLKGHA/(100000.*DELX(1)))*ENRICH
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C **********************************************
C
      SUBROUTINE TMCONC(TC)
C     -----------------
C     Calculate time of concentration based on TR-55 method
C     TC = time of concentration (hrs)
C

      INCLUDE 'PPARM.INC'
      INCLUDE 'CHYDR.INC'
C
      REAL S1,S2,HL1,HL2,WATER,TT1,V2,TT2,TC
C
C     ASSUME S2=S1, R2=0.4 FT, N2=0.05.  LIMIT HL1 TO 300'
      S1=SLP/100.
      S2=S1
C      R2=0.4
C      N2=0.08
C
      HL1=AMIN1(HL*3.28,300.)
      HL2=AMAX1(0.0,(HL*3.28)-300)
C
      WATER=(RUNOF)/2.54
C
      TT1=(0.007*(N1*HL1)**0.8) / ((WATER**0.5)*(S1**0.4))
      V2=16.1345*(S2)**0.5
      TT2=HL2/(3600.*V2)
      TC=TT1+TT2
C
      RETURN
      END
C
C **********************************************
C
      SUBROUTINE TMCOEF(EC0,EC1,EC2)
C
      INCLUDE 'PPARM.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CMISC.INC'
C
      INTEGER  IFND,J,IREGOLD
      INTEGER  NBG(4),NEN(4)
      REAL     CC(32),CC0(32),CC1(32),CC2(32)
      REAL     CTEMP,IAP,EC0,EC1,EC2

C
      DATA NBG /1,9,17,25/
      DATA NEN /8,13,22,30/
      DATA CC  /0.10,0.20,0.25,0.30,0.35,0.40,0.45,0.50,
     *          0.10,0.20,0.25,0.30,0.50,0.00,0.00,0.00,
     *          0.10,0.30,0.35,0.40,0.45,0.50,0.00,0.00,
     *          0.10,0.30,0.35,0.40,0.45,0.50,0.00,0.00/
      DATA CC0 /2.30550,2.23537,2.18219,2.10624,2.00303,
     *          1.87733,1.76312,1.67889,
     *          2.03250,1.91978,1.83842,1.72657,1.63417,
     *          0.0,0.0,0.0,
     *          2.55323,2.46532,2.41896,2.36409,2.29238,
     *          2.20282,0.0,0.0,
     *          2.47317,2.39628,2.35477,2.30726,2.24876,
     *          2.17772,0.0,0.0/
      DATA CC1 /-0.51429,-0.50387,-0.48488,-0.45695,-0.40769,
     *          -0.32274,-0.15644,-0.06930,
     *          -0.31583,-0.28215,-0.25543,-0.19826,-0.09100,
     *           0.0,0.0,0.0,
     *          -0.61512,-0.62257,-0.61594,-0.59857,-0.57005,
     *          -0.51599,0.0,0.0,
     *          -0.51848,-0.51202,-0.49735,-0.46541,-0.41314,
     *          -0.36803,0.0,0.0/
      DATA CC2 /-0.11750,-0.08929,-0.06589,-0.02835,0.01983,
     *           0.05754,0.00453,0.0,
     *           -0.13748,-0.07020,-0.02597,0.02633,0.0,
     *           0.0,0.0,0.0,
     *           -0.16403,-0.11657,-0.08820,-0.05621,-0.02281,
     *           -0.01259,0.0,0.0,
     *           -0.17083,-0.13245,-0.11985,-0.11094,-0.11508,
     *           -0.09525,0.0,0.0/
C
      IREGOLD=IREG
      IF(IREG.NE.2)THEN
        IF((JULDAY.LE.121).OR.(JULDAY.GE.258))THEN
          IREG=2
        ELSEIF(PRECIP.GT.5.08)THEN
          IREG=1
        ENDIF
      ENDIF
C
      IFND=0
      IAP=INABS/(THRUFL+SMELT)
C
      IF(IAP.LE.CC(NBG(IREG)))THEN
        EC0=CC0(NBG(IREG))
        EC1=CC1(NBG(IREG))
        EC2=CC2(NBG(IREG))
      ELSE
        DO 100 J=NBG(IREG),NEN(IREG)
          IF((IAP.LE.CC(J)).AND.(IFND.EQ.0))THEN
            CTEMP=(IAP-CC(J-1)) / (CC(J)-CC(J-1))
            EC0=CTEMP * (CC0(J)-CC0(J-1)) + CC0(J-1)
            EC1=CTEMP * (CC1(J)-CC1(J-1)) + CC1(J-1)
            EC2=CTEMP * (CC2(J)-CC2(J-1)) + CC2(J-1)
            IFND=1
          ENDIF
  100   CONTINUE
        IF(IFND.EQ.0)THEN
          EC0=CC0(NEN(IREG))
          EC1=CC1(NEN(IREG))
          EC2=CC2(NEN(IREG))
        ENDIF
      ENDIF
C
      IREG=IREGOLD
C
      RETURN
      END
C
C
      SUBROUTINE SLTEMP(
     I  LPRZOT,MODID)
C
C     + + + PURPOSE + + +
C     Calculates the soil temperature profile using
C     air temperatures, solar radiation, surface albedo, wind velocity,
C     evaporation, soil water content, and soil physical properties as
C     input data. This procedure is based on the methods of
C     Thebodeaux (1979);
C     Van Bavel and  Hillel (1975); de Vries (1963);
C     and Hanks et al. (1971).
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      !Use m_Canopy
      Use m_Wind
      INTEGER     LPRZOT
      CHARACTER*3 MODID
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     LPRZOT....Fortran unit number for output file
C     MODID...character string for identification of output file LPRZOT
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER      I,J,K,L,N,NUMDYS
      REAL         AIRDEN,Z0,D,ZCH,HTC,QC1,QEVF,QLW1,QLW2,QSWR,
     1             QGHF,TEMPK,STK,FX1,FX2,DELTA,EVAP,AAA,BBB,
     2             THKLY1,ABSOIL
      REAL         XVOL(5,NCMPTS),VOLCOR,LBTEMP,LNCHK,LOGCHK,
     1             DIFFCO(NCMPTS),ALAMDA(0:5),GEE(5,3),AKAY(5),
     2             THZERO(2),GFLD,SIGMA0,SIGMA1,SIGMA2,VAPLMD,AIRLMD,
     3             TA(NCMPTS),TB(NCMPTS),TC(NCMPTS),TF(NCMPTS)
C
C     + + + INTRINSICS + + +
C
      INTRINSIC ABS
C
C     + + + EXTERNALS + + +
C
      EXTERNAL LOGCHK,LNCHK,TRDIA1,SUBOUT
C
C     + + + DATA INITIALIZATIONS + + +
C
      DATA GEE(1,1),GEE(1,2),GEE(1,3)/2*0.125,0.750/
      DATA GEE(2,1),GEE(2,2),GEE(2,3)/2*0.125,0.750/
      DATA GEE(3,1),GEE(3,2),GEE(3,3)/2*0.5,0.0/
      DATA GEE(4,1),GEE(4,2),GEE(4,3)/3*0.333/
      DATA ALAMDA/122.7,1762.6,604.8,51.8,122.7,5.3/
      DATA VAPLMD/15.2/
C
C     + + + END SPECIFICATIONS + + +
C
C     Interpolation of daily values from neighboring monthly values of
C     soil surface albedo and bottom boundary temperature
C
      BBT(13) = BBT(1)
      NUMDYS = CNDMO(LEAP,MONTH+1) - CNDMO(LEAP,MONTH)
      LBTEMP = BBT(MONTH) + (BBT(MONTH+1)-BBT(MONTH))*DOM/NUMDYS
      ALBEDO(13) = ALBEDO(1)
      ABSOIL = ALBEDO(MONTH)+(ALBEDO(MONTH+1)-ALBEDO(MONTH))*DOM/NUMDYS
C
C     Estimation of surface albedo from canopy albedo and
C     soil surface albedo
C
      IF (SNOW .LT. 0.5)THEN
        ABSOIL = 0.23*COVER + ABSOIL*(1.-COVER)
      ELSE
        ABSOIL = 0.8
      END IF
C
C     Evaporation correction for crop canopy
C
      EVAP = STTDET*(1.-COVER)
C
      AIRLMD  = 5.3
C
C     If thermal conductivity and heat capacities are supplied,
C     bypass this sec.
C
      IF (IDFLAG .EQ. 0)GOTO 110
C
C     This portion of the routine estimates the Thermal Diffusivity of
C     soil compartment as the soil water content changes with time and
C     depth, using the procedure of de Vries (1963).
C
      DO 100 L =1,NCOM2
C
C     The vol fractions of sand,clay,and OM are adjusted so that their
C     total value equals to (1-porosity)
C
        VOLCOR=(1.0-THETAS(L))/((SAND(L)/2.65+CLAY(L)/2.65+
     1         OC(L)*1.724/1.3)*BD(L))
C
C       Conversion of Wt percents of soil constituents to vol fractions
C
        XVOL(1,L) = SAND(L)*BD(L)/2.65*VOLCOR
        XVOL(3,L) = OC(L)*1.724*BD(L)/1.30*VOLCOR
        XVOL(2,L) = 1.0-THETAS(L)-XVOL(1,L)-XVOL(3,L)
C
C       Defining water content and air in the soil pores
C
        XVOL(4,L) = THETO(L)
        IF(THETO(L) .LT. THEWP(L))XVOL(4,L)=THEWP(L)
        IF(THETO(L) .GT. THETAS(L))XVOL(4,L)=THETAS(L)
        XVOL(5,L) = THETAS(L) - XVOL(4,L)
C
C       Estimation of 'G' parameter when W.C is greater than F.C.
C
        IF (XVOL(4,L) .GT. THEFC(L))THEN
          GEE(5,1) = 0.333 - XVOL(5,L)/THETAS(L)*(0.333-0.035)
          ALAMDA(5) = AIRLMD + VAPLMD
C
C       Estimation of 'G' parameter when water content is less than F.C.
C
        ELSE
          GFLD = 0.333 - (THETAS(L)-THEFC(L))/THETAS(L)*(0.333-0.035)
          GEE(5,1) = 0.013 + XVOL(4,L)/THEFC(L)*(GFLD-0.013)
          ALAMDA(5) = AIRLMD + XVOL(4,L)/THEFC(L)*VAPLMD
        END IF
        GEE(5,2)=GEE(5,1)
        GEE(5,3)=1.-2*GEE(5,1)
        ALAMDA(0) = ALAMDA(4)
C
C       Estimation of thermal conductivity
C
        K = 0
 10     K = K+1
        SIGMA1 = 0.0
        SIGMA2 = 0.0
        DO 20 I = 1,5
          SIGMA0 = 0.0
C
C         Estimation of 'K' parameter
C
          DO 30 J = 1, 3
            SIGMA0 = SIGMA0+1./(1.+(ALAMDA(I)/ALAMDA(0)-1.)*GEE(I,J))
 30       CONTINUE
          AKAY(I) = SIGMA0/3.
          SIGMA1 = SIGMA1 + AKAY(I)*XVOL(I,L)*ALAMDA(I)
          SIGMA2 = SIGMA2 + AKAY(I)*XVOL(I,L)
 20     CONTINUE
C
C       Thermal Conductivity in cal/cm-day-C
C
        THZERO(K) =SIGMA1/SIGMA2
        IF (THETO(L) .LT. THEWP(L) .AND. K .LT. 2)THEN
          XVOL(4,L) = 0.0
          XVOL(5,L) = THETAS(L)
          ALAMDA(5) = AIRLMD
          ALAMDA(0) = ALAMDA(5)
          GOTO 10
        END IF
C
C       Interpolation of thermal cond. when W.C. is less than
C       critical point
C
        IF (THETO(L) .LT. THEWP(L))THEN
          THZERO(2) = 1.25*THZERO(2)
          THCOND(L)=THZERO(2)+THETO(L)/THEWP(L)*(THZERO(1)-THZERO(2))
        ELSE
          THCOND(L)=THZERO(1)
        END IF
C
C       Volumetric Heat Capacity of the soil layer, cal/cm3-C
C
        VHTCAP(L)=0.46*(XVOL(1,L)+XVOL(2,L)) + 0.6*XVOL(3,L) + THETO(L)
C
100   CONTINUE
110   CONTINUE
C
      DO 120 L = 1, NCOM2
C
C       Diffusion coefficient, cm2/day
C
        DIFFCO(L) = THCOND(L)/VHTCAP(L)
 120  CONTINUE
C
C     This portion of the subroutine estimates the Upper
C     Boundary Temperature using Energy-Balance at the air/soil
C     interface. The fourth order equation in terms of soil surface
C     temperature is solved by Newton-Raphson method for upper
C     boundary temperature.
C
C     Air Density(from Thibodeaux), gm/cm3
C
      AIRDEN = (-0.0042*TEMP +1.292)*1.E-3

      ! Computes zero displacement height, D (meter)
      ! and the roughness length, Z0 (meter)
      ZCH = HEIGHT / 100.0    ! convert to meter
      Call Get_Crop_Params (ZCH, Z0, D)
C
C     Heat Transfer coefficient at air-surface interface, cm/day
C     Wind speed in cm/sec, (Wind * 86400) in cm/day
C
      HTC = vonKarman**2 * WIND * 86400 /
     &   ((Log((uWind_Reference_Height-D)/Z0))**2)
C
C     Sensible air Heat Flux term, cal/cm2-K-day
C
      QC1= AIRDEN*0.2402*HTC
C
C     Evaporation heat flux term, cal/cm2-day, EVAP in cm/day
C
      QEVF = 580.0 * EVAP * 1.0
C
C     Atmospheric Longwave radiation component term, cal/cm2-K-day
C
      TEMPK = TEMP + 273.18
      QLW1 = EMMISS*0.936E-5*(TEMPK**2)*11.7E-8
C
C     Longwave radiation component emitted by the soil
C     term, cal/cm2-K-day
C
      QLW2 = EMMISS*11.7E-8
C
C     Short Wave radiation term, cal/cm2-day
C
      QSWR = (1.- ABSOIL)*SOLRAD
C
C     Calculation of Soil Heat flux term, cal/cm-C-day
C     Estimation of average temp gradient in the top 5cm of soil
C
      N = 1
      THKLY1 = DELX(1)
      AAA = 1.0/DELX(1)
      BBB = (SPT(1) + 273.18)/DELX(1)
35    IF(THKLY1 .LT. 5.0) THEN
        N = N +1
        THKLY1 = THKLY1 + DELX(N)
        BBB = BBB + (SPT(N) - SPT(N-1))/DELX(N)
      GOTO 35
      ENDIF
      AAA = AAA/N
      BBB = BBB/N
      QGHF= THCOND(1)
C
C     Initializing the soil surface temperature
C
      STK = TEMPK
      DELTA = 0.0
C
C     Newton-Raphson method to solve the 4th order equation for UBT
C
 40   STK = STK - DELTA
      FX1 = STK**4 + (QC1 + QGHF*AAA)/QLW2*STK - (QLW1*TEMPK**4.- QEVF
     1      + QC1*TEMPK + QSWR + QGHF*BBB)/QLW2
      FX2 = 4.*STK**3 + (QC1 + QGHF*AAA)/QLW2
      DELTA = FX1/FX2
C
C     Convergence criteria, 0.1 deg C
C
      IF(ABS(DELTA) .GT. 0.1)GOTO 40
      UBT = STK - 273.18
C
C     This portion of the routine simulates the Soil Temperature Profile
C     when Upper Boundary, Bottom Boundary, and Initial temperatures are
C     provided. Top Boundary Layer:
C
      TA(1)=0.0
      TC(1)=-(DIFFCO(1)+DIFFCO(2))*.5/(DELX(1)*(DELX(1)+DELX(2))*0.5)
      TB(1)=1.0+DIFFCO(1)/(DELX(1)**2)-TC(1)
      TF(1)=SPT(1)+DIFFCO(1)/(DELX(1)**2)*UBT
C
C       Non Boundary Layer:
C
        DO 50 I= 2, NCOM2-1
          TA(I) = -(DIFFCO(I-1)+DIFFCO(I))*0.5/(DELX(I)*(DELX(I)+
     1             DELX(I-1))*0.5)
          TC(I) = -(DIFFCO(I)+DIFFCO(I+1))*0.5/(DELX(I)*(DELX(I)+
     1             DELX(I+1))*0.5)
          TB(I) = 1.0 - (TA(I)+TC(I))
          TF(I) = SPT(I)
50      CONTINUE
C
C        Bottom Boundary Layer:
C
         TA(NCOM2) = -(DIFFCO(NCOM2-1)+DIFFCO(NCOM2))*0.5/
     1                (DELX(NCOM2)*(DELX(NCOM2)+DELX(NCOM2-1))*0.5)
         TB(NCOM2) = 1.0 -TA(NCOM2)+DIFFCO(NCOM2)/(DELX(NCOM2)**2)
         TC(NCOM2) = 0.0
         TF(NCOM2) =SPT(NCOM2)+DIFFCO(NCOM2)/(DELX(NCOM2)**2)*
     1              LBTEMP
C
          CALL TRDIA1(TA,TB,TC,SPT,TF,NCOM2,LPRZOT,MODID)
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE FARM (RODPTH,APPLY,CURVN)
C
C     + + + PURPOSE + + +
C     new subroutine added to ensure pesticide application is
C     applied during adequate moisture conditions
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
C
      LOGICAL   APPLY
      INTEGER*4 RODPTH
      REAL      CURVN
C
C     + + + ARGUMENT DEFINITIONS + + +
C
C     APPLY   - logical to flag  pesticide application
C     RODPTH  - number of runoff compartments (top of PRZM)
C     CURVN   - generated curve number from subroutine HYDROL
C
C
C     + + + PARAMETERS + + +
C
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
C
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMET.INC'
C
C     + + + LOCAL VARIABLES + + +
C
      INTEGER*4 I
      REAL      JEFAVG,JEFAG1
      REAL      THETAL,THETAH,THETAV,THEAV1
C
C     + + + END SPECIFICATIONS + + +
C
      THETAL  = 0.0
      THETAH  = 0.0
      JEFAVG = 0.0
      DO 70 I=1,RODPTH
        JEFAVG  =  JEFAVG + THETO(I)
        THETAL  =  THETAL + THEWP(I)
        THETAH  =  THETAH + THEFC(I)
70    CONTINUE
        JEFAG1  =  JEFAVG/RODPTH
        THETAV  =  (THETAL/RODPTH)
        THEAV1  =  (THETAH/RODPTH) * .9
C
      IF(FRMFLG.EQ.1)THEN
        IF ((JEFAG1 .GE. THETAV .AND. JEFAG1 .LE. THEAV1).AND.
     1      (CURVN .LT. CN(NCROP,ISCOND,3) .AND.
     2       CURVN .GT. CN(NCROP,ISCOND,1))) THEN
          APPLY = .TRUE.
        ENDIF
      ELSEIF(FRMFLG.EQ.2)THEN
        IF(PRECIP.EQ.0.0)THEN
          APPLY = .TRUE.
        ENDIF
      ELSEIF(FRMFLG.EQ.3)THEN
        IF (((JEFAG1 .GE. THETAV .AND. JEFAG1 .LE. THEAV1).AND.
     1       (CURVN .LT. CN(NCROP,ISCOND,3) .AND.
     2        CURVN .GT. CN(NCROP,ISCOND,1))).AND.(PRECIP.EQ.0.0))THEN
          APPLY = .TRUE.
        ENDIF
      ELSE
        APPLY = .FALSE.
      ENDIF
C
C
      RETURN
      END
C
C
C
      SUBROUTINE   SEPTIN
C
C     + + + PURPOSE + + +
C     Introduce septic effluent into PRZM soil column.
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CSPTIC.INC'
      INCLUDE 'CNITR.INC'
      INCLUDE 'CPEST.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I,LNC
C
C     + + + END SPECIFICATIONS + + +
C
      LNC = NCOMEN(SEPHZN) - NCOMBE(SEPHZN) + 1
      DO 10 I = NCOMBE(SEPHZN),NCOMEN(SEPHZN)
C       introduce water volume from septic effluent into column
        LINF(I)  = INFLOW/LNC
        AMMINF(I)= AMMON/LNC * 1.0E5
        NITINF(I)= NITR/LNC * 1.0E5
        ORGINF(I)= ORGN/LNC * 1.0E5
        NIT(1,I) = NIT(1,I) + ORGINF(I) * (1.0 - ORGRFC)
        NIT(2,I) = NIT(2,I) + AMMINF(I)
        NIT(4,I) = NIT(4,I) + NITINF(I)
        NIT(7,I) = NIT(7,I) + ORGINF(I) * ORGRFC
 10   CONTINUE
C
      RETURN
      END

