subroutine ADMESS(IUNIT,NMESS,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T,IFLAG)
! Revised 12 July 1982 by L.A. Burns
! This subroutine contains the diagnostic messages of the Adam integrator
Implicit None
real (kind (0D0)) :: TINIT,TFINAL,TINCR,RELERR,ABSERR,T
integer :: IUNIT,NMESS,NEQN,IFLAG
Messages: select case (NMESS)
case (10) ! Startup message
   write (IUNIT,fmt=&
      '(/,A,I5,A,/,A,1PG12.5,A,G12.5,/,A,G12.1,/,A,/,2(A,G12.5))')&
      ' ADMINT has been called to integrate ',NEQN,' equations',&
      ' from initial time',TINIT,' to final time',TFINAL,&
      ' with output at steps of ',TINCR,' and initial error tolerances of',&
      ' RELER = ',RELERR,' and ABSER = ',ABSERR
case (20) ! Successful completion
   write (IUNIT,fmt='(/,A,1PG12.5,/)') ' Integration complete at T = ',T
case (25) ! Illegal value of IFLAG
write (IUNIT,fmt='(/A,1PG12.5,/,A,/,A,I11)')&
   ' The integration terminated at T = ',T,&
   ' because an unidentifiable error indicated by',&
   ' an irregular return from ADAM with IFLAG = ',IFLAG
case (30) ! IFLAG = 3
   write (IUNIT,fmt='(A,1PG12.5,A,/,A,/,A,G12.5,A,G12.5,/,A,/)')&
      ' *WARNING--AT T =',T,', the error tolerances',&
      ' passed to ADAM were found to be too small for the',&
      ' machine precision. They have been increased to',&
      ' RELER =',RELERR,' and ABSER =',ABSERR,' to continue integration.'
case (40) ! IFLAG = 4
   write (IUNIT,fmt='(A,1PG12.5,A,/,A,/,A,/,A,G12.5,A,G12.5,/)')&
      ' *WARNING--AT T =',T,', ADAM was unable to',&
      ' meet the requested error tolerances at the smallest',&
      ' allowable stepsize. Integration is continuing with',&
      ' the tolerances increased to RELER =',RELERR,' and ABSER =',ABSERR
case (50) ! IFLAG = 5
   write (IUNIT,fmt='(A,1PG12.5,A,/,3(A,/))')&
      ' *WARNING--AT T =',T,', the number of function',&
      ' calls exceeded the maximum number, MAXNFE, allowed',&
      ' by ADAM. The function evaluation counter has been',&
      ' reduced by MAXNFE to allow integration to proceed.'
case (60) ! IFLAG = 6
   write (IUNIT,fmt='(A,1PG12.5,A,/,3(A,/))')&
      " *WARNING--AT T =",T," hours, stiffness has been detected",&
      " in the numerical integration. The simulation has",&
      " been transferred to the Gear's method algorithm",&
      " to allow integration to proceed."
case (70) ! IFLAG = 7
   write (IUNIT,fmt='(A,1PG12.5,A,/,6(A,/))')&
      ' *WARNING--AT T =',T,', ADAM returned with an',&
      ' indication that this integration is unnecessarily',&
      ' costly because the requested output interval is',&
      ' substantially smaller than the natural stepsize.',&
      ' (Refer to program documentation for alternative',&
      ' approaches.) The output frequency monitor has been',&
      ' reset to allow integration to proceed.'
case (80) ! IFLAG = 8
   write (IUNIT,fmt='(A,1PG12.5,/3(A,/))')&
      ' The program is terminated at T =',T,&
      ' because a component of the solution vanished while ABSER = 0.',&
      ' It will be necessary to provide a nonzero absolute error',&
      ' tolerance to perform this integration.'
case (90) ! IFLAG = 9
   write (IUNIT,fmt='(A,1PG12.5,/,2(A,/),A,I11,3(A,G12.5,/),A,/,A)')&
      ' The program is terminated at T =',T,&
      ' because invalid input was received by ADAM.',&
      ' Check the following parameters--',&
      ' NEQN =',NEQN,' RELER =',RELERR,' ABSER =',ABSERR,' TINCR =',TINCR,&
      ' Also, check that the output routine',&
      ' does not reset IFLAG to an illegal value.'
case (92)
   write (IUNIT,fmt='(A,1PG12.5,3(/A)/)')&
      ' The integration has been truncated at time',T,&
      ' (hours), because ADAM has returned irregularly several times,',&
      ' indicating extreme difficulty in the integration. Please check',&
      ' the accuracy of the problem statement.'
case default
   write (IUNIT,fmt='(A)')' Malfunction in Subroutine "ADMESS."'
end select Messages
end subroutine ADMESS
