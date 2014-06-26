subroutine SOLFCT(TIME,YTEMP,GLOLIT)
use SOLAR_data
! Computation of irradiance as function of solar zenith angle.
! Completed 26 November 1983 by L.A. Burns.
! Revised 04-SEP-1985 (LAB) to hardwire result of EXP(-(>=87.4))
use Floating_Point_Comparisons ! Revision 09-Feb-1999
! Local variables:
Implicit None
real :: TIME, GLOLIT, YTEMP, BEAM, REFANG, TEMANG
real :: S1,S2,T1,T2,REFLEC,EXPARG,SKYLIT
real :: XMU, XMU2, XMUI(3), ZENANG, SLAMTH, PHI
! expar2 is used to trap underflows in exponential light extinction,
!   as it is more efficient to trap them than to let the exp -> 0.0.
real :: expar2
! BEAM is solar beam intensity.
! GLOLIT is global light intensity (beam + skylight)
! XMU are generalized cosine functions specific to air, aerosol, and ozone
! ZENANG is solar zenith angle
! SLAMTH and PHI are skylight computational variables
! Convert time (sec) to local hour angle and compute cosine of
! zenith angle (XMU):
XMU = SLSD+CLCD*cos(TIME/13751.)
if (XMU .LessThan. 0.0) XMU = 0.0
! Compute fraction of beam reflected
ZENANG = acos(XMU) ! Calculate zenith angle (the angle of incidence) and apply
REFANG = asin(sin(ZENANG)/REFIND(LAMBDA))! Snell's law for angle of refraction

! Special cases arise for normal incidence and when the angles of incidence
! and refraction sum to 90 degrees...
if (ZENANG .LessThan. 0.0017) then ! normal incidence of beam
   REFLEC = REFRAT ! (REFRAT is computed in SOLAR)
else 
   TEMANG = abs(1.571-(ZENANG+REFANG))
   if (TEMANG .LessThan. 0.0017) then
      ! i + j is 90 degrees, use Brewster's law
      REFLEC = BREW ! (BREW is computed in SOLAR)
   else ! use Fresnel's law
      S1 = sin(ZENANG-REFANG) ! Compute trig functions for Fresnel's law
      S2 = sin(ZENANG+REFANG)
      T1 = tan(ZENANG-REFANG)
      T2 = tan(ZENANG+REFANG)
      ! Compute fraction of beam reflected via Fresnel's law:
      REFLEC = (abs(((S1*S1)/(S2*S2))+((T1*T1)/(T2*T2))))/2.
   end if
end if

XMU2 = XMU*XMU
XMUI(1) = sqrt((XMU2+1.8E-03)/1.0018)
XMUI(2) = sqrt((XMU2+3.0E-04)/1.0003)
XMUI(3) = sqrt((XMU2+7.4E-03)/1.0074)
!
EXPARG = RAYDEP(LAMBDA)/XMUI(1)+AERDEP(LAMBDA)/XMUI(2)+OZDEP(LAMBDA)/XMUI(3)
! trap underflows
if (EXPARG .LessThanOrEqual. XTES) then
   BEAM = XMU*HLAM(LAMBDA)*exp(-EXPARG)
else
   BEAM = 0.0
endif
BEAM = BEAM*(1.0-REFLEC) ! beam irradiance just below water surface
! Compute skylight functions:
PHI = sqrt((1.+TTEE)/(XMU2+TTEE))-1.0
! trap underflows and tailor expression accordingly
EXPARG = abs(G3T3*PHI)
EXPAR2 = abs(GT1GT2*PHI)
if (EXPAR2 .GreaterThan. XTES) then
   SLAMTH = 0.0
elseif (EXPARG .GreaterThan. XTES) then
   SLAMTH = EFF*exp(GT1GT2*PHI)
else
 SLAMTH = (EFF+ONEFF*exp(G3T3*PHI))*exp(GT1GT2*PHI)
endif
SKYLIT = (0.934/(1.0-0.066*AIREFL))*EMMHI*SLAMTH ! Add sky radiation to beam
GLOLIT = BEAM+SKYLIT
return
end Subroutine SOLFCT
