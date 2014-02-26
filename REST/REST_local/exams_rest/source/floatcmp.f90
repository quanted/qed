!     Last change:  LSR   8 Nov 2000    1:03 pm
! [Keywords]  Floating_Point_Comparisons: Comparisons between real numbers;
! [Keywords]  Numeric Model Intrinsics;
! [Keywords]  [Goose]: Numeric Models, pages 228-229.

Module Floating_Point_Comparisons

  ! Subprograms in this module:
  !     Logical Elemental Function fl_EQ(X,Y)  Truth of (x == y)
  !     Logical Elemental Function fl_NE(X,Y)  Truth of (x /= y)
  !     Logical Elemental Function fl_GT(X,Y)  Truth of (x >  y)
  !     Logical Elemental Function fl_GE(X,Y)  Truth of (x >= y)
  !     Logical Elemental Function fl_LE(X,Y)  Truth of (x <= y)
  !     Logical Elemental Function fl_LT(X,Y)  Truth of (x <  y)
  !
  ! Operators defined in this module:
  !     .Equals.        .NotEqual.
  !     .GreaterThan.   .GreaterThanOrEqual.
  !     .LessThan.      .LessThanOrEqual.

  ! Notes:
  ! 1. User-defined binary operators have the lowest precedence.
  !    Consider the expression a>b .and. c<d.  The simple substitution
  !    a.GreaterThan.b .and. c.LessThan.d would be evaluated as
  !    a.GreaterThan. (b .and. c) .LessThan.d -- a syntax error because
  !    the operators .GreaterThan. (or .LessThan.d) are not defined when
  !    one of the arguments is a logical expression. Use parenthesis to
  !    ensure the correct order of evaluation, e.g.,
  !    (a.GreaterThan.b) .and. (c.LessThan.d).
  !
  ! 2. Consider x1 and x2 points in the number line, nominally x1 < x2.
  !    Let r1 be the spacing at (x1), and r2 be the spacing at (x2).
  !    Due to the limitations of the digital representation of real numbers
  !    by the computer, any number "y" contained in the closed interval
  !    [x1-r1, x1+r1] is indistinguishable from x1. It is because of this
  !    inherent uncertainty that when comparing real numbers the spacing
  !    (or fuzziness) around each number must be taken into account.
  !
  !    There is another item that must be taken into account. A real
  !    number is represented as:
  !
  !                      p
  !       x = s * b^e * Sum (f_k * b^-k)
  !                     k=1
  !    where
  !       (The functions Radix, Digits, Exponent, MinExponent, and MaxExponent
  !        are Fortran 90 intrinsic functions.)

  !       x is the real value
  !       s is the sign (either +1 or -1)
  !       b is the base (radix, integer b > 1); b = Radix(x)
  !       p is the number of mantissa digits (p integer > 1); p = Digits(x)
  !       e is the integer exponent in the range e_min <= e <= e_max, where
  !         e = Exponent(x)
  !         e_min = MinExponent(x)
  !         e_max = MaxExponent(x)
  !       f_k an integer: 0 <= f_k < b, f_1 /= 0 unless x == 0;
  !
  !    Other related F90 intrinsic functions:
  !       Fraction(x) = x * b^-e
  !       Tiny(x) = b^(e_min-1)
  !       Huge(x) = (1 - b^-p) * b^e_max
  !       Range(x) = Int(Min(Log10(Huge(x)), -Log10(Tiny(x))))
  !       Scale(x,i) = x * b^i
  !       RRspacing(x) = Abs(x * b^-e) * b^p
  !       Spacing(x) = b^(e-p)
  !       Epsilon(x) = b^(1-p) == Spacing(1.0)
  !       Set_Exponent(x,i) = x * b^(i-e)
  !       Precision(x) = Floor( (p-1)*Log(b) + z )
  !                                   z = 1  if b is an integral power of 10,
  !                                   z = 0  otherwise
  !       Nearest(x,s) == Nearest number different from x in the direction "s".
  !
  !    if x = 0, then e == 0 and f_k == 0.
  !
  !    Nominally, Nearest(x,s) = x + Sign(s)*Spacing(x), except
  !    where x is a power of the radix, e.g., x = 2^e, where e is
  !    an integer in the range e_min <= e <= e_max.
  !
  !    The functions Exponent(x) and Spacing(x) are step functions with
  !    discontinuities present at x = 2^e, e integer, e_min <= e <= e_max.
  !    Consider x = 8.0.  Assume Radix(x) == 2. Then Exponent(8.0) == 4,
  !    Spacing(8.0) == 2^(4-p), and Nearest(8.0,+1.0) == 8.0 + 2^(4-p), i.e.,
  !    x+Spacing(x). However, Nearest(8.0,-1.0) == 8.0 + 2^(3-p), i.e.,
  !    x-Spacing(x)/2, because Exponent(y) == 3 for 4 <= y < 8. Therefore,
  !    the nearest numbers to x are not +-Spacing(x) for x a power of the
  !    radix (2 in this case).
  !
  !    Consider now the test for equality: x == y. Traditionally,
  !    x == y  if  x-r < y < x+r, where r is a small positive number.
  !    A natural choice is r = Spacing(x). However, if x is a power
  !    of the radix, the segment [x-r, x] contains three numbers:
  !
  !                    --+-----+-------+------------+--
  !                     x-r   x-r/2    x           x+r
  !
  !    The test "Nearest(x,-1) < y < Nearest(x,+1)" takes into account the
  !    asymmetry of the position of the numbers around a power of the radix.
  !    In the text that follows, the expression x1 +- r1 is defined as
  !    Nearest(x1, +-1.0).
  !
  !    Let x1, and x2 be two real (fuzzy) numbers.
  !
  !    EQ Definition: x1 == x2
  !       Fuzzy x1 is equal to fuzzy x2 if the intersection of their respective
  !       intervals [x1-r1, x1+r1] and [x2-r2, x2+r2] is not empty.
  !
  !             <----[-----+-----]-----------[-----+-----]---->
  !                x1-r1   x1  x1+r1       x2-r2   x2  x2+r2
  !
  !       Note that x1 == x2 if and only if x1<=x2 and x2<=x1.
  !             x1 <= x2       .and.       x2 <= x1
  !          x2-r2 <= x1+r1    .and.    x1-r1 <= x2+r2
  !          x2-x1 <= r1+r2    .and.    x1-x2 <= r1+r2     (used later)
  !          r1+r2 >= x2-x1    .and.    x2-x1 >= -(r1+r2)  (used later)
  !       i.e.,
  !          Nearest(x2,-1) <= Nearest(x1,+1)  .and.
  !          Nearest(x1,-1) <= Nearest(x2,+1)
  !
  !    NE Definition: x1/=x2  if  .Not. (x1 == x2), i.e.,
  !          .not. (Nearest(x2,-1) <= Nearest(x1,+1)  .and.
  !                 Nearest(x1,-1) <= Nearest(x2,+1))
  !       i.e.,
  !          (Nearest(x2,-1) > Nearest(x1,+1)  .or.
  !           Nearest(x1,-1) > Nearest(x2,+1))
  !
  !    GT Definition: x2>x1  if  x2-r2>x1+r1 (i.e., intervals do not overlap)
  !       i.e.,
  !          (Nearest(x2,-1) > Nearest(x1,+1))
  !
  !    LE Definition: x2<=x1  if .Not. (x2 > x1)
  !       i.e.,
  !          (Nearest(x2,-1) <= Nearest(x1,+1))
  !
  !    GE Definition: x2>=x1  if
  !                 x2 > x1     .Or.   x2 == x1
  !          if  x2-r2 > x1+r1  .Or.  (x2-r2 <= x1+r1 .and. x1-r1 <= x2+r2)
  !          if  r1+r2 < x2-x1  .Or.  -(r1+r2) <= x2-x1 <= r1+r2
  !          if  -(r1+r2) <= x2-x1    (i.e., Union of solution sets)
  !          if  r1+r2 >= x1-x2
  !          if  x2+r2 >= x1-r1
  !       i.e.,
  !          (Nearest(x2,+1) >= Nearest(x1,-1))
  !
  !    LT Definition: x2 < x1  if  .Not.  x2 >= x1, i.e.,
  !          (Nearest(x2,+1) < Nearest(x1,-1))
  !
  !
  ! 3. When an integer value is compared to either a single or double precision
  !    value, the integer will be promoted to either single or double precision,
  !    as appropriate.

  ! History:
  ! = [lsr] Tue Dec  8 12:54:11 1998
  !   . initially I tried to port the f77 code. This is a Complete rewrite.
  !     The Fortran 90 code bears no resemblance to the old code.
  !   . test suite: ~/f90/tests/fuzzy_comparisons/main3.f90; passed.
  !   . finished: Thu Dec 17 15:12:32 1998
  !   . finished: Fri Dec 18 11:21:52 1998 (again)
  ! = [lsr] Tue Oct 17 15:10:17 1995
  !   . ported to osf/1
  ! = [lsr] 09:28 fri 26-aug-1994.
  !   - processed by SPAG 4.50I  at 10:32 on 26 Aug 1994
  !   - test75.f used to validate answers: passed;

  Implicit None
  Private
  Public :: fl_EQ, fl_NE, fl_GT, fl_GE, fl_LE, fl_LT
  Public :: Operator(.Equals.),       Operator(.NotEqual.)
  Public :: Operator(.GreaterThan.),  Operator(.GreaterThanOrEqual.)
  Public :: Operator(.LessThan.),     Operator(.LessThanOrEqual.)

  Integer, Parameter :: ksp = Kind(1.0e0)  ! single precision
  Integer, Parameter :: kdp = Kind(1.0d0)  ! double precision

  ! Generic interfaces for the subprograms.
  ! "s" denotes a real(ksp) argument, i.e., a single precision number
  ! "d" denotes a real(kdp) argument, i.e., a double precision number
  ! "i" denotes an integer argument
  !
  ! Example.  The first argument of the function siEq is a real(Kind=ksp)
  ! number; its second argument is an integer.


  Interface fl_EQ ! (x == y)
     Module Procedure ssEq
     Module Procedure siEq
     Module Procedure sdEq
     Module Procedure ddEq
     Module Procedure dsEq
     Module Procedure diEq
     Module Procedure iiEq
     Module Procedure isEq
     Module Procedure idEq
  End Interface

  Interface fl_NE ! (x /= y)
     Module Procedure ssNe
     Module Procedure siNe
     Module Procedure sdNe
     Module Procedure ddNe
     Module Procedure dsNe
     Module Procedure diNe
     Module Procedure iiNe
     Module Procedure isNe
     Module Procedure idNe
  End Interface

  Interface fl_GT ! (x > y)
     Module Procedure ssGt
     Module Procedure siGt
     Module Procedure sdGt
     Module Procedure ddGt
     Module Procedure dsGt
     Module Procedure diGt
     Module Procedure iiGt
     Module Procedure isGt
     Module Procedure idGt
  End Interface

  Interface fl_GE ! (x >= y)
     Module Procedure ssGe
     Module Procedure siGe
     Module Procedure sdGe
     Module Procedure ddGe
     Module Procedure dsGe
     Module Procedure diGe
     Module Procedure iiGe
     Module Procedure isGe
     Module Procedure idGe
  End Interface

  Interface fl_LE ! (x <= y)
     Module Procedure ssLe
     Module Procedure siLe
     Module Procedure sdLe
     Module Procedure ddLe
     Module Procedure dsLe
     Module Procedure diLe
     Module Procedure iiLe
     Module Procedure isLe
     Module Procedure idLe
  End Interface

  Interface fl_LT ! (x < y)
     Module Procedure ssLt
     Module Procedure siLt
     Module Procedure sdLt
     Module Procedure ddLt
     Module Procedure dsLt
     Module Procedure diLt
     Module Procedure iiLt
     Module Procedure isLt
     Module Procedure idLt
  End Interface

  ! --- Operators ---

  Interface Operator (.Equals.) ! (x == y)
     Module Procedure ssEq
     Module Procedure siEq
     Module Procedure sdEq
     Module Procedure ddEq
     Module Procedure dsEq
     Module Procedure diEq
     Module Procedure iiEq
     Module Procedure isEq
     Module Procedure idEq
  End Interface

  Interface Operator (.NotEqual.) ! (x /= y)
     Module Procedure ssNe
     Module Procedure siNe
     Module Procedure sdNe
     Module Procedure ddNe
     Module Procedure dsNe
     Module Procedure diNe
     Module Procedure iiNe
     Module Procedure isNe
     Module Procedure idNe
  End Interface

  Interface Operator (.GreaterThan.) ! (x > y)
     Module Procedure ssGt
     Module Procedure siGt
     Module Procedure sdGt
     Module Procedure ddGt
     Module Procedure dsGt
     Module Procedure diGt
     Module Procedure iiGt
     Module Procedure isGt
     Module Procedure idGt
  End Interface

  Interface Operator (.GreaterThanOrEqual.) ! (x >= y)
     Module Procedure ssGe
     Module Procedure siGe
     Module Procedure sdGe
     Module Procedure ddGe
     Module Procedure dsGe
     Module Procedure diGe
     Module Procedure iiGe
     Module Procedure isGe
     Module Procedure idGe
  End Interface

  Interface Operator (.LessThanOrEqual.) ! (x <= y)
     Module Procedure ssLe
     Module Procedure siLe
     Module Procedure sdLe
     Module Procedure ddLe
     Module Procedure dsLe
     Module Procedure diLe
     Module Procedure iiLe
     Module Procedure isLe
     Module Procedure idLe
  End Interface

  Interface Operator (.LessThan.) ! (x < y)
     Module Procedure ssLt
     Module Procedure siLt
     Module Procedure sdLt
     Module Procedure ddLt
     Module Procedure dsLt
     Module Procedure diLt
     Module Procedure iiLt
     Module Procedure isLt
     Module Procedure idLt
  End Interface


Contains

  ! ----------------------------------- real(Kind=ksp) == Single Precision
  Elemental Function ssEq(sx, sy) ! ssEq = (sx == sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssEq
    Logical                    :: z1, z2

    z1 = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) <= Nearest(sx,+1.0))
    ssEq = z1 .And. z2
  End Function ssEq


  Elemental Function ssNe(sx, sy) ! ssNe = (sx /= sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssNe
    Logical                    :: z1, z2

    z1 = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) > Nearest(sx,+1.0))
    ssNe = z1 .Or. z2
  End Function ssNe


  Elemental Function ssGt(sx, sy) ! ssGt = (sx > sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssGt

    ssGt = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
  End Function ssGt


  Elemental Function ssLe(sx, sy) ! ssLe = (sx <= sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssLe

    ssLe = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
  End Function ssLe


  Elemental Function ssGe(sx, sy) ! ssGe = (sx >= sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssGe

    ssGe = (Nearest(sx,+1.0) >= Nearest(sy,-1.0))
  End Function ssGe


  Elemental Function ssLt(sx, sy) ! ssLt = (sx < sy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: ssLt

    ssLt = (Nearest(sx,+1.0) < Nearest(sy,-1.0))
  End Function ssLt


  ! ----------------------------------- real(Kind=kdp) == Double Precision
  Elemental Function ddEq(dx, dy) ! ddEq = (dx == dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddEq
    Logical                    :: z1, z2

    z1 = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) <= Nearest(dx,+1.0))
    ddEq = z1 .And. z2
  End Function ddEq


  Elemental Function ddNe(dx, dy) ! ddNe = (dx /= dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddNe
    Logical                    :: z1, z2

    z1 = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) > Nearest(dx,+1.0))
    ddNe = z1 .Or. z2
  End Function ddNe


  Elemental Function ddGt(dx, dy) ! ddGt = (dx > dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddGt

    ddGt = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
  End Function ddGt


  Elemental Function ddLe(dx, dy) ! ddLe = (dx <= dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddLe

    ddLe = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
  End Function ddLe


  Elemental Function ddGe(dx, dy) ! ddGe = (dx >= dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddGe

    ddGe = (Nearest(dx,+1.0) >= Nearest(dy,-1.0))
  End Function ddGe


  Elemental Function ddLt(dx, dy) ! ddLt = (dx < dy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: ddLt

    ddLt = (Nearest(dx,+1.0) < Nearest(dy,-1.0))
  End Function ddLt


  ! ----------------------------------- Mixed Interface: (Single, Double)
  Elemental Function sdEq(sx, dy) ! sdEq = (sx == dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdEq
    Logical                    :: z1, z2

    z1 = (Nearest(sx,-1.0) <= Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) <= Nearest(sx,+1.0))
    sdEq = z1 .And. z2
  End Function sdEq


  Elemental Function sdNe(sx, dy) ! sdNe = (sx /= dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdNe
    Logical                    :: z1, z2

    z1 = (Nearest(sx,-1.0) > Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) > Nearest(sx,+1.0))
    sdNe = z1 .Or. z2
  End Function sdNe


  Elemental Function sdGt(sx, dy) ! sdGt = (sx > dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdGt

    sdGt = (Nearest(sx,-1.0) > Nearest(dy,+1.0))
  End Function sdGt


  Elemental Function sdLe(sx, dy) ! sdLe = (sx <= dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdLe

    sdLe = (Nearest(sx,-1.0) <= Nearest(dy,+1.0))
  End Function sdLe


  Elemental Function sdGe(sx, dy) ! sdGe = (sx >= dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdGe

    sdGe = (Nearest(sx,+1.0) >= Nearest(dy,-1.0))
  End Function sdGe


  Elemental Function sdLt(sx, dy) ! sdLt = (sx < dy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: sdLt

    sdLt = (Nearest(sx,+1.0) < Nearest(dy,-1.0))
  End Function sdLt


  ! ----------------------------------- Mixed Interface: (Double, Single)
  Elemental Function dsEq(dx, sy) ! dsEq = (dx == sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsEq
    Logical                    :: z1, z2

    z1 = (Nearest(dx,-1.0) <= Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) <= Nearest(dx,+1.0))
    dsEq = z1 .And. z2
  End Function dsEq


  Elemental Function dsNe(dx, sy) ! dsNe = (dx /= sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsNe
    Logical                    :: z1, z2

    z1 = (Nearest(dx,-1.0) > Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) > Nearest(dx,+1.0))
    dsNe = z1 .Or. z2
  End Function dsNe


  Elemental Function dsGt(dx, sy) ! dsGt = (dx > sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsGt

    dsGt = (Nearest(dx,-1.0) > Nearest(sy,+1.0))
  End Function dsGt


  Elemental Function dsLe(dx, sy) ! dsLe = (dx <= sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsLe

    dsLe = (Nearest(dx,-1.0) <= Nearest(sy,+1.0))
  End Function dsLe


  Elemental Function dsGe(dx, sy) ! dsGe = (dx >= sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsGe

    dsGe = (Nearest(dx,+1.0) >= Nearest(sy,-1.0))
  End Function dsGe


  Elemental Function dsLt(dx, sy) ! dsLt = (dx < sy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: dsLt

    dsLt = (Nearest(dx,+1.0) < Nearest(sy,-1.0))
  End Function dsLt


  ! ----------------------------------- Integer; added for completeness
  Elemental Function iiEq(x, y) ! iiEq = (x == y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiEq

    iiEq = (x == y)
  End Function iiEq


  Elemental Function iiNe(x, y) ! iiNe = (x /= y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiNe

    iiNe = (x /= y)
  End Function iiNe


  Elemental Function iiGt(x, y) ! iiGt = (x > y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiGt

    iiGt = (x > y)
  End Function iiGt


  Elemental Function iiLe(x, y) ! iiLe = (x <= y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiLe

    iiLe = (x <= y)
  End Function iiLe


  Elemental Function iiGe(x, y) ! iiGe = (x >= y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiGe

    iiGe = (x >= y)
  End Function iiGe


  Elemental Function iiLt(x, y) ! iiLt = (x < y)
    Implicit None
    Integer, Intent(In) :: x
    Integer, Intent(In) :: y
    Logical             :: iiLt

    iiLt = (x < y)
  End Function iiLt


  ! ----------------------------------- Mixed Interface: (Single, Integer)
  Elemental Function siEq(sx, iy) ! siEq = (sx == iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siEq
    Real(Kind=ksp)             :: sy
    Logical                    :: z1, z2

    sy = Real(iy, Kind=ksp)
    z1 = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) <= Nearest(sx,+1.0))
    siEq = z1 .And. z2
  End Function siEq


  Elemental Function siNe(sx, iy) ! siNe = (sx /= iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siNe
    Real(Kind=ksp)             :: sy
    Logical                    :: z1, z2

    sy = Real(iy, Kind=ksp)
    z1 = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) > Nearest(sx,+1.0))
    siNe = z1 .Or. z2
  End Function siNe


  Elemental Function siGt(sx, iy) ! siGt = (sx > iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siGt
    Real(Kind=ksp)             :: sy

    sy = Real(iy, Kind=ksp)
    siGt = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
  End Function siGt


  Elemental Function siLe(sx, iy) ! siLe = (sx <= iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siLe
    Real(Kind=ksp)             :: sy

    sy = Real(iy, Kind=ksp)
    siLe = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
  End Function siLe


  Elemental Function siGe(sx, iy) ! siGe = (sx >= iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siGe
    Real(Kind=ksp)             :: sy

    sy = Real(iy, Kind=ksp)
    siGe = (Nearest(sx,+1.0) >= Nearest(sy,-1.0))
  End Function siGe


  Elemental Function siLt(sx, iy) ! siLt = (sx < iy)
    Implicit None
    Real(Kind=ksp), Intent(In) :: sx
    Integer,        Intent(In) :: iy
    Logical                    :: siLt
    Real(Kind=ksp)             :: sy

    sy = Real(iy, Kind=ksp)
    siLt = (Nearest(sx,+1.0) < Nearest(sy,-1.0))
  End Function siLt


  ! ----------------------------------- Mixed Interface: (Double, Integer)
  Elemental Function diEq(dx, iy) ! diEq = (dx == iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diEq
    Real(Kind=kdp)             :: dy
    Logical                    :: z1, z2

    dy = Real(iy, Kind=kdp)
    z1 = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) <= Nearest(dx,+1.0))
    diEq = z1 .And. z2
  End Function diEq


  Elemental Function diNe(dx, iy) ! diNe = (dx /= iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diNe
    Real(Kind=kdp)             :: dy
    Logical                    :: z1, z2

    dy = Real(iy, Kind=kdp)
    z1 = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) > Nearest(dx,+1.0))
    diNe = z1 .Or. z2
  End Function diNe


  Elemental Function diGt(dx, iy) ! diGt = (dx > iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diGt
    Real(Kind=kdp)             :: dy

    dy = Real(iy, Kind=kdp)
    diGt = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
  End Function diGt


  Elemental Function diLe(dx, iy) ! diLe = (dx <= iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diLe
    Real(Kind=kdp)             :: dy

    dy = Real(iy, Kind=kdp)
    diLe = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
  End Function diLe


  Elemental Function diGe(dx, iy) ! diGe = (dx >= iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diGe
    Real(Kind=kdp)             :: dy

    dy = Real(iy, Kind=kdp)
    diGe = (Nearest(dx,+1.0) >= Nearest(dy,-1.0))
  End Function diGe


  Elemental Function diLt(dx, iy) ! diLt = (dx < iy)
    Implicit None
    Real(Kind=kdp), Intent(In) :: dx
    Integer,        Intent(In) :: iy
    Logical                    :: diLt
    Real(Kind=kdp)             :: dy

    dy = Real(iy, Kind=kdp)
    diLt = (Nearest(dx,+1.0) < Nearest(dy,-1.0))
  End Function diLt


  ! ----------------------------------- Mixed Interface: (Integer, Single)
  Elemental Function isEq(ix, sy) ! isEq = (ix == sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isEq
    Real(Kind=ksp)             :: sx
    Logical                    :: z1, z2

    sx = Real(ix, Kind=ksp)
    z1 = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) <= Nearest(sx,+1.0))
    isEq = z1 .And. z2
  End Function isEq


  Elemental Function isNe(ix, sy) ! isNe = (ix /= sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isNe
    Real(Kind=ksp)             :: sx
    Logical                    :: z1, z2

    sx = Real(ix, Kind=ksp)
    z1 = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
    z2 = (Nearest(sy,-1.0) > Nearest(sx,+1.0))
    isNe = z1 .Or. z2
  End Function isNe


  Elemental Function isGt(ix, sy) ! isGt = (ix > sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isGt
    Real(Kind=ksp)             :: sx

    sx = Real(ix, Kind=ksp)
    isGt = (Nearest(sx,-1.0) > Nearest(sy,+1.0))
  End Function isGt


  Elemental Function isLe(ix, sy) ! isLe = (ix <= sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isLe
    Real(Kind=ksp)             :: sx

    sx = Real(ix, Kind=ksp)
    isLe = (Nearest(sx,-1.0) <= Nearest(sy,+1.0))
  End Function isLe


  Elemental Function isGe(ix, sy) ! isGe = (ix >= sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isGe
    Real(Kind=ksp)             :: sx

    sx = Real(ix, Kind=ksp)
    isGe = (Nearest(sx,+1.0) >= Nearest(sy,-1.0))
  End Function isGe


  Elemental Function isLt(ix, sy) ! isLt = (ix < sy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=ksp), Intent(In) :: sy
    Logical                    :: isLt
    Real(Kind=ksp)             :: sx

    sx = Real(ix, Kind=ksp)
    isLt = (Nearest(sx,+1.0) < Nearest(sy,-1.0))
  End Function isLt


  ! ----------------------------------- Mixed Interface: (Integer, Double)
  Elemental Function idEq(ix, dy) ! idEq = (ix == dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idEq
    Real(Kind=kdp)             :: dx
    Logical                    :: z1, z2

    dx = Real(ix, Kind=kdp)
    z1 = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) <= Nearest(dx,+1.0))
    idEq = z1 .And. z2
  End Function idEq


  Elemental Function idNe(ix, dy) ! idNe = (ix /= dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idNe
    Real(Kind=kdp)             :: dx
    Logical                    :: z1, z2

    dx = Real(ix, Kind=kdp)
    z1 = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
    z2 = (Nearest(dy,-1.0) > Nearest(dx,+1.0))
    idNe = z1 .Or. z2
  End Function idNe


  Elemental Function idGt(ix, dy) ! idGt = (ix > dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idGt
    Real(Kind=kdp)             :: dx

    dx = Real(ix, Kind=kdp)
    idGt = (Nearest(dx,-1.0) > Nearest(dy,+1.0))
  End Function idGt


  Elemental Function idLe(ix, dy) ! idLe = (ix <= dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idLe
    Real(Kind=kdp)             :: dx

    dx = Real(ix, Kind=kdp)
    idLe = (Nearest(dx,-1.0) <= Nearest(dy,+1.0))
  End Function idLe


  Elemental Function idGe(ix, dy) ! idGe = (ix >= dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idGe
    Real(Kind=kdp)             :: dx

    dx = Real(ix, Kind=kdp)
    idGe = (Nearest(dx,+1.0) >= Nearest(dy,-1.0))
  End Function idGe


  Elemental Function idLt(ix, dy) ! idLt = (ix < dy)
    Implicit None
    Integer,        Intent(In) :: ix
    Real(Kind=kdp), Intent(In) :: dy
    Logical                    :: idLt
    Real(Kind=kdp)             :: dx

    dx = Real(ix, Kind=kdp)
    idLt = (Nearest(dx,+1.0) < Nearest(dy,-1.0))
  End Function idLt


End Module Floating_Point_Comparisons
