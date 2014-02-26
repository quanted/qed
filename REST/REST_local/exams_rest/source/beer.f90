subroutine BEER(LIGHTL,J,K2,ILM)
! Computes average irradiances via Beer-Lambert Law.
! Created October 1982 by L.A. Burns.
! Revised 11 May 1984 (LAB) to separate suspended sediment & bulk d.
! Revised 04-SEP-1985 (LAB)
! Revised 05-May-2000 (LAB) to set profundal DFAC to 1.5.
! Revised 14-Sep-2000 (LAB) to use DOCETA for average aquatic humus
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Floating_Point_Comparisons
Implicit None
! CMPET is composite light attenuation coefficient.
real (kind (0D0)):: WTEMP(46), XIZERO
real, dimension(KOUNT) :: LIGHTL
real :: CMPET, XLBOT, XINT, TOTAVE, TOTTOP
integer :: IBOT, ILM(7), I, K2, ION, Index_Lambda
integer, intent (in) :: J
logical :: test
! J is the number of the segment being processed.
! K2 is the number of the chemical being processed.
! ION is counter on ionic species

! Absorption coefficients for pure water
! (data from Smith and Baker 1981 Applied Optics 20:177-184).
real, parameter :: WATETA(46) = &
      (/.288,.268,.249,.231,.215,.194,.174,.157,.141,.133,&
        .126,.119,.105,.0994,.0952,.0903,.0844,.0793,.0678,.0561,.0463,&
        .0379,.0300,.0220,.0191,.0171,.0162,.0153,.0144,.0145,.0145,&
        .01566,.0156,.0176,.0196,.0295,.0492,.0638,.0940,.244,.314,.349,&
        .440,.768,2.47,2.07/)

! Specific absorption coefficients for chlorophyll pigments:
! (/meter /(mg pigment/liter)), data from Smith and Baker (1978)
! and (for first 20 values) from Baker and Smith 1982.
real, parameter :: PIGETA(46) = &
      (/145.,138.,132.,126.,120.,115.,109.,106.,101.,95.,&
        90.,85.,80.,78.,75.,72.,70.,68.,64.,59.,&
        55.,55.,51.,46.,42.,41.,39.,38.,35.,32.,31.,28.,26.,24.,22.,&
        19.,14.,10.,8.,6.,5.,8.,13.,3.,2.,0./)

! Specific absorption coefficients for "dissolved" organic carbon:
! DOCETA are specific light absorption coefficients of (humic) DOC.
! Calculated from DOCETA =  0.71*exp(0.0145*(450.-Lambda))
! Zepp and Schlotzhauer 1981. Chemosphere 10:479-486
real, parameter, dimension(46) :: DOCETA = &
      (/8.35, 8.05, 7.77, 7.49, 7.22, 6.97, 6.72,&
        6.48, 6.25, 6.03, 5.81, 5.61, 5.41, 5.21,&
        5.03, 4.85, 4.68, 4.47, 4.05, 3.50,&
        3.03, 2.62, 2.26, 1.96, 1.69, 1.47,&
        1.27, 1.10, 0.95, 0.82, 0.71, 0.61,&
        0.53, 0.46, 0.40, 0.33, 0.24, 0.17, 0.12, 0.08,(0.0, i=41,46)/)


! Specific absorption coefficients for suspended sediments (/m/(mg/L))
! Datum from Miller and Zepp 1979 (Water Research) - average of 6 natural
! sediments, determined at 331 nm (assumed flat spectral response)
real, parameter :: SEDETA = 0.34
!
! Logical to indicate whether compartment has overlying water mass
logical :: Surface_water
! Datum for forcing exponential underflows to non-error zero.
! Useful for implementations in which underflows are not simply set
! to zero, but result in failures.
! Exponential light extinction produces underflows when the
! exponent (that is, the diffuse attenuation coefficient times the
! depth) is greater than about 87.4 (on machines with range to 1.E-38).
! In such cases, the light at the bottom of the segment can simply be
! set to zero.
! real :: XTES = 87.0
!
! This program sector computes a composite zenith light extinction
! coefficient ("CMPET") from the magnitude of the suspended
! sediment, chlorophyll, and doc specified for the compartment.
! This computation is based on the absorption maximum of the
! compound (input "LAMAXG") or, if this number is not in the
! environmentally relevant part of the solar spectrum, CMPET is
! computed at 300 nm. Computing at this single waveband is a
! necessity when calculating photolysis from a simple KDP.
!
! First, characterize the compartment (J):
! If the compartment number is "1" or the prior type is "B" the
! segment has an air/water interface:

If (j==1) then   !2013
   test=.true.
else
   test = (TYPEG(J-1)=='B')
end if
If (test) then
! if ((J==1) .or. (J>1 .and. TYPEG(J-1)=='B')) then
  Surface_water = .true. ! NO overlying water mass
else
  Surface_water = .false. ! There IS an overlying water mass
end if
Ion_loop: do ION = 1, 7  ! Begin loop on ionic species for PHOTO1 computations
if (SPFLGG(ION,K2) == 0) cycle Ion_loop  ! Skip nonexistent ions
!
! If LAMAX has already been mapped into the light absorption
! coefficient tables (i.e., ILM, which is set to zero in SUNLYS,
! has been reset here), these computations can be skipped until
! needed for the next chemical.
LAMAX_not_mapped: if (.not. ILM(ION) > 0) then
  Index_Lambda = floor(LAMAXG(ION,K2)*100.) ! Locate proper absorption line 
  Wavelength: select case (Index_lambda)    !  of absorption coefficients
  case (:27874) Wavelength  ! If LAMAXG is in short wavelength UV,
      ILM(ION) = 9          ! (i.e., L < 278.75 nm), use 300 nm
  case (27875:32121) Wavelength ! 278.75 <= L  < 321.22
      ! First seventeen lines of table: set parameters for mapping LAMAXG
      ! onto the table - "IBOT" is index of first line of this section of the
      ! table, "XLBOT" is bottom of waveband, "XINT" is bandwidth.
      IBOT = 1; XLBOT = 278.75; XINT = 2.5
      ILM(ION) = &
        IBOT+int((LAMAXG(ION,K2)-XLBOT)/XINT) ! Map LAMAXG onto table index
  case (32122:32499) Wavelength ! 321.22 <= L < 325.00
      ILM(ION) = 18
  case (32500:49499) Wavelength ! 325 <= L <495
      IBOT = 19; XLBOT = 325.; XINT = 10.
      ILM(ION) = &
        IBOT+int((LAMAXG(ION,K2)-XLBOT)/XINT) ! Map LAMAXG onto table index
  case (49500:51249) Wavelength !  495.00 <= L < 512.5
      ILM(ION) = 36
  case (51250:68749) Wavelength ! 512.5 <= L < 687.50
      IBOT = 37; XLBOT = 512.5; XINT = 25.
      ILM(ION) = &
        IBOT+int((LAMAXG(ION,K2)-XLBOT)/XINT) ! Map LAMAXG onto table index
  case (68750:72499) Wavelength ! 687.60 <= L < 725
      ILM(ION) = 44
  case (72500:77499) Wavelength ! 725.00 <= L < 775.00
      ILM(ION) = 45
  case (77500:) Wavelength ! 775.00 <= L, i.e., 775 nm or longer
      ILM(ION) = 46
  end select Wavelength
end if LAMAX_not_mapped
!
! Compute composite absorption coefficient for compartment at max wavelength
CMPET = SEDETA*SUSEDG(J,NDAT)+WATETA(ILM(ION))+PIGETA(ILM(ION))&
        *CHLG(J,NDAT)+DOCETA(ILM(ION))*DOCG(J,NDAT)
! The distribution factor (DFACG) is the optical path in the
! compartment as a ratio to the depth. It is difficult to
! compute, but a probable best value is 1.19 (Hutchinson, Treatise
! Limnology). However, in the presence of a large concentration
! of scattering particles, it may approach or reach 2.0. In order
! to ensure that an improper value is not loaded and used in
! computations, if the input DFACG is invalid it is set to 1.19 for surface
! waters (Type L and E) and to 1.50 for profundal waters (H).
if ((DFACG(J,NDAT).LessThan.1.0) .or. (DFACG(J,NDAT).GreaterThan.2.0)) then
   if (TYPEG(J)=='L' .or. TYPEG(J)=='E') then
      DFACG(J,NDAT) = 1.19
   elseif (TYPEG(J)=='H') then
      DFACG(J,NDAT) = 1.50
   end if
end if
if (TCELG(J,NDAT) .GreaterThan. 0.0) then ! If the water is liquid,
 XIZERO = 1.0   !     set the nominal level of surface light to 1.0.
else            ! If, however, temperature is zero or less (ice cover),
 XIZERO = 0.0   !     set the nominal light to zero
end if  ! BUT, if there is an overlying water mass, BOTLIT contains the actual
if (.not.Surface_water)   XIZERO = BOTLIT ! light intensity at the top
! Compute average light level (as fraction of incident light)
!   from the composite zenith light extinction coefficient:
BOTLIT = XIZERO*exp(-(CMPET*DEPTHG(J)*DFACG(J,NDAT)))
AVELIT(ION) = (XIZERO-BOTLIT)/(CMPET*DEPTHG(J)*DFACG(J,NDAT))
end do Ion_loop
! Compute total diffuse attenuation coefficients:
  TOTETA = DFACG(J,NDAT)*(WATETA+PIGETA*CHLG(J,NDAT)+&
                   DOCETA*DOCG(J,NDAT)+SEDETA*SUSEDG(J,NDAT))
! Compute average and bottom light intensities for compartment.
select case (Surface_water)
case (.true.)        ! Compartment does NOT have an overlying water mass
  ! If there is ice cover, load zero:
  if (TCELG(J,NDAT) .LessThanOrEqual. 0.0) then; WTEMP = 0.0D+00
  else; WTEMP = WLAML; end if  ! If not, load surface irradiance field
case (.false.)  ! Compartment HAS an overlying water mass; BOTLAM contains the
  WTEMP = BOTLAM ! light intensity at the bottom of the previous compartment
end select
! Compute light at bottom of compartment and average light level:
  BOTLAM = WTEMP*exp(-TOTETA*DEPTHG(J))
  WAVEL = (WTEMP-BOTLAM)/(TOTETA*DEPTHG(J))
! Compute average photon fluence in range 278.75--395 nm:
if (.not. (LIGHTL(J) .GreaterThan. 0.0)) then
! Compute sums used to report average irradiance to user:
  TOTTOP = sum(WLAML(1:25))
  TOTAVE = sum(WAVEL(1:25))
  if (TOTTOP .GreaterThan. 0.0) LIGHTL(J) = TOTAVE/TOTTOP
end if
return
end Subroutine BEER
