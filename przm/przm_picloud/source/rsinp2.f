C
C
      SUBROUTINE   INPREA
     I                   (MCARLO, PRZMON, VADFON, SEPTON, NITRON,
     I                    NCHEM, NLDLT, TRNSIM, FLOSIM, NPZONE, NVZONE,
     I                    IDAY0, IMON0, IYR0, IDAYN, IMONN, IYRN,
     I                    LMXZON, LNCMP2,
     I                    LMODID, IRUN,
     O                    CORDND,
     O                    SRNFG, IDNODE)
C
C     + + + PURPOSE + + +
C     called by main to read input files (PRZM,MCARLO)
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4   NCHEM,IRUN,NPZONE,NVZONE,
     1            IDAY0,IMON0,IYR0,IDAYN,IMONN,IYRN,
     2            LMXZON,LNCMP2,NLDLT,
     3            SRNFG,IDNODE(LMXZON)
      CHARACTER*3 LMODID
      LOGICAL     MCARLO, PRZMON, TRNSIM, FLOSIM, VADFON, SEPTON, NITRON
      REAL        CORDND(LMXZON,LNCMP2)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MCARLO - logical for monte carlo being ON or OFF
C     PRZMON - logical for przm being ON or OFF
C     VADFON - vadoft on flag
C     SEPTON - septic effluent on flag
C     NITRON - nitrogen modeling on flag
C     NCHEM  - number of chemicals being simulated
C     NLDLT  - maximum number of days in a time step (31)
C     NPZONE - number of przm zones
C     NVZONE - number of vadoft zones
C     TRNSIM - logical for transport being ON or OFF
C     FLOSIM - logical for flow being ON or OFF
C     IDAY0  - starting day of current time step
C     IMON0  - starting month of current time step
C     IYR0   - starting year of current time step
C     IDAYN  - ending day of current time step
C     IMONN  - ending month of current time step
C     IYRN   - ending year of current time step
C     LMXZON - local version of MXZONE so not multiply defined
C     LNCMP2 - local version of NCMPP2 so not multiply defined
C     MODID  - model id (pest,conc,water)
C     IRUN   - current run number
C     CORDND - nodal coordinates
C     SRNFG  - start of run flag
C     IDNODE - base node for PRZM
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
      INCLUDE 'PMXZON.INC'
      INCLUDE 'PMXNSZ.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CVNTR1.INC'
      INCLUDE 'CFILEX.INC'
      INCLUDE 'CSPTIC.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      I,LNG,IERROR,IFIL,BASEND,IPZONE,IVZONE,LNCHEM
      CHARACTER*80 MESAGE,LINCOD
      CHARACTER*1  IBUFF(80)
      LOGICAL      FRSTRD,FATAL,MCTFLG
C
C     + + + FUNCTIONS + + +
      INTEGER   LNGSTR
C
C     + + + EXTERNALS + + +
      EXTERNAL  SUBIN,PZSCRN,PRZMRD,ERRCHK,PRZECH,INIACC,THCALC,
     1          KDCALC,MCPRZ,INITL,RSTPUT,RSTPT1,SUBOUT,LNGSTR,
     2          VADINP,VADPUT
C
C     + + + OUTPUT FORMATS + + +
 2010 FORMAT (1X,A3,1X,110(1H*),/,1X,A3,1X,110(1H*),/,1X,A3,/,1X,A3,
     1        50X,'E R R O R',/,1X,A3,/,1X,A3,10X,'END OF INPUT ',
     2        'FILE FOUND TOO SOON - RECHECK INPUT SEQUENCE',/,1X,A3,
     3        /,1X,A3,1X,80A1,/,1X,A3,/,1X,A3,1X,110(1H*))
 2020 FORMAT (1X,A3,1X,110(1H*),/,1X,A3,1X,110(1H*),/,1X,A3,/,1X,A3,
     1        50X,'E R R O R',/,1X,A3,/,1X,A3,10X,'FORMAT ERROR IN ',
     2        'THE INPUT SEQUENCE - RECHECK INPUT FILE',/,1X,A3,
     3        /,1X,A3,1X,80A1,/,1X,A3,/,1X,A3,1X,110(1H*))
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'INPREA'
      CALL SUBIN(MESAGE)
C
      FRSTRD = IRUN .EQ. 1
C
      IF (PRZMON) THEN
        MESAGE = 'Reading [  PRZM ] data'
        CALL PZSCRN(1,MESAGE)
C
        ISTYR = IYR0
        ISDAY = IDAY0
        ISMON = IMON0
C
C       loop through all PRZM zones
        DO 10 IPZONE = 1, NPZONE
          IF (MCARLO) THEN
C         rewind input files for MC simulations
            IF (PRZMON) THEN
              IFIL = FPRZIN(IPZONE)
              REWIND IFIL
              IFIL = FMETEO(IPZONE)
              IF (IFIL.GT.0) THEN
C               dont rewind if WDM file in use
                REWIND IFIL
              END IF
              IFIL = FSPTIC(IPZONE)
              IF (IFIL.GT.0) THEN
C               septic effluent file in use
                REWIND IFIL
              END IF
            END IF
          END IF
C         rewind restart file
          IFIL = FPRZRS(IPZONE)
          REWIND IFIL
C
C         default to no septic effluent introduced
          SEPHZN = 0
C
          HEADER = 0
C
          CALL PRZMRD (FPRZIN(IPZONE),NCHEM,SEPTON,NITRON,
     O                 IBUFF,BASEND,LINCOD)
C
C         save base node for this zone in IDNODE for later processing
C         in the PRZM to VADOFT linkage
C
          IDNODE(IPZONE) = BASEND
C
          IF (RETCOD .NE. 0) THEN
            IF (RETCOD.EQ.1) WRITE(FECHO,2010) (LMODID,I=1,8),IBUFF,
     1                                        (LMODID,I=1,2)
            IF (RETCOD.EQ.2) WRITE(FECHO,2020) (LMODID,I=1,8),IBUFF,
     1                                        (LMODID,I=1,2)
            LNG    = LNGSTR(LINCOD)
            MESAGE = 'Error reading PRZM data, line [' //
     1                LINCOD(1:LNG) // ']'
            FATAL  = .TRUE.
            IERROR = 1400
            CALL ERRCHK(IERROR,MESAGE,FATAL)
          ENDIF
C
C         check irrigation flag
          IRNONE = 0
          IF (IRFLAG.EQ.0) THEN
            IRTYPE = 0
          END IF
          IF (IRFLAG.EQ.2) THEN
            IRNONE = 4
          END IF
          IF (FRSTRD) THEN
            IF (MCARLO) THEN
C             przm output file not open, send to kecho file
              CALL PRZECH (FECHO,LMODID,SEPTON,NITRON,
     I                     IDAY0,IMON0,IYR0,IDAYN,IMONN,IYRN)
            ELSE
C             echo to przm output file
              CALL PRZECH (FPRZOT(IPZONE),LMODID,SEPTON,NITRON,
     I                     IDAY0,IMON0,IYR0,IDAYN,IMONN,IYRN)
            END IF
          END IF
C
C         initialize accumulators
          CALL INIACC
          SRNFG = 1
C
C         transfer random values to PRZM variables for Monte Carlo
          IF (MCARLO) THEN
            MCTFLG = .FALSE.
            CALL MCPRZ(
     I                 MCTFLG,IPZONE,IPZONE)
          ENDIF
C
CJAM
C         begin change for monte carlo 9-8-91
          IF (THFLAG.EQ.1) CALL THCALC
          IF (KDFLAG.EQ.1) CALL KDCALC
C         end change 9-8-91
CJAM
C
C         initialize variables
C
          LMXZON = MXZONE
          LNCMP2 = NCMPP2
          CALL INITL (
     I                IPZONE,LMXZON,LNCMP2,
     O                CORDND)
C
C         save I.C.s in binary files
          CALL RSTPUT (FPRZRS(IPZONE),IPZONE)
          CALL RSTPT1 (FPRZRS(IPZONE),IPZONE)
C
 10     CONTINUE
      ENDIF
C
      IF (VADFON) THEN
C       vadoft flow on
        FRSTRD = .TRUE.
        MESAGE = 'Reading [VADOFT] flow data'
        CALL PZSCRN(1,MESAGE)
C
        DO 20 IVZONE = 1, NVZONE
C         loop through zones
C
C         initialize accumulators
          CUSMIF = 0.0
          CUSMEF = 0.0
          CUWVIF = 0.0
          CUWVEF = 0.0
C
          FLOSIM = .TRUE.
          IF (MCARLO) THEN
C           rewind files
            IFIL = FVADIN(IVZONE)
            REWIND IFIL
            IFIL = FVRSTF(IVZONE)
            REWIND IFIL
            IFIL = FVRSTT(IVZONE)
            REWIND IFIL
          ENDIF
          IF (NITRON) THEN
C           simulate three nitrogen constituents
            LNCHEM = 3
          ELSE
C           simulate number of chemicals in execution supervisor
            LNCHEM = NCHEM
          END IF
C
          CALL VADINP(
     I                FVADIN(IVZONE),FECHO,FVTP10(IVZONE),NLDLT,LNCHEM,
     I                IVZONE,TRNSIM,FLOSIM,PRZMON,FRSTRD,MCARLO)
          CALL VADPUT(
     I                FVRSTF(IVZONE),IVZONE,FLOSIM)
          IF (TRNSIM) THEN
C           vadoft transport on
            MESAGE = 'Reading [VADOFT] transport data'
            CALL PZSCRN(1,MESAGE)
            FLOSIM = .FALSE.
            CALL VADINP(
     I                 FVADIN(IVZONE),FECHO,FVTP10(IVZONE),NLDLT,LNCHEM,
     I                  IVZONE,TRNSIM,FLOSIM,PRZMON,FRSTRD,MCARLO)
            CALL VADPUT(
     I                  FVRSTT(IVZONE),IVZONE,FLOSIM)
          ENDIF
 20     CONTINUE
        FRSTRD = .FALSE.
      ENDIF
C
      CALL SUBOUT
C
      RETURN
      END SUBROUTINE INPREA
C
C
C
      SUBROUTINE   PRZMRD (LPRZIN, NCHEXE, SEPTON, NITRON,
     O                     IBUFF, BASEND, LINCOD)
C
C     + + + PURPOSE + + +
C     reads and checks input data. also performs some
C     input related calculations such as computing runoff curve numbers
C     for dry and wet antecedent conditions and converting calendar to
C     julian dates.
C     Modification date: 4/26/96 JMC
C
      Use Date_Module
      Use General_Vars!new
      Use Floating_Point_Comparisons
      Use General_Vars
      Use m_CN_functions
      Use m_Crop_Dates
      Use m_Debug   ! m_debug
      Use m_Wind
      Use m_utils
      use m_readvars
c
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4    LPRZIN,BASEND,NCHEXE,KM,I51
      LOGICAL      SEPTON,NITRON
      CHARACTER*1  IBUFF(80)
      CHARACTER*80 LINCOD
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZIN - unit number for przm input file
C     BASEND - ???
C     NCHEXE - ???
C     SEPTON - septic effluent on flag
C     NITRON - nitrogen modeling on flag
C     IBUFF  - ???
C     LINCOD - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'EXAM.INC'
      INCLUDE 'CECHOT.INC'
      INCLUDE 'HLFDUM.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,J,JP1,K,KK,APM,APD,HAM,HAD,MAM,
     1             MAD,EMM,EMD,IBGN,KLIN,JNN,JLIN,ISTRT,IEND,IERROR
      INTEGER*4    N,M,L,IDIFF,I1,CROPNO
      CHARACTER*80 MESAGE
      LOGICAL      FATAL,EOF,FRSTRD
      Integer :: iflit, ios
      Logical :: missing_iflit
      Logical :: was_present, xerror

      ! compartment_epsilon - any residue (defined below) smaller than
      !     compartment_epsilon will be added to the last compartment
      !     of the horizon, otherwise another compartment is needed.
      !     Note that compartment_epsilon is a fraction of DPN.
      !     See examples below.
      Real, Parameter :: compartment_epsilon = 0.10
      Logical :: value_in_range
      Real    :: v_real, v_residue
      Real    :: total_thickness, max_root_zone_depth
      Integer :: v_int, k_begin
      Integer :: y4     ! 4-digit year, e.g., 1967
      Integer :: i_total, i_times, i_block, i_loop
      Integer :: i_beg, i_end, i_pos
      Logical :: error_was_issued
c
c if CAM == 1,2,3 then force soil incorporation depth == 4 cm
      Real, Parameter :: cam123_soil_depth = 4.0 ! cm
C
C     + + + INTRINSICS + + +
      INTRINSIC   MOD,INT
C
C     + + + EXTERNALS + + +
      EXTERNAL  ECHORD,ERRCHK,COMRD2,PRZNRD
C
C     + + + DATA INITIALIZATIONS + + +
C
C     + + + INPUT FORMATS + + +
1000  FORMAT(A78)
1005  FORMAT(3A20)
1006  FORMAT(3(4X,2I2,I8))
1010  FORMAT(10I8)
1015  FORMAT(F8.0,3(I8,F8.0))
1020  FORMAT(8F8.0)
1021  FORMAT(16(I2,I2,1X))
1022  FORMAT(16(F4.2,1X))
1023  FORMAT(2I8)
1024  FORMAT(4F8.0,8X,I8,2F8.0)
1025  FORMAT(14F5.0)
1026  FORMAT(3F8.0)
1027  FORMAT(15I5.0)
1028  FORMAT(15F5.0)
1029  FORMAT(16(I4,1X))
1030  FORMAT(2F8.0,I8,F8.0,2I8,5I4)
1040  FORMAT(I8,3F8.0,I8,3(1X,I3),2F8.0)
1050  FORMAT(F8.0,8X,9I4)
1052  FORMAT(6F8.0)
1053  FORMAT(7F8.0)
1051  FORMAT(I8,6F8.0)
1055  FORMAT(9F8.0)
1065  FORMAT(I8,9F8.0)
1080  FORMAT(2X,3I2,2X,3I2,2X,3I2,I8)
1100  FORMAT(4X,A4,A1,3X,A4,1X,I3,1X,I3,F8.0,7X,A1,I8)
1110  FORMAT(3(4X,A4,4X,A4,I8),I4)
1111  FORMAT(8X,6F8.0)
1115  FORMAT(8X,7F8.0)
1120  FORMAT(8X,9F8.0)
1125  FORMAT(8X,6F8.0)
1130  FORMAT(I8,4X,A4)
1150  FORMAT(2X,3I2,1X,A8,1X,I3,3F8.0)
1151  FORMAT(2X,3I2,I3,3(I2,F5.0,F6.0,F5.0,F5.0))
1160  FORMAT(80A1)
C
1810  FORMAT(I8)
1820  FORMAT(I8,A16)
1830  FORMAT(I8,A16,2I8,F8.0)
C     + + + OUTPUT FORMATS + + +
2000  FORMAT('NDC [',I4,'] is greater than NC [',I4,']')
2010  FORMAT('NCPDS [',I4,'] is greater than MXCPD [',I4,']')
2020  FORMAT('NAPS [',I4,'] is greater than NAPP [',I4,']')
2021  FORMAT('WINDAY [',I2,'] for application [',I2,'] is too large')
2030  FORMAT('NCOM2+1 [',i0,'] is greater than NCMPTS [',i0,']')
2040  FORMAT('NHORIZ [',I4,'] is greater than NCMPTS [',I4,']')
2050  FORMAT('NPLOTS [',I4,'] is greater than 12, only 1st 12  ',
     1       'variables will be written')
2060  FORMAT('Number of chemicals in PRZM [',I1,'] <> number of ',
     1       'chemicals in EXESUP [',I1,']')
C
C     + + + END SPECIFICATIONS + + +
C
      I   = 80
C
      FRSTRD = .TRUE.
C
C     these were not initialized , JAM 4/22/91
      DO 78 M=1,3
        SOL(M)=0.0
        DO 79 L=1,NCMPTS
          ADL(L)   = 0.0
          AD(L)    = 0.0
          DKRW12(L)= 0.0
          DKRW23(L)= 0.0
          DKRW13(L)= 0.0
          DKRS12(L)= 0.0
          DKRS23(L)= 0.0
          DKRS13(L)= 0.0
          OKH(M,L) = 0.0
          Q(L)  = 0.0
          CM(L) = 0.0
          SPT(L)     = 0.0
          SAND(L)    = 0.0
          CLAY(L)    = 0.0
          VHTCAP(L)  = 0.0
          THCOND(L)  = 0.0
          DO 88 N=1,6
            Y(N,M,L)   = 0.0
 88       CONTINUE
 79     CONTINUE
 78   CONTINUE
C     end of corrections ,JAM 4/22/91
C
C     reads in title for PRZM
      LINCOD = ' 1.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1000,END=910,ERR=920) TITLE
C
C     reads in comment line for hydrology parameters
      LINCOD = ' 2.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1000,END=910,ERR=920) HTITLE
C
C     hydrology and sediment production parameters
      LINCOD = ' 3.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1030,END=910,ERR=920)
     1  PFAC,SFAC,IPEIND,ANETD,INICRP,ISCOND,(METDSN(I),I=1,5)
C
      IF (METDSN(1) .GT. 0) THEN
C       check wdm met datasets (call WTFNDT)
      END IF
C
C     reads this if IPEIND = 1 , the daylight hours (12)
      IF (IPEIND.EQ.1 .OR. IPEIND.EQ.2) THEN
        LINCOD = ' 4.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1052,END=910,ERR=920) (DT(I),I=1,6)
        LINCOD = ' 5.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1052,END=910,ERR=920) (DT(I),I=7,12)
      ENDIF
C
C     reads to see if erosion flag is on or off
      LINCOD = ' 6.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1810,END=910,ERR=920) ERFLAG
C
C    Check status of ERosion FLAG take appropriate action (2004-08-13 LAB)
C    ERFLAG = 0 indicates that erosion will not be calculated
      if (ERFLAG.eq.1 .or. ERFLAG.gt.4 .or. ERFLAG.lt.0) then
         IERROR = 2020
         Write (MESAGE,'(" Erosion flag (ERFLAG) out of range")')
         FATAL = .True.
         Call ERRCHK (IERROR, MESAGE, FATAL)
C     if ERFLAG is > 1 then read in erosion parameters
      ELSEIF (ERFLAG .GT. 1) THEN
        LINCOD = ' 7.0B'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1024,END=910,ERR=920)
     *          USLEK,USLELS,USLEP,AFIELD,IREG,SLP,HL
      ELSE ! ERFLAG = 0, no action needed
      ENDIF
C
C     crop information for individual crops
      LINCOD = ' 8.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      missing_iflit = .False.
      
      ! statement of the problem. we are adding a new parameter, flit_num,
      ! which may be present in the przm input file, or not. WE do not want to 
      ! break old przmfiles so we will read the line an try to find new parameter
      ! iwithout aborting if the parameter is not there.
      ! the format the line:
      !  Old: i8
      !  new: i8, 1x, I1
      ! so, the first read the "old" parameters columns 1-9 == length (i8, 1x)
      ! then we pass message(10:10) which should contain or not an extra value.

      !READ(MESAGE(1:9),'(i8)',END=910,ERR=920) NDC

      READ(MESAGE(1:9),1010,END=910,ERR=920) NDC
! read flit_num VERY carefully, since it may be missing from the line
! if an error was detected use the przm message(920)
! if not present assign flit_num a default value.
! the format is (i8, 1x, i1) ==> the second integer (if present) is between columns 9-10
! column 9 oshould be blank.
      call get_int(MESAGE(9:10), was_present, xerror, flit_num)
      if (xerror) go to 920
      missing_iflit = (.not. was_present)

      if (missing_iflit) then
! flit_num is missing, give it a default value.	      
      	flit_num = cn_beta
      end if
      
      select case(flit_num)
      Case(cn_beta, cn_chow)
         ! aceptable values for flit_num
      Case Default
   	! flit_num contains an unrecognized option(number).
        IERROR = 2060
        WRITE(MESAGE,2001) flit_num, cn_beta, cn_chow
2001	format('flit_num == [', i0, 
     &   '] is invalid; appropriate values are ', i0, ' or ', i0, '.')	
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR, MESAGE, FATAL)
      end select 

C
C     check NDC, cannot be > 5
      IF (NDC .GT. NC) THEN
        IERROR = 2060
        WRITE(MESAGE,2000) NDC, NC
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR, MESAGE, FATAL)
      ENDIF
C
C     reads crop parameters up to number of NDC
      LINCOD = ' 9.0'
      DO 40 I=1,NDC
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1040,END=910,ERR=920)
     1       ICNCN(I),CINTCP(I),AMXDR(I),COVMAX(I),ICNAH(I),
     2       (CN(I,KK,2),KK=1,3),WFMAX(I),HTMAX(I)
C
C       generate curve numbers for antecedent conditions I and III
	call Fill_CN_Array()
        !DO K = 1, 3
        !   CN(I,K,1) = cn_1_func(CN(I,K,2))
        !   CN(I,K,3) = cn_3_func(CN(I,K,2))
        !End Do
40    CONTINUE
C
C
      IF (ERFLAG .GT. 1) THEN
        Number_of_Crops = NDC
        Allocate(Crop_Info(Number_of_Crops))
        Do KM = 1, NDC
          LINCOD = ' 9.0A'
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1023,END=910,ERR=920)CROPNO,NUSLEC(KM)

            ! Associate array entries: crop number (CropNo) to ICNCN
            ! Crop Id Number:  ICNCN(1:NDC)
            ! i_pos such that (CROPNO == ICNCN(i_pos))
            i_pos = 0
            CropId: Do i = 1, NDC
               If (CROPNO == ICNCN(i)) Then
                  i_pos = i
                  Exit CropId
               End If
            End Do CropId
            If (i_pos <= 0) Then
               ! error in PRZM input file.
               IERROR = 2065
               WRITE(MESAGE,2820) CROPNO, ICNCN(1:NDC)
2820  FORMAT('CROPNO [',i0,'] not found in ICNCN(1:NDC): ',30(i0,1x))
               FATAL  = .TRUE.
               CALL ERRCHK(IERROR, MESAGE, FATAL)
            End If

            i_total = NUSLEC(KM) ! total number of items to read
            i_block = 16         ! maximum number of items to read
            i_times = Ceiling(Real(i_total) / i_block) ! number of times to loop
            i_end = 0            ! last item read

            ! Allocate storage for new arrays
            Crop_Info(KM)%Crop_Number = CROPNO
            Crop_Info(KM)%nUSELEC = i_total  ! == NUSLEC(KM)
            Allocate(Crop_Info(KM)%doy(i_total),
     &               Crop_Info(KM)%USLE_C(i_total),
     &               Crop_Info(KM)%Manning_N(i_total),
     &               Crop_Info(KM)%CN1(i_total),
     &               Crop_Info(KM)%CN2(i_total),
     &               Crop_Info(KM)%CN3(i_total))

            Do i_loop = 1, i_times
               ! Also, i_beg = (i_loop-1)*i_block + 1
               i_beg = i_end + 1    ! first item to read this time
               i_end = Min(i_beg+i_block-1, i_total)  ! last item to read
               LINCOD = ' 9.0B'
               CALL ECHORD(LPRZIN, LINCOD, FRSTRD,MESAGE)
               READ(MESAGE,1021,END=910,ERR=920)
     *                 (GDUSLEC(i_pos,I),GMUSLEC(i_pos,I),I=i_beg,i_end)
               Crop_Info(KM)%doy(i_beg:i_end) = iDoY(yyyy=Year_for_doy,
     &                             mm=GDUSLEC(i_pos,i_beg:i_end),
     &                             dd=GMUSLEC(i_pos,i_beg:i_end))

               LINCOD = ' 9.0C'
               CALL ECHORD(LPRZIN, LINCOD, FRSTRD,MESAGE)
               READ(MESAGE,1022,END=910,ERR=920)
     *                 (USLEC(i_pos,I),I=i_beg,i_end)
               Crop_Info(KM)%USLE_C(i_beg:i_end) =
     &                        USLEC(i_pos,i_beg:i_end)

               LINCOD = ' 9.0D'
               CALL ECHORD(LPRZIN, LINCOD, FRSTRD,MESAGE)
               READ(MESAGE,1022,END=910,ERR=920)
     *                 (MNGN(i_pos,I),I=i_beg,i_end)
               Crop_Info(KM)%Manning_N(i_beg:i_end) =
     &                        MNGN(i_pos,i_beg:i_end)

               LINCOD = ' 9.0E'
               CALL ECHORD(LPRZIN, LINCOD, FRSTRD,MESAGE)
               READ(MESAGE,1029,END=910,ERR=920)
     *                 (CN(i_pos,I,2),I=i_beg,i_end)
               Crop_Info(KM)%CN2(i_beg:i_end) =
     &                        CN(i_pos,i_beg:i_end,2)


            End Do
C           generate curve numbers for antecedent conditions I and III
            DO K = 1, i_total
               CN(i_pos,K,1) = cn_1_func(CN(i_pos,K,2))
               CN(i_pos,K,3) = cn_3_func(CN(i_pos,K,2))
            End Do
            Crop_Info(KM)%CN1 = cn_1_func(Crop_Info(KM)%CN2)
            Crop_Info(KM)%CN3 = cn_3_func(Crop_Info(KM)%CN2)
        End Do ! Do KM = 1, NDC
        ! If (new_code) Call Aux_1()   ! m_debug
      ENDIF
C
      LEAP=1
      DO 605 KM=1,NDC
        DO 606 I=1,NUSLEC(KM)
          JUSLEC(KM,I)= GDUSLEC(KM,I)+ CNDMO(LEAP,GMUSLEC(KM,I))
606     CONTINUE
605   CONTINUE
C
C     crop rotation information, number of cropping periods
      LINCOD = '10.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1810,END=910,ERR=920) NCPDS
C
C     crop rotation information, number of cropping periods
C
C     check NCPDS
      IF (NCPDS .GT. MXCPD) THEN
        IERROR = 2070
        WRITE(MESAGE,2010) NCPDS, MXCPD
        FATAL  = .TRUE.
        CALL ERRCHK( IERROR, MESAGE, FATAL)
      ENDIF
C
      ! Allocate events array.
      ! Remember: PRZM year is (effectively) years since 1900.
      !           "Jd" requires 4-digit year.
      Nevents = ncpds
      If (Allocated(Crop_Period)) Deallocate(Crop_Period)
      Allocate(Crop_Period(Nevents))

C     reads emergence, maturation, and harvest dates up to NCPDS
      MESAGE = ''
      WRITE(KECHOT,1000)MESAGE
      LINCOD = '11.0'
      DO 50 I=1,NCPDS
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1080,END=910,ERR=920)
     1              EMD,EMM,IYREM(I),MAD,MAM,IYRMAT(I),HAD,HAM,
     2              IYRHAR(I),INCROP(I)
C
C       determine julian dates from calendar dates
        LEAP=1
        IF (MOD(IYREM(I),4) .EQ. 0) LEAP= 2
        IEMER(I)= EMD+ CNDMO(LEAP,EMM)

        LEAP= 1
        IF (MOD(IYRMAT(I),4) .EQ. 0) LEAP= 2
        MAT(I) = MAD+ CNDMO(LEAP,MAM)

        LEAP= 1
        IF (MOD(IYRHAR(I),4) .EQ. 0) LEAP= 2
        IHAR(I)= HAD+CNDMO(LEAP,HAM)

        y4 = IYREM(I) + iybase ! 4-digit year, e.g., 1967
        Crop_Period(i)%jd_emergence = Jd(yyyy=y4, mm=EMM, dd=EMD)

        y4 = IYRMAT(I) + iybase
        Crop_Period(i)%jd_maturation = Jd(yyyy=y4, mm=MAM, dd=MAD)

        y4 = IYRHAR(I) + iybase
        Crop_Period(i)%jd_harvest = Jd(yyyy=y4, mm=HAM, dd=HAD)

        Crop_Period(i)%jd_begin = Crop_Period(i)%jd_emergence
        Crop_Period(i)%jd_end = Crop_Period(i)%jd_harvest
        Crop_Period(i)%CropPeriod = i
        Crop_Period(i)%Crop_Number = INCROP(I)

50    CONTINUE

      ! Sort events chronologically.
      Call Events_Sort()

C     reads pesticide title
      LINCOD = '12.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1000,END=910,ERR=920) PTITLE
C
C     pesticide application information
C     new addition --- farm flag -jam 4/24/91
C     farm flag allows window application dates
      LINCOD = '13.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      FRMFLG=0
      DK2FLG=0
      READ(MESAGE,4130,END=910,ERR=920) NAPS,NCHEM,FRMFLG,DK2FLG
4130  FORMAT(4I8)
C
C     check NAPS
      IF (NAPS .GT. NAPP) THEN
        IERROR = 2080
        WRITE(MESAGE,2020) NAPS, NAPP
        FATAL  = .TRUE.
        CALL ERRCHK( IERROR, MESAGE, FATAL)
      ENDIF
      DO I51=1,NAPP ! do 51 ...
         IAPYR(I51)  = 0
         IAPDY(I51)  = 0
         WINDAY(I51) = 0
      end do 		! 51 continue
      WIN = 0
C
      IF (.NOT.NITRON) THEN
C       check NCHEXE to make sure it = Run file NCHEM
        IF (NCHEXE .NE. NCHEM) THEN
          IERROR = 2010
          WRITE(MESAGE,2060) NCHEM, NCHEXE
          FATAL  = .TRUE.
          CALL ERRCHK(IERROR,MESAGE,FATAL)
        ENDIF
      END IF
C
      IF (NCHEM .EQ. 0) NCHEM = 1
CJMC Add DK2FLG to allow two phase degradation
      IF(DK2FLG.NE.0)THEN
        LINCOD = '14.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1006) (DKDAY(K),DKMNTH(K),DKNUM(K),K=1,NCHEM)
      ENDIF
      LINCOD = '15.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1005) (PSTNAM(K),K=1,NCHEM)
C
      LINCOD = '16.0'
C     new line added for farm flag
C     allows a window for pesticide application (integer)
        DO 58 I=1,NAPS
          CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
            READ(MESAGE,1151,END=910,ERR=920)
     1      APD,APM,IAPYR(I),WINDAY(I),
     2      (CAM(K,I),DEPI(K,I),TAPP(K,I),
     3       APPEFF(K,I),DRFT(K,I),K=1,NCHEM)
           APDEX(I)=APD
           APMEX(I)=APM
C
C       determine julian application date
        LEAP = 1
        IF (MOD(IAPYR(I),4) .EQ. 0) LEAP = 2
        IAPDY(I) = APD+ CNDMO(LEAP,APM)
58    CONTINUE
      FAM=0
      DO 172 I=1,NAPS
        DO 173 K=1,NCHEM
          IF (CAM(K,I) .EQ. 2 .OR. CAM(K,I) .EQ. 3
     *       .OR. CAM(K,I) .EQ. 9 .OR. CAM(K,I) .EQ. 10)FAM=2
 173    CONTINUE
 172  CONTINUE


! [lsr] 22 Jan 2003 10:41 am.
! if CAM == 1,2,3 then force soil incorporation depth (DEPI) == 4 cm
! if CAM == 4-10, then DEPI must be >= DPN(1) (see PRZM manual,
!               section 4, page 4-22, Record 16: CAM)

      DO I = 1, NAPS
         DO K = 1, NCHEM
            Select Case(CAM(K,I))
               Case(1:3)
                  If (DEPI(K,I) .NotEqual. cam123_soil_depth) Then
                     WRITE(MESAGE,2180) K, I, DEPI(K,I),
     *                  cam123_soil_depth, CAM(K,I)
 2180 FORMAT('Warning, DEPI(', i0, ',', i0, ') changed from ',
     *                  f0.1, ' to ', f0.1,
     *                  ' because CAM is equal to ', i0)
                     IERROR= 2180
                     FATAL = .False.
                     CALL ERRCHK(IERROR,MESAGE,FATAL)
                     DEPI(K,I) = cam123_soil_depth
                  End If

               Case(4:10)
                  If (DEPI(K,I) .LessThan. DPN(1)) Then
                     WRITE(MESAGE,2190) K, I, DEPI(K,I),
     *                  DPN(1), CAM(K,I)
 2190 FORMAT('Warning, DEPI(', i0, ',', i0, ') changed from ',
     *                  f0.1, ' to ', f0.1,
     *                  ' because CAM is equal to ', i0)
                     IERROR= 2190
                     FATAL = .False.
                     CALL ERRCHK(IERROR,MESAGE,FATAL)
                     DEPI(K,I) = DPN(1)
                  End If

               Case Default
                  ! Range check: All values of CAM should be handled
                  ! explicitly above.
                  WRITE(MESAGE,2200) K, I, CAM(K,I)
 2200 FORMAT('Error, CAM(', i0, ',', i0, ') == ', i0,
     *                  ' is out of the valid range 1-10')
                  IERROR= 2200
                  FATAL = .True.
                  CALL ERRCHK(IERROR,MESAGE,FATAL)

            End Select
         End Do
      End Do

C     make sure winday is shorter than difference between two app. dates
      DO 59 I = 1,NAPS
        IDIFF = 0
        I1 = I + 1
        IF (I1 .LE. NAPS) THEN
          IF (IAPYR(I).EQ.IAPYR(I+1)) THEN
            IDIFF = IAPDY(I+1) - IAPDY(I)
            IF (WINDAY(I).GE.IDIFF) THEN
              IERROR = 2160
              WRITE(MESAGE,2021) WINDAY(I),I
              FATAL = .TRUE.
              CALL ERRCHK(IERROR,MESAGE,FATAL)
            ENDIF
          ENDIF
        ENDIF
59    CONTINUE
C
C     reads soil application model (1-8)
      LINCOD = '17.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1015,END=910,ERR=920) FILTRA,
     *     (IPSCND(K),UPTKF(K),K=1,NCHEM)
C
      !debug
      ! record 18 should be read also if cam= 9,10
      ! make sure cam=9&10 are processed just like cam=2&3
      IF(FAM.EQ.2)THEN
C       plant pesticide parameters, reads if CAM = 2 or 3
        LINCOD = '18.0'
        DO 70 K=1,NCHEM
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1026,END=910,ERR=920)PLVKRT(K),PLDKRT(K),FEXTRC(K)
70      CONTINUE
      ENDIF
C
      IF((FAM.EQ.2).AND.(NCHEM.GT.1))THEN
C       plant pesticide parameters, reads if CAM = 2 or 3
C       and number of chemicals is >1
        LINCOD = '18.0A'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1026,END=910,ERR=920)PTRN12,PTRN13,PTRN23
      ENDIF
C
C     reads in comment title for soil properties
      LINCOD = '19.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1000,END=910,ERR=920) STITLE
C
C     soil profile and pesticide transport parameters
      LINCOD = '20.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1050,END=910,ERR=920)
     1  CORED,BDFLAG,THFLAG,KDFLAG,HSWZT,MCFLAG,IRFLAG,ITFLAG,
     2  IDFLAG,BIOFLG

      ! ITFLAG valid?
      Select Case(ITFLAG)
      Case(0, 1, 2)
         ! Valid code. Do nothing.
      Case Default
         ! Invalid code. Abort.
         WRITE(MESAGE,3020) ITFLAG
 3020    FORMAT('ITFLAG [ ', i0, ' ] was not 0, 1 or 2.')
         IERROR= 6130
         FATAL = .True.
         CALL ERRCHK(IERROR,MESAGE,FATAL)
      End Select

C
C    reads in biodegradation values if BIOFLG is on.
      IF (BIOFLG .EQ. 1) THEN
        LINCOD = '21.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1053,END=910,ERR=920)
     1    AM,AC,AS,AR,KE
C
C    reads in biodegradation values if BIOFLG is on.
        LINCOD = '22.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1053,END=910,ERR=920)
     1    KSM,KCM,KC,MKS,KR,KIN,KSK
C
C    reads in biodegradation values if BIOFLG is on.
        LINCOD = '23.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1053,END=910,ERR=920)
     1    KLDM,KLDC,KLDS,KLDR,KL1,KL2
C
C    reads in biodegradation values if BIOFLG is on.
        LINCOD = '24.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1053,END=910,ERR=920)
     1    USM,UCM,MUC,US,UR
C
C    reads in biodegradation values if BIOFLG is on.
        LINCOD = '25.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1053,END=910,ERR=920)
     1    YSM,YCM,YC,YS,YR
      ENDIF
C
C     reads in pesticide specific data
      LINCOD = '26.0'
      CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
      READ(MESAGE,1055,END=910,ERR=920)
     1    (DAIR(I),I=1,NCHEM),(HENRYK(I),I=1,NCHEM),(ENPY(I),I=1,NCHEM)
C
C     reads in irrigation parameters if IRFLAG > 0
C     new option allows IRFLAG = 2 to irrigate only during crop period
      IF(IRFLAG .NE. 0)THEN
        LINCOD = '27.0'
        CALL ECHORD(
     I     LPRZIN, LINCOD, FRSTRD,
     O     MESAGE)
        READ (MESAGE,1051,END=910,ERR=920) IRTYPE,FLEACH,PCDEPL,
     1                                      RATEAP,UC
C
      value_in_range = (0.0 <= PCDEPL) .And. (PCDEPL <= 0.9)
      If (.Not. value_in_range) Then
         WRITE(MESAGE,3000) PCDEPL
 3000    FORMAT('Warning: PCDEPL = ', f0.2, ' was not in the range ',
     *          '0 <= PCDEPL <= 0.9; PCDEPL was reset to 0.5')
         IERROR= 2210
         FATAL = .False.
         CALL ERRCHK(IERROR,MESAGE,FATAL)
         PCDEPL = 0.5
      End If
c
C       reads this line only if furrow irrigation is desired (ITYPE=2)
        IF(IRTYPE .EQ.2)THEN
          LINCOD = '28.0'
          CALL ECHORD(
     I       LPRZIN, LINCOD, FRSTRD,
     O       MESAGE)
          READ(MESAGE,1020,END=910,ERR=920)Q0,BT,ZRS,SF,EN,XL,XFRAC
          LINCOD = '29.0'
          CALL ECHORD(
     I       LPRZIN, LINCOD, FRSTRD,
     O       MESAGE)
          READ(MESAGE,1020,END=910,ERR=920)KS,HF
        END IF
      END IF
C
C     reads in sorption partition params if KDFLAG = 1
      IF (KDFLAG .EQ. 1) THEN
        LINCOD = '30.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1040,END=910,ERR=920) PCMC,(SOL(K),K=1,NCHEM)
      ENDIF

      ! Read parameters for soil temperature simulation ?
      R31_32: Select Case(ITFLAG)
      Case(1, 2)
        LINCOD = '31.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ (MESAGE,1025,END=910,ERR=920)
     1    (ALBEDO(I),I=1,12), EMMISS, uWind_Reference_Height

        LINCOD = '32.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ (MESAGE,1025,END=910,ERR=920)
     1    (BBT(I),I=1,12)

        ! reads in Q10FAC and TBASE
        LINCOD = '32.0A'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ (MESAGE,1020,END=910,ERR=920)(QFAC(K),K=1,NCHEM),
     *                                    (TBASE(K),K=1,NCHEM)

      Case Default
         QFAC = 1.0     ! effectively no temperature correction.
         TBASE = 0
      End Select R31_32

      ! Read record 32b only if (ITFLAG == 2)
      R32ab: Select Case(ITFLAG)
      Case(2)
        LINCOD = '32.0B'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
          READ (MESAGE,1920,END=910,ERR=920)
     &         (MSFLG(k),MSEFF(k),MSLAB(k),k=1,NCHEM)
1920      FORMAT(3(I8,2F8.0))

          ! MSFLG valid ?
          ! Check all NCHEM values before aborting.
          error_was_issued = .False.
          Do k = 1, NCHEM
             Select Case(MSFLG(k))
             Case(MS_Absolute_FC, MS_Relative_FC)
               ! Valid codes; do nothing.

             Case Default
               ! Invalid code. Issue a fatal error and stop.
               WRITE(MESAGE,3040) k, MSFLG(k)
 3040          FORMAT('MSFLG(',i0,') [ ', i0, ' ] was not 1 or 2.')
               IERROR= 6140
               FATAL = .False.
               CALL ERRCHK(IERROR,MESAGE,FATAL)
               error_was_issued = .True.
             End Select
          End Do
          If (error_was_issued) Then
            WRITE(MESAGE,3050)
 3050       FORMAT('Errors detected. PRZM stopped.')
            IERROR= 6150
            FATAL = .True.
            CALL ERRCHK(IERROR,MESAGE,FATAL)
          End If

      Case Default
         ! MSFLG neither assigned nor used if (ITFLAG != 2).
         ! Give MSFLG a default value (not 1, 2) so that
         ! "Select Case" is usable in all cases.
         MSFLG = 0
         MSEFF = 0.0
         MSLAB = 1.0
      End Select R32ab

C
C     reads in number of horizons
      LINCOD = '33.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1010,END=910,ERR=920) NHORIZ
C
C     check NHORIZ
      IF (NHORIZ .GT. NCMPTS) THEN
        IERROR = 2090
        WRITE(MESAGE,2040) NHORIZ, NCMPTS
        FATAL  = .TRUE.
        CALL ERRCHK( IERROR, MESAGE, FATAL)
      ENDIF
C
      DO 80 I=1,NHORIZ
C         read in soil params + drainage
          LINCOD = '34.0'
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1065,END=910,ERR=920)
c****** ADL IS ADDED TO READ IN HORIZONTAL FLOW TIME CONSTANT *******
     1    HORIZN(I),THKNS(I),BD(I),THETO(I),AD(I),
     2    (DISP(K,I),K=1,NCHEM),ADL(I)
C
C     read in biodegradation values here
      IF (BIOFLG .EQ. 1) THEN
        LINCOD = '35.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
          READ(MESAGE,1111,END=910,ERR=920)
     1    Q(I),CM(I),Y(1,1,I),Y(2,1,I),Y(3,1,I),Y(4,1,I)
      ENDIF
C
C     reads in degradation rates
        LINCOD = '36.0'
        IF(DK2FLG.EQ.0)THEN
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
          READ(MESAGE,1120,END=910,ERR=920)
     1      (DWRAT1(K,I),K=1,NCHEM),(DSRAT1(K,I),K=1,NCHEM),
     2      (DGRAT1(K,I),K=1,NCHEM)
           DO 335 J=1,NCHEM
              DDW(J,I)=DWRAT1(J,I)
              DDS(J,I)=DSRAT1(J,I)
              DDG(J,I)=DGRAT1(J,I)
              DWRAT1(J,I)=EXP(DWRAT1(J,I))-1.
              DSRAT1(J,I)=EXP(DSRAT1(J,I))-1.
              DGRAT1(J,I)=EXP(DGRAT1(J,I))-1.
              DWRATE(J,I)=DWRAT1(J,I)
              DSRATE(J,I)=DSRAT1(J,I)
              DGRATE(J,I)=DGRAT1(J,I)
 335       CONTINUE
        ELSE
            LINCOD = '36.0'
            CALL ECHORD(
     I        LPRZIN, LINCOD, FRSTRD,
     O        MESAGE)
            READ(MESAGE,1120,END=910,ERR=920)
     1        (DWRAT1(K,I),K=1,NCHEM),(DSRAT1(K,I),K=1,NCHEM),
     2        (DGRAT1(K,I),K=1,NCHEM)
           DO 336 J=1,NCHEM
              DDW1(J,I)=DWRAT1(J,I)
              DDS1(J,I)=DSRAT1(J,I)
              DDG1(J,I)=DGRAT1(J,I)
              DWRAT1(J,I)=EXP(DWRAT1(J,I))-1.
              DSRAT1(J,I)=EXP(DSRAT1(J,I))-1.
              DGRAT1(J,I)=EXP(DGRAT1(J,I))-1.
              DWRATE(J,I)=DWRAT1(J,I)
              DSRATE(J,I)=DSRAT1(J,I)
              DGRATE(J,I)=DGRAT1(J,I)
 336       CONTINUE
            LINCOD = '36.A'
            CALL ECHORD(
     I        LPRZIN, LINCOD, FRSTRD,
     O        MESAGE)
            READ(MESAGE,1120,END=910,ERR=920)
     1        (DWRAT2(K,I),K=1,NCHEM),(DSRAT2(K,I),K=1,NCHEM),
     2        (DGRAT2(K,I),K=1,NCHEM)
           DO 337 J=1,NCHEM
              DDW2(J,I)=DWRAT2(J,I)
              DDS2(J,I)=DSRAT2(J,I)
              DDG2(J,I)=DGRAT2(J,I)
              DWRAT2(J,I)=EXP(DWRAT2(J,I))-1
              DSRAT2(J,I)=EXP(DSRAT2(J,I))-1
              DGRAT2(J,I)=EXP(DGRAT2(J,I))-1
 337       CONTINUE
        ENDIF
C
C         reads in these soil params if these flags
          LINCOD = '37.0'
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1115,END=910,ERR=920)
     1        DPN(I),THEFC(I),THEWP(I),OC(I),(KD(K,I),K=1,NCHEM)
C
C         reads in temp, %sand, %clay, thermal conductivity, heat cap.
          IF (ITFLAG .EQ. 1) THEN
            LINCOD = '38.0'
            CALL ECHORD(
     I        LPRZIN, LINCOD, FRSTRD,
     O        MESAGE)
            READ(MESAGE,1120,END=910,ERR=920)
     1        SPT(I),SAND(I),CLAY(I),THCOND(I),VHTCAP(I)
          ENDIF
C
C     read transformation rates if NCHEM > 1
      IF (NCHEM .GT. 1) THEN
      LINCOD = '39.0'
          IF(DK2FLG.EQ.0)THEN
            CALL ECHORD(
     I         LPRZIN, LINCOD, FRSTRD,
     O         MESAGE)
            READ(MESAGE,1125,END=910,ERR=920)
     1         DKRW12(I),DKRW13(I),DKRW23(I),
     *         DKRS12(I),DKRS13(I),DKRS23(I)
               DDKW12(I)=DKRW12(I)
               DDKW13(I)=DKRW13(I)
               DDKW23(I)=DKRW23(I)
               DDKS12(I)=DKRS12(I)
               DDKS13(I)=DKRS13(I)
               DDKS23(I)=DKRS23(I)
               DKRW12(I)=EXP(DKRW12(I))-1
               DKRW13(I)=EXP(DKRW13(I))-1
               DKRW23(I)=EXP(DKRW23(I))-1
               DKRS12(I)=EXP(DKRS12(I))-1
               DKRS13(I)=EXP(DKRS13(I))-1
               DKRS23(I)=EXP(DKRS23(I))-1
          ELSE
            LINCOD = '39.0'
            CALL ECHORD(
     I         LPRZIN, LINCOD, FRSTRD,
     O         MESAGE)
            READ(MESAGE,1125,END=910,ERR=920)
     1         DKW112(I),DKW113(I),DKW123(I),
     2         DKS112(I),DKS113(I),DKS123(I)
               DDKW112(I)=DKW112(I)
               DDKW113(I)=DKW113(I)
               DDKW123(I)=DKW123(I)
               DDKS112(I)=DKS112(I)
               DDKS113(I)=DKS113(I)
               DDKS123(I)=DKS123(I)
               DKW112(I)=EXP(DKW112(I))-1
               DKW113(I)=EXP(DKW113(I))-1
               DKW123(I)=EXP(DKW123(I))-1
               DKS112(I)=EXP(DKS112(I))-1
               DKS113(I)=EXP(DKS113(I))-1
               DKS123(I)=EXP(DKS123(I))-1
            LINCOD = '39.A'
            CALL ECHORD(
     I         LPRZIN, LINCOD, FRSTRD,
     O         MESAGE)
            READ(MESAGE,1125,END=910,ERR=920)
     1         DKW212(I),DKW213(I),DKW223(I),
     1         DKS212(I),DKS213(I),DKS223(I)
               DDKW212(I)=DKW212(I)
               DDKW213(I)=DKW213(I)
               DDKW223(I)=DKW223(I)
               DDKS212(I)=DKS212(I)
               DDKS213(I)=DKS213(I)
               DDKS223(I)=DKS223(I)
               DKW212(I)=EXP(DKW212(I))-1
               DKW213(I)=EXP(DKW213(I))-1
               DKW223(I)=EXP(DKW223(I))-1
               DKS212(I)=EXP(DKS212(I))-1
               DKS213(I)=EXP(DKS213(I))-1
               DKS223(I)=EXP(DKS223(I))-1
          ENDIF
        ENDIF
80    CONTINUE

      ! Calculate NCOM2, number of compartments
      !
      ! Divide horizon KLIN, of thickness THKNS(KLIN) into JNN compartments of
      ! of width DPN(KLIN)
      ! JNN is number of compartments in horizon
      ! k_begin and NCOMBE -- beginning compartment number for horiz KLIN
      ! IBGN and NCOMEN    -- end compartment number for horiz KLIN
      ! compartment_epsilon - defined above.
      ! v_real -- (real value) number of compartments needed to span THKNS(KLIN)
      ! v_int  -- (integer value) truncated integer part of v_real
      !
      ! Example #1:
      !   Let THKNS = 1.45, and DPN = 0.70
      !       v_real = 1.45/0.70 = 2.07
      !       v_int = Int(2.07) = 2
      !       v_Residue = v_real-v_int = 0.07
      !       The residue is smaller than compartment_epsilon, therefore
      !           the number of compartments is JNN = v_int = 2.
      !           The residue will be absorbed by the last compartment.
      !           The width of the first JNN-1 (1) compartments is THKNS = 0.70
      !           The width of the last compartment (JNN) is: THKNS - (JNN-1)*DPN = 0.75
      !
      ! Example #2:
      !   Let THKNS = 1.45, and DPN = 0.32
      !       v_real = 1.45/0.32 = 4.53
      !       v_int = Int(4.53) = 4
      !       v_Residue = v_real-v_int = 4.53 - 4 = 0.53
      !       The residue is greater than compartment_epsilon, therefore
      !           one more compartment is needed: JNN = v_int + 1 = 5.
      !           The width of the first JNN-1 (4) compartments is THKNS = 0.32
      !           The width of the last compartment (JNN) is: THKNS - (JNN-1)*DPN = 0.17

      IBGN = 0
      DO KLIN = 1, NHORIZ
         ! The case THKNS < DPN is absurd. Max() ensures at least one compartment.
         v_real = Max(THKNS(KLIN) / DPN(KLIN), 1.0)
         v_int = Int(v_real)
         v_residue = Abs(v_real - v_int)     ! 0 <= v_residue < 1
         If (v_residue <= compartment_epsilon) Then
            ! See example #1 above.
            JNN = v_int
         Else
            ! See example #2 above.
            JNN = v_int + 1
         End If
         k_begin = IBGN + 1
         IBGN = k_begin + JNN - 1
         NCOMBE(KLIN) = k_begin
         NCOMEN(KLIN) = IBGN
         ! We will catch IBGN > NCMPTS on exit and inform the user
         ! on the number of compartments needed.
         If (IBGN <= NCMPTS) Then   ! DELX(NCMPTS)
            DELX(k_begin:IBGN) = DPN(KLIN)               ! Set all JNN compartments
            DELX(IBGN) = THKNS(KLIN) - (JNN-1)*DPN(KLIN) ! Fix last JNN compartment
         End If
      End Do

      total_thickness = Sum(THKNS(1:NHORIZ))
      max_root_zone_depth = MaxVal(AMXDR(1:NDC))
      If (max_root_zone_depth > total_thickness) Then
         IERROR = 2220
         WRITE(MESAGE,3220) total_thickness, max_root_zone_depth
3220     FORMAT('Sum(THKNS(1:NHORIZ)) [', f0.2,
     &         '] is less than Max(AMXDR(1:NDC)) [', f0.2, ']')
         FATAL = .False.      ! Only inform the user.
         CALL ERRCHK( IERROR, MESAGE, FATAL)

         ! Add the difference to the last soil slice (compartment).
         ! Adjust related parameters.

         If (IBGN <= NCMPTS) Then   ! DELX(NCMPTS)
            v_residue = Max(max_root_zone_depth - total_thickness, 0.0)
            DELX(IBGN) = DELX(IBGN) + v_residue
            THKNS(NHORIZ) = THKNS(NHORIZ) + v_residue
            total_thickness = Sum(THKNS(1:NHORIZ))
            CORED = total_thickness
         End If
      End If

      NCOM2 = IBGN

      ! check NCOM2 < Dimension[DelX(NCMPTS)]
      IF (NCOM2+1 > NCMPTS) THEN
        IERROR = 2100
        WRITE(MESAGE,2030) NCOM2, NCMPTS
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      ENDIF
C
C     initial pesticide levels if desired
C     zero PESTR array here
      DO 95 K=1,NCHEM
        DO 90 I=1,NCOM2
          PESTR(K,I)=0.0
          SPESTR(K,I) = 0.0
          Y(1,K,I) = Y(1,1,I)
          Y(2,K,I) = Y(2,1,I)
          Y(3,K,I) = Y(3,1,I)
          Y(4,K,I) = Y(4,1,I)
90      CONTINUE
95    CONTINUE
C
C     read flag for initial levels of pest. + conversion
      LINCOD = '40.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1010,END=910,ERR=920) ILP,CFLAG
      IF (ILP.EQ.1) THEN
        LINCOD = '41.0'
        DO 97 K = 1, NCHEM
          DO 98 ISTRT = 1, NCOM2, 8
            IEND = ISTRT + 7
            IF (IEND.GT.NCOM2) IEND = NCOM2
            CALL ECHORD(
     I        LPRZIN, LINCOD, FRSTRD,
     O        MESAGE)
            READ(MESAGE,1020,END=910,ERR=920)
     1        (PESTR(K,I),I=ISTRT,IEND)
 98       CONTINUE
 97     CONTINUE
      ENDIF
C
      IF (NITRON) THEN
C       nitrogen transport being simulated, read input parameters
        CALL PRZNRD (LPRZIN,FRSTRD,SEPTON,
     O               LINCOD)
      END IF
C
C     summary output information
      LINCOD = '42.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1110,END=910,ERR=920)
     1  ITEM1,STEP1,LFREQ1,ITEM2,STEP2,LFREQ2,ITEM3,STEP3,LFREQ3,EXMFLG
C
      IF (ERFLAG .EQ. 0) EXMFLG = 0
C
      IF(EXMFLG.GT.0)THEN
C     EXAMS input data/create exams batch file
        LINCOD = '43.0'
        CALL ECHORD(
     I    LPRZIN, LINCOD, FRSTRD,
     O    MESAGE)
        READ(MESAGE,1810,END=910,ERR=920)EXMENV
        IF(NCHEM.EQ.1)THEN
          LINCOD = '44.0'
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1820,END=910,ERR=920)EXMCHM(1),CASSNO(1)
        ELSE
          DO 197 K = 1, NCHEM
            LINCOD = '44.0'
            CALL ECHORD(
     I        LPRZIN, LINCOD, FRSTRD,
     O        MESAGE)
            READ(MESAGE,1830,END=910,ERR=920)EXMCHM(K),CASSNO(K),
     *                               NPROC(K),RFORM(K),YIELD(K)
 197      CONTINUE
        ENDIF
      ENDIF
C
      IF(EXMFLG.EQ.1)CALL OUTEXA
C
C     time series output information
      LINCOD = '45.0'
      CALL ECHORD(
     I  LPRZIN, LINCOD, FRSTRD,
     O  MESAGE)
      READ(MESAGE,1130,END=910,ERR=920) NPLOTS,STEP4
C
C     check NPLOTS
      IF (NPLOTS .GT. 12) THEN
        IERROR = 2110
        WRITE(MESAGE,2050) NPLOTS
        FATAL  = .FALSE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
        NPLOTS = 12
      ENDIF
      IF (NPLOTS .GT. 0) THEN
        LINCOD = '46.0'
        DO 100 I=1,NPLOTS
          CALL ECHORD(
     I      LPRZIN, LINCOD, FRSTRD,
     O      MESAGE)
          READ(MESAGE,1100,END=910,ERR=920) PLNAME(I),INDX(I),
     1      MODE(I),IARG(I),IARG2(I),CONST(I),PLTYP(I),PLTDSN(I)
          IF (PLTYP(I) .EQ. ' ') PLTYP(I) = 'P'
100     CONTINUE
      ENDIF
      RETCOD=0
C
C     special actions
      SAVAL = 9999
      SAYR  = 9999
      LINCOD = '47.0'
      CALL COMRD2(
     I  LPRZIN,
     O  MESAGE, EOF)
      IF (EOF) GO TO 990
      READ(MESAGE,1000,END=990,ERR=920) ATITLE
      LINCOD = '48.0'
      CALL COMRD2(
     I  LPRZIN,
     O  MESAGE, EOF)
      IF (EOF) GO TO 990
      READ(MESAGE,1150,END=990,ERR=920)
     1      SADAY,SAMON,SAYR,SPACT,NACTS,(SPACTS(K),K=1,3)
      I = 1
      IF (MOD(SAYR,4) .EQ. 0 .AND. MOD(SAYR,100) .NE. 0) I = 2
      SAVAL = SADAY + CNDMO(I,SAMON)
      GO TO 990
C
910   CONTINUE
C
C     end of file found too soon
      RETCOD=1
C
C     get record
      BACKSPACE (LPRZIN)
      READ (LPRZIN,1160) IBUFF
      GO TO 990
C
920   CONTINUE
C
C     error found on read
      RETCOD=2
C
C     get record
      BACKSPACE (LPRZIN)
      READ (LPRZIN,1160) IBUFF
C
990   CONTINUE
C
C     pass NCOM2 as the base node for PRZM to VADOFT link
      BASEND = NCOM2
C

c

C
      RETURN

      Contains
      Subroutine Aux_1()
         ! Print crop parameters  ! m_debug
         Implicit None
         Integer :: KM

         DO KM = 1, NDC
            Write (802, *) 'KM = ', KM, ', NUSLEC(KM) = ', NUSLEC(KM)

4010        Format(1x, 3x, 'ICNCN = ', I8, ', Rest: ', 3F8.2,I8,2F8.2)
            Write (802, 4010)
     1       ICNCN(KM),CINTCP(KM),AMXDR(KM),COVMAX(KM),ICNAH(KM),
     2       WFMAX(KM),HTMAX(KM)

            Write (802, 4020) (GDUSLEC(KM,I),GMUSLEC(KM,I),
     &                               I=1,NUSLEC(KM))
4020        Format (1x, 3x, 32(i2.2,i2.2, 3x))

            Write (802, 4040) (USLEC(KM,I),I=1,NUSLEC(KM))
            Write (802, 4040) (MNGN(KM,I),I=1,NUSLEC(KM))
4040        Format (1x, 3x, 32(f5.3, 2x))

            Write (802, *) '   CN AMC ii, i, iii follow:'
            Write (802, 4060) (CN(KM,I,2),I=1,NUSLEC(KM))
            Write (802, 4060) (CN(KM,I,1),I=1,NUSLEC(KM))
            Write (802, 4060) (CN(KM,I,3),I=1,NUSLEC(KM))
4060        Format (1x, 3x, 32(i2, 5x))

            Write (802, '(/)')
         End Do
      End Subroutine Aux_1

      Subroutine Aux_2()
         ! Print crop parameters (derived type)  ! m_debug
         Implicit None
         Integer :: KM

         DO KM = 1, NDC
!            Allocate(Crop_Info(KM)%doy(i_total),
!     &               Crop_Info(KM)%USLE_C(i_total),
!     &               Crop_Info(KM)%Manning_N(i_total),
!     &               Crop_Info(KM)%CN1(i_total),
!     &               Crop_Info(KM)%CN2(i_total),
!     &               Crop_Info(KM)%CN3(i_total))
!      Integer :: Crop_Number = e_Bogus
!      Real :: Max_Interception_Storage = 0.0
!      Real :: Max_Rooting_depth = 0.0
!      Real :: Max_Areal_canopy_coverage = 0.0
!      Integer :: nUSELEC = e_Bogus
!      Integer, Dimension(:), Pointer :: doy => Null()
!      Real, Dimension(:), Pointer :: USLE_C => Null()
!      Real, Dimension(:), Pointer :: Manning_N => Null()
!      Integer, Dimension(:), Pointer :: CN1 => Null()
!      Integer, Dimension(:), Pointer :: CN2 => Null()
!      Integer, Dimension(:), Pointer :: CN3 => Null()

            Write (802, 9220) Crop_Info(KM)%Crop_Number
9220        Format (/, 1x, 'Crop Number: ', i0)

            Write (802, 9240) 'Max_Interception_Storage',
     &           Crop_Info(KM)%Max_Interception_Storage
            Write (802, 9240) 'Max_Rooting_depth',
     &           Crop_Info(KM)%Max_Rooting_depth
            Write (802, 9240) 'Max_Areal_canopy_coverage',
     &           Crop_Info(KM)%Max_Areal_canopy_coverage
9240        Format (1x, 3x, a, f7.3)

            Write (802, '(/)')
        End Do
      End Subroutine Aux_2

      End Subroutine Przmrd
C
C
      SUBROUTINE   INIACC
C
C     + + + PURPOSE + + +
C     initialize all accumulators to zero
C     Modofication date: 2/14/92 JAM
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMISC.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CSPTIC.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,K
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL    SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'INIACC'
      CALL SUBIN(MESAGE)

! From Dirk Young/DC/USEPA/US 10/20/04 12:08 PM
! THETN is actually the begining day water content at this point
! in the program because the call to IRRIG occurs before the
! hydrologic updates in HYDR1. Thus in the IRRIG routine, the
! definition of THETN is contrary to the manual's definition.
!
! Related to this issue is that since THETN is not updated by
! the time IRRIG is called, on the first day of the simulation
! water content is zero, which will cause irrigation to always
! occur on the first day of the simulation -- that is because
! THETN is initialized to zero (see file RSinp.for, subroutine
! INIACC, line 1369).  I  suggest that you change THETN to be
! initialized with the same values as THETO (which are read in
! from the input file).
!
! See also subroutine IRRIG.

      THETN = THETO
      DO 10 I = 1,NCOM2
        ET(I)     = 0.0
        ! THETN(I)  = 0.0     ! See comment above.
        VEL(I)    = 0.0
        THETAS(I) = 0.0
        OUTFLO(I) = 0.0
        MINPW(I)  = 0.0
        MOUTW(I)  = 0.0
        MEOUTW(I) = 0.0
        YEOUTW(I) = 0.0
        YOUTW(I)  = 0.0
        MSTR(I)   = 0.0
        YSTR(I)   = 0.0
        MOOUTW(I) = 0.0
        YOOUTW(I) = 0.0
        AINF(I)   = 0.0
        LINF(I)   = 0.0
10    CONTINUE
      DO 11, I=1,NCOM2
        YINPW(I)  = 0.0
11    CONTINUE
      DO 30 K = 1, NCHEM
        DO 20 I = 1, NCOM2
cjmc  wterm now is dimensioned by ncom2,nchem
          GAMMA(K,I)  = 0.0
          WTERM(K,I)  = 0.0
          MINPP(K,I)  = 0.0
          MINPP2(K,I) = 0.0
          MOUTP(K,I)  = 0.0
          MSTRP(K,I)  = 0.0
          MDOUT(K,I)  = 0.0
          VOUTM(K,I)  = 0.0
          YINPP(K,I)  = 0.0
          YINPP2(K,I) = 0.0
          YOUTP(K,I)  = 0.0
          YSTRP(K,I)  = 0.0
          YDOUT(K,I)  = 0.0
          VOUTY(K,I)  = 0.0
          MTRFM(K,I)  = 0.0
          YTRFM(K,I)  = 0.0
          MLOUT(K,I)  = 0.0
          YLOUT(K,I)  = 0.0
          IF(DK2FLG.EQ.1)THEN
            DSRATE(K,I) = 0.0
            DWRATE(K,I) = 0.0
            DGRATE(K,I) = 0.0
          ENDIF
20      CONTINUE
30    CONTINUE
      AINF(NCOM2+1) = 0.0
      RUNOF  = 0.0
      CWBAL  = 0.0
      SNOW   = 0.0
      OSNOW  = 0.0
      MINPW1 = 0.0
      MINPW2 = 0.0
      MOUTW1 = 0.0
      MOUTW2 = 0.0
      MOUTW3 = 0.0
      MOUTW4 = 0.0
      MOUTW5 = 0.0
      MOUTW6 = 0.0
      MSTR1  = 0.0
      MSTR2  = 0.0
      YINPW1 = 0.0
      YINPW2 = 0.0
      YOUTW1 = 0.0
      YOUTW2 = 0.0
      YOUTW3 = 0.0
      YOUTW4 = 0.0
      YOUTW5 = 0.0
      YOUTW6 = 0.0
      YSTR1  = 0.0
      YSTR2  = 0.0
      DO 40 K = 1, NCHEM
        IF(DK2FLG.EQ.1)THEN
          DKRW12(K)=0.0
          DKRW13(K)=0.0
          DKRW23(K)=0.0
          DKRS12(K)=0.0
          DKRS13(K)=0.0
          DKRS23(K)=0.0
          DKSTAT(K)=0
        ENDIF
        CRPAPP(K)=0
        CPBAL(K)  =0.0
        MINPP1(K) = 0.0
        MINPP8(K) = 0.0
        MOUTP1(K) = 0.0
        MOUTP2(K) = 0.0
        MOUTP3(K) = 0.0
        MOUTP4(K) = 0.0
        MOUTP5(K) = 0.0
        MOUTP6(K) = 0.0
        MOUTP7(K) = 0.0
        MOUTP8(K) = 0.0
        MOUTP9(K) = 0.0
        MSTRP1(K) = 0.0
        YINPP1(K) = 0.0
        YINPP8(K) = 0.0
        YOUTP1(K) = 0.0
        YOUTP2(K) = 0.0
        YOUTP3(K) = 0.0
        YOUTP4(K) = 0.0
        YOUTP5(K) = 0.0
        YOUTP6(K) = 0.0
        YOUTP7(K) = 0.0
        YOUTP8(K) = 0.0
        YOUTP9(K) = 0.0
        YSTRP1(K) = 0.0
        DCOFLX(K) = 0.0
        MCOFLX(K) = 0.0
        YCOFLX(K) = 0.0
        SDKFLX(K) = 0.0
        SUPFLX(K) = 0.0
        LATFLX(K) = 0.0
        FPDLOS(K) = 0.0
        FPVLOS(K) = 0.0
        FOLP0(K)  = 0.0
        FOLPST(K) = 0.0
        YRINF1(K)  = 0.0
        YRFLX1(K)  = 0.0
        YRINF2(K)  = 0.0
        YRFLX2(K)  = 0.0
40    CONTINUE
      DOUTFL = 0.0
      MOUTFL = 0.0
      YOUTFL = 0.0
      LEAP   = 0
      DOM    = 0
      MONTH  = 0
      JULDAY = 0
      IY     = 0
      RETCOD = 0
      IFIRST = 0
      CEVAP  = 0.0
      CINT   = 0.0
      DIN    = 0.0
      SMELT  = 0.0
      PRECIP = 0.0
      SNOWFL = 0.0
      THRUFL = 0.0
      TDET   = 0.0
      SEDL   = 0.0
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   KDCALC
C
C     + + + PURPOSE + + +
C     computes Kd values for each soil layer by
C     one of three methods, developed by (1) Karickhoff
C                                        (2) Kenaga
C                                        (3) Chiou
C     these models work for non ionic compounds that exhibit
C     linear adsorption properties
C     Modification date: 2/14/92 JAM
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CPEST.INC'
      INCLUDE 'CMISC.INC'
C
C     + + + LOCAL VARIABLES + + +
      REAL         LOGKOC,KOC
      INTEGER*4    I,K
      CHARACTER*80 MESAGE
C
C     + + + FUNCTIONS + + +
      REAL   LOGCHK
C
C     + + + EXTERNALS + + +
      EXTERNAL  SUBIN,SUBOUT,LOGCHK
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'KDCALC'
      CALL SUBIN(MESAGE)
C
      DO 20 K=1,NCHEM
        DO 10 I=1,NHORIZ
          IF (PCMC .EQ. 1) THEN
C           Karickhoff model  (SOL(K) = MOLE FRACTION/LITER)
            LOGKOC= (-0.54 * LOGCHK(SOL(K)))+ 0.44
          ELSEIF (PCMC .EQ. 2) THEN
C           Kenaga model      (SOL(K) = MILLIGRAMS/LITER)
            LOGKOC= 3.64- (0.55*LOGCHK(SOL(K)))
          ELSE
C           Chiou model       (SOL(K) = MICROMOLES/LITER)
            LOGKOC= 4.04- (0.557*LOGCHK(SOL(K)))
          ENDIF
          KOC     = 10.**LOGKOC
            IF (PCMC .EQ. 4) KOC = SOL(K)
            KD(K,I) = KOC * (OC(I)/100.)
            KOC = 0.0
10      CONTINUE
20    CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   MCPRZ
     I                  (OUT,IZ,NMCDAY)
C
C     + + + PURPOSE + + +
C     transfers PRZM variables between Monte Carlo arrays
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4 IZ,NMCDAY
      LOGICAL   OUT
C
C     + + + ARGUMENT DEFINITIONS + + +
C     IZ     - ???
C     NMCDAY - ???
C     OUT    - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMCRVR.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CNITR.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,IELMNT,ICHM,II
      REAL*8       YMC
      CHARACTER*80 MESAGE
C
C     + + + FUNCTIONS + + +
      INTEGER    FNDCHM
C
C     + + + INTRINSICS + + +
      INTRINSIC  NINT,REAL
C
C     + + + EXTERNALS + + +
      EXTERNAL   SUBIN,PZCHK,FNDHOR,MAXAVG,SUBOUT,FNDCHM
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'MCPRZ'
      CALL SUBIN(MESAGE)
C
C     transfer random inputs to PRZM variables:
      IF(.NOT. OUT)THEN
        DO 20 I=1,MCVAR
          IF(INDZ(I,1).EQ.IZ)THEN
            II = IND1(I,1)
            ICHM = FNDCHM(PNAME(I))
C
C           soil bulk density BD (g/cm^3):
            IF (PNAME(I) .EQ. 'BULK DENSITY')THEN
                        BD(II) = RMC(I)
C
C           wilting point (cm3/cm3):
            ELSE IF (PNAME(I) .EQ. 'WILTING POINT')THEN
                        THEWP(II) = RMC(I)
C
C           field capacity (cm3/cm3):
            ELSE IF (PNAME(I) .EQ. 'FIELD CAPACITY')THEN
                        THEFC(II) = RMC(I)
C
C           organic carbon content (%):
            ELSE IF (PNAME(I) .EQ. 'ORGANIC CARBON')THEN
                        OC(II) = RMC(I)
C
C           pesticide solubility
            ELSE IF (PNAME(I)(1:3) .EQ. 'KOC') THEN
                     SOL(ICHM) = RMC(I)
C
C           application amount (KG/HA):
            ELSE IF (PNAME(I)(1:11) .EQ. 'APPLICATION')THEN
                        TAPP(ICHM,II) = RMC(I)
C
C           dispersion coefficient (cm2/day):
            ELSE IF (PNAME(I)(1:10) .EQ. 'DISPERSION')THEN
                        DISP(ICHM,II) = RMC(I)
C
C           decay rate in water (days^-1):
            ELSE IF (PNAME(I)(1:11) .EQ. 'WATER DECAY')THEN
                        DWRATE(ICHM,II) = RMC(I)
C
C           decay rate of vapor (days^-1):
            ELSE IF (PNAME(I)(1:11) .EQ. 'VAPOR DECAY')THEN
                        DGRATE(ICHM,II) = RMC(I)
C
C           decay rate of sorbed chemical  (days^-1):
            ELSE IF (PNAME(I)(1:12) .EQ. 'SORBED DECAY')THEN
                        DSRATE(ICHM,II) = RMC(I)
C
C           Henry's constant:
            ELSE IF (PNAME(I)(1:15) .EQ. 'HENRYS CONSTANT')THEN
                        HENRYK(ICHM) = RMC(I)
C
C           irrigation triggering moisture level (fraction):
            ELSE IF (PNAME(I) .EQ. 'IRRIG LEVEL')THEN
                        PCDEPL = RMC(I)
C
C           application year:
            ELSE IF (PNAME(I) .EQ. 'APP YEAR')THEN
                        IAPYR(II) = NINT(RMC(I))
C
C           Julian application day:
            ELSE IF (PNAME(I) .EQ. 'APP DAY')THEN
                        IAPDY(II) = NINT(RMC(I))
C
            ELSE IF (PNAME(I) .EQ. 'NO3 APPLICATION') THEN
C             nitrate application (kg/ha)
              TAPP(2,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NH3 APPLICATION') THEN
C             ammonia application (kg/ha)
              TAPP(1,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'ORGN APPLICATION') THEN
C             organic N application (kg/ha)
              TAPP(3,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'PLANTN UPTAKE') THEN
C             plant N uptake rate (/day)
              KPLN(II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'BG PLANT N RETURN') THEN
C             below groud plant return rate (/day)
              KRETBN(II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'AG PLANT N RETURN') THEN
C             above ground plant return rate (/day)
              KRETAN(II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NH4 DESORPTION') THEN
C             ammonium desorption rate (/day)
              NPM(1,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NH4 ADSORPTION') THEN
C             ammonium adsorption rate (/day)
              NPM(2,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NO3 IMMOBILIZATION') THEN
C             nitrate immobilization rate (/day)
              NPM(3,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'AMMONIFICATION') THEN
C             organic N ammonification rate (/day)
              NPM(4,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'DENITRIFICATION') THEN
C             denitrification rate (/day)
              NPM(5,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NITRIFICATION') THEN
C             nitrification rate (/day)
              NPM(6,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NH4 IMMOBILIZATION') THEN
C             ammonium immobilization rate (/day)
              NPM(7,II) = RMC(I)
            ELSE IF (PNAME(I) .EQ. 'NH3 VOLATILIZATION') THEN
C             ammonia volatilization rate (/day)
              NPM(8,II) = RMC(I)
            END IF
          END IF
   20   CONTINUE
C
C       special checks for consistency of generated numbers:
        CALL PZCHK
C
      ELSE
C       transfer PRZM outputs to Monte Carlo arrays:
        DO 30 I=1,NVAR
          IF(INDZ(I,2).EQ.IZ)THEN
            II = IND1(I,2)
            ICHM = FNDCHM(SNAME(I,1))
C
C           soil bulk density BD (g/cm^3)
            IF (SNAME(I,1) .EQ. 'BULK DENSITY')THEN
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = BD(IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'WILTING POINT')THEN
C             wilting point (cm3/cm3):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = THEWP(IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'FIELD CAPACITY')THEN
C             Field Capacity (cm3/cm3):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = THEFC(IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'ORGANIC CARBON')THEN
C             organic carbon content (%):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = OC(IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:3) .EQ. 'KOC') THEN
C             pesticide solubility
              YMC = SOL(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:11) .EQ. 'APPLICATION')THEN
C             application amount, chemical 1 (KG/HA):
              YMC = 1.E5*TAPP(ICHM,II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:10) .EQ. 'DISPERSION')THEN
C             dispersion coefficient (cm2/day):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = DISP(ICHM,IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:11) .EQ. 'WATER DECAY')THEN
C             decay rate in water (days^-1):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = DWRATE(ICHM,IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:11) .EQ. 'VAPOR DECAY')THEN
C             decay rate of vapor (days^-1):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = DGRATE(ICHM,IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:12) .EQ. 'SORBED DECAY')THEN
C             decay rate of sorbed chemical 1 (days^-1):
              CALL FNDHOR(
     I                    II, NCOM2, HORIZN,
     O                    IELMNT)
              YMC = DSRATE(ICHM,IELMNT)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:15) .EQ. 'HENRYS CONSTANT')THEN
C             Henry's constant:
              YMC = HENRYK(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'IRRIG LEVEL')THEN
C             irrigation level:
              YMC = PCDEPL
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'APP YEAR')THEN
C             application year:
              YMC = REAL(IAPYR(II))
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'APP DAY')THEN
C             Julian application day:
              YMC = REAL(IAPDY(II))
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'THETA')THEN
C             soil water content THETN (cm3/cm3)
              YMC = THETN(II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:14) .EQ. 'SOIL PESTICIDE')THEN
C             total soil pesticide (Chemical 1) (KG/HA):
              YMC = PESTR(ICHM,II)*DELX(II)*
     1               THETN(II)*1.E5
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'INFILTRATION')THEN
C             infiltration depth (CM):
              YMC = AINF(II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'RUNOFF')THEN
C             runoff depth (CM):
              YMC = RUNOF
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'PRECIPITATION')THEN
C             precipitation (CM):
              YMC = PRECIP
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'EVAPOTRANSPIRATION')THEN
C             evapotranspiration (CM):
              YMC = ET(II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'IRRIG DEPTH')THEN
C             flood or furrow application depth:
              YMC = APDEP
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:11) .EQ. 'RUNOFF FLUX')THEN
C             runoff flux, chemical 1 (kg/ha)
              YMC = 1.E5*ROFLUX(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:12) .EQ. 'EROSION FLUX')THEN
C             erosion flux, chemical 1 (kg/ha)
              YMC = 1.E5*ERFLUX(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:10) .EQ. 'DECAY FLUX')THEN
C             decay flux, chemical 1 (kg/ha)
              YMC = 1.E5*DKFLUX(ICHM,II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:11) .EQ. 'VOLAT. FLUX')THEN
C             volat. flux, chemical 1 (kg/ha)
              YMC = 1.E5*PVFLUX(ICHM,II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:10) .EQ. 'PLANT FLUX')THEN
C             plant flux, chemical 1 (kg/ha)
              YMC = 1.E5*UPFLUX(ICHM,II)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:9) .EQ. 'ROOT FLUX')THEN
C             root zone flux, chemical 1 (kg/ha)
              YMC = 1.E5*RZFLUX(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:10) .EQ. 'CORE FLUX')THEN
C             bottom of core flux, chemical 1 (kg/ha/day)
C             dcoflx passed in with units of kg/ha from slpst0
C             and slpst1 subroutines
              YMC = DCOFLX(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1)(1:15) .EQ. 'TOTAL CORE FLUX')THEN
C             bottom of core flux, chemical 1 (kg/ha)
C             ycoflx passed in with units of kg/ha from slpst0
C             and slpst1 subroutines
              YMC = YCOFLX(ICHM)
              CALL MAXAVG(
     I                    NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                    STOR,XMC(I))
C
            ELSE IF (SNAME(I,1) .EQ. 'RUNOFF FLUX NH3') THEN
C             runoff flux, ammonia
              YMC = NCFX1(4,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(I,1) .EQ. 'RUNOFF FLUX NO3') THEN
C             runoff flux, nitrate
              YMC = NCFX1(5,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(I,1) .EQ. 'RUNOFF FLUX ORGN') THEN
C             runoff flux, organic N
              YMC = NCFX1(6,1) + NCFX1(7,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(I,1) .EQ. 'EROSION FLUX NH3') THEN
C             erosion flux, ammonia
              YMC = NCFX1(2,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(I,1) .EQ. 'EROSION FLUX ORGN') THEN
C             runoff flux, organic N
              YMC = NCFX1(1,1) + NCFX1(3,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'GW FLUX NH3') THEN
C             groundwater flux, ammonia
              YMC = NCFX2(NCOM2,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'GW FLUX NO3') THEN
C             groundwater flux, nitrate
              YMC = NCFX4(NCOM2,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'GW FLUX ORGN') THEN
C             groundwater flux, organic N
              YMC = NCFX13(NCOM2,1) + NCFX15(NCOM2,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'GW FLUX TOTN') THEN
C             groundwater flux, total N
              YMC = NCFX2(NCOM2,1) + NCFX4(NCOM2,1) +
     $              NCFX13(NCOM2,1) + NCFX15(NCOM2,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'UPTAKE FLUX NH3') THEN
C             plant uptake flux, ammonia
              YMC = NCFX21(NCOM2+1,1) + NCFX23(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'UPTAKE FLUX NO3') THEN
C             plant uptake flux, nitrate
              YMC = NCFX20(NCOM2+1,1) + NCFX22(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'UPTAKE FLUX TOTN') THEN
C             plant uptake flux, total N
              YMC = NCFX21(NCOM2+1,1) + NCFX23(NCOM2+1,1) +
     $              NCFX20(NCOM2+1,1) + NCFX22(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'RETURN FLUX ORGN') THEN
C             plant return flux, organic N
              YMC = NCFX25(NCOM2+1,1) + NCFX26(NCOM2+1,1) +
     $              NCFX27(NCOM2+1,1) + NCFX28(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'IMMOBIL. FLUX NH4') THEN
C             immobilization flux, ammonium
              YMC = NCFX8(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'IMMOBIL. FLUX NO3') THEN
C             immobilization flux, nitrate
              YMC = NCFX17(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'IMMOBIL. FLUX TOTN') THEN
C             immobilization flux, total N
              YMC = NCFX8(NCOM2+1,1) + NCFX17(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'VOLATIL. FLUX') THEN
C             volatilization flux, ammonia
              YMC = NCFX18(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'DENIT. FLUX') THEN
C             denitrification flux
              YMC = NCFX6(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'NITRIFICATION FLUX') THEN
C             nitrification flux
              YMC = NCFX12(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            ELSE IF (SNAME(1,I) .EQ. 'AMMONIFIC. FLUX') THEN
C             ammonification flux
              YMC = NCFX9(NCOM2+1,1)
              CALL MAXAVG (NMAX,NPMAX,I,NMCDAY,NAVG(I),YMC,
     O                     STOR,XMC(I))
            END IF
          END IF
   30   CONTINUE
C
      END IF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      FUNCTION   FNDCHM(
     I                  A)
C
C     + + + PURPOSE + + +
C     Function to find chemical number for chemical-specific variables.
C     FNDCHM is designed for Monte-Carlo character labels in which the
C     chemical number is the last non-blank character, i.e.: "CONC 1".
C     The function returns a value of 1, 2, or 3, with 1 as the
C     default value of FNDCHM.
C     Modification date: 2/14/92 JAM
C
C     + + + ARGUMENTS + + +
      CHARACTER*20 A
C
C     + + + ARGUMENT DEFINITIONS + + +
C     A - the monte carlo character label (up to 20 characters in length)
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    FNDCHM,I
      CHARACTER*1  BLNK
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL   SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'FNDCHM'
      CALL SUBIN(MESAGE)
C
      BLNK = ' '
      FNDCHM = 1
      DO 100 I=20,1,-1
        IF(A(I:I) .NE. BLNK)THEN
          IF(A(I:I) .EQ. '1')THEN
            FNDCHM = 1
          ELSE IF(A(I:I) .EQ. '2')THEN
            FNDCHM = 2
          ELSE IF(A(I:I) .EQ. '3')THEN
            FNDCHM = 3
          END IF
          GO TO 111
        END IF
  100 CONTINUE
C
  111 CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   FNDHOR
     I                   (II, NCOM2, HORIZN,
     O                    IELMNT)
C
C     + + + PURPOSE + + +
C     find number of first compartment in horizon NO. II
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4 II,IELMNT,NCOM2,HORIZN(NCOM2)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     II     - ???
C     IELMNT - ???
C     NCOM2  - ???
C     HORIZN - ???
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    ICOM,IERROR
      LOGICAL      FATAL
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL     SUBIN,ERRCHK,SUBOUT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT('First element for horizon [',I3,'] not found')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE='FNDHOR'
      CALL SUBIN(MESAGE)
C
      DO 199 ICOM = 1, NCOM2
        IELMNT = ICOM
        IF (HORIZN(ICOM) .EQ. II) GO TO 999
 199  CONTINUE
C
      IERROR = 5110
      WRITE(MESAGE,2000) II
      FATAL = .TRUE.
      CALL ERRCHK(IERROR,MESAGE,FATAL)
C
 999  CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   PZCHK
C
C     + + + PURPOSE + + +
C     Subroutine checks generated PRZM variables for consistency and
C     adjusts values if appropriate
C     Modification date: 2/14/92 JAM
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I
      REAL         ORGM,BDTEM,THTEM
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL    SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE='PZCHK'
      CALL SUBIN(MESAGE)
C
C     check soil horizon variables:
      DO 10 I=1,NHORIZ
C       calculation of porosity from INITL:
        ORGM=OC(I)*1.724
        BDTEM = BD(I)
        IF (BDFLAG.EQ.1) BDTEM=100./(ORGM/0.224+(100.-ORGM)/BDTEM)
        THTEM=1.0-BDTEM/2.65
C       check wilting point, field capacity:
        IF(THEFC(I) .GT. THTEM)THEFC(I) = THTEM - .001
        IF(THEWP(I) .GT. THEFC(I))THEWP(I) = THEFC(I) - .001
   10 CONTINUE
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   MAXAVG(
     I                    NMAX,NPMAX,IVAR,NMCDAY,NAVG,Y,
     O                    STOR,X)
C
C     + + + PURPOSE + + +
C     find the maximum average value for monte-carlo
C     outputs over specified periods (i.e. the maximum 5-day dosage)
C     Modification date: 2/14/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4 NMAX,NPMAX,IVAR,NMCDAY,NAVG
      REAL*8    Y,STOR(NPMAX,NMAX),X
C
C     + + + ARGUMENT DEFINITIONS + + +
C     NMAX   - ???
C     NPMAX  - ???
C     IVAR   - ???
C     NMCDAY - ???
C     NAVG   - ???
C     Y      - ???
C     STOR   - ???
C     X      - ???
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    K
      REAL         SUM
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
      INTRINSIC     REAL,ABS
C
C     + + + EXTERNALS + + +
      EXTERNAL     SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'MAXAVG'
      CALL SUBIN(MESAGE)
C
      IF(NMCDAY .LT. NAVG)THEN
C     if the number of days is less than the averaging period, store
C     the daily value of variable IVAR:
        STOR(NMCDAY,IVAR) = Y
      ELSE
C     if the elapsed number of days is greater than the averaging
C     period, compute the average value for the period and compare
C     to the previous maximum average:
        STOR(NAVG,IVAR) = Y
        SUM = 0.0
        DO 100 K=1,NAVG
          SUM = SUM + STOR(K,IVAR)/REAL(NAVG)
  100   CONTINUE
        IF(NMCDAY .EQ. NAVG) X = SUM
        IF(ABS(SUM) .GT. ABS(X)) X = SUM
C       reset the time series storage array for the next averaging
C       period by dropping the first value at the start of the
C       current averaging period:
        DO 200 K=2,NAVG
          STOR(K-1,IVAR) = STOR(K,IVAR)
  200   CONTINUE
C
      END IF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   INITL
     I                  (IPRZM,LMXZON,LNCMP2,
     O                   CORDND)
C
C     + + + PURPOSE + + +
C     initializes variables
C     Modification date: 8/25/92 JAM
C
      Use m_Crop_Dates
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   IPRZM,LMXZON,LNCMP2
      REAL      CORDND(LMXZON,LNCMP2)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     IPRZM  - current przm run number
C     LMXZON - local version of MXZONE
C     LNCMP2 - local version of NCMPP2
C     CORDND - nodal coordinates
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'CSPTIC.INC'
      INCLUDE 'CNITR.INC'
C
C     + + + LOCAL VARIABLES + + +
      REAL         POS,RZD,TTHKNS,ORGM,MODFC,T,TOL,RATIO1,TOP1,
     1             DEPTH,AAA,DDLNI,DDLNJ,DDLNK,CELLBG,TREM,TDIF,LNC,
     2             MIDTOT,DDLN,DELMID,U
      INTEGER      I,J,JB,IB,ISTDY,IENDY,NEYR,NBYR,SJDAY,IBM1,
     1             RODPTH,ILIN,JLIN,KLIN,M,K,KK,IERROR,NCM2P2,
     2             MINDIF,IDFF,LPAD,MTROK
      CHARACTER*80 MESAGE
      LOGICAL      FATAL
      Logical :: In_Cropping_Period
      Integer :: jPos
      Logical :: qfound_id, qfound_cp
C
C     + + + INTRINSICS + + +
      INTRINSIC   MOD,AMAX1,NINT,ABS,DBLE
C
C     + + + EXTERNALS + + +
      EXTERNAL    SUBIN,ERRCHK,SUBOUT,COPYR
C
C     + + + OUTPUT STATEMENTS + + +
 2100 FORMAT('Soil profile description is incomplete, data available ',
     1       'for',F5.2,' of',F5.2,' cm')
 2010 FORMAT('Sum of horizon thicknesses exceeds core depth')
 2120 FORMAT('Calculated value of soil moisture exceeds the saturation',
     1       ' value')
 2150 FORMAT('Horizon into which septic effluent is to be introduced ',
     $       '> number of horizons.')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'INITL'
      CALL SUBIN(MESAGE)
C
C     initialize hydrologic variables
      ILIN = 0
      DDLNI= 0.0
6077  CONTINUE
        ILIN = ILIN + 1
        DDLNI = DDLNI + DELX(ILIN)
      IF (ANETD .GT. DDLNI) GO TO 6077
      NCOM0 = ILIN
      NCOM2M= NCOM2- 1
C
      DO 777 I=1,12
        OUTPUJ(I)=0.0
        OUTPJJ(I)=0.0
777   CONTINUE
C     initialize henry's law constant for first time here
      DO 535 K = 1, NCHEM
        AOFF(K)=-1
        DO 530 I = 1,NCOM2
          OKH(K,I) = HENRYK(K)
 530    CONTINUE
 535  CONTINUE
      TTHKNS = 0.0
      DO 5 I = 1, NHORIZ
        TTHKNS = THKNS(I) + TTHKNS
5     CONTINUE
      TOL = 0.01
      IF (TTHKNS .GT. CORED+TOL) THEN
        IERROR = 2120
        WRITE(MESAGE,2010)
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      ENDIF
      IF (TTHKNS .LT. CORED-TOL) THEN
        WRITE(MESAGE,2100) TTHKNS, CORED
        IERROR = 2130
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      ENDIF
      IF (SEPHZN.GT.NHORIZ) THEN
C       septic effluent introduced too deep
        WRITE(MESAGE,2150)
        IERROR = 2170
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      END IF
C
      NCM2P2 = NCOM2 + 2
      POS    = 0.0
      CORDND(IPRZM,1) = POS
      DO  6 I = 1, NCOM2
        IF (I .EQ. 1) THEN
          POS = DELX(I) / 2.0
        ELSE
          POS = POS + (DELX(I) + DELX(I-1)) / 2.0
        ENDIF
        CORDND(IPRZM,I+1) = POS
 6    CONTINUE
C
      CORDND(IPRZM,NCM2P2) = POS + DELX(NCOM2) / 2.0
C
      DO 10 I=1,NHORIZ
        ORGM=OC(I)*1.724
        IF (BDFLAG.EQ.1) BD(I)=100./(ORGM/0.224+(100.-ORGM)/BD(I))
        THETAS(I)=1.0-BD(I)/2.65
C
C       check that calculated THEFC is less than THETAS (carried over
C       from THCALC)
        IF (THEFC(I) .GE. THETAS(I)) THEN
          IERROR = 2140
          WRITE(MESAGE,2120)
          FATAL  = .TRUE.
          CALL ERRCHK(IERROR,MESAGE,FATAL)
        ENDIF
10    CONTINUE
C
C     determine initial crop conditions -
      ! SJDAY - Julian Starting Day of Simulation
      ! ISTYR - Starting Year of Simulation
      ! IYREM - Year of Crop Emergence
      ! IEMER - Julian Day of Crop Emergence
      ! IYRHAR - Year of Crop Harvest
      ! IHAR  - Julian Day of Crop Harvest
      ! ncpds - Number of Cropping Periods in the simulation
      LEAP = 1
      IF (MOD(ISTYR,4).EQ.0 .AND. MOD(ISTYR,100).NE.0) LEAP = 2
      SJDAY= ISDAY+CNDMO(LEAP,ISMON)
c
      ! Find starting cropping period and crop number.
      ! Find_Crop_Number will always determine
      !     NCP == cropping period number
      !     NCROP === crop id number
      Call Find_Crop_Number (Jd_Begin_Simul, In_Cropping_Period,
     &                       NCP, NCROP, jPos)

      ! If the start of simulation is not contained in a cropping
      ! period and there is more than one crop (NDC > 1) then use
      ! INICRP to determine the soil conditions between the start
      ! of the simulation and the emergence date of the first
      ! cropping period.
      If (.Not. In_Cropping_Period) Then
         qfound_id = .False.  ! found crop id number
         qfound_cp = .False.  ! found cropping period
         If (NDC > 1) Then
            ! Crop Id Number:  ICNCN(1:NDC)
            ! Find the array position associated with crop number INICRP.
            ! Note: INICRP defined only if ERFlag == 0
            CropId: Do i = 1, NDC
               If (INICRP == ICNCN(i)) Then
                  qfound_id = .True.
                  NCROP = i
                  Exit CropId
               End If
            End Do CropId

            ! Crop number associated with Cropping periods:  InCrop(1:NCPDS)
            ! Find the first cropping period associated with crop number INICRP.
            CropCp: Do i = 1, NCPDS
               If (INICRP == INCROP(i)) Then
                  qfound_cp = .True.
                  NCP = i
                  Exit CropCp
               End If
            End Do CropCp
         End If
         ! We could test here qfound_id and qfound_cp.
         ! This coherence test should be performed on input:   ! m_debug
         ! * InCrop(1:NCPDS) contained in ICNCN(1:NDC) and viceversa,
         ! * INICRP in ICNCN(1:NDC),
         ! * CROPNO in ICNCN(1:NDC)
      End If
      ! NCP and NCROP are defined.
c
! m_debug:  date manipulation
C Determine which USLEC to begin simulation with
        LPAD=0
        IUSLEC=0
        DO 325 I=1,NUSLEC(NCROP)
          IF(LEAP.EQ.1)THEN
            IDFF=-365
            IF(JUSLEC(NCROP,I).LE.SJDAY)THEN
              IF(IDFF.LE.JUSLEC(NCROP,I)-SJDAY)IUSLEC=I
              IDFF=JUSLEC(NCROP,I)-SJDAY
              IUSLEC=I
            ENDIF
          ELSE
            LPAD=0
            IDFF=-366
            IF(JUSLEC(NCROP,I).GT.59)LPAD=1
            IF(JUSLEC(NCROP,I)+LPAD.LE.SJDAY)THEN
              IF(IDFF.LE.JUSLEC(NCROP,I)+LPAD-SJDAY)IUSLEC=I
              IDFF=JUSLEC(NCROP,I)+LPAD-SJDAY
              IUSLEC=I
            ENDIF
          ENDIF
 325    CONTINUE
        IF(IUSLEC.EQ.0)THEN
          DO 425 I=1,NUSLEC(NCROP)
            IF(LEAP.EQ.1)THEN
              IF(IDFF.EQ.-365)THEN
                IDFF=365
                IF(JUSLEC(NCROP,I).GT.SJDAY)THEN
                  IF(IDFF.GT.JUSLEC(NCROP,I)-SJDAY)IUSLEC=I
                  IDFF=JUSLEC(NCROP,I)-SJDAY
                  IUSLEC=I
                ENDIF
            ENDIF
            ELSE
              LPAD=0
              IF(IDFF.EQ.-366)THEN
                IDFF=366
                IF(JUSLEC(NCROP,I).GT.59)LPAD=1
                IF(JUSLEC(NCROP,I)+LPAD.GT.SJDAY)THEN
                  IF(IDFF.GT.JUSLEC(NCROP,I)+LPAD-SJDAY)IUSLEC=I
                  IDFF=JUSLEC(NCROP,I)+LPAD-SJDAY
                  IUSLEC=I
                ENDIF
              ENDIF
            ENDIF
 425      CONTINUE
        ENDIF
C
        IF(IDFF.LT.0)THEN
          UCFLG=0
        ELSEIF(IDFF.EQ.0)THEN
          UCFLG=2
        ELSEIF(IDFF.GT.0)THEN
          UCFLG=1
        ENDIF
C       initial conditions are now set
C
! m_debug:  date manipulation
C       find the total number of days from emergence date
C       to crop maturity for beginning crop
        TNDGS(NCP)= 0
        NBYR= IYREM(NCP)
        NEYR= IYRMAT(NCP)
        DO 110 I= NBYR,NEYR
          ISTDY= 0
          IF (IYREM(NCP) .EQ. I) ISTDY= IEMER(NCP)
          IENDY= 365
          IF (I .NE. IYREM(NCP) .AND. I .NE. IYRMAT(NCP) .AND.
     1      MOD(I,4) .NE. 0 .AND. MOD(I,100) .NE. 0) IENDY= 366
          IF (IYRMAT(NCP) .EQ. I) IENDY=MAT(NCP)
          TNDGS(NCP)= IENDY- ISTDY+ TNDGS(NCP)
110     CONTINUE
C
C       find the total number of days from emergence date
C       to crop maturity for beginning crop
        NDCNT= 0
        NBYR= IYREM(NCP)
        NEYR= ISTYR
        DO 120 I= NBYR,NEYR
          ISTDY= 0
          IF (IYREM(NCP) .EQ. I) ISTDY= IEMER(NCP)
          IENDY= 365
          IF (I .NE. IYREM(NCP) .AND. I .NE. ISTYR .AND.
     1      MOD(I,4) .NE. 0 .AND. MOD(I,100) .NE. 0) IENDY= 366
          IF (ISTYR .EQ. I) IENDY=SJDAY
          NDCNT= IENDY- ISTDY+ NDCNT
120     CONTINUE
        ISCOND = 2
C
C       now check to see if we are past the harvest date
        IF ((ISTDY.GE.IHAR(NCP) .AND. ISTYR.EQ.IYRHAR(NCP)) .OR.
     1    (ISTYR.GT.IYRHAR(NCP))) THEN
C         WE ARE PAST THE HARVEST DATE
          RZI= 0
          NDCNT= 0
          ! m_debug -- ICNAH Warning: Do we need
          !    If (ErFlag == 0) Then
          !       ISCOND = ICNAH(NCROP)
          !    End If
          ! How is the value of ISCOND determined when (ErFlag != 0) ?
          ISCOND = ICNAH(INCROP(NCP))
        ENDIF
C
C
C
C     determine number of compartments in each horizon,
C     use this number for distributing fractions and storages from nitrogen
C     inputs in each horizon equally to the compartments within
      IF (NHORIZ.GT.1) THEN
C       look through horizons from bottom to top as in loop below (160)
        TTHKNS = 0.0
        TREM = 0.0
        T = 0.0
        DO 140 I = NHORIZ,2,-1
          TTHKNS = TTHKNS + THKNS(I)
          K = NCOMEN(I) - NCOMEN(I-1)
          T = T + K * DELX(NCOMEN(I))
          TDIF = TTHKNS - T
          IF (TDIF.GT.TOL) THEN
C           horizon's compartments end before horizon boundary
C           add fraction of next compartment
            LNC  = K + TDIF/DELX(NCOMEN(I-1)) + TREM
C           don't include this fraction in next horizon
            TREM = -TDIF/DELX(NCOMEN(I-1))
          ELSE IF (-TDIF.GT.TOL) THEN
C           horizon's compartments exceed horizon boundary
C           subtract fraction of last compartment
            LNC  = K + TDIF/DELX(NCOMEN(I)) + TREM
C           add remainder of last compartment to next horizon
            TREM = -TDIF/DELX(NCOMEN(I))
          ELSE
C           compartment's end on horizon boundary, no fractions
            LNC  = K + TREM
            TREM = 0.0
          END IF
C         monthly below-ground plant uptake fractions
          DO 130 J = 1,12
            NUPTM(J,I) = NUPTM(J,I)/LNC
 130      CONTINUE
          IF (VNUTFG.EQ.0) THEN
C           above-ground plant uptake fraction
            ANUTF(I) = ANUTF(I)/LNC
          ELSE
C           monthly above-ground plant uptake fractions
            DO 135 J = 1,12
              ANUFM(J,I) = ANUFM(J,I)/LNC
 135        CONTINUE
          END IF
C         nitrogen storages
          DO 137 J = 1,8
            NIT(J,I) = NIT(J,I)/LNC
 137      CONTINUE
 140    CONTINUE
        LNC = NCOMEN(1) + TREM
C       adjust first horizon's values
        DO 150 J = 1,12
          NUPTM(J,1) = NUPTM(J,1)/LNC
 150    CONTINUE
        IF (VNUTFG.EQ.0) THEN
          ANUTF(1) = ANUTF(1)/LNC
        ELSE
          DO 152 J = 1,12
            ANUFM(J,1) = ANUFM(J,1)/LNC
 152      CONTINUE
        END IF
        DO 154 J = 1,8
          NIT(J,1) = NIT(J,1)/LNC
 154    CONTINUE
      ELSE
C       only one horizon, it contains all compartments
C       adjust horizon's uptake value for distribution to compartments
        DO 155 J = 1,12
          NUPTM(J,1) = NUPTM(J,1)/NCOM2
 155    CONTINUE
      END IF
C
C     assign horizon soil profile values to individual soil layers
      IB = NHORIZ
      T  = 0.0
      TTHKNS = THKNS(IB)
      MTROK=0
      MTR1=NCOM2
      U=0.0
      DO 160 J = 1, NCOM2-1
        IBM1= IB - 1
        JB  = NCOM2 - J + 1
        T   = T + DELX(JB)
        U = U + DELX(J)
        IF((U.GE.100.0).AND.(MTROK.EQ.0))THEN
          MTR1=J
          MTROK=1
        ENDIF
        MODFC  = 0.0

        IF (T .LE. TTHKNS+.01) THEN
          BD(JB)    = BD(IB)
          THETAS(JB)= THETAS(IB)
          THETO(JB) = THETO(IB)
          THEFC(JB) = THEFC(IB)
          THEWP(JB) = THEWP(IB)
          HORIZN(JB)= HORIZN(IB)
          SAND(JB)  = SAND(IB)
          CLAY(JB)  = CLAY(IB)
          OC(JB)    = OC(IB)
          Q(JB)     = Q(IB)
          CM(JB)    = CM(IB)
          AD(JB)    = AD(IB)
          ADL(JB)   = ADL(IB)
          SPT(JB)   = SPT(IB)
          THCOND(JB)= THCOND(IB)
          VHTCAP(JB)= VHTCAP(IB)
          DKRW12(JB)= DKRW12(IB)
          DKRW13(JB)= DKRW13(IB)
          DKRW23(JB)= DKRW23(IB)
          DKRS12(JB)= DKRS12(IB)
          DKRS13(JB)= DKRS13(IB)
          DKRS23(JB)= DKRS23(IB)
          DO 161 K=1, NCHEM
            DWRATE(K,JB) = DWRATE(K,IB)
            DSRATE(K,JB) = DSRATE(K,IB)
            DGRATE(K,JB) = DGRATE(K,IB)
            KD(K,JB)     = KD(K,IB)
            DISP(K,JB)   = DISP(K,IB)
            Y(1,K,JB)    = Y(1,1,IB)
            Y(2,K,JB)    = Y(2,1,IB)
            Y(3,K,JB)    = Y(3,1,IB)
            Y(4,K,JB)    = Y(4,1,IB)
161       CONTINUE
C         nitrogen parameters
          K = 12
          IF (VNUTFG.EQ.0) THEN
            KPLN(JB) = KPLN(IB)
            ANUTF(JB)= ANUTF(IB)
          ELSE
            CALL COPYR (K,KPLNM(1,IB),KPLNM(1,JB))
            CALL COPYR (K,ANUFM(1,IB),ANUFM(1,JB))
          END IF
          IF (AMVOFG.EQ.1) THEN
            KVOL(JB) = KVOL(IB)
          END IF
          IF (VNPRFG.EQ.0) THEN
            KRETBN(JB) = KRETBN(IB)
          ELSE
            CALL COPYR (K,KRBNM(1,IB),KRBNM(1,JB))
          END IF
          IF (NUPTFG.EQ.1) THEN
            CALL COPYR (K,NUPTM(1,IB),NUPTM(1,JB))
          END IF
          K = 11
          CALL COPYR (K,NPM(1,IB),NPM(1,JB))
          DNTHRS(JB) = DNTHRS(IB) * THETAS(IB)
          K = 4
          CALL COPYR (K,ORNPM(1,IB),ORNPM(1,JB))
          K = 8
          CALL COPYR (K,NIT(1,IB),NIT(1,JB))
        ELSE
C
          MODFC     = (T - TTHKNS) / DELX(JB)
          BD(JB)    = BD(IB)    * (1.0-MODFC)+ BD(IBM1)    * MODFC
          THETAS(JB)= THETAS(IB)* (1.0-MODFC)+ THETAS(IBM1)* MODFC
          THETO(JB) = THETO(IB) * (1.0-MODFC)+ THETO(IBM1) * MODFC
          THEFC(JB) = THEFC(IB) * (1.0-MODFC)+ THEFC(IBM1) * MODFC
          THEWP(JB) = THEWP(IB) * (1.0-MODFC)+ THEWP(IBM1) * MODFC
          HORIZN(JB)= HORIZN(IBM1)
          SAND(JB)  = SAND(IB)  * (1.0-MODFC)+ SAND(IBM1)  * MODFC
          CLAY(JB)  = CLAY(IB)  * (1.0-MODFC)+ CLAY(IBM1)  * MODFC
          OC(JB)    = OC(IB)    * (1.0-MODFC)+ OC(IBM1)    * MODFC
          Q(JB)     = Q(IB)     * (1.0-MODFC)+ Q(IBM1)     * MODFC
          CM(JB)    = CM(IB)    * (1.0-MODFC)+ CM(IBM1)    * MODFC
          Y(1,1,JB)   = Y(1,1,IB)   * (1.0-MODFC)+ Y(1,1,IBM1)   * MODFC
          Y(2,1,JB)   = Y(2,1,IB)   * (1.0-MODFC)+ Y(2,1,IBM1)   * MODFC
          Y(3,1,JB)   = Y(3,1,IB)   * (1.0-MODFC)+ Y(3,1,IBM1)   * MODFC
          Y(4,1,JB)   = Y(4,1,IB)   * (1.0-MODFC)+ Y(4,1,IBM1)   * MODFC
          Y(1,2,JB)   = Y(1,1,IB)   * (1.0-MODFC)+ Y(1,1,IBM1)   * MODFC
          Y(2,2,JB)   = Y(2,1,IB)   * (1.0-MODFC)+ Y(2,1,IBM1)   * MODFC
          Y(3,2,JB)   = Y(3,1,IB)   * (1.0-MODFC)+ Y(3,1,IBM1)   * MODFC
          Y(4,2,JB)   = Y(4,1,IB)   * (1.0-MODFC)+ Y(4,1,IBM1)   * MODFC
          Y(1,3,JB)   = Y(1,1,IB)   * (1.0-MODFC)+ Y(1,1,IBM1)   * MODFC
          Y(2,3,JB)   = Y(2,1,IB)   * (1.0-MODFC)+ Y(2,1,IBM1)   * MODFC
          Y(3,3,JB)   = Y(3,1,IB)   * (1.0-MODFC)+ Y(3,1,IBM1)   * MODFC
          Y(4,3,JB)   = Y(4,1,IB)   * (1.0-MODFC)+ Y(4,1,IBM1)   * MODFC
          AD(JB)    = AD(IB)    * (1.0-MODFC)+ AD(IBM1)    * MODFC
          ADL(JB)   = ADL(IB)   * (1.0-MODFC)+ ADL(IBM1)   * MODFC
          SPT(JB)   = SPT(IB)   * (1.0-MODFC)+ SPT(IBM1)   * MODFC
          THCOND(JB)= THCOND(IB)* (1.0-MODFC)+ THCOND(IBM1)* MODFC
          VHTCAP(JB)= VHTCAP(IB)* (1.0-MODFC)+ VHTCAP(IBM1)* MODFC
          DKRW12(JB)= DKRW12(IB)* (1.0-MODFC)+ DKRW12(IBM1)* MODFC
          DKRW23(JB)= DKRW23(IB)* (1.0-MODFC)+ DKRW23(IBM1)* MODFC
          DKRW13(JB)= DKRW13(IB)* (1.0-MODFC)+ DKRW13(IBM1)* MODFC
          DKRS12(JB)= DKRS12(IB)* (1.0-MODFC)+ DKRS12(IBM1)* MODFC
          DKRS23(JB)= DKRS23(IB)* (1.0-MODFC)+ DKRS23(IBM1)* MODFC
          DKRS13(JB)= DKRS13(IB)* (1.0-MODFC)+ DKRS13(IBM1)* MODFC
          DO 162 K=1, NCHEM
            DWRATE(K,JB)= DWRATE(K,IB)* (1.0-MODFC)+
     1                    DWRATE(K,IBM1)* MODFC
            DSRATE(K,JB)= DSRATE(K,IB)* (1.0-MODFC)+
     1                    DSRATE(K,IBM1)* MODFC
            DGRATE(K,JB)= DGRATE(K,IB)* (1.0-MODFC)+
     1                    DGRATE(K,IBM1)* MODFC
            KD(K,JB)    = KD(K,IB)*(1.0-MODFC) + KD(K,IBM1)*MODFC
            DISP(K,JB)  = DISP(K,IB)*(1.0-MODFC) + DISP(K,IBM1)*MODFC
162       CONTINUE
C         nitrogen parameters
          IF (VNUTFG.EQ.0) THEN
            KPLN(JB) = KPLN(IB) * (1.0-MODFC)+ KPLN(IBM1) * MODFC
            ANUTF(JB)= ANUTF(IB)* (1.0-MODFC)+ ANUTF(IBM1)* MODFC
          ELSE
            DO 163 K = 1,12
              KPLNM(K,JB)= KPLNM(K,IB)* (1.0-MODFC)+ KPLNM(K,IBM1)*MODFC
              ANUFM(K,JB)= ANUFM(K,IB)* (1.0-MODFC)+ ANUFM(K,IBM1)*MODFC
 163        CONTINUE
          END IF
          IF (AMVOFG.EQ.1) THEN
            KVOL(JB) = KVOL(IB) * (1.0-MODFC)+ KVOL(IBM1) * MODFC
          END IF
          IF (VNPRFG.EQ.0) THEN
            KRETBN(JB) = KRETBN(IB)* (1.0-MODFC)+ KRETBN(IBM1)* MODFC
          ELSE
            DO 164 K = 1,12
              KRBNM(K,JB)= KRBNM(K,IB)* (1.0-MODFC)+ KRBNM(K,IBM1)*MODFC
 164        CONTINUE
          END IF
          IF (NUPTFG.EQ.1) THEN
            DO 165 K = 1,12
              NUPTM(K,JB)= NUPTM(K,IB)* (1.0-MODFC)+ NUPTM(K,IBM1)*MODFC
 165        CONTINUE
          END IF
          DO 166 K = 1,11
            NPM(K,JB) = NPM(K,IB)* (1.0-MODFC)+ NPM(K,IBM1)* MODFC
 166      CONTINUE
          DNTHRS(JB) = DNTHRS(IB) * THETAS(IB) * (1.0-MODFC) +
     $                 DNTHRS(IBM1) * THETAS(IBM1) * MODFC
          DO 167 K = 1,4
            ORNPM(K,JB) = ORNPM(K,IB)* (1.0-MODFC)+ ORNPM(K,IBM1)* MODFC
 167      CONTINUE
          DO 168 K = 1,8
            NIT(K,JB) = NIT(K,IB)* (1.0-MODFC)+ NIT(K,IBM1)* MODFC
 168      CONTINUE
C
          IB        = IB - 1
          TTHKNS    = TTHKNS + THKNS(IB)
        ENDIF
160   CONTINUE
C
C     initialize soil water variables
C     Hardwiring the initialization of runoff depth parameters
C     to 10 cm or the surface compartment thickness, whichever
C     is greater.  PV @ AQUA TERRA Consultants, Mountain View, CA.
C
      AAA = AMAX1(DELX(1),10.0)
      JLIN = 0
      DDLNJ = 0.0
6088  JLIN = JLIN + 1
      DDLNJ = DDLNJ + DELX(JLIN)
      IF (AAA .GT. DDLNJ) GO TO 6088
      RODPTH = JLIN
      THETH  = 0.0
      TFCRNF = 0.0
      TWPRNF = 0.0
      DO 170 I=1,RODPTH
        THETH = THETH + 0.5*(THEFC(I)+THEWP(I))
        TFCRNF = TFCRNF + THEFC(I)*DELX(I)
        TWPRNF = TWPRNF + THEWP(I)*DELX(I)
170   CONTINUE
      THETH = THETH/RODPTH
      DO 180 I=1,NCOM2
        SW(I) = THETO(I)*DELX(I)
        FC(I) = THEFC(I)*DELX(I)
        WP(I) = THEWP(I)*DELX(I)
180   CONTINUE
C
C     find maximum root zone depth
      RZD = 0.0
      DO 200 I=1,NDC
        RZD = AMAX1(RZD,AMXDR(I))
200   CONTINUE
      KLIN = 0
      DDLNK = 0.0
6099  KLIN = KLIN + 1
      DDLNK = DDLNK + DELX(KLIN)
      IF (RZD .GT. DDLNK) GO TO 6099
      NCOMRZ = KLIN
C
c
cjmc *********************************************************
cjmc BEGIN WEI MODIFICATIONS
c
C     Calculate number of compartments which make up runoff
C     pesticide extraction depth, defined by variable PRDPTH.
C
      ERSNTT = 0.0
      PRDPTH = 2.0
      KLIN = 0
      DDLN = 0.0
15    CONTINUE
        KLIN = KLIN + 1
        DDLN = DDLN + DELX(KLIN)
      IF (DDLN .LT. PRDPTH) GO TO 15
      RNCMPT = KLIN
      PFRAC = PRDPTH - (DDLN-DELX(KLIN))
c
      midtot=0.0 ! repair 2004-08-13 of bug found by Dirk Young
      DO 16 I=1,RNCMPT
        DELMID=DELX(I)/2.
        MIDTOT=MIDTOT+DELMID
        DRI(I)=.7*(1./((2.*MIDTOT)+.9))**2
   16 CONTINUE
c
cjmc END WEI MODIFICATIONS
c****************************************************************
C
C     set time step for 1 day
      DO 205 K = 1, NCHEM
        FMRMVL(K)=0.0
205   CONTINUE
      DELT  = 1
C
C     chemical loop added, 1's converted to K'2
      DO 211 K = 1, NCHEM
        DO 210 I=1,NCOM2
C         external units of PESTR are mg/kg
          IF (CFLAG .EQ. 0) PESTR(K,I)=1.E-6*PESTR(K,I)*BD(I)/THETO(I)
C         external units of PESTR are kg/ha
          IF (CFLAG .EQ. 1) PESTR(K,I)=
     1                1.E-5*PESTR(K,I)/(DELX(I)*THETO(I))
          SPESTR(K,I)=PESTR(K,I)*THETO(I)/(THETO(I)+KD(K,I)*BD(I)+
     1                (THETAS(I)-THETO(I))*OKH(K,I))
          IF (BIOFLG .EQ. 1)THEN
            C12(K,I) = CM(I) * 0.01D0 * (DBLE(THETO(I) * DELX(I)))
          ENDIF
210     CONTINUE
211   CONTINUE
C
C     perform units conversions for input variables
C     COVMAX..PERCENT--->FRACTION
C     WFMAX...KG/M**2--->G/CM**2
C     TAPP... KG/HA  --->G/CM**2
C
      DO 220 I=1,NDC
        COVMAX(I)=COVMAX(I)/100.
        WFMAX(I)=WFMAX(I)/10.
220   CONTINUE
      DO 230 I=1,NAPS
         DO 235 K=1,NCHEM
          TAPP(K,I)=TAPP(K,I)/1.0E5
235      CONTINUE
230   CONTINUE
      DO 250 I=1,NCOM2
        MSTR(I)  = THETO(I)*DELX(I)
        YSTR(I)  = MSTR(I)
250   CONTINUE
C
C     determine number of first pesticide application
      I= 0
260   CONTINUE
      I= I+ 1
      IF (ISTYR .GT. IAPYR(I) .OR.
     1   (ISTYR.EQ.IAPYR(I) .AND. SJDAY.GT.IAPDY(I))) GO TO 260
      NAPPC = I
C
      NUM=4
      DO 270 K=1,NCHEM
        NPI(K)=NUM*NCOM2
270   CONTINUE
C
C     determine fixed cell centers (ZC) and initial locations of
C     moving points (Z). Initialize concentrations and masses.
      CNCPND=0.0
      ZC(1)=DELX(1)/2.
C
      DO 300  J=2,NCOM2
        ZC(J)= ZC(J-1) + (DELX(J-1)+DELX(J))/2.
300   CONTINUE
      DO 360 K=1,NCHEM
        DO 310 J=1,NCOM2
          SPTEMP(K,J)=0.0
          CELLBG=ZC(J)-DELX(J)/2. + DELX(J)/2./NUM
          MASSO(K,J)=0.0
          DO 310 I=1,NUM
            Z(K,(J-1)*NUM + I) = CELLBG + (I-1)*DELX(J)/NUM
310     CONTINUE
        DO 320 M=1,NPI(K)
          CC(K,M)=0.0
320     CONTINUE
C
C       find the initial density point in each horizon
        DO 330 I=1,NHORIZ
          DEN(K,I) = NUM/DPN(I)
330     CONTINUE
C
C       find interfaces that have a ratio of densities > 2
        J = 1
        DEPTH = 0
        DO 345 I=1,NHORIZ-1
          RATIO(K,I) = 0
          TOP(K,I) = 0.
          PCOUNT(K,I) = 0
345     CONTINUE
        DO 350 I=2,NHORIZ
          RATIO1 = DEN(K,I-1)/DEN(K,I)
          DEPTH = DEPTH + THKNS(I-1)
          IF (RATIO1 .GE. 2.) THEN
            RATIO(K,J) = NINT(RATIO1)
C
C           find the top of the first compartment w/in underlying horz
            DO 340 KK=1,NCOM2
              TOP1 = ZC(KK) - (DELX(KK)/2.)
              IF (ABS(TOP1-DEPTH) .LE. 0.001) THEN
                TOP(K,J) = TOP1
                J = J + 1
                GO TO 350
              ENDIF
340         CONTINUE
          ENDIF
350     CONTINUE
        ICROSS(K) = J - 1
360   CONTINUE
C
      MOCFLG = 0
C
      CALL SUBOUT
C
      RETURN
      End Subroutine INITL
C
C
C
      SUBROUTINE   RSTPUT (LPRZRS,IPRZM)
C
C     + + + PURPOSE + + +
C     to write accumulators, storages and parameters
C     into a file in unformatted fashion for the application
C     of PRZM's RESTART mode
C     Modification date: 2/18/923 JAM
C
      Use m_Wind

C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4   LPRZRS,IPRZM
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZRS - Fortran unit number to write to
C     IPRZM  - current przm run number
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'EXAM.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,J,K
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL   SUBIN,PZSCRN,SUBOUT
C
C     + + + OUTPUT FORMAT + + +
 5000 FORMAT('Writing PRZM restart data, zone [',I2,']')
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'RSTPUT'
      CALL SUBIN(MESAGE)
C
      WRITE(MESAGE,5000) IPRZM
      CALL PZSCRN(2,MESAGE)
C
      WRITE (LPRZRS) IPRZM
C
      WRITE (LPRZRS) HEADER
C
C     parameters indicate arrays' dimensions
      WRITE(LPRZRS) NHORIZ, NCOM2, NCOM2M, NDC, NCPDS, NAPS, NCHEM
      WRITE(LPRZRS) ((CNDMO(I,J),I=1,2), J=1,13)
      WRITE(LPRZRS) (CMONTH(I),  I=1,12)
      WRITE(LPRZRS) (DT(I),      I=1,12)
      WRITE(LPRZRS) (BBT(I),     I=1,12)
      WRITE(LPRZRS) (ALBEDO(I),  I=1,12)
      WRITE(LPRZRS) (MODE(I),    I=1,12)
      WRITE(LPRZRS) (PLNAME(I),  I=1,12)
      WRITE(LPRZRS) (INDX(I),    I=1,12)
      WRITE(LPRZRS) SPACT
      WRITE(LPRZRS) (PLTYP(I),   I=1,12)
      WRITE(LPRZRS) (PSTNAM(I),  I=1,NCHEM)
      WRITE(LPRZRS) HTITLE
      WRITE(LPRZRS) ATITLE
      WRITE(LPRZRS) TITLE
      WRITE(LPRZRS) PTITLE
C
C     wdms file unit numbers
      WRITE(LPRZRS) METDSN
C
C     hydrology and sediment production parameters
      WRITE(LPRZRS) PFAC,   SFAC,  IPEIND,  ANETD, INICRP, ISCOND,
     1             ERFLAG, USLEK, USLELS,  USLEP, AFIELD
      IF(ERFLAG.EQ.1)THEN
        WRITE(LPRZRS) TR
        WRITE(LPRZRS) (NUSLEC(K),K=1,NDC)
        WRITE(LPRZRS) ((USLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
        WRITE(LPRZRS) ((JUSLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
      ELSEIF(ERFLAG.GT.1)THEN
        WRITE(LPRZRS) (NUSLEC(K),K=1,NDC)
        WRITE(LPRZRS) SLP,IREG,HL
        WRITE(LPRZRS) ((USLEC(K,I),I=1,NUSLEC(K)),K=1,NDC)
        WRITE(LPRZRS) ((JUSLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
        WRITE(LPRZRS) ((MNGN(K,I),  I=1,NUSLEC(K)),K=1,NDC)
      ENDIF
C
C     biodegradation
      WRITE(LPRZRS) AM,AC,AS,AR,KE,KSM,KCM,KC,MKS,KR,KIN,
     1              KSK,KLDM,KLDC,KLDS,KLDR,KL1,KL2,USM,UCM,
     2              MUC,US,UR,YSM,YCM,YC,YS,YR
C
      WRITE(LPRZRS) (HENRYK(I), I=1,NCHEM)
      WRITE(LPRZRS) (ENPY(I),   I=1,NCHEM)
      WRITE(LPRZRS) (FOLPST(I), I=1,NCHEM)
      WRITE(LPRZRS) (CPBAL(I),  I=1,NCHEM)
      WRITE(LPRZRS) (FMRMVL(I), I=1,NCHEM)
      WRITE(LPRZRS) (SOL(I),    I=1,NCHEM)
      WRITE(LPRZRS) (DKDAY(I),  I=1,NCHEM)
      WRITE(LPRZRS) (DKMNTH(I), I=1,NCHEM)
      WRITE(LPRZRS) (DKNUM(I),  I=1,NCHEM)
      WRITE(LPRZRS) (UPTKF(I),  I=1,NCHEM)
      WRITE(LPRZRS) (DAIR(I),   I=1,NCHEM)
      WRITE(LPRZRS) NAPPC,  NCROP, IUSLEC,
     1             CORED,   BDFLAG, THFLAG, KDFLAG, HSWZT
      WRITE(LPRZRS) MCFLAG, IRFLAG, ITFLAG, MCOFLG, PCMC, BIOFLG,
     1             CWBAL,  EMMISS, IDFLAG, FRMFLG, DK2FLG
      WRITE(LPRZRS) uWind_Reference_Height,  JULDAY, MONTH,  TDET,
     &             NCOMRZ,
     1             NCOM1,  NCOM0,  NCP,    DELT,   SNOWFL, THRUFL
      WRITE(LPRZRS) RZI,    NDCNT,  LEAP,   IY,     RETCOD, IFIRST,
     1             ITEM1,  STEP1,  LFREQ1, ITEM2,  STEP2,  LFREQ2,
     2             ITEM3,  STEP3,  LFREQ3, NPLOTS, STEP4, EXMFLG
C
C     irrigation type
      WRITE(LPRZRS) IRTYPE
C
      WRITE(LPRZRS) ((SPESTR(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((PESTR(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((OKH(K,I),    I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) (SW(I),        I=1,NCOM2)
      WRITE(LPRZRS) (WP(I),        I=1,NCOM2)
      WRITE(LPRZRS) (FC(I),        I=1,NCOM2)
      WRITE(LPRZRS) (DELX(I),      I=1,NCOM2)
      WRITE(LPRZRS) (THETAS(I),    I=1,NCOM2)
      WRITE(LPRZRS) (BD(I),        I=1,NCOM2)
      WRITE(LPRZRS) ((KD(K,I),     I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) (THEFC(I),     I=1,NCOM2)
      WRITE(LPRZRS) (THEWP(I),     I=1,NCOM2)
      WRITE(LPRZRS) ((DWRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DSRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DGRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DWRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DWRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DSRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DSRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DGRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((DGRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) (THETO(I),     I=1,NCOM2)
      WRITE(LPRZRS) (AINF(I),      I=1,NCOM2)
      WRITE(LPRZRS) (SAND(I),      I=1,NCOM2)
      WRITE(LPRZRS) (HORIZN(I),    I=1,NCOM2)
      WRITE(LPRZRS) (OC(I),        I=1,NCOM2)
      WRITE(LPRZRS) (Q(I),   I=1,NCOM2)
      WRITE(LPRZRS) (CM(I),   I=1,NCOM2)
      WRITE(LPRZRS) (Y(1,1,I),     I=1,NCOM2)
      WRITE(LPRZRS) (Y(2,1,I),     I=1,NCOM2)
      WRITE(LPRZRS) (Y(3,1,I),     I=1,NCOM2)
      WRITE(LPRZRS) (Y(4,1,I),     I=1,NCOM2)
      WRITE(LPRZRS) (CLAY(I),      I=1,NCOM2)
      WRITE(LPRZRS) (ADL(I),       I=1,NCOM2)
      WRITE(LPRZRS) (AD(I),        I=1,NCOM2)
      WRITE(LPRZRS) ((DISP(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) (SPT(I),       I=1,NCOM2)
      WRITE(LPRZRS) PTRN12
      WRITE(LPRZRS) PTRN13
      WRITE(LPRZRS) PTRN23
      WRITE(LPRZRS) MTR1
      WRITE(LPRZRS) (DKRW12(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKRW13(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKRW23(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKRS12(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKRS13(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKRS23(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW112(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW113(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW123(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW212(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW213(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKW223(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS112(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS113(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS123(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS212(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS213(I),    I=1,NCOM2)
      WRITE(LPRZRS) (DKS223(I),    I=1,NCOM2)
      WRITE(LPRZRS) (THCOND(I),    I=1,NCOM2)
      WRITE(LPRZRS) (VHTCAP(I),    I=1,NCOM2)
C
      WRITE(LPRZRS) (THKNS(I),     I=1,NHORIZ)
C
C     pesticide application information
      WRITE(LPRZRS) ((TAPP(K,I),   I=1,NAPS),K=1,NCHEM)
      WRITE(LPRZRS) ((APPEFF(K,I), I=1,NAPS),K=1,NCHEM)
      WRITE(LPRZRS) ((DRFT(K,I),   I=1,NAPS),K=1,NCHEM)
      WRITE(LPRZRS) (IAPYR(I),     I=1,NAPS)
      WRITE(LPRZRS) (IAPDY(I),     I=1,NAPS)
      WRITE(LPRZRS) WIN,(WINDAY(I),I=1,NAPS)
      WRITE(LPRZRS) ((DEPI(K,I),   I=1,NAPS),K=1,NCHEM)
      WRITE(LPRZRS) ((CAM(K,I),    I=1,NAPS),K=1,NCHEM)
C
      WRITE(LPRZRS)  FILTRA
      WRITE(LPRZRS) (AOFF(I),   I=1,NCHEM)
      WRITE(LPRZRS) (QFAC(I),   I=1,NCHEM)
      WRITE(LPRZRS) (TBASE(I),  I=1,NCHEM)
      WRITE(LPRZRS) (MSEFF(I),  I=1,NCHEM)
      WRITE(LPRZRS) (MSLAB(I),  I=1,NCHEM)
      WRITE(LPRZRS) (MSFLG(I),  I=1,NCHEM)
      WRITE(LPRZRS) (IPSCND(I), I=1,NCHEM)
      WRITE(LPRZRS) (PLDKRT(I), I=1,NCHEM)
      WRITE(LPRZRS) (FEXTRC(I), I=1,NCHEM)
      WRITE(LPRZRS) (PLVKRT(I), I=1,NCHEM)
C
C     crop rotation information
      WRITE(LPRZRS) (INCROP(I), I=1,NCPDS)
      WRITE(LPRZRS) (IYREM(I),  I=1,NCPDS)
      WRITE(LPRZRS) (IYRMAT(I), I=1,NCPDS)
      WRITE(LPRZRS) (IYRHAR(I), I=1,NCPDS)
      WRITE(LPRZRS) (IEMER(I),  I=1,NCPDS)
      WRITE(LPRZRS) (MAT(I),    I=1,NCPDS)
      WRITE(LPRZRS) (TNDGS(I),  I=1,NCPDS)
      WRITE(LPRZRS) (IHAR(I),   I=1,NCPDS)
C
C     crop information
      WRITE(LPRZRS) COVER,WEIGHT,HEIGHT
      WRITE(LPRZRS) (COVMAX(I), I=1,NDC)
      WRITE(LPRZRS) (WFMAX(I),  I=1,NDC)
      WRITE(LPRZRS) (HTMAX(I),  I=1,NDC)
      WRITE(LPRZRS) (AMXDR(I),  I=1,NDC)
      WRITE(LPRZRS) (ICNAH(I),  I=1,NDC)
      WRITE(LPRZRS) (CINTCP(I), I=1,NDC)
      WRITE(LPRZRS) (ICNCN(I),  I=1,NDC)
      WRITE(LPRZRS) ((IFSCND(K,I),K=1,3),I=1,NDC)
C
      WRITE(LPRZRS) (((CN(I,J,K),K=1,3),J=1,NUSLEC(I)), I=1,NDC)
C
C     output summary parameters
      WRITE(LPRZRS) (MCOFLX(K), K=1,NCHEM)
      WRITE(LPRZRS) (YCOFLX(K), K=1,NCHEM)
      WRITE(LPRZRS) (MINPP1(K), K=1,NCHEM)
      WRITE(LPRZRS) (MINPP8(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP1(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP2(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP3(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP4(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP5(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP6(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP7(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP8(K), K=1,NCHEM)
      WRITE(LPRZRS) (MOUTP9(K), K=1,NCHEM)
      WRITE(LPRZRS) (YINPP1(K), K=1,NCHEM)
      WRITE(LPRZRS) (YINPP8(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP1(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP2(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP3(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP4(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP5(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP6(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP7(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP8(K), K=1,NCHEM)
      WRITE(LPRZRS) (YOUTP9(K), K=1,NCHEM)
      WRITE(LPRZRS) (MSTRP1(K), K=1,NCHEM)
      WRITE(LPRZRS) (YSTRP1(K), K=1,NCHEM)
C
      WRITE(LPRZRS) ((MINPP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MINPP2(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YINPP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YINPP2(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MOUTP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MLOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MDOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YOUTP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YLOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YDOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MSTRP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((VOUTM(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YSTRP(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((VOUTY(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((MTRFM(K,I),  I=1,NCOM2),K=1,NCHEM)
      WRITE(LPRZRS) ((YTRFM(K,I),  I=1,NCOM2),K=1,NCHEM)
C
      WRITE(LPRZRS) MSTR1,  MSTR2,  YSTR1,  YSTR2,  DOUTFL,
     1             MINPW1, MINPW2, MOUTW1, MOUTW2, MOUTW3, MOUTW4
      WRITE(LPRZRS) MOUTW5, MOUTW6, YINPW1, YINPW2, YOUTW1, YOUTW2,
     1             YOUTW3, YOUTW4, YOUTW5, YOUTW6, MOUTFL, YOUTFL,
     2             DINFLO, MINFLO, YINFLO, DSNINF, MSNINF, YSNINF
C
      WRITE(LPRZRS) (MINPW(I),  I=1,NCOM2)
      WRITE(LPRZRS) (YINPW(I),  I=1,NCOM2)
      WRITE(LPRZRS) (MSTR(I),   I=1,NCOM2)
      WRITE(LPRZRS) (YSTR(I),   I=1,NCOM2)
      WRITE(LPRZRS) (MOUTW(I),  I=1,NCOM2)
      WRITE(LPRZRS) (MEOUTW(I), I=1,NCOM2)
      WRITE(LPRZRS) (YOUTW(I),  I=1,NCOM2)
      WRITE(LPRZRS) (YEOUTW(I), I=1,NCOM2)
      WRITE(LPRZRS) (MOOUTW(I), I=1,NCOM2)
      WRITE(LPRZRS) (YOOUTW(I), I=1,NCOM2)
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
C
      SUBROUTINE   RSTPT1 (LPRZRS,IPRZM)
C
C     + + + PURPOSE + + +
C     to write accumulators, storages and parameters
C     into a file in unformatted fashion for the application
C     of PRZM's RESTART mode
C     Modification date: 2/18/92 JAM
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4   LPRZRS,IPRZM
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZRS - Fortran unit number to write to
C     IPRZM  - current number of przm run
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CSPTIC.INC'
      INCLUDE 'CNITR.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,K,NCP1
      CHARACTER*80 MESAGE
C
C     + + + EXTERNALS + + +
      EXTERNAL   SUBIN,SUBOUT
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'RSTPT1'
      CALL SUBIN(MESAGE)
C
      WRITE (LPRZRS) IPRZM
C
C     CACCUM.INC
      WRITE (LPRZRS) MOUTPV, YOUTPV
      WRITE (LPRZRS) (DCOFLX(I), I=1,NCHEM)
C
C     CCROP.INC
      WRITE (LPRZRS) COVER,  WEIGHT,  HEIGHT
C
C     CMET.INC
      WRITE (LPRZRS) TEMP,    PEVP,  PRECIP,  TR,   SOLRAD
      WRITE (LPRZRS) WIND,  IDFLAG,  STTDET, UBT
      WRITE (LPRZRS) (ALBEDO(I), I=1,13)
      WRITE (LPRZRS) (METDSN(I), I=1,5)
      WRITE (LPRZRS) (THCOND(I), I=1,NCOM2)
      WRITE (LPRZRS) (VHTCAP(I), I=1,NCOM2)
C
C     CHYDR.INC
      WRITE (LPRZRS) (ET(I),     I=1,NCOM2)
      WRITE (LPRZRS) THETH,  CINT,   CEVAP,  INABS,  SEDL
      WRITE (LPRZRS) (THETN(I),  I=1,NCOM2)
      WRITE (LPRZRS) SMELT, CINTB,    DIN,  RUNOF,  NCOM2M
      WRITE (LPRZRS) (AINF(I),   I=1,NCOM2)
      WRITE (LPRZRS) (VEL(I),    I=1,NCOM2)
      WRITE (LPRZRS) WBAL,  SNOW,  OSNOW, STRYR,  ENDYR
      WRITE (LPRZRS) (OUTFLO(I), I=1,NCOM2)
      WRITE (LPRZRS) (DPN(I),    I=1,NCOM2)
      WRITE (LPRZRS) (NPI(I),    I=1,NCHEM)
cjmc added by WATERBORNE 5/23/95
      WRITE (LPRZRS) RNCMPT
      WRITE (LPRZRS) PRDPTH,PFRAC
      WRITE (LPRZRS) (DRI(I),    I=1,NCOM2)
cjmc end of additions
      DO 10 K = 1,NCHEM
        WRITE (LPRZRS) (Z(K,I),     I=1,NPI(K))
 10   CONTINUE
C      WRITE (LPRZRS) (Z(1,I),     I=1,NPI(1))
C      WRITE (LPRZRS) (Z(2,I),     I=1,NPI(2))
C      WRITE (LPRZRS) (Z(3,I),     I=1,NPI(3))
      WRITE (LPRZRS) ((DEN(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((RATIO(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((PCOUNT(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((TOP(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) (ZC(I),     I=1,NCOM2)
      WRITE (LPRZRS) NUM,   VLFLAG
      WRITE (LPRZRS) (ICROSS(I), I=1,NCHEM)
C
C     CPEST.INC
      WRITE (LPRZRS) (ELTERM(K), K=1,NCHEM)
      WRITE (LPRZRS) (FPDLOS(K), K=1,NCHEM)
      WRITE (LPRZRS) (PLNTAP(K), K=1,NCHEM)
      WRITE (LPRZRS) (ERFLUX(K), K=1,NCHEM)
      WRITE (LPRZRS) (SUPFLX(K), K=1,NCHEM)
      WRITE (LPRZRS) (LATFLX(K), K=1,NCHEM)
      WRITE (LPRZRS) (SDKFLX(K), K=1,NCHEM)
      WRITE (LPRZRS) (FOLP0(K),  K=1,NCHEM)
      WRITE (LPRZRS) (ROFLUX(K), K=1,NCHEM)
      WRITE (LPRZRS) (PBAL(K),   K=1,NCHEM)
      WRITE (LPRZRS) (RZFLUX(K), K=1,NCHEM)
      WRITE (LPRZRS) (WOFLUX(K), K=1,NCHEM)
cjmc  wterm now is dimensioned by ncom2,nchem
      WRITE (LPRZRS) ((GAMMA(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((WTERM(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((DFFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((ADFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((LTFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((UPFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((DKFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((PVFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((SOILAP(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((KH(K,I),    I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ELTT,  CNCPND
      WRITE (LPRZRS) ((SPTEMP(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((MASSO(K,I), I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((SRCW(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((SRCS(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((RTRW(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((RTRS(K,I),   I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((TRFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) ((SRCFLX(K,I),I=1,NCOM2),K=1,NCHEM)
      WRITE (LPRZRS) (CONDUC(K), K=1,NCHEM)
      WRITE (LPRZRS) (CNDBDY(K), K=1,NCHEM)
      WRITE (LPRZRS) (FPVLOS(K), K=1,NCHEM)
      WRITE (LPRZRS) (TTRFLX(K), K=1,NCHEM)
      WRITE (LPRZRS) (TSRCFX(K), K=1,NCHEM)
      WRITE (LPRZRS) (TCNC(K),   K=1,NCHEM)
      WRITE (LPRZRS) (DKSTRT(K), K=1,NCHEM)
      WRITE (LPRZRS) (DKEND(K),  K=1,NCHEM)
      WRITE (LPRZRS) (DKSTAT(K), K=1,NCHEM)
      WRITE (LPRZRS) (CC(1,I),   I=1,100)
      WRITE (LPRZRS) (CC(1,I),   I=101,200)
      WRITE (LPRZRS) (CC(1,I),   I=201,300)
      WRITE (LPRZRS) (CC(1,I),   I=301,400)
      WRITE (LPRZRS) (CC(1,I),   I=401,500)
      WRITE (LPRZRS) (CC(1,I),   I=501,600)
      WRITE (LPRZRS) (CC(1,I),   I=601,700)
      WRITE (LPRZRS) (CC(1,I),   I=701,800)
      WRITE (LPRZRS) (CC(1,I),   I=801,900)
      WRITE (LPRZRS) (CC(1,I),   I=901,1000)
      WRITE (LPRZRS) (CC(1,I),   I=1001,1100)
      WRITE (LPRZRS) (CC(1,I),   I=1101,1200)
      WRITE (LPRZRS) (CC(1,I),   I=1201,1300)
      WRITE (LPRZRS) (CC(1,I),   I=1301,1400)
      WRITE (LPRZRS) (CC(1,I),   I=1401,1500)
      WRITE (LPRZRS) (CC(1,I),   I=1501,1600)
      WRITE (LPRZRS) (CC(1,I),   I=1601,1700)
      WRITE (LPRZRS) (CC(1,I),   I=1701,1800)
      WRITE (LPRZRS) (CC(1,I),   I=1801,1900)
      WRITE (LPRZRS) (CC(1,I),   I=1901,2000)
      WRITE (LPRZRS) (CC(2,I),   I=1,100)
      WRITE (LPRZRS) (CC(2,I),   I=101,200)
      WRITE (LPRZRS) (CC(2,I),   I=201,300)
      WRITE (LPRZRS) (CC(2,I),   I=301,400)
      WRITE (LPRZRS) (CC(2,I),   I=401,500)
      WRITE (LPRZRS) (CC(2,I),   I=501,600)
      WRITE (LPRZRS) (CC(2,I),   I=601,700)
      WRITE (LPRZRS) (CC(2,I),   I=701,800)
      WRITE (LPRZRS) (CC(2,I),   I=801,900)
      WRITE (LPRZRS) (CC(2,I),   I=901,1000)
      WRITE (LPRZRS) (CC(2,I),   I=1001,1100)
      WRITE (LPRZRS) (CC(2,I),   I=1101,1200)
      WRITE (LPRZRS) (CC(2,I),   I=1201,1300)
      WRITE (LPRZRS) (CC(2,I),   I=1301,1400)
      WRITE (LPRZRS) (CC(2,I),   I=1401,1500)
      WRITE (LPRZRS) (CC(2,I),   I=1501,1600)
      WRITE (LPRZRS) (CC(2,I),   I=1601,1700)
      WRITE (LPRZRS) (CC(2,I),   I=1701,1800)
      WRITE (LPRZRS) (CC(2,I),   I=1801,1900)
      WRITE (LPRZRS) (CC(2,I),   I=1901,2000)
      WRITE (LPRZRS) (CC(3,I),   I=1,100)
      WRITE (LPRZRS) (CC(3,I),   I=101,200)
      WRITE (LPRZRS) (CC(3,I),   I=201,300)
      WRITE (LPRZRS) (CC(3,I),   I=301,400)
      WRITE (LPRZRS) (CC(3,I),   I=401,500)
      WRITE (LPRZRS) (CC(3,I),   I=501,600)
      WRITE (LPRZRS) (CC(3,I),   I=601,700)
      WRITE (LPRZRS) (CC(3,I),   I=701,800)
      WRITE (LPRZRS) (CC(3,I),   I=801,900)
      WRITE (LPRZRS) (CC(3,I),   I=901,1000)
      WRITE (LPRZRS) (CC(3,I),   I=1001,1100)
      WRITE (LPRZRS) (CC(3,I),   I=1101,1200)
      WRITE (LPRZRS) (CC(3,I),   I=1201,1300)
      WRITE (LPRZRS) (CC(3,I),   I=1301,1400)
      WRITE (LPRZRS) (CC(3,I),   I=1401,1500)
      WRITE (LPRZRS) (CC(3,I),   I=1501,1600)
      WRITE (LPRZRS) (CC(3,I),   I=1601,1700)
      WRITE (LPRZRS) (CC(3,I),   I=1701,1800)
      WRITE (LPRZRS) (CC(3,I),   I=1801,1900)
      WRITE (LPRZRS) (CC(3,I),   I=1901,2000)
      WRITE (LPRZRS) (CRCNC(I),  I=1,2)
C
C     CMISC.INC
      WRITE (LPRZRS) ISDAY,  ISMON,   ISTYR, IEDAY,  IEMON,   IEYR
      WRITE (LPRZRS) NACTS,  CFLAG,     ILP,  SAYR,  SADAY,  SAMON
      WRITE (LPRZRS) SSFLAG,   DOM,  DAYCNT,  SAVAL
      WRITE (LPRZRS) (IARG(I),  I=1,12)
      WRITE (LPRZRS) (IARG2(I),  I=1,12)
      WRITE (LPRZRS) (CONST(I), I=1,12)
      WRITE (LPRZRS) (PLTDSN(I),I=1,12)
      WRITE (LPRZRS) (OUTPUT(I),I=1,12)
      WRITE (LPRZRS) (SPACTS(I),I=1,3)
      WRITE (LPRZRS) SPACT
      WRITE (LPRZRS) (PLNAME(I),I=1,12)
      WRITE (LPRZRS) (MODE(I),  I=1,12)
      WRITE (LPRZRS) (INDX(I),  I=1,12)
      WRITE (LPRZRS) (PLTYP(I), I=1,12)
      WRITE (LPRZRS) (PSTNAM(I),I=1,3)
      WRITE (LPRZRS) TITLE
      WRITE (LPRZRS) PTITLE
      WRITE (LPRZRS) HTITLE
      WRITE (LPRZRS) STITLE
      WRITE (LPRZRS) ATITLE
      WRITE (LPRZRS) NTITLE
C
C     CIRGT.INC
      WRITE (LPRZRS) Q0, KS, HF, DW, BT, ZRS, XL, SF, EN, SMDEF
      WRITE (LPRZRS) DX, UC, NSPACE, PCDEPL, RATEAP
      WRITE (LPRZRS) FLEACH, XFRAC, APDEP
      WRITE (LPRZRS) (QS(I), I=1,200)
      WRITE (LPRZRS) (QS(I), I=201,400)
      WRITE (LPRZRS) (QS(I), I=401,600)
      WRITE (LPRZRS) (QS(I), I=601,800)
      WRITE (LPRZRS) (QS(I), I=801,1000)
      WRITE (LPRZRS) (FS(I), I=1,200)
      WRITE (LPRZRS) (FS(I), I=201,400)
      WRITE (LPRZRS) (FS(I), I=401,600)
      WRITE (LPRZRS) (FS(I), I=601,800)
      WRITE (LPRZRS) (FS(I), I=801,1000)
C
C     CSPTIC.INC
      WRITE (LPRZRS) SEPDSN,SEPHZN
      WRITE (LPRZRS) INFLOW,AMMON,NITR,ORGN,ORGRFC
      WRITE (LPRZRS) (LINF(I),I=1,NCOM2)
      WRITE (LPRZRS) (AMMINF(I),I=1,NCOM2)
      WRITE (LPRZRS) (NITINF(I),I=1,NCOM2)
      WRITE (LPRZRS) (ORGINF(I),I=1,NCOM2)
C
C     CNITR.INC
      WRITE (LPRZRS) VNUTFG,FORAFG,ITMAXA,NUPTFG,FIXNFG,AMVOFG,ALPNFG,
     $               VNPRFG,(NIADFG(I),I=1,6),NC1,NCRP,
     $               ((CRPDAT(K,I),K=1,4),I=1,3),
     $               ((CRPDAY(K,I),K=1,13),I=1,3),NWCNT(6),NECNT(1),
     $               (NAPFRC(K),K=1,NAPS)
      WRITE (LPRZRS) ((CRPFRC(K,I),K=1,13),I=1,3),NUPTGT,NMXRAT
      WRITE (LPRZRS) ((NIAFXM(K,I),K=1,12),I=1,3),
     $               ((NIACNM(K,I),K=1,12),I=1,3)
      WRITE (LPRZRS) ((KPLNM(K,I),I=1,NCOM2),K=1,12)
      WRITE (LPRZRS) ((KRBNM(K,I),I=1,NCOM2),K=1,12)
      WRITE (LPRZRS) (KRANM(I),I=1,12),(KRLNM(I),I=1,12),
     $               (BNPRFM(I),I=1,12),(LNPRFM(I),I=1,12),
     $               (NUPTFM(I),I=1,12)
      WRITE (LPRZRS) ((NUPTM(K,I),I=1,NCOM2),K=1,12)
      WRITE (LPRZRS) (GNPM(I),I=1,11),((NPM(K,I),I=1,NCOM2),K=1,11)
      WRITE (LPRZRS) (DNTHRS(I),I=1,NCOM2),
     $               ((ORNPM(K,I),I=1,NCOM2),K=1,4)
      WRITE (LPRZRS) ((ANUFM(K,I),I=1,NCOM2),K=1,12)
      WRITE (LPRZRS) (KVOL(I),I=1,NCOM2),THVOL,TRFVOL,AGPLTN,LITTRN
      WRITE (LPRZRS) ((NIT(K,I),I=1,NCOM2),K=1,8),(TNIT(I),I=1,8),
     $               TOTNIT,TONIT0
      WRITE (LPRZRS) (NDFC(I),I=1,NCMPP1),(KPLN(I),I=1,NCOM2),
     $               (KRETBN(I),I=1,NCOM2),BGNPRF,AGKPRN,
     $               (KRETAN(I),I=1,NCOM2),LINPRF
      WRITE (LPRZRS) (NUPTG(I),I=1,NCOM2),(PNUTG(I),I=1,NCOM2),
     $               (ANUTF(I),I=1,NCOM2)
      WRITE (LPRZRS) ((NRXF(K,I),I=1,NCOM2),K=1,16)
      WRITE (LPRZRS) ((NCFX1(K,I),K=1,7),I=1,3),
     $               ((NCFX2(K,I),K=1,NCOM2),I=1,3)
      NCP1 = NCOM2 + 1
      WRITE (LPRZRS) ((NCFX3(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX4(K,I),K=1,NCOM2),I=1,3)
      WRITE (LPRZRS) ((NCFX5(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX6(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX7(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX8(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX9(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX10(K,I),K=1,3),I=1,3),
     $               ((NCFX11(K,I),K=1,3),I=1,3)
      WRITE (LPRZRS) ((NCFX12(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX13(K,I),K=1,NCOM2),I=1,3)
      WRITE (LPRZRS) ((NCFX14(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX15(K,I),K=1,NCOM2),I=1,3)
      WRITE (LPRZRS) ((NCFX16(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX17(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX18(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX19(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX20(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX21(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX22(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX23(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) (NCFX24(1,I),I=1,3),((NCFX25(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX26(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX27(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((NCFX28(K,I),K=1,NCP1),I=1,3)
      WRITE (LPRZRS) ((CNIT(K,I),I=1,NCOM2),K=1,8)
C
      REWIND (UNIT=LPRZRS)
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
C
      SUBROUTINE   RSTGET (LPRZRS,IPZCHK)
C
C     + + + PURPOSE + + +
C     to pass accumulators, storages and parameters
C     into PRZM in unformatted fashion for the application
C     of PRZM's RESTART mode
C     Modification date: 2/18/92 JAM
C
      Use m_Wind

C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4 LPRZRS,IPZCHK
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZRS - Fortran unit number to read from
C     IPZCHK - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'EXAM.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,J,K,IPRZM,IERROR
      CHARACTER*80 MESAGE
      LOGICAL      FATAL
C
C     + + + EXTERNALS + + +
      EXTERNAL   SUBIN,ERRCHK,PZSCRN,SUBOUT
C
C     + + + OUTPUT FORMATS + + +
 5000 FORMAT('Reading PRZM restart data, zone [',I2,']')
 8000 FORMAT('Attempted to read PRZM zone',I2,
     1       ', restart file indicated zone',I2)
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'RSTGET'
      CALL SUBIN(MESAGE)
C
      WRITE(MESAGE,5000) IPZCHK
      CALL PZSCRN(2,MESAGE)
C
      READ (LPRZRS) IPRZM
      IF (IPRZM .NE. IPZCHK) THEN
        IERROR = 2020
        WRITE(MESAGE,8000) IPZCHK, IPRZM
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      ENDIF
C
      READ (LPRZRS) HEADER
C
C     parameters indicate arrays' dimensions
      READ(LPRZRS) NHORIZ, NCOM2, NCOM2M, NDC, NCPDS, NAPS, NCHEM
C
      READ(LPRZRS) ((CNDMO(I,J),I=1,2), J=1,13)
      READ(LPRZRS) (CMONTH(I),  I=1,12)
      READ(LPRZRS) (DT(I),      I=1,12)
      READ(LPRZRS) (BBT(I),     I=1,12)
      READ(LPRZRS) (ALBEDO(I),  I=1,12)
      READ(LPRZRS) (MODE(I),    I=1,12)
      READ(LPRZRS) (PLNAME(I),  I=1,12)
      READ(LPRZRS) (INDX(I),    I=1,12)
      READ(LPRZRS) SPACT
      READ(LPRZRS) (PLTYP(I),   I=1,12)
      READ(LPRZRS) (PSTNAM(I),  I=1,NCHEM)
      READ(LPRZRS) HTITLE
      READ(LPRZRS) ATITLE
      READ(LPRZRS) TITLE
      READ(LPRZRS) PTITLE
C
C     wdms file unit numbers
      READ(LPRZRS) METDSN
C
C     hydrology and sediment production parameters
      READ(LPRZRS) PFAC,   SFAC,  IPEIND,  ANETD, INICRP, ISCOND,
     1            ERFLAG, USLEK, USLELS,  USLEP, AFIELD
      IF(ERFLAG.EQ.1)THEN
        READ(LPRZRS) TR
        READ(LPRZRS) (NUSLEC(K),K=1,NDC)
        READ(LPRZRS) ((USLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
        READ(LPRZRS) ((JUSLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
      ELSEIF(ERFLAG.GT.1)THEN
        READ(LPRZRS) (NUSLEC(K),K=1,NDC)
        READ(LPRZRS) SLP,IREG,HL
        READ(LPRZRS) ((USLEC(K,I),I=1,NUSLEC(K)),K=1,NDC)
        READ(LPRZRS) ((JUSLEC(K,I),  I=1,NUSLEC(K)),K=1,NDC)
        READ(LPRZRS) ((MNGN(K,I),  I=1,NUSLEC(K)),K=1,NDC)
      ENDIF
C
C     biodegradation
      READ(LPRZRS) AM,AC,AS,AR,KE,KSM,KCM,KC,MKS,KR,KIN,
     1             KSK,KLDM,KLDC,KLDS,KLDR,KL1,KL2,USM,UCM,
     2             MUC,US,UR,YSM,YCM,YC,YS,YR
C
      READ(LPRZRS) (HENRYK(I), I=1,NCHEM)
      READ(LPRZRS) (ENPY(I),   I=1,NCHEM)
      READ(LPRZRS) (FOLPST(I), I=1,NCHEM)
      READ(LPRZRS) (CPBAL(I),  I=1,NCHEM)
      READ(LPRZRS) (FMRMVL(I), I=1,NCHEM)
      READ(LPRZRS) (SOL(I),    I=1,NCHEM)
      READ(LPRZRS) (DKDAY(I),  I=1,NCHEM)
      READ(LPRZRS) (DKMNTH(I), I=1,NCHEM)
      READ(LPRZRS) (DKNUM(I),  I=1,NCHEM)
      READ(LPRZRS) (UPTKF(I),  I=1,NCHEM)
      READ(LPRZRS) (DAIR(I),   I=1,NCHEM)
      READ(LPRZRS)  NAPPC,  NCROP, IUSLEC,
     1            CORED,   BDFLAG, THFLAG, KDFLAG, HSWZT
      READ(LPRZRS) MCFLAG, IRFLAG, ITFLAG, MCOFLG, PCMC, BIOFLG,
     1            CWBAL,  EMMISS, IDFLAG, FRMFLG, DK2FLG
      READ(LPRZRS) uWind_Reference_Height,  JULDAY, MONTH,  TDET,
     &            NCOMRZ,
     1            NCOM1,  NCOM0,  NCP,    DELT,   SNOWFL, THRUFL
      READ(LPRZRS) RZI,    NDCNT,  LEAP,   IY,     RETCOD, IFIRST,
     1            ITEM1,  STEP1,  LFREQ1, ITEM2,  STEP2,  LFREQ2,
     2            ITEM3,  STEP3,  LFREQ3, NPLOTS, STEP4, EXMFLG
C
C     irrigation type
      READ(LPRZRS) IRTYPE
C
      READ(LPRZRS) ((SPESTR(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((PESTR(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((OKH(K,I),    I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) (SW(I),        I=1,NCOM2)
      READ(LPRZRS) (WP(I),        I=1,NCOM2)
      READ(LPRZRS) (FC(I),        I=1,NCOM2)
      READ(LPRZRS) (DELX(I),      I=1,NCOM2)
      READ(LPRZRS) (THETAS(I),    I=1,NCOM2)
      READ(LPRZRS) (BD(I),        I=1,NCOM2)
      READ(LPRZRS) ((KD(K,I),     I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) (THEFC(I),     I=1,NCOM2)
      READ(LPRZRS) (THEWP(I),     I=1,NCOM2)
      READ(LPRZRS) ((DWRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DSRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DGRATE(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DWRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DWRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DSRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DSRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DGRAT1(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((DGRAT2(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) (THETO(I),     I=1,NCOM2)
      READ(LPRZRS) (AINF(I),      I=1,NCOM2)
      READ(LPRZRS) (SAND(I),      I=1,NCOM2)
      READ(LPRZRS) (HORIZN(I),    I=1,NCOM2)
      READ(LPRZRS) (OC(I),        I=1,NCOM2)
      READ(LPRZRS) (Q(I),   I=1,NCOM2)
      READ(LPRZRS) (CM(I),   I=1,NCOM2)
      READ(LPRZRS) (Y(1,1,I),     I=1,NCOM2)
      READ(LPRZRS) (Y(2,1,I),     I=1,NCOM2)
      READ(LPRZRS) (Y(3,1,I),     I=1,NCOM2)
      READ(LPRZRS) (Y(4,1,I),     I=1,NCOM2)
      READ(LPRZRS) (CLAY(I),      I=1,NCOM2)
      READ(LPRZRS) (ADL(I),       I=1,NCOM2)
      READ(LPRZRS) (AD(I),        I=1,NCOM2)
      READ(LPRZRS) ((DISP(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) (SPT(I),       I=1,NCOM2)
      READ(LPRZRS) PTRN12
      READ(LPRZRS) PTRN13
      READ(LPRZRS) PTRN23
      READ(LPRZRS) MTR1
      READ(LPRZRS) (DKRW12(I),    I=1,NCOM2)
      READ(LPRZRS) (DKRW13(I),    I=1,NCOM2)
      READ(LPRZRS) (DKRW23(I),    I=1,NCOM2)
      READ(LPRZRS) (DKRS12(I),    I=1,NCOM2)
      READ(LPRZRS) (DKRS13(I),    I=1,NCOM2)
      READ(LPRZRS) (DKRS23(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW112(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW113(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW123(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW212(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW213(I),    I=1,NCOM2)
      READ(LPRZRS) (DKW223(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS112(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS113(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS123(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS212(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS213(I),    I=1,NCOM2)
      READ(LPRZRS) (DKS223(I),    I=1,NCOM2)
      READ(LPRZRS) (THCOND(I),    I=1,NCOM2)
      READ(LPRZRS) (VHTCAP(I),    I=1,NCOM2)
C
      READ(LPRZRS) (THKNS(I),     I=1,NHORIZ)
C
C     pesticide application information
      READ(LPRZRS) ((TAPP(K,I),   I=1,NAPS),K=1,NCHEM)
      READ(LPRZRS) ((APPEFF(K,I), I=1,NAPS),K=1,NCHEM)
      READ(LPRZRS) ((DRFT(K,I),   I=1,NAPS),K=1,NCHEM)
      READ(LPRZRS) (IAPYR(I),     I=1,NAPS)
      READ(LPRZRS) (IAPDY(I),     I=1,NAPS)
      READ(LPRZRS) WIN,(WINDAY(I),I=1,NAPS)
      READ(LPRZRS) ((DEPI(K,I),   I=1,NAPS),K=1,NCHEM)
      READ(LPRZRS) ((CAM(K,I),    I=1,NAPS),K=1,NCHEM)
C
      READ(LPRZRS)  FILTRA
      READ(LPRZRS) (AOFF(I),   I=1,NCHEM)
      READ(LPRZRS) (QFAC(I),   I=1,NCHEM)
      READ(LPRZRS) (TBASE(I),  I=1,NCHEM)
      READ(LPRZRS) (MSEFF(I),  I=1,NCHEM)
      READ(LPRZRS) (MSLAB(I),  I=1,NCHEM)
      READ(LPRZRS) (MSFLG(I),  I=1,NCHEM)
      READ(LPRZRS) (IPSCND(I), I=1,NCHEM)
      READ(LPRZRS) (PLDKRT(I), I=1,NCHEM)
      READ(LPRZRS) (FEXTRC(I), I=1,NCHEM)
      READ(LPRZRS) (PLVKRT(I), I=1,NCHEM)
C
C     crop rotation information
      READ(LPRZRS) (INCROP(I), I=1,NCPDS)
      READ(LPRZRS) (IYREM(I),  I=1,NCPDS)
      READ(LPRZRS) (IYRMAT(I), I=1,NCPDS)
      READ(LPRZRS) (IYRHAR(I), I=1,NCPDS)
      READ(LPRZRS) (IEMER(I),  I=1,NCPDS)
      READ(LPRZRS) (MAT(I),    I=1,NCPDS)
      READ(LPRZRS) (TNDGS(I),  I=1,NCPDS)
      READ(LPRZRS) (IHAR(I),   I=1,NCPDS)
C
C     crop information
      READ(LPRZRS) COVER,WEIGHT,HEIGHT
      READ(LPRZRS) (COVMAX(I), I=1,NDC)
      READ(LPRZRS) (WFMAX(I),  I=1,NDC)
      READ(LPRZRS) (HTMAX(I),  I=1,NDC)
      READ(LPRZRS) (AMXDR(I),  I=1,NDC)
      READ(LPRZRS) (ICNAH(I),  I=1,NDC)
      READ(LPRZRS) (CINTCP(I), I=1,NDC)
      READ(LPRZRS) (ICNCN(I),  I=1,NDC)
      READ(LPRZRS) ((IFSCND(K,I),K=1,3),I=1,NDC)
C
      READ(LPRZRS) (((CN(I,J,K),K=1,3),J=1,NUSLEC(I)), I=1,NDC)
C
C     output summary parameters
      READ(LPRZRS) (MCOFLX(K), K=1,NCHEM)
      READ(LPRZRS) (YCOFLX(K), K=1,NCHEM)
      READ(LPRZRS) (MINPP1(K), K=1,NCHEM)
      READ(LPRZRS) (MINPP8(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP1(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP2(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP3(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP4(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP5(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP6(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP7(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP8(K), K=1,NCHEM)
      READ(LPRZRS) (MOUTP9(K), K=1,NCHEM)
      READ(LPRZRS) (YINPP1(K), K=1,NCHEM)
      READ(LPRZRS) (YINPP8(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP1(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP2(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP3(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP4(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP5(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP6(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP7(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP8(K), K=1,NCHEM)
      READ(LPRZRS) (YOUTP9(K), K=1,NCHEM)
      READ(LPRZRS) (MSTRP1(K), K=1,NCHEM)
      READ(LPRZRS) (YSTRP1(K), K=1,NCHEM)
C
      READ(LPRZRS) ((MINPP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MINPP2(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YINPP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YINPP2(K,I), I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MOUTP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MLOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MDOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YOUTP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YLOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YDOUT(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MSTRP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((VOUTM(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YSTRP(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((VOUTY(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((MTRFM(K,I),  I=1,NCOM2),K=1,NCHEM)
      READ(LPRZRS) ((YTRFM(K,I),  I=1,NCOM2),K=1,NCHEM)
C
      READ(LPRZRS) MSTR1,  MSTR2,  YSTR1,  YSTR2,  DOUTFL,
     1            MINPW1, MINPW2, MOUTW1, MOUTW2, MOUTW3, MOUTW4
      READ(LPRZRS) MOUTW5, MOUTW6, YINPW1, YINPW2, YOUTW1, YOUTW2,
     1            YOUTW3, YOUTW4, YOUTW5, YOUTW6, MOUTFL, YOUTFL,
     2            DINFLO, MINFLO, YINFLO, DSNINF, MSNINF, YSNINF
C
      READ(LPRZRS) (MINPW(I),  I=1,NCOM2)
      READ(LPRZRS) (YINPW(I),  I=1,NCOM2)
      READ(LPRZRS) (MSTR(I),   I=1,NCOM2)
      READ(LPRZRS) (YSTR(I),   I=1,NCOM2)
      READ(LPRZRS) (MOUTW(I),  I=1,NCOM2)
      READ(LPRZRS) (MEOUTW(I), I=1,NCOM2)
      READ(LPRZRS) (YOUTW(I),  I=1,NCOM2)
      READ(LPRZRS) (YEOUTW(I), I=1,NCOM2)
      READ(LPRZRS) (MOOUTW(I), I=1,NCOM2)
      READ(LPRZRS) (YOOUTW(I), I=1,NCOM2)
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   RSTGT1 (RSTFG,LPRZRS,IPZCHK)
C
C     + + + PURPOSE + + +
C     to pass accumulators, storages and parameters
C     into PRZM in unformatted fashion for the application
C     of PRZM's RESTART mode
C     Modification date: 2/18/92 JAM
C     Further modified at AQUA TERRA Consultants 9/93, to consider
C     lateral pesticide flux and upto 12 time series outputs
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4   RSTFG,LPRZRS,IPZCHK
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LPRZRS - fortran unit number to read from
C     RSTFG  - restart flag
C     IPZCHK - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CACCUM.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CSPTIC.INC'
      INCLUDE 'CNITR.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    I,K,IPRZM,IERROR,NCP1
      CHARACTER*80 MESAGE
      LOGICAL      FATAL
C
C     + + + EXTERNALS + + +
      EXTERNAL    SUBIN,ERRCHK,SUBOUT
C
C     + + + OUTPUT FORMATS + + +
 8000 FORMAT('Attempted to read PRZM zone',I2,
     1       ', restart file indicated zone',I2)
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'RSTGT1'
      CALL SUBIN(MESAGE)
C
      READ (LPRZRS) IPRZM
      IF (IPRZM .NE. IPZCHK) THEN
        IERROR = 2030
        WRITE(MESAGE,8000) IPZCHK, IPRZM
        FATAL  = .TRUE.
        CALL ERRCHK(IERROR,MESAGE,FATAL)
      ENDIF
C
C     CACCUM.INC
      READ (LPRZRS) MOUTPV, YOUTPV
      READ (LPRZRS) (DCOFLX(I), I=1,NCHEM)
C
C     CCROP.INC
      READ (LPRZRS) COVER,  WEIGHT,  HEIGHT
C
C     CMET.INC
      READ (LPRZRS) TEMP,    PEVP,  PRECIP,  TR,   SOLRAD
      READ (LPRZRS) WIND,  IDFLAG,  STTDET, UBT
      READ (LPRZRS) (ALBEDO(I), I=1,13)
      READ (LPRZRS) (METDSN(I), I=1,5)
      READ (LPRZRS) (THCOND(I), I=1,NCOM2)
      READ (LPRZRS) (VHTCAP(I), I=1,NCOM2)
C
C     CHYDR.INC
      READ (LPRZRS) (ET(I),     I=1,NCOM2)
      READ (LPRZRS) THETH,  CINT,   CEVAP,  INABS,  SEDL
      READ (LPRZRS) (THETN(I),  I=1,NCOM2)
      READ (LPRZRS) SMELT, CINTB,    DIN,  RUNOF,  NCOM2M
      READ (LPRZRS) (AINF(I),   I=1,NCOM2)
      READ (LPRZRS) (VEL(I),    I=1,NCOM2)
      READ (LPRZRS) WBAL,  SNOW,  OSNOW, STRYR,  ENDYR
      READ (LPRZRS) (OUTFLO(I), I=1,NCOM2)
      READ (LPRZRS) (DPN(I),    I=1,NCOM2)
      READ (LPRZRS) (NPI(I),    I=1,NCHEM)
cjmc added by WATERBORNE 5/23/95
      READ (LPRZRS) RNCMPT
      READ (LPRZRS) PRDPTH,PFRAC
      READ (LPRZRS) (DRI(I),    I=1,NCOM2)
cjmc end of additions
      DO 10 K = 1,NCHEM
        READ (LPRZRS) (Z(K,I),     I=1,NPI(K))
 10   CONTINUE
C      READ (LPRZRS) (Z(1,I),     I=1,NPI(1))
C      READ (LPRZRS) (Z(2,I),     I=1,NPI(2))
C      READ (LPRZRS) (Z(3,I),     I=1,NPI(3))
      READ (LPRZRS) ((DEN(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((RATIO(K,I), I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((PCOUNT(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((TOP(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) (ZC(I),     I=1,NCOM2)
      READ (LPRZRS) NUM,   VLFLAG
      READ (LPRZRS) (ICROSS(I), I=1,NCHEM)
C
C     CPEST.INC
      READ (LPRZRS) (ELTERM(K), K=1,NCHEM)
      READ (LPRZRS) (FPDLOS(K), K=1,NCHEM)
      READ (LPRZRS) (PLNTAP(K), K=1,NCHEM)
      READ (LPRZRS) (ERFLUX(K), K=1,NCHEM)
      READ (LPRZRS) (SUPFLX(K), K=1,NCHEM)
      READ (LPRZRS) (LATFLX(K), K=1,NCHEM)
      READ (LPRZRS) (SDKFLX(K), K=1,NCHEM)
      READ (LPRZRS) (FOLP0(K),  K=1,NCHEM)
      READ (LPRZRS) (ROFLUX(K), K=1,NCHEM)
      READ (LPRZRS) (PBAL(K),   K=1,NCHEM)
      READ (LPRZRS) (RZFLUX(K), K=1,NCHEM)
      READ (LPRZRS) (WOFLUX(K), K=1,NCHEM)
cjmc  wterm now is dimensioned by ncom2,nchem
      READ (LPRZRS) ((GAMMA(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((WTERM(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((DFFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((ADFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((LTFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((UPFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((DKFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((PVFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((SOILAP(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((KH(K,I),    I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ELTT,  CNCPND
      READ (LPRZRS) ((SPTEMP(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((MASSO(K,I), I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((SRCW(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((SRCS(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((RTRW(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((RTRS(K,I),   I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((TRFLUX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) ((SRCFLX(K,I),I=1,NCOM2),K=1,NCHEM)
      READ (LPRZRS) (CONDUC(K), K=1,NCHEM)
      READ (LPRZRS) (CNDBDY(K), K=1,NCHEM)
      READ (LPRZRS) (FPVLOS(K), K=1,NCHEM)
      READ (LPRZRS) (TTRFLX(K), K=1,NCHEM)
      READ (LPRZRS) (TSRCFX(K), K=1,NCHEM)
      READ (LPRZRS) (TCNC(K),   K=1,NCHEM)
      READ (LPRZRS) (DKSTRT(K), K=1,NCHEM)
      READ (LPRZRS) (DKEND(K),  K=1,NCHEM)
      READ (LPRZRS) (DKSTAT(K), K=1,NCHEM)
      READ (LPRZRS) (CC(1,I),   I=1,100)
      READ (LPRZRS) (CC(1,I),   I=101,200)
      READ (LPRZRS) (CC(1,I),   I=201,300)
      READ (LPRZRS) (CC(1,I),   I=301,400)
      READ (LPRZRS) (CC(1,I),   I=401,500)
      READ (LPRZRS) (CC(1,I),   I=501,600)
      READ (LPRZRS) (CC(1,I),   I=601,700)
      READ (LPRZRS) (CC(1,I),   I=701,800)
      READ (LPRZRS) (CC(1,I),   I=801,900)
      READ (LPRZRS) (CC(1,I),   I=901,1000)
      READ (LPRZRS) (CC(1,I),   I=1001,1100)
      READ (LPRZRS) (CC(1,I),   I=1101,1200)
      READ (LPRZRS) (CC(1,I),   I=1201,1300)
      READ (LPRZRS) (CC(1,I),   I=1301,1400)
      READ (LPRZRS) (CC(1,I),   I=1401,1500)
      READ (LPRZRS) (CC(1,I),   I=1501,1600)
      READ (LPRZRS) (CC(1,I),   I=1601,1700)
      READ (LPRZRS) (CC(1,I),   I=1701,1800)
      READ (LPRZRS) (CC(1,I),   I=1801,1900)
      READ (LPRZRS) (CC(1,I),   I=1901,2000)
      READ (LPRZRS) (CC(2,I),   I=1,100)
      READ (LPRZRS) (CC(2,I),   I=101,200)
      READ (LPRZRS) (CC(2,I),   I=201,300)
      READ (LPRZRS) (CC(2,I),   I=301,400)
      READ (LPRZRS) (CC(2,I),   I=401,500)
      READ (LPRZRS) (CC(2,I),   I=501,600)
      READ (LPRZRS) (CC(2,I),   I=601,700)
      READ (LPRZRS) (CC(2,I),   I=701,800)
      READ (LPRZRS) (CC(2,I),   I=801,900)
      READ (LPRZRS) (CC(2,I),   I=901,1000)
      READ (LPRZRS) (CC(2,I),   I=1001,1100)
      READ (LPRZRS) (CC(2,I),   I=1101,1200)
      READ (LPRZRS) (CC(2,I),   I=1201,1300)
      READ (LPRZRS) (CC(2,I),   I=1301,1400)
      READ (LPRZRS) (CC(2,I),   I=1401,1500)
      READ (LPRZRS) (CC(2,I),   I=1501,1600)
      READ (LPRZRS) (CC(2,I),   I=1601,1700)
      READ (LPRZRS) (CC(2,I),   I=1701,1800)
      READ (LPRZRS) (CC(2,I),   I=1801,1900)
      READ (LPRZRS) (CC(2,I),   I=1901,2000)
      READ (LPRZRS) (CC(3,I),   I=1,100)
      READ (LPRZRS) (CC(3,I),   I=101,200)
      READ (LPRZRS) (CC(3,I),   I=201,300)
      READ (LPRZRS) (CC(3,I),   I=301,400)
      READ (LPRZRS) (CC(3,I),   I=401,500)
      READ (LPRZRS) (CC(3,I),   I=501,600)
      READ (LPRZRS) (CC(3,I),   I=601,700)
      READ (LPRZRS) (CC(3,I),   I=701,800)
      READ (LPRZRS) (CC(3,I),   I=801,900)
      READ (LPRZRS) (CC(3,I),   I=901,1000)
      READ (LPRZRS) (CC(3,I),   I=1001,1100)
      READ (LPRZRS) (CC(3,I),   I=1101,1200)
      READ (LPRZRS) (CC(3,I),   I=1201,1300)
      READ (LPRZRS) (CC(3,I),   I=1301,1400)
      READ (LPRZRS) (CC(3,I),   I=1401,1500)
      READ (LPRZRS) (CC(3,I),   I=1501,1600)
      READ (LPRZRS) (CC(3,I),   I=1601,1700)
      READ (LPRZRS) (CC(3,I),   I=1701,1800)
      READ (LPRZRS) (CC(3,I),   I=1801,1900)
      READ (LPRZRS) (CC(3,I),   I=1901,2000)
      READ (LPRZRS) (CRCNC(I),   I=1,2)
C
C     CMISC.INC
      READ (LPRZRS) ISDAY,  ISMON,   ISTYR, IEDAY,  IEMON,   IEYR
      READ (LPRZRS) NACTS,  CFLAG,     ILP,  SAYR,  SADAY,  SAMON
      READ (LPRZRS) SSFLAG,   DOM,  DAYCNT,  SAVAL
      READ (LPRZRS) (IARG(I),  I=1,12)
      READ (LPRZRS) (IARG2(I),  I=1,12)
      READ (LPRZRS) (CONST(I), I=1,12)
      READ (LPRZRS) (PLTDSN(I),I=1,12)
      READ (LPRZRS) (OUTPUT(I),I=1,12)
      READ (LPRZRS) (SPACTS(I),I=1,3)
      READ (LPRZRS) SPACT
      READ (LPRZRS) (PLNAME(I),I=1,12)
      READ (LPRZRS) (MODE(I),  I=1,12)
      READ (LPRZRS) (INDX(I),  I=1,12)
      READ (LPRZRS) (PLTYP(I), I=1,12)
      READ (LPRZRS) (PSTNAM(I),I=1,3)
      READ (LPRZRS) TITLE
      READ (LPRZRS) PTITLE
      READ (LPRZRS) HTITLE
      READ (LPRZRS) STITLE
      READ (LPRZRS) ATITLE
      READ (LPRZRS) NTITLE
C
C     CIRGT.INC
      READ (LPRZRS) Q0, KS, HF, DW, BT, ZRS, XL, SF, EN, SMDEF
      READ (LPRZRS) DX, UC, NSPACE, PCDEPL, RATEAP
      READ (LPRZRS) FLEACH, XFRAC, APDEP
      READ (LPRZRS) (QS(I), I=1,200)
      READ (LPRZRS) (QS(I), I=201,400)
      READ (LPRZRS) (QS(I), I=401,600)
      READ (LPRZRS) (QS(I), I=601,800)
      READ (LPRZRS) (QS(I), I=801,1000)
      READ (LPRZRS) (FS(I), I=1,200)
      READ (LPRZRS) (FS(I), I=201,400)
      READ (LPRZRS) (FS(I), I=401,600)
      READ (LPRZRS) (FS(I), I=601,800)
      READ (LPRZRS) (FS(I), I=801,1000)
C
C     CSPTIC.INC
      READ (LPRZRS) SEPDSN,SEPHZN
      READ (LPRZRS) INFLOW,AMMON,NITR,ORGN,ORGRFC
      READ (LPRZRS) (LINF(I),I=1,NCOM2)
      READ (LPRZRS) (AMMINF(I),I=1,NCOM2)
      READ (LPRZRS) (NITINF(I),I=1,NCOM2)
      READ (LPRZRS) (ORGINF(I),I=1,NCOM2)
C
C     CNITR.INC
      READ (LPRZRS) VNUTFG,FORAFG,ITMAXA,NUPTFG,FIXNFG,AMVOFG,ALPNFG,
     $              VNPRFG,(NIADFG(I),I=1,6),NC1,NCRP,
     $              ((CRPDAT(K,I),K=1,4),I=1,3),
     $              ((CRPDAY(K,I),K=1,13),I=1,3),NWCNT(6),NECNT(1),
     $              (NAPFRC(K),K=1,NAPS)
      READ (LPRZRS) ((CRPFRC(K,I),K=1,13),I=1,3),NUPTGT,NMXRAT
      READ (LPRZRS) ((NIAFXM(K,I),K=1,12),I=1,3),
     $               ((NIACNM(K,I),K=1,12),I=1,3)
      READ (LPRZRS) ((KPLNM(K,I),I=1,NCOM2),K=1,12)
      READ (LPRZRS) ((KRBNM(K,I),I=1,NCOM2),K=1,12)
      READ (LPRZRS) (KRANM(I),I=1,12),(KRLNM(I),I=1,12),
     $               (BNPRFM(I),I=1,12),(LNPRFM(I),I=1,12),
     $               (NUPTFM(I),I=1,12)
      READ (LPRZRS) ((NUPTM(K,I),I=1,NCOM2),K=1,12)
      READ (LPRZRS) (GNPM(I),I=1,11),((NPM(K,I),I=1,NCOM2),K=1,11)
      READ (LPRZRS) (DNTHRS(I),I=1,NCOM2),
     $               ((ORNPM(K,I),I=1,NCOM2),K=1,4)
      READ (LPRZRS) ((ANUFM(K,I),I=1,NCOM2),K=1,12)
      READ (LPRZRS) (KVOL(I),I=1,NCOM2),THVOL,TRFVOL,AGPLTN,LITTRN
      READ (LPRZRS) ((NIT(K,I),I=1,NCOM2),K=1,8),(TNIT(I),I=1,8),
     $              TOTNIT,TONIT0
      READ (LPRZRS) (NDFC(I),I=1,NCMPP1),(KPLN(I),I=1,NCOM2),
     $               (KRETBN(I),I=1,NCOM2),BGNPRF,AGKPRN,
     $               (KRETAN(I),I=1,NCOM2),LINPRF
      READ (LPRZRS) (NUPTG(I),I=1,NCOM2),(PNUTG(I),I=1,NCOM2),
     $               (ANUTF(I),I=1,NCOM2)
      READ (LPRZRS) ((NRXF(K,I),I=1,NCOM2),K=1,16)
      READ (LPRZRS) ((NCFX1(K,I),K=1,7),I=1,3),
     $               ((NCFX2(K,I),K=1,NCOM2),I=1,3)
      NCP1 = NCOM2 + 1
      READ (LPRZRS) ((NCFX3(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX4(K,I),K=1,NCOM2),I=1,3)
      READ (LPRZRS) ((NCFX5(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX6(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX7(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX8(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX9(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX10(K,I),K=1,3),I=1,3),
     $               ((NCFX11(K,I),K=1,3),I=1,3)
      READ (LPRZRS) ((NCFX12(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX13(K,I),K=1,NCOM2),I=1,3)
      READ (LPRZRS) ((NCFX14(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX15(K,I),K=1,NCOM2),I=1,3)
      READ (LPRZRS) ((NCFX16(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX17(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX18(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX19(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX20(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX21(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX22(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX23(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) (NCFX24(1,I),I=1,3),((NCFX25(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX26(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX27(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((NCFX28(K,I),K=1,NCP1),I=1,3)
      READ (LPRZRS) ((CNIT(K,I),I=1,NCOM2),K=1,8)
C
      IF (RSTFG.EQ.3) THEN
C       last read, ok to delete
        CLOSE (UNIT=LPRZRS,STATUS='DELETE')
      ELSE
C       dont delete, rewind
        REWIND (UNIT=LPRZRS)
      END IF
C
      CALL SUBOUT
C
      RETURN
      END
C
C
C
      SUBROUTINE   PRZECH (LECHO,LMODID,SEPTON,NITRON,
     I                     IDAY0,IMON0,IYR0,IDAYN,IMONN,IYRN)
C
C     + + + PURPOSE + + +
C     echoes user input variables
C     Modification date: 2/14/92 JAM
C
      USE General_Vars
      Use m_Wind
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER*4   LECHO,IDAY0,IMON0,IYR0,IDAYN,IMONN,IYRN
      CHARACTER*3 LMODID
      LOGICAL     SEPTON,NITRON
C
C     + + + ARGUMENT DEFINITIONS + + +
C     LECHO  - local fortran unit number for file FECHO
C     LMODID - character string for output file identification
C     SEPTON - septic effluent on flag
C     NITRON - nitrogen modeling on flag
C     IDAY0  - ???
C     IMON0  - ???
C     IYR0   - ???
C     IDAYN  - ???
C     IMONN  - ???
C     IYRN   - ???
C
C     + + + PARAMETERS + + +
      INCLUDE 'PPARM.INC'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMET.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CIRGT.INC'
      INCLUDE 'CBIO.INC'
      INCLUDE 'HLFDUM.INC'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER*4    NLINES,UL,LL,J,K,I,M,APM,APD,HAM,HAD,MAM,MAD,
     1             EMM,EMD,KM
      CHARACTER*4  BLNK
      CHARACTER*80 MESAGE
C
C     + + + INTRINSICS + + +
      INTRINSIC   MOD,INT
C
C     + + + EXTERNALS + + +
      EXTERNAL    SUBIN,SUBOUT,NITECH
C
C     + + + DATA INITIALIZATIONS + + +
      DATA BLNK/'    '/
C
C     + + + OUTPUT FORMATS + + +
C2000  FORMAT(1X,A3,/,1X,A3,1X,35('*'),/,1X,A3,1X,'*',T40,'*',
2000  FORMAT(1X,A3,/,1X,A3,1X,35('*'))
2001  FORMAT(
     7        1X,A3,1X,
     8      /,1X,A3,' ',A78,/,1X,A3,/,1X,A3)
2010  FORMAT(1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,1X,'SIMULATION START DATE ',
     1       '(DAY-MONTH-YEAR)',T53,I2,' ',A4,', ',I2,/,1X,A3,
     2       1X,'SIMULATION  END  DATE (DAY-MONTH-YEAR)',T53,I2,' ',
     3       A4,', ',I2)
2018  FORMAT(1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,1X,'HYDROLOGY AND SEDIMENT',
     1       ' RELATED PARAMETERS',/,1X,A3,
     2           1X,'-----------------------------------------')
2020  FORMAT(1X,A3,/,1X,A3,1X,'PAN COEFFICIENT FOR EVAPORATION',T54,
     1       F10.4,/,1X,A3,1X,'FLAG FOR ET SOURCE (0=EVAP,1=TEMP, ',
     2       '2=EITHER)',T54,I10,/,1X,A3,1X,'DEPTH TO WHICH ET IS ',
     3       'COMPUTED YEAR-ROUND (CM)',T54,F10.4)
2025  FORMAT(1X,A3,/,1X,A3,1X,'PRECIP DSN : ',I6,
     1             /,1X,A3,1X,'EVAP DSN:    ',I6,
     2             /,1X,A3,1X,'TEMP DSN:    ',I6,
     3             /,1X,A3,1X,'WIND DSN:    ',I6,
     4             /,1X,A3,1X,'SOLRAD DSN:  ',I6)
2030  FORMAT (1X,A3,/,1X,A3,1X,'MONTHLY DAYLIGHT HOURS',/,1X,A3,
     1        T11,'MONTH',T20,'DAY HOURS',T37,'MONTH',T45,'DAY HOURS',
     2        T61,'MONTH',T70,'DAY HOURS')
2035  FORMAT (1X,A3,T13,A4,T23,G10.4,T38,A4,T48,G10.4,T63,A4,
     1        T73,G10.4,/,1X,A3)
2040  FORMAT (1X,A3,1X,'SNOW MELT COEFFICIENT (CM/DEG-C-DAY)',T58,F10.4)
2050  FORMAT (1X,A3,1X,'INITIAL CROP NUMBER',T54,I10,/,1X,A3,1X,
     1        'INITIAL CROP CONDITION',T54,I10,/,1X,A3,/,1X,A3)
2060  FORMAT (1X,A3,1X,'SOIL EROSION PARAMETERS',/,
     1        1X,A3,1X,'-----------------------',/,1X,A3,/,
     2        1X,A3,1X,'USLE "K"  PARAMETER',T54,G10.4,/,
     3        1X,A3,1X,'USLE "LS" PARAMETER',T54,G10.4,/,
     4        1X,A3,1X,'USLE "P"  PARAMETER',T54,G10.4,/,
     5        1X,A3,1X,'FIELD OR PLOT AREA (HA)',T54,G10.4,/,
     6        1X,A3,1X,'AVERAGE EROSIVE STORM DURATION (HR)',T54,G10.4,
     7        /,1X,A3,/,1X,A3)
2061  FORMAT (1X,A3,1X,'SOIL EROSION PARAMETERS',/,
     1        1X,A3,1X,'-----------------------',/,1X,A3,/,
     2        1X,A3,1X,'USLE "K"  PARAMETER',T54,G10.4,/,
     3        1X,A3,1X,'USLE "LS" PARAMETER',T54,G10.4,/,
     4        1X,A3,1X,'USLE "P"  PARAMETER',T54,G10.4,/,
     5        1X,A3,1X,'FIELD OR PLOT AREA (HA)',T54,G10.4,/,
     6        1X,A3,1X,'STORM TYPE',T54,I4,/,
     6        1X,A3,1X,'SLOPE',T54,G10.4,/,
     6        1X,A3,1X,'HYDRAULIC LENGTH (M)',T54,G10.4,/,
     7        1X,A3,/,1X,A3)
2066  FORMAT (1X,A3,1X,'CROPPING EROSION PARAMETERS',/,
     1        1X,A3,1X,'---------------------------',/,
     2        1X,A3)
2062  FORMAT (1X,A3,/,1X,A3,1X,'CROP NUMBER',T54,I4,/,
     2        1X,A3,1X,'NUMBER OF USLEC FACTORS',T54,I4,/,
     7        1X,A3)
2063  FORMAT (1X,A3,1X,' #   DAY  MONTH  USLEC  MANNINGS N',
     1        T50,'CURVE NUMBERS',/,
     1        1X,A3,1X,T44,'AMC I   AMC II  AMC III',/,
     1        1X,A3)
2064  FORMAT (1X,A3,1X,I2,4X,I2,5X,I2,2X,F5.3,4X,F5.3,3X,3I8)
2065  FORMAT  (1X,A3,/,1X,A3)
2070  FORMAT (1X,A3,1X,'CROP INFORMATION',/,1X,A3,1X,
     1        '----------------',/,1X,A3,/,1X,A3,T13,'MAXIMUM'
     2        ,T55,'SURFACE',/,1X,A3,T13,'INTERCEPT.' ,T23,'MAXIMUM'
     3        ,T35,'MAXIMUM',T45,'MAXIMUM',T55,'CONDITION',T65,
     4        ' MAXIMUM',T105,/,1X,A3,T6,
     5        'CROP',T13,'POTENTIAL',T23,'ROOT DEPTH',T35,'COVER',T45,
     6        'WEIGHT',T55,'AFTER',T65,' HEIGHT',T74,' AMC',T80,
     7        'RUNOFF CURVE NUMBERS',T105,/,1X,A3,T6,
     8        'NUMBER',T13,'  (CM)',T23,'  (CM)',T35,' (%)   ',T45,
     9        '(KG/M**2)',T55,'HARVEST',T65,'  (CM)',T75,
     X        '    FALLOW    CROP  RESIDUE',T105,/,1X,A3)
2071  FORMAT (1X,A3,1X,'CROP INFORMATION',/,1X,A3,1X,
     1        '----------------',/,1X,A3,/,1X,A3,T13,'MAXIMUM'
     2        ,T55,'SURFACE',/,1X,A3,T13,'INTERCEPT.' ,T23,'MAXIMUM'
     3        ,T35,'MAXIMUM',T45,'MAXIMUM',T55,'CONDITION',T65,
     4        ' MAXIMUM',T105,/,1X,A3,T6,
     5        'CROP',T13,'POTENTIAL',T23,'ROOT DEPTH',T35,'COVER',T45,
     6        'WEIGHT',T55,'AFTER',T65,' HEIGHT',T74,T80,
     7        T105,/,1X,A3,T6,
     8        'NUMBER',T13,'  (CM)',T23,'  (CM)',T35,' (%)   ',T45,
     9        '(KG/M**2)',T55,'HARVEST',T65,'  (CM)',T75,
     X        T105,/,1X,A3)
2080  FORMAT (1X,A3,1X,T77,'I',I7,I8,I9,/,1X,A3,
     1        1X,I4,T15,G10.4,T25,G10.4,T35,G10.4,T45,G10.4,T55,I5,
     2        T65,F8.3,T76,'II',I7,I8,I9,T105,/,1X,A3,
     3        1X,T75,'III',I7,I8,I9,/,1X,A3,/,1X,A3)
2081  FORMAT (1X,A3,1X,T77,/,1X,A3,
     1        1X,I4,T15,G10.4,T25,G10.4,T35,G10.4,T45,G10.4,T55,I5,
     2        T65,F8.3,T76,T105,/,1X,A3,
     3        1X,T75,/,1X,A3,/,1X,A3)
2090  FORMAT (1X,A3,1X,'CROP ROTATION INFORMATION',/,1X,A3,
     1        1X,'-------------------------',/,1X,A3,/,1X,A3,
     2        1X,'CROP'  ,T25,'EMERGENCE',T45,'MATURATION',
     3        T65,'HARVEST',/,1X,A3,
     4        1X,'NUMBER',T25,'DATE'     ,T45,'DATE'  ,
     5        T65,'DATE',/,1X,A3)
2100  FORMAT (1X,A3,1X,I4,T25,3(I2,1X,A4,', ',I2,9X))
2108  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,
     1        1X,'PESTICIDE APPLICATION INFORMATION',/,1X,A3,
     2        1X,'---------------------------------')
2115  FORMAT (1X,A3,/,1X,A3,1X,T40,'CHEMICAL',T55,'PESTICIDE',
     *        T70,'INCORPORATION',/,
     1        1X,A3,1X,'PESICIDE',T25,'APPLICATION',
     *        T40,'APPLICATION',T55,'APPLIED',T70,
     2        'DEPTH',/,1X,A3,1X,'NAME',T25,'DATE',
     *        T40,'MODEL',T55,'(KG/HA)',T70,
     3        '(CM)',/,1X,A3)
2121  FORMAT (1X,A3,1X,A20,T25,I2,1X,A4,', ',I2,T40,I8,
     *        T55,G10.4,T70,G10.4)
2129  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,1X,
     1        'PLANT PESTICIDE PARAMETERS',/,1X,A3,1X,
     2        '--------------------------',/,1X,A3,/,1X,A3)
2130  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,1X,
     1        'PLANT PESTICIDE PARAMETERS',/,1X,A3,1X,
     2        '--------------------------',/,1X,A3,/,1X,A3,1X,
     3        'MODEL UTILIZED (1=SOIL,2=LINEAR,3=EXPONENTIAL)',
     4        T54,I10/,1X,A3)
2131  FORMAT (1X,A3,1X,'FOLIAR PESTICIDE DECAY RATE (/DAY)',T54,G10.4,/,
     1        1X,A3,1X,'EXTRACTION COEFFICIENT      (/CM)',T54,G10.4,/,
     2        1X,A3,1X,'FOLIAR PESTICIDE VOLATILIZATION RATE (/DAY)',
     3        T54,G10.4)
2132  FORMAT (1X,A3,1X,'FILTRATION PARAMETER     (M**2/MG)',T54,G10.4)
2133  FORMAT (1X,A3,1X,'AFTER HARVEST DATE, REMAINING ','CHEMICAL ',I2,
     *        ' IN CANOPY IS SURFACE APPLIED',/,
     *        1X,A3,1X,'PLANT UPTAKE EFFICIENCY FACTOR',T54,G10.4)
2134  FORMAT (1X,A3,1X,'AFTER HARVEST DATE, REMAINING ','CHEMICAL ',I2,
     *        ' IN CANOPY IS REMOVED',/,
     *        1X,A3,1X,'PLANT UPTAKE EFFICIENCY FACTOR',T54,G10.4)
2135  FORMAT (1X,A3,1X,'AFTER HARVEST DATE, REMAINING ','CHEMICAL ',I2,
     *        ' IN CANOPY IS TREATED AS SURFACE RESIDUE',/,
     *        1X,A3,1X,'PLANT UPTAKE EFFICIENCY FACTOR',T54,G10.4)
2136  FORMAT (1X,A3,/,1X,A3,1X,T60,A20,A20,A20,/,1X,A3,/,
     1        1X,A3,1X,'FOLIAR PESTICIDE DECAY RATE (/DAY)',T60,
     2        G10.4,T80,G10.4,T100,G10.4,/,1X,A3,1X,
     3        'EXTRACTION COEFFICIENT      (/CM)',T60,G10.4,T80,
     4        G10.4,T100,G10.4,/,1X,A3,1X,
     5        'FOLIAR PESTICIDE VOLATILIZATION RATE (/DAY)',T60,
     6        G10.4,T80,G10.4,T100,G10.4,/,1X,A3,1X,
     5        'FOLIAR TRANSFORMATION RATE (1->2)(/DAY)',T60,
     6        G10.4,/,1X,A3,1X,
     5        'FOLIAR TRANSFORMATION RATE (1->3)(/DAY)',T60,
     6        G10.4,/,1X,A3,1X,
     5        'FOLIAR TRANSFORMATION RATE (2->3)(/DAY)',T60,
     6        G10.4,/,1X,A3)
2137  FORMAT (1X,A3,/,1X,A3,1X,T60,A20,A20,/,1X,A3,/,
     1        1X,A3,1X,'FOLIAR PESTICIDE DECAY RATE (/DAY)',T60,
     2        G10.4,T80,G10.4,/,1X,A3,1X,
     3        'EXTRACTION COEFFICIENT      (/CM)',T60,G10.4,T80,
     4        G10.4,/,1X,A3,1X,
     5        'FOLIAR PESTICIDE VOLATILIZATION RATE (/DAY)',T60,
     6        G10.4,T80,G10.4,/,1X,A3,1X,
     5        'FOLIAR TRANSFORMATION RATE (1->2)(/DAY)',T60,
     6        G10.4,/,1X,A3)
2138  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,
     1        T6,'GENERAL SOIL INFORMATION',/,1X,A3,
     2        T6,'------------------------',/,1X,A3,/,1X,A3,
     3        T6,'CORE DEPTH (CM)',T58,G10.4,/,1X,A3,
     4        T6,'TOTAL HORIZONS IN CORE',T54,I10,/,1X,A3,
     6        T6,'THETA FLAG',T33,'(0=INPUT,1=CALCULATED)',
     7        T55,I9,/,1X,A3,
     8        T6,'PARTITION COEFFICIENT FLAG',
     9        T33,'(0=INPUT,1=CALCULATED)',T55,I9,/,1X,A3,
     X        T6,'BULK DENSITY FLAG',T33,'(0=INPUT,1=CALCULATED)',
     1        T55,I9)
21382 FORMAT( 1X,A3,
     2        T6,'SOIL HYDRAULICS MODULE     (0=HYDR1,1=HYDR2)',
     3        T55,I9,/,1X,A3,
     4        T6,'TRANSPORT SOLUTION TECHNIQUE   (0=BACKDIFF,1=MOC)',
     5        T55,I9,/,1X,A3,
     6        T6,'IRRIGATION FLAG                (0=OFF,1=ON)',
     7        T55,I9,/,1X,A3,
     6        T6,'TEMPERATURE CORRECTION         (0=OFF,1=ON)',
     7        T55,I9,/,1X,A3,
     8        T6,'THERMAL CONDUCTIVITY    (0=SUPPLIED,1=CALCULATED)',
     9        T55,I9,/,1X,A3,
     A        T6,'BIODEGRADATION FLAG            (0=OFF,1=ON)',
     B        T55,I9)
21384 FORMAT (1X,A3,/,1X,A3,
     1        T6,'BIODEGRADATION VALUES',/,1X,A3,
     2        T6,'---------------------',/,1X,A3,/,1X,A3,
     3        T6,'MAINTENANCE COEFFICIENT OF Xi POPULATION =',
     4        T55,F8.3,F8.3,F8.3,F8.3,/,1X,A3,
     B        T6,'AVERAGE ENZYME CONTENT OF Xi POPULATION =',
     C        T55,F8.3,/,1X,A3,
     D        T6,'SATURATION CONTENT OF Xi POPULATION =',
     E        T55,F8.2,F8.2,F8.2,F8.2,F8.2,/,1X,A3,
     J        T6,'INHIBITION CONSTANT =',
     K        T55,F8.2,/,1X,A3,
     L        T6,'CARBON SOLUBILIZATION CONSTANT =',
     M        T55,F8.3,/,1X,A3,
     N        T6,'DEATH RATE OF THE Xi POPULATION =',
     O        T55,F8.3,F8.3,F8.3,F8.3,/,1X,A3,
     P        T6,'SECOND ORDER DEATH RATE OF Xi =',
     Q        T55,F8.2)
21387 FORMAT  (1X,A3,
     R        T6,'DISSOCIATION CONSTANT =',
     S        T55,F8.2,/,1X,A3,
     T        T6,'MAX. SPECIFIC GROWTH RATE OF Xi =',
     U        T55,F8.3,F8.3,F8.3,F8.3,F8.3,/,1X,A3,
     V        T6,'TOTAL GROWTH YIELD OF Xi =',
     W        T55,F8.3,F8.3,F8.3,F8.3,F8.3,/,1X,A3)
21385 FORMAT (1X,A3,/,1X,A3,T6,'HORIZON     Q        CM      Y(1)  ',
     1        '   Y(2)     Y(3)     Y(4)  ',/,
     2        1X,A3,T6,'-------- -------- -------- -------- --------',
     4        ' -------- --------',/,1X,A3)
21386 FORMAT (1X,A3,T8,I2,5X,F8.5,1X,F8.5,1X,F8.6,1X,F8.6,1X,F8.3,1X,
     1        F8.3)
2140  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,T6,'SOIL HORIZON ',
     1        'INFORMATION',/,1X,A3,T6,'------------------------')
2150  FORMAT (1X,A3,/,1X,A3,T28,'DISS.',T35,'SORB.',T42,'VAPOR',T49,
     1        'INITIAL',T83,'FIELD',T93,'WILTING',/,1X,A3,T28,'PEST.',
     2        T35,'PEST.',T42,'PEST.',T49,'SOIL',T83,'CAPACITY',T93,
     3        'POINT',/,1X,A3,T18,'BULK',T28,'DECAY',T35,'DECAY',T42,
     4        'DECAY',T49,'WATER',T59,'DRAINAGE',T71,
     +        'LAT DRAIN',T83,'WATER',T93,
     5        'WATER',T103,'PARTITION',T113,'DISPERSION',T125,'ORGANIC',
     6        /,1X,A3,T6,'HORI-',T12,'THICK',T18,'DENSITY',T28,'RATE',
     7        T35,'RATE',T42,'RATE',T49,'CONTENT',T59,'PARAMETER',T71,
     +        'PARAMETER',T83,
     8        'CONTENT',T93,'CONTENT',T103,'COEFF',T113,'COEFF',T125,
     9        'CARBON',/,1X,A3,T7,'ZON',T12,'(CM)',T18,'(G/CM**3)',T28,
     X        '(/DAY)',T35,'(/DAY)',T42,'(/DAY)',T49,'(CM/CM)',T59,
     +        '(/DAY)',T71,
     1        '(/DAY)',T83,'(CM/CM)',T93,'(CM/CM)',T103,'(CM**3/G)',
     2        T113,'(CM**2/DAY)',T125,'  (%)',
     3        /,1X,A3,T6,122(1H-),/,1X,A3)
2160  FORMAT (1X,A3,/,1X,A3,T28,'DISS.',T35,'SORB.',T42,'VAPOR',T49,
     1        'INITIAL',T83,'FIELD',T93,'WILTING',/,1X,A3,T28,'PEST.',
     2        T35,'PEST.',T42,'PEST.',T49,'SOIL',T83,'CAPACITY',T93,
     3        'POINT',/,1X,A3,T18,'BULK',T28,'DECAY',T35,'DECAY',T42,
     4        'DECAY',T49,'WATER',T59,'DRAINAGE',T71,
     +        'LAT DRAIN',T83,'WATER',T93,
     5        'WATER',T103,'ORGANIC',T113,'DISPERSION',/,1X,A3,T6,
     6        'HORI-',T12,'THICK',T18,'DENSITY',T28,'RATE',T35,'RATE',
     7        T42,'RATE',T49,'CONTENT',T59,'PARAMETER',T71,
     +        'PARAMETER',T83,'CONTENT',
     8        T93,'CONTENT',T103,'CARBON',T113,'COEFF',/,1X,A3,T7,'ZON',
     9        T12,'(CM)',T18,'(G/CM**3)',T28,'(/DAY)',T35,'(/DAY)',T42,
     X        '(/DAY)',T49,'(CM/CM)',T59,'(/DAY)',T71,'(/DAY)',T83,
     +        '(CM/CM)',T93,
     1        '(CM/CM)',T103,'  (%)    ',T113,'(CM**2/DAY)',/,1X,A3,
     2        T6,118(1H-),/,1X,A3)
2170  FORMAT (1X,A3,/,1X,A3,T28,'DISS.',T35,'SORB.',T42,'VAPOR',T49,
     1        'INITIAL',/,1X,A3,T28,'PEST.',T35,'PEST.',T42,'PEST.',
     2        T49,'SOIL',/,1X,A3,T18,'BULK',T28,'DECAY',T35,'DECAY',
     3        T42,'DECAY',T49,'WATER',T59,'DRAINAGE',T71,
     +        'LAT DRAIN',T103,'PARTITION',
     4        T113,'DISPERSION',T125,'ORGANIC',/,1X,A3,T6,'HORI-',T12,
     5        'THICK',T18,'DENSITY',T28,'RATE',T35,'RATE',T42,'RATE',
     6        T49,'CONTENT',T59,'PARAMETER',T71,
     +        'PARAMETER',T83,'SAND',T93,'CLAY',T103,
     7        'COEFF',T113,'COEFF',T125,'CARBON',/,1X,A3,T7,'ZON',T12,
     8        '(CM)',T18,'(G/CM**3)',T28,'(/DAY)',T35,'(/DAY)',T42,
     9        '(/DAY)',T49,'(CM/CM)',T59,'(/DAY)',T71,'(DAY/)',T83,
     +        '  (%)  ',T93,
     X        '  (%)  ',T103,'(CM**3/G)',T113,'(CM**2/DAY)',T125,
     1        '  (%)',/,1X,A3,T6,118(1H-),/,1X,A3)
2180  FORMAT (1X,A3,/,1X,A3,T28,'DISS.',T35,'SORB.',T42,'VAPOR',T49,
     1        'INITIAL',/,1X,A3,T28,'PEST.',T35,'PEST.',T42,'PEST.',
     2        T49,'SOIL',/,1X,A3,T18,'BULK',T28,'DECAY',T35,'DECAY',
     3        T42,'DECAY',T49,'WATER',T59,'DRAINAGE',T71,
     +        'LAT DRAIN',T103,'ORGANIC',
     4        T113,'DISPERSION',/,1X,A3,T6,'HORI-',T12,'THICK',T18,
     5        'DENSITY',T28,'RATE',T35,'RATE',T42,'RATE',T49,'CONTENT',
     6        T59,'PARAMETER',T71,'PARAMETER',T83,
     +        'SAND',T93,'CLAY',T103,'CARBON',T113,
     7        'COEFF',/,1X,A3,T7,'ZON',T12,'(CM)',T18,'(G/CM**3)',T28,
     8        '(/DAY)',T35,'(/DAY)',T42,'(/DAY)',T49,'(CM/CM)',T59,
     9        '(/DAY)',T71,'(/DAY)',T83,'  (%)  ',T93,'  (%)  ',
     +        T103,'  (%)    ',
     X        T113,'(CM**2/DAY)',/,1X,A3,T6,118(1H-),/,1X,A3)
2155  FORMAT (1X,A3,/,1X,A3,T30,'INITIAL',T72,'FIELD',T87,'WILTING',/,
     1        1X,A3,T30,'SOIL',T72,'CAPACITY',T87,'POINT',/,1X,A3,
     2        T18,'BULK',T30,'WATER',T45,'DRAINAGE',T60,
     +        'LAT DRAIN',T72,'WATER',T87,
     3        'WATER',T102,'ORGANIC',/,1X,A3,T6,'HORI-',T12,'THICK',
     4        T18,'DENSITY',T30,'CONTENT',T45,'PARAMETER',T60,
     +        'PARAMETER',T72,
     5        'CONTENT',T87,'CONTENT',T102,'CARBON',/,1X,A3,T7,'ZON',
     6        T12,'(CM)',T18,'(G/CM**3)',T30,'(CM/CM)',T45,
     7        '(/DAY)',T60,'(/DAY)',T72,'(CM/CM)',T87,'(CM/CM)',
     +        T102,'  (%)',
     8        /,1X,A3,T6,122(1H-),/,1X,A3)
2165  FORMAT (1X,A3,/,1X,A3,T30,'INITIAL',T72,'FIELD',T87,'WILTING',/,
     1        1X,A3,T28,T30,'SOIL',T72,'CAPACITY',T87,'POINT',/,1X,A3,
     2        T18,'BULK',T30,'WATER',T45,'DRAINAGE',T60,
     +        'LAT DRAIN',T72,'WATER',T87,
     3        'WATER',T90,'ORGANIC',/,1X,A3,T6,'HORI-',T12,'THICK',
     4        T18,'DENSITY',T30,'CONTENT',T45,'PARAMETER',T60,
     +        'PARAMETER',T72,'CONTENT',
     5        T87,'CONTENT',T102,'CARBON',/,1X,A3,T7,'ZON',T12,'(CM)',
     6        T18,'(G/CM**3)',T30,'(CM/CM)',T45,'(/DAY)',T60,
     +        '(/DAY)',T72,'(CM/CM)',
     7        T87,'(CM/CM)',T102,'  (%)',/,1X,A3,T6,118(1H-),/,1X,A3)
2175  FORMAT (1X,A3,/,1X,A3,T30,'INITIAL',/,1X,A3,T30,T49,'SOIL',/,1X,
     1        A3,T18,'BULK',T30,'WATER',T45,'DRAINAGE',T60,'LAT DRAIN',
     +        T102,'ORGANIC',/,
     2        1X,A3,T6,'HORI-',T12,'THICK',T18,'DENSITY',T30,'CONTENT',
     3        T45,'PARAMETER',T60,'PARAMETER',T72,'SAND',T87,'CLAY',
     +        T102,'CARBON',/,1X,
     4        A3,T7,'ZON',T12,'(CM)',T18,'(G/CM**3)',T30,'(CM/CM)',T45,
     5        '(/DAY)',T60,'(/DAY)',T72,'  (%)  ',T87,'  (%)  ',T102,
     +        '  (%)',/,
     6        1X,A3,T6,118(1H-),/,1X,A3)
2185  FORMAT (1X,A3,/,1X,A3,T30,'INITIAL',/,1X,A3,T30,'SOIL',/,1X,A3,
     1        T18,'BULK',T30,'WATER',T45,'DRAINAGE',T60,'LAT DRAIN',
     +        T102,'ORGANIC',/,1X,
     2        A3,T6,'HORI-',T12,'THICK',T18,'DENSITY',T30,'CONTENT',
     3        T45,'PARAMETER',T60,'PARAMETER',T72,'SAND',T87,'CLAY',
     +        T102,'CARBON',/,1X,
     4        A3,T7,'ZON',T12,'(CM)',T18,'(G/CM**3)',T30,'(CM/CM)',T45,
     5        '(/DAY)',T60,'(/DAY)',T72,'  (%)  ',T87,'  (%)  ',T102,
     +        '  (%)    ',
     6        /,1X,A3,T6,118(1H-),/,1X,A3)
2188  FORMAT (1X,A3,T7,I2,3X,F5.1,T18,F6.4,T30,F6.3,T45,F4.2,T60,F4.2,
     1       T72,F6.5,T87,F6.3,T102,F6.3)
2190  FORMAT (1X,A3,T7,I2,3X,F5.1,2X,F6.4,2X,F6.5,1X,F4.2,1X,F6.5,1X,
     1        F7.3,3X,F9.3,3X,F9.3,3X,F8.3,2X,F7.3,2X,F9.5,1X,G10.3,
     2        4X,F7.4)
2191  FORMAT (1X,A3,/,1X,A3,/,1X,A3,T6,' HORIZON ',3X,
     1        'LAYER DEPTH (CM)',/,1X,A3)
2192  FORMAT (1X,A3,T6,I5,10X,F6.2)
2193  FORMAT (1X,A3,/,1X,A3,/,1X,A3,T6,' HORIZON ',3X,
     1        'LAYER DEPTH (CM)',3X,'TEMPERATURE',/1X,A3)
2194  FORMAT (1X,A3,T6,I5,10X,F6.2,13X,F6.2)
2195  FORMAT (1X,A3,/,1X,A3,/,1X,A3,T6,' HORIZON ',3X,
     1        'LAYER DEPTH (CM)',3X,'TEMPERATURE',6X,
     2        'SAND',6X,'CLAY',6X,'ORGANIC CARBON',/,1X,A3)
2196  FORMAT (1X,A3,T6,I5,10X,F6.2,13X,F6.2,4X,F8.2,2X,F8.2,8X,F8.2)
2200  FORMAT (1X,A3,T6,5(I9,')',G10.4))
2201  FORMAT (1X,A3,/,1X,A3,/,1X,A3,T6,' HORIZON ',3X,
     1        'LAYER DEPTH (CM)',4X,'TEMPERATURE',8X,
     2        'THERMAL COND',9X,'HEAT CAPACITY',/1X,A3)
2202  FORMAT (1X,A3,T6,I5,10X,F6.2,13X,F6.2,14X,F6.2,15X,F6.2)
2205  FORMAT (1X,A3,/,1X,A3,/,1X,A3,1X,'OUTPUT FILE PARAMETERS',/,1X,A3,
     1        1X,'----------------------',/,1X,A3,/,1X,A3,
     2        1X,'OUTPUT    TIME STEP    LAYER FREQ',/,1X,A3)
2210  FORMAT (1X,A3,/,1X,A3,1X,2X,A4,6X,A4,10X,I4)
2220  FORMAT (1X,A3,/,1X,A3,/,1X,A3,/,1X,A3,
     1        T6,'PLOT FILE INFORMATION',/,1X,A3,
     2        T6,'---------------------',/,1X,A3,/,1X,A3,
     1        T6,'NUMBER OF PLOTTING VARIABLES ',T44,I4,/,1X,A3,
     2        T6,'TIMSER NAME',T25,'MODE',T35,'CMPT BEG',
     3	      T45,'CMPT END',T65,'CONSTANT',T80,'TYPE',T85,'DSN'/,1X,A3)
2230  FORMAT (1X,A3,T6,A4,A1,T25,A4,T35,I3,T45,I3,
     *        T65,G10.4,T80,A1,T85,I4)
2240  FORMAT (1X,A3,/,1X,A3,/,1X,A3,' ',A78,/,1X,A3,/,1X,A3)
2250  FORMAT (1X,A3,/,1X,A3,/,1X,A3,1X,'INITIAL PESTICIDE LEVELS IN ',
     1        'EACH COMPARTMENT (KG/HA)',/,1X,A3,1X,52('-'),/,1X,A3)
2251  FORMAT (1X,A3,/,1X,A3,/,1X,A3,1X,'INITIAL PESTICIDE LEVELS IN ',
     1        'EACH COMPARTMENT (MG/KG)',/,1X,A3,1X,52('-'),/,1X,A3)
2255  FORMAT (1X,A3,/,1X,A3,' MONTHLY VALUES OF SOIL SURFACE ALBEDO
     1 (JAN through DEC)',/,1X,A3,T14,12(F6.2),/,1X,A3,
     1        ' SOIL EMMISSIVITY ',T60,G10.4,/,1X,A3,' HEIGHT ABOVE ',
     2        'GROUND WHERE WIND SPEED MEASURED (M)',T60,G10.4,/,1X,A3,
     3        ' BOTTOM BOUNDARY TEMPERATURE MONTHLY VALUE, JAN - DEC',
     4        /,1X,A3,T14,12(F6.2,1X),/,1X,A3)
2260  FORMAT (1X,A3,/,1X,A3,1X,'PESTICIDE PROPERTY INFORMATION',/,1X,A3,
     1        ' ------------------------------',/,1X,A3,
     2        ' HENRY''S LAW CONSTANT ',T58,G10.4,/,1X,A3,
     3        ' DIFFUSION COEFFICIENT (CM**2/DAY)',T58,G10.4,/1X,A3)
2275  FORMAT (1X,A3,' REACTION HEAT (KCAL/MOLE) ',T58,G10.4,/,1X,A3)
2274  FORMAT (1X,A3,' REACTION HEAT (KCAL/MOLE) ',T60,G10.4,T80,G10.4,
     1        /,1X,A3)
2276  FORMAT (1X,A3,' REACTION HEAT (KCAL/MOLE) ',T60,G10.4,T80,G10.4,
     1        T100,G10.4,/,1X,A3)
2279  FORMAT (1X,A3,/,1X,A3,1X,'PESTICIDE PROPERTY INFORMATION',/,1X,A3,
     1        ' ------------------------------',/,1X,A3,1X,
     2        'PESTICIDE NAME ',T60,A20,A20,/,1X,A3,/,1X,
     3        A3,' HENRY''S LAW CONSTANT',T60,G10.4,T80,G10.4,
     4        /,1X,A3,' DIFFUSION COEFFICIENT (CM**2/DAY)',
     5        T60,G10.4,T80,G10.4,/1X,A3)
2280  FORMAT (1X,A3,/,1X,A3,1X,'PESTICIDE PROPERTY INFORMATION',/,1X,A3,
     1        ' ------------------------------',/,1X,A3,1X,
     2        'PESTICIDE NAME ',T60,A20,A20,A20,/,1X,A3,/,1X,
     3        A3,' HENRY''S LAW CONSTANT',T60,G10.4,T80,G10.4,T100,
     4        G10.4,/,1X,A3,' DIFFUSION COEFFICIENT (CM**2/DAY)',
     5        T60,G10.4,T80,G10.4,T100,G10.4,/1X,A3)
2300  FORMAT (1X,A3,/,1X,A3,1X,T65,A20,A20,A20)
2301  FORMAT (1X,A3,/,
     1        1X,A3,T10,'HORIZON',T30,I10,/,1X,A3,T10,'-------',/,1X,A3)
2302  FORMAT (1X,A3,T10,'LIQUID PHASE DECAY RATE (/DAY)',
     1        T60,3(10X,G9.3))
2303  FORMAT (1X,A3,T10,'SOLID PHASE DECAY RATE (/DAY)',
     1        T60,3(10X,G9.3))
2304  FORMAT (1X,A3,T10,'GAS PHASE DECAY RATE (/DAY)',
     1        T60,3(10X,G9.3))
2305  FORMAT (1X,A3,T10,'ADSORPTION PARTITION COEFFICIENTS (CM**3/G)',
     1        T60,3(10X,G9.3))
2306  FORMAT (1X,A3,T10,'DISPERSION COEFFICIENTS (CM**2/DAY)',T60,
     1        3(10X,G9.3))
2307  FORMAT (1X,A3,T10,'TRANSFORMATION RATE CONSTANTS LIQ. (/DAY)',
     1        T65,'(1-2)',G9.3,5X,'(1-3)',G9.3,5X,'(2-3)',G9.3)
2327  FORMAT (1X,A3,T10,'TRANSFORMATION RATE CONSTANTS SOL. (/DAY)',
     1        T65,'(1-2)',G9.3,5X,'(1-3)',G9.3,5X,'(2-3)',G9.3)
2308  FORMAT (1X,A3,/,1X,A3,1X,T65,A20,A20)
2320  FORMAT (1X,A3,'BI-PHASE DAY',T65,I4,T85,I4)
2321  FORMAT (1X,A3,'BI-PHASE MONTH',T65,I4,T85,I4)
2322  FORMAT (1X,A3,'BI-PHASE DAYS AFTER APPLICATION',T65,I4,T85,I4,
     1        /,1X,A3)
2330  FORMAT (1X,A3,'BI-PHASE DAY',T65,I4,T85,I4,T105,I4)
2331  FORMAT (1X,A3,'BI-PHASE MONTH',T65,I4,T85,I4,T105,I4)
2332  FORMAT (1X,A3,'BI-PHASE DAYS AFTER APPLICATION',T65,I4,T85,I4,
     1        T105,I4,/,1X,A3)
2309  FORMAT (1X,A3,/,
     1        1X,A3,T10,'HORIZON',T30,I10,/,1X,A3,T10,'-------',/,1X,A3)
2310  FORMAT (1X,A3,T10,'LIQUID PHASE DECAY RATE (/DAY)',
     1        T60,2(10X,G9.3))
2311  FORMAT (1X,A3,T10,'SOLID PHASE DECAY RATE (/DAY)',
     1        T60,2(10X,G9.3))
2312  FORMAT (1X,A3,T10,'GAS PHASE DECAY RATE (/DAY)',
     1        T60,2(10X,G9.3))
2313  FORMAT (1X,A3,T10,'ADSORPTION PARTITION COEFFICIENTS (CM**3/G)',
     1        T60,2(10X,G9.3))
2314  FORMAT (1X,A3,T10,'DISPERSION COEFFICIENTS (CM**2/DAY)',T60,
     1        2(10X,G9.3))
2315  FORMAT (1X,A3,T10,'TRANSFORMATION RATE CONSTANTS LIQ. (/DAY)',
     1        T65,'(1-2)',G9.3)
2325  FORMAT (1X,A3,T10,'TRANSFORMATION RATE CONSTANTS SOL. (/DAY)',
     1        T65,'(1-2)',G9.3)
 2410 FORMAT (1X,A3,/,1X,A3,5X,'IRRIGATION DATA:'/,1X,A3)
 2420 FORMAT (1X,A3,5X,'IRTYPE = ',I5,/,1X,A3,5X,'LEACHING FACTOR:',
     1        E10.3,5X,'IRRIGATION FRACTION:',E10.3)
 2430 FORMAT (1X,A3,5X,'SPRINKLER CAPACITY (CM/HR):',E10.3,
     1        /,1X,A3,5X,'SPRINKLER UNIFORMITY COEFFICIENT:',E10.3)
 2440 FORMAT (1X,A3,/,1X,A3,/,1X,A3,5X,'FLOW RATE ENTERING FURROW: ',
     1        E10.3,/,1X,A3,5X,'BOTTOM WIDTH:',E10.3,5X,'SIDE SLOPE:',
     2        E10.3,/,1X,A3,5X,'CHANNEL SLOPE:',E10.3,/,1X,A3,5X,
     3        'MANNINGS N:',E10.3,5X,'FURROW LENGTH:',E10.3,/,1X,A3,5X,
     4        'LOCATION IN FURROW USED IN TRANSPORT MODEL:',E10.3)
 2450 FORMAT (1X,A3,5X,'SAT. HYDRAULIC COND.:',E10.3,5X,
     1        'SUCTION PARAM:',E10.3)
C
C     + + + END SPECIFICATIONS + + +
C
      MESAGE = 'PRZECH'
      CALL SUBIN(MESAGE)
C
C     write simulation title
      WRITE(LECHO,2000) (LMODID,I=1,2)
      Call przm_id(LECHO, LMODID)
      WRITE(LECHO,2001) (LMODID,I=1,2),TITLE,(LMODID,I=1,2)
C
C     write starting and ending dates of simulation
      WRITE(LECHO,2010) (LMODID,I=1,4),IDAY0,CMONTH(IMON0),IYR0,
     1                  LMODID,IDAYN,CMONTH(IMONN),IYRN
C      WRITE(6,*)CMONTH(IMON0),CMONTH(IMONN)
C
C-----Write out hydrology and sediment related parameters
      WRITE(LECHO,2240) (LMODID,I=1,3),HTITLE,(LMODID,I=1,2)
      WRITE(LECHO,2018) (LMODID,I=1,5)
      WRITE(LECHO,2020) (LMODID,I=1,2),PFAC,LMODID,IPEIND,
     1                  LMODID,ANETD
      IF (METDSN(1).GT.0) WRITE(LECHO,2025) LMODID,
     1                  (LMODID,METDSN(I),I=1,5)
      IF (IPEIND.EQ.1.OR.IPEIND.EQ.2) THEN
        WRITE(LECHO,2030) (LMODID,I=1,3)
        DO 5 I= 1,4
          J= 3*(I-1)+ 1
          WRITE(LECHO,2035) LMODID,(CMONTH(K),DT(K),K=J,J+2),LMODID
 5      CONTINUE
      END IF
C
      WRITE(LECHO,2040) LMODID,SFAC
      WRITE(LECHO,2050) LMODID,INICRP,LMODID,ISCOND,(LMODID,I=1,2)
      IF (ERFLAG.EQ.1)THEN
        WRITE(LECHO,2060) (LMODID,I=1,4),USLEK,LMODID,
     1                   USLELS,LMODID,USLEP,LMODID,AFIELD,LMODID,
     2                   TR,(LMODID,I=1,2)
      ELSEIF (ERFLAG.GT.1)THEN
        WRITE(LECHO,2061) (LMODID,I=1,4),USLEK,LMODID,
     1                   USLELS,LMODID,USLEP,LMODID,AFIELD,LMODID,
     2                   IREG,LMODID,SLP,LMODID,HL,(LMODID,I=1,2)
      ENDIF
C
      IF (ERFLAG.NE.0)THEN
        WRITE(LECHO,2066) (LMODID,I=1,3)
        DO 78 KM=1,NDC
          WRITE(LECHO,2062) LMODID,LMODID,KM,LMODID,NUSLEC(KM),LMODID
          WRITE(LECHO,2063) (LMODID,I=1,3)
            DO 79 J=1,NUSLEC(KM)
              WRITE(LECHO,2064) LMODID,J,GDUSLEC(KM,J),GMUSLEC(KM,J),
     1                           USLEC(KM,J),MNGN(KM,J),CN(KM,J,1),
     2                           CN(KM,J,2),CN(KM,J,3)
 79         CONTINUE
 78     CONTINUE
        WRITE(LECHO,2065) (LMODID,I=1,2)
      ENDIF
C     write out crop information
      IF (ERFLAG.EQ.0)WRITE(LECHO,2070) (LMODID,I=1,8)
      IF (ERFLAG.GT.0)WRITE(LECHO,2071) (LMODID,I=1,8)
      DO 10 I=1,NDC
        IF (ERFLAG.EQ.0)THEN
        WRITE(LECHO,2080) LMODID,(CN(I,K,1),K=1,3),LMODID,ICNCN(I),
     1                      CINTCP(I),AMXDR(I),COVMAX(I),WFMAX(I),
     2                      ICNAH(I),HTMAX(I),(CN(I,K,2),K=1,3),
     3                      LMODID,(CN(I,K,3),K=1,3),
     4                      (LMODID,J=1,2)
        ELSEIF (ERFLAG.GT.0)THEN
          WRITE(LECHO,2081) LMODID,LMODID,ICNCN(I),
     1                      CINTCP(I),AMXDR(I),COVMAX(I),WFMAX(I),
     2                      ICNAH(I),HTMAX(I),
     3                      LMODID,(LMODID,J=1,2)
        ENDIF
10    CONTINUE
C
C     write out crop rotation information
      WRITE(LECHO,2090) (LMODID,I=1,6)
C
      DO 50 I=1,NCPDS
        LEAP=1
        IF (MOD(IYREM(I),4).EQ.0) LEAP=2
        DO 20 J=1,12
          IF (IEMER(I) .GT. CNDMO(LEAP,J) .AND. IEMER(I) .LE.
     1      CNDMO(LEAP,J+1)) EMM=J
20      CONTINUE
        EMD=IEMER(I)-CNDMO(LEAP,EMM)
        LEAP=1
        IF (MOD(IYRMAT(I),4) .EQ. 0) LEAP=2
        DO 30 J=1,12
          IF (MAT(I) .GT. CNDMO(LEAP,J) .AND. MAT(I) .LE.
     1      CNDMO(LEAP,J+1)) MAM=J
30      CONTINUE
        MAD=MAT(I)-CNDMO(LEAP,MAM)
        LEAP=1
        IF (MOD(IYRHAR(I),4) .EQ. 0) LEAP=2
        DO 40 J=1,12
          IF (IHAR(I) .GT. CNDMO(LEAP,J) .AND. IHAR(I) .LE.
     1      CNDMO(LEAP,J+1)) HAM=J
40      CONTINUE
        HAD=IHAR(I)-CNDMO(LEAP,HAM)
        WRITE(LECHO,2100) LMODID,INCROP(I),EMD,CMONTH(EMM),IYREM(I),
     1                   MAD,CMONTH(MAM),IYRMAT(I),
     2                   HAD,CMONTH(HAM),IYRHAR(I)
50    CONTINUE
C
      IF (.NOT.NITRON) THEN
C       write pesticide application information
        WRITE(LECHO,2240) (LMODID,J=1,3),PTITLE,(LMODID,J=1,2)
        WRITE(LECHO,2108) (LMODID,J=1,5)
C
        WRITE(LECHO,2115) (LMODID,J=1,5)
C
        DO 70 I=1,NAPS
          LEAP=1
          IF (MOD(IAPYR(I),4) .EQ. 0) LEAP=2
          DO 60 J=1,12
            IF (IAPDY(I) .GT. CNDMO(LEAP,J) .AND. IAPDY(I) .LE.
     1        CNDMO(LEAP,J+1)) APM=J
60        CONTINUE
          APD=IAPDY(I)-CNDMO(LEAP,APM)
          DO 65 K=1,NCHEM
            IF (TAPP(K,I) .GT. 0.0) WRITE(LECHO,2121) LMODID,PSTNAM(K),
     1                     APD,CMONTH(APM),IAPYR(I),CAM(K,I),TAPP(K,I),
     2                     DEPI(K,I)
65        CONTINUE
70      CONTINUE
C
C       write out plant pesticide parameters
        WRITE(LECHO,2129) (LMODID,I=1,7)
        IF (FAM.GE.2) THEN
          IF (NCHEM .EQ. 1) THEN
            WRITE(LECHO,2131) LMODID,PLDKRT(1),LMODID,FEXTRC(1),
     1                       LMODID,PLVKRT(1)
          ELSE IF (NCHEM .EQ. 2) THEN
            WRITE(LECHO,2137) (LMODID,I=1,2),(PSTNAM(K),K=1,NCHEM),
     1                       (LMODID,I=1,2),(PLDKRT(K),K=1,NCHEM),
     2                       LMODID,(FEXTRC(K),K=1,NCHEM),LMODID,
     3                       (PLVKRT(K),K=1,NCHEM),LMODID,PTRN12,LMODID
          ELSE IF (NCHEM .EQ. 3) THEN
            WRITE(LECHO,2136) (LMODID,I=1,2),(PSTNAM(K),K=1,NCHEM),
     1                       (LMODID,I=1,2),(PLDKRT(K),K=1,NCHEM),
     2                       LMODID,(FEXTRC(K),K=1,NCHEM),LMODID,
     3                       (PLVKRT(K),K=1,NCHEM),LMODID,PTRN12,
     4                       LMODID,PTRN13,LMODID,PTRN23,LMODID
          ENDIF
        ENDIF
        IF (FAM.EQ.2) WRITE(LECHO,2132) LMODID,FILTRA
        DO 98 K=1,NCHEM
          IF (IPSCND(K) .EQ. 1) THEN
            WRITE(LECHO,2133) LMODID,K,LMODID,UPTKF(K)
          ELSE
            IF (IPSCND(K) .EQ. 2) THEN
              WRITE(LECHO,2134) LMODID,K,LMODID,UPTKF(K)
            ELSE
              IF (IPSCND(K) .EQ. 3) THEN
                WRITE(LECHO,2135) LMODID,K,LMODID,UPTKF(K)
              ENDIF
            ENDIF
          ENDIF
 98     CONTINUE
      ENDIF
C
C     write out soil profile information for pesticide transport
      WRITE(LECHO,2240) (LMODID,J=1,3),STITLE,(LMODID,J=1,2)
      WRITE(LECHO,2138)(LMODID,J=1,7),CORED,LMODID,NHORIZ,
     1                  LMODID,THFLAG,LMODID,KDFLAG,LMODID,BDFLAG
      WRITE(LECHO,21382) LMODID,
     2                  HSWZT,LMODID,MCFLAG,LMODID,IRFLAG,LMODID,ITFLAG,
     3                  LMODID,IDFLAG,LMODID,BIOFLG
C
C     echo biodegradation values in lines 14.a - 14.f   -jam
      IF (BIOFLG .EQ. 1) THEN
      WRITE(LECHO,21384)(LMODID,J=1,5),AM,AC,
     1                  AS,AR,LMODID,KE,LMODID,KSM,
     2                  KCM,KC,MKS,KR,
     3                  LMODID,KIN,LMODID,KSK,LMODID,KLDM,KLDC,KLDS,
     4                  KLDR,LMODID,KL1
      WRITE(LECHO,21387)LMODID,KL2,LMODID,
     5                  USM,UCM,MUC,US,UR,LMODID,YSM,
     7                  YCM,YC,YS,YR,LMODID
      WRITE(LECHO,21385)(LMODID,J=1,4)
      DO 855 I=1,NHORIZ
      WRITE(LECHO,21386) LMODID,HORIZN(I),Q(I),CM(I),Y(1,1,I),Y(2,1,I),
     1                   Y(3,1,I),Y(4,1,I)
855   CONTINUE
      ENDIF
C
C     irrigation data
      IF(IRFLAG .NE. 0)THEN
        WRITE(LECHO,2410) (LMODID,I=1,3)
        WRITE(LECHO,2420) LMODID,IRTYPE,LMODID,FLEACH,PCDEPL
        IF (IRTYPE.GT.2)THEN
          WRITE(LECHO,2430) LMODID,RATEAP,LMODID,UC
        ELSE IF(IRTYPE .EQ. 2)THEN
          WRITE(LECHO,2440) (LMODID,I=1,3),Q0,LMODID,BT,ZRS,
     1                    LMODID,SF,LMODID,EN,XL,LMODID,XFRAC
          WRITE(LECHO,2450) LMODID,KS,HF
        END IF
      END IF
C
      Select Case(ITFLAG)
      Case(1, 2)
        WRITE (LECHO,2520) (LMODID,I=1,3),(ALBEDO(I),I=1,12),
     &                     LMODID,EMMISS,
     &                     LMODID,uWind_Reference_Height,
     &                     (LMODID,I=1,2),(BBT(I),I=1,12),LMODID
2520  FORMAT (1X,A3,/,1X,A3,' MONTHLY VALUES OF SOIL SURFACE ALBEDO ',
     & '(JAN through DEC)',/,1X,A3,T14,12(F6.2),/,
     & 1X,A3,' SOIL EMMISSIVITY ',T60,G10.4,/,
     & 1X,A3,' HEIGHT ABOVE GROUND WHERE WIND SPEED MEASURED (M)',
     &      T60,G10.4,/,
     & 1X,A3,' BOTTOM BOUNDARY TEMPERATURE MONTHLY VALUE, JAN - DEC',
     &        /,1X,A3,T14,12(F6.2,1X),/,1X,A3)

        WRITE (LECHO,2540) LMODID,' Q10-FACTOR',(QFAC(K),K=1,NCHEM)
        WRITE (LECHO,2540) LMODID,' Q10 BASE TEMPERATURE',
     &                        (TBASE(K),K=1,NCHEM)
2540  FORMAT (1X,A3,a,T60,3G10.4)

      End Select

      Select Case(ITFLAG)
      Case(2)
        WRITE (LECHO,2560) LMODID,
     &         ' MOISTURE FLAG (1=ABSOLUTE MOISTURE, 2=RELATIVE TO FC',
     &         (MSFLG(K),K=1,NCHEM)
2560    FORMAT (1X,A3,a,T60,3I8)

        WRITE (LECHO,2540) LMODID,
     &         ' B-VALUE - EXPONENT OF MOISTURE CORRECTION',
     &         (MSEFF(K),K=1,NCHEM)

        WRITE (LECHO,2540) LMODID,
     &         ' REFERENCE SOIL MOISTURE',
     &         (MSLAB(K),K=1,NCHEM)

      End Select

      IF (.NOT.NITRON) THEN
        IF (NCHEM .EQ. 1) THEN
          WRITE(LECHO,2260) (LMODID,I=1,4),HENRYK(1),LMODID,
     *                       DAIR(1),LMODID
          IF (ITFLAG.EQ.1) WRITE(LECHO,2275) LMODID,ENPY(1),LMODID
        ELSE IF (NCHEM .EQ. 2) THEN
          WRITE(LECHO,2279)(LMODID,I=1,4),(PSTNAM(M),M=1,NCHEM),(LMODID,
     1       I=1,2),(HENRYK(M),M=1,NCHEM),LMODID,
     *       (DAIR(I),I=1,NCHEM),LMODID
          IF (ITFLAG.EQ.1) WRITE(LECHO,2274) LMODID,(ENPY(K),K=1,NCHEM),
     1                     LMODID
        ELSE IF (NCHEM .EQ. 3) THEN
          WRITE(LECHO,2280)(LMODID,I=1,4),(PSTNAM(M),M=1,NCHEM),(LMODID,
     1       I=1,2),(HENRYK(M),M=1,NCHEM),LMODID,
     *       (DAIR(I),I=1,NCHEM),LMODID
          IF (ITFLAG.EQ.1) WRITE(LECHO,2276) LMODID,(ENPY(K),K=1,NCHEM),
     1                     LMODID
        ENDIF
      END IF
C
      WRITE(LECHO,2140) (LMODID,I=1,5)
      IF (NCHEM .EQ. 1) THEN
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2155)(LMODID,I=1,8)
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2165)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2175)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2185)(LMODID,I=1,8)
      ELSE IF (NCHEM .EQ. 2) THEN
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2155)(LMODID,I=1,8)
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2165)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2175)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2185)(LMODID,I=1,8)
      ELSE IF (NCHEM .EQ. 3) THEN
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2155)(LMODID,I=1,8)
        IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2165)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.0)
     1                        WRITE(LECHO,2175)(LMODID,I=1,8)
        IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.1)
     1                        WRITE(LECHO,2185)(LMODID,I=1,8)
      ENDIF
C
      DO 80 I=1,NHORIZ
          IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.0 .AND. BDFLAG.EQ.0)
     1    WRITE(LECHO,2188) LMODID,HORIZN(I),THKNS(I),BD(I),THETO(I),
     2                     AD(I),ADL(I),THEFC(I),THEWP(I)
          IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.0 .AND. BDFLAG.EQ.1)
     1    WRITE(LECHO,2188) LMODID,HORIZN(I),THKNS(I),BD(I),THETO(I),
     2                     AD(I),ADL(I),THEFC(I),THEWP(I),OC(I)
          IF (THFLAG.EQ.0 .AND. KDFLAG.EQ.1)
     1    WRITE(LECHO,2188) LMODID,HORIZN(I),THKNS(I),BD(I),THETO(I),
     2                     AD(I),ADL(I),THEFC(I),THEWP(I),OC(I)
          IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.0)
     1    WRITE(LECHO,2188) LMODID,HORIZN(I),THKNS(I),BD(I),THETO(I),
     2                     AD(I),ADL(I),SAND(I),CLAY(I),OC(I)
          IF (THFLAG.EQ.1 .AND. KDFLAG.EQ.1)
     1    WRITE(LECHO,2188) LMODID,HORIZN(I),THKNS(I),BD(I),THETO(I),
     2                     AD(I),ADL(I),SAND(I),CLAY(I),OC(I)
80    CONTINUE
C
      IF (ITFLAG .EQ. 0) THEN
        WRITE(LECHO,2191) (LMODID,I=1,4)
      ELSE IF (THFLAG .EQ. 1 .AND. IDFLAG .EQ. 1) THEN
        WRITE(LECHO,2193) (LMODID,I=1,4)
      ELSE IF (IDFLAG .EQ. 0)THEN
        WRITE(LECHO,2201) (LMODID,I=1,4)
      ELSE
        WRITE(LECHO,2195) (LMODID,I=1,4)
      ENDIF
C
      DO 83 I = 1, NHORIZ
        IF (ITFLAG .EQ. 0) THEN
          WRITE (LECHO,2192) LMODID,I,DPN(I)
        ELSE IF (THFLAG .EQ. 1 .AND. IDFLAG .EQ. 1) THEN
          WRITE (LECHO,2194) LMODID,I,DPN(I),SPT(I)
        ELSE IF (IDFLAG .EQ. 0)THEN
          WRITE (LECHO,2202) LMODID,I,DPN(I),SPT(I),THCOND(I),
     1                          VHTCAP(I)
        ELSE
          WRITE (LECHO,2196) LMODID,I,DPN(I),SPT(I),
     1                        SAND(I),CLAY(I),OC(I)
        ENDIF
83    CONTINUE
C
      IF (NITRON) THEN
C       soil nitrogen information
        CALL NITECH (LECHO,LMODID,SEPTON)
      ELSE
C       pesticide decay terms
        IF(DK2FLG.EQ.0)THEN
          IF (NCHEM .EQ. 1) THEN
            WRITE(LECHO,2308) (LMODID,J=1,2),(PSTNAM(K),K=1,1)
            DO 82 I=1, NHORIZ
              WRITE(LECHO,2309) LMODID,LMODID,I,LMODID,LMODID
              WRITE(LECHO,2310) LMODID,(DDW(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2313) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2314) LMODID,(DISP(K,I),K=1,NCHEM)
82          CONTINUE
          ELSEIF (NCHEM .EQ. 2) THEN
            WRITE(LECHO,2308) (LMODID,J=1,2),(PSTNAM(K),K=1,2)
            DO 84 I=1, NHORIZ
              WRITE(LECHO,2309) LMODID,LMODID,I,LMODID,LMODID
              WRITE(LECHO,2310) LMODID,(DDW(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2313) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2314) LMODID,(DISP(K,I),K=1,NCHEM)
              WRITE(LECHO,2315) LMODID,DDKW12(I)
              WRITE(LECHO,2325) LMODID,DDKS12(I)
84          CONTINUE
          ELSEIF (NCHEM .EQ. 3) THEN
            WRITE(LECHO,2300) (LMODID,J=1,2),(PSTNAM(K),K=1,3)
            DO 85 I=1, NHORIZ
              WRITE(LECHO,2301) LMODID,LMODID,I,LMODID,LMODID
              WRITE(LECHO,2302) LMODID,(DDW(K,I),K=1,NCHEM)
              WRITE(LECHO,2303) LMODID,(DDS(K,I),K=1,NCHEM)
              WRITE(LECHO,2304) LMODID,(DDG(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2305) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2306) LMODID,(DISP(K,I),K=1,NCHEM)
              WRITE(LECHO,2307) LMODID,DDKW12(I),DDKW13(I),DDKW23(I)
              WRITE(LECHO,2327) LMODID,DDKS12(I),DDKS13(I),DDKS23(I)
85          CONTINUE
        ELSEIF(DK2FLG.EQ.1)THEN
          IF (NCHEM .EQ. 1) THEN
            WRITE(LECHO,2308) (LMODID,J=1,2),(PSTNAM(K),K=1,1)
            DO 182 I=1, NHORIZ
              WRITE(LECHO,2309) LMODID,LMODID,I,LMODID,LMODID
              WRITE(LECHO,2310) LMODID,(DDW1(K,I),K=1,NCHEM)
              WRITE(LECHO,2310) LMODID,(DDW2(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS1(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS2(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG1(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG2(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2313) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2314) LMODID,(DISP(K,I),K=1,NCHEM)
182          CONTINUE
          ELSEIF (NCHEM .EQ. 2) THEN
            WRITE(LECHO,2308) (LMODID,J=1,3),(PSTNAM(K),K=1,2)
            WRITE(LECHO,2320) LMODID,(DKDAY(K),K=1,2)
            WRITE(LECHO,2321) LMODID,(DKMNTH(K),K=1,2)
            WRITE(LECHO,2322) LMODID,(DKNUM(K),K=1,2),LMODID
            DO 184 I=1, NHORIZ
              WRITE(LECHO,2309) LMODID,I,LMODID,LMODID
              WRITE(LECHO,2310) LMODID,(DDW1(K,I),K=1,NCHEM)
              WRITE(LECHO,2310) LMODID,(DDW2(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS1(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS2(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG1(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG2(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2313) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2314) LMODID,(DISP(K,I),K=1,NCHEM)
              WRITE(LECHO,2315) LMODID,DDKW112(I)
              WRITE(LECHO,2315) LMODID,DDKW212(I)
              WRITE(LECHO,2325) LMODID,DDKS112(I)
              WRITE(LECHO,2325) LMODID,DDKS212(I)
184          CONTINUE
          ELSEIF (NCHEM .EQ. 3) THEN
            WRITE(LECHO,2300) (LMODID,J=1,3),(PSTNAM(K),K=1,3)
            WRITE(LECHO,2330) LMODID,(DKDAY(K),K=1,3)
            WRITE(LECHO,2331) LMODID,(DKMNTH(K),K=1,3)
            WRITE(LECHO,2332) LMODID,(DKNUM(K),K=1,3),LMODID
            DO 185 I=1, NHORIZ
              WRITE(LECHO,2301) LMODID,I,LMODID,LMODID
              WRITE(LECHO,2310) LMODID,(DDW1(K,I),K=1,NCHEM)
              WRITE(LECHO,2310) LMODID,(DDW2(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS1(K,I),K=1,NCHEM)
              WRITE(LECHO,2311) LMODID,(DDS2(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG1(K,I),K=1,NCHEM)
              WRITE(LECHO,2312) LMODID,(DDG2(K,I),K=1,NCHEM)
              IF (KDFLAG.EQ.0)WRITE(LECHO,2313) LMODID,
     *                              (KD(K,I),K=1,NCHEM)
              WRITE(LECHO,2306) LMODID,(DISP(K,I),K=1,NCHEM)
              WRITE(LECHO,2307) LMODID,DDKW112(I),DDKW113(I),DDKW123(I)
              WRITE(LECHO,2307) LMODID,DDKW212(I),DDKW213(I),DDKW223(I)
              WRITE(LECHO,2327) LMODID,DDKS112(I),DDKS113(I),DDKS123(I)
              WRITE(LECHO,2327) LMODID,DDKS212(I),DDKS213(I),DDKS223(I)
185          CONTINUE
          ENDIF
        ENDIF
      ENDIF
        IF (ILP.NE.0) THEN
          NLINES=INT(NCOM2/5+1.)
          IF (CFLAG.EQ.1) WRITE(LECHO,2250) (LMODID,I=1,5)
          IF (CFLAG.EQ.0) WRITE(LECHO,2251) (LMODID,I=1,5)
          DO 90 K=1,NCHEM
            DO 90 I=1,NLINES
              LL =(I-1)*5+1
              UL =LL+4
              IF (UL.GT.NCOM2) UL= NCOM2
              WRITE(LECHO,2200) LMODID,(J,PESTR(K,J),J=LL,UL)
90        CONTINUE
        ENDIF
      ENDIF
C
C     write out output flags
      IF (ITEM1.NE.BLNK .OR. ITEM2.NE.BLNK .OR. ITEM3.NE.BLNK)
     1  WRITE(LECHO,2205) (LMODID,I=1,7)
      IF (ITEM1.NE.BLNK) WRITE(LECHO,2210) (LMODID,I=1,2),ITEM1,
     1                                     STEP1,LFREQ1
      IF (ITEM2.NE.BLNK) WRITE(LECHO,2210) (LMODID,I=1,2),ITEM2,
     1                                     STEP2,LFREQ2
      IF (ITEM3.NE.BLNK) WRITE(LECHO,2210) (LMODID,I=1,2),ITEM3,
     1                                     STEP3,LFREQ3
      IF (NPLOTS.GT.0) THEN
        WRITE(LECHO,2220) (LMODID,I=1,7),NPLOTS,(LMODID,I=1,2)
        DO 140 I=1,NPLOTS
          IF (PLTYP(1) .EQ. 'P') THEN
            WRITE(LECHO,2230) LMODID,PLNAME(I),INDX(I),MODE(I),IARG(I),
     1                       IARG2(I),CONST(I),PLTYP(I)
          ELSE
            WRITE(LECHO,2230) LMODID,PLNAME(I),INDX(I),MODE(I),IARG(I),
     1                       IARG2(I),CONST(I),PLTYP(I),PLTDSN(I)
          ENDIF
140     CONTINUE
      ENDIF
C
C
      CALL SUBOUT
C
      RETURN
      END

