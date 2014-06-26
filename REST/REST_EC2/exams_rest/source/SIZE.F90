module Initial_Sizes ! file size.f90
! Revised 07-SEP-1985, L.A. Burns, data handlers
! Text of comments revised 11/18/88, 07-Dec-1999, 12-Feb-2001, 2004-05-24
! This file contains the Parameter statements that govern the
! maximum number of environmental segments and chemicals for daf storage
Implicit None
Save
! Number of chemicals set at 5, compartments at 100
integer, parameter :: NCHEM=5, NPX=100
! NCHEM is the number of chemicals with loading patterns in exams.daf
! NPX is the number of segments storable in environments in exams.daf
! NEQN (=nchem*npx) is the number of equations involved.
! Used in integration routines, set when called as KCHEM * KOUNT
!integer, parameter :: NWORK=NEQN*NEQN+17*NEQN, TOTLEN=2*NWORK+NEQN
! NWORK is the size of the working storage for the integration
!   (NWORK must be at least NEQN*NEQN+17*NEQN and >= 19).
! TOTLEN is the number of 4-byte (REAL*4) spaces in WORK+IWORK.
!   NWORK is twice as big because WORK is real (kind (0D0)).
!   When integers occupy 2 bytes, and the length of the Fortran
!   Numerical Storage Unit (NSU) is four bytes,
!     set TOTLEN=2*NWORK+NEQN/2
! For the preferred implementation using a single NSU of 4 bytes,
!     set TOTLEN=2*NWORK+NEQN.

integer, parameter :: KountMult = 6
! KountMult is the maximum number of transport pathways in any environment
integer, parameter :: NCON=NPX*KountMult
! NCON is the maximum number of transport pathways -- in a fully
!    three-dimensional model, each segment has 6 faces. In Exams
!    the number of permitted connections for an environment is dynamically
!    linked to KOUNT as some multiple thereof (KountMult above).
!    NCON establishes the total number of connection specifications
!    that can be stored in exams.daf based on NPX.
integer, parameter :: NTRAN = 250
! NTRAN is the maximum number of transformation pathways that can
! be specified as producing autochthonous chemical loadings.

integer, parameter :: NMODE=3, MAXDAT=13
! NMODE is the number of operational modes in this version.
! MAXDAT is the maximum number of data blocks that can be loaded
! into the environmental descriptors -- 12 monthlies + averages
!
integer, parameter :: MAXMAS=800
! MAXMAS is the maximum number of allochthonous chemical pulses.
! The current value is 800 (as in PRZM parameter NAPP).
!
integer, parameter :: FILDAT=57 ! Number of DAF control parameters
! The 57 control pointers for EXAMS' direct access file (i.e., the number of
! integer variables per chemical, number of Reals per chemical, etc., etc.)
! are held in the first few records of the file.
! The number of (integer-valued) pointers required to decode the DAF structure
! is given by FILDAT. The number of header records needed to hold FILDAT
! integers is computed by the Utility program based on the value of VARIEC.
! The content of the header records is reported by the Utility program when
! runs, as the last section of the report file (for0007.dat).
end module Initial_Sizes
