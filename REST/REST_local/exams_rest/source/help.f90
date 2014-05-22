subroutine HELP(OPTION)
! Purpose: to provide online assistance to the user.
! Implements the "HELP" and "DESCRIBE" commands.
! Revised 25-DEC-1985, 22-APR-87 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Input_Output
use Initial_sizes
use Model_Parameters
use Help_Text_Space
use MultiScan
Implicit None
! VARIEC, VARCEC, and FILDAT are Fortran parameters
integer :: IBUFF(VARIEC), OPTION, IPRT
! INTEGER OFFSET, TRECS, IRECS, NRECS, NINTS, SKIP, UP
integer :: HELEN(MAXHLP), MINHLP(MAXHLP), EOF, RECDAT(FILDAT), HRECS
! RECDAT carries the file information
! HRECS is the number of header records required.
integer :: NEXT,M,I,L,INSAVE,IMBED,INDX,IN,NOHELP,NN,MATCH,N1,N2
integer :: LENT,J,IM,II,IOFF,NCHAR,K
character(len=1) :: CBUFF(VARCEC),HELPS(MAXINI),CIM,BUFFER(VARCEC)
character(len=4) ::  TEMP
character(len=1), dimension(1), parameter :: BLANK = ' '
call READSP ! Read the data from the disk file
IPRT = 0
NEXT = 0
HRECS = FILDAT/VARIEC   ! Read the header record for file control information
if (FILDAT-VARIEC*HRECS /= 0) HRECS = HRECS+1
M = 0
Outer: do I = 1, HRECS
   read (RANUNT,rec=I) IBUFF
   Inner: do L = 1, VARIEC
      M = M+1
      if (M > FILDAT) exit Outer
      RECDAT(M) = IBUFF(L)
   end do Inner
end do Outer
INSAVE = RECDAT(3)-1
! VARIEC = RECDAT(14)
Query_loop: do ! Search for start of help keyword or name of input datum
   START = IMBED(INPUT,STOPIT)
   if (START /= -999) exit Query_loop
   ! Null input, so
   INDX = 1
   ! When OPTION is 0, the request is a base HELP
   if (OPTION == 0) then
      call Emit_help_text (stdout, RANUNT, IBUFF, CBUFF)
      return
   end if
   ! Solicit system parameter name -- Option = 1 (DESCRIBE command).
   write (stdout,fmt='(A)',advance='NO')&
      ' Enter name of input parameter-> '
   call INREC (EOF,stdin)
   if (EOF == 1) then
      write (stdout,fmt='(/A)') ' End-of-file encountered.'
      return
   end if
   STOPIT = 0
end do Query_loop
! look for the end of the keyword or system parameter name
call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
if (TYPE == 100) STOPIT = Key_Buffer+1
! process selected option
if (OPTION /= 1) then
   ! try to match the keyword against the list of available keywords
   ! retrieve the keyword table from the disk file
   IN = RECDAT(1)-1
   call UNPREC(IN,HELEN,NOHELP,MAXHLP)
   call UNPREC(IN,MINHLP,NOHELP,MAXHLP)
   IN = IN+1
   read (RANUNT,rec=IN) BUFFER
   do I = 1, 4
      TEMP(I:I) = BUFFER(I)
   end do
   read (TEMP,fmt='(I4)') NN
   L = 4
   M = 0
   do I = 1, NN
      L = L+1
      if (L > VARCEC) then
         IN = IN+1
         read (RANUNT,rec=IN) BUFFER
         L = 1
      endif
      M = M+1
      HELPS(M) = BUFFER(L)
   end do
   INDX = MATCH(NOHELP,MAXINI,HELEN,HELPS,MINHLP)
   INSAVE = IN
   if (INDX /= 0) then
      call Emit_help_text (stdout, RANUNT, IBUFF, CBUFF)
      return
   end if
end if
! common area for options 0 and 1, testing for a system parameter name
INDX = MATCH(NOMOD,LNMODS,MODLEN,MODS,MODMIN)
INSAVE = IN
if (INDX == 0) then
   write (stdout,fmt='(/A)')&
      ' No information available for this request.'
   return
end if
if (TD(INDX) == 0) then
   write (stdout,fmt='(/A)')&
      ' No information available for this COMMON name.'
   return
end if
NEXT = 1
! get the full name from the table
N1 = 0
N2 = INDX-1
do I = 1, N2
   N1 = N1+MODLEN(I)
end do
LENT = MODLEN(INDX)
N2 = N1+LENT
N1 = N1+1
! don't print last letter; it is a "G"
if (MODS(N2) == 'G') then
   N2 = N2-1
   LENT = LENT-1
endif
call DESOUT (INDX,MODS(N1),LENT,stdout)
if (OPTION == 1) return
call Emit_help_text (stdout, RANUNT, IBUFF, CBUFF)
return
contains
subroutine Emit_help_text (TTYOUT, READLUN, IBUFF, CBUFF)
   integer :: TTYOUT, READLUN
   integer, dimension (:) :: IBUFF
   character(len=1), dimension (:) :: CBUFF
   IN = INSAVE
   if (OPTION==1 .or. NEXT==1) IN = RECDAT(7)-1
   I = VARIEC/3
   J = INDX/I
   if (J*I-INDX /= 0) J = J+1
   IN = IN+J
   read (readlun,rec=IN) IBUFF ! read the pointer record
   IM = INDX-(J-1)*I
   IM = (IM-1)*3+1
   II = IBUFF(IM)
   IOFF = IBUFF(IM+1)-1
   NCHAR = IBUFF(IM+2)
   read (readlun,rec=II) CBUFF ! read text record
   K = 0
   do I = 1, NCHAR
      IOFF = IOFF+1
      if (IOFF > VARCEC) then
         II = II+1
         read (readlun,rec=II) CBUFF ! read next text record
         IOFF = 1
      endif
      CIM = CBUFF(IOFF)
      if (CIM /= '$') then
         K = K+1
         INPUT(K:K) = CIM
         cycle
      end if
      if (K == 0) cycle
      if (K == 1 .and. INPUT(1:1) == ' ') cycle
      write (ttyout,fmt='(1X,A)') INPUT(1:K)
      IPRT = 1
      K = 0
   end do
   if (IPRT == 0) write (ttyout,fmt='(/A)')&
      ' No information for this variable.'
   end subroutine Emit_help_text
end subroutine HELP
