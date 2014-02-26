subroutine ERASE
! Purpose: to erase a selected environment, chemical, load, or product.
! Revised 25-DEC-85 (LAB)
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Input_Output
use Initial_Sizes
Implicit None
real :: RESULT
integer :: CC,WHICH,IREC,II,NUSED,J,I,IMBED,EOF
character(len=1), dimension(VARCEC) :: CBUFF
character(len=12), dimension(4) :: Message_text = &
(/' Chemical   ',  ' Environment',  ' Load       ',  ' Product    '/)
call DECOD1 (3,WHICH,CC,RESULT); if (CC > 1) return
IREC = int(RESULT)
call DECOD2 (IREC,CC,WHICH,II,CBUFF); if (CC == 3) return
read (RANUNT,rec=II) CBUFF    ! Read passwords
NUSED = 50  ! Skip over name of entry
do J = 1, 6 ! Read password for privilege to write on this record
   WPASS(WHICH)(J:J) = CBUFF(NUSED+2)
   NUSED = NUSED+2
end do
Protected: if (WPASS(WHICH) /= 'GLOBAL') then ! Entry is write-protected
   write (stdout,fmt='(A/A)',advance='NO')&   ! solicit password
      ' This entry is protected from unauthorized erasure.',&
      ' Please enter the Store Access Password-> '
   call INREC (EOF,stdin)
   if (EOF == 1) then
      write (stdout,fmt='(A)') ' ERASE command cancelled.'
      return
   endif
   START = IMBED(INPUT,0)
   if (START == -999) then  ! all blank input
      write (stdout,fmt='(A)') ' ERASE command cancelled.'
      return
   endif
   if(INPUT(START:START+5)/=WPASS(WHICH) .and. INPUT(START:START+5)/=SYSPAS)&
      then; write (stdout,fmt='(A/A)')&
         ' Password does not match. Please check your records;',&
         ' The ERASure has been cancelled.'
      return
   end if
end if Protected
CBUFF = ' ' ! Erasure consists of blanking the name field; all further access
NUSED = 50  ! is thereby denied until the entire entry is re-written.
RPASS(WHICH) = 'GLOBAL' ! In addition, the passwords are cleared
WPASS(WHICH) = 'GLOBAL' ! for global access.
do I = 1, 6
   CBUFF(NUSED+1) = RPASS(WHICH)(I:I)
   CBUFF(NUSED+2) = WPASS(WHICH)(I:I)
NUSED = NUSED+2
end do
write (RANUNT,rec=II) CBUFF
write (stdout, fmt='(/A,I5,A/A)')&
   trim(Message_text(WHICH))//' ',IREC,' erased.',&
   ' Password protections for this entry have been removed.'
end subroutine ERASE
