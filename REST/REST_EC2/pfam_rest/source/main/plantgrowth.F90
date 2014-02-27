module grow_plants
!  Written by Dirk F. Young (Virginia, USA).
contains
    subroutine plant_growth
        !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        !this routine (which was taken from FastPRZM) creates a vector or plant fractional growth (plant_factor), given the days that the plant was at zero
        !hieght. day at 100% ht, and day of removal.  Any combination of dates can be used as long as they dont overlap one another.
        !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        use variables, ONLY: PlantZero_day ,PlantZero_month,PlantFull,PlantRemove
        use nonInputVariables, ONLY: num_records, plant_factor, startday
        use utilities_module
        implicit none

        ! local variables
        integer,allocatable,dimension(:) ::stage1,stage2,stage3
        integer,allocatable,dimension(:) ::plant_year
        integer ::status,i

        integer :: enddate, endyear,firstyear,number_of_years
        integer :: dummy
        integer :: j
        integer :: a_limit,b_limit,a_diff,b_diff,b_limit_2,g_limit
        integer :: d_size
        integer,allocatable,dimension(:) :: me, c
        real ,allocatable,dimension(:) :: rme
        real,allocatable,dimension(:) :: d,fract

        !determine number of years in simulation

        enddate = startday +num_records-1
        call get_date (enddate, endYEAR,dummy,dummy)
        call get_date (startday,firstYEAR,dummy,dummy)

        number_of_years = endyear-firstyear+1

        allocate(stage1(number_of_years), STAT = status)
        allocate(stage2(number_of_years), STAT = status)
        allocate(stage3(number_of_years), STAT = status)
        allocate(plant_year(number_of_years), STAT = status)

        allocate(me(number_of_years), STAT = status)
        allocate(rme(number_of_years), STAT = status)
        allocate(c(number_of_years), STAT = status)

        forall(i=1:number_of_years) plant_year(i) = firstYEAR+i-1
        forall(i=1:number_of_years) stage1(i) = jd(plant_year(i),PlantZero_month,PlantZero_day)-startday+1

        stage2 = stage1+PlantFull
        stage3 = stage1+PlantRemove

        plant_factor = 0.
        c=0

        me = stage2- stage1
        c = me+1     !number of days from emer to stage2 (inclde first and last)
        rme =real(me)

        d_size = maxval(c)
        allocate(d(d_size),fract(d_size), STAT = status)

        forall(j=1:d_size) d(j) = real(j-1)  !create an array from zero to number of days between emerg and stage2


        ! min and max functions are in here in case plant growth dates exceed simulation dates
        !This loop maps the stage1,stage2, stage3 interval onto the same time refernce as the metfile
        do i=1,number_of_years

            fract(1:c(i)) = d(1:c(i))/rme(i)  !array of fractional growth (i.e., 1,0.25,0.5,0.75,1.0)

            a_limit = max(stage1(i),1)  !index for plant factor cannot be negative, must start at 1
            b_limit = min(stage2(i),num_records)!index for plant factor cannot be >num_records

            a_diff = a_limit-stage1(i)+1 !amount to adjust index by
            b_diff = stage2(i) -b_limit+1

            if (a_limit <= num_records) then  !preclude the case where crop is out of range of simulation
            !these are the plant factors between emergence and stage3
            plant_factor(a_limit:b_limit) = fract(a_diff:b_diff)
            end if

            !do stage2 to stage3 (height =1)
            b_limit_2 = max(1,stage2(i))
            g_limit = min(num_records,stage3(i))

            if (g_limit >= 1) then  !preclude the case where crop is out of range of simulation
            plant_factor(b_limit_2:g_limit)= 1
            end if

        end do

        deallocate (d,fract, STAT= status)
    end subroutine plant_growth


end module grow_plants


