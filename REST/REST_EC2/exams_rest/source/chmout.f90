subroutine CHMOUT(LUNNUM)
! CHMOUT writes the contents of the ADB (chemical data) to the
! sequential file attached to LUN LUNNUM. (16-MAY-1985, LAB)
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revisions 07-April-2001 adding aquatic metabolism half-lives
! Revised 2004-05-17 to include biolysis study temperatures
use Implementation_Control
use Global_Variables
use Local_Working_Space
Implicit None
integer :: I, J, K
! I, J, are loop counters
! K carries parameter MCHEMG identifying the ADB target sector.
integer, intent(in) :: LUNNUM
K = MCHEMG
write (LUNNUM,fmt='(A)',err=5010) CHEMNA(K)
! Write out the data as needed:
! Flags to indicate which species occur:
write (LUNNUM,fmt='(7(I1,1X))') (SPFLGG(I,K),I=1,7)
! Seven species can occur. SPFLGG flags the chemical species
!SPFLGG  Species
!------  -------
! 1      SH3      neutral
! 2      SH4+     singly charged cation
! 3      SH5++    doubly charged cation
! 4      SH6+++   triply charged cation
! 5      SH2-     singly charged anion
! 6      SH=      doubly charged anion
! 7      S(3-)    triply charged anion
!-----------------------------------------------------------------------
! Chemical input data is read in via a loop, with loop increments
! controlled by SPFLGG. In this way, the input data can be loaded
! in blocks that contain data only for those species that actually
! exist; non-existent species do not require a block of null data.
! Write required basic data
write (LUNNUM,5000,err=5010) MWTG(K),KOCG(K),KOWG(K)
write (LUNNUM,5000,err=5010) MPG(K),HENRYG(K),EHENG(K),VAPRG(K),EVPRG(K)
Species: do J = 1, 7 ! loop on all species
if (SPFLGG(J,K) /= 1) cycle
write(LUNNUM,5000,err=5010) SOLG(J,K),ESOLG(J,K),KPSG(J,K),&
                            KPBG(J,K),KPDOCG(J,K)
if (J > 1) write (LUNNUM,5000,err=5010) PKG(J-1,K),EPKG(J-1,K),KIECG(J-1,K)
write (LUNNUM,5000,err=5010) (QYield(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (ABSORG(I,J,K),I=1,46)
write (LUNNUM,5000,err=5010) KDPG(J,K),RFLATG(J,K),LAMAXG(J,K)
write (LUNNUM,5000,err=5010) (KAHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (EAHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (KNHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (ENHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (KBHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (EBHG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (KOXG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (EOXG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (K1O2G(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (EK1O2G(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (KREDG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (EREDG(I,J,K),I=1,3)
write (LUNNUM,5000,err=5010) (KBACWG(I,J,K),I=1,4)
write (LUNNUM,5000,err=5010) (QTBAWG(I,J,K),I=1,4)
write (LUNNUM,5000,err=5010) (KBACSG(I,J,K),I=1,4)
write (LUNNUM,5000,err=5010) (QTBASG(I,J,K),I=1,4)
write (LUNNUM,5000,err=5010) (QTBTWG(I,J,K),I=1,4)
write (LUNNUM,5000,err=5010) (QTBTSG(I,J,K),I=1,4)
end do Species
! Write aerobic aquatic metabolism half-life and
! anaerobic aquatic metabolism half-life at the end of the chemical file
write (LUNNUM,5000,err=5010) AerMet(K), AnaerM(K)
return
5000  format (1PG10.4,7G10.4)
5010 write (stdout,fmt='(/A)') ' Error writing chemical file.',&
                               ' Check results before further use.'
return
end Subroutine CHMOUT
