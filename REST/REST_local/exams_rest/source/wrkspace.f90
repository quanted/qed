! file WRKSPACE.F90 -- storage for integration routines.
! Revised 02-May-1997 - L.A. Burns
module Integrator_Working_Storage
Implicit None
Save
real (kind (0D0)) :: ABSERR, RELERR, TINIT
real (kind (0D0)), dimension(:), allocatable :: WORK
integer :: IBACK, ISOO, IUNIT
! IBACK reminds the DRIVMn routines which integration method was requested.

! ISOO  signals which integrator will be requested, and whether the work
! is complete.
! ISOO=0 at the successful completion of integration.
! ISOO=2 if more work will be done with the ADAM-PECE integrator.
! ISOO=3 if more work will be done with the Gear's method integrator.

integer, dimension(:), allocatable :: IWORK
logical ABEXIT
! ABEXIT is a logical variable used to direct reentry via
! a CONTINUE issued following abnormal exit from integrators
end module Integrator_Working_Storage
