Module I_errchk
   Interface

      Subroutine errchk (IERROR, MESAGE, FATAL)
         Integer, Intent(IN) :: IERROR
         Character (LEN = 80), Intent(INOUT) :: MESAGE
         Logical, Intent(IN) :: FATAL

         !VAST.../TRACE/ SUBLVL(IN)
         !VAST.../TRACHR/ OUTSTR(IN)
         !VAST.../ECHOIT/ ECHOLV(INOUT)
         !VAST.../FILEX/ FECHO(IN)
         !VAST...Calls: PZSCRN, TRCLIN, LFTJUS, FILCLO
         !...This routine performs I/O.

      End Subroutine errchk
   End Interface
End Module I_errchk
