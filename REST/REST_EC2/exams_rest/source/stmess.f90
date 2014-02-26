subroutine STMESS(IUNIT,NMESS,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
! Revised 23 July 1982 by L.A. Burns
! Revised 23 September 1982 for high precision operations.
! This subroutine contains the diagnostic messages of the
! stiff equation integrator.
Implicit None
real (kind (0D0)) :: TINIT,TFINAL,TINCR,RELERR,ABSERR,T
!integer IFLAG !(add to call list to restore)
integer :: IUNIT,NMESS,NEQN
Messages: select case (NMESS)
case (10) ! Start-up message
   write (IUNIT,fmt=&
      '(/,A,I5,A,/,A,1PG12.5,/,A,G12.5,/,A,G12.5,/,A,/,A,G12.5,A,G12.5)')&
      ' STFINT has been called to integrate',NEQN,' equations',&
      ' from initial time',TINIT,&
      ' to final time',TFINAL,&
      ' with output at steps of',TINCR,&
      ' and initial error tolerances of',&
      ' RELER =',RELERR,' and ABSER =',ABSERR
case (20) ! Illegal value of IFLAG
!   write (IUNIT,fmt='(/A,1PG12.5,/,A,/,A,/,A,I11)')&
   write (IUNIT,fmt='(/A,1PG12.5,/A/A)')&
      ' The program is terminated at T =',T,&
      ' because an unidentifiable error has caused',&
      ' STIFF to return with the illegal value of IFLAG.'
!      ' IFLAG =',IFLAG
case (30) ! IFLAG = 3
   write (IUNIT,fmt='(/,A,1PG12.5,A,/,2(A,/),A,G12.5,A,G12.5,/,A)')&
      ' *WARNING--at T =',T,', the error tolerances',&
      ' passed to STIFF were found to be too small for the',&
      ' machine precision. They have been increased to',&
      ' RELER =',RELERR,' and ABSER =',ABSERR,&
      ' to continue integration.'
case (40) ! IFLAG = 4
   write (IUNIT,fmt='(A,1PG12.5,A,/,A,/,A,/,A,G12.5,/,A,G12.5)')&
      ' *WARNING--at T =',T,', STIFF was unable to',&
      ' meet the requested error tolerances at the smallest',&
      ' allowable stepsize.  Integration is continuing with',&
      ' the tolerances increased to RELER =',RELERR,&
      ' and ABSER =',ABSERR
case (50) ! IFLAG = 5
   write (IUNIT,fmt='(A,1PG12.5,A,/,3(A,/))')&
      ' *WARNING--at T =',T,', the number of function',&
      ' calls exceeded the maximum number, MAXNFE, allowed',&
      ' by STIFF.  The function evaluation counter has been',&
      ' reduced by MAXNFE to allow integration to proceed.'
   write (IUNIT,fmt='(A,/,A,1PG12.5,A,G12.5)')&
      ' The error tolerances have been increased to',&
      ' RELER =',RELERR,' and ABSER =',ABSERR
case (60) ! IFLAG = 6
   write (IUNIT,fmt='(A,1PG12.5,A,/,3(A,/),2(A,G12.5))')&
      ' *WARNING--at T =',T,', the convergence test',&
      ' in GEAR could not be met at the smallest',&
      ' allowable stepsize. Integration is continuing',&
      ' with the error tolerances increased to',&
      ' RELER =',RELERR,' and ABSER =',ABSERR
case (70) ! IFLAG = 7
   write (IUNIT,fmt='(A,1PG12.5,A,/,6(A,/))')&
      ' *WARNING--at T =',T,', STIFF returned with an',&
      ' indication that this integration is unnecessarily',&
      ' costly because the requested output interval is',&
      ' substantially smaller than the natural stepsize.',&
      ' (Refer to program documentation for alternative approaches.)',&
      ' The output frequency monitor has been reset to allow integration',&
      ' to proceed.'
case (80) ! IFLAG = 8
   write (IUNIT,fmt='(/A,1PG12.5,/,4(A,/))')&
      ' The program is terminated at T =',T,&
      ' because a component of the solution',&
      ' vanished while ABSER = 0. It will be ',&
      ' necessary to provide a nonzero absolute ',&
      ' error tolerance to perform this integration.'
case (90) ! IFLAG = 9
   write (IUNIT,fmt='(/,A,1PG12.5,3(/,A),I11,/,3(A,G12.5,/),2(A,/))')&
      ' The program is terminated at T =',T,&
      ' because invalid input was received by STIFF.',&
      ' check the following parameters--',&
      '  NEQN =',NEQN,&
      ' RELER =',RELERR,&
      ' ABSER =',ABSERR,&
      ' TINCR =',TINCR,&
      ' Also, check that the output routine',&
      ' does not reset IFLAG to an illegal value.'
case (92) ! Too many error returns
   write (IUNIT,fmt='(A,1PG12.5,/,3(A,/))')&
      ' The integration has been truncated at time',T,&
      ' (hours), because STIFF has returned irregularly several times',&
      ' indicating extreme difficulty in the integration.',&
      ' Please check the accuracy of the problem statement.'
case (95) ! Integration complete
   write (IUNIT,fmt='(/,A,1PG12.5,/)') ' Integration complete at T = ',T
case default Messages
   write (IUNIT,fmt='(A)') ' Malfunction in Subroutine "STMESS."'
end select Messages
end Subroutine STMESS
