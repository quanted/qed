module mass_inputs
!  Written by Dirk F. Young (Virginia, USA).
contains

    subroutine ParentMass2
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !Given the days and months of the mass applied, this routine sets up a vector with the daily mass applied
        !for the entire simulation.
        
        !This version incorporates slow release of pesticide
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
        use utilities_module
        use variables, ONLY: area, minimum_depth, applicationDay, applicationMonth, applicationMass, &
                             slowRelease,num_apps, max_apps

        use nonInputVariables, ONLY:num_records,daily_depth,startday,& 
                                    m1_input ,&   !subroutine output: mass to water column
                                    m2_input      !subroutine output: mass to benthic
        implicit none
        ! **************Variables Section********************************************************************    
        integer:: firstyear, lastyear, dummy, numyears, status,i   
        integer, allocatable, dimension(:,:) :: app_dates
        real(8), allocatable, dimension(:,:) :: release_fraction
         
        integer, dimension(max_apps) :: release_duration
             
        real(8) :: totalmass(max_apps)

        real(8) :: store, new, total
        integer :: j,k, lastpt
        !*************************************************************
        !Section to find out how many years are in the metfile *******
        call get_date (startday, firstyear ,dummy,dummy)
        call get_date (startday+num_records-1, lastyear,dummy,dummy)
          numyears = lastyear-firstyear+1  
        !*************************************************************
        allocate(app_dates(num_apps ,numyears), STAT = status)

        forall(j=1:num_apps,i=1:numyears) app_dates(j,i)= jd(firstyear+i-1,applicationMonth(j),applicationDay(j))-startday+1
 
        totalmass = applicationMass*area/10000.  !10000 m2 per hA ,Convert to Absolute Mass; area is in sq meters; apply_mass is kg/ha 
        m2_input=0.
        m1_input = 0.
          
        where (slowrelease > 0)
           release_duration= -log(0.05)/slowrelease + 2          
        elsewhere
           release_duration = 1 
        end where
  
 
      allocate(release_fraction(max_apps, maxval(release_duration)), STAT = status)
      release_fraction = 0.0

       !Calculate daily released fraction of pesticide mass 
       do k=1, num_apps
          store = 1.
          total= 0.
          do j = 1, release_duration(k)-1
            new = exp(-slowrelease(k)*j)
            release_fraction(k,j) = store-new
             store = new
            total = release_fraction(k,j)+ total
          end do
          release_fraction(k, release_duration(k)) = 1.-total
       end do




       !populate mass into input vector disperse the input mass
       do i=1,numyears
          do j=1,num_apps
            if (app_dates(j,i)>0 .AND.  app_dates(j,i) < num_records) then 
              lastpt = min(app_dates(j,i)+release_duration(j)-1, num_records)
              m1_input(app_dates(j,i):lastpt) = m1_input(app_dates(j,i):lastpt)+totalmass(j)* &
              release_fraction(j,1:release_duration(j))
            end if
          end do    
       end do

    !At this point, all mass is in the vector m1_input, regardless of the water level.  THe following
    !lines place the mass in m1_input into the vector m2_input if the water level is at the minimum depth.
     where (daily_depth == minimum_depth)
         m2_input = m1_input
         m1_input=0.
     end where
            
   end subroutine ParentMass2
            


!    subroutine ParentMass
!        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!        !Given the days and months of the mass applied, this routine sets up a vector with the daily mass applied
!        !for the entire simulation.
!        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
!
!        use utilities_module
!        use variables, ONLY: area, minimum_depth, applicationDay, applicationMonth, applicationMass
!
!        use nonInputVariables, ONLY:num_records,daily_depth,startday,& 
!                                    m1_input ,&   !subroutine output: mass to water column
!                                    m2_input      !subroutine output: mass to benthic
!        implicit none
!
!        ! **************Variables Section********************************************************************    
!        integer:: firstyear, lastyear, dummy, numyears, status,i
!
!        integer, allocatable, dimension(:) ::vector_of_app_dates_1
!        integer, allocatable, dimension(:) ::vector_of_app_dates_2
!        integer, allocatable, dimension(:) ::vector_of_app_dates_3
!        integer, allocatable, dimension(:) ::vector_of_app_dates_4
!        integer, allocatable, dimension(:) ::vector_of_app_dates_5
!        integer, allocatable, dimension(:) ::vector_of_app_dates_6  
!        integer, allocatable, dimension(:) ::vector_of_app_dates_7  
!        integer, allocatable, dimension(:) ::vector_of_app_dates_8
!        integer, allocatable, dimension(:) ::vector_of_app_dates_9
!        integer, allocatable, dimension(:) ::vector_of_app_dates_10  
!        integer, allocatable, dimension(:) ::vector_of_app_dates_11 
!
!        real(8):: AbsoluteMass1  !mass that goes in adjusted for area  (Note: apply_mass1 is per area)
!        real(8):: AbsoluteMass2
!        real(8):: AbsoluteMass3
!        real(8):: AbsoluteMass4
!        real(8):: AbsoluteMass5
!        real(8):: AbsoluteMass6
!        real(8):: AbsoluteMass7
!        real(8):: AbsoluteMass8
!        real(8):: AbsoluteMass9
!        real(8):: AbsoluteMass10
!        real(8):: AbsoluteMass11
!
!        !*************************************************************
!        !Section to find out how many years are in the metfile *******
!        call get_date (startday, firstyear ,dummy,dummy)
!        call get_date (startday+num_records-1, lastyear,dummy,dummy)
!          numyears = lastyear-firstyear+1  
!        !*************************************************************
!
!        allocate(vector_of_app_dates_1(numyears), STAT = status)
!        allocate(vector_of_app_dates_2(numyears), STAT = status)
!        allocate(vector_of_app_dates_3(numyears), STAT = status)
!        allocate(vector_of_app_dates_4(numyears), STAT = status)
!        allocate(vector_of_app_dates_5(numyears), STAT = status)
!        allocate(vector_of_app_dates_6(numyears), STAT = status)
!        allocate(vector_of_app_dates_7(numyears), STAT = status)
!        allocate(vector_of_app_dates_8(numyears), STAT = status)
!        allocate(vector_of_app_dates_9(numyears), STAT = status)
!        allocate(vector_of_app_dates_10(numyears), STAT = status)
!        allocate(vector_of_app_dates_11(numyears), STAT = status)
!
!        forall(i=1:numyears) vector_of_app_dates_1(i) = jd(firstyear+i-1,applicationMonth(1), applicationDay(1))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_2(i) = jd(firstyear+i-1,applicationMonth(2), applicationDay(2))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_3(i) = jd(firstyear+i-1,applicationMonth(3), applicationDay(3))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_4(i) = jd(firstyear+i-1,applicationMonth(4), applicationDay(4))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_5(i) = jd(firstyear+i-1,applicationMonth(5), applicationDay(5))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_6(i) = jd(firstyear+i-1,applicationMonth(6), applicationDay(6))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_7(i) = jd(firstyear+i-1,applicationMonth(7), applicationDay(7))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_8(i) = jd(firstyear+i-1,applicationMonth(8), applicationDay(8))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_9(i) = jd(firstyear+i-1,applicationMonth(9), applicationDay(9))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_10(i)= jd(firstyear+i-1,applicationMonth(10),applicationDay(10))-startday+1
!        forall(i=1:numyears) vector_of_app_dates_11(i)= jd(firstyear+i-1,applicationMonth(11),applicationDay(11))-startday+1
!
!        !Convert to Absolute Mass; area is in sq meters; apply_mass is kg/ha
!        AbsoluteMass1 = applicationMass(1)*area/10000.  !10000 m2 per hA
!        AbsoluteMass2 = applicationMass(2)*area/10000.
!        AbsoluteMass3 = applicationMass(3)*area/10000.
!        AbsoluteMass4 = applicationMass(4)*area/10000.
!        AbsoluteMass5 = applicationMass(5)*area/10000.
!        AbsoluteMass6 = applicationMass(6)*area/10000.
!        AbsoluteMass7 = applicationMass(7)*area/10000.
!        AbsoluteMass8 = applicationMass(8)*area/10000.
!        AbsoluteMass9 = applicationMass(9)*area/10000.
!        AbsoluteMass10 = applicationMass(10)*area/10000.
!        AbsoluteMass11 = applicationMass(11)*area/10000.
!
!        m2_input=0.
!        m1_input = 0.
!        
!        do i=1, numyears
!            if (vector_of_app_dates_1(i) >0 .AND.  vector_of_app_dates_1(i) < num_records) then 
!                          m1_input(vector_of_app_dates_1(i)) =m1_input(vector_of_app_dates_1(i))+AbsoluteMass1
!            end if
!
!            if (vector_of_app_dates_2(i) >0 .AND.  vector_of_app_dates_2(i) < num_records) then 
!                          m1_input(vector_of_app_dates_2(i)) =m1_input(vector_of_app_dates_2(i))+AbsoluteMass2
!            end if
!
!            if (vector_of_app_dates_3(i) >0 .AND.  vector_of_app_dates_3(i) < num_records) then 
!                          m1_input(vector_of_app_dates_3(i)) =m1_input(vector_of_app_dates_3(i))+AbsoluteMass3
!            end if
!
!            if (vector_of_app_dates_4(i) >0 .AND.  vector_of_app_dates_4(i) < num_records) then 
!                          m1_input(vector_of_app_dates_4(i)) =m1_input(vector_of_app_dates_4(i))+AbsoluteMass4
!            end if
!
!            if (vector_of_app_dates_5(i) >0 .AND.  vector_of_app_dates_5(i) < num_records) then 
!                          m1_input(vector_of_app_dates_5(i)) =m1_input(vector_of_app_dates_5(i))+AbsoluteMass5
!            end if
!
!            if (vector_of_app_dates_6(i) >0 .AND.  vector_of_app_dates_6(i) < num_records) then 
!                          m1_input(vector_of_app_dates_6(i)) =m1_input(vector_of_app_dates_6(i))+AbsoluteMass6
!            end if
!         
!            if (vector_of_app_dates_7(i) >0 .AND.  vector_of_app_dates_7(i) < num_records) then 
!                          m1_input(vector_of_app_dates_7(i)) =m1_input(vector_of_app_dates_7(i))+AbsoluteMass7
!            end if   
!            
!            if (vector_of_app_dates_8(i) >0 .AND.  vector_of_app_dates_8(i) < num_records) then 
!                          m1_input(vector_of_app_dates_8(i)) =m1_input(vector_of_app_dates_8(i))+AbsoluteMass8
!            end if   
!            
!            if (vector_of_app_dates_9(i) >0 .AND.  vector_of_app_dates_9(i) < num_records) then 
!                          m1_input(vector_of_app_dates_9(i)) =m1_input(vector_of_app_dates_9(i))+AbsoluteMass9
!            end if   
!                   
!            if (vector_of_app_dates_10(i) >0 .AND.  vector_of_app_dates_10(i) < num_records) then 
!                          m1_input(vector_of_app_dates_10(i)) =m1_input(vector_of_app_dates_10(i))+AbsoluteMass10
!            end if   
!               
!            if (vector_of_app_dates_11(i) >0 .AND.  vector_of_app_dates_11(i) < num_records) then 
!                          m1_input(vector_of_app_dates_11(i)) =m1_input(vector_of_app_dates_11(i))+AbsoluteMass11
!            end if   
!
!        end do
!
!        !At this point, all mass is in the vector m1_input, regardless of the water level.  THe following
!        !lines place the mass in m1_input into the vector m2_input if the water level is at the minimum depth.
!
!        where (daily_depth == minimum_depth)
!            m2_input = m1_input
!            m1_input=0.
!        end where
!            
!   end subroutine ParentMass
            
        
          
   !*******************************************************************************    
   subroutine DegradateProduction(j)
      use nonInputVariables, ONLY: num_records,degradateProduced1,degradateProduced2, v1,v2,    &
               k_photo, k_hydro, k_aer_aq,capacity_1,aqconc_avg1,aqconc_avg2,k_anaer_aq,capacity_2 
      use variables, ONLY: xPhoto, xHydro, xAerobic,xBenthic,Time_int, mwt
      implicit none               
      integer,intent(in) :: j
      real(8) :: MWTRatio

      MWTRatio = MWT(j+1)/MWT(j)
    
      degradateProduced1 = MWTRatio*(xPhoto(j)*k_photo*v1 + xHydro(j)*k_hydro*v1 + xAerobic(j)*k_aer_aq*capacity_1)*aqconc_avg1(:,j)*Time_int
      degradateProduced2 = MWTRatio*(xHydro(j)*k_hydro*v2 + xBenthic(j)*k_anaer_aq*capacity_2)*aqconc_avg2(:,j)*Time_int 
             
      !Degradate production is delayed one time step to approximate the process and to maintain analytical solution for time step  
      degradateProduced1(2:num_records)= degradateProduced1(1:num_records-1)
      degradateProduced2(2:num_records)= degradateProduced2(1:num_records-1)
      degradateProduced1(1)= 0.
      degradateProduced2(1)= 0.

   end subroutine DegradateProduction
        
end module mass_inputs