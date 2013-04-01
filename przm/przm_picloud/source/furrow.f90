Module m_furrow

   Implicit None
   Private
   Public :: furrow


Contains

   Subroutine furrow

      ! + + + PURPOSE + + +
      ! computes flow and infiltration down a furrow using
      ! a Kinematic Wave with Green-Ampt infiltration.
      ! flow equation is approximated by a backwards-time and -space
      ! finite difference, solved by iteration.
      ! Modification date: 2/14/92 JAM

      Implicit None

      ! common blocks + + +
      Include 'CIRGT.INC'

      Real, Parameter :: two_thirds = 2.0/3.0
      Integer :: i, it, iter, ix, n, ntime, ntrem
      Real :: a, a0, a1, a2, alph, aold, aus, b, b0, b2, bold, bus
      Real :: d2a, d2b, d2fq, da, db, del, del2, delq, depth, dfq
      Real :: dt, dtrem, dvol, dvolus, em, eps0, ferr, fq, fq2
      Real :: fsold, fvol, omega, p1, p2, q, q1, q2, qend, qold
      Real :: r1, r2, ratio, s, tend, term, time, tmp0, vchan
      Real :: vinf, volin, x, xadv, y, y0, y1, y2, yavg, yus

      Real :: lnchk
      Character :: mesage*80

      ! Local variable definitions; units are SI (m,s):
      !       FERR...error tolerance for iteration, as fraction of OMEGA
      !       OMEGA...known terms in finite difference equation
      !       FQ....unknowns in finite difference equation
      !       DT....time step for flow computations (s)
      !       DTREM...time step after furrow is flowing full
      !
      !       First letter naming conventions:
      !                   Q   = flow rates (m3/s)
      !                   A   = cross-sectional areas (m2)
      !                   B   = flow top widths (m)
      !                   Y   = flow depths (m)
      !                   D** = first derivative of **
      !                   D2** = second derivative of **
      !                   VOL = volumes (m3)

      !>>namelist /xx0/ bt, zrs, sf, en
      !>>namelist /xx1/ y1, a1, p1, r1, q1
      !>>namelist /xx2/ y2, a2, p2, r2, q2

      mesage = 'FURROW'
      Call subin (mesage)

      !     Compute cross section Area-Flow relationship
      !         A = ALPH * Q**EM
      !
      ! See "Furrow Irrigation", chapter 6 of the PRZM manual.
      ! Q0:    flow rate of water entering heads of individual furrows (m3 s-1).
      ! bt:    bottom width of the furrows (m).
      ! zrs:   slope of the furrow channel walls (horizontal/vertical).
      ! SF:    slope of the furrow channel bottom (vertical/horizontal).
      ! EN:    Manning's roughness coefficient for the furrow.
      ! X2:    length of the furrow (m).
      ! XFRAC: location in furrow where PRZM infiltration calculations are performed,
      !        as a fraction of the furrow length (X2).  If XFRAC = -1, average depths are used in PRZM.
      !
      !    a   b        c   d
      !     \  |        |  /
      !      \ |        | /
      !       \|        |/
      !        +--------+
      !        f        e
      !        <-- bt -->
      !
      ! Assume an isoceles trapezoidal furrow afed. The cross-sectional area (A) abcdef is equal
      ! to the area of bcef + the area of the triangles abf and cdf. The triangles are congruent.
      !
      ! Given:
      !     Length of ce: depth of furrow (y1 or y2 below)
      !     Length of fe: bottom width of furrow (bt, input)
      !     zrs: slope of the furrow channel walls (horizontal/vertical) (input)
      !                 c   d
      !                 |  /|
      !                 | / |
      !                 |/  |
      !                 +---+
      !                 e   g
      !
      ! The height of triangle cde is ce, i.e., the depth of the furrow (y).
      ! Segment cd = Segment eg = horizontal length associated with the slope
      !
      !       Horizontal   eg
      ! zrs = ---------- = --  ==> eg = ce * zrs = y * zrs
      !        Vertical    ce
      !
      ! Also, ed^2 = eg^2 + dg^2 = (y*zrs)^2 + y^2
      !         ed = y * Sqrt(1+zrs^2)
      ! (This result will be needed later.)
      !
      ! The area of the triangles = 2 * (1/2) (base eg) (height ce) = y * zrs
      ! The area of the square is bt * y
      !
      ! Cross-sectional area "A" at depth "y" = bt * y  +  zrs * y^2
      !
      ! Hydraulic radius of flow "R" = cross-sectional area of flow (A) / wetted perimeter (P)
      ! Wetted perimeter "P" = af + fe + ed
      !                      = bt  +  2 * y * Sqrt(1+zrs^2)
      ! (because af = ed. ed resolved above.)

!>>Write (6, nml=xx0)
!>>Call aaaa ()

      y1 = 0.01               ! depth of furrow,  1 cm in meters
      y2 = 0.10               ! depth of furrow, 10 cm in meters
      a1 = (bt + zrs*y1)*y1   ! cross-sectional area at y1
      a2 = (bt + zrs*y2)*y2   ! cross-sectional area at y2
      tmp0 = 2*Sqrt(1.0 + zrs**2)
      p1 = bt + tmp0*y1       ! wetted perimeter at y1
      p2 = bt + tmp0*y2       ! wetted perimeter at y2
      r1 = a1/p1              ! Hydraulic radius at y1
      r2 = a2/p2              ! Hydraulic radius at y2

      ! Approximate Manning's equation: Q = A R^(2/3) S^(1/2) / n,
      ! with: A = Alpha * Q^m
      ! Determine "m" and Alpha given points(a1,q1) and (a2,q2)
      tmp0 = Sqrt(sf)/en
      q1 = a1*tmp0*r1**two_thirds   ! flow rate at y1
      q2 = a2*tmp0*r2**two_thirds   ! flow rate at y2
!>>Write (6, nml=xx1)
!>>Write (6, nml=xx2)
      em = lnchk(a2/a1) / lnchk(q2/q1)
      alph = a1/q1**em
!>>Write (6, *) 'lnchk(q2/q1) == lnchk(0/0) == ', lnchk(q2/q1)
!>>stop 'zzzz'

      ! compute conditions at head of furrow.
      ! Given initial flow rate (Q0) determine the associated furrow depth (y0).
      ! Compute the initial cross-sectional area of flow (A0) with the
      ! approximation to Manning's equation. From the comments above, the
      ! cross-sectional area:
      !        A0 = bt * y0  +  zrs * y0^2
      ! Solving for y0:
      !        y0 = (-bt + B0) / (2 * zrs),
      ! where
      !        B0 = Sqrt(bt^2 + 4*zrs*A0)
      ! An equivalent, numerically more stable expression for y0 is:
      !        y0 = (2 * A0) / (bt + B0)

      qs(1) = q0              ! initial flow rate
      qend = q0
      a0 = alph*q0**em        ! initial cross-sectional area
      b0 = Sqrt(bt**2 + 4.0*a0*zrs)
      y0 = 2.0*zrs/(b0 + bt)  ! initial depth
      yavg = a0/b0

      ! finite - difference time loop initialization
      ferr = 0.01
      dx = 10.0
      dt = 60.0
      tend = 86400.0             ! 1 day in seconds
      time = 0.0
      x = 0.0
      volin = 0.0
      nspace = Nint(xl/dx + 1)
      ntime = Nint(tend/dt)      ! time steps: 1440 minutes in 1 day
      qs(1:nspace) = 0.0
      fs(1:nspace) = 0.0

      Do n = 1, ntime
         x = 0.0
         fvol = 0.0
         time = time + dt        ! not used

         ! compute infiltration at head of furrow and set upstream boundary conditions
         Call infil (ks, yavg, hf, dw, dt, fs(1))  ! fs(1) has always the same value
         volin = volin + q0*dt
         dvolus = 0.0
         q = q0
         depth = y0
         a = a0
         b = b0

         ! finite-difference space loop -- solve for flow rate at
         ! each downstream station by iteration
         Do i = 2, nspace
            x = x + dx

            ! Kinematic Wave Equation:
            !
            !     Partial Q     Partial A
            !     ---------  +  --------- = -q
            !     Partial x     Partial t
            !
            ! A = alpha * Q^m
            ! q = b * Fs
            ! b = Sqrt(bt^2 + 4*zrs*A)
            !     flow width at location i
            !     effective width of flow (width of portion of cross section which is transporting sediment)
            !
            ! Fs = Cumulative infiltration
            !
            ! Calculate current infiltration; compute finite difference
            ! terms for known upstream and previous conditions:

            aold = alph*qs(i)**em
            bold = Sqrt(bt**2 + 4.0*aold*zrs)
            fsold = fs(i)
            y = aold/bold
            Call infil (ks, y, hf, dw, dt, fs(i))
            omega = dt*q/dx + aold + bold*fsold
            eps0 = Abs(ferr*omega)
            aus = a
            bus = b
            yus = depth

            ! Compute finite difference terms for first guess of new Q
            ! (first guess = upstream flow rate):

            fq = dt*q/dx + a + b*fs(i)

            ! Iteration using 2nd order Taylor series expansion to
            ! compute next guess of Q; maximum of 10 iterations allowed:

            Do iter = 1, 10

               ! Compute derivatives with respect to Q:

               ! A = alpha * Q^m
               da = alph * em * q**(em - 1)
               d2a = alph * em * (em - 1) * q**(em - 2)

               ! b = Sqrt(bt^2 + 4*zrs*A)
               db = 2.0 * zrs * da / b
               d2b = 2.0*zrs*d2a/b - 4.0*zrs**2*da**2/b**3

               ! f = dt/dx*Q + A + b*Fs
               dfq = dt/dx + da + db*fs(i)
               d2fq = d2a + d2b*fs(i)

               ! Compute new guesses of Q (two roots):

               ratio = dfq/d2fq
               term = ratio**2 - 2.0*(fq - omega)/d2fq
               term = Max(0.0, term)
               term = Sqrt(term)
               qold = q

               q = qold - ratio + term
               If (q <= 0.0) q = q0/100.0
               a = alph*q**em
               b = Sqrt(bt**2 + 4.0*a*zrs)
               fq = dt*q/dx + a + b*fs(i)
               del = Abs(fq - omega)

               q2 = qold - ratio - term
               If (q2 <= 0.0) q2 = q0/100.0
               a2 = alph*q2**em
               b2 = Sqrt(bt**2 + 4.0*a2*zrs)
               fq2 = dt*q2/dx + a2 + b2*fs(i)
               del2 = Abs(fq2 - omega)

               ! Choose Q with smallest error DEL; check for convergence:

               If (del2 < del) Then
                  q = q2
                  a = a2
                  b = b2
                  fq = fq2
                  del = del2
               End If

               !
               If (del <= eps0/iter) go to 20
            End Do

            ! If no convergence after 10 iterations, truncate wave front
            ! (exit finite-difference spatial loop):

            Exit

            ! Convergence; end iteration loop and compute volumes
            ! in furrow channel and ground:

20          Continue
            s = (depth - yus)/dx
            vchan = aus*dx + s*bus*dx**2/2.0 + zrs*s**2*dx**3/3.0
            vinf = (bus*fs(i-1) + b*fs(i)) * dx / 2.0
            fvol = fvol + vchan + vinf

            ! Store new value of flow rate Q and check volume balance;
            ! If volume in channel + volume infiltrated is greater than
            ! total inflow volume, truncate wave front (exit F-D space loop):

            dvol = Abs(fvol - volin)
            If (fvol>=volin .And. dvol>=dvolus) Exit
            qs(i) = q
            depth = 2 * a / (b + bt)      ! (b - bt)/(2.*zrs)
            dvolus = dvol
            xadv = x
         End Do

         ! Check if change in flow at end of furrow is significant
         ! (greater than 5 percent). If not, discontinue finite
         ! difference flow computations.

         If (Abs(xadv - xl) >= 1.0E-5) Cycle
         If (fs(nspace) >= smdef/100.0) go to 100
         delq = (qend - q)/qend
         If (delq <= 0.05) Exit
         qend = q
      End Do

      ! End of Finite Difference Flow computation loops;
      ! Compute infiltration for remainder of day assuming
      ! constant flow in the channel:

      ntrem = (ntime - n)/60 + 1
      dtrem = dt * 10.0
      Do it = 1, ntrem
         Do ix = 1, nspace
            a = alph*qs(ix)**em
            b = Sqrt(bt**2 + 4.0*a*zrs)
            y = a/b
            Call infil (ks, y, hf, dw, dtrem, fs(ix))
         End Do
         If (fs(nspace) < smdef/100.0) Cycle
         Exit
      End Do


100   Continue
      Call subout

!>>Contains
!>>Subroutine aaaa ()
!>>
!>>   Implicit None
!>>!
!>>!     Compute cross section Area-Flow relationship
!>>!         A = ALPH * Q**EM
!>>
!>>      Real, External :: SQRCHK
!>>
!>>      Write (6, *) ' **** PRZM 3.12 beta code ******* '
!>>      Write (6, nml=xx0)
!>>      Y1 = .01
!>>      Y2 = .10
!>>      A1 = BT*Y1 + ZRS*Y1**2.
!>>      A2 = BT*Y2 + ZRS*Y2**2.
!>>      P1 = BT + REAL(SQRCHK(DBLE(1.+ZRS**2.)))*2.*Y1
!>>      P2 = BT + REAL(SQRCHK(DBLE(1.+ZRS**2.)))*2.*Y2
!>>      R1 = A1/P1
!>>      R2 = A2/P2
!>>      Q1 = A1*(R1**.66667)*(SF**.5)/EN
!>>      Q2 = A2*(R2**.66667)*(SF**.5)/EN
!>>      Write (6, nml=xx1)
!>>      Write (6, nml=xx2)
!>>
!>>
!>>      !EM = (LNCHK(A2)-LNCHK(A1))/(LNCHK(Q2)-LNCHK(Q1))
!>>      !Write (6, *) 'em = ', em
!>>      !Call Sleep(10)
!>>
!>>End Subroutine  aaaa

   End Subroutine furrow


   Subroutine infil(ks, d, hf, dw, dt, fc)

      ! Computes Green-Ampt infiltration assuming
      ! a constant depth over time step DT.
      !
      ! The integrated Green-Ampt equation:
      !
      !     Ks dt = Fc  -  h * Ln[1 + Fc/h]
      !
      ! has the analytic solution
      !
      !     Fc = -h * (1 + LambertW(z))
      !
      ! where
      !                   Ks dt
      !     z = -Exp(-1 - -----)
      !                     h
      !
      ! LambertW(z) is the Lambert W function (see PRZM manual).
      ! For realistic simulation values, -Exp(-1) < z < 0 .
      ! In this range the Lambert W function has two branches.
      ! The range of the principal branch (W_0(x)) is positive,
      ! which would generate an unrealistic Fc.
      ! The range of the other branch (denoted W_{-1}(x)) is
      ! oo < W_{-1}(x) <= -1. This branch generates a realistic
      ! answer and is used in this subroutine.
      !
      ! Modification History:
      ! = [lsr] Wed Mar 03 13:13:28 EST 2004
      !   * the integrated Green-Ampt equation is
      !     is solved analytically.
      !
      ! = 2/14/92 JAM
      !   * the integrated Green-Ampt equation is
      !     solved by iteration for the new value
      !     of cumulative infiltration FC.

      Use m_LambertW
      Use General_Vars, Only:  Double
      Implicit None

      ! KS = saturated hydraulic conductivity (L/T)
      ! D  = depth of surface water (L)
      ! HF = Green-ampt suction parameter (L)
      ! DW = porosity (unitless)
      ! DT = time interval
      ! FC = cumulative infiltration (L)

      Real,  Intent(in) :: ks
      Real,  Intent(in) :: d
      Real,  Intent(in) :: hf
      Real,  Intent(in) :: dw
      Real,  Intent(in) :: dt
      Real, Intent(out) :: fc

      Character(Len=80) :: mesage
      Logical :: fatal
      Integer :: ierror
      Real :: h
      Real(Double) :: z, Wz
      Real(Double), Parameter :: One = 1.0_Double
      Real,         Parameter :: Tol = Epsilon(h)

      mesage = 'INFIL'
      Call subin (mesage)

      ! See equations above and the PRZM manual.

      h = (d + hf) * dw

      If (h <= Tol) Then
         mesage = 'INFIL: (d+hf)*dw <= 0'
         ierror = 6010
         fatal  = .True.
         Call Errchk (ierror, mesage, fatal)
      End If

      z = -Exp(-One - ks*dt/h)
      Call LambertW (z, Wz, Principal_Branch=.False., Nerror=ierror)
      If (ierror /= 0) Then
         ierror = 6020
         fatal  = .True.
         Call Errchk (ierror, Trim(LambertW_Message), fatal)
      End If

      Fc = -h * (One + Wz)

      Call subout

   End Subroutine infil

End Module m_furrow

