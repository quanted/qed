C
C
C
      SUBROUTINE   FPLOT
     I                   (MESSFL,SCLU,X,SZ,C,SE,N,NZ,ILH,
     I                    NMDAYS,STATN,GDEVTY,LOGARH,NSM,NEM)
C
C     + +  PURPOSE + + +
C     Fill graphics common block with default values for
C     Log-Pearson type plot.
C
C     + + + HISTORY + + +
C     kmf, Oct 24, 2000 - removed call to gpdevc and related call
C                         to anprgt.  gpdevc was changing the
C                         output device when it shouldn't, causing
C                         some output file formats to have changing
C                         plot sizes when more than one plot was
C                         output to a file.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL,SCLU,N,NZ,ILH,NMDAYS,GDEVTY,LOGARH,NSM,NEM
      REAL        X(N),SZ(N),C(27),SE(27)
      CHARACTER*1 STATN(80)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number for message file
C     SCLU   - cluster number on message file
C     X      - log of peak flows base 10
C     SZ     - probabilities as a fraction
C     C      - log of computed flow base 10
C     SE     - probabilities of computed flows
C     N      - number of measured peak flows
C     NZ     - number of zero peak flows
C     ILH    - flag for statistic
C              1 - n-day high flow
C              2 - n-day low flow
C              3 - month
C     NMDAYS - number of days for flow statistic
C     STATN  - station number and name
C     GDEVTY - device type
C              1 - display monitor
C              2 - laser printer
C              3 - pen plotter
C              4 - CGM or GKS meta file
C     LOGARH - log transformation flag, 1-yes, 2-no
C     NSM    - start month of season
C     NEM    - end month of season
C
C     + + + PARAMETERS + + +
      INCLUDE 'pa193.inc'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER     I,I1,I2,I4,I5,I80,I240,SGRP,IPOS,RETCOD,I3,    
     1            LEN,LOC,OLEN,NP,NZP,LL(2),WHICH(4),GCV(2),GLN(2),
     2            GSY(2),GPT(2),GTRAN(4),GCL(2),LX,IMIN,IMAX,
     3                       GTICS(4),GBVALF(4),L20,IIMAX,IIMIN
      REAL        TMP(MXYRS),Z,VMIN(4),VMAX(4),GLOC(2),R0,
     1            GSIZEL,GXPAGE,GYPAGE,GXPHYS,GYPHYS,GXLEN,GYLEN,
     2            GPLMN(4),GPLMX(4),
     3            XMIN,XMAX,YMIN,YMAX
      CHARACTER*1 CDUM(80),BLNK,CY(80),CX(80),GTITL(240),GLB(20,4),
     1            CD(5),CF(4),CL(4),CH(5),
     2            MC(12,3)
C
C     + + + INTRINSICS + + +
      INTRINSIC   ABS
C
C     + + + FUNCTIONS + + +
      REAL        GAUSEX, SRMIN, SRMAX
C
C     + + + EXTERNALS + + +
      EXTERNAL    GAUSEX, SRMIN, SRMAX, GPNCRV, GPDATA, GPWCXY
      EXTERNAL    GETTXT, GPLEDG, CHRCHR, INTCHR, GPLABL, ZIPC, COPYI
      EXTERNAL    GPCURV, GPVAR, GPSIZE,                 SCALIT, GPSCLE
      EXTERNAL    GPLBXB
C
C     + + + DATA INITIALIZATION + + +
      DATA   I1, I2, I3, I4, I5, I80, I240,BLNK, R0
     #    /   1,  2,  3,  4,  5,  80,  240, ' ',0.0/
      DATA GCV/6,6/, GLN/0,1/, GSY/4,0/, GPT/0,0/, GCL/1,1/, L20/20/
      DATA CL/'l','o','w',' '/,  CH/'h','i','g','h',' '/
     &     CF/'f','l','o','w'/,  CD/'-','d','a','y',' '/
      DATA GBVALF,GTICS/4*1,4*10/
      DATA GSIZEL, GXPAGE, GYPAGE, GXPHYS, GYPHYS, GXLEN, GYLEN
     1    /  0.11,   10.0,    8.0,    1.5,    1.5,   7.5,   5.0/
      DATA MC/'J','a','n','F','e','b','M','a','r','A','p','r',
     &        'M','a','y','J','u','n','J','u','l','A','u','g',
     &        'S','e','p','O','c','t','N','o','v','D','e','c'/
C
C    + + + OUTPUT FORMATS + + +
C    (keep in code for general information)
C 400 FORMAT ('0','THE FOLLOWING DATA VALUE ',F13.3,' WITH ASSOCIATED ',
C    1'PROBABILITY OF ',F7.4,' WAS NOT PLOTTED'/)
C 410 FORMAT ('0','THE FOLLOWING COMPUTED VALUE ',F13.3,' WITH ASSOCIAT'
C    1,'ED PROBABILITY OF ',F7.4,' WAS NOT PLOTTED'/)
C 420 FORMAT (' ',60X,'PROBABILITY'/' ',7X,'0.995 0.99',11X,'0.95',4X,'0
C    1.90',5X,'0.80',14X,'0.50',14X,'0.20',5X,'0.1',7X,'0.04',3X,'0.02',
C    22X,'0.01',1X,'0.005',1X)
C 450 FORMAT (' ',7X,'1.005 1.01',11X,'1.05',4X,'1.11',5X,'1.25',15X,'2'
C    1,17X,'5',7X,'10',8X,'25',5X,'50',4X,'100',2X,'200'/' ',56X,'RECURR
C    2ENCE INTERVALS',1X//)
C 460 FORMAT ('0','THE FOLLOWING SYMBOLS MAY APPEAR IN THE PLOT'/' ','X
C    1- AN INPUT DATA VALUE'/' ','* - A CALCULATED VALUE'/' ','O - A CAL
C    2CULATED VALUE AND ONE DATA VALUE AT SAME POSITION'/' ','2 - TWO IN
C    3PUT DATA VALUES PLOTTED AT SAME POSITION'/' ','3 - THREE INPUT DAT
C    4A VALUES PLOTTED AT SAME POSITION'/' ','A - A CALCULATED VALUE AND
C    5 TWO DATA VALUES AT SAME POSITION'/' ','B - A CALCULATED VALUE AND
C    6 THREE DATA VALUES AT SAME POSITION')
C 470 FORMAT ('0','NOTE -- THE INPUT DATA VALUES ARE BASED ON NON-ZERO V
C    1ALUES AND TOTAL (NON-ZERO + ZERO VALUES) SAMPLE SIZE.')
C 480 FORMAT (' ',8X,'THE CALCULATED VALUES ARE BASED ON ADJUSTED (UNCON
C    1DITIONAL) PARAMETER VALUES.')
C
C     + + + END SPECIFICATIONS + + +
C
      NP = N
      IF (NP .GT. MXYRS) NP = MXYRS
      NZP = NZ
      IF (NZP .GT. MXYRS) NZP = MXYRS
Ckmf  removed call to gpdevc, Oct 24, 2000, kmf
Ckmf  set default device
Ckmf  IND = 39+ GDEVTY
Ckmf  CALL ANPRGT (IND,GDEVCD)
Ckmf  CALL GPDEVC (GDEVTY,GDEVCD)
C     number of curves and variables
      CALL GPNCRV (I2,I4)
C     data to plot
      IPOS = 1
      DO 2 I = 1,NP
        TMP(I) = GAUSEX(SZ(I))
 2    CONTINUE
      Z = ABS(TMP(1))
      IF (Z .LT. ABS(TMP(NP))) Z = ABS(TMP(NP))
      VMIN(1) = -Z
      VMAX(1) = Z
      WHICH(1) = 4
      CALL GPDATA (I1,NP,TMP,RETCOD)
C
      IPOS = IPOS + NP
      DO 4 I = 1,NP
        IF (LOGARH .EQ. 1) THEN
          TMP(I) = 10.0**X(I)
        ELSE
          TMP(I) = X(I)
        END IF
 4    CONTINUE
      VMIN(2) = SRMIN(NP,TMP)
      VMAX(2) = SRMAX(NP,TMP)
      WHICH(2) = 1
      CALL GPDATA (I2,NP,TMP,RETCOD)
C
      IPOS = IPOS + NP
      DO 6 I = 1,27
        TMP(I) = GAUSEX(SE(I))
 6    CONTINUE
      IF (ILH.EQ.1) THEN
C       for high flows
        DO 7 I = 1,27
          IF (TMP(I) .LT. -Z) IMIN = I
          IF (TMP(I) .LT. Z)  IMAX = I
 7      CONTINUE
        IMIN = IMIN + 1
        VMIN(3) = TMP(IMIN)
        VMAX(3) = TMP(IMAX)
      ELSE
C       for low flows
        DO 8 I = 1,27
          IF (TMP(I) .GT. -Z) IMAX = I
          IF (TMP(I) .GT. Z)  IMIN = I
 8      CONTINUE
        IMIN = IMIN + 1
        VMIN(3) = TMP(IMAX)
        VMAX(3) = TMP(IMIN)
      END IF
      LEN = ABS(IMAX-IMIN) + 1
      WHICH(3) = 4
C     drop any zero flows if analysis with logs
      IF (LOGARH .EQ. 1) THEN
C       values in C are logs when LOGARH = 1
        IIMIN = IMIN
        IIMAX = IMAX
        DO 11 I = IMIN, IMAX
          IF (C(I) .LT. -10.0) IIMIN = I+1
 11     CONTINUE
C       reset IMIN and LEN
        LEN = ABS(IIMAX - IIMIN) + 1
        IMIN = IIMIN
        IMAX = IIMAX
      END IF
      CALL GPDATA (I3,LEN,TMP(IMIN),RETCOD)
C
      IPOS = IPOS + LEN
      DO 9 I = IMIN,IMAX
        IF (LOGARH .EQ. 1) THEN
          TMP(I) = 10.0**C(I)
        ELSE
          TMP(I) = C(I)
        END IF
 9    CONTINUE
      VMIN(4) = SRMIN(LEN,TMP(IMIN))
      VMAX(4) = SRMAX(LEN,TMP(IMIN))
      WHICH(4) = 1
      CALL GPDATA (I4,LEN,TMP(IMIN),RETCOD)
C
C     set which variable for each curve
      CALL GPWCXY (I1,I2,I1)
      CALL GPWCXY (I2,I4,I3)
C
C     labels and axis type
      CALL ZIPC (I80,BLNK,CDUM)
C     select log or arith for left y-axis
C     if LOGARH = 1, LL = 2,   if LOGARH = 2, LL = 1
      LL(1)= 3 - LOGARH
      LL(2)= 0
C     label for x and y axes
      IF (ILH.EQ.1) THEN
C       for high flow
        SGRP = 46
        LX   = 3
      ELSE
        SGRP = 43
        LX   = 3
      END IF
      LEN = 80
      CALL GETTXT (MESSFL,SCLU,SGRP,LEN,CX)
      SGRP= 21
      LEN = 80
      CALL GETTXT (MESSFL,SCLU,SGRP,LEN,CY)
      CALL ZIPC (I240,BLNK,GTITL)
      LEN = 80
      CALL CHRCHR (LEN, STATN, GTITL)
      CALL GPLABL (LX,LL,R0,CY,CX,CDUM,GTITL)
C     also x-axis label
      CALL GPLBXB (CX)
C     determine default x-axis scale based on min/max values
      IF (VMIN(1).LT.VMIN(3)) THEN
        XMIN= VMIN(1)
      ELSE
        XMIN= VMIN(3)
      END IF
      IF (VMAX(1).GT.VMAX(3)) THEN
        XMAX= VMAX(1)
      ELSE
        XMAX= VMAX(3)
      END IF
      CALL SCALIT (LX,XMIN,XMAX,GPLMN(4),GPLMX(4))
C     determine default y-axis scale based on min/max values
      IF (VMIN(2).LT.VMIN(4)) THEN
        YMIN= VMIN(2)
      ELSE
        YMIN= VMIN(4)
      END IF
      IF (VMAX(2).GT.VMAX(4)) THEN
        YMAX= VMAX(2)
      ELSE
        YMAX= VMAX(4)
      END IF
      CALL SCALIT (LL(1),YMIN,YMAX,GPLMN(1),GPLMX(1))
C     set scale for axes
      GPLMN(2)= 0.0
      GPLMN(3)= 0.0
      GPLMX(2)= 0.0
      GPLMX(3)= 0.0
      CALL GPSCLE (GPLMN,GPLMX,GTICS,GBVALF)
C     location of legend
      IF (ILH.EQ.1) THEN
        GLOC(1) = 0.05
      ELSE
        GLOC(1) = 0.5
      END IF
      GLOC(2) = 0.9
      CALL GPLEDG (GLOC)
C     get variable names and set min/max for each variable
C     Assigned std deviates, Observed flow, Calc std deviates,
C     Estimated flow
      SGRP= 24
      LEN = 80
      CALL GETTXT (MESSFL,SCLU,SGRP,LEN,GLB)
C     set transformations flags
      GTRAN(1) = 1
      GTRAN(2) = LL(1)
      GTRAN(3) = 1
      GTRAN(4) = LL(1)
      CALL GPVAR (VMIN,VMAX,WHICH,GTRAN,GLB)
C     set specs for curves
C     Observed    Log-Pearson Type III
      SGRP= 25
      LEN = 80
      CALL GETTXT (MESSFL,SCLU,SGRP,LEN,GLB)
C
      IF (LOGARH .EQ. 2) THEN
C       delete Log- if not Log-Pearson analysis
        CALL COPYI (L20,GLB(5,2),GLB(1,2))
      END IF
C     construct label for flow statistic
      IF (ILH .LE. 2) THEN
C       n-day high(1)/low(2) flow
        LOC = 1
        LEN = 5
        CALL INTCHR (NMDAYS,LEN,I1,OLEN,GLB(LOC,1))
        LOC = LOC + OLEN
        CALL CHRCHR (I5,CD,GLB(LOC,1))
        LOC = LOC + I5
        IF (ILH .EQ. 2) THEN
          CALL CHRCHR (I4,CL,GLB(LOC,1))
          LOC = LOC + I4
        ELSE
          CALL CHRCHR (I5,CH,GLB(LOC,1))
          LOC = LOC + I5
        END IF
      ELSE
C       month-to month flow
        LOC = 1
        LEN = 3
        CALL CHRCHR (LEN,MC(NSM,1),GLB(LOC,1))
        GLB(4,1) = '-'
        LOC = 5
        CALL CHRCHR (LEN,MC(NEM,1),GLB(LOC,1))
        LOC = 9
      END IF
C     add 'flow'
      CALL CHRCHR (I4,CF,GLB(LOC,1))
C
      CALL GPCURV (GCV,GLN,GSY,GCL,GPT,GLB)
C     set plot sizes
      CALL GPSIZE (GSIZEL,GXPAGE,GYPAGE,GXPHYS,GYPHYS,GXLEN,GYLEN,R0)
C
      RETURN
      END
