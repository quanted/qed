module Gear_data     ! file geardata.f90
Implicit None
save
real (kind (0D0)) :: A(7), AHINV, Time, HOLD, H, EPS
integer :: NFE, ICRASH, K, KOLD, ITST, IWEVAL
logical :: START
end module Gear_data
