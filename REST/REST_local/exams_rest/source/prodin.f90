subroutine PRODIN (LogUnit,Problem)
! Subroutine to read an external file of allochthonous chemical loadings
use Implementation_Control
use Global_Variables
Implicit None
integer :: SkipNames ! to skip records with the chemical names
integer :: I, KNT, IOError
integer, intent (in)  :: LogUnit ! Logical Unit Number for reading file
logical, intent (out) :: Problem
character (len=1) :: Skipper
Problem = .false.
read (LogUnit,fmt='(22x,I6)',IOSTAT=IOerror) SkipNames
if (IOError/=0) then
   Problem = .true.
   return
end if
do I = 1, skipnames
   read (LogUnit,fmt='(1A)',IOSTAT=IOerror) Skipper
   if (IOError/=0) then
      Problem = .true.
      return
   end if
end do
read (LogUnit,fmt='(30x,I6)',IOSTAT=IOerror) KNT
if (IOError/=0) then
   Problem = .true.
   return
end if
if (KNT==0) then
   write (stderr,fmt='(/A)') ' Warning: No data in the file.'
   Problem = .true.
   return
end if
! KNT is the number of pathways in the file
if (KNT>size(CHPARG)) then
   KNT=size(CHPARG)
   write (stderr,fmt='(A/A,I0,A)')&
      ' The file contains more transformation pathways than can be READ.',&
      ' Only the first ',KNT,' pathways will be acquired.'
end if
! skip column header documentation
read (LogUnit,fmt='(1A)',IOSTAT=IOError) Skipper
if (IOError/=0) then
   Problem = .true.
   return
end if
do I = 1, KNT
   read (LogUnit, fmt='(6x,4(1x,I5),1x,ES9.3,2x,ES9.3)',IOSTAT=IOError) &
      CHPARG(I), TPRODG(I), NPROCG(I), RFORMG(I), YIELDG(I), EAYLDG(I)
   if (IOError/=0) then
      Problem = .true.
      return
   end if
end do
return
end subroutine PRODIN
