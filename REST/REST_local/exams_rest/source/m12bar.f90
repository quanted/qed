subroutine M12BAR
! Created 25 April 1984 by L.A. Burns
! Revised 27-DEC-85 (LAB)
use Implementation_Control
use Input_Output ! Command language variables
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
Implicit None
! Set up data handler for scratchpad:
integer :: IBUFF(VARIEC)
! Zero the data space:
ALPHA = 0.0;  BIOLKL = 0.0; EXPOKL = 0.0; HYDRKL = 0.0; OXIDKL = 0.0
PHOTKL = 0.0; REDKL = 0.0;  S1O2KL = 0.0; VOLKL = 0.0;  YSATL = 0.0
! Because the allochthonous loads may be reduced in any month, in
! Modes 1/2--PRSWG 0 operations the final computed value of CONLDL is
! retained for further computation. In this way the final values of
! the external loadings (reported in Table 14) definitely reflect the
! actual load values used for simulation. The only circumstance under
! which this technique could cause a difference in the PRSWG 0
! simulations vs. the (PRSWG=1, MONTHG=13) Mode 1/2 simulations is
! in those (presumably very rare) cases where there is a major seepage
! load into a benthic segment whose bulk density and water content
! undergoes large seasonal variation. This would arise because CONLDL
! is computed (in TRANSP subroutine) as the sum of the allochthonous
! loads (TOTLDL) divided by the aqueous volume (WATVOL(J)) of each
! segment; WATVOL could conceivably change under the conditions
! described.
! CONLDL = 0.0D+00
INTINL = 0.0D+00; TOTKL = 0.0D+00; BIOTOL = 0.0; SEDCOL = 0.0
SEDMSL = 0.0;     WATVOL = 0.0;    YIELDL = 0.0D+00
! End of re-initialization of data space.
do NDAT = 1, 12 ! Loop to recover and accumulate the computational variables
  call UNPBAR (IBUFF)
end do
! Convert computational variables to average values:
ALPHA =  ALPHA/12.0;   BIOLKL = BIOLKL/12.0; EXPOKL = EXPOKL/12.0
HYDRKL = HYDRKL/12.0;  OXIDKL = OXIDKL/12.0; PHOTKL = PHOTKL/12.0
REDKL =  REDKL/12.0;   S1O2KL = S1O2KL/12.0; VOLKL = VOLKL/12.0
YSATL =  YSATL/12.0
! CONLDL = CONLDL/12.0 ! See comment above re: commenting out CONLDL
INTINL = INTINL/12.0; TOTKL = TOTKL/12.0;   BIOTOL = BIOTOL/12.0
SEDCOL = SEDCOL/12.0; SEDMSL = SEDMSL/12.0; WATVOL = WATVOL/12.0
YIELDL = YIELDL/12.0
return
end Subroutine M12BAR
