subroutine KINSEL(MAXSEL,KOUNT,NSEL,SELECT)
! Purpose: To determine the parameters of a kinetic plot command
! Subroutines required: KINNUM
! Revised 27-DEC-85 (LAB); Revised 10/25/88 (LAB) -- run-time formats for
! implementation-dependent cursor control.
! Revised 10/26/88 to unify command abort style to "quit"
! Converted to Fortran90 2/20/96; 6/17/96
use Implementation_Control; use Input_Output
Implicit None
real :: RESULT
integer :: NSEL,SELECT(7),IFLAG,I,J,N,KOUNT,M,MAXSEL
! NSEL=0 Original version, with NSEL=0, let user choose abscissa as first
! selection; this caused more confusion than it was worth. Thus,
SELECT(1) = 1 ! Force time to abscissa
NSEL = 1
call Help_message_one
Query_one: do
   write (stdout,fmt='(/A)',advance='NO') ' Parameter-> '
   call KINNUM (IFLAG,RESULT)
   select case (IFLAG)
      case (1,4) ! request for help or null imput
         call Help_message_one
         cycle Query_one
   case (2,5) ! Quit requested
      write (stdout,fmt='(A)') ' PLOT cancelled.'
      NSEL = 0
      return
   case (3)
      write (stdout,fmt='(//A)') ' Unrecognized response.'
      cycle Query_one
   case (6) ! proper numerical response
      I = int(RESULT)
      if (I == 0) exit Query_one
      if (I<1 .or. I>6) then
      write (stdout,fmt='(/A,I3,A)') ' Parameter ',I,' is out-of-range.'
      cycle Query_one
      end if
      ! Map the user input to match the position in the input record
      J = I+1
      if (J == 5 .or. J == 6) J = J-1
      if (I == 3) J = 6
      I = J
      NSEL = NSEL+1
      SELECT(NSEL) = I
   end select
end do Query_one
J = 1
call Help_message_two
Query_two: do
   if (J == 1) write (stdout,fmt='(/A)',advance='NO')&
      ' Enter segment number---> '
   if (J == 2) write (stdout,fmt='(A)',advance='NO')&
      ' Enter parameter number-> '
   call KINNUM (IFLAG,RESULT)
   select case (IFLAG)
   case (1,4) ! request for help or null input
      call Help_message_two
      cycle Query_two
   case (2,5) ! QUIT or eof
      write (stdout, fmt='(/A)') ' PLOT cancelled.'
      NSEL = 0
      return
   case (3)
      write (stdout,fmt='(/A)') ' Unrecognized response.'
      cycle Query_two
   case (6) ! proper numerical response
      I = int(RESULT)
      if (I == 0) return
      if (J==1) then
         N = I
         if (N<1 .or. N>KOUNT) then
            write (stdout,fmt='(/A,I3,A)')&
               ' Segment number ',N,' is out-of-range.'
            cycle Query_two
         end if
      else
         M = I
         if (M<1 .or. M>5) then
            write (stdout,fmt='(/A,I3,A)')&
               ' Parameter ',M,' is out-of-range.'
            cycle Query_two
         end if
      end if
      J = J+1
      if (J == 2) cycle Query_two
      I = 7+(N-1)*5+M
      NSEL = NSEL+1
      SELECT(NSEL) = I
      J = 1
      cycle Query_two
   end select
end do Query_two
return
contains
Subroutine Help_message_one
   write (stdout,fmt='(/2(/A)/6(/A)//A/A)')&
   ' The following parameters are available for time-trace plotting',&
   ' of values averaged over the ecosystem space:',&
   ' 1 - Water Column: average dissolved  (mg/L)',&
   ' 2 -               average sorbed     (mg/kg)',&
   ' 3 -               total mass         (kg)',&
   ' 4 - Benthic:      average dissolved  (mg/L)',&
   ' 5                 average sorbed     (mg/kg)',&
   ' 6                 total mass         (kg)',&
   ' Enter parameters, one per line;',&
   ' enter "0" to end data entry and proceed.'
end Subroutine Help_message_one
Subroutine Help_message_two
   write (stdout,fmt='(//A/5(A/)//A/A)')&
   ' The following parameters are available for each segment:'       ,&
   ' 1 -  Total concentration   (Water Column, mg/L; benthic, mg/kg)',&
   ' 2 -  Dissolved             (mg/liter of fluid volume)'          ,&
   ' 3 -  Sorbed                (mg/kg of sediment)'                 ,&
   ' 4 -  Biosorbed             (ug/g)'                              ,&
   ' 5 -  Mass                  (grams/square meter of AREA)'        ,&
   ' Enter segment-parameter number pair, one number per line;'      ,&
   ' enter 0 when data entry is complete; or Quit to cancel.'
end Subroutine Help_message_two
end subroutine KINSEL
