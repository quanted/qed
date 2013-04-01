C
C
C
      SUBROUTINE   LPWDO1
     I                   (WDMFL,MESSFL,SCLU,OT,DSN,LOGARH,
     I                     XBAR,STD,SKEW,NZI,NPARM,
     O                     ATRSAV,TCNT,RETCOD)
C     + + + PURPOSE + + +
C     This routine stores six computed statistics as attributes on
C     the WDM file for the Pearson and Log-Pearson Type III
C     distributions.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER    WDMFL, MESSFL, SCLU, OT, DSN, LOGARH, RETCOD,
     &           NZI, NPARM, TCNT
      REAL       XBAR, STD, SKEW
      CHARACTER*6 ATRSAV(6)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     WDMFL  - Fortran unit number of users WDM file
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number for AIDE subroutines
C     OT     - Fortran unit number for error messages
C     DSN    - WDM data set number for analysis
C     LOGARH - log transformation flag, 1-yes, 2-no
C     XBAR   - mean of annual series
C     STD    - standard deviation of annual series
C     SKEW   - skew coefficient of annual series
C     NZI    - number of years of zero events
C     NPARM  - number of non-zero years
C     ATRSAV - character array of attribute names added to
C              data set on users WDM file
C     TCNT   - count of attributes added to users WDM file
C     RETCOD - return code
C               0 - attributes put on WDM file successfully
C              -1 - problem adding attributes to wdm.
C                   see file opened on unit 99 for details
C                   (usually error.fil)
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     INDXR(3,2), INDEX(3), SGRP, RETC, CNTDSN,
     $            LEN4
      CHARACTER*1 DISTR(4,2)
      CHARACTER*6 ATNAMR(3,2), ATNAME(3)
C
C     + + + EXTERNALS + + +
      EXTERNAL   SVATR3, SVATI2, SVATC1
C
C     + + + DATA INITIALIZATIONS + + +
Ckmf                  mean    st dev     skew  (log/no log) transforms
      DATA ATNAMR / 'MEANND', 'SDND  ', 'SKWND ',
     $              'MEANVL', 'STDDEV', 'SKEWCF' /
      DATA INDXR  /     280,      281,      282,
     $                  14,       15,       16   /
C                     zero     non zero  distrib
      DATA ATNAME / 'NUMZRO', 'NONZRO', 'LDIST ' /
      DATA INDEX  /     287,      286,      326  /
      DATA DISTR  / 'L','P','3',' ',  'L','P',' ',' ' /
      DATA LEN4   / 4 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCOD = 0
      CNTDSN = 1
      TCNT   = 0
C     write mean, standard deviation, and skew to data set
      SGRP = 51
      IF (LOGARH .EQ. 2) SGRP = 52
      CALL SVATR3 ( MESSFL, SCLU, SGRP, WDMFL, OT,
     I              CNTDSN, DSN,
     I              INDXR(1,LOGARH), ATNAMR(1,LOGARH),
     I              XBAR, STD, SKEW,
     O              RETC )
      IF (RETC .EQ. 0) THEN
C       attributes successfully saved
        ATRSAV(1) = ATNAMR(1,LOGARH)
        ATRSAV(2) = ATNAMR(2,LOGARH)
        ATRSAV(3) = ATNAMR(3,LOGARH)
        TCNT = TCNT + 3
      ELSE
C       problem with attribute(s)
        RETCOD = -1
      END IF
C     write number of zero and number of non-zero events to data set
      SGRP = 53
      CALL SVATI2 ( MESSFL, SCLU, SGRP, WDMFL, OT,
     I              CNTDSN, DSN,
     I              INDEX, ATNAME, NZI, NPARM,
     O              RETC )
      IF (RETC .EQ. 0) THEN
        ATRSAV(TCNT+1) = ATNAME(1)
        ATRSAV(TCNT+2) = ATNAME(2)
        TCNT = TCNT + 2
      ELSE
C       problem with attribute(s)
        RETCOD = -1
      END IF
C     write distribution type to data set
      SGRP = 54
      CALL SVATC1 ( MESSFL, SCLU, SGRP, WDMFL, OT,
     I              CNTDSN, DSN,
     I              INDEX(3), ATNAME(3), DISTR(1,LOGARH), LEN4,
     O              RETC )
      IF (RETC .EQ. 0) THEN
        ATRSAV(TCNT+1) = ATNAME(3)
        TCNT = TCNT + 1
      ELSE
C       problem with attribute(s)
        RETCOD = -1
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LPWDO2
     I                   ( WDMFL, MESSFL, SCLU, OT, DSN, ILH, NMDAYS,
     I                     NZI, RI, QNEW, Q, SCNOUT,
     M                     TCNT, ATRSAV )
C
C     + + + PURPOSE + + +
C     This routine stores values of events for pre-selected recurrence
C     intervals as attributes on a WDM file for the Pearson and
C     Log-Pearson Type III distribution.
C
C     + + + HISTORY + + +
C     wrk 01/12/12  number of table entries increased from 11 to 12 for
C                   0.3333 recurrence interval.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   WDMFL, MESSFL, SCLU, OT, DSN,
     &          ILH, NMDAYS, NZI, TCNT, SCNOUT
      REAL      RI(13), QNEW(13), Q(13)
      CHARACTER*6 ATRSAV(19)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     WDMFL  - Fortran unit number of users WDM file
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number for AIDE subroutines
C     OT     - Fortran unit number for error messages
C     DSN    - WDM data set number for analysis
C     ILH    - flag for statistic
C              1 - n-day high flow
C              2 - n-day low flow
C              3 - month
C     NMDAYS - number of days for flow statistic
C     NZI    - number of years of zero events
C     RI     - recurrence interval
C     QNEW   - statistic adjusted for zero flow
C     Q      - statistics for each specified recurrence interval
C     SCNOUT - flag for screen output (1-no, 2-yes)
C     TCNT   - count of number of attributes placed on WDM file
C     ATRSAV - character array of attribute names added to
C              data set on users WDM file
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     RIINT, SAIND(11), SATYP, SALEN, SGRP, SCLUIO, RETC,
     $            JUSTR, I, K, N, L2, L3, L6, OLEN
      REAL        QTEMP(11)
      CHARACTER*1 SANAM(6,11), SANAMK(3), BLNK, Z0
C
C     + + + INTRINSICS
      INTRINSIC  INT
C
C     + + + EXTERNALS + + +
      EXTERNAL  INTCHR, CARVAR, WDBSGX, SVATRM
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   Z0, BLNK, JUSTR, L2, L3, L6
     $    / '0',  ' ',     0,  2,  3,  6 /
C
C     + + + END SPECIFICATIONS + + +
C
C     low or high flows
      IF (ILH .EQ. 2) THEN
C       low flow
        SANAMK(1) = 'L'
      ELSE
C      assume high flow
       SANAMK(1) = 'H'
      END IF
C     duration
      CALL INTCHR ( NMDAYS, L2, JUSTR, OLEN, SANAMK(2) )
      IF (SANAMK(2) .EQ. BLNK) SANAMK(2) = Z0
C
      N = 1
C     Dec 01 - increased from 11 to 12 to add .3333 recurrence interval
      DO 380 I = 1,12
C       build possible attribute name for each recurrence interval
        RIINT = INT(RI(I)+0.001)
        IF (RIINT .GE. 2) THEN
C         recurrence interval >= 2 years, may be an attribute
          SANAM(1,N) = SANAMK(1)
          SANAM(2,N) = SANAMK(2)
          SANAM(3,N) = SANAMK(3)
          CALL INTCHR ( RIINT, L3, JUSTR, OLEN, SANAM(4,N) )
          DO 375 K = 4, 6
C           replace blanks with zero
            IF(SANAM(K,N) .EQ. BLNK) SANAM(K,N) = Z0
 375      CONTINUE
C         find attribute index number for attribute sanam
C         sanam returns as all blanks if no match
          CALL WDBSGX ( MESSFL,
     M                  SANAM(1,N),
     O                  SAIND(N), SATYP, SALEN )
          IF (SAIND(N) .GT. 0) THEN
C           found index number
            IF (NZI .GT. 0) THEN
C             adjusted for zero flows
              QTEMP(N) = QNEW(I)
            ELSE
C             no adjustments
              QTEMP(N) = Q(I)
            END IF
            N = N + 1
          END IF
        END IF
 380  CONTINUE
      IF (N .GT. 1) THEN
C       found at least one recurrence interval attribute
        N = N - 1
        SGRP = 60
        IF (SCNOUT .EQ. 2) THEN
C         screen io
          SCLUIO = SCLU
        ELSE
C         no screen io
          SCLUIO = 0
        END IF
        CALL SVATRM ( MESSFL, SCLUIO, SGRP, WDMFL, OT, N, DSN,
     I                SAIND, SANAM, QTEMP,
     O                RETC )
        IF (RETC .EQ. 0) THEN
C         attributes successfully saved
          DO 400 I = 1, N
            TCNT = TCNT + 1
            CALL CARVAR ( L6, SANAM(1,I), L6, ATRSAV(TCNT) )
 400      CONTINUE
        END IF
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LPWDO3
     I                   ( WDMFL, MESSFL, SCLU, OT, DSN,
     I                     NZI, NQS, RI, QNEW, Q, SCNOUT,
     M                     TCNT, ATRSAV )
C
C     + + + PURPOSE + + +
C     This routine stores values of events for pre-selected recurrence
C     intervals as attributes on a WDM file for the Pearson and
C     Log-Pearson Type III distribution.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     WDMFL, MESSFL, SCLU, OT, DSN, NQS,
     $            NZI, TCNT, SCNOUT
      REAL        RI(13), QNEW(13), Q(13)
      CHARACTER*1 ATRSAV(19)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     WDMFL  - Fortran unit number of users WDM file
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number for AIDE subroutines
C     OT     - Fortran unit number for error messages
C     DSN    - WDM data set number for analysis
C     NMDAYS - number of days for flow statistic
C     NZI    - number of years of zero events
C     NQS    - number of quantiles
C     RI     - recurrence interval
C     QNEW   - statistic adjusted for zero flow
C     Q      - statistics for each specified recurrence interval
C     SCNOUT - flag for screen output (1-no, 2-yes)
C     TCNT   - count of number of attributes placed on WDM file
C     CBUF   - character string of attribute names added to
C              data set on users WDM file
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     IPCT, SAIND(13), SATYP, SALEN, SGRP, SCLUIO, RETC,
     $            JUSTR, I, K, N, L3, L6, OLEN
      REAL        QTEMP(13)
      CHARACTER*1 SANAM(6,13), BLNK, Z0
C
C     + + + INTRINSICS
      INTRINSIC  INT
C
C     + + + EXTERNALS + + +
      EXTERNAL  INTCHR, CARVAR, WDBSGX, SVATRM
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   Z0, BLNK, JUSTR, L3, L6
     $    / '0',  ' ',      0, 3,  6 /
C
C     + + + END SPECIFICATIONS + + +
C
      N = 1
      DO 380 I = 1,NQS
        SANAM(1,N) = 'L'
        SANAM(2,N) = 'Q'
        SANAM(3,N) = 'U'
        IPCT = INT(0.1 + 1000.0/RI(I))
        CALL INTCHR ( IPCT, L3, JUSTR, OLEN, SANAM(4,N) )
        DO 375 K = 4, 6
C         replace blanks with zero
          IF(SANAM(K,N) .EQ. BLNK) SANAM(K,N) = Z0
 375    CONTINUE
C       find attribute index number for attribute sanam
C       sanam returns as all blanks if no match
        CALL WDBSGX (MESSFL,
     M               SANAM(1,N),
     O               SAIND(N),SATYP,SALEN)
        IF (SAIND(N) .GT. 0) THEN
C         found index number
          IF (NZI .GT. 0) THEN
C           adjusted for zero flows
            QTEMP(N) = QNEW(I)
          ELSE
C           no adjustments
            QTEMP(N) = Q(I)
          END IF
          N = N + 1
        END IF
 380  CONTINUE
      IF (N .GT. 1) THEN
C       found at least one recurrence interval attribute
        N = N - 1
        SGRP = 60
        IF (SCNOUT .EQ. 2) THEN
C         screen io possible
          SCLUIO = SCLU
        ELSE
C         no screen io
          SCLUIO = 0
        END IF
        CALL SVATRM ( MESSFL, SCLUIO, SGRP, WDMFL, OT, N, DSN,
     I                SAIND, SANAM, QTEMP,
     O                RETC )
        IF (RETC .EQ. 0) THEN
C         attributes successfully saved
          DO 400 I = 1, N
            TCNT = TCNT + 1
            CALL CARVAR ( L6, SANAM(1,I), L6, ATRSAV(TCNT) )
 400      CONTINUE
        END IF
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   PRAOPT
     I                   (MESSFL,SCLU,WDMFL,DSNCNT,DSNBUF,IGR,
     M                    FLNAME,FPRT,IPLOT,WOUT,SCNOUT,CHGDAT,
     M                    NBYR,NEYR,LOGARH)
C
C     + + + PURPOSE + + +
C     Modify parameters for output and options for
C     A193 Log-Pearson Frequency analysis.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER      MESSFL,SCLU,WDMFL,DSNCNT,DSNBUF(DSNCNT),IGR,SCNOUT,
     &             FPRT,IPLOT,WOUT,CHGDAT,NBYR,NEYR,LOGARH
      CHARACTER*64 FLNAME
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number for message file
C     SCLU   - cluster number on message file
C     WDMFL  - Fortran unit number for WDM file
C     DSNCNT - number of data sets in buffer
C     DSNBUF - array of data-set numbers in buffer
C     IGR    - graphics available flag
C              1 - graphics available, 2 - graphics not available
C     FLNAME - output file name
C     FPRT   - Fortran unit number for output file
C     IPLOT  - generate frequency plot flag,
C              0 - dont generate, 1 - generate frequency plot
C     WOUT   - output stats to WDM file flag (1 - NO, 2 - YES)
C     SCNOUT - output stats to screen (1 - no,  2 - yes)
C              1 - dont output to WDM, 2 - output to WDM
C     CHGDAT - change data period flag
C              1 - use Full period for each data set
C              2 - use Common period for all data sets
C              3 - Specify period for each data set
C     NBYR   - beginning year for analysis
C     NEYR   - ending year for analysis
C     LOGARH - log transformation flag, 1-yes, 2-no
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     I, I0, I1, I64, I80, SGRP, INUM, CNUM, IRET, RETCOD,
     &            IVAL(2), CVAL(5), SDATE(6), EDATE(6), CIND, CLEN,
     &            IMIN(2), IMAX(2), IDEF(2), CORM, CBAS
      REAL        RVAL
      DOUBLE PRECISION DDUM
      CHARACTER*1  BUFF(80),             BLNK
C
C     + + + EXTERNALS + + +
      EXTERNAL    ZSTCMA, ZGTRET, QSCSET, QRESPM
      EXTERNAL                    ZIPC
      EXTERNAL    PRNTXT, WTDATE, STFLOP
      EXTERNAL    Q1INIT, Q1EDIT, QSTCTF, QSTCOB, QGTCTF, QGTCOB
C
C     + + + END SPECIFICATIONS + + +
C
      I0  = 0
      I1  = 1
      I64 = 64
      I80 = 80
      BLNK= ' '
C
C     allow previous command
      I= 4
      CALL ZSTCMA (I,I1)
C
 10   CONTINUE
C       output options screen
C     write (99,*) ' ****'
C     write (99,*) ' ****'
C     write (99,*) ' **** --> q1edit: flname = ', flname
        SGRP= 2
        CALL Q1INIT (MESSFL, SCLU, SGRP)
C       set default values
        CIND = 1
        CLEN = 64
        CALL QSTCTF (CIND, CLEN, FLNAME)
        CNUM = 5
        CBAS = 2
        CVAL(1) = IPLOT+ 1
        CVAL(2) = WOUT
        CVAL(3) = SCNOUT
        CVAL(4) = CHGDAT
        CVAL(5) = LOGARH
        CALL QSTCOB (CNUM, CBAS, CVAL)
C       allow user to edit screen
        CALL Q1EDIT (IRET)
        IF (IRET.EQ.1) THEN
C         user wants to continue
C         get values from screen
          CALL QGTCOB (CNUM, CBAS, CVAL)
          IPLOT = CVAL(1) - 1
          WOUT = CVAL(2)
          SCNOUT = CVAL(3)
          CHGDAT = CVAL(4)
          LOGARH = CVAL(5)
          CALL QGTCTF (CIND, CLEN, FLNAME)
C     write (99,*) ' **** --> stflop: flname = ', flname
          SGRP = 3
          CALL STFLOP ( MESSFL, SCLU, SGRP,
     M                  FPRT, FLNAME,
     O                  RETCOD )
C     write (99,*) ' **** <-- stflop: flname = ', flname
C     write (99,*) ' ****               fprt = ', fprt
C     write (99,*) ' ****             retcod = ', retcod
C     write (99,*) ' ****'
C     write (99,*) ' ****'
          IF (CHGDAT.EQ.2 .AND. IRET.EQ.1) THEN
C           user wants common period
            IF (DSNCNT.EQ.0) THEN
C             no data sets to determine common period for
              SGRP= 6
              CALL PRNTXT (MESSFL,SCLU,SGRP)
            ELSE
C             determine common period
              CORM = 1
              CALL WTDATE (WDMFL,DSNCNT,DSNBUF,CORM,
     O                     SDATE,EDATE,RETCOD)
              IF (RETCOD.EQ.0) THEN
C               common period found, modify as desired
                NBYR = SDATE(1)
                NEYR = EDATE(1)
 30             CONTINUE
C                 set default year bounds
                  INUM= 2
                  IMIN(1)= NBYR
                  IMAX(1)= NEYR
                  IDEF(1)= NBYR
                  IMIN(2)= NBYR
                  IMAX(2)= NEYR
                  IDEF(2)= NEYR
                  IVAL(1)= 0
                  IVAL(2)= 0
                  CALL QSCSET (INUM,I1,I1,I1,INUM,IMIN,IMAX,IDEF,
     I                         RVAL,RVAL,RVAL,DDUM,DDUM,DDUM,
     I                         IVAL,I1,I1,I1,BLNK)
C                 get starting and ending year
                  IVAL(1)= NBYR
                  IVAL(2)= NEYR
                  CALL ZIPC (I80,BLNK,BUFF)
                  SGRP = 5
                  CALL QRESPM (MESSFL,SCLU,SGRP,INUM,I1,I1,
     M                         IVAL,RVAL,CVAL,BUFF)
C                 get user exit command value
                  CALL ZGTRET (IRET)
                  IF (IRET.EQ.1) THEN
C                   user wants to continue
                    NBYR= IVAL(1)
                    NEYR= IVAL(2)
                    IF (NBYR.GE.NEYR) THEN
C                     start year must preceed end year
                      SGRP = 7
                      CALL PRNTXT (MESSFL,SCLU,SGRP)
                    END IF
                  END IF
                IF (NBYR.GE.NEYR) GO TO 30
              ELSE
C               no common period found, problem
                SGRP= 8
                CALL PRNTXT (MESSFL,SCLU,SGRP)
              END IF
            END IF
          END IF
        ELSE
C         user wants back to main Frequency menu
          IRET= 1
        END IF
      IF (IRET.EQ.2) GO TO 10
C
C     turn off previous command
      I= 4
      CALL ZSTCMA (I,I0)
C
      IF (IPLOT.EQ.1 .AND. IGR.EQ.2) THEN
C       user wants graphics, but it is not available
        SGRP= 26
        CALL PRNTXT (MESSFL,SCLU,SGRP)
        IPLOT= 0
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LPINPT
     I                   (MESSFL,SCLU,WDMFL,OT,
     I                    DSN,SCNOUT,CHGDAT,MXYRS,
     M                    NBYR,NEYR,
     O                    STATN,NMO,NSM,NSD,NEM,NED,
     O                    NPOS,NNEG,NMDAYS,NUMONS,NZI,
     O                    ILH,Y,RETCOD)
C
C     + + + PURPOSE + + +
C     This routine retrieves data for frequency analysis from a
C     WDM file.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL,SCLU,WDMFL,OT,DSN,CHGDAT,NBYR,NEYR,
     $            NMO,NSM,NSD,NEM,NED,MXYRS,SCNOUT,
     $            NPOS,NNEG,NMDAYS,NUMONS,NZI,ILH,RETCOD
      REAL        Y(MXYRS)
      CHARACTER*1 STATN(80)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number on message file
C     WDMFL  - Fortran unit number of users WDM file
C     OT     - Fortran unit number for error messages
C     DSN    - WDM dataset number for analysis
C     SCNOUT - flag for screen output (1-no, 2-yes)
C     CHGDAT - change data period flag
C              1 - use Full period for each data set
C              2 - use Common period for all data sets
C              3 - Specify period for each data set
C     NBYR   - begin year for analysis
C     NEYR   - end year for analysis
C     STATN  - station number and name, if they are available
C               1-16 - station number
C              17-64 - station name
C     STANAM - station name
C     STAID  - station number
C     NMO    - number of months in season or period
C     NSM    - start month of season
C     NEM    - end month of season
C     NPOS   - number of non-zero years
C     NNEG   - number of negative years
C     NMDAYS - number of days for flow statistic
C     NUMONS - number of months for statistic
C     NZI    - number of years of zero events
C     ILH    - flag for statistic
C              1 - n-day high flow
C              2 - n-day low flow
C              3 - month
C     Y      - array of n-day hi or lo flows
C     RETCOD - return code
C               -1 - problem and user wants to stop all analysis
C                0 - ok
C                1 - error, couldn't get all input, skip data set
C                2 - problem with tsstep/tcode, not annual, skip data set
C               -6 - no data present in data set, skip data set
C               -7 - too many years of data to analyze
C              -81 - data set does not exist
C              -82 - data set exists but is not time series
C              -85 - trying to write to a read-only data set
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      I,N,L1,L3,L4,L5,L80,IRET,
     1             SDATE(6),EDATE(6),SGRP,SCLUIO,
     2                  QFLG,DTRAN,TUNITS,TSSTEP,ITUNIT,ITSTEP,
     3                      LVAL(6),RETC,RETC1,RETC2,
     4             L2, ITMP(3), INDEX(4), DAY(12)
      REAL         TSFILL
      CHARACTER*1  TSTYPE(4), BLANK
      CHARACTER*6  ATNAME(4)
C
C     + + + FUNCTIONS + + +
      INTEGER     CHRINT
C
C     + + + EXTERNALS + + +
      EXTERNAL    CHRINT, CMPTIM, ZIPC
      EXTERNAL    WDBSGC, WDBSGI, WDTGET, DSINFO, SVATI4
      EXTERNAL    PRNTXT
C
C     + + + DATA INITIALIZATION + + +
      DATA  L1, L2, L3, L4, L5, L80, DTRAN, QFLG, BLANK
     #    /  1,  2,  3,  4,  5,  80,     0,   30,  ' '  /
      DATA  ATNAME  /  'SEASBG', 'SEADBG', 'SEASND', 'SEADND' /
      DATA  INDEX   /      256,      446,      257,      447  /
      DATA  DAY   / 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 /
C
C     + + + END SPECIFICATIONS + + +
C
      TUNITS= 6
      TSSTEP= 1
      NPOS  = 0
      NNEG  = 0
      NZI   = 0
C
C     get statin id and name
      CALL ZIPC ( L80, BLANK, STATN )
      CALL DSINFO ( WDMFL, DSN, L80, STATN )
C
C     get tstype
      CALL WDBSGC ( WDMFL, DSN, L1, L4, TSTYPE, RETCOD )
      IF (RETCOD .NE. 0) CALL ZIPC ( L4, BLANK, TSTYPE )
C
C     get period of record and tsstep & tcode
C     (returns 1 day if attributes are missing from dsn)
      CALL WDGTTM ( WDMFL, DSN,
     O              SDATE, EDATE, ITSTEP, ITUNIT, TSFILL, RETCOD )
      IF (RETCOD .EQ. 0) THEN
        IF (EDATE(1)-SDATE(1) .GT. 3) THEN
C         check for annual time step
          CALL CMPTIM ( ITUNIT, ITSTEP, TUNITS, TSSTEP,
     O                  RETC1, RETC2 )
          IF (RETC2 .NE. 0) THEN
C           not an annual time step
            RETCOD = 2
          END IF
        ELSE
C         not enough data
          RETCOD = 1
          SGRP = 29
          CALL PRNTXT ( MESSFL, SCLU, SGRP )
        END IF
      END IF
C
      IF (RETCOD .EQ. 0) THEN
C       dates look ok so far
        IF (CHGDAT .EQ. 1) THEN
C         use full period of record for each dsn
          NBYR = SDATE(1)
          NEYR = EDATE(1)
        ELSE IF (CHGDAT .EQ. 2) THEN
C         use common period for all dsn,
C         nbyr & neyr are input
        ELSE IF (CHGDAT .EQ. 3) THEN
C         user specifying period of analysis for each dsn
          CALL LPDATE ( MESSFL, SCLU, DSN,
     I                  SDATE(1), EDATE(1),
     O                  NBYR, NEYR, RETCOD )
        ELSE
C         chgdat should be 1, 2, or 3, force to 1 (full)
          NBYR = SDATE(1)
          NEYR = EDATE(1)
        END IF
        N = NEYR - NBYR + 1
        IF (N .GT. MXYRS) THEN
C         too many years
          RETCOD = -7
        END IF
      END IF
C
      IF (RETCOD.EQ.0) THEN
C       continue, get annual time series
        SDATE(1) = NBYR
        EDATE(1) = NEYR
        CALL WDTGET (WDMFL,DSN,TSSTEP,SDATE,N,DTRAN,QFLG,TUNITS,
     O               Y,RETCOD)
        IF (RETCOD .EQ. 0) THEN
C         get number of good years and non-zero years
          DO 20 I = 1,N
            IF (Y(I) .GE. 1.0E-9) THEN
              NPOS = NPOS + 1
              Y(NPOS) = Y(I)
            ELSE IF (Y(I) .GT. -1.0E-9) THEN
C             zero defined as between -1.0E-9 and 1.0E-9
              NZI = NZI + 1
            ELSE
C             negative values ignored
              NNEG = NNEG + 1
            END IF
 20       CONTINUE
        END IF
      END IF
C
      IF (RETCOD .EQ. 0) THEN
C       get statistic type and duration
        NUMONS = 0
        NMDAYS = 0
        IF (TSTYPE(1) .EQ. 'H') THEN
C         high flow
          ILH = 1
          NMDAYS = CHRINT(L3,TSTYPE(2))
        ELSE IF (TSTYPE(1) .EQ. 'L') THEN
C         low flow
          ILH = 2
          NMDAYS = CHRINT(L3,TSTYPE(2))
        ELSE IF (TSTYPE(1) .EQ. 'P'  .AND.
     $           TSTYPE(2) .EQ. 'E'  .AND.
     $           TSTYPE(3) .EQ. 'A'  .AND.
     $           TSTYPE(4) .EQ. 'K') THEN
C         annual peak, assume 1-day high (added 11/15 - kmf)
          ILH = 1
          NMDAYS = 1
        ELSE IF (TSTYPE(1) .EQ. 'M') THEN
C         monthly statistics
          ILH = 3
          NUMONS = CHRINT (L2,TSTYPE(3))
        ELSE
C         tstype does not contain expected information
C                statistic: 1-high,2-low
C                duration
 30       CONTINUE
            SGRP = 10
            ITMP(1) = -999
            ITMP(2) = DSN
            ITMP(3) = 1
            I = 2
            CALL Q1INIT ( MESSFL, SCLU, SGRP )
            CALL QSETI  ( I, ITMP )
            I = 1
            CALL QSETCO ( I, ITMP(3) )
            CALL Q1EDIT ( IRET )
          IF (IRET .EQ. -1) GO TO 30
C         assume Accept (iret=1), get duration and low/high
          CALL QGETI  ( I, NMDAYS )
          CALL QGETCO ( I, ILH )
        END IF
C
C       Get beg and end month of season
        CALL WDBSGI (WDMFL,DSN,INDEX(1),L1, NSM,RETC)
        IF (RETC .NE. 0) NSM = -999
        CALL WDBSGI (WDMFL,DSN,INDEX(2),L1, NSD,RETC)
        IF (RETC .NE. 0) NSD = -999
        CALL WDBSGI (WDMFL,DSN,INDEX(3),L1, NEM,RETC)
        IF (RETC .NE. 0) NEM = -999
        CALL WDBSGI (WDMFL,DSN,INDEX(4),L1, NED,RETC)
        IF (RETC .NE. 0) NED = -999
        IF (TSTYPE(1) .NE. 'M') THEN
C         expect high or low
          IF (NSM .LE. 0  .OR.  NEM .LE. 0) THEN
C           attributes seasnd and seasbg missing, get values
C           add to wdm? lval(4): 1-yes, 2-no
 40         CONTINUE
C             seasbg, seasnd, add to wdm: 1-yes, 2-no
              LVAL(1) = NSM
              LVAL(2) = NEM
              LVAL(3) = 2
C             seadbg, seadnd, dsn
              LVAL(4) = NSD
              LVAL(5) = NED
              LVAL(6) = DSN
              SGRP = 31
              CALL Q1INIT ( MESSFL, SCLU, SGRP )
              CALL QSETI  ( L3, LVAL(4) )
              CALL QSETCO ( L3, LVAL(1) )
              CALL Q1EDIT ( IRET )
            IF (IRET .EQ. -1) GO TO 40
C           assume Accept (iret=1)
            CALL QGETI ( L2, LVAL(4) )
            CALL QGETCO ( L3, LVAL(1) )
            NSM = LVAL(1)
            NSD = LVAL(4)
            NEM = LVAL(2)
            NED = LVAL(5)
            IF (LVAL(3) .EQ. 1) THEN
C             add missing seasbg, seadbg, seasnd and seadnd  to dsn
              IF (SCNOUT .EQ. 2) THEN
C               screen io possible
                SCLUIO = SCLU
              ELSE
C               no screen io
                SCLUIO = 0
              END IF
              SGRP = 55
              CALL SVATI4 ( MESSFL, SCLUIO, SGRP, WDMFL, OT, L1, DSN,
     I                      INDEX, ATNAME, NSM, NEM, NSD, NED,
     O                      RETC )
            END IF
          ELSE IF (NSD .LE. 0  .OR.  NED .LE. 0) THEN
C           assume full months, don't save to wdm
            IF (NSD .LE. 0) NSD = 1
            IF (NED .LE. 0) NED = DAY(NEM)
          END IF
        END IF
C
        IF (TSTYPE(1) .EQ. 'M') THEN
C         special case of monthly statistic
          NEM = NSM + NUMONS - 1
          IF (NEM .GT. 12) NEM = NEM - 12
          NMO = NUMONS
        ELSE
C         compute length of season in months for other cases
          NMO = NEM
          IF (NEM .GE. NSM) THEN
            NMO = NMO + 1 - NSM
          ELSE
            NMO = NMO + 13 - NSM
          END IF
        END IF
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LPDATE
     I                   ( MESSFL, SCLU, DSN,
     I                     SDATE, EDATE, 
     O                     NBYR, NEYR, RETCOD )
C
C     + + + PURPOSE + + +
C     Get time period for analysis.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   MESSFL, SCLU, DSN, SDATE, EDATE,
     $          NBYR, NEYR, RETCOD
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number for AIDE subroutines
C     DSN    - WDM data set number for analysis
C     SDATE  - year available date starts
C     EDATE  - year available data ends
C     NBYR   - year to begin analyzing data
C     NEYR   - year to end analyzing data
C     RETCOD - return code
C               0 - valid dates specified
C               1 - problem selecting dates, skip this data set
C              -1 - problem selecting dates, abandon this and
C                   remaining data sets.
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   SGRP, SGRPT, I1, I5, PREV, INTR, OFF, ITMP(5),
     $          IRET, AGAIN
C
C     + + + EXTERNALS + + +
      EXTERNAL  Q1INIT, QSETI, QSETCO, Q1EDIT, QGETI, QGETCO
      EXTERNAL  ZSTCMA
C
C     + + + DATA INITIALIZATION + + +
      DATA     I1, I5, PREV, INTR, OFF
     $      /   1,  5,    4,    6,   0 /
C
C     + + + END SPECIFICATIONS + + +
C
C     make sure Prev and Intrpt are off
      CALL ZSTCMA ( PREV, OFF )
      CALL ZSTCMA ( INTR, OFF )
C
 100  CONTINUE
C       save default start and end years for data set
        ITMP(1) = SDATE
        ITMP(2) = EDATE
        ITMP(3) = DSN
        ITMP(4) = SDATE
        ITMP(5) = EDATE
        SGRP = 9
        CALL Q1INIT ( MESSFL, SCLU, SGRP )
        CALL QSETI ( I5, ITMP )
        CALL Q1EDIT ( IRET )
        IF (IRET .EQ. -1) THEN
C         Oops, start again
          Again = 1
        ELSE
C         assume Accept (iret=1), get period of analysis
          CALL QGETI ( I5, ITMP )
          NBYR= ITMP(1)
          NEYR= ITMP(2)
          AGAIN = 0
          IF (NBYR .LT. SDATE  .OR.  NEYR .GT. EDATE) THEN
C           requested date before/after actual start/end date
            SGRPT = 27
            AGAIN = 1
          ELSE IF (NEYR .LT. NBYR+3) THEN
C           requested period of analysis too short
            SGRPT = 28
            AGAIN = 1
          END IF
          IF (AGAIN .EQ. 1) THEN
C           problem with dates, 1-Reenter, 2-Skip, 3-Abandon
 200        CONTINUE
              ITMP(1) = SDATE
              ITMP(2) = EDATE
              ITMP(3) = DSN
              ITMP(4) = NBYR
              ITMP(5) = NEYR
              SGRP = SGRPT
              CALL Q1INIT ( MESSFL, SCLU, SGRP )
              CALL QSETI ( I5, ITMP )
              CALL QSETCO ( I1, AGAIN )
              CALL Q1EDIT ( IRET )
            IF (IRET .EQ. -1) GO TO 200
C           assume Accept (iret=1)
            CALL QGETCO ( I1, AGAIN )
          END IF
        END IF
      IF (AGAIN .EQ. 1) GO TO 100
C
C     assume continue processing
      RETCOD = 0
      IF (AGAIN .EQ. 2) THEN
C       Skip processing this station
        RETCOD = 1
      ELSE IF (AGAIN .EQ. 3) THEN
C       Abandon processing this and remaining data sets
        RETCOD = -1
      END IF
C
      RETURN
      END
