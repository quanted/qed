subroutine STORE()
! Purpose--to store the current environment, chemical, load, or product 
! in the UDB direct access file
! Subroutines required--DECOD1, DECOD2, DECOD4, IMBED, INREC,
! PAK, PAKENV, PACLDS, PACPRO
! Revised 27-DEC-85, 22-APR-87 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Revised 11/17/88 to accommodate VAX multi-user environment
use Input_Output
use Global_Variables
use Local_Working_Space
use Implementation_Control
Implicit None
real :: RESULT
integer :: CC,EOF,WHICH,KT,IREC,II,J,IMBED,NUSED
character(len=1) :: CBUFF(VARCEC)
character(len=50) :: TEMP
call DECOD1 (1,WHICH,CC,RESULT)
if (CC > 1) return
KT = 1
if (MCHEMG > 1) KT = MCHEMG
IREC = int(RESULT)
if (WHICH < 2) then
   call DECOD4 (1,IREC,KT,KCHEM,CC)
   if (CC > 1) return
endif
call DECOD2 (IREC,CC,WHICH,II,CBUFF)
if (CC == 3) return

Record_in_use: if (CC == 1) then ! tell user and ask for instructions
do J = 1, 50
   TEMP(J:J) = CBUFF(J)
end do
write (stdout,fmt='(/,A,I3,A,/,A,/,/,A)',Advance='NO')&
   ' Record ',IREC,' is in use with',' '//trim(TEMP),' Replace?-> '
call INREC (EOF,stdin)
if (EOF == 1) then
   call It_died (4)
   return
endif
START = IMBED(INPUT,0)
if (START == -999) then
   call It_died (0) ! blank response
   return
endif
if (INPUT(START:START) /= 'Y' .and. INPUT(START:START) /= 'y') then
   call It_died (0) ! user requested cancellation of command
   return
endif

! User wants to store in an active slot. Check on password protection.
NUSED = 50  ! skip characters used for title
do J = 1, 6 ! Read password for privilege to write on this record
   WPASS(WHICH)(J:J) = CBUFF(NUSED+2)
   NUSED = NUSED+2
end do
Protected: if (WPASS(WHICH) /= 'GLOBAL') then     ! Entry is write-protected,
   write (stdout,fmt='(/A,/A)',Advance='No')&     ! solicit password
   " This entry is protected from unauthorized revision.",&
   " Please enter the Store Access Password-> "
   call INREC (EOF,stdin)
   if (EOF == 1) then
     call It_died (5)
     return
   endif
   START = IMBED(INPUT,0)
   if (START == -999) then
     call It_died (0) ! blank input
     return
   endif
   if (INPUT(START:START+5) /= WPASS(WHICH) .and. &
       INPUT(START:START+5)/= SYSPAS) then  ! password invalid
      call It_died (6)
      return
   end if
end if Protected
end if Record_in_use

! Record not in use or authorized revision, store the data. Note the fail-
! safe technique of storing and then re-reading for report
select case (WHICH)
case (1) ! chemical
   if (len_trim(CHEMNA(KT)) == 0) then
      call It_died (7)
      return
   else
      call PAK (IREC,KT)                  ! Store the data
      read (RANUNT,rec=II) CBUFF  ! Read what was stored
      do J = 1, 50
         TEMP(J:J) = CBUFF(J)             ! Load the result of the read
      end do                              ! And report to the user
      write (stdout,fmt='(/A)')&
         ' Chemical stored: "'//trim(TEMP)//'"'
   end if
case (2) ! environment
   if (len_trim(ECONAM) == 0) then
      call It_died (8)
      return
   elseif (KOUNT>NPX) then
      call It_died(9)
      return
   else
      call PAKENV (IREC)          ! Store the data
      read (RANUNT,rec=II) CBUFF  ! Read what was stored
      do J = 1, 50
         TEMP(J:J) = CBUFF(J)             ! Load the result of the read
      end do                              ! And report to the user
      write (stdout,fmt='(/A)')&
         ' Environment stored: "'//trim(TEMP)//'"'
   end if
case (3) ! loadings
   if (len_trim(LOADNM) == 0) then
      call It_died(1) ! advise the user
      return          ! and abort the operation
   elseif (KOUNT>NPX) then
      call It_died(10)
      return
   elseif (KCHEM>NCHEM) then
      call It_died(11)
      return
   else
      call PACLDS (IREC)
      read (RANUNT,rec=II) CBUFF
      do J = 1, 50
         TEMP(J:J) = CBUFF(J)
      end do
      write (stdout,fmt='(/A)') ' Load stored: "'//trim(TEMP)//'"'
   end if
case (4)
   if (len_trim(PRODNM) == 0) then
      call It_died(2) ! advise the user
      return          ! and abort the operation
   else
      call PACPRO (IREC)
      read (RANUNT,rec=II) CBUFF
      do J = 1, 50
         TEMP(J:J) = CBUFF(J)
      end do
      write (stdout,fmt='(/A)') ' Product stored: "'//trim(TEMP)//'"'
   end if
case default
   ! WHICH has an improper value -- write fail-safe message
   call It_died(3)                ! that STORE failed
end select
! End of store operation, return to EXAMS prompt
return

contains
Subroutine It_died(how)
integer, intent (in) :: how ! it died, i.e., select detail for the user
How_it_died: select case (how)
case (0)
! no message
case (1)
   write (stdout,fmt='(/A,/A)')&
      ' You must NAME the allochthonous loadings dataset before STORE can',&
      ' enter the data into the UDB catalog.'
case (2)
   write (stdout,fmt='(/A,/A)')&
      ' You must NAME the product chemistry dataset before STORE can',&
      ' enter the data into the UDB catalog.'
case (3)
   write (stdout,fmt='(/A)') ' Command failed; please try again.'
case (4)
   write (stdout,fmt='(/A)') ' End-of-File mark in input.'
case (5) ! end of file while reading password; emit empty report
   write (stdout,fmt='()')
case (6)
   write (stdout,fmt='(/A)')&
      ' Password is incorrect.'
case (7)
   write (stdout,fmt='(/A,/A)')&
      ' You must NAME the chemical before STORE can',&
      ' enter the data into the UDB catalog.'
case (8)
   write (stdout,fmt='(/A,/A)')&
      ' You must NAME the environment before STORE can',&
      ' enter the data into the UDB catalog.'
case (9)
   write (stdout,fmt='(a,i0,a/a,i0,a/a)')&
      " Exams' database can store environments of up to ",NPX,' segments.',&
      ' This environment, with its ',KOUNT,' segments, must be stored',&
      ' in a separate file using the "Write" command.'
case (10)
   write (stdout,fmt='(a,i0,a/a,i0,a/a)')&
      " Exams' database can store loadings for up to ",NPX,' segments.',&
      ' This load pattern, with its ',KOUNT,' segments, must be stored',&
      ' in a separate file using the "Write" command.'
case (11)
   write (stdout,fmt='(a,i0,a/a,i0,a/a)')&
      " Exams' database can store loadings for up to ",NCHEM,' chemicals.',&
      ' This load pattern, with its ',KCHEM,' chemicals, must be stored',&
      ' in a separate file using the "Write" command.'
end select How_it_died
write (stdout,fmt='(/A)') ' The STORE command has been cancelled.'
end Subroutine It_died

end subroutine STORE
