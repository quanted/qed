subroutine DISTRB
! This subroutine computes the (equilibrium) fraction of the total
! concentration of chemicals ("Y" state variable) that is present in each
! chemical species or form (7 ionic species, each of which may be dissolved,
! complexed with "dissolved" organic matter, sediment-sorbed, or biosorbed).
! Created August 1979 by L.A. Burns
! Revised 03-Jun-1984 (LAB) to compute KPB from KOW
! Revised 08-Feb-1999 for floating pont comparisons
! Revised 19-Jul-2000 to implement results of study of Kpdoc as f(Kow)
! Revised 02-March-2001 to give non-zero KPSG precedence (line 109 ff)
! Notes
!   Sorption of ions needs more work. Needs especially some methods for
!   calculating binding constants when input data missing
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons
Implicit None
! Local variables for this subroutine
integer :: I, J, K, K1, K2, K3
real :: DISFUN(28), DOCL, SUMFUN, TKEL, TOTMAS
real :: HPLUS, HPLSQ, HPLCUB, HYDRX, HYDSQ, HYDCUB
! DISFUN are contributions of each species to the distribution constants ALPHA

! Transfer (or compute if appropriate) Koc, KpB, and KpDOC

! Initialize variables
DISFUN=0.0; DOCL=0.0; SUMFUN=0.0; TKEL=-300.0; TOTMAS=0.0; KPSL=0.0

partition_coefficient_loop: do K = 1, KCHEM
  KOCL(K) = KOCG(K); KOWL(K) = KOWG(K) ! transfer input data
  if ((KOCG(K) .Equals. 0.0) .and. (KOWG(K) .GreaterThan. 0.0))&
      KOCL(K) = 0.35*KOWG(K)
  ! If necessary, estimate Kow from Koc for use in KpB and KpDOC
  if ((KOWG(K).Equals.0.0).and.(KOCG(K).GreaterThan.0.0))&
      KOWL(K) = KOCL(K)/0.35
  ! Neither Kow nor Koc present, but given Kpdoc...
  if ((KOCG(K) .Equals. 0.0) .and. (KOWG(K) .Equals. 0.0)) then
      KOWL(K) = KPDOCG(1,K)/0.074
      KOCL(K) = 0.35*KOWL(K)
  end if
  ! for now, assume ionic speciation doesn't affect DOC binding
  ! and bioconcentration; i.e., set ionic species parameters from Kow
  species: do I = 1, 7
    KPBL(I,K) = KPBG(I,K); KPDOCL(I,K) = KPDOCG(I,K)
    if (SPFLGG(I,K) == 0 .or. (KOWL(K) .LessThanOrEqual. 0.0)) cycle species
    if (KPBG(I,K)  .LessThanOrEqual. 0.0) KPBL(I,K)   = 0.436*(KOWL(K)**0.907)
    if (KPDOCG(I,K).LessThanOrEqual. 0.0) KPDOCL(I,K) = 0.074*KOWL(K)
  end do species
end do partition_coefficient_loop
! Commentary for partition_coefficient_loop:
! The use of octanol-water partition coefficients is discussed in
!    Karickhoff, S.W., D.S. Brown, and T.A. Scott. 1979.
!       Water Research 13:241-248.
! The 0.35 factor for computing Koc for whole sediments is from
!    Seth, R., D. Mackay, and J. Muncke. 1999.
!       Environ Sci Technol 33:2390-2394.
! Computation of KpB from Kow is from
!    Baughman, G.L, and D.F. Paris. 1981.
!       CRC Crit Rev Microbiol 8:205
! The computation of KpDOC as 7.4% of Kow is based on analysis of literature.
! This value is used for water column compartments; Kocl is used for benthics.

do K = 1, KCHEM ! first, transfer user kp values, which take precedence
   do J = 1, KOUNT
      do I = 1,7
         KPSL(I,J,K) = KPSG(I,K)
      end do
   end do
end do

! Compute total sorbing biomass in system segments and the fraction
! transported with system mass flows. PLMASG is mg/L of (dry) biomass in water
! column segments; it does not include macrophytes, benthic algae etc., but
! refers solely to the plankton and is transportable with the hydrologic flows
! through the segment. All biomass must be reduced to kg/liter of the
! associated water column. For bottom sediment segments, which may contain
! plant roots and infauna, BNMASG is grams/square meter (dry weight);
! benthic biomass is assumed to be fixed in place.
!
! pre-zero to eliminate previous run
WATVOL = 0.0; SEDMSL = 0.0; SEDCOL = 0.0; BIOTOL = 0.0

first_segments: do J = 1, KOUNT ! take segments in numerical order
   select case (typeg(j))
      case ("B") ! bottom sediments
      PLMASG(J,NDAT) = 0.0 ! load null entry in water column data type
      TOTMAS = BULKDG(J,NDAT)*VOLG(J)*1.0E+03 ! compute total mass in segment
      !             g/cm3    *  m3   * (1.E6 cm3/m3 * 1.E-3 kg/g)
      SEDMSL(J) = TOTMAS/(PCTWAG(J,NDAT)/100.) ! sediment mass (kilograms)
      WATVOL(J) = TOTMAS-SEDMSL(J)    ! liters of water present in segment
      SEDCOL(J) = SEDMSL(J)/WATVOL(J) ! sediment concentration as kg/L
      ! bottom sediment segments--infra-benthic biomass expressed as
      ! grams/square meter of bottom area-convert values to kg/L of pore water
      BIOTOL(J) = (BNMASG(J,NDAT)*AREAG(J)*0.001)/WATVOL(J)
   case default ! i.e., all cases other than Benthic
      BIOTOL(J) = PLMASG(J,NDAT)*1.0E-06 ! Water column - convert mg/L to kg/L
      BNMASG(J,NDAT) = 0.0 ! load null entry in benthos data type
      WATVOL(J) = VOLG(J)*1000. ! convert cubic meters to liters
      SEDCOL(J) = SUSEDG(J,NDAT)*1.E-6
      SEDMSL(J) = SEDCOL(J)*WATVOL(J) ! compute sediment mass in segment
   end select
end do first_segments

segments: do J = 1, KOUNT ! take segments in numerical order
   do K3 = 1, KCHEM ! evaluate partition coefficients; let the user's (KPSG)
                    ! value take precedence
     if ( (KOCL(K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(1,J,K3).GreaterThan. 0.0) ) )&
        KPSL(1,J,K3) = KOCL(K3)*FROCG(J,NDAT)

     if ( (KIECG(1,K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(2,J,K3).GreaterThan. 0.0) ) )&
        KPSL(2,J,K3) = KIECG(1,K3)*CECG(J,NDAT)

     if ( (KIECG(2,K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(3,J,K3).GreaterThan. 0.0) ) )&
        KPSL(3,J,K3) = KIECG(2,K3)*CECG(J,NDAT)

     if ( (KIECG(3,K3) .GreaterThan. 0.0) &
       .and. (.not. (KPSL(4,J,K3).GreaterThan. 0.0) ) )&
       KPSL(4,J,K3) = KIECG(3,K3)*CECG(J,NDAT)

     if ( (KIECG(4,K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(5,J,K3).GreaterThan. 0.0) ) )&
        KPSL(5,J,K3) = KIECG(4,K3)*AECG(J,NDAT)

     if ( (KIECG(5,K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(6,J,K3).GreaterThan. 0.0) ) )&
        KPSL(6,J,K3) = KIECG(5,K3)*AECG(J,NDAT)

     if ( (KIECG(6,K3) .GreaterThan. 0.0) &
        .and. (.not. (KPSL(7,J,K3).GreaterThan. 0.0) ) )&
        KPSL(7,J,K3) = KIECG(6,K3)*AECG(J,NDAT)
end do

! compute local value of dissolved organic carbon, i.e.,
DOCL = 1.0E-06*DOCG(J,NDAT) ! convert DOCG from mg/L(aq.) to Kg/L(aq)

! adjust dissociation constants for temperature
TKEL = TCELG(J,NDAT)+273.15 ! compute Kelvin temperature (TKEL)
all_chems: do K3 = 1, KCHEM
   KB1L(J,K3) = 0.0 ! pre-zero the dissociation constants
   KB2L(J,K3) = 0.0
   KB3L(J,K3) = 0.0
   KA1L(J,K3) = 0.0
   KA2L(J,K3) = 0.0
   KA2L(J,K3) = 0.0
   ! revalue only for those species that actually occur
   if (SPFLGG(2,K3) /= 0) then
     KB1L(J,K3) = 10.**(-PKG(1,K3)) ! evaluate singly charged (+1) cation
     if (EPKG(1,K3) .NotEqual. 0.0)&
         KB1L(J,K3) = 10.**(PKG(1,K3)-(EPKG(1,K3)/(R_Factor*TKEL)))
   end if
   if (SPFLGG(3,K3) /= 0) then
     KB2L(J,K3) = 10.**(-PKG(2,K3)) ! evaluate doubly charged (+2) cation
     if (EPKG(2,K3) .NotEqual. 0.0)&
       KB2L(J,K3) = 10.**(PKG(2,K3)-(EPKG(2,K3)/(R_Factor*TKEL)))
   end if
   if (SPFLGG(4,K3) /= 0) then
     KB3L(J,K3) = 10.**(-PKG(3,K3)) ! evaluate triply charged (+3) cation
     if (EPKG(3,K3) .NotEqual. 0.0)&
         KB3L(J,K3) = 10.**(PKG(3,K3)-(EPKG(3,K3)/(R_Factor*TKEL)))
   end if
   if (SPFLGG(5,K3) /= 0) then
      KA1L(J,K3) = 10.**(-PKG(4,K3)) ! evaluate singly charged (-1) anion
      if (EPKG(4,K3) .NotEqual. 0.0)&
        KA1L(J,K3) = 10.**(PKG(4,K3)-(EPKG(4,K3)/(R_Factor*TKEL)))
   end if
   if (SPFLGG(6,K3) /= 0) then
      KA2L(J,K3) = 10.**(-PKG(5,K3)) ! evaluate doubly charged (-2) anion
      if (EPKG(5,K3) .NotEqual. 0.0)&
          KA2L(J,K3) = 10.**(PKG(5,K3)-(EPKG(5,K3)/(R_Factor*TKEL)))
   end if
   if (SPFLGG(7,K3) /= 0) then
      KA3L(J,K3) = 10.**(-PKG(6,K3)) ! evaluate triply charged (-3) anion
      if (EPKG(6,K3) .NotEqual. 0.0)&
          KA3L(J,K3) = 10.**(PKG(6,K3)-(EPKG(6,K3)/(R_Factor*TKEL)))
   end if
   ! Dissociation constants now calculated and adjusted for temperature.
end do all_chems

HPLUS = 10.**(-PHG(J,NDAT)) ! compute local hydronium 
HYDRX = 10.**(-POHG(J,NDAT)) ! and hydroxide ion concentrations
HPLSQ = HPLUS*HPLUS ! compute square and cube of ion concentrations
HPLCUB = HPLSQ*HPLUS
HYDSQ = HYDRX*HYDRX
HYDCUB = HYDSQ*HYDRX

chemicals: do K3 = 1, KCHEM ! compute distribution coefficients for segment J
! first, compute sequential contribution of each factor
DISFUN(1) = 1.0                     ! dissolved neutral molecule
DISFUN(2) = KPSL(1,J,K3)*SEDCOL(J)  ! neutral molecule sorbed with sediments
if (TYPEG(J) == 'B') then           ! neutral molecule complexed with
  DISFUN(3) = KOCL(K3)*DOCL         ! dissolved organic carbon ("DOC")
else
  DISFUN(3) = KPDOCL(1,K3)*DOCL
endif
DISFUN(4) = KPBL(1,K3)*BIOTOL(J)    ! neutral molecule biosorbed

DISFUN(5) = KB1L(J,K3)/HYDRX                    ! SH4+ dissolved
DISFUN(6) = DISFUN(5)*KPSL(2,J,K3)*SEDCOL(J)    ! SH4+ sorbed with sediment
if (TYPEG(J) == 'B') then                       ! SH4+ complexed with "DOC"
  DISFUN(7) = DISFUN(5)*KOCL(K3)*DOCL
else
  DISFUN(7) = DISFUN(5)*KPDOCL(2,K3)*DOCL
end if
DISFUN(8) = DISFUN(5)*KPBL(2,K3)*BIOTOL(J)      ! SH4+ biosorbed
!
DISFUN(9) = KB2L(J,K3)*KB1L(J,K3)/HYDSQ         ! SH5++ dissolved
DISFUN(10) = DISFUN(9)*KPSL(3,J,K3)*SEDCOL(J)   ! SH5++ sorbed with sediment
if (TYPEG(J) == 'B') then                       ! SH5++ complexed with "DOC"
   DISFUN(11) = DISFUN(9)*KOCL(K3)*DOCL
else
   DISFUN(11) = DISFUN(9)*KPDOCL(3,K3)*DOCL
end if
DISFUN(12) = DISFUN(9)*KPBL(3,K3)*BIOTOL(J)     ! SH5++ biosorbed
!
DISFUN(13) = KB1L(J,K3)*KB2L(J,K3)*KB3L(J,K3)/HYDCUB ! SH6+++ dissolved
DISFUN(14) = DISFUN(13)*KPSL(4,J,K3)*SEDCOL(J)  ! SH6+++ sorbed with sediment
if (TYPEG(J) == 'B') then                       ! SH6+++ complexed with "DOC"
  DISFUN(15) = DISFUN(13)*KOCL(K3)*DOCL
else
  DISFUN(15) = DISFUN(13)*KPDOCL(4,K3)*DOCL
end if
DISFUN(16) = DISFUN(13)*KPBL(4,K3)*BIOTOL(J)    ! SH6+++ biosorbed
!
DISFUN(17) = KA1L(J,K3)/HPLUS                   ! SH2- dissolved
DISFUN(18) = DISFUN(17)*KPSL(5,J,K3)*SEDCOL(J)  ! SH2- sorbed with sediment
if (TYPEG(J) == 'B') then                       ! SH2- complexed with "DOC"
  DISFUN(19) = DISFUN(17)*KOCL(K3)*DOCL
else
  DISFUN(19) = DISFUN(17)*KPDOCL(5,K3)*DOCL
end if
DISFUN(20) = DISFUN(17)*KPBL(5,K3)*BIOTOL(J)    ! SH2- biosorbed
!
DISFUN(21) = KA1L(J,K3)*KA2L(J,K3)/HPLSQ        ! SH= dissolved
DISFUN(22) = DISFUN(21)*KPSL(6,J,K3)*SEDCOL(J)  ! SH= sorbed with sediment
if (TYPEG(J) == 'B') then                       ! SH= complexed with "DOC"
  DISFUN(23) = DISFUN(21)*KOCL(K3)*DOCL
else
  DISFUN(23) = DISFUN(21)*KPDOCL(6,K3)*DOCL
end if
DISFUN(24) = DISFUN(21)*KPBL(6,K3)*BIOTOL(J)    ! SH= biosorbed
!
DISFUN(25) = KA1L(J,K3)*KA2L(J,K3)*KA3L(J,K3)/HPLCUB ! S(-3) dissolved
DISFUN(26) = DISFUN(25)*KPSL(7,J,K3)*SEDCOL(J)  ! S(-3) sorbed with sediment
if (TYPEG(J) == 'B') then                       ! S(-3) complexed with "DOC"
  DISFUN(27) = DISFUN(25)*KOCL(K3)*DOCL
else
  DISFUN(27) = DISFUN(25)*KPDOCL(7,K3)*DOCL
end if
DISFUN(28) = DISFUN(25)*KPBL(7,K3)*BIOTOL(J)    ! S(-3) biosorbed
!
! sum the factors
  SUMFUN = sum(DISFUN(1:28))

do I = 1, 28 ! compute the distribution coefficients
  ALPHA(I,J,K3) = DISFUN(I)/SUMFUN
end do

! Totals: ALPHA(29) is total dissolved,
!         ALPHA(30) is total sediment-sorbed,
!         ALPHA(31) is total DOC complexed,
! and     ALPHA(32) is total biosorbed.
do I = 29, 32
  ALPHA(I,J,K3) = 0.0
  K1 = I-28
  K2 = I-4
  do K = K1, K2, 4
    ALPHA(I,J,K3) = ALPHA(I,J,K3)+ALPHA(K,J,K3)
  end do 
end do
end do chemicals

! For those cases with zero biomass, ALPHA(32,J,K3) will now serve to zero out
! transport of biosorbed chemical. Therefore BIOTOL (biomass concentrations)
! are now set with dummy unit values (where necessary) in order to prevent
! division by zero in both the transport computations and the output routines.
if (BIOTOL(J) .Equals. 0.0) BIOTOL(J) = 1.0
end do segments
return
end subroutine DISTRB
