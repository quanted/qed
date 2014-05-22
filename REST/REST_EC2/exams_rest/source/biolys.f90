subroutine BIOLYS(K2) ! Computes bacterial transformation kinetics
! Revised 12 July 1983 (LAB) for mode 3 operations.
! Revised 08-JUN-1984 (LAB) to separate bacterioplankton and benthic bacteria
! Revised 2004-05-17 (LAB) to specify the temperature of biolysis studies
!     (QTBTWG and QTBTSG)
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Floating_Point_Comparisons
Implicit None
real :: KBACWLocal, KBACSLocal, ACBACL, XMULTW, XMULTS ! Local variables
      ! KBACWLocal is biolysis rate constant in water column
      ! KBACSLocal is biolysis in bottom sediments
      ! ACBACL is actively degrading bacterial population
      ! XMULTW is set to 1 for water column segments, else zero.
      ! XMULTS is set to 1 for benthic segments, else zero.
integer :: J,I,II,K,KK ! loop counters
integer, intent (in) :: K2 ! ADB number of chemical
Segments: do J = 1, KOUNT
  Select case (TYPEG(J)) ! Set for Benthic or water column segment type
  case ("B") ! Benthic segment
    XMULTW = 0.0; XMULTS = 1.0
    ! For sediments,, convert bacterial populations (cfu/100 grams
    ! dry weight of sediment) to active cfu/mL of pore water:
    ACBACL = (BNBACG(J,NDAT)*SEDMSL(J))/(WATVOL(J)*100.0)
  case default ! not a sediment, thus a type of water column
    XMULTW = 1.0; XMULTS = 0.0
    ACBACL = BACPLG(J,NDAT) ! water column active bacteria (cfu/mL):
  End select
  II = -3 ! Initialize counter to map onto ALPHA matrix:
  Ions: do K = 1, 7 ! Ionic species loop
    II = II+1 ! Increment ALPHA map
    if (SPFLGG(K,K2) == 0) cycle Ions
    Forms: do I = 1, 4 ! Loop on dissolved, sorbed, etc. forms:
      KK = 3*K+II+I-1
      KBACWLocal = KBACWL(I,K,K2)  ! Load global (input) value of
      KBACSLocal = KBACSL(I,K,K2)  ! bacterial biolysis rate constants
      if (QTBAWG(I,K,K2) .NotEqual. 0.0)& ! adjust for temperature
        KBACWLocal=KBACWL(I,K,K2)*QTBAWG(I,K,K2)**&
         ((TCELG(J,NDAT)-QTBTWG(I,K,K2))/10.0)
      if (QTBASG(I,K,K2) .NotEqual. 0.0)& ! adjust for temperature
        KBACSLocal=KBACSL(I,K,K2)*QTBASG(I,K,K2)**&
         ((TCELG(J,NDAT)-QTBTSG(I,K,K2))/10.0)
      ! Add current contribution to total rate constants:
      BIOLKL(J,K2)= BIOLKL(J,K2)+ALPHA(KK,J,K2)*ACBACL*&
                    (KBACWLocal*XMULTW+KBACSLocal*XMULTS)
    end do Forms
  end do Ions
end do Segments
end Subroutine BIOLYS
