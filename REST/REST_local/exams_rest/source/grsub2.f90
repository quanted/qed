subroutine GRSUB2(Y,W,IPS,WT,YP,C,ERROR,SAVER,FOURU,NEQN)
! revised 7-JUN-1983 by L.A. Burns
! revised 15-APR-87 (LAB) for high precision operations
! revised 05-Feb-99 for floating point comparisons
! revised 22 January 2001 for simplified call structure for FDER
use local_gear_data
use Gear_data
use Floating_Point_Comparisons
Use Define_f
Implicit None
! computational variables
real (kind (0D0)) :: CNORM, FOURU, GFACT
integer :: NEQN, J,J2,I,ITER
integer, save :: J1
integer :: IPS(NEQN)
real (kind (0D0)) :: Y(NEQN,7), YP(NEQN), WT(NEQN), W(NEQN,NEQN), &
   C(NEQN), ERROR(NEQN), SAVER(NEQN,7)
logical :: Skip_iterations

Skip_iterations = .false.
CONVRG = .false.
Newton: do ! Solve for Y at Time+H by using Newton iteration
   Time = Time + H
   ! Obtain starting value for iteration by multiplying Y by Pascal triangle
   ! matrix, and initialize ERROR(*) and the iteration counter ITER.
   do J = 2, KP1
      do J2 = K, J-1, -1
         do I = 1, NEQN
            Y(I,J2) = Y(I,J2)+Y(I,J2+1)
         end do
      end do
   end do
   ERROR = 0.0
   ITER  = 0
   ! W(*,*) is reevaluated only if convergence has already failed, or
   ! if there has been a change of order or stepsize.
   ! W is not reevaluated during the iteration.
   ! (NEQN=1 is treated as a special case.)
   call FCT (Time,Y(1:neqn,1),YP)
   NFE = NFE+1
   if (.not. IWEVAL < 1) then
      call FDER (W)
      IWEVAL = -1
      if (NEQN == 1) then
         W(1,1) = 1.0 + W(1,1)*A(1)*H
         Skip_iterations = (W(1,1) .Equals. 0.0)
      else
         AHINV = 1.0/(A(1)*H)
         do I = 1, NEQN
           W(I,I) = W(I,I)+AHINV
         end do
         ! LU_DECOMP performs an LU factorization of W, with partial pivoting.
         ! IPS(*) is used to hold information on the row interchanges.
         ! C is used for working storage.
         ! J1 is set to -1 if W is found to be singular.

         Call LU_Decomp(NEQN, W, IPS, J1)
         Skip_iterations = (J1 < 0)
       end if
   end if
   ! Up to 6 iterations are taken. The iteration is terminated when the norm
   ! of the correction C(*) is less than BND. The successive corrections are
   ! accumulated in ERROR(*).
   Do_not_skip_iterations: if (.not. Skip_iterations) then
      Iterations: do ITER = 1,6
         if (ITER/=1) then
            call FCT (Time,Y(1:neqn,1),YP)
            NFE = NFE+1
         end if
         If (NEQN == 1) Then
            C(1) = (Y(1,2)-YP(1)*H)/W(1,1)
         else! Solve for C(*) using factorized form of W returned by LU_DECOMP
            C = (Y(:,2)-YP(:)*H)*AHINV
            ! Should J1 be -1 then a singular matrix is indicated; its
            ! inclusion in the call list is a fail-safe protection from things
            ! we hope can't happen.
            Call LU_Solve (NEQN, W, C, IPS, J1)
         End If
         ! Apply the correction to Y(*,1) and Y(*,2), and add it to ERROR(*).
         ! Compute the norm of C and test whether convergence was achieved.
         CNORM = 0.0
         do I = 1, NEQN
           Y(I,1) = Y(I,1)+A(1)*C(I)
           Y(I,2) = Y(I,2)-C(I)
           ERROR(I) = ERROR(I)+C(I)
           CNORM = dmax1(CNORM,dabs(C(I)/WT(I)))
         end do
!        Convergence tests:
!        If any component of the solution is negative...
!         If (Any(Y(1:NEQN,1) .LessThan. 0.0D+00)) cycle Iterations
!        If the norm of "C" is too large...
         if (CNORM .GreaterThan. BND) cycle Iterations
         CONVRG = .true.
         return
      end do Iterations
   end if Do_not_skip_iterations

   ! The iteration did not converge. W will be reevaluated for another
   ! attempt. H is reduced to H/4, unless this is the first failure
   ! and W was not reevaluated for it.
   Time = TOLD
   if (IWEVAL /= 0) then
      H = 0.25*H
      if (dabs(H) .GreaterThanOrEqual. HMIN) then
                                 ! Restore Y(*,1) and go to block 1 for
                                 ! an attempt with the new stepsize.
         do I = 1, NEQN
            Y(I,1) = SAVER(I,1)
         end do
         CONVRG = .false.
         return
      end if
   end if
   do J = 1, KP1      ! Restore Y
      do I = 1, NEQN
         Y(I,J) = SAVER(I,J)
      end do
   end do
   ! If this is the first convergence failure, try again with W reevaluated.
   IWEVAL = 1
   if (dabs(H) .GreaterThanOrEqual. HMIN) then
      cycle Newton
   else  ! Convergence could not be achieved at smallest possible stepsize.
         ! Increase EPS to a value which will allow convergence and return.
      GFACT = max(CNORM/BND,2.0D+00)
      EPS = EPS*GFACT*(1.0D+00+FOURU)
      H = dsign(HMIN,H)
      ICRASH = 3
      exit Newton
   endif
end do Newton
return
contains

  Subroutine LU_Decomp(N, A, Ipvt, Js)
    ! Decomposes a double precision matrix by Gaussian elimination.
    ! Uses "LU_Solve" to compute solutions to linear systems.
    ! Input
    !    N = order of the matrix.
    !    A = NxN matrix to be triangularized.
    ! Output
    !    A  contains an upper triangular matrix  U  and a permutated
    !       version of a lower triangular matrix  I-L  such that
    !       (permutation matrix)*A = L*U .
    !    Ipvt = the pivot vector.
    !           Ipvt(k) = the index of the k-th pivot row
    !           Ipvt(N) = (-1)**(number of interchanges)
    !    Js = exit status
    !           1: the LU factorization of A was successful
    !          -1: A is singular
    ! The determinant of A can be obtained on output by
    !    det(A) = Ipvt(N) * A(1,1) * A(2,2) * ... * A(N,N).
    ! Routines LU_Decomp and LU_Solve from the book Computer Methods
    ! for Mathematical Computations, by Forsythe, Malcolm, and Moler,
    ! Prentice-Hall, Englewood, Cliffs, NJ (1977).
    ! Developed by George Forsythe, Mike Malcolm, and Cleve Moler.
    !
    ! History:
    ! From: http://www.antennas.duth.gr/cdroms/NETLIB/netlib/fmm/00_index.htm
    ! decomp.f processed by SPAG 6.05Kc at 14:20 on 12 Mar 1999
    ! Processed by "to_f90" on Fri Mar 12 14:23:25 1999
    ! Modified for use in EXAMS, replacing older "decomp" subroutine.

    Use Floating_Point_Comparisons
    Implicit None
    Integer,           Intent(in)    :: N
    Real(Kind(0D0)),   Intent(inout) :: A(:,:)
    Integer,           Intent(out)   :: Ipvt(:)
    Integer,           Intent(out)   :: Js

    Real(Kind(0D0)), Parameter :: Zero = 0.0D+00
    Real(Kind(0D0)) :: t
    Integer         :: i, j, k, m

    Js = -1
    Ipvt = 0
    Ipvt(N) = 1
    If (N == 1) Then ! 1-by-1
       If (A(1,1) .Equals. Zero) Return
       Js = 1
       Return
    End If

    ! Gaussian elimination with partial pivoting
    Gaussian_Elimination: Do k = 1, N - 1
       ! Find pivot
       m = k
       Do i = k + 1, N
          If (Abs(A(i,k)) .GreaterThan. Abs(A(m,k))) m = i
       End Do
       Ipvt(k) = m
       If (m /= k) Ipvt(N) = -Ipvt(N)
       t = A(m,k)
       A(m,k) = A(k,k)
       A(k,k) = t

       ! If the pivot is zero the matrix A is singular.
       If (t .Equals. Zero) Return

       ! Compute multipliers
       Do i = k + 1, N
          A(i,k) = -A(i,k)/t
       End Do

       ! Interchange and eliminate by columns
       Interchange: Do j = k + 1, N
          t = A(m,j)
          A(m,j) = A(k,j)
          A(k,j) = t
          If (t .Equals. Zero) Cycle Interchange
          Do i = k + 1, N
             A(i,j) = A(i,j) + A(i,k)*t
          End Do
       End Do Interchange
    End Do Gaussian_Elimination
    If (A(N,N) .Equals. Zero) Return
    Js = 1
  End Subroutine LU_Decomp

  Subroutine LU_Solve(N, A, B, Ipvt, Js)
    ! Solution of linear system, A*x = b
    ! Must not be used if "LU_Decomp" has detected a singularity.
    ! Input
    !    N = order of matrix.
    !    A = triangularized matrix obtained from "LU_Decomp".
    !    B = right hand side vector.
    !    Ipvt = pivot vector obtained from "LU_Decomp".
    !    Js = exit status from LU_Decomp
    !           1: the LU factorization of A was successful
    !          -1: A is singular
    ! Output
    !    B = solution vector, "x"
    Implicit None
    Integer,         Intent(in)    :: N, Js, Ipvt(:)
    Real(Kind(0D0)), Intent(in)    :: A(:,:)
    Real(Kind(0D0)), Intent(inout) :: B(:)
    Integer                        :: i, k, m
    Real(Kind(0D0))                :: t

    If (Js < 0) return
    If (N == 1) Then
       B(1) = B(1)/A(1,1)
       Return
    End If

    ! Forward elimination
    Do k = 1, N - 1
       m = Ipvt(k)
       t = B(m)
       B(m) = B(k)
       B(k) = t
       Do i = k + 1, N
          B(i) = B(i) + A(i,k)*t
       End Do
    End Do

    ! Back substitution
    Do k = N, 2, -1
       B(k) = B(k)/A(k,k)
       t = -B(k)
       Do i = 1, k - 1
          B(i) = B(i) + A(i,k)*t
       End Do
    End Do
    B(1) = B(1)/A(1,1)
  End Subroutine LU_Solve

end Subroutine GRSUB2
