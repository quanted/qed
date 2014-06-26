module Rates_and_Sums
! File LOCAL2.F90
! Revised 16 January 1984 (L.A. Burns) to eliminate INDEXW
! Revised 25 September 1984 (LAB) - reformulation.
! Module for communications among routines called by GHOST
!use Initial_Sizes
Implicit None
Save

real, allocatable :: KA1L(:,:), KA2L(:,:), KA3L(:,:),&
KB1L(:,:), KB2L(:,:), KB3L(:,:), KPSL(:,:,:)

real, allocatable :: NPSCOL(:), NPSFL(:), RAINFL(:), SEDFL(:,:,:),&
SEDOUL(:), SEEPSL(:), STRMFL(:), STSCOL(:), WATFL(:,:), WATOUL(:)

real, allocatable :: ACCUM2(:,:,:), ACCUM3(:,:), ACCUM4(:,:)
! ACCUM1, ACCUM2, ACCUM3, and ACCUM4 are used as accumulators
! for documenting mean values of environmental parameters.
end module Rates_and_Sums
