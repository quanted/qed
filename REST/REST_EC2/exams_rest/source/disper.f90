subroutine DISPER
! DISPER computes the turbulent transport field (including
! boundary conditions) for water and sediments, and generates the
! transport field as a sum of advective and turbulent motions.
! Revised 12 April 1983 by L.A. Burns
! Revised 11 July 1983 for mode 3 operations.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 08-Feb-1999 for floating point comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons
Implicit None
! Local variables:
integer :: I, J, K, KK, K3, L1
real :: TEMPL, TEMSED, XTEMP1, XTEMP2
! Calculation of dispersive fluxes:
! Take pairings one-by-one
Pairs: do K = 1, size(JTURBG)
! Increment loop for blank pairings
if (JTURBG(K) == ITURBG(K) .and. JTURBG(K) == 0) cycle Pairs

! Issue warning for internal pairs (note that 0 case already dealt with)
if (JTURBG(K) == ITURBG(K)) then
   write (stderr,FMT='(A,/,A,I4,A)')&
      ' System definition warning: The dispersive pairs include an internal',&
      ' mixing of segment ',JTURBG(K),'. This entry has been ignored.'
   cycle pairs
end if

! Issue warning if any dispersive pairing refers to a segment
! number that is not part of the system (i.e., > KOUNT, < 0)
if (JTURBG(K) > KOUNT .or. ITURBG(K) > KOUNT .or. JTURBG(K) < 0 .or. &
      ITURBG(K) < 0) then ! Write warning and go on
   write (stderr,FMT='(A,I5,/,A,/,A)')&
      ' System definition warning: Dispersive pairing number',K,&
      ' refers to a segment that is not part of this ecosystem.',&
      ' This specification has been ignored.'
   cycle pairs
end if

! Check parameters for zero values
if (.not.(     (DSPG(K,NDAT) .NotEqual. 0.0)&
         .and. (XSTURG(K)    .NotEqual. 0.0)&
         .and. (CHARLG(K)    .NotEqual. 0.0)  )) then
   write (stderr,FMT='(A,I5,/,A)')& ! Notify user and skip pairing
      ' System definition warning: dispersive pairing number',K,&
      ' is incomplete. This specification has been ignored.'
   cycle pairs
end if

! The entry can be processed; simplify subsequent code by assigning
! current segment numbers to indices J and I
J = JTURBG(K)
I = ITURBG(K)

! Detect and process cases:
! (Both upstream and downstream boundary conditions are considered,
! although in the current application both refer to dispersive
! exchanges with sinks (i.e., boundary condition concentration = 0.0)
! Although there is no difference between the treatment of upstream and
! downstream boundary conditions, the distinction has been retained in
! the code to simplify modifications.

Upstream_BC: if (J == 0) then ! Upstream boundary condition
   if (TYPEG(I) == 'B') then ! Bottom sediment upstream boundary condition
      ! screen for patent error
      if (DSPG(K,NDAT) .GreaterThan. 1.0E-03) then
         ! patent error...issue warning message
         DSPG(K,NDAT) = 1.0E-05
         write (stderr, fmt='(A/A)')&
         ' Sediment dispersivity cannot be greater than',&
         ' 1.0E-03 m2/hr. Input reset to 1.0E-05.'
      end if
      TEMPL = (WATVOL(I)/VOLG(I))*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
      WATOUL(I) = WATOUL(I)+TEMPL
   else ! Water column upstream boundary condition:
      ! screen boundary condition for patent error
      if (DSPG(K,NDAT) .LessThan. 1.0E-03) then
         ! patent error...issue warning message
         write (stderr, fmt='(A)')&
         ' Water column dispersivity cannot be less than 1.0E-03 m2/hr.'
               write (stderr, fmt='(A/A)')&
         ' This appears to be a horizontal transport path;',&
         ' it has been set to 1.0E+03 m2/hr.'
         DSPG(K,NDAT)=1.0E+03
      end if
      TEMPL = 1000.*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
      WATOUL(I) = WATOUL(I)+TEMPL
      SEDOUL(I) = SEDOUL(I)+TEMPL*SEDCOL(I)
   end if; cycle Pairs
end if Upstream_BC

Downstream_BC: if (I == 0) then ! Downstream boundary condition
   if (TYPEG(J) == 'B') then ! Bottom sediment downstream boundary condition
      ! screen for patent error
      if (DSPG(K,NDAT) .GreaterThan. 1.0E-03) then
         ! patent error...issue warning message
         DSPG(K,NDAT) = 1.0E-05
         write (stderr, fmt='(A/A)')&
         ' Sediment dispersivity cannot be greater than',&
         ' 1.0E-03 m2/hr. Input reset to 1.0E-05.'
      end if
      TEMPL = (WATVOL(J)/VOLG(J))*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
      WATOUL(J) = WATOUL(J)+TEMPL
   else ! Water column downstream boundary condition
      ! screen boundary condition for patent error
      if (DSPG(K,NDAT) .LessThan. 1.0E-03) then
         ! patent error...issue warning message
         write (stderr, fmt='(A)')&
         ' Water column dispersivity cannot be less than 1.0E-03 m2/hr.'
               write (stderr, fmt='(A/A)')&
         ' This appears to be a horizontal transport path;',&
         ' it has been set to 1.0E+03 m2/hr.'
         DSPG(K,NDAT)=1.0E+03
      end if
      TEMPL = 1000.*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
      WATOUL(J) = WATOUL(J)+TEMPL
      SEDOUL(J) = SEDOUL(J)+TEMPL*SEDCOL(J)
   end if; cycle Pairs
end if Downstream_BC

! Not a boundary condition, so an interchange among system segments:
! 1. Check for bottom sediment - water column interaction:
Bed_Water: if (                              &
   (TYPEG(J)=='B'.and.TYPEG(I)/='B') .or.    &
   (TYPEG(J)/='B'.and.TYPEG(I)=='B')         &
   ) then
! Internal dispersive exchange between water column and sediment:
! screen for patent error
if (DSPG(K,NDAT) .GreaterThan. 1.0E-03) then
   ! patent error...issue warning message
   DSPG(K,NDAT) = 1.0E-05
   write (stderr, fmt='(A/A)')&
   ' Sediment dispersivity cannot be greater than',&
   ' 1.0E-03 m2/hr. Input reset to 1.0E-05.'
end if
if (TYPEG(J) == 'B') then ! "J" is the benthic segment
  KK = J
  K3 = I
else !  Segment "I" is the benthic segment
  KK = I
  K3 = J
end if
! Compute water exchange as product of porosity of sediment and
! dispersion coefficient:
TEMPL = (WATVOL(KK)/VOLG(KK))*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
! Increment WATFL with a symmetrical exchange of water:
WATFL(I,J) = WATFL(I,J)+TEMPL
WATFL(J,I) = WATFL(J,I)+TEMPL
!
! Compute resuspension and bursting of surface sediment, subduction of
! sediments by benthic fauna, etc. so as to give a residence time for
! benthic solids that matches the pore water residence time...
TEMSED = TEMPL*SEDCOL(KK)
Chemical_loop: do L1 = 1, KCHEM
   SEDFL(K3,KK,L1) = SEDFL(K3,KK,L1)+TEMSED
   ! If the chemical does not sorb, its transport is mediated solely via
   ! the pore water exchange equations, and sediment resettlement can be
   ! computed as a symmetrical return flow from the water column:
   if ((ALPHA(30,K3,L1).Equals.0.0) .and. (ALPHA(30,KK,L1).Equals.0.0)) then
      SEDFL(KK,K3,L1) = SEDFL(KK,K3,L1)+TEMSED
      cycle Chemical_loop
   end if
   ! If the chemical sorbs to sediment phases, and the sediment properties
   ! differ, apparent resettlement of sediments must be corrected for any
   ! differences in the sorptive capacity of the suspended and the bed
   ! sediments to avoid an artificial mixing of the sediment properties:
   XTEMP1 = (ALPHA(29,K3,L1)+ALPHA(31,K3,L1))*SEDCOL(K3)/ALPHA(30,K3,L1)
   XTEMP2 = ALPHA(30,KK,L1)/(SEDCOL(KK)*(ALPHA(29,KK,L1)+ALPHA(31,KK,L1)))
   SEDFL(KK,K3,L1) = SEDFL(KK,K3,L1)+TEMSED*XTEMP1*XTEMP2
end do Chemical_loop
cycle Pairs
end if Bed_Water

! 2. segments of same type - separate water-water from sed-sed:

Same_Type: if (TYPEG(J) == 'B') then ! Sediment-sediment pairing
   ! Note that sediment does not flow between benthic sediments...
   ! addition of such a feature would require treatment of sediment properties
   ! as being subject to mixing
   if (DSPG(K,NDAT) .GreaterThan. 1.0E-03) then
   ! patent error...issue warning message
      DSPG(K,NDAT) = 1.0E-05
      write (stderr, fmt='(A/A)')&
      ' Sediment dispersivity cannot be greater than',&
      ' 1.0E-03 m2/hr. Input reset to 1.0E-05.'
   end if
   TEMPL = (((WATVOL(J)/VOLG(J))+(WATVOL(I)/VOLG(I)))/2.)*&
          (DSPG(K,NDAT)*XSTURG(K)/CHARLG(K))
   WATFL(I,J) = WATFL(I,J)+TEMPL
   WATFL(J,I) = WATFL(J,I)+TEMPL
else ! Water-column to water-column pairing...with sediment flow
   ! screen water column exchange for patent error
   if (DSPG(K,NDAT) .LessThan. 1.0E-03) then
      ! patent error...issue warning message
      write (stderr, fmt='(A)')&
      ' Water column dispersivity cannot be less than 1.0E-03 m2/hr.'
      if (abs(J-I)==1) then
         write (stderr, fmt='(A/A)')&
         ' This appears to be a vertical transport path;',&
         ' it has been set to 1.0E-02 m2/hr.'
         DSPG(K,NDAT)=1.0E-02
      else
         write (stderr, fmt='(A/A)')&
         ' This appears to be a horizontal transport path;',&
         ' it has been set to 1.0E+03 m2/hr.'
         DSPG(K,NDAT)=1.0E+03
      end if
   end if
   TEMPL = 1000.*DSPG(K,NDAT)*XSTURG(K)/CHARLG(K)
   WATFL(I,J) = WATFL(I,J)+TEMPL
   WATFL(J,I) = WATFL(J,I)+TEMPL
   Chemical_loop2: do L1 = 1, KCHEM
      SEDFL(I,J,L1) = SEDFL(I,J,L1)+TEMPL*SEDCOL(J)
      SEDFL(J,I,L1) = SEDFL(J,I,L1)+TEMPL*SEDCOL(I)
   end do Chemical_loop2
end if Same_Type
end do Pairs
end Subroutine DISPER
