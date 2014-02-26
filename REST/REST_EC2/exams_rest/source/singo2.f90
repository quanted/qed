subroutine SINGO2(K2,NSEG)
! Computes photochemical transformations due to singlet oxygen.
! Created 15 June 1983 by L.A. Burns
! Revised 26 October 1983 (LAB) to expand to 280 nm.
! Revised 14-Sep-2000 (LAB) to use DOCETA for average aquatic humus
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None

integer, intent (in) :: K2, NSEG
! K2 is the number of the chemical currently being processed
! NSEG is the number of the segment being processed in SUNLYS

! Local Variables:
integer :: I, II, K, KK, LAMKNT
real :: ABSLIT, DISO2, TEMP, S3, TKEL
! TEMP is a temporary variable
! DISO2 is local value of oxygen tension (Molar).
! ABSLIT is rate of light absorption and generation of (humic) triplets,
! with units of mol(photons)/Liter per second (light absorption) and,
! when multiplied by PHI, units of moles of triplet per Liter per sec.

! KOX is rate constant for energy transfer from humic triplet to oxygen
! KOX has a value between 1.E9 and 3.E9 (Zepp, p.c.), here taken as:
real, parameter :: KOX = 2.0E+09 ! /M/s
! As increasing oxygen tension from air-saturated to oxygen saturation
! decreases the steady-state concentration of triplet sensitizer by
! a factor of 4 (Zepp, Schlotzhauer and Sink 1985. ES&T 19:74-81),
! and taking DOCG as 20 mg/L (per R.G. Zepp-concentration  of 21 mg/L is
! what was used in the experiment with Aucilla River water) gives:
real, parameter :: KDECS3=8.0E+04, KQNCH=4.0E+03
! KDECS3 is rate constant for spontaneous decay of humic triplet to
! ground state (units /s).
! KQNCH is rate constant for self-quenching by humic triplets (/M/s),
! but here calculated in terms of /s/(mg/L)
! KDECO2 is first-order decay constant for singlet oxygen (/s), based on a
! lifetime of 4 microseconds (Haag et al. 1984. Chemosphere 13:631-640)
real, parameter :: KDECO2 = 2.5E+05 ! (/s)
! PHI is quantum yield for production of sensitizer (humic) triplets,
! calculated from Phi = 0.015*exp(0.01(366-lambda))
real, parameter, dimension(38) :: PHI = (/0.0354, 0.0346, 0.0337, 0.0329,&
0.0321, 0.0313, 0.0305, 0.0298, 0.0290, 0.0283, 0.0276, 0.0269, 0.0263,&
0.0256, 0.0250, 0.0244, 0.0238, 0.0230, 0.0215, 0.0195, 0.0176,&
0.0159, 0.0144, 0.0130, 0.0118, 0.0107, 0.0097, 0.0087, 0.0079,&
0.0072, 0.0065, 0.0059, 0.0053, 0.0048, 0.0043, 0.0038,&
0.0031, 0.0024/)
!
! DOCETA are specific light absorption coefficients of (humic) DOC.
! Calculated from DOCETA =  0.71*exp(0.0145*(450.-Lambda))
! Zepp and Schlotzhauer 1981. Chemosphere 10:479-486
real, parameter, dimension(38) :: DOCETA = (/8.35, 8.05, 7.77, &
      7.49, 7.22, 6.97, 6.72, 6.48, 6.25, 6.03, 5.81, 5.61, 5.41, 5.21, &
      5.03, 4.85, 4.68, 4.47, 4.05, 3.50, 3.03, 2.62, 2.26, 1.96, 1.69, &
      1.47, 1.27, 1.10, 0.949, 0.821, 0.710, 0.614,&
      0.531, 0.460, 0.398, 0.326, 0.239, 0.167/)
!
! Calculate singlet oxygen concentrations. This only needs to be done once for
! each segment. Note that only first 38 elements of solar spectrum are used
if (SINCAL < NSEG) then
   ! compute the segment concentration of singlet oxygen
   ! Use size(PHI) elements of WAVEL (38 elements as of 3/96)
   ! Convert dissolved oxygen concentration to Molar value
   DISO2 = DISO2G(NSEG,NDAT)/32000.0
   ! moles/L= mg/L * (1mole/32g) * (1g/1000 mg)
   ! Compute concentration of (humic) sensitizer triplets:
   ! Calculate light absorption function over range 280-562.5 nm
   ABSLIT = 0.0 ! Must use explicit loop as WAVEL is dim(46)
   ! ABSLIT = sum(PHI*DOCETA*Irrad) ! (38 elements of WAVEL in Irrad)
   do LAMKNT = 1,38
      ABSLIT = ABSLIT + PHI(LAMKNT)*DOCETA(LAMKNT)*WAVEL(LAMKNT)
   end do
   ABSLIT = ABSLIT*DFACG(NSEG,NDAT)*DOCG(NSEG,NDAT)*1.2064E-06
   ! The numerical term in this equation compensates for the
   ! multiplication of the light field by (ln 10 * 3600 s/hr * 1000 mL/L)
   ! in subroutine SOLAR and also advances the computation of light
   ! absorption by humics by multiplying by (1000 cm3/L and 0.01 m/cm):
   ! (1000 * 0.01)/(2.3026 * 3600 * 1000) = 1.2064E-06
   ! Now compute steady-state concentration of (humic) sensitizer triplets
   S3 = ABSLIT/(KOX*DISO2+KDECS3+KQNCH*DOCG(NSEG,NDAT))
   ! and then the steady-state concentration of singlet oxygen
   S1O2L(NSEG) = (KOX*DISO2/KDECO2)*S3
   SINCAL = NSEG ! Signal that calculation has been done for this segment
end if
! Begin computations of transformation rate:
TKEL = TCELG(NSEG,NDAT)+273.15  ! Compute Kelvin temperature of segment
S1O2KL(NSEG,K2) = 0.0 ! Fail-safe initialization of local rate constant
II = -3                   ! initialize counter to map onto ALPHA matrix
Ionic_species_loop:&      ! Start loop over ionic species
do K = 1, 7
   II = II+1 ! Increment ALPHA map
   if (SPFLGG(K,K2) == 0) cycle Ionic_species_loop
   Forms_loop: do I = 1, 3 ! Loop on dissolved, sorbed, etc., forms
      KK = 3*K+II+I-1
      TEMP = K1O2G(I,K,K2)
      if (EK1O2G(I,K,K2) .NotEqual. 0.0)& ! if temperature-sensitive...
         TEMP = 10.**(K1O2G(I,K,K2)-(EK1O2G(I,K,K2)/(R_Factor*TKEL)))
      ! Now add contribution to overall second-order rate constant
      S1O2KL(NSEG,K2) = S1O2KL(NSEG,K2)+TEMP*ALPHA(KK,NSEG,K2)
   End do forms_loop
End do Ionic_species_loop
! Convert segment second-order rate constant to pseudo-first-order
S1O2KL(NSEG,K2) = S1O2KL(NSEG,K2)*S1O2L(NSEG)
return
end Subroutine SINGO2
