subroutine DATACK(K)
! Evaluates chemical input data; flags active processes
! Revised 15 June 1983 to add reduction
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 08-Feb-1999 to use floating point comparisons
! Revised 07-April-2001 to include aquatic metabolism in biolysis test
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Floating_Point_Comparisons
Implicit None
! Local variables for this subroutine
integer :: I, J ! Counters
integer :: StartMonth, EndMonth, BacNum ! controls for biolysis data evaluation
integer, intent (in) :: K ! the chemical under investigation
real :: BIOTES, HYDTES, PHOTES, REDTES ! Test sums
real :: Benthic_Bacteria, Planktonic_Bacteria
! Preset data switches to inactivate processes
PHOTSW = .false.; BIOSW = .false.;  VOLSW = .false.
HYDRSW = .false.; PRODSW = .false.; REDSW = .false.
! Set test sums to 0.0:
BIOTES = 0.0; HYDTES = 0.0; PHOTES = 0.0; REDTES = 0.0
! loop through chemical input data
Ions: do J = 1, 7
   ! Skip ionic species that do not exist
   ! N.B.: even if rate constants /=0, non-existing species will not set flags
   if (SPFLGG(J,K) == 0) cycle Ions
   BIOTES = BIOTES + sum(KBACWG(:,J,K)) + sum(KBACSG(:,J,K)) + AerMet(K) &
                   + AnaerM(K)
   HYDTES = HYDTES + sum(KAHG(:,J,K))   + sum(KNHG(:,J,K)) + sum(KBHG(:,J,K))
   PHOTES = PHOTES + sum(QYield(:,J,K)) + sum(KOXG(:,J,K)) + sum(K1O2G(:,J,K))
   REDTES = REDTES + sum(KREDG(:,J,K))
end do Ions
if (BIOTES .NotEqual. 0.0) BIOSW = .true.
! Evaluate biolysis data for use of aquatic metabolism half-lives
! Transfer input data to local versions
KBACWL(:,:,K)=KBACWG(:,:,K); KBACSL(:,:,K)=KBACSG(:,:,K)
if (((sum(KBACWL(:,:,K)).Equals.0.0).and.(AerMet(K) .GreaterThan. 0.0)) .or. &
    ((sum(KBACSL(:,:,K)).Equals.0.0).and.(AnaerM(K) .GreaterThan. 0.0))) then 
   ! data transfer needed, gather bacterial population data:
   Select case (MODEG)
   case (1,2) ! use the current value of MONTHG to locate the data
      StartMonth=MONTHG; EndMonth=MONTHG
   case default ! all others -- calculate averages of environmental data
      StartMonth=6; EndMonth=8
   end select
   if ((sum(KBACWL(:,:,K)).Equals.0.0).and.(AerMet(K).GreaterThan.0.0)) then
      Planktonic_Bacteria = 0.0
      ! Calculate mean water-column bacterial population
         BacNum=0
         do j=1,kount
            if (TYPEG(J) == 'B') cycle
            Planktonic_Bacteria = Planktonic_Bacteria + &
               (sum(BACPLG(J,StartMonth:EndMonth)) / (EndMonth-StartMonth+1))
            BacNum=BacNum+1
         end do
      ! transfer aquatic aerobic metabolism half-life
      ! to KBACWL for dissolved phase (only), irrespective of ionization
      ! Check on the environmental data:
      if ((Planktonic_Bacteria .GreaterThan. 0.0) .and. BacNum>0) then
         KBACWL(1,:,K) = (0.69314718/(AerMet(K)*24.0)) &! first order K
            / (Planktonic_Bacteria/BacNum)    ! converted to second-order
      end if
   end if

   if ((sum(KBACSL(:,:,K)).Equals.0.0).and.(AnaerM(K) .GreaterThan. 0.0)) then
      Benthic_Bacteria   = 0.0
      ! Calculate mean surficial bed sediment bacterial population
      BacNum=0
         do j=1,kount
            if(TYPEG(J)/= 'B'.or. (TYPEG(J)=='B'.and.TYPEG(J-1)=='B')) cycle
            Benthic_Bacteria = Benthic_Bacteria + &
               sum(&
         BNBACG(J,StartMonth:EndMonth)/(PCTWAG(J,StartMonth:Endmonth)-100.)&
               ) / (EndMonth-StartMonth+1)
            BacNum=BacNum+1
         end do
      ! transfer aquatic anaerobic metabolism half-life
      ! to KBACSL for dissolved phase (only), irrespective of ionization
      ! Check on the environmental data:
      if ((Benthic_Bacteria .GreaterThan. 0.0) .and. BacNum>0) then
         KBACSL(1,:,K) = (0.69314718/(AnaerM(K)*24.0)) &! first order K
            / (Benthic_Bacteria/BacNum)    ! converted to second-order
      end if
   end if
end if
if (HYDTES .NotEqual. 0.0) HYDRSW = .true.
if (REDTES .NotEqual. 0.0) REDSW = .true.
if (PHOTES .NotEqual. 0.0) PHOTSW = .true.
if ( (MWTG(K) .GreaterThan. 0.0) .and. &
   ( (HENRYG(K) .GreaterThan. 0.0) .or. (VAPRG(K) .GreaterThan. 0.0))&
    ) VOLSW = .true.

do I = 1, NTRAN
   if (CHPARG(I) == K) then    ! the current chemical
      PRODSW = .true.          !  produces a transformation product
      exit
   endif
end do

end Subroutine DATACK
