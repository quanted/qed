module mass_transfer
!  Written by Dirk F. Young (Virginia, USA).
contains
subroutine omega_mass_xfer
!This subroutine calculates the littoral to benthic mass transfer coefficient
use variables, ONLY:  D_over_dx, benthic_depth
use nonInputVariables, ONLY: omega
implicit none


!real(8),intent(out):: omega     !mass transfer coefficient referenced to benthic region [per sec]

!real(8) :: CHARL

!According to EFED standard practice, the parameter CHARL is one half the sum
!of the distance between benthic and water column midpoints.  D. Young has 
!raised issues with this (see SAP 2004 document).  In the mean time, the omega value
!will remain constant at the initial value as determined by current EFED practice
!as defined here.  Better estimates should be looked in to:

!charl = 0.5*(benthic_depth + depth_0)

! charl = massXferLength  !user input for mass transfer length


!Note: in EXAMS, DSP is a total dispersion coefficient
!based on total volume in benthic region

    omega = D_over_dx/benthic_depth !(m3/hr)/(3600 s/hr)


end subroutine omega_mass_xfer













end module mass_transfer