Module Inf_NaN_Detection

   !!     Inf_NaN_Detection module
   !!     Copyright(c) 2003, Lahey Computer Systems, Inc.
   !!     Copies of this source code, or standalone compiled files
   !!     derived from this source may not be sold without permission
   !!     from Lahey Computers Systems. All or part of this module may be
   !!     freely incorporated into executable programs which are offered
   !!     for sale. Otherwise, distribution of all or part of this file is
   !!     permitted, provided this copyright notice and header are included.
   !!
   !!     This module exposes four elemental functions:
   !!
   !!     IsNAN(x)    - test for a "not a number" value
   !!
   !!     IsINF(x)    - test for either a positive or negative "infinite" value
   !!
   !!     IsPosINF(x) - test for a positive "infinite" value
   !!
   !!     IsNegINF(x) - test for a negative "infinite" value
   !!
   !!     Each function accepts a single or double precision real argument, and
   !!     returns a true or false value to indicate the presence of the value
   !!     being tested for. If the argument is array valued, the function returns
   !!     a conformable logical array, suitable for use with the ANY function, or
   !!     as a logical mask.
   !!
   !!     Each function operates by transferring the bit pattern from a real
   !!     variable to an integer container. Unless testing for + or - infinity,
   !!     the sign bit is cleared to zero. The value is exclusive ORed with
   !!     the value being tested for. The integer result of the IEOR function is
   !!     converted to a logical result by comparing it to zero.

   Implicit None
   Private
   Public :: IsNAN, IsINF, IsPosINF, IsNegINF

   ! Kind numbers for single and double precision integer containers
   Integer, Parameter :: Single = Selected_int_kind(Precision(1.0e0))
   Integer, Parameter :: Double = Selected_int_kind(Precision(1.0d0))

   ! Single precision IEEE values
   Integer(Single), Parameter :: sNaN    = Z"7FC00000"
   Integer(Single), Parameter :: sPosInf = Z"7F800000"
   Integer(Single), Parameter :: sNegInf = Z"FF800000"

   ! Double precision IEEE values
   Integer(Double), Parameter :: dNaN    = Z"7FF8000000000000"
   Integer(Double), Parameter :: dPosInf = Z"7FF0000000000000"
   Integer(Double), Parameter :: dNegInf = Z"FFF0000000000000"

   ! Locatation of single and double precision sign bit (Intel)
   ! Subtract one because bit numbering starts at zero
   Integer, Parameter :: SPSB = Bit_size(sNaN) - 1
   Integer, Parameter :: DPSB = Bit_size(dNaN) - 1

   Interface IsNAN
      Module Procedure sIsNAN
      Module Procedure dIsNAN
   End Interface IsNAN

   Interface IsINF
      Module Procedure sIsINF
      Module Procedure dIsINF
   End Interface IsINF

   Interface IsPosINF
      Module Procedure sIsPosINF
      Module Procedure dIsPosINF
   End Interface IsPosINF

   Interface IsNegINF
      Module Procedure sIsNegINF
      Module Procedure dIsNegINF
   End Interface IsNegINF

Contains

   ! Single precision test for NaN
   Elemental Function sIsNAN(x) Result(res)
      Real(Single), Intent(In) :: x
      Logical :: res
      res = Ieor(Ibclr(Transfer(x,sNan),SPSB), sNaN) == 0
   End Function sIsNAN

   ! Double precision test for NaN
   Elemental Function dIsNAN(d) Result(res)
      Real(Double), Intent(In) :: d
      Logical :: res
      res = Ieor(Ibclr(Transfer(d,dNaN),DPSB), dNaN) == 0
   End Function dIsNAN

   ! Single precision test for Inf
   Elemental Function sIsINF(x) Result(res)
      Real(Single), Intent(In) :: x
      Logical :: res
      res = Ieor(Ibclr(Transfer(x,sPosInf),SPSB), sPosInf) == 0
   End Function sIsINF

   ! Double precision test for Inf
   Elemental Function dIsINF(d) Result(res)
      Real(Double), Intent(In) :: d
      Logical :: res
      res = Ieor(Ibclr(Transfer(d,dPosInf),DPSB), dPosInf) == 0
   End Function dIsINF

   ! Single precision test for +Inf
   Elemental Function sIsPosINF(x) Result(res)
      Real(Single), Intent(In) :: x
      Logical :: res
      res = Ieor(Transfer(x,sPosInf), sPosInf) == 0
   End Function sIsPosINF

   ! Double precision test for +Inf
   Elemental Function dIsPosINF(d) Result(res)
      Real(Double), Intent(In) :: d
      Logical :: res
      res = Ieor(Transfer(d,dPosInf), dPosInf) == 0
   End Function dIsPosINF

   ! Single precision test for -Inf
   Elemental Function sIsNegINF(x) Result(res)
      Real(Single), Intent(In) :: x
      Logical :: res
      res = Ieor(Transfer(x,sNegInf), sNegInf) == 0
   End Function sIsNegINF

   ! Double precision test for -Inf
   Elemental Function dIsNegINF(d) Result(res)
      Real(Double), Intent(In) :: d
      Logical :: res
      res = Ieor(Transfer(d,dNegInf), dNegInf) == 0
   End Function dIsNegINF

End Module Inf_NaN_Detection


