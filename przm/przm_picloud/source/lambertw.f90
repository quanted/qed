Module m_LambertW

   Use General_Vars, Only:  Double
   Implicit None
   Private
   Public :: LambertW

   ! LambertW_LUN - Logical unit number for messages
   ! LambertW_Ierror - Error associated with the last call to LambertW
   ! LambertW_Message - Error associated with the last call to LambertW
   ! LambertW_Debug - truth of "Print debugging messages"
   Integer,             Public, Save :: LambertW_LUN = 6
   Integer,             Public, Save :: LambertW_Ierror = 0
   Character(Len=1024), Public, Save :: LambertW_Message = ''
   Logical,             Public, Save :: LambertW_Debug = .False.

Contains

   Subroutine LambertW (X, Wx, Principal_Branch, Nerror, X_is_offset)

      ! Computes the Lambert function, W(x), defined implicitly by:
      !
      !     W(x) * Exp(W(x)) = x
      !
      ! Principal branch, W_0(x):
      !     Domain:  -exp(-1) <= x < oo
      !     Range:   -1 <= W_0(x) < oo
      !
      ! The "Other" branch, W_{-1}:
      !     Domain:  -exp(-1) <= x < 0
      !     Range:   -oo < W_{-1}(x) <= -1
      !
      ! References:
      ! [1] Algorithm 743, Collected Algorithms from ACM.
      !     This work published in Transactions on Mathematical Software,
      !     Vol. 21, No. 2, June, 1995, p. 172-181
      !
      ! History:
      ! * Fortran 77 version downloaded from http://www.netlib.org/toms/743
      ! * Translated to Fortran 95 on 2004-02-27

      Implicit None

      Real(Double), Intent(In)  :: x      ! argument of W(x)
      Real(Double), Intent(Out) :: Wx     ! W(x)

      ! Principal_Branch = Truth of compute W0; Default value: .True.
      !        .True.   Compute W0,       the principal branch
      !        .False.  Compute W{-1},    the "other" real-valued branch
      Logical, Optional, Intent(In) :: Principal_Branch

      ! X_is_offset = determines how LambertW is to treat the argument X
      !    .True.    X is the offset from -exp(-1), so compute W(X-exp(-1))
      !    .False.   X is desired X, so compute W(X)
      ! Default value: False
      Logical, Optional, Intent(In) :: X_is_offset

      ! Nerror is the output error flag:
      !     Nerror   Description
      !     ------   -----------
      !        0     Routine completed successfully
      !        1     The offset x = #.#e## must be > 0; Computing W(x - exp(-1))
      !        2     Out of Domain: x = # must be > -Exp(-1)=-0.368
      !        3     Out of W{-1}'s domain: x = #; Domain: -Exp(-1)=-0.368 < x < 0
      Integer, Optional, Intent(Out) :: Nerror

      ! NBITS is the number of bits (less 1) in the mantissa of the
      !    floating point number number representation of the machine.
      !    It is used to determine the level of accuracy to which the W
      !    function should be calculated. This value is chosen to
      !    allow for rounding error in the final bit.
      !
      !    Most machines use a 24-bit mantissa for single precision and
      !    53-56 bits for double precision. The IEEE standard is 53
      !    bits. The Fujitsu VP2200 uses 56 bits. Long word length
      !    machines vary, e.g., the Cray X/MP has a 48-bit mantissa for
      !    single precision.

      Integer, Parameter :: nbits = Digits(x) - 1

      Integer      :: i, niter
      Logical      :: Compute_w0, Value_is_offset
      Real(Double) :: an2, delx, eta, reta
      Real(Double) :: t, temp, temp2, ts, xx, zl, zn

      ! Various mathematical constants
      Logical,      Save :: Vars_Initialized = .False.
      Real(Double), Save :: an3, an4, an5, an6, c13, c23, d12
      Real(Double), Save :: em, em2, em9, s2, s21, s22, s23
      Real(Double), Save :: tb, tb2, x0, x1
      Real(Double), Parameter :: eps0 = Epsilon(em)

      If (.Not. Vars_Initialized) Then
         Vars_Initialized = .True.
         c13 = 1.0D0 / 3.0D0
         c23 = 2.0D0 * c13
         em  = -Exp(-1.0D0)
         em9 = -Exp(-9.0D0)
         em2 = 2.0D0 / em
         d12 = -em2
         tb  = 0.5D0 ** nbits
         tb2 = Sqrt(tb)
         x0  = tb**(1.0D0/6.0D0) * 0.5D0
         x1  = (1.0D0 - 17.0D0*tb**(2.0D0/7.0D0))*em
         an3 = 8.0D0 / 3.0D0
         an4 = 135.0D0 / 83.0D0
         an5 = 166.0D0 / 39.0D0
         an6 = 3167.0D0 / 3549.0D0
         s2  = Sqrt(2.0D0)
         s21 = 2.0D0*s2 - 3.0D0
         s22 = 4.0D0 - 3.0D0*s2
         s23 = s2 - 2.0D0
      End If

      LambertW_Ierror = 0
      LambertW_Message = ''
      If (Present(Nerror)) Nerror = 0
      Wx = 0.0D0

      Compute_w0 = .True.
      If (Present(Principal_Branch)) Then
         Compute_w0 = Principal_Branch
      End If

      Value_is_offset = .False.
      If (Present(X_is_offset)) Then
         Value_is_offset = X_is_offset
      End If


      If (Value_is_offset) Then     ! x is an offset; Compute W(x - exp(-1))
         delx = x
         If (delx < 0.0D0) Then
            Write (LambertW_Message, 9160) delx
9160        Format('LambertW: The offset x = ', es8.1, ' must be > 0')
            LambertW_Ierror = 1
            If (Present(Nerror)) Nerror = LambertW_Ierror
            Return
         End If
         xx = x + em
         !         if (d12*delx<tb**2 .and. LambertW_Debug) write (LambertW_LUN, 9180) delx
         ! 9180    format('LambertW: Warning: For this offset (',d16.8,'),',/,&
         !            ' W is negligibly different from -1')
      Else                          ! no offset; Compute W(x)
         If (x < em) Then
            Write (LambertW_Message, 9190) x, em
9190        Format('LambertW: Out of Domain: x = ', es8.1, ' must be > -Exp(-1)=', f6.3)
            LambertW_Ierror = 2
            If (Present(Nerror)) Nerror = LambertW_Ierror
            Return
         Else If (Abs(x - em) <= eps0) Then
            Wx = -1.0D0
            Return
         End If
         xx   = x
         delx = xx - em
         If (delx<tb2 .And. LambertW_Debug) Write (LambertW_LUN, 9200) xx
9200     Format('LambertW: Warning: x (= ',d16.8,') is close to -exp(-1).',/,&
               ' Enter x as an offset to -exp(-1) for greater accuracy')
      End If


      If (Compute_w0) Then    ! Principal branch:  Wp, W0
         If (Abs(xx) <= x0) Then
            Wx = xx/(1.0D0 + xx/(1.0D0 + xx/(2.0D0 + xx/(0.6D0 + 0.34D0*xx))))
            Return
         Else If (xx <= x1) Then
            reta = Sqrt(d12*delx)
            Wx = reta/(1.0D0 + reta/(3.0D0 + reta/(reta/(an4 + reta/(reta*an6&
                  + an5)) + an3))) - 1.0D0
            Return
         Else If (xx <= 2.0D1) Then
            reta = s2*Sqrt(1.0D0 - xx/em)
            an2  = 4.612634277343749D0*Sqrt(Sqrt(reta + 1.09556884765625D0))
            Wx = reta/(1.0D0 + reta/(3.0D0 + (s21*an2 + s22)*reta/(s23*(an2 + &
                  reta)))) - 1.0D0
         Else
            zl = Log(xx)
            Wx = Log(xx/Log(xx/zl**Exp(-1.124491989777808D0/(&
                  0.4225028202459761D0 + zl))))
         End If

      Else If (xx >= 0.0D0) Then ! Other branch:  Wm, W{-1}
         Write (LambertW_Message, 9220) xx, em
9220     Format("LambertW: Out of W{-1}'s domain: x = ", es8.1, '; Domain: -Exp(-1)=', f6.3, ' < x < 0')
         LambertW_Ierror = 3
         If (Present(Nerror)) Nerror = LambertW_Ierror
         Return
      Else If (xx <= x1) Then
         reta = Sqrt(d12*delx)
         Wx = reta/(reta/(3.0D0 + reta/(reta/(an4 + reta/(reta*an6 - an5)) - &
               an3)) - 1.0D0) - 1.0D0
         Return
      Else If (xx <= em9) Then
         zl = Log((-xx))
         t  = (-1.0D0) - zl
         ts = Sqrt(t)
         Wx = zl - (2.0D0*ts)/(s2 + (c13 - t/(2.7D2 + ts*127.0471381349219D0))&
               *ts)
      Else
         zl  = Log((-xx))
         eta = 2.0D0 - em2*xx
         Wx  = Log(xx/Log((-xx/((1.0D0 - 0.5043921323068457D0*(zl + 1.0D0))*(&
               Sqrt(eta) + eta/3.0D0) + 1.0D0))))
      End If

      ! The case of large NBITS
      niter = 1
      If (nbits >= 56) niter = 2

      Do i = 1, niter
         zn    = Log(xx/Wx) - Wx
         temp  = 1.0D0 + Wx
         temp2 = temp + c23*zn
         temp2 = 2.0D0*temp*temp2
         Wx = Wx * (1.0D0 + (zn/temp)*(temp2-zn)/(temp2-2.0D0*zn))
      End Do

   End Subroutine LambertW

End Module m_LambertW
