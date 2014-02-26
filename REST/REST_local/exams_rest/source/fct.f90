module define_f
implicit none
contains
subroutine FCT(TIME,Y,DY)
! FCT computes total derivatives for the integrators
! Revised 18 July 1983 (LAB) for mode 3 operations.
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
real (kind (0D0)), intent (in) :: Y(:), TIME
! Y is constituent concentration (mg/L) referred to the
!  AQUEOUS phase of the compartment
real (kind (0D0)), intent (out) :: DY(:)
! Local variables for this subroutine
integer :: I, J, K, K1, N
! N maps the 2-dimensional matrices onto column-major order Y, DY via
! y(kount,kchem) => y(kount*kchem) => y(iv)
! y(j,k) => y(iv) where iv = (k-1) * kount) + j
! 
! Condensed equations for time-trace computations within stable data domains
N = 0
chemicals: do K = 1, KCHEM
   segments: do J=1,KOUNT ! Compute part of derivative due to external loads
      N=N+1
!      if (N /= (k-1)*kount+j) then
!      write (*,*) ' N= ', N, ' should be ', (k-1)*kount+j
!      end if
      DY(N) = CONLDL(J,K)-Y(N)*TOTKL(J,K)     ! and dissipative processes
!     DY(J,K) = CONLDL(J,K)-Y(J,K)*TOTKL(J,K) ! and dissipative processes
      internal_loads: do I = 1, KOUNT         ! Add in internal (recycle) load
!       DY(J,K) = DY(J,K)+Y(I,K))*INTINL(I,J,K)
        DY(N) = DY(N)+Y((K-1)*KOUNT+I)*INTINL(I,J,K)
      end do internal_loads
      products: do K1 = 1, KCHEM              ! Add in product loads
        DY(N) = DY(N)+YIELDL(K,K1,J)*Y((K1-1)*KOUNT+J)
!       DY(J,K) = DY(J,K)+YIELDL(K,K1,J)*Y(J,K1)
      end do products
   end do segments
end do chemicals
return
end Subroutine FCT
end module define_f
