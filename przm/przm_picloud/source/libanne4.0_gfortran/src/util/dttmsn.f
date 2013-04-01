C
C
C
      SUBROUTINE   WDSYSD
     O                   (IDATE)
C
C     + + + PURPOSE + + +
C     Fetch system date and time for DSN creation/modification
C     attributes.  Assumes that sydatm returns a 2 digit year
C     and that the year is 2000 or later.
C     *** FORTRAN 77 ONLY ***
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   IDATE(4)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     IDATE  - integer array containing character representation
C              of date and time
C              (1) - 4-digit year
C              (2) - 2-digit month and 2-digit day
C              (3) - 2-digit hour and 2-digit month
C              (4) - 2-digit second and 2 blanks
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      YR,MO,DY,HR,MN,SC
      CHARACTER*16 DATE
C
C     + + + EXTERNALS + + +
      EXTERNAL     SYDATM
C
C     + + + INPUT FORMATS + + +
 1000 FORMAT (A4,5A2,2X)
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (I4,5I2,2X)
C
C     + + + END SPECIFICATIONS + + +
C
      CALL SYDATM (YR,MO,DY,HR,MN,SC)
      YR = YR + 2000
      WRITE (DATE,2000) YR,MO,DY,HR,MN,SC
      READ (DATE,1000) IDATE
C
      RETURN
      END
C
C
C
      SUBROUTINE   SYDATM
     O                   ( YR, MO, DY, HR, MN, SC )
C
C     + + + PURPOSE + + +
C     Returns the current date and time.  Calls the system dependent
C     subroutines SYDATE for the date and SYTIME for the time.
Cy2k  Note:  Returns a 2-digit year for backwords compatability
Cy2k  with older code.  No assumptions are made as to what number
Cy2k  of digits are returned by the Sun routine IDATE.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   YR, MO, DY, HR, MN, SC
C
C     + + + ARGUMENT DEFINITIONS
C     YR     - year
C     MO     - month
C     DY     - day
C     HR     - hour
C     MN     - minute
C     SC     - second
C
C     + + + EXTERNALS + + +
      EXTERNAL   SYDATE, SYTIME
C
C     + + + END SPECIFICATIONS + + +
C
C     get date
      CALL SYDATE ( YR, MO, DY )
C
C     get time
      CALL SYTIME ( HR, MN, SC )
C
      RETURN
      END
C
C
C
      SUBROUTINE   SYDATE
     O                   ( YR, MO, DA )
C
C     + + + PURPOSE + + +
C     This subroutine is used to retrieve the system date.
C     This version of SYDATE calls the standard SUN OS system
C     subroutine IDATE.  Note that the SUN VMS version of
C     IDATE is call idate ( m, d, y )
Cy2k  Note:  Returns a 2-digit year for backwords compatability
Cy2k  with older code.  No assumptions are made as to what number
Cy2k  of digits are returned by the Sun routine IDATE.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   YR, MO, DA
C
C     + + + ARGUMENT DEFINITIONS + + +
C     YR     - year
C     MO     - month
C     DA     - day
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   STRING(3)
C
C     + + + EXTERNALS + + +
!eca  EXTERNAL  IDATE
C
C     + + + END SPECIFICATIONS + + +
C
      CALL IDATE ( STRING )
      YR = MOD( STRING(3), 100 )
      MO = STRING(2)
      DA = STRING(1)
C
      RETURN
      END
C
C
C
      SUBROUTINE   SYTIME
     O                   ( HR, MN, SC )
C
C     + + + PURPOSE + + +
C     This subroutine is used to retrieve the system time.
C     This version of SYTIME calls the standard SUN OS system
C     subroutine  ITIME.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   HR, MN, SC
C
C     + + + ARGUMENT DEFINITIONS + + +
C     HR     - Number of hours since midnight
C     MN     - Number of minutes since hour
C     SC     - Number of seconds since minute
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   STRING(3)
C
C     + + + LOCAL DEFINITIONS + + +
C     STRING - current time
C              (1) hour since midnight
C              (2) minute since hour
C              (3) second since minute
C
C     + + + EXTERNALS + + +
!eca  EXTERNAL  ITIME
C
C     + + + END SPECIFICATIONS + + +
C
      CALL ITIME ( STRING )
C     broken out to avoid I*2 overflow possibility
      HR = STRING(1)
      MN = STRING(2)
      SC = STRING(3)
C
      RETURN
      END
