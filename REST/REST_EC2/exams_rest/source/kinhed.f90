subroutine KINHED(EOF,CMPNAM,SYSNAM,KOUNT,TYPES,ICODE,MCHEMG)
! PURPOSE: To extract the chemical name, system name,
!  and number and types of segments.
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
Implicit None
integer :: EOF,ICODE,K,KCHEM,KOUNT,MCHEMG
character(len=50) :: CMPNAM, SYSNAM
character(len=1), dimension(KOUNT) :: TYPES
! Get: number of chemicals, mode, and number of segments
read (PLTLUN,end=120) KCHEM,K,KOUNT,ICODE ! K is dummy read
if (MCHEMG<1 .or. MCHEMG>KCHEM) then
   EOF=2
   return
end if
! Get the descriptors
do K = 1, KCHEM   ! First the chemical names
  if (K == MCHEMG) then
    read (PLTLUN,end=120) CMPNAM
  else
    read (PLTLUN,end=120) ! advance only
  endif
end do
read (PLTLUN,end=120) SYSNAM   ! Now the system name
read (PLTLUN,end=120) TYPES    ! Get the segment types
EOF = 0
return
120 continue
EOF = 1
return
end Subroutine KINHED
