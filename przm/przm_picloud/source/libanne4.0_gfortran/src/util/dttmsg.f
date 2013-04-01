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
Cy2k  with older code.  Assumes that the Silicon Graphics routine
Cy2k  FDATE will continue to return a 2-digit year in positions
Cy2k  9 and 10.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   YR, MO, DY, HR, MN, SC
C
C     + + + ARGUMENT DEFINITIONS
C     YR     - year
C     MO     - month
C     DA     - day
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
C     This version of SYDATE calls the Silicon Graphics system
C     routine FDATE.
Cy2k  Note:  Returns a 2-digit year for backwords compatability
Cy2k  with older code.  Assumes that the Silicon Graphics routine
Cy2k  FDATE will continue to return a 2-digit year in positions
Cy2k  9 and 10.
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
      CHARACTER*24 DATBUF
C
C     + + + FUNCTIONS + + +
      CHARACTER*24 FDATE
C
C     + + + EXTERNALS + + +
      EXTERNAL  FDATE
C
C     + + + INPUT FORMATS + + +
 1000 FORMAT ( 5X, I2, 1X, I2, 12X, I2 )
C
C     + + + END SPECIFICATIONS + + +
C
      DATBUF = FDATE ( )
      READ (DATBUF,1000) MO, YR, DA
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
C     This version of SYTIME calls the Silicon Graphics system
C     routine FDATE.
Cy2k  NOTE:  assumes that FDATE will continue to return a
Cy2k         2-digit year in positions 9 and 10.
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
      CHARACTER*24 DATBUF
C
C     + + + FUNCTIONS + + +
      CHARACTER*24 FDATE
C
C     + + + EXTERNALS + + +
      EXTERNAL  FDATE
C
C     + + + INPUT FORMATS + + +
 1000 FORMAT ( 11X, I2, 1X, I2, 1X, I2 )
C
C     + + + END SPECIFICATIONS + + +
C
      DATBUF = FDATE ( )
      READ (DATBUF,1000) HR, MN, SC
C
      RETURN
      END
