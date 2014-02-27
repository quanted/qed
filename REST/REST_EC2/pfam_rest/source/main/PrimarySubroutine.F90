module PrimarySubroutineRoutines
!  Written by Dirk F. Young (Virginia, USA).
contains


!***************************************************************************
! THIS IS THE ANALYTICAL SOLUTION TO THE EFED SUBSETS OF THE EXAMS MODEL. 
!
! Attempt was made to put all EXAMS partameters in CAPITAL LETTERS
! errors are reported in fort.11
!___________________________________________________________________________
subroutine PrimarySubroutine
    use outputprocessing
    use mass_transfer
    use grow_plants
    use flood
    use metfileprocessing
    use chemicaltransformation    
    use variables, ONLY: aer_aq,anae_aq,temp_ref_aer , temp_ref_anae,drysoil,temp_ref_dry,nchem
    use allocations
  
    implicit none              
    !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    integer, parameter::n_size=90   !should equal the size of maximum window for averaging period (i.e., 90 days)
    integer :: eof_met         !flag to idicate end of met file error
    integer :: ierror           !met file open error flag
    integer :: i
    !*************  Met file Calculations  *****************************************
    !count met file records for array allocation,
    call count_met( ierror) !returns: num_records= number of days in simulation
    if (ierror /=0) then
            write (11,*) 'no met file'
            return
    end if
    !******************************************************************************
    call allocation1        !allocates all the num record variables
    call initializations    !located in the allocations module
    !******************************************************************************
    call read_metfile(eof_met) 
        if (eof_met /=0) then
            write (11,*) 'error: met file out of whack'
            return
        end if
    !******************************************************************************  
       
    call plant_growth    !returns the plant factor (daily plant size)
    call flood_control   !outputs the daily paddy depths
    call omega_mass_xfer  
    
    do i=1, nchem 
       call transformation(i)
    end do
       

    call process_output
    

    
end subroutine PrimarySubroutine
!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX



end module PrimarySubroutineRoutines



