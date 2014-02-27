subroutine TRANSP(INTOUL,K)
! Computes pseudo-first-order transport coefficients
! Revised 08-JUN-1984 (LAB) to separate planktonic and benthic biomass
! by using setting of "plankt" to distinguis between them.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real :: INTOUL(KOUNT), PLANKT ! Local computational variables
! PLANKT is set to zero as needed to inhibit transport of benthos
integer :: I, J, K
do J = 1, KOUNT
   ! Compute effect of *****-INPUT LOADINGS-***** on concentration
   CONLDL(J,K) = 1.0D+06*TOTLDL(J,K)/WATVOL(J)
   ! Compute first order rate constants for segment
   ! Compute (system and internal transport) EXPORT coefficients:
   ! 1. Exports from ecosystem
   PLANKT = 0.0               ! The transport of biosorbed materials follows
   if (SEDOUL(J) .GreaterThan. 0.0) PLANKT = 1.0 ! that of other solids
   EXPOKL(J,K) = WATOUL(J)*ALPHA(29,J,K)+SEDOUL(J)*ALPHA(30,J,K)/&
      SEDCOL(J)+WATOUL(J)*ALPHA(31,J,K)+WATOUL(J)*ALPHA(32,J,K)*PLANKT
   ! 2. Exports from segments that remain in ecosystem:
   INTOUL(J) = 0.0
   do I = 1, KOUNT
      PLANKT = 0.0          ! The transport of biosorbed materials follows
      if (SEDFL(I,J,K) .GreaterThan. 0.0) PLANKT = 1.0 ! that of other solids
      INTOUL(J) = INTOUL(J) + WATFL(I,J)*ALPHA(29,J,K)&
         + SEDFL(I,J,K)*ALPHA(30,J,K)/SEDCOL(J) + WATFL(I,J)*ALPHA(31,J,K)&
         + WATFL(I,J)*ALPHA(32,J,K)*PLANKT
   end do
end do
! Compute first order coefficients for INTERNAL TRANSPORT INPUTS:
! (and transpose matrix) --------------*************************------
do J = 1, KOUNT
   do I = 1, KOUNT
   INTINL(I,J,K) = 0.00D+00
      PLANKT = 0.0            ! The transport of biosorbed materials follows
      if (SEDFL(J,I,K) .GreaterThan. 0.0) PLANKT = 1.0  ! that of other solids
      INTINL(I,J,K) = (WATFL(J,I)*ALPHA(29,I,K)&
         + SEDFL(J,I,K)*ALPHA(30,I,K)/SEDCOL(I) + WATFL(J,I)*ALPHA(31,I,K)&
         + WATFL(J,I)*ALPHA(32,I,K)*PLANKT)/WATVOL(J)
      ! Final division by WATVOL converts INTINL to a factor expressing
      ! concentration change in receiving segment.
      end do
end do
return
end Subroutine TRANSP
