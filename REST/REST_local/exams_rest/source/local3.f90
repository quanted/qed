module Process_Controls
! File LOCAL3.F90
use Initial_Sizes
Implicit None
Save
! Revised 25 September 1984 by L.A. Burns
! This file holds variables needed in FIRORD and its subroutines
! Switches to control subroutine calls:
LOGICAL :: BIOSW, HYDRSW, PHOTSW, PRODSW, REDSW, VOLSW
! PHOTSW -- photochemical processes
! BIOSW  -- biotransformations
! VOLSW  -- volatilization
! HYDRSW -- hydrolytic transformations
! PRODSW -- product transformation chemistry
! REDSW  -- reductive transformations

! Local computational variables:
real (kind (0D0)) ::AVELIT(7), BOTLIT, BOTLAM(46), WAVEL(46)
real (kind (0E0)), allocatable :: KDPL(:,:), OXRADL(:), S1O2L(:)
real :: TOTETA(46)
! KDPL is local value of direct light absorption by compound
! (units /hr) specified by ion and segment for transfer to
! product chemistry subroutine (dimensions 7 x KOUNT)
! OXRADL is internal (corrected) value of oxidant radicals for each segment
! S1O2L is concentration of singlet oxygen in each segment
end module Process_Controls
