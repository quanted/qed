C
C
C
      SUBROUTINE   OPTOUT
     I                    (MESSFL, WNDNAM,
     M                     TORF, LINES, WIDTH,
     O                     FOUT, RETC)
C
C     + + + PURPOSE + + +
C     This routine asks if output is to go to the terminal or a file.
C     For the terminal option the user specifies the width and number
C     of lines for the terminal.  for file the user specifies the width
C     and the number of lines per page for printout.  For a flat file
C     the user should specify a value greater than the expected output.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER   MESSFL, TORF, LINES, WIDTH, FOUT, RETC
      CHARACTER WNDNAM*(*)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     WNDNAM - data window screen name
C     TORF   - output option
C              1 - terminal
C              2 - file, flat or printed
C     LINES  - number of lines for page or terminal screen
C     WIDTH  - number of characters wide
C     FOUT   - Fortran unit number for output
C     RETC   - return code
C              0 - successful
C              1 - could not open output file
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   ERR, RNUM, INUM, CNUM, IVAL(2), OPT(1,3),
     #          SGRP, FSCLU, IND
      REAL      RVAL(1)
      CHARACTER*1  TBUFF(80)
C
C     + + + EXTERNALS + + +
      EXTERNAL   QRESPM, ANPRGT, QFOPEN, ZWNSET
C
C     + + + DATA INITIALIZATIONS + + +
      DATA  RNUM, INUM, CNUM, IND
     #    /    1,   2,     1,   4 /
C
C     + + + END SPECIFICATIONS + + +
C
      FSCLU= 2
      RETC = 0
      ERR  = 0
C
C     set programmer specified defaults
      IVAL(1) = -999
      IVAL(2) = -999
      OPT(1,1)= 1
      IF (LINES.GT.5 .AND. LINES.LT.200000) THEN
C       valid number of lines
        IVAL(1) = LINES
      END IF
      IF (WIDTH.GT.40 .AND. WIDTH.LT.250) THEN
C       valid number of characters
        IVAL(2) = WIDTH
      END IF
      IF (TORF.NE.1) THEN
C       set output target to file (instead of default of screen)
        OPT(1,1) = TORF
      END IF
C
C     get user specifications
      CALL ZWNSET (WNDNAM)
      SGRP = 57
      CALL QRESPM (MESSFL, FSCLU, SGRP, INUM, RNUM, CNUM,
     M             IVAL, RVAL, OPT, TBUFF)
      IF (OPT(1,1) .EQ. 1) THEN
C       terminal output, get unit number
        CALL ANPRGT (IND, FOUT)
      ELSE
C       file output, open file and get unit number
        CALL ZWNSET (WNDNAM)
        SGRP = 12
        CALL QFOPEN (MESSFL, FSCLU, SGRP, FOUT, ERR)
      END IF
C
      TORF = OPT(1,1)
      LINES= IVAL(1)
      WIDTH= IVAL(2)
      IF (ERR.NE.0) THEN
C       problem opening file
        RETC = 1
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   REOPEN
     I                    ( MESSFL, SCLU, SGRP1, SGRP2,
     M                      FOUT )
C
C     + + + PURPOSE + + +
C     Open an output file.  If a file is already open, the
C     name is displayed on the screen, and the user has the
C     opportunity to use it.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER      MESSFL, SCLU, SGRP1, SGRP2, FOUT
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster group in message file
C     SGRP1  - group number for case where no file is open
C     SGRP2  - group number for case where file is open
C     FOUT   - Fortran unit number of file
C
C     + + + LOCAL VARIABLES + + +
      INTEGER      RTCMND, LEN1, LEN64, KEEP, PREV, ON, OFF
      CHARACTER*64 FNAME
C
C     + + + EXTERNALS + + +
      EXTERNAL   Q1EDIT, Q1INIT, QSTCTF, QGETF, ZSTCMA
      EXTERNAL   QFSTAT, QFCLOS
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN64, KEEP, PREV, ON, OFF
     $      /   1,    64,    0,    4,  1,   0 /
C
C     + + + END SPECIFICATIONS + + +
C
C     turn on Prev
      CALL ZSTCMA ( PREV, ON )
C
      IF (FOUT .LE. 0) THEN
C       no file open
 100    CONTINUE
          CALL Q1INIT ( MESSFL, SCLU, SGRP1 )
          CALL Q1EDIT ( RTCMND )
          IF (RTCMND .EQ. 1) then
C           file opened
            CALL QGETF ( LEN1, FOUT )
          END IF
        IF (RTCMND .EQ. -1) GO TO 100
      ELSE
C       a file is already open, get name
        CALL QFSTAT ( FOUT, FNAME )
  200   CONTINUE
          CALL Q1INIT ( MESSFL, SCLU, SGRP2 )
          CALL QSTCTF ( LEN1, LEN64, FNAME )
          CALL Q1EDIT ( RTCMND )
          IF (RTCMND .EQ. 1) THEN
C           close old file and retrieve unit number of new file
            CALL QFCLOS ( FOUT, KEEP )
            CALL QGETF ( LEN1, FOUT )
            WRITE (99,*) ' old file closed, new file opened'
          ELSE IF (RTCMND .EQ. 2) THEN
C           Prev, use old file, new file not opened
            WRITE (99,*) ' using file already opened'
          END IF
        IF (RTCMND .EQ. -1) GO TO 200
      END IF
C
C     turn Prev off
      CALL ZSTCMA ( PREV, OFF )
C
      RETURN
      END
C
C
C
      SUBROUTINE   STFLOP
     I                   ( MESSFL, SCLU, SGRP,
     M                     FOUT, NEWFIL,
     O                     RETC )
C
C     + + + PURPOSE + + +
C     Open a file for output.  If a file is already open, it checks
C     to see if it is the requested file.  If the requested file is
C     the same as the already open file, no action is taken.  If
C     the requested file is different from the already open file,
C     the open file is closed and the new file is opened.
C
C     + + + DUMMY ARGUMENTS + + + 
      INTEGER   MESSFL, SCLU, SGRP, FOUT, RETC
      CHARACTER*64 NEWFIL
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - cluster number on message file
C     SGRP   - group in SCLU containing file open message
C     FOUT   - Fortran unit number of print output file
C     NEWFIL - name of file for print output
C     RETC   - return code
C               0 - everything ok
C              <0 - return code from file open
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   NEWF, INQERR, FIXYES, KEEP, OPNFLG
      LOGICAL   OD
C
C     + + + LOCAL DEFINITIONS + + +
C     FIXYES - indicator for action to take when problem with file open
C              2 - called subroutine should try to handle it
C              0 - calling routine will print message
C              1 - called routine will print message but not try to fix
C     KEEP   - indicator for action to take when closing file
C              0 - keep file
C              1 - delete file
C
C     + + + EXTERNALS + + +
      EXTERNAL   QFCLOS, QFOPFN
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   FIXYES, KEEP
     $     /      2,    0 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETC = 0
C
      IF (FOUT .LE. 0) THEN
C       no file open, set flag to open this file
        OPNFLG = 1
      ELSE
C       a file is already open, is it the requested file?
        INQUIRE ( FILE = NEWFIL,
     $          NUMBER = NEWF,
     $          OPENED = OD,
     $          IOSTAT = INQERR )
C     write (99,*) '**** <-- inquire:  file = ', newfil
C     write (99,*) '****             opened = ', od
C     write (99,*) '****             iostat = ', inqerr
C     write (99,*) '****               newf = ', newf
C     write (99,*) '****               fout = ', fout
        IF (INQERR .EQ. 0) THEN
C         no error condition, what about the file
          IF (OD .EQV. .TRUE.) THEN
C           file is open
            OPNFLG = 0
            IF (NEWF .NE. FOUT) THEN
C             unxepected unit, close expected unit & renumber
              CALL QFCLOS ( FOUT, KEEP )
              FOUT = NEWF
            END IF
          ELSE
C           file is not open, open it
            OPNFLG = 1
          END IF
        ELSE
C         error condition, assume new output file, close old one
          CALL QFCLOS ( FOUT, KEEP )
          OPNFLG = 1
        END IF
      END IF
C             
      IF (OPNFLG .EQ. 1) THEN
C       open the file
        CALL QFOPFN ( MESSFL, SCLU, SGRP, NEWFIL, FIXYES,
     O                FOUT, RETC )
        IF (RETC .NE. 0) FOUT = 0
      END IF
C
      RETURN
      END
