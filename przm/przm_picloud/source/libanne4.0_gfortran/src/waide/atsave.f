C
C
C
      SUBROUTINE   SVATR1
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME, ATTR1,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the array of attributes in attribute attr for each of
C     the data sets in dsn.  An error message is written to file
C     unit OT for each attribute that was not successfully added
C     to a data set.  If sclu > 0, an error message is written to
C     the screen for the first 100 data sets that had problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX, RTCMND
      REAL        ATTR1(CNTDSN)
      CHARACTER*6 ATNAME
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attributes
C     INDEX  - index number of attribute
C     ATNAME - name of attribute
C     ATTR1  - attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN2, RETCNT, RETC1, REPORT(2,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RETC1  - return code
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAR
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', F10.2,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN2
     $     /    1,    2 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attributes to data set
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX, LEN1, ATTR1(I),
     O                RETC1 )
        IF (RETC1 .NE. 0) THEN
C         problem putting attributes on wdm 
          WRITE (OT,2000) DSN(I), INDEX, ATNAME, ATTR1(I), RETC1
          IF (RETCNT .LT. MAXCNT) THEN
            RETCNT = RETCNT + 1
            REPORT(1,RETCNT) = DSN(I)
            REPORT(2,RETCNT) = RETC1
          END IF
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN2, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATR2
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME, ATTR1, ATTR2,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the 2 arrays of attributes in attributes index(1) and index(2)
C     for each of the data sets in dsn.  An error message is written
C     to file unit OT for each attribute that was not successfully
C     added to a data set.  If sclu > 0, an error message is written to
C     the screen for the first 100 data sets that had problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX(2), RTCMND
      REAL        ATTR1(CNTDSN), ATTR2(CNTDSN)
      CHARACTER*6 ATNAME(2)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit nuber for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attributes
C     INDEX  - array of attribute index numbers
C     ATNAME - array of attribute names
C     ATTR1  - first attribute
C     ATTR2  - second attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN3, RETCNT, RETC1, RETC2, REPORT(3,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RET__  - return code for RETC1 and RETC2
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAR
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', F10.2,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN3
     $     /    1,    3 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attributes to data set
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX(1), LEN1, ATTR1(I),
     O                RETC1 )
        IF (RETC1 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(1), ATNAME(1), ATTR1(I), RETC1
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX(2), LEN1, ATTR2(I),
     O                RETC2 )
        IF (RETC2 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(2), ATNAME(2), ATTR2(I), RETC2
        IF (RETCNT .LT. MAXCNT  .AND.
     $     (RETC1 .NE. 0  .OR. RETC2 .NE. 0)) THEN
C         problem putting attributes on wdm 
          RETCNT = RETCNT + 1
          REPORT(1,RETCNT) = DSN(I)
          REPORT(2,RETCNT) = RETC1
          REPORT(3,RETCNT) = RETC2
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN3, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATR3
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME, ATTR1, ATTR2, ATTR3,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the 3 arrays of attributes in attributes index(1, 2, and 3)
C     for each of the data sets in dsn.  An error message is written
C     to file unit OT for each attribute that was not successfully
C     added to a data set.  If sclu > 0, an error message is written to
C     the screen for the first 100 data sets that had problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX(3), RTCMND
      REAL        ATTR1(CNTDSN), ATTR2(CNTDSN), ATTR3(CNTDSN)
      CHARACTER*6 ATNAME(3)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attributes
C     INDEX  - array of attribute index numbers
C     ATNAME - array of attribute names
C     ATTR1  - first attribute
C     ATTR2  - second attribute
C     ATTR3  - third attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN4, RETCNT, RETC1, RETC2, RETC3,
     $          REPORT(4,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RET__  - return code for RETC1 and RETC2
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAR
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', F10.2,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN4
     $     /    1,    4 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attributes to data set
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX(1), LEN1, ATTR1(I),
     O                RETC1 )
        IF (RETC1 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(1), ATNAME(1), ATTR1(I), RETC1
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX(2), LEN1, ATTR2(I),
     O                RETC2 )
        IF (RETC2 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(2), ATNAME(2), ATTR2(I), RETC2
        CALL WDBSAR ( WDMSFL, DSN(I), MESSFL, INDEX(3), LEN1, ATTR3(I),
     O                RETC3 )
        IF (RETC3 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(3), ATNAME(3), ATTR3(I), RETC3
        IF (RETCNT .LT. MAXCNT  .AND.
     $     (RETC1 .NE. 0  .OR.  RETC2 .NE. 0  .OR.  RETC3 .NE. 0)) THEN
C         problem putting attributes on wdm 
          RETCNT = RETCNT + 1
          REPORT(1,RETCNT) = DSN(I)
          REPORT(2,RETCNT) = RETC1
          REPORT(3,RETCNT) = RETC2
          REPORT(4,RETCNT) = RETC3
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN4, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATI2
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME, ATTR1, ATTR2,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the 4 arrays of attributes in attributes index(1), index(2),
C     index(3), and index(4) for each of the data sets in dsn.  An error
C     message is written to file unit OT for each attribute that was
C     not successfully added to a data set.If sclu > 0, an error message
C     is written to the screen for the first 100 data sets that had
C     problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX(2), RTCMND, ATTR1(CNTDSN), ATTR2(CNTDSN)
      CHARACTER*6 ATNAME(2)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attributes
C     INDEX  - array of attribute index numbers
C     ATNAME - array of attribute names
C     ATTR1  - first attribute
C     ATTR2  - second attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN3, RETCNT, RETC1, RETC2, REPORT(3,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RETC_  - return code for RETC1, RETC2, RETC3, and RETC4
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAI
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', I10,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN3
     $     /    1,    3 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attributes to data set
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(1), LEN1, ATTR1(I),
     O                RETC1 )
        IF (RETC1 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(1), ATNAME(1), ATTR1(I), RETC1
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(2), LEN1, ATTR2(I),
     O                RETC2 )
        IF (RETC2 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(2), ATNAME(2), ATTR2(I), RETC2
        IF (RETCNT .LT. MAXCNT  .AND.
     $     (RETC1 .NE. 0  .OR.  RETC2 .NE. 0)) THEN
C         problem putting attributes on wdm 
          RETCNT = RETCNT + 1
          REPORT(1,RETCNT) = DSN(I)
          REPORT(2,RETCNT) = RETC1
          REPORT(3,RETCNT) = RETC2
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN3, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATI4
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME, ATTR1, ATTR2, ATTR3, ATTR4,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the 4 arrays of attributes in attributes index(1), index(2),
C     index(3), and index(4) for each of the data sets in dsn.  An error
C     message is written to file unit OT for each attribute that was
C     not successfully added to a data set.  If sclu > 0, an error message
C     is written to the screen for the first 100 data sets that had
C     problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX(4), RTCMND, ATTR1(CNTDSN), ATTR2(CNTDSN),
     $            ATTR3(CNTDSN), ATTR4(CNTDSN)
      CHARACTER*6 ATNAME(4)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attributes
C     INDEX  - array of attribute index numbers
C     ATNAME - array of attribute names
C     ATTR1  - first attribute
C     ATTR2  - second attribute
C     ATTR3  - third attribute
C     ATTR4  - fourth attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN5, RETCNT, RETC1, RETC2, RETC3, RETC4,
     $          REPORT(5,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RETC_  - return code for RETC1, RETC2, RETC3, and RETC4
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAI
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', I10,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN5
     $     /    1,    5 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attributes to data set
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(1), LEN1, ATTR1(I),
     O                RETC1 )
        IF (RETC1 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(1), ATNAME(1), ATTR1(I), RETC1
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(2), LEN1, ATTR2(I),
     O                RETC2 )
        IF (RETC2 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(2), ATNAME(2), ATTR2(I), RETC2
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(3), LEN1, ATTR3(I),
     O                RETC3 )
        IF (RETC3 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(3), ATNAME(3), ATTR3(I), RETC3
        CALL WDBSAI ( WDMSFL, DSN(I), MESSFL, INDEX(4), LEN1, ATTR4(I),
     O                RETC4 )
        IF (RETC4 .NE. 0)
     $    WRITE (OT,2000) DSN(I), INDEX(4), ATNAME(4), ATTR4(I), RETC4
        IF (RETCNT .LT. MAXCNT  .AND.
     $     (RETC1 .NE. 0  .OR.  RETC2 .NE. 0   .OR.
     $      RETC3 .NE. 0  .OR.  RETC4 .NE. 0)) THEN
C         problem putting attributes on wdm 
          RETCNT = RETCNT + 1
          REPORT(1,RETCNT) = DSN(I)
          REPORT(2,RETCNT) = RETC1
          REPORT(3,RETCNT) = RETC2
          REPORT(4,RETCNT) = RETC3
          REPORT(5,RETCNT) = RETC4
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN5, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATC1
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN,
     I                      INDEX, ATNAME,  ATTR1, LENA,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     Saves the array of attributes in attribute attr for each of
C     the data sets in dsn.  An error message is written to file
C     unit OT for each attribute that was not successfully added
C     to a data set.  If sclu > 0, an error message is written to
C     the screen for the first 100 data sets that had problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTDSN, DSN(CNTDSN),
     $            INDEX, LENA, RTCMND
      CHARACTER*6 ATNAME
      CHARACTER*1 ATTR1(LENA,CNTDSN)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - >0 - message file cluster
C              =0 - no screen io
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of data sets
C     DSN    - array of data sets to save attribute
C     INDEX  - index number of attribute
C     ATNAME - name of attribute
C     ATTR1  - attribute
C     LENA   - length of attribute
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, J, LEN1, LEN2,
     $          RETCNT, RETC1, REPORT(2,MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RETC1  - return code
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAC
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6 )
 2001 FORMAT (   '         value =', 48A   )
 2002 FORMAT (   '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN2
     $     /    1,    2 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTDSN
C       save attribute to data set
        CALL WDBSAC ( WDMSFL, DSN(I), MESSFL,
     I                INDEX, LENA, ATTR1(1,I),
     O                RETC1 )
        IF (RETC1 .NE. 0) THEN
C         problem putting attributes on wdm 
          WRITE (OT,2000) DSN(I), INDEX, ATNAME
          WRITE (OT,2001) (ATTR1(J,I), J = 1, LENA)
          WRITE (OT,2002) RETC1
          IF (RETCNT .LT. MAXCNT) THEN
            RETCNT = RETCNT + 1
            REPORT(1,RETCNT) = DSN(I)
            REPORT(2,RETCNT) = RETC1
          END IF
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND.  SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN2, RETCNT, REPORT )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
C
C
C
      SUBROUTINE   SVATRM
     I                    ( MESSFL, SCLU, SGRP, WDMSFL, OT, CNTATR, DSN,
     I                      INDEX, ATNAME, ATTRM,
     O                      RTCMND )
C
C     + + + PURPOSE + + +
C     For dsn, saves the array attrm of attributes in attributes index.
C     An errir nessage is written to file unit OT for each attribute
C     that was not successfully added to a data set.  An error message
C     is written to the screen for the first 100 data sets that had
C     problems.
C
C     + + + DUMMY ARGUMENTS + + +
      INTEGER     MESSFL, SCLU, SGRP, WDMSFL, OT, CNTATR, DSN,
     $            INDEX(CNTATR), RTCMND
      REAL        ATTRM(CNTATR)
      CHARACTER*6 ATNAME(CNTATR)
C
C     + + + ARGUMENT DEFINITIONS + + +
C     MESSFL - Fortran unit number of message file
C     SCLU   - message file group number
C     SGRP   - message file cluster number
C     WDMSFL - Fortran unit number of wdm file
C     OT     - Fortran unit number for error messages
C     CNTDSN - number of attributes to be saved
C     DSN    - data set to save attributes in
C     INDEX  - array of attribute index numbers
C     ATNAME - array of attribute names
C     ATTRM  - array of attribute values
C     RTCMND - return code
C               0 - everything successful
C               1 - user responded Accept to error warning
C               2 - user responded Prev to error warning
C              -1 - user responded Oops to error warning
C
C     + + + PARAMETERS + + +
      INTEGER    MAXCNT
      PARAMETER  ( MAXCNT = 100 )
C
C     + + + LOCAL VARIABLES + + +
      INTEGER   I, LEN1, LEN2, LEN4, LEN6, IND1,
     $          RETCNT, RETC, REPORT(2,MAXCNT)
      CHARACTER*6 REPATN(MAXCNT)
C
C     + + + LOCAL DEFINITIONS + + +
C     RETC   - return code for RETC1 and RETC2
C                0 - successful
C              -81 - data set does not exist
C             -103 - no room on label for attribute
C             -104 - data present, can't update attribute
C             -105 - attribute not allowed for this type data set
C             -109 - incorrect real value for attribute
C
C     + + + EXTERNALS + + +
      EXTERNAL   WDBSAR
      EXTERNAL   Q2INIT, Q2SETI, Q2EDIT
C
C     + + + OUTPUT FORMATS + + +
 2000 FORMAT (   ' *** Error writing attribute to wdm file',
     $        /, '           dsn =', I10,
     $        /, '         index =', I10,
     $        /, '          name =', 4X,A6,
     $        /, '         value =', F10.2,
     $        /, '        retcod =', I10 )
C
C     + + + DATA INITIALIZATIONS + + +
      DATA   LEN1, LEN2, LEN4, LEN6, IND1
     $     /    1,    2,    4,    6,    1 /
C
C     + + + END SPECIFICATIONS + + +
C
      RETCNT = 0
      RTCMND = 0
      DO 100 I = 1, CNTATR
C       save attributes to data set
        CALL WDBSAR ( WDMSFL, DSN, MESSFL, INDEX(I), LEN1, ATTRM(I),
     O                RETC )
        IF (RETC .NE. 0) THEN
C         problem saving attribute value
          WRITE (OT,2000) DSN, INDEX(I), ATNAME(I), ATTRM(I), RETC
          IF (RETCNT .LT. MAXCNT) THEN
C           save info for screen message
            RETCNT = RETCNT + 1
            REPORT(1,RETCNT) = DSN
            REPORT(2,RETCNT) = RETC
            REPATN(RETCNT) = ATNAME(I)
          END IF
        END IF
 100  CONTINUE
C
      IF (RETCNT .GE. 1  .AND. SCLU .GT. 0) THEN
C       problem with attributes, warn user
        CALL Q2INIT ( MESSFL, SCLU, SGRP )
        CALL Q2SETI ( LEN2, RETCNT, REPORT )
        CALL Q2SCTF ( IND1, LEN6, RETCNT, REPATN )
        CALL Q2EDIT ( RETCNT, RTCMND )
      END IF
C
      RETURN
      END
