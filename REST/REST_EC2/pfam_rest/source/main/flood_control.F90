module flood
!Written by Dirk F. Young (Virginia, USA).
contains

!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subroutine flood_control
! Theses are the water level and washout routines.
! Given the inputs of water levels and flow through along with associated dates, 
! this routine populates several arrays as output (see intent(out) variables below

use utilities_module
use variables, ONLY:  event0_day, event0_month, eventDay,eventWeir, eventWashout, eventMinimum,eventFill, area, &
minimum_depth, leakage
use nonInputVariables, ONLY: num_records,precip, evap ,daily_depth, depth_release, makeupwater ,k_flow, &
fractional_removal,startday, overflow         
  implicit none
  
  real(8),dimension(num_records)             :: k_overflow         !washout due to weir changes and rainfall excess (1/sec) 
  real(8),dimension(num_records)             :: k_washout          !daily washout due to manual flow of paddy(1/sec)
  integer                                    :: firstyear, lastyear,dummy
  real(8),dimension(num_records)             :: minLevel            !minimum flood level prior to refill initiation
  real(8),dimension(num_records)             :: weir_depth
  real(8),dimension(num_records)             :: net               ! the net daily precipitaion/evaporation
  real(8),dimension(num_records)             :: prerelease_depth  !vector to hold calculation of depth after rain evap calcs
  real(8),dimension(num_records)             :: refill
  
  integer,allocatable,dimension(:)           :: reference_days !for multi-year mode
  integer :: i, numyears,status
    
  depth_release = 0.
  k_flow = 0.
  k_overflow = 0.
  k_washout = 0.
  overflow = 0.
 
  !******************************************************************************************************************
  call get_date (startday, firstyear ,dummy,dummy)
  call get_date (startday+num_records-1, lastyear,dummy,dummy)
  numyears = lastyear-firstyear+1  
  allocate(reference_days(numyears+1), STAT = status) !the extra year is used as a flag below

  !this is the zero reference day for each year as an absolute day value from the start of the simulation
  !jan 1 will be day number 1 (not zero)
    
  forall (i=1:numyears) reference_days(i) = jd (firstyear+i-1,event0_month,event0_day)-startday+1

  weir_depth = 0.0 !initialize    
  reference_days(numyears+1) = 1000000 !this serves as a flag for the last forall statement below
  
  minLevel = 0.
  k_washout = 0.
  refill=0.
 
  forall(i=1:numyears)  !Set paddy depth for the entire simulation
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(1)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(2)-1))))= eventWeir(1)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(2)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(3)-1))))= eventWeir(2)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(3)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(4)-1))))= eventWeir(3)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(4)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(5)-1))))= eventWeir(4)   
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(5)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(6)-1))))= eventWeir(5) 
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(6)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(7)-1))))= eventWeir(6)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(7)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(8)-1))))= eventWeir(7)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(8)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(9)-1))))= eventWeir(8)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(9)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(10)-1))))= eventWeir(9)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(10)))):max(1, min(num_records, &
    (reference_days(i)+eventDay(11)-1))))= eventWeir(10)
    weir_depth(max(1,min(num_records,  (reference_days(i)+eventDay(11)))):max(1, min(num_records, &
    (reference_days(i+1)          -1))))= eventWeir(11)    
  end forall  
  where (weir_depth < minimum_depth) weir_depth = minimum_depth  ! set wier minimum depth

  forall(i=1:numyears)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(1)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(2)-1))))= eventFill(1)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(2)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(3)-1))))= eventFill(2)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(3)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(4)-1))))= eventFill(3)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(4)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(5)-1))))= eventFill(4)   
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(5)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(6)-1))))= eventFill(5) 
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(6)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(7)-1))))= eventFill(6)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(7)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(8)-1))))= eventFill(7)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(8)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(9)-1))))= eventFill(8)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(9)))) :max(1, min(num_records, &
    (reference_days(i)+eventDay(10)-1))))= eventFill(9)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(10)))):max(1, min(num_records, &
    (reference_days(i)+eventDay(11)-1))))= eventFill(10)
    refill(max(1,min(num_records,  (reference_days(i)+eventDay(11)))):max(1, min(num_records, &
    (reference_days(i+1)          -1))))= eventFill(11)    
  end forall
  where (refill < minimum_depth) refill = minimum_depth  ! set refill minimum depth
  
  forall(i=1:numyears)   !Set Washout Vector for user-defined washout rates
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(1)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(2)-1))))= eventWashout(1)
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(2)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(3)-1))))= eventWashout(2)
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(3)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(4)-1))))= eventWashout(3)
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(4)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(5)-1))))= eventWashout(4)  
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(5)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(6)-1))))= eventWashout(5) 
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(6)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(7)-1))))= eventWashout(6)
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(7)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(8)-1))))= eventWashout(7)
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(8)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(9)-1))))= eventWashout(8)  
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(9)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(10)-1))))= eventWashout(9) 
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(10)))): max(1,min(num_records, &
    (reference_days(i)+eventDay(11)-1))))= eventWashout(10)      
    k_washout(max(1,min(num_records,  (reference_days(i)+eventDay(11)))): max(1,min(num_records, &
    (reference_days(i+1)         -1))))= eventWashout(11)        
  end forall

  forall(i=1:numyears)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(1)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(2)-1))))= eventMinimum(1)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(2)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(3)-1))))= eventMinimum(2)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(3)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(4)-1))))= eventMinimum(3)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(4)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(5)-1))))= eventMinimum(4) 
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(5)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(6)-1))))= eventMinimum(5) 
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(6)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(7)-1))))= eventMinimum(6)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(7)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(8)-1))))= eventMinimum(7)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(8)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(9)-1))))= eventMinimum(8)
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(9)))) : max(1,min(num_records, &
    (reference_days(i)+eventDay(10)-1))))= eventMinimum(9)  
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(10)))): max(1,min(num_records, &
    (reference_days(i)+eventDay(11)-1))))= eventMinimum(10)  
    minLevel(max(1,min(num_records,(reference_days(i)+eventDay(11)))): max(1,min(num_records, &
    (reference_days(i+1)         -1))))= eventMinimum(11)   
  end forall
  !******************************************************************************************************************

  k_washout=k_washout/86400.  !convert to seconds

  ! Check for excessive rainfall .  The assumption here is that paddy will be maintained at the user defined depth
  where (k_washout > 0.)
      net = precip  !if there is flow through, then assume that all evap and leakage is made up always
  elsewhere
      net = precip-evap-leakage !leakage is a scalar(m), others are vectors
  end where
  
  daily_depth = minimum_depth  !initialize

  daily_depth(1) = max(refill(1),minimum_depth)  !first depth is set to first refill depth.
  prerelease_depth =  daily_depth
  
  depth_release = 0.
  makeupwater =  0.
  
  do i = 2, num_records
      daily_depth(i) = daily_depth(i-1)+net(i)

      prerelease_depth(i) = max(daily_depth(i),minimum_depth)  !holds depth values before wier adjustments and post rain evap leak
      
      !Condition for refilling after evaporation & leakage
      if(daily_depth(i)< minlevel(i)) then
        makeupwater(i) = refill(i) - daily_depth(i)
        daily_depth(i) = refill(i)
      end if     
   
      !--------------- Weir lowered -----------------------------
      if (weir_depth(i) < weir_depth(i-1) ) then            
        if (daily_depth(i) > weir_depth(i)) then
             depth_release(i) = daily_depth(i)-weir_depth(i)
             daily_depth(i)= weir_depth(i)
        end if     
      
      !----------- Overflow by rainfall ---------------------------  
      else if  (weir_depth(i) == weir_depth(i-1) ) then 
      
        if (daily_depth(i)> weir_depth(i)) then    ! if the volume is greater than weir, then overflow is allowed
            overflow(i) = daily_depth(i)- weir_depth(i) 
            daily_depth(i)= weir_depth(i)   
        end if       
      end if
 
      !---------- Water raised manually by irrigation refilw ------             
      if (refill(i) > refill(i-1)  .and. daily_depth(i) < refill(i))then     
          makeupwater(i) = makeupwater(i) + (refill(i)-daily_depth(i))
          daily_depth(i)  = refill(i)
      end if

  
      daily_depth(i) = max(minimum_depth, daily_depth(i))
  end do

  fractional_removal= depth_release/prerelease_depth
  
  !The washout rate:
  k_overflow = overflow/daily_depth/86400.    !per second
  k_flow = k_washout+k_overflow  

end subroutine flood_control
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end module flood