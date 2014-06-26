subroutine VOLAT(KO2L,K)
! VOLAT computes volatilization rate constants using a two-resistance
! model of movement of chemicals across the air-water interface.
! VOLKL is the first-order rate coefficient to be computed.
! Revised 12 July 1983 (LAB) for mode 3 operations.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real :: KO2L(KOUNT), TempReaeration, BanksWind
integer :: K
logical :: test
! Local variables for this subroutine:
real :: Conductivity,HENRYL,RESGAS,RESLIQ,SOLL,TKEL,VAPRL,WAT_velocity
integer :: J
Segments: do J = 1, KOUNT
KO2L(J) = 0.0
! Only the dissolved unionized form of the molecule can volatize, and
! the process is restricted to water-column segments with a air/water
! interface. Segment number 1 is required to be a water column with a
! free water surface (i.e., active air-water interface). Thereafter,
! Hypolimnion and Benthic segments can be skipped. In addition, if
! the current segment has an overlying water column (i.e., (J-1) is
! not of type "B"), then the segment can be skipped (note that this
! feature requires that each vertical segment of the system have a
! bottom sediment as a terminator).

! if (J>1 .and. (TYPEG(J)=='H' .or. TYPEG(J)=='B' .or. TYPEG(J-1)/='B'))&
!    cycle Segments

test=.False.
If (j>1) then   !2013
   If (TYPEG(J)=='H' .or. TYPEG(J)=='B' .or. TYPEG(J-1)/='B') then
      test=.true.
   end if
end if
If (test) cycle Segments
! Now check for infinite resistance to transport -- due, for
! example, to ice cover, or temperature indication of ice cover, or no wind.
if ( (WINDG(J,NDAT) .LessThanOrEqual. 0.0) .or. &
     (KO2G(J,NDAT)  .LessThan.        0.0) .or. & ! by accident?
     (TCELG(J,NDAT) .LessThanOrEqual. 0.0)      &
   )  cycle Segments
! Evaluate oxygen transfer rate from input data:
! Reaeration in cm/hr @ 20 deg. C. in input data, here converted to
! units of meters/hour and adjusted for local temperature
! If KO2 has not been entered by the user, it is estimated from Banks' (1975)
! relationship with wind speed.
! Here, the input parameter is windspeed at 10 cm, so need WINDG(J,NDAT) * 2.0
!    to recover wind speed at 10 m height.

TempReaeration = 0.0

if (KO2G(J,NDAT) .GreaterThan. 0.0) then
   TempReaeration = KO2G(J,NDAT)
else
   BanksWind = WINDG(J,NDAT) * 2.0
   if (BanksWind .LessThan. 5.5)  then
      TempReaeration = 1.51 * SQRT(BanksWind)
   elseif (BanksWind .LessThan. 30.) then
      TempReaeration = 0.115 * BanksWind * BanksWind
   else
      write (stderr,fmt='(a)') ' Windspeed exceeds Banks range;',&
            ' Oxygen piston velocity cannot be precisely calculated.',&
            ' It has been set to the Banks maximum of 104 cm/h.'
      TempReaeration = 104.0
   end if
end if

KO2L(J) = (TempReaeration/100.0)*(1.024**(TCELG(J,NDAT)-20.0))
! Check if entry to routine was invoked simply to compute KO2L
! for Canonical Profile table. If so, skip to next segments
if ( (HENRYG(K) .Equals. 0.0) .and. &
     (VAPRG(K)  .Equals. 0.0) .and. &
     (EHENG(K)  .Equals. 0.0) .and. &
     (EVPRG(K)  .Equals. 0.0)       &
   )  cycle Segments
TKEL = 273.15+TCELG(J,NDAT)

! Liquid phase resistance...estimated from molecular weight...----------------
   RESLIQ = 1./(KO2L(J)*sqrt(32./MWTG(K)))
! Liquid phase resistance ----------------------------------------------------

! Gas phase resistance -------------------------------------------------------
if ((HENRYG(K).NotEqual.0.0).or.(EHENG(K).NotEqual.0.0)) then
   HENRYL = HENRYG(K) ! Input data specifies Henry's Law constant
   if (EHENG(K) .NotEqual. 0.0) &
      HENRYL= 10.**(HENRYG(K)-(EHENG(K)/(R_Factor*TKEL)))
else       ! Input data does NOT specify Henry's Law constant, so
   ! compute Henry's Law constant from vapor pressure and solubility.
   ! Convert vapor pressure (mm Hg) to atmospheres:
   VAPRL = VAPRG(K)/760.0
   ! Temperature correction:
   if (EVPRG(K) .NotEqual. 0.0)&
      VAPRL = (10.**(VAPRG(K)-(EVPRG(K)/(R_Factor*TKEL))))/760.
   ! Compute solubility as moles per cubic meter:
   SOLL = SOLG(1,K)
   ! Temperature correction:
   if (ESOLG(1,K) .NotEqual. 0.0) SOLL =&
      (10.**(SOLG(1,K)-(ESOLG(1,K)/(R_Factor*TKEL))))*MWTG(K)*1000.
   ! Convert mg/L to moles/cubic meter
   SOLL = SOLL/MWTG(K)
   HENRYL = VAPRL/SOLL
end if
! Compute water vapor transport term as a function of windspeed
! (Liss 1973. Deep-Sea Research 20:221)
WAT_velocity = 0.1857+11.36*WINDG(J,NDAT)
RESGAS = 1./((WAT_velocity*HENRYL*sqrt(18./MWTG(K)))/(TKEL*8.206E-05))
! (Gas constant is 8.206E-05, molecular weight of water is 18.)
! Gas phase resistance -------------------------------------------------------

! Compute overall first order volatilization coefficient:
Conductivity = 1.0/(RESLIQ+RESGAS)
VOLKL(J,K) = (Conductivity*ALPHA(1,J,K)*AREAG(J))/VOLG(J)
end do Segments
end Subroutine VOLAT
