subroutine SUNLYS(LIGHTL,K2)
! Revised 26 October 1983 (LAB) to expand to 280 nm.
! "SUNLYS" is primarily a dispatching and data assembly routine
! for the computation of photochemical transformation kinetics.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real, dimension(KOUNT) :: LIGHTL
integer :: I, II, ILM(7), J, K, K2, KK, LAMKNT
! LIGHTL is a vector computed as the percentage of total photons in the
! waveband 280-395 nm as a mean value for each segment. It is a measure of the
! mean light intensity at depth in the segments in the photochemically active
! portion of the solar spectrum. LIGHTL is reported as part of the canonical
! profile of the system, and it is used to adjust the nominal concentration of
! photochemical oxidants (OXRADG) for light extinction.
! PHOTKL: vector of first-order direct photolysis rate constants.
! K2 is the number of the chemical currently being processed.
! ILM: index in the table of spectral absorption coefficients.
! K is a counter for loops on the (7) ionic species.
! LAMKNT counts through wavelength intervals.
logical :: ABSTOL(7), PHOXSW, SINGSW
! ABSTOL is light absorption by seven ionic chemical species (data check)
! PHOXSW indicates availability of radical oxidation rate data
! SINGSW indicates availability of singlet oxygen rate constants
ICALL = ICALL+1  ! Increment counter of calls to SUNLYS and
                 ! call internal subroutine to evaluate data availability
call SUNDAT (K2,ABSTOL,ABSORG,KOXG,K1O2G)
ILM = 0 ! Zero map index vector relating "LAMAXG" to light absorption spectrum
Segment_loop: do J = 1, KOUNT
  if (TYPEG(J) == 'B') cycle Segment_loop ! Increment loop if this is benthic
  AVELIT = 0.0 ! Zero average light intensity vector
  call BEER (LIGHTL,J,K2,ILM)! Call subroutine to compute segment light levels
  ! Initialize counter to map into ALPHA vector:
  II = -3
  Ionic_species: do K = 1, 7
    II = II+1 ! Increment ALPHA counter
    if (SPFLGG(K,K2) == 0) cycle Ionic_species ! Skip non-existent species
    ! Compute rate constant for species, adjust by reaction quantum
    ! yield and distribution coefficient (ALPHA) in next (forms) loop:
    if (ABSTOL(K)) then  ! Case 1: absorption spectrum available,
      do LAMKNT = 1, 46  ! Compute light absorption by chemical
        KDPL(K,J) = KDPL(K,J)+DFACG(J,NDAT)*WAVEL(LAMKNT)*ABSORG(LAMKNT,K,K2)
      end do ! (N.B.--KDPL is initialized in FIRORD)
    else
      ! Case 2: direct load of rate constant at latitude RFLATG(K);
      ! adjust rate for cloudiness, latitude, light extinction:
      if (KDPG(K,K2) .GreaterThan. 0.0) KDPL(K,J) = KDPG(K,K2)*AVELIT(K)*&
      (1.-0.056*CLOUDG(NDAT))*(191696.65+87054.63*cos(0.0349*LATG))&
      /(191696.65+87054.63*cos(0.0349*RFLATG(K,K2)))
      ! Latitude adjustments based on total irradiance data
      ! from Smithsonian meteorological tables
    end if
    forms: do I = 1, 3  ! (dissolved, sorbed with sediment, DOC-complexed)
      KK = 3*K+II+I-1  ! Calculate address for distribution coefficient (ALPHA)
      PHOTKL(J,K2) = & ! Adjust direct photolysis by quantum yield and
        PHOTKL(J,K2)+ALPHA(KK,J,K2)*KDPL(K,J)*QYield(I,K,K2) ! distribution
    end do forms ! End of forms (dissolved, particle-sorbed, etc.) loop
  end do Ionic_species
  if (SINGSW) call SINGO2 (K2,J) ! Call singlet oxygen transformations
  ! SINGO2 should be called at least once for each segment
  ! to calculate [singlet oxygen] for report in output tables, so
  if (K2 == KCHEM .and. SINCAL < J) call SINGO2 (K2,J)
end do Segment_loop
if (PHOXSW .or. K2==KCHEM) call PHOX (K2,LIGHTL)
return
contains
subroutine SUNDAT(K2,ABSTOL,ABSORG,KOXG,K1O2G)
   ! Evaluates photochemical input data to control subroutine calls
   ! Revised 13 June 1983 by L.A. Burns
   ! Revised 26 October 1983 (LAB) to extend phtochemistry to 280 nm
   ! Revised 15 August 2000 (LAB) to enforce use of absorbance data
   !   whenever possible
   real, dimension(:,:,:) :: ABSORG, KOXG, K1O2G
   integer :: I, J ! Local variables
   integer, intent (in) :: K2 ! number of chemical under evaluation
   logical, dimension(:) :: ABSTOL
   ABSTOL = .false.
   Absorbance:&
   do J = 1, 7 ! check on availability of absorbance data
      do I = 1, 46
         if (ABSORG(I,J,K2) .GreaterThan. 0.0) then
            ! if any absorbance line present, use these data
            ABSTOL = .true.
            ! Note that setting the entire ABSTOL vector 'true' enforces
            ! the use of absorbance data for the entire suite of
            ! photochemical computations. One could examine each ionic
            ! species separately and allow a mix of absorbance data and
            ! pseudo-first-order rate constants, but this seems
            ! excessively byzantine...
            exit Absorbance ! as soon as one species shows absorbance data
         end if
      end do
   end do Absorbance
   if (.not. all(ABSTOL)) then
      ! Using KDP, so alias the "quantum yield" to transfer the full rate
      ! but prevent reaction of sorbed or complexed species...
      Qyield(1,:,k2)=1.0
      Qyield(2,:,k2)=0.0
      Qyield(3,:,k2)=0.0
   end if
   ! Evaluate availability of rate constants
   PHOXSW = .false. ! evaluate availability of oxidation rate constants
   Oxidation_rates:&
   do J = 1, 7
      do I = 1, 3
         if (KOXG(I,J,K2) .GreaterThan. 0.0) then
            PHOXSW = .true.
            exit Oxidation_rates
         end if
      end do
   end do Oxidation_rates
   SINGSW = .false. ! evaluate availability of singlet oxygen reaction rates
   Singlet_Oxygen:&
   do J = 1, 7
      do I = 1, 3
         if (K1O2G(I,J,K2) .GreaterThan. 0.0) then
            SINGSW = .true.
            exit Singlet_Oxygen
         end if
      end do
   end do Singlet_Oxygen
end subroutine SUNDAT
end Subroutine SUNLYS
