C
C
C
      SUBROUTINE   GRDUMP
     I                    ( OPT, TEXT )
C
C     + + + PURPOSE + + +
C     Output selected variables form the plotting common blocks
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER       OPT
      CHARACTER*12  TEXT
C
C     + + + ARGUMENT DEFINITIONS + + +
C     OPT    - what should be output
C              0 - all of below
C              1 - physical dimensions
C              2 - relative dimensions
C              3 - devices
C              4 - title
C              5 - devices + title
C     TEXT   - descriptive text
C
C     + + + PARAMETERS + + +
      INCLUDE 'ptsmax.inc'
C
C     + + + COMMON BLOCKS + + +
      INCLUDE 'cplot.inc'
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (  1X, A12, ' grdump:  plotting parameters:' )
 2001 FORMAT ( 23X, '         dimensions:  xpage =',  F6.2,
     $      /, 23X, '                      ypage =',  F6.2,
     $      /, 23X, '                       xlen =',  F6.2,
     $      /, 23X, '                       ylen =',  F6.2,
     $      /, 23X, '                       alen =',  F6.2,
     $      /, 23X, '                      sizel =',  F6.2 )
 2002 FORMAT ( 23X, '          locations:  xphys =',  F6.2,
     $      /, 23X, '                      yphys =',  F6.2,
     $      /, 23X, '                     xwinlc =', 4F6.2 )
 2003 FORMAT ( 23X, '    units & devices: devtyp =', I6,
     $      /, 23X, '                     devcod =', I6,
     $      /, 23X, '                     mtplut =', I6 )
 2004 FORMAT ( 23X, '              title:   titl = ', 40A1 )
C
C     + + + END SPECIFICATIONS + + +
C
      WRITE (FE,2000) TEXT
C
      IF (OPT .EQ. 0  .OR.  OPT .EQ. 1) THEN
C       physical dimensions
        WRITE (FE,2001) XPAGE, YPAGE, XLEN, YLEN, ALEN, SIZEL
      END IF
      IF (OPT .EQ. 0  .OR.  OPT .EQ. 2) THEN
C       relative dimensions
        WRITE (FE,2002) XPHYS, YPHYS, XWINLC
      END IF
C
      IF (OPT .EQ. 0  .OR.  OPT .EQ. 3  .OR.  OPT .EQ. 5) THEN
C       devices
        WRITE (FE,2003) DEVTYP, DEVCOD, MTPLUT
      END IF
C
      IF (OPT .EQ. 0  .OR.  OPT .EQ. 4  .OR.  OPT .EQ. 5) THEN
C       title
        WRITE (FE,2004) (TITL(I), I = 1, 40)
      END IF
C
      RETURN
      END
