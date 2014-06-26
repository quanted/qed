subroutine RECALL ! Purpose: to recall previously STOREd chemicals,
                  ! environments, loads, and products.
! Revised 25-DEC-85, 22-APR-87 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
Implicit None
real :: RESULT
integer :: WHICH,CC,EOF,IREC,II,J,IMBED
integer :: Next_CBUFF
character :: CBUFF(VARCEC)
character (len=50) :: NAME
call DECOD1 (2,WHICH,CC,RESULT) ! if CC=1, all is well
if (CC > 1) return ! i.e., if end-of-file or Quit requested, return
IREC = int(RESULT)
Get_chemical: if (WHICH == 1) then ! chemical UDB is target
call DECOD4 (2,IREC,MCHEMG,KCHEM,CC)
   Not_good: if (CC > 1) then ! when CC=1, all is well--if not so, then
      call Reset_Passwords (RPASS,WPASS)
      write (stderr,fmt='(A)') ' RECALL command cancelled.'
      return
   end if Not_good
end if Get_chemical

call DECOD2 (IREC,CC,WHICH,II,CBUFF)
error: select case (CC) ! possible error returns--again CC=1 signals all O.K.
case (3) error ! record number exceeds permitted range
   call Reset_passwords (RPASS,WPASS)
   return
case (2) error ! Record not defined
   write (stderr,fmt='(/A/A)')&
      ' No entry in the catalog at this location.',&
      ' RECALL command cancelled.'
   call Reset_passwords (RPASS,WPASS)
   return
end select error

read (RANUNT,rec=II) CBUFF ! Read name and passwords
do J = 1, 50
   NAME(J:J) = CBUFF(J)
end do
Next_CBUFF = 51
do J = 1, 6
   RPASS(WHICH)(J:J) = CBUFF(Next_CBUFF)
   Next_CBUFF = Next_CBUFF+2
end do

if (RPASS(WHICH) == 'GLOBAL') then
   select case (WHICH) ! Get the Chemical, Environment, Load, or Product
      case (1)         ! record and print the name that is on the record
         call UNPAK (IREC,MCHEMG)
         IRUN = 0 ! prevent "continue" until "run" has been executed
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected compound is "'//trim(NAME)//'"'
      case (2)
         call UNPENV (IREC)
         IRUN = 0 ! prevent "continue" until "run" has been executed
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected environment is "'//trim(NAME)//'"'
      case (3)
         call UNPLDS (IREC)
         if (echo) write (stdout,fmt='(/A)')&
           ' Selected load is "'//trim(NAME)//'"'
      case (4)
         call UNPPRO (IREC)
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected product is "'//trim(NAME)//'"'
   end select
   call Reset_passwords (RPASS,WPASS)
   return
end if

write (stderr,fmt='(A/A)',advance='NO')& ! Entry is read protected,
   ' This entry is protected from unauthorized access.',& ! so
   ' Please enter the Recall Access Password-> '        ! solicit password
call INREC (EOF,stdin)
if (EOF == 1) then
   ! end-of-file reading password...message is intentionally obtuse
   write (stderr,fmt='(A)') ' RECALL command cancelled.'
   call Reset_passwords (RPASS,WPASS)
   return
endif

START = IMBED(INPUT,0)
if (START == -999) then ! If input is all blanks, cancel operation
   write (stderr,fmt='(A)') ' RECALL command cancelled.'
   call Reset_passwords (RPASS,WPASS)
   return
endif

if (INPUT(START:START+5) == RPASS(WHICH)&
   .or. INPUT(START:START+5)== SYSPAS) then
   select case (WHICH) ! Get the Chemical, Environment, Load, or Product
      case (1)         ! record and print the name that is on the record
         call UNPAK (IREC,MCHEMG)
         IRUN = 0 ! prevent "continue" until "run" has been executed
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected compound is "'//trim(NAME)//'"'
      case (2)
         call UNPENV (IREC)
         IRUN = 0 ! prevent "continue" until "run" has been executed
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected environment is "'//trim(NAME)//'"'
      case (3)
         call UNPLDS (IREC)
         if (echo) write (stdout,fmt='(/A)')&
           ' Selected load is "'//trim(NAME)//'"'
      case (4)
         call UNPPRO (IREC)
         if (echo) write (stdout,fmt='(/A)')&
            ' Selected product is "'//trim(NAME)//'"'
   end select
   call Reset_passwords (RPASS,WPASS)
else
   write (stderr,fmt='(A/A)')&
      ' Password does not match.',&
      ' RECALL command cancelled.'
   call Reset_passwords (RPASS,WPASS)
end if
return ! for clarity of exposition...this ends the routine, so
       ! it returns at this point anyway
end subroutine RECALL

Subroutine Reset_Passwords (RPASS,WPASS)
character(len=6), dimension(4) :: RPASS, WPASS
! Reset the password field to default value
RPASS = 'GLOBAL'
WPASS = 'GLOBAL'
return
end Subroutine Reset_Passwords
