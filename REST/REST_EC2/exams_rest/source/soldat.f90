module SOLAR_data ! in file "soldat.f90"
! Revised 25 September 1984 by L.A. Burns
! Revised 22 Feb 1996 by L.A. Burns
Implicit None
Save
real, dimension(46) :: AERDEP, HLAM, OZDEP, RAYDEP
! AERDEP is aerosol (turbidity) optical depth.
! HLAM is solar input at the top of the atmosphere at the date to be
!    processed--i.e., solar constant/(square of the radius vector)
! OZDEP is the ozone optical depth, i.e., the product of the
!    amount of ozone in the atmosphere OZONEG (in cm NTP), the ozone
!    absorption coefficients (K3), and the elevation correction NHI(3)
! RAYDEP is Rayleigh optical depth corrected for ground station
!    elevation: RAYFAC * NHI(1); the latter the pressure correction

real :: AIREFL, BREW, CLCD, EFF, EMMHI, G3T3, GT1GT2,ONEFF, REFRAT, SLSD, TTEE

! BREW is reflection computed according to Brewster's law (when
!    sum of the angles of incidence and reflection is 90 degrees).
! CLCD is cos(latitude) * cos(solar declination)
! EFF, ONEFF, G3T3, GT1GT2, TTEE are computational elements for skylight.
! EMMHI is product of vertical beam intensity (HIBEAM) and EMM
!    (the latter the "M" function), for skylight computations.
! REFRAT is reflection for normal incidence of light beam.
! SLSD is sin(latitude) * sin(solar declination)

! REFIND is refractive index of water at 20 C, from Jerlov's book
! p 23, computed by linear interpolation between pairs of values.
real, dimension(46) :: REFIND=(/1.3662,1.3652,1.3643,1.3634,1.3625,1.3615,&
1.3606,1.3597,1.3588,1.3578,1.3569,1.3565,1.3561,1.3557,1.3553,1.3548,&
1.3544,1.3539,1.3528,1.3511,1.3495,1.3479,1.3467,1.3456,1.3444,&
1.3433,1.3424,1.3415,1.3407,1.3399,1.3393,1.3387,1.3381,1.3375,&
1.3369,1.3364,1.3355,1.3346,1.3336,1.3327,1.3322,1.3316,1.3310,&
1.3303,1.3293,1.3283/)

real :: Xtes
! Xtes is used to prevent underflows in the light extinction routines.
! It is set (xtes = abs(log(tiny(1.0E+00)))) in subroutine Announ.

integer :: LAMBDA
! LAMBDA points to wavelength intervals

End module SOLAR_data
