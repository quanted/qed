subroutine CHKSUB(ARGS,INDX,LOWUP,IT)
! Purpose: To validate subscript ranges
! Subroutines required: none
! Revision date 24-APR-87 (LAB)
! conversion to Fortran90 6/5/96
! Revision 08-Feb-1999 to use floating point comparisons
! Revision 07-Feb-2001 to support dynamic memory allocation
! ITS indicates the type of variable
! ---               ----------------
!  1                 scalar
!  2                 vector
!  3                 2-D matrix
!  4                 3-D matrix
! Revision 2004-05-17 to include QTBTWG and QTBTSG biolysis study temperatures
use Alias_Transfer
use Model_Parameters
use Floating_Point_Comparisons
use Global_Variables
Implicit None
real :: ARGS(10), ARG1, ARG2, ARG3
integer :: INDX, LOWUP(6), IT
integer :: K, I, ITS, LOW1, LOW2, LOW3, UP1, UP2, UP3
! determine parameter group and offset variable within that group
K = 0
Outer: do
   do I = 1, NOCOM
      K = K+COMVAR(I)
      if (K >= INDX) exit Outer
   end do
   IT = -3 ! completion of inner loop indicates fault
   return
end do Outer
ICOM = I
IVAR = K-COMVAR(I)
IVAR = INDX-IVAR
! Limits of storage loops
LOW1 = 1
LOW2 = 1
LOW3 = 1
UP1 = 1
UP2 = 1
UP3 = 1

call Check_Size ! to determine the currently allocated size of the variable

ITS = TS(INDX)
if (ITS == 1) then ! scalar
   call Finisher (LOWUP)
   return
end if
! At least one subscript specified
ARG1 = ARGS(1)
if (int(ARG1) == -1) then ! '*' specified
   LOW1 = 1
   UP1 = TCL1(INDX)
   ARG1 = 1.0
else ! Single element defined
   LOW1 = int(ARG1)
   UP1 = int(ARG1)
end if
if (((ARG1).LessThan.(1.0)) .or. &
      ((ARG1).GreaterThan.(real(TCL1(INDX)))))  then
   IT =3
   return
end if
if (ITS == 2) then ! vector
   call Finisher (LOWUP)
   return
end if

! At least two subscripts specified
ARG2 = ARGS(2)
if (int(ARG2) == -1) then ! '*' specified
   LOW2 = 1
   UP2 = TCL2(INDX)
   ARG2 = 1.0
else
   LOW2 = int(ARG2)
   UP2 = int(ARG2)
end if
if ( (ARG2 .LessThan. 1.0) .or. &
     (ARG2 .GreaterThan. (real(TCL2(INDX)))) &
   ) then
   IT =3
   return
end if
if (ITS == 3) then ! matrix, two subscripts
   call Finisher (LOWUP)
   return
end if

! Matrix with 3 subscripts specified
ARG3 = ARGS(3)
if (int(ARG3) == -1) then ! '*' specified
   LOW3 = 1
   UP3 = TCL3(INDX)
   ARG3 = 1.0
else
   LOW3 = int(ARG3)
   UP3 = int(ARG3)
end if
if (((ARG3).LessThan.(1.0)) .or. &
      ((ARG3).GreaterThan.(real(TCL3(INDX))))) then
   IT =3
   return
end if
call Finisher (LOWUP)
return

contains
subroutine Finisher (LOWUP)
   integer, dimension (:) :: LOWUP
   ! Store subscripts in array to reduce argument transmission
   LOWUP(1) = LOW1
   LOWUP(2) = LOW2
   LOWUP(3) = LOW3
   LOWUP(4) = UP1
   LOWUP(5) = UP2
   LOWUP(6) = UP3
   IT = 0
end subroutine Finisher

subroutine Check_Size
! Developed 07-Feb-2001 from GETVAR to support dynamic memory allocation
! Modified 09-April-2001 for aquatic metabolism half-lives
! Checks the current allocated dimensions of Exams' global variables
! Subroutines required: none
! Called by CHKSUB to establish size of current variable
Implicit None

Groups: select case (ICOM)
case (1) Groups ! Parameter Group: NAMEG
   select case (IVAR)
      case (1); TCL1(INDX) = size (CHEMNA) 
      case (2); ! character scalar ECONAM
      case (3); ! character scalar LOADNM
      case (4); ! character scalar PRODNM
      case (5); TCL1(INDX) = size (TYPEG)
      case (6); TCL1(INDX) = size (AIRTYG)
   end select
case (2) Groups ! Parameter Group: CONTRG
   ! These are almost all scalars and thus not reallocated; use data from daf.
   ! The variables are
   !  FIXFIL   IUNITG   MCHEMG   KCHEM   MODEG   PRSWG   MONTHG
   !  NYEARG   YEAR1G   TCODEG   CINTG   TENDG   TINITG  ABSERG
   !  RELERG
   select case (IVAR)
      case (16); TCL1(INDX) = size (EventD)
   end select
case (3) Groups ! Parameter Group: PCHEMG
   select case (IVAR)
      case (1); TCL1(INDX) = size (SPFLGG,1); TCL2(INDX) = size (SPFLGG,2)
      case (2); TCL1(INDX) = size (MWTG)
      case (3); TCL1(INDX) = size (SOLG,1);  TCL2(INDX) = size (SOLG,2)
      case (4); TCL1(INDX) = size (ESOLG,1); TCL2(INDX) = size (ESOLG,2)
      case (5); TCL1(INDX) = size (PKG,1);   TCL2(INDX) = size (PKG,2)
      case (6); TCL1(INDX) = size (EPKG,1);  TCL2(INDX) = size (EPKG,2)
   end select
case (4) Groups ! Parameter Group: PARTG
   select case (IVAR)
      case (1); TCL1(INDX)= size (KOCG)
      case (2); TCL1(INDX)= size (KOWG)
      case (3); TCL1(INDX) = size (KPBG,1);   TCL2(INDX) = size (KPBG,2)
      case (4); TCL1(INDX) = size (KPDOCG,1); TCL2(INDX) = size (KPDOCG,2)
      case (5); TCL1(INDX) = size (KPSG,1);   TCL2(INDX) = size (KPSG,2)
      case (6); TCL1(INDX) = size (KIECG,1);  TCL2(INDX) = size (KIECG,2)
   end select
case (5) Groups ! Parameter Group: VOLATG
   select case (IVAR)
      case (1); TCL1(INDX) = size (MPG)
      case (2); TCL1(INDX) = size (HENRYG)
      case (3); TCL1(INDX) = size (EHENG)
      case (4); TCL1(INDX) = size (VAPRG)
      case (5); TCL1(INDX) = size (EVPRG)
   end select
case (6) Groups ! Parameter Group: DPHOTG
   select case (IVAR)
      case (1); TCL1(INDX) = size(Qyield,1);  TCL2(INDX) = size(QYield,2)
                TCL3(INDX) = size(Qyield,3)
      case (2); TCL1(INDX) = size (KDPG,1);   TCL2(INDX) = size (KDPG,2)
      case (3); TCL1(INDX) = size (RFLATG,1); TCL2(INDX) = size (RFLATG,2)
      case (4); TCL1(INDX) = size(ABSORG,1);  TCL2(INDX) = size(ABSORG,2)
                TCL3(INDX) = size(ABSORG,3)
      case (5); TCL1(INDX) = size (LAMAXG,1); TCL2(INDX) = size (LAMAXG,2)
   end select
case (7) Groups ! Parameter Group: HYDROG
   select case (IVAR)
      case (1); TCL1(INDX) = size(KAHG,1); TCL2(INDX) = size(KAHG,2)
                TCL3(INDX) = size(KAHG,3)
      case (2); TCL1(INDX) = size(EAHG,1); TCL2(INDX) = size(EAHG,2)
                TCL3(INDX) = size(EAHG,3)
      case (3); TCL1(INDX) = size(KNHG,1); TCL2(INDX) = size(KNHG,2)
                TCL3(INDX) = size(KNHG,3)
      case (4); TCL1(INDX) = size(ENHG,1); TCL2(INDX) = size(ENHG,2)
                TCL3(INDX) = size(ENHG,3)
      case (5); TCL1(INDX) = size(KBHG,1); TCL2(INDX) = size(KBHG,2)
                TCL3(INDX) = size(KBHG,3)
      case (6); TCL1(INDX) = size(EBHG,1); TCL2(INDX) = size(EBHG,2)
                TCL3(INDX) = size(EBHG,3)
   end select
case (8) Groups ! Parameter Group: REDOXG
   select case (IVAR)
      case (1); TCL1(INDX) = size(KOXG,1);   TCL2(INDX) = size(KOXG,2)
                TCL3(INDX) = size(KOXG,3)
      case (2); TCL1(INDX) = size(EOXG,1);   TCL2(INDX) = size(EOXG,2)
                TCL3(INDX) = size(EOXG,3)
      case (3); TCL1(INDX) = size(K1O2G,1);  TCL2(INDX) = size(K1O2G,2)
                TCL3(INDX) = size(K1O2G,3)
      case (4); TCL1(INDX) = size(EK1O2G,1); TCL2(INDX) = size(EK1O2G,2)
                TCL3(INDX) = size(EK1O2G,3)
      case (5); TCL1(INDX) = size(KREDG,1);  TCL2(INDX) = size(KREDG,2)
                TCL3(INDX) = size(KREDG,3)
      case (6); TCL1(INDX) = size(EREDG,1);  TCL2(INDX) = size(EREDG,2)
                TCL3(INDX) = size(EREDG,3)
   end select
case (9) Groups ! Parameter Group: BIOLYG
   select case (IVAR)
      case (1); TCL1(INDX) = size(KBACWG,1); TCL2(INDX) = size(KBACWG,2)
                TCL3(INDX) = size(KBACWG,3)
      case (2); TCL1(INDX) = size(QTBAWG,1); TCL2(INDX) = size(QTBAWG,2)
                TCL3(INDX) = size(QTBAWG,3)
      case (3); TCL1(INDX) = size(KBACSG,1); TCL2(INDX) = size(KBACSG,2)
                TCL3(INDX) = size(KBACSG,3)
      case (4); TCL1(INDX) = size(QTBASG,1); TCL2(INDX) = size(QTBASG,2)
                TCL3(INDX) = size(QTBASG,3)
      case (5); TCL1(INDX) = size(QTBTWG,1); TCL2(INDX) = size(QTBTWG,2)
                TCL3(INDX) = size(QTBTWG,3)
      case (6); TCL1(INDX) = size(QTBTSG,1); TCL2(INDX) = size(QTBTSG,2)
                TCL3(INDX) = size(QTBTSG,3)
      case (7); TCL1(INDX) = size (AerMet)
      case (8); TCL1(INDX) = size (AnaerM)
   end select
case (10) Groups ! Parameter Group: TRPORT
   select case (IVAR)
      case (1); ! KOUNT
      case (2); TCL1(INDX) = size (JFRADG)
      case (3); TCL1(INDX) = size (ITOADG)
      case (4); TCL1(INDX) = size (ADVPRG)
      case (5); TCL1(INDX) = size (JTURBG)
      case (6); TCL1(INDX) = size (ITURBG)
      case (7); TCL1(INDX) = size (XSTURG)
      case (8); TCL1(INDX) = size (CHARLG)
      case (9); TCL1(INDX) = size (DSPG,1); TCL2(INDX) = size (DSPG,2)
   end select
case (11) Groups ! Parameter Group: SEDMG
   select case (IVAR)
      case (1); TCL1(INDX) = size (SUSEDG,1); TCL2(INDX) = size (SUSEDG,2)
      case (2); TCL1(INDX) = size (BULKDG,1); TCL2(INDX) = size (BULKDG,2)
      case (3); TCL1(INDX) = size (FROCG,1);  TCL2(INDX) = size (FROCG,2)
      case (4); TCL1(INDX) = size (CECG,1);   TCL2(INDX) = size (CECG,2)
      case (5); TCL1(INDX) = size (AECG,1);   TCL2(INDX) = size (AECG,2)
      case (6); TCL1(INDX) = size (PCTWAG,1); TCL2(INDX) = size (PCTWAG,2)
   end select
case (12) Groups ! Parameter Group: QUALG
   select case (IVAR)
      case (1); TCL1(INDX) = size (TCELG,1);   TCL2(INDX) = size (TCELG,2)
      case (2); TCL1(INDX) = size (PHG,1);     TCL2(INDX) = size (PHG,2)
      case (3); TCL1(INDX) = size (POHG,1);    TCL2(INDX) = size (POHG,2)
      case (4); TCL1(INDX) = size (OXRADG)
      case (5); TCL1(INDX) = size (REDAGG,1); TCL2(INDX) = size (REDAGG,2)
      case (6); TCL1(INDX) = size (BACPLG,1); TCL2(INDX) = size (BACPLG,2)
      case (7); TCL1(INDX) = size (BNBACG,1); TCL2(INDX) = size (BNBACG,2)
      case (8); TCL1(INDX) = size (PLMASG,1); TCL2(INDX) = size (PLMASG,2)
      case (9); TCL1(INDX) = size (BNMASG,1); TCL2(INDX) = size (BNMASG,2)
      case (10);TCL1(INDX) = size (KO2G,1);   TCL2(INDX) = size (KO2G,2)
   end select
case (13) Groups ! Parameter Group: PHOTOG
   select case (IVAR)
      case (1); TCL1(INDX) = size (DOCG,1);   TCL2(INDX) = size (DOCG,2)
      case (2); TCL1(INDX) = size (CHLG,1);   TCL2(INDX) = size (CHLG,2)
      case (3); TCL1(INDX) = size (CLOUDG)
      case (4); TCL1(INDX) = size (DFACG,1);  TCL2(INDX) = size (DFACG,2)
      case (5); TCL1(INDX) = size (DISO2G,1); TCL2(INDX) = size (DISO2G,2)
      case (6); TCL1(INDX) = size (OZONEG)
   end select
case (14) Groups ! Parameter Group: GEOMT
   select case (IVAR)
      case (1); TCL1(INDX) = size (VOLG)
      case (2); TCL1(INDX) = size (AREAG)
      case (3); TCL1(INDX) = size (DEPTHG)
      case (4); TCL1(INDX) = size (XSAG)
      case (5); TCL1(INDX) = size (LENGG)
      case (6); TCL1(INDX) = size (WIDTHG)
   end select
case (15) Groups ! Parameter Group: CLIMG
   select case (IVAR)
      case (1); TCL1(INDX) = size (RAING)
      case (2); TCL1(INDX) = size (EVAPG,1);   TCL2(INDX) = size (EVAPG,2)
      case (3); ! scalar LATG
      case (4); ! scalar LONGG
      case (5); TCL1(INDX) = size (WINDG,1);   TCL2(INDX) = size (WINDG,2)
      case (6); ! scalar ELEVG
      case (7); TCL1(INDX) = size (RHUMG)
      case (8); TCL1(INDX) = size (ATURBG)
   end select
case (16) Groups ! Parameter Group: FLOWG
   select case (IVAR)
      case (1); TCL1(INDX) = size (STFLOG,1);   TCL2(INDX) = size (STFLOG,2)
      case (2); TCL1(INDX) = size (STSEDG,1);   TCL2(INDX) = size (STSEDG,2)
      case (3); TCL1(INDX) = size (NPSFLG,1);   TCL2(INDX) = size (NPSFLG,2)
      case (4); TCL1(INDX) = size (NPSEDG,1);   TCL2(INDX) = size (NPSEDG,2)
      case (5); TCL1(INDX) = size (SEEPSG,1);   TCL2(INDX) = size (SEEPSG,2)
   end select
case (17) Groups ! Parameter Group: LOADSG
   select case (IVAR)
      case (1); TCL1(INDX) = size(STRLDG,1); TCL2(INDX) = size(STRLDG,2)
                TCL3(INDX) = size(STRLDG,3)
      case (2); TCL1(INDX) = size(NPSLDG,1); TCL2(INDX) = size(NPSLDG,2)
                TCL3(INDX) = size(NPSLDG,3)
      case (3); TCL1(INDX) = size(PCPLDG,1); TCL2(INDX) = size(PCPLDG,2)
                TCL3(INDX) = size(PCPLDG,3)
      case (4); TCL1(INDX) = size(DRFLDG,1); TCL2(INDX) = size(DRFLDG,2)
                TCL3(INDX) = size(DRFLDG,3)
      case (5) ! scalar PRBENG
      case (6); TCL1(INDX) = size(SEELDG,1); TCL2(INDX) = size(SEELDG,2)
                TCL3(INDX) = size(SEELDG,3)
      case (7); TCL1(INDX) = size (IMASSG)
      case (8); TCL1(INDX) = size (ISEGG)
      case (9); TCL1(INDX) = size (ICHEMG)
      case (10); TCL1(INDX) = size (IMONG)
      case (11); TCL1(INDX) = size (IDAYG)
      case (12); TCL1(INDX) = size (IYEARG)
      case (13) ! scalar SPRAYG
   end select
case (18) Groups ! Parameter Group: SPECTR
   select case (IVAR)
      case (1); TCL1(INDX) = size (CHPARG)
      case (2); TCL1(INDX) = size (TPRODG)
      case (3); TCL1(INDX) = size (NPROCG)
      case (4); TCL1(INDX) = size (RFORMG)
      case (5); TCL1(INDX) = size (YIELDG)
      case (6); TCL1(INDX) = size (EAYLDG)
   end select
end select Groups
return
end Subroutine Check_Size


end Subroutine CHKSUB
