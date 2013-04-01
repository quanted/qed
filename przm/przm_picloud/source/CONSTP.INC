!     These COMMON block allows for the storage of machine dependent
!     numeric constants for the PRZM2 model.

! RPREC  - the number of (decimal) digits of precision of a real number.
! DPREC  - the number of (decimal) digits of precision of a double.
! R0MIN  - the smallest (positive) representable real number.
! RP1MIN - the minimum representable real number greater than (plus) 1.0.
! R0MAX  - the largest representable real number.
! D0MIN  - the smallest (positive) representable double.
! DP1MIN - the minimum representable double greater than (plus) 1.0.
! D0MAX  - the largest representable double.

      INTEGER RPRec , DPRec
      REAL R0Min , RP1min , R0Max
      DOUBLE PRECISION D0Min , DP1min , D0Max
      COMMON /IPCONS/ RPRec , DPRec
      COMMON /RPCONS/ R0Min , RP1min , R0Max
