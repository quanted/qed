C
C
C
      SUBROUTINE   PRA193
     I                    ( MESSFL, WDMFL, IGR, APNAM,
     M                      DSNCNT, DSNBMX, DSNBUF )
C
C     + + + PURPOSE + + +
C     Fit a log Pearson Type III distribution to one or more
C     sets of input data.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   MESSFL, WDMFL, IGR, DSNCNT, DSNBMX, DSNBUF(DSNBMX)
      CHARACTER*11  APNAM
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number for main message file
C     WDMFL  - Fortran unit number for users WDM file
C     IGR    - graphics available flag
C              1 - graphics available
C              2 - graphics not available
C     APNAM  - program name and version
C     DSNCNT - number of data sets in the buffer
C     DSNBMX - maximum size of data set buffer
C     DSNBUF - array of data set numbers to be processed
C
C     + + + LOCAL VARIABLES + + +
      INTEGER         I1, SCLU, SGRP, RESP, SCNOUT, IWAIT,
     $             FPRT, IPLOT, CHGDAT, NBYR, NEYR, LOGARH,
     $             ICNT, DELFG, WOUT,         WSID, ICLOS, RETCOD
     $           , IND, DEVTYP, DEVCOD
      CHARACTER*8  PTHNAM, LPTHNM(1)
      CHARACTER*64 FLNAME
C
C     + + + LOCAL DEFINITIONS + + +
C     CHGDAT - change data period flag
C              1 - use Full period for each data set
C              2 - use Common period for all data sets
C              3 - Specify period for each data set
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C     SCNOUT - option flag for displaying statistics on screen
C              1 - do not display on screen
C              2 - display statistics on screen
C     WOUT   - option flag for saving statistics to wdm file
C              1 - do not output to wdm
C              2 - save statistics to wdm file
C
C     + + + EXTERNALS + + +
      EXTERNAL     PRAOPT, LGPFIT, PRWMSE
      EXTERNAL     QRESP,  PRNTXT, ZWNSOP, QFCLOS
      EXTERNAL     PDNPLT, GETFUN
      EXTERNAL     GPINIT
      EXTERNAL     ANPRGT, GPDEVC
C
      DATA  SCLU, CHGDAT, LOGARH, SCNOUT, WOUT, I1
     $     / 153,      1,      1,      1,    2,  1 /
C
C     + + + END SPECIFICATIONS + + +
C
C     initialize output parameters
      FLNAME = 'frqncy.out'
      FPRT   = 0
      IF (IGR.EQ.1) THEN
C       init to output graphics
        IPLOT  = 1
      ELSE
C       graphics not available
        IPLOT= 0
      END IF
C
      RESP = 1
 10   CONTINUE
C       resp: 1-Select, 2-Options, 3-Analyze, 4-Return
        LPTHNM(1) = 'S'
        CALL ZWNSOP (I1,LPTHNM)
        SGRP= 1
        CALL QRESP (MESSFL,SCLU,SGRP,RESP)
        IF (RESP .EQ. 1) THEN
C         select datasets
          PTHNAM = 'SF      '
          CALL PRWMSE (MESSFL,WDMFL,DSNBMX, PTHNAM,
     M                 DSNBUF,DSNCNT)
          RESP = 2
        ELSE IF (RESP .EQ. 2) THEN
C         modify output options
          CALL PRAOPT (MESSFL,SCLU,WDMFL,DSNCNT,DSNBUF,IGR,
     M                 FLNAME,FPRT,IPLOT,WOUT,SCNOUT,CHGDAT,
     M                 NBYR,NEYR,LOGARH)
          RESP = 3
        ELSE IF (RESP .EQ. 3  .AND.  DSNCNT .GT. 0) THEN
C         perform analysis
          IF (FPRT .EQ. 0) THEN
C           no output file open, open default
            CALL GETFUN ( I1, FPRT )
            FLNAME = 'frqncy.out'
            OPEN ( UNIT=FPRT, FILE=FLNAME, STATUS='UNKNOWN' )
          END IF
          ICNT= 0
          CALL GPINIT
Ckmf      set default device to screen, Dec 06 2000
          DEVTYP = 1
          IND = 39 + DEVTYP
          CALL ANPRGT (IND, DEVCOD)
          CALL GPDEVC (DEVTYP, DEVCOD)
Ckmf      end set default device, kmf, Dec 06 2000
C
 310      CONTINUE
C           begin loop for each station
            ICNT = ICNT + 1
            CALL LGPFIT ( MESSFL, SCLU, WDMFL, FPRT, DSNBUF(ICNT),
     I                    APNAM,
     I                    SCNOUT, WOUT, IPLOT, LOGARH, CHGDAT,
     M                    NBYR, NEYR, RETCOD )
          IF (ICNT .LT. DSNCNT) GO TO 310
C         close workstations
          WSID  = 1
          ICLOS = 1
          IWAIT = 0
          CALL PDNPLT (WSID,ICLOS,IWAIT)
          RESP = 1
        ELSE IF (RESP .EQ. 3  .AND.  DSNCNT .LE. 0) THEN
C         no data sets to work with
          SGRP= 18
          CALL PRNTXT (MESSFL,SCLU,SGRP)
          RESP = 1
        END IF
      IF (RESP.NE.4) GO TO 10
C
      DELFG = 0
      CALL QFCLOS (FPRT, DELFG)
C
      RETURN
      END
C
C
C
      SUBROUTINE   LGPFIT
     I                   ( MESSFL, SCLU, WDMFL, FPRT, DSN, APNAM,
     I                     SCNOUT, WOUT, IPLOT, LOGARH, CHGDAT,
     M                     NBYR, NEYR, RETCOD )
C
C     + + + PURPOSE + + +
C     Manages the steps in a log pearson fit of annual data.
C     Calls LPINPT to read data from a wdm file, calls LGPST1 to
C     compute general statistics (mean, standard deviation, skew,
C     etc.), LGPST2 to fit curve and compute probability, and
C     LGPPLT to plot the curves.
C
C     + + + HISTORY + + +
C     wrk 01/12/12  # of rows in n-day tables increased from 11 to 12
C                   to include the .3333 recurrence interval.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER      MESSFL, SCLU, WDMFL, FPRT, DSN,
     $             SCNOUT, WOUT, IPLOT, LOGARH, CHGDAT,
     $             NBYR, NEYR, RETCOD
      CHARACTER*11  APNAM
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster in message file
C     WDMFL  - Fortran unit number of wdm file
C     FPRT   - Fortran unit number for printing
C     DSN    - Data-set to be analyzed
C     APNAM  - program name and version
C     SCNOUT - option flag for displaying statistics on screen
C              1 - do not display on screen
C              2 - display statistics on screen
C     WOUT   - option flag for saving statistics to wdm file
C              1 - do not output to wdm 
C              2 - save statistics to wdm file
C     IPLOT  - option flag for plotting
C              1 - generate frequency plot
C              0 - do not generate frequency plot
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C     CHGDAT - change data period flag
C              1 - use Full period for each data set
C              2 - use Common period for all data sets
C              3 - Specify period for each data set
C     NBYR   - beginning year for analysis
C     NEYR   - ending year for analysis
C     RETCOD - return code
C
C     + + + PARAMETERS + + +
      INCLUDE 'pa193.inc'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      I, I1, ILH, IRET, LEN, NEM, NSM, NMDAYS,
     $             NMO, NPOS, NNEG, NQS, NUMONS, NZI, TCNT,
     $             SGRP, DEVTYP,          NSD, NED, MXYR
      REAL         CVR, SCC, SESKEW, SKEW, STD, VAR, XBAR,
     $             ADP(13), P(13), Q(13), QNEW(13), RI(13),
     $             C(27), CCPA(27), SE(27), RSOUT(22),
     $             Y(MXYRS), X(MXYRS)
      CHARACTER*1  STATN(80)
      CHARACTER*6  ATRSAV(19)
      CHARACTER*9  MONTH(12)
C
C     + + + LOCAL DEFINITIONS + + +
C     NMDAYS - number of days for flow statistic
C     ILH    - flag for statistics option
C              1 - high
C              2 - low
C              3 - month
C     NSM    - start month of season
C     NSD    - start day of season
C     NEM    - end month of season
C     NED    - end day of season
C     NMO    - number of months in season or period
C     NZI    - number of years of zero events
C     NPOS   - number of non-zero years
C     NNEG   - number of negative years, assumed missing and ignored
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C
C     + + + EXTERNALS + + +
      EXTERNAL   LPINPT, LGPST1, LGPST2, LGPPLT
      EXTERNAL   LPWDO1, LPWDO2, LPWDO3
      EXTERNAL   Q1INIT, QSETR,  Q1EDIT, PMXTXI
C
C     + + + DATA INITIALIZATIONS + + +
      DATA  MONTH / '  January', ' February', '    March', '    April',
     $              '      May', '     June', '     July', '   August',
     $              'September', '  October', ' November', ' December' /
C
C     + + + OUTPUT FORMATS + + +
 2001 FORMAT ( /,
     $  /,'                Log-Pearson Type III Statistics',
     $  /,'                           ', A,
     $  /,'                  (based on USGS Program A193)',
     $ //,'  Notice -- Use of Log-Pearson Type III or Pearson-Type III',
     $  /,'            distributions are for preliminary computations.',
     $  /,'            User is responsible for assessment and ',
     $  /,'            interpretation.')
 2003 FORMAT ( /,
     $  /,'                  Pearson Type III Statistics',
     $  /,'                           ', A,
     $  /,'                  (based on USGS Program A193)',
     $ //,'  Notice -- Use of Pearson Type III distribution is for',
     $  /,'            preliminary computations.  User is responsible',
     $  /,'            for assessment and interpretation.')
 2010 FORMAT (//, 15X, 64A1 )
 2031 FORMAT (    15X, A9, 1X, I2,      ' - start of season',
     $         /, 15X, A9, 1X, I2,      ' - end of season',
     $         /, 15X, I5,' -',I5,      ' - time period' )
 2033 FORMAT (    15X, 8X, I4,          ' - number of months',
     $         /, 15X, 3X, A9,          ' - starting month',
     $         /, 15X, I6,' -',I5,      ' - time period' )
 2041 FORMAT (    15X, I3, '-day high', ' - parameter' )
 2042 FORMAT (    15X, I4, '-day low',  ' - parameter' )
 2043 FORMAT (    15X, I6, '-month',    ' - parameter' )
 2050 FORMAT (    15X, 9X, I3,          ' - non-zero values',
     $         /, 15X, 9X, I3,          ' - zero values',
     $         /, 15X, 9X, I3,          ' - negative values (ignored)',
     $        //, ( 5X, 5F12.3 ) )
 2101 FORMAT (//,'  The following 7 statistics are based on non-zero',
     $           ' values:',
     $        //,'  Mean                             ', F14.3,
     $         /,'  Variance                         ', F14.3,
     $         /,'  Standard Deviation               ', F14.3,
     $         /,'  Skewness                         ', F14.3,
     $         /,'  Standard Error of Skewness       ', F14.3,
     $         /,'  Serial Correlation Coefficient   ', F14.3,
     $         /,'  Coefficient of Variation         ', F14.3 )
 2102 FORMAT (//,'  The following 7 statistics are based on non-zero',
     $           ' values:',
     $        //,'  Mean (logs)                             ', F10.3,
     $         /,'  Variance (logs)                         ', F10.3,
     $         /,'  Standard Deviation (logs)               ', F10.3,
     $         /,'  Skewness (logs)                         ', F10.3,
     $         /,'  Standard Error of Skewness (logs)       ', F10.3,
     $         /,'  Serial Correlation Coefficient (logs)   ', F10.3,
     $         /,'  Coefficient of Variation (logs)         ', F10.3 )

 2211 FORMAT ( /,
     $  /,'        Exceedance        Recurrence        Parameter',
     $  /,'        Probability        Interval           Value  ',
     $  /,'        -----------       ----------        ---------' )
 2212 FORMAT ( /,
     $  /,'       Non-exceedance     Recurrence        Parameter',
     $  /,'        Probability        Interval           Value  ',
     $  /,'        -----------       ----------        ---------' )
 2213 FORMAT ( /,
     $  /,'       Non-exceedance      Parameter',
     $  /,'        Probability          Value  ',
     $  /,'        -----------        ---------' )
 2221 FORMAT ( 7X, F12.4, 5X, F12.2, 5X, F12.3 )
 2223 FORMAT ( 7X, F12.4, 5X, F12.3 )
 2231 FORMAT ( /,
     $/,'                                         Adjusted   Adjusted ',
     $/,'   Exceedance  Recurrence   Parameter   Exceedance  Parameter',
     $/,'  Probability   Interval      Value    Probability    Value  ',
     $/,'  -----------  -----------  ---------  -----------  ---------')
 2232 FORMAT ( /,
     $/,'      Non-                            Adjusted Non- Adjusted ',
     $/,'   Exceedance   Recurrence  Parameter   Exceedance  Parameter',
     $/,'  Probability    Interval     Value    Probability    Value  ',
     $/,'  -----------  -----------  ---------  -----------  ---------')
 2233 FORMAT ( /,
     $/,'       Non-                Adjusted Non- Adjusted ',
     $/,'    Exceedance   Parameter   Exceedance  Parameter',
     $/,'   Probability     Value    Probability    Value  ',
     $/,'   -----------   ---------  -----------  ---------' )
 2241 FORMAT ( 1X, F12.4, 1X, F12.2, F11.3, 1X, F12.4, F11.3 )
 2243 FORMAT ( 2X, F12.4, 1X, F11.3, 1X, F12.4, F11.3 )
 2250 FORMAT ( /,
     $  /,'  Note -- Adjusted parameter values include zero values',
     $  /,'          and correspond with non-exceedance probabilities',
     $  /,'          in column 1 and recurrence interval in column 2.',
     $  /,'          Parameter values in column 3 are based on',
     $  /,'          non-zero values.' )
 2260 FORMAT (//, I5, ' statistics were added as attributes to',
     $           ' data set', I6, ':',
     $        //, ( 9X, 6 ( 1X, A6 ) ) )
 2905 FORMAT ( /,' ***',
     $         /,' *** Not enough data values, must be at least 3.',
     $         /,' ***' )
 2907 FORMAT ( /,' ***',
     $         /,' *** Too many years to process',
     $         /,' ***         max years =', I5,
     $         /,' ***        begin year =', I5,
     $         /,' ***          end year =', I5,
     $         /,' ***' )
 2921 FORMAT ( /,' ***',
     $         /,' *** Datum too large or small to process.',
     $         /,' ***' )
 2922 FORMAT ( /,' ***',
     $         /,' *** Mean or variance is negative or zero',
     $         /,' ***             mean = ', F12.5,
     $         /,' ***         variance = ', F12.5,
     $         /,' ***' )
 2931 FORMAT ( /,' ***',
     $         /,' *** Absolute value of skew is greater than 3.3',
     $         /,' ***             skew = ', F12.5,
     $         /,' ***' )
 2932 FORMAT ( /,' ***',
     $         /,' *** Error occurred in interpolation routine.',
     $         /,' ***' )
 2999 FORMAT ( /,' ***',
     $         /,' *** No further processing for this data set.',
     $         /,' ***' )
C
C     + + + END SPECIFICATIONS + + +
C
      DEVTYP = 1
      I1     = 1
C     get data
      MXYR = MXYRS
      CALL LPINPT ( MESSFL, SCLU, WDMFL, FPRT,
     I              DSN, SCNOUT, CHGDAT, MXYR,
     M              NBYR, NEYR,
     O              STATN, NMO, NSM, NSD, NEM, NED, NPOS, NNEG,
     O              NMDAYS, NUMONS, NZI, ILH, Y, RETCOD )
      IF (RETCOD .EQ. 0) THEN
        IF (ILH .EQ. 3) THEN
C         monthly statistics
          NQS = 12
        ELSE
C         n-day statistics
          NQS = 11
        END IF
C  
C       write header and input data
        IF (LOGARH .EQ. 1) THEN
          WRITE (FPRT,2001) APNAM
        ELSE
          WRITE(FPRT,2003) APNAM
        END IF
        WRITE (FPRT,2010) (STATN(I), I = 1, 64)
        IF (ILH .LE. 2) THEN
C         n-day flow statistics
          WRITE (FPRT,2031) MONTH(NSM), NSD, MONTH(NEM), NED, NBYR, NEYR
          IF (ILH .EQ. 1) THEN
C           high flow
            WRITE (FPRT,2041) NMDAYS
          ELSE
C           low flow
            WRITE (FPRT,2042) NMDAYS
          END IF
        ELSE
C         monthly statistics
          WRITE (FPRT,2033) NMO, MONTH(NSM), NBYR, NEYR
          WRITE (FPRT,2043) NUMONS
        END IF
        WRITE (FPRT,2050) NPOS, NZI,  NNEG, ( Y(I), I = 1, NPOS )
C
        IF (NPOS .LT. 3) THEN
C         not get enough data for dataset &. Skipping analysis.
          SGRP = 12
          CALL PMXTXI(MESSFL,SCLU,SGRP,I1,I1,I1,I1,DSN)
          RETCOD = -5
        ELSE
C         enough data, continue analysis
          IF (SCNOUT .EQ. 2) THEN
C           show data set being analyzed
            SGRP= 13
            CALL PMXTXI(MESSFL,SCLU,SGRP,I1,I1,I1,I1, DSN)
          ELSE
C           processing data set (print and go)
            SGRP = 34
            CALL PMXTXI(MESSFL,SCLU,SGRP,I1,I1,I1,I1, DSN)
          END IF
        END IF
      END IF
C
      IF (RETCOD .EQ. 0) THEN
C       still ok, comupute statistics
        CALL LGPST1 ( FPRT, Y, LOGARH, NPOS,
     O                XBAR, VAR, STD, SKEW, SESKEW, SCC, CVR, X,
     O                RETCOD )
      END IF
C
      IF (RETCOD .EQ. 0) THEN
C       successfully computed statistics, table
        IF (LOGARH .EQ. 2) THEN
C         statistics, no log transformation
          WRITE (FPRT,2101) XBAR, VAR, STD,
     $          SKEW, SESKEW, SCC, CVR
        ELSE
C         statistics, with log transformation
          WRITE (FPRT,2102) XBAR, VAR, STD,
     $          SKEW, SESKEW, SCC, CVR
        END IF
        IF (WOUT .EQ. 2) THEN
C         save attributes on wdm file
          CALL LPWDO1 ( WDMFL, MESSFL, SCLU, FPRT, DSN,
     I                  LOGARH, XBAR, STD, SKEW, NZI, NPOS,
     O                  ATRSAV, TCNT, RETCOD )
        END IF
C       conditional probablility
        CALL LGPST2 ( NPOS, NZI, NUMONS, NQS, XBAR, STD, SKEW,
     I                      LOGARH, ILH,
     M                      SE,
     O                      C, CCPA, P, Q, ADP, QNEW, RI,
     O                      RSOUT, RETCOD )
      END IF
C
      IF (RETCOD .EQ. 0) THEN
C       successfully computed probabilities, table
C       Dec 01 - # of rows in n-day tables increased from 11 to 12
C       to include the .3333 recurrence interval.
        IF (NZI .LE. 0) THEN
C         no zero data values
          IF (ILH .LE. 2) THEN
C           n-day flow statistics
            IF (ILH .EQ. 1) THEN
C             high flow
              WRITE (FPRT,2211)
            ELSE
C             low flow
              WRITE (FPRT,2212)
            END IF
            WRITE (FPRT,2221) (P(I), RI(I), Q(I), I = 1, 12)
          ELSE
C           monthly statistics
            WRITE (FPRT,2213)
            WRITE (FPRT,2223) (P(I), Q(I), I = 1, NQS)
          END IF
        ELSE
C         zero values, adjusted probablilities
          IF (ILH .LE. 2) THEN
C           n-day flow statistics
            IF (ILH .EQ. 1) THEN
C             high flow
              WRITE (FPRT,2231)
            ELSE
C             low flow
              WRITE (FPRT,2232)
            END IF
            WRITE (FPRT,2241) (P(I),RI(I),Q(I),ADP(I),QNEW(I),I=1,12)
          ELSE
C           monthly statistics
            WRITE (FPRT,2233)
            WRITE (FPRT,2243) (P(I),Q(I),ADP(I),QNEW(I),I=1,NQS)
          END IF
          WRITE (FPRT,2250)
        END IF
C
        IF (WOUT .EQ. 2) THEN
C         construct attribute name, find number, put attributes
          IF (ILH .LE. 2) THEN
C           for n-day statistics
            CALL LPWDO2 (WDMFL, MESSFL, SCLU, FPRT, DSN, ILH, NMDAYS,
     I                   NZI, RI, QNEW, Q, SCNOUT,
     M                   TCNT, ATRSAV )
          ELSE
C           for n-month statistics
            CALL LPWDO3 (WDMFL, MESSFL, SCLU, FPRT, DSN,
     I                   NZI, NQS, RI, QNEW, Q, SCNOUT, 
     M                   TCNT, ATRSAV )
          END IF
          IF (TCNT .GT. 0) THEN
C           print out which attributes added
            WRITE (FPRT,2260) TCNT, DSN, (ATRSAV(I),I=1,TCNT)
          END IF
        END IF
C
        IF (SCNOUT .EQ. 2) THEN
C         put results on screen
          SGRP = 40
          CALL Q1INIT (MESSFL,SCLU,SGRP)
          LEN = 22
          CALL QSETR (LEN,RSOUT)
          CALL Q1EDIT (IRET)
        END IF
        IF (IPLOT .EQ. 1) THEN
C         generate plot
          CALL LGPPLT ( MESSFL, SCLU, STATN, NPOS, NZI, NMDAYS,
     I                  LOGARH, ILH, NSM, NEM, C, CCPA, SE, 
     M                  X, DEVTYP )
        END IF
      END IF
C
      IF (RETCOD .NE. 0) THEN
C       problem with computations
        IF (RETCOD .EQ. -5) THEN
C         not enough data values
          WRITE (FPRT,2905)
        ELSE IF (RETCOD .EQ. -7) THEN
C         too many years
          WRITE (FPRT,2907) MXYRS, NBYR, NEYR
        ELSE IF (RETCOD .EQ. -21) THEN
C         datum too large
          WRITE (FPRT,2921)
        ELSE IF (RETCOD .EQ. -22) THEN
C         mean or variance <= 0, do not continue
          WRITE (FPRT,2922) XBAR, VAR
        ELSE IF (RETCOD .EQ. -31) THEN
C         skew < -3.3 or skew > 3.3
          WRITE (FPRT,2931) SKEW
        ELSE IF (RETCOD .EQ. -32) THEN
C         error in interpolation routine
          WRITE (FPRT,2932)
        END IF
        WRITE (FPRT,2999)
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LGPST1
     I                    ( FPRT, Y, LOGARH, N,
     O                      XBAR, VAR, STD, SKEW, SESKEW, SCC, CVR, X,
     O                      RETCOD )
C
C     + + + PURPOSE + + +
C     Computes mean, standard deviation, variance, skew, standard
C     error of skew, serial correlation coefficient, and coefficient
C     of variation.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER      FPRT, LOGARH, N, RETCOD
      REAL         Y(N), X(N),
     $             XBAR, VAR, STD, SKEW, SESKEW, SCC, CVR
C
C     + + + ARGUMENT DEFINITIONS + + +
C     FPRT   - Fortran unit number for error messages
C     Y      - annual time series
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C     N      - number of years
C     XBAR   - mean
C     VAR    - variance
C     STD    - standard deviation
C     SKEW   - skewness
C     SESKEW - standard error of skewness
C     SCC    - serial correlation coefficient
C     CVR    - coefficient of variation
C     X      - annual series
C              log base 10 tranformation if LOGARH = 1
C     RETCOD - return code
C                0 - no problems
C              -21 - datum value too large or small
C              -22 - mean or variance <= 0
C
C     + + + PARAMETERS + + +
      INCLUDE 'pa193.inc'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     NMONE, I
      REAL        XX(MXYRS), SUM1, SUM2, SUM3, SUM4, FN, DEV, SVAR, SNO
C
C     + + + INTRINSICS + + +
      INTRINSIC    ALOG10, FLOAT, ABS, SQRT
C
C     + + + OUTPUT FORMATS + + +
 2016 FORMAT('  *** Datum to large or small to process:',E12.5)
C
C     + + + END SPECIFICATIONS + + +
C
C     initialize variables
      RETCOD = 0
      SUM1   = 0.0
      FN     = FLOAT(N)
      IF (LOGARH .EQ. 2) THEN
C       compute with no transformations
C       accumulate the sum for computation of mean
        DO 320 I = 1, N
          X(I) = Y(I)
          SUM1 = SUM1 + X(I)
 320    CONTINUE
      ELSE
C       convert data to logs base 10
C       accumulate the sum of the logs for computation of mean
        DO 325 I = 1, N
          X(I) = ALOG10 ( Y(I) )
          SUM1 = SUM1 + X(I)
 325    CONTINUE
      END IF
C     mean
      XBAR = SUM1 / FN
C
C     accumulate sum of squares and cube of deviations from mean
      SUM2 = 0.0
      SUM3 = 0.0
      DO 330 I = 1, N
        DEV = X(I) - XBAR
        IF (ABS(DEV) .LT. 1.0E12) THEN
          SUM2 = SUM2  +  DEV * DEV
          SUM3 = SUM3  +  DEV * DEV * DEV
        ELSE
C         datum too large
          WRITE(FPRT,2016) X(I)
          RETCOD = -21
        END IF
 330  CONTINUE
C
C     compute the variance
      VAR = SUM2  /  (FN - 1.0)
      IF (VAR .GT. 0.1E-7 .AND.  RETCOD .EQ. 0) THEN
C       compute the standard deviation
        STD = SQRT ( VAR )
C       compute the skewness
        SKEW = (FN * SUM3)  /  ( (FN-1.0) * (FN-2.0) * STD*STD*STD )
C       compute the standard error of the skewness
        SVAR = (6.0 * FN * (FN-1.0)) / ((FN-2.0) * (FN+1.0) * (FN+3.0))
        SESKEW = SQRT ( SVAR )
C       compute serial correlation and coefficient of variation
        SUM3  = 0.0
        SNO   = N - 1
        NMONE = N - 1
        DO 335 I = 1, NMONE
          XX(I) = X(I) * X(I+1)
          SUM3  = XX(I) + SUM3
 335    CONTINUE
        SCC  = (SUM1 - X(N)) * (SUM1 - X(1))
        SCC  = (SNO * SUM3) - SCC
        SUM3 = 0.0
        DO 340 I=1,N
          XX(I) = X(I) * X(I)
          SUM3  = XX(I) + SUM3
 340    CONTINUE
        SUM4 = (SUM3 - (X(1) * X(1)))  *  SNO
        SUM3 = (SUM3 - (X(N) * X(N)))  *  SNO
        SUM2 = SUM1 - X(1)
        SUM1 = SUM1 - X(N)
        SUM1 = SUM1 * SUM1
        SUM2 = SUM2 * SUM2
        SUM3 = (SUM3 - SUM1)  *  (SUM4 - SUM2)
        SUM3 = SQRT ( SUM3 )
        SCC  = SCC / SUM3
        CVR  = STD / XBAR
      ELSE
C       mean or variance <= 0, do not continue
        RETCOD = -22
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LGPST2
     I                    ( N, NZI, NUMONS, NQS, XBAR, STD, SKEW,
     I                      LOGARH, ILH, 
     O                      SE, C, CCPA, P, Q, ADP, QNEW, RI,
     O                      RSOUT, RETCOD )
C
C     + + + PURPOSE + + +
C     Computes probabilities.  Does conditional probablility
C     adjustment if there are zero events.  Computes flow
C     statistics for selected recurrence intervals.
C
C     + + + HISTORY + + +
C     wrk 01/12/10  correct for problem at lower tail where a negaitve
C                   value may be computed in some instances.
C     wrk 01/12/12  add computation for 0.3333 recurrence interval.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   N, NZI, LOGARH, ILH, NUMONS, NQS, RETCOD
      REAL      SKEW, XBAR, STD, SE(27), C(27), CCPA(27),
     $          ADP(13), Q(13), QNEW(13), P(13), RI(13), RSOUT(22)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     N      - number of years
C     NZI    - number of years of zero events
C     NUMONS - number of number of months for statistic
C     NQS    - number of statistics
C              12 - for monthly statistic
C              11 - for high or low statistic
C     XBAR   - mean
C     STD    - standard deviation
C     SKEW   - skewness
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C     ILH    - flag for statistics option
C              1 - n-day high flow
C              2 - n-day low flow
C              3 - month
C     SE     - probabilities associated with C flows
C              exceedance if ILH = 1
C              non-exceedance otherwise
C     C      - flow characteristics associated with SE
C     CCPA   - if NZI > 0, then flow characterisitcs C with
C              conditional probablility adjustment,
C              otherwise undefined.
C     P      - exceedance (ILH=1) or non-exceedance (ILH>1)
C              probablility
C     Q      - parameter value
C     ADP    - if NZI > 0, adjusted exceedance (ILH=1) or
C              non-exceedance probablility (ILH>1),
C              otherwise undefined
C     QNEW   - if NZI > 0, adjusted parameter value,
C              otherwise undefined
C     RI     - recurrence interval
C     RSOUT  - recurrence intervals (1:11) and parameter
C              values (12:22), not adjusted for zero events
C     RETCOD - return code
C              -31 - skew out of range (< -3.3 or > 3.3)
C              -32 - error in interpolation routine
C
C     + + + SAVES + + +
      INTEGER     INITSV
      REAL        PLUS(27,35), FNEG(27,35), GP(35), GN(35)
      SAVE        PLUS, FNEG, GP, GN
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   IK, NTOP, NTOT, I
      REAL      FK(27), QCPA(27), T, TZI, TNI, PX, PNX
C
C     + + + FUNCTIONS + + +
      REAL       HARTAK
C
C     + + + INTRINSICS + + +
      INTRINSIC   ABS, REAL, INT
C
C     + + + EXTERNALS + + +
      EXTERNAL   FILLN, FILLGN, INTERN, FILLPL
      EXTERNAL   FILLP, FILLGP, INTERS
      EXTERNAL   CPA193, CALCQP
      EXTERNAL   HARTAK
C
C     + + + DATA INTITIALIZATIONS + + +
      DATA  INITSV / 0 /
C
C     + + + END SPECIFICATIONS + + +
C
      IF (INITSV .EQ. 0) THEN
C       initialize arrays
        CALL FILLN  ( FNEG )
        CALL FILLP  ( PLUS )
        CALL FILLGN ( GN )
        CALL FILLGP ( GP )
        INITSV = 1
      END IF
C
C     initialize variables
      RETCOD = 0
C
      IF (ABS(SKEW).GT.3.30) THEN
C       skew out of range ( < -3.3 or > 3.3 )
        RETCOD = -31
      ELSE
C       skew in valid range, interpolate
        IF (SKEW.GE.0.0) THEN
          CALL INTERS (SKEW,PLUS,GP,FK,IK)
        ELSE
          CALL INTERN (SKEW,FNEG,GN,FK,IK)
        END IF
        IF (IK.NE.0) THEN
C         error in interpolation routine
          RETCOD = -32
        END IF
      END IF
C
      IF (RETCOD .EQ. 0) THEN
        DO 345 I=1,27
          C(I)=XBAR+FK(I)*STD
C         Dec 01 - correct for problem at lower tail for negative values
          IF (LOGARH .EQ. 2  .AND.  C(I) .LT. 0.0) C(I) = 0.0
 345    CONTINUE
        NTOP=0
        NTOT=N + NZI
        IF (NZI.GT.0) THEN
C         zero events, conditional probability adjustment
          CALL CPA193 (C,NTOT,NZI,NTOP,
     O                 CCPA)
          DO 350 I=1,27
C           Dec 01 - first, correct for problem at lower tail for neg values
            IF (LOGARH .EQ. 2  .AND.  CCPA(I) .LT. 0) CCPA(I) = 0.0
            IF (ABS(CCPA(I)+31.0) .GT. 0.001) THEN
C             This logic is to change a very small number as
C             defined in the HARTAK routine used by CPA193
              IF (LOGARH .EQ. 1) THEN
                QCPA(I)=10.0**CCPA(I)
              ELSE
                QCPA(I) = CCPA(I)
              END IF
            ELSE
              QCPA(I)=0.0
            END IF
 350      CONTINUE
        END IF
C
C       Compute flow statistics for selected recurrence intervals
        CALL FILLPL ( SE )
        CALL CALCQP ( LOGARH, ILH, C, QCPA, NZI, NUMONS, NQS,
     M               SE,
     O               Q, QNEW, P )
        DO 360 I = 1,11
          RI(I) = 1.0/P(I)
          RSOUT(I) = REAL(INT(100.0*RI(I)+0.01))/100.0
          RSOUT(I+11) = Q(I)
 360    CONTINUE
        IF (NZI .GT. 0) THEN
C         zero flows
          T   = N
          TZI = NZI
          TNI = T + TZI
          IF (ILH .GT. 1) THEN
C           n-day low flow or month
            DO 365 I = 1,11
              ADP(I) = (T/TNI)*P(I) + TZI/TNI
 365        CONTINUE
          ELSE
C           n-day high flows
            DO 370 I = 1,11
              ADP(I) = T/TNI*P(I)
 370        CONTINUE
          END IF
        END IF
      END IF
C
C     rev 12/2001 wk -- compute and insert 3-year n-day statistics into
C     the Q, QNEW, P, ADP, and RI arrays which are returned to LGPFIT
C     for printing.
C
      IF (ILH .NE. 3) THEN
C       n-day, not monthly, 
C       open up space in arrays for storing 3-year n-day stats
        DO  410 I=1,6
          Q(13-I)    = Q(12-I)
          P(13-I)    = P(12-I)
          RI(13-I)   = RI(12-I)
          IF (NZI.GT.0) THEN
            QNEW(13-I) = QNEW(12-I)
            ADP(13-I)  = ADP(12-I)
          END IF
  410   CONTINUE
C
C       compute the 3-yr stats
        P(6)    = 0.3333
        RI(6)   = 3.00
        PNX     =  P(6)
        IF(ILH .EQ. 1) PNX   = 1. -  P(6)
        Q(6) = HARTAK( PNX  , C)
        IF (LOGARH .EQ. 1)  Q(6) = 10.**Q(6)
C
        IF(NZI .GT. 0) THEN
C          adjust for zero values
           PX      =  1. - PNX
           ADP(6)  =  PX*N/(N+NZI)
           IF(ILH .EQ. 2)  ADP(6) =  1. - ADP(6)
           QNEW(6) =  HARTAK(  PNX - PX*NZI/N ,  C )
           IF(QNEW(6) .GT. -30.9) THEN
              IF(LOGARH.EQ.1) QNEW(6)  = 10.**QNEW(6)
           ELSE
              QNEW(6) = 0.
           ENDIF
        ENDIF
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   LGPPLT
     I                   ( MESSFL, SCLU, STATN, N, NZI, NMDAYS,
     I                     LOGARH, ILH, NSM, NEM,
     I                     C, CCPA, SE, 
     M                     X, DEVTYP )
C
C     + + + PURPOSE + + +
C     Sort flows and manage plotting.
C
C     + + + HISTORY + + +
C     kmf Oct 24, 2000 - added code to free up Fortran unit number
C                        of old output plot file when a new file
C                        has been opened.  Previously, the unit
C                        number had remained allocated, when the
C                        user output many plots to individual files,
C                        the maximum number of unit numbers that
C                        the library manages was exceeded.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, N, NZI, NMDAYS, ILH, LOGARH,
     $            NSM, NEM, DEVTYP
      REAL        X(N), C(27), CCPA(27), SE(27)
      CHARACTER*1 STATN(80)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster in message file
C     STATN  - station number and name
C     N      - number of years
C     NZI    - number of years of zero events
C     NMDAYS - number of days for flow statistic
C     LOGARH - flag for log transformation (base 10)
C              1 - yes
C              2 - no
C     ILH    - flag for statistics option
C              1 - n-day high flow
C              2 - n-day low flow
C              3 - month
C     NSM    - start month of season
C     NEM    - end month of season
C     C      - flow characteristics associated with SE
C     CCPA   - if NZI > 0, then flow characterisitcs C with
C              conditional probablility adjustment,
C              otherwise undefined.
C     SE     - probabilities associated with C flows
C              exceedance if ILH = 1
C              non-exceedance otherwise
C     X      - annual flows,
C              sorted in ascending order if ILH > 1
C              sorted in descending order otherwise
C              log base 10 tranformation if LOGARH = 1
C     DEVTYP - plotting device type
C              1 - display monitor
C              2 - laser printer
C              3 - pen plotter
C              4 - CGM or GKS meta file
C
C     + + + PARAMETERS + + +
      INCLUDE 'pa193.inc'
C
C     + + + SAVES + + +
      INTEGER   FILOLD
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     I, I1, IC(7), ICLOS, IWAIT, IXTYP, LEN,
     $            RESP2, RETCOD, SGRP, WNDFLG, WSID, XTYP, CMPTYP,
     $            KEEP, FILNEW
Ckmf $          , DEVCOD
      REAL        SZ(MXYRS), FI, T, TNI, TZI
      CHARACTER*1 CXLAB(80)
      CHARACTER*8 LPTHNM(1), WNDNAM(2)
C
C     + + + INTRINSICS + + +
      INTRINSIC   FLOAT
C
C     + + + EXTERNALS + + +
      EXTERNAL   FPLOT
      EXTERNAL   RANKLW, RANK
      EXTERNAL   GETTXT, ZWNSOP, QRESP, ANPRGT
      EXTERNAL           GGATXB, GPLBXB
      EXTERNAL   PDNPLT, PLTONE, PROPLT, PSTUPW
      EXTERNAL   GGMTFL, GETFUN
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   I1, IC,  FILOLD
     $     /  1, 7*1,      0 /
C
C     + + + END SPECIFICATIONS + + +
C
      T   = N
      TZI = NZI
      TNI = T + TZI
C     get computer type
      I = 1
      CALL ANPRGT (I, CMPTYP)
C     initialize plotting specs
Ckmf  Dec 07, 2000 - gpinit is already called ~99
Ckmf  CALL GPINIT
C
Ckmf  set default device to screen, Dec 06 2000
Ckmf  this causes the size and position of the plot to
Ckmf  change when multiple plots are written to a PS file.
Ckmf  I = 39 + DEVTYP
Ckmf  CALL ANPRGT (I, DEVCOD)
Ckmf  CALL GPDEVC (DEVTYP, DEVCOD)
Ckmf  end set default device, kmf, Dec 06 2000
      DO 385 I=1,N
        FI=FLOAT(I)
        IF (ILH .EQ. 1  .OR.  NZI .EQ. 0) THEN
C         for highs w and w/o zeros, plot lows w/o zeros
          SZ(I)=FI/(TNI+1.0)
        ELSE
          SZ(I)=(FI+TZI)/(TNI+1.0)
        END IF
 385  CONTINUE
C
      IF (ILH.GT.1) THEN
C       low flow or month
        CALL RANKLW (N, X)
      ELSE
C       high flow
        CALL RANK (N, X)
      END IF
      IF (NZI.GT.0) THEN
        CALL FPLOT (MESSFL,SCLU,X,SZ,CCPA,SE,N,NZI,
     I              ILH,NMDAYS,STATN,DEVTYP,LOGARH,
     I              NSM,NEM)
      ELSE
        CALL FPLOT (MESSFL,SCLU,X,SZ,C,SE,N,NZI,
     I              ILH,NMDAYS,STATN,DEVTYP,LOGARH,
     I              NSM,NEM)
      END IF
      WSID = 1
      RESP2 = 1
 390  CONTINUE
C       option: 1-plot, 2-modify, 3-return
        LPTHNM(1) = 'S'
        CALL ZWNSOP (I1,LPTHNM)
        SGRP= 20
        CALL QRESP (MESSFL,SCLU,SGRP,RESP2)
        IF (RESP2.EQ.2) THEN
C         modify options
          WNDNAM(1)= 'Modify'
          WNDNAM(2)= 'SFAM'
          CALL GGATXB (IXTYP)
          CALL PROPLT (MESSFL,IC,WNDNAM,WNDFLG)
          CALL GGATXB (XTYP)
          IF (IXTYP .NE. XTYP) THEN
C           user changed x axis type so change label
            LEN = 80
            SGRP = 40 + XTYP
            CALL GETTXT (MESSFL,SCLU,SGRP,LEN,CXLAB)
            CALL GPLBXB (CXLAB)
          END IF
          IF (WNDFLG .EQ. 1) THEN
C           user changed device
            IF (CMPTYP .NE. 1) THEN
C             not pc, close workstation
              IWAIT = 0
              ICLOS = 1
              CALL PDNPLT (WSID,ICLOS,IWAIT)
              CALL GGMTFL ( FILNEW )
              IF (FILOLD .NE. FILNEW) THEN
C               changed output file
                IF (FILOLD .NE. 0) THEN
C                 free the unit number for the old file
                  KEEP = 2
                  CALL GETFUN ( KEEP, FILOLD )
                END IF
                FILOLD = FILNEW
              END IF
            END IF
          END IF
          RESP2 = 1
        ELSE IF (RESP2.EQ.1) THEN
C         generate plot
          IWAIT = 0
          CALL PSTUPW (WSID, RETCOD)
          CALL PLTONE
          IF (CMPTYP .EQ. 1) THEN
            ICLOS = 1
          ELSE
            ICLOS = 0
          END IF
          CALL PDNPLT (WSID,ICLOS,IWAIT)
          RESP2 = 2
        END IF
      IF (RESP2.NE.3) GO TO 390
C
      RETURN
      END
