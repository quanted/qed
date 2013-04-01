
Module Date_Module

   ! Valid inputs are:
   ! 1. Julian calendar    : from Mon 01 Jan -4712 (Julian Day number 0) to Thu 04 Oct 1582.
   ! 2. Gregorian calendar : from Fri 15 Oct 1582 to 31 Dec Huge(0).
   !
   ! The dates 1582-October 5-14 did not exist (at least in most
   !     Catholic Europe) and are invalid.
   !
   ! Date arguments are always in ISO format order, i.e., yyyy-mm-dd
   !
   ! Examples:
   !     Jd ....... 0   Mon Jan  1 -4712 (4713 B.C.)
   !     Jd . 584,257   Wed Aug 11, -3113 (Gregorian) Starting Epoch of the Maya long count
   !     Jd 2,299,160   Thu Oct  4 1582  ! Last day of the Julian calendar
   !     Jd 2,299,161   Fri Oct 15 1582  ! First day of the Gregorian calendar
   !     Jd 2,435,444   Fri Dec  2 1955
   !     Jd 2,443,644   Mon May 15 1978
   !
   ! References:
   ! [1] [Meeus] Astronomical Algorithms by Jean Meeus. Willmann-Bell,
   !     2nd ed., 1998.  (ISBN: 0-943396-61-1)
   !
   ! [2] [Baum] Date Algorithms, 1998.
   !     http://www.capecod.net/~pbaum/date/date0.htm
   !     <A HREF="e:\5\Fortran\Tests\Calendar\Docs\d1\050.Date.Algorithms.htm#$1">
   !
   ! [3] [Latham] Standard C Date/Time Library; Programming the Worlds Calendars and
   !     Clocks by Lance Latham. R&D Books, 1998. (ISBN: 0879304960)
   !
   ! [4] [D&R] Calendrical Calculations by Nachum Dershowitz, and Edward M. Reingold.
   !     Cambridge Univ Press, 1997. (ISBN: 0521564131)
   !     Note:  n B.C.E. = - (n - 1)    or    -n = (n + 1) B.C.E.
   !
   ! [5] http://aa.usno.navy.mil/data/docs/JulianDate.html
   !
   !
   ! History:
   ! [lsr] Thu Nov 15 08:49:15 2001
   ! * [Meeus] algorithms altered slightly to allow for integer Julian days,
   !   following recommendations in [Baum]. See also algorithmns in [Latham].

   Implicit None

   Private

   ! In the code that follows:
   ! yyyy : year -4712 .. -1, 0, 1, ...
   ! mm . : month 1..12
   ! dd . : day 1 .. 31 (depends on the month and the leapness of the year, obviously)
   ! Doy  : Day of the year;  1.Jan -> DoY 1, ..., 31.Dec -> DoY 365 or 366 (leap year)

   Public :: Jd            ! yyyy-mm-dd -> Julian Day
   Public :: Jd_to_ymd     ! Julian day -> yyyy-mm-dd
   Public :: iDoY          ! yyyy-mm-dd -> Day_of_Year, e.g., 1984-04-22 -> 113
   Public :: Day_Of_Week   ! yyyy-mm-dd -> 0(Sunday) .. 6(Saturday)
   Public :: IsLeapYear    ! Determine if Iyear is a leap year.
   Public :: Calend        ! yyyy, DoY  -> mm-dd
   Public :: DaySub        ! Jd -> yyyy-mm-dd, DoY, Day_of_Week
   Public :: Delta_Days    ! Number of days between two dates
   Public :: Unix_Date     ! e.g., 'Sat Sep  5 10:12:26 1998'
   Public :: ISO_Date      ! e.g., '1998-08-27 15:35:46'
   Public :: xTiming       ! time a procedure
   Public :: Elapsed_Time  ! Suitable for: ## Elapsed cpu time: 0:03:04.89
   Public :: Number_of_Days_in_Month ! e.g., 31, 28(or 29), ...
   Public :: i_to_ISO      ! counter DoY to ISO Date

   Type, Public :: Timing_Type
      Character(Len=80) :: Id
      Character(Len=80) :: ybegin_date, yend_date
      Real :: time_beg, time_end
   End Type Timing_Type

   Integer, Parameter, Public :: TBegin =  1010
   Integer, Parameter, Public :: TEnd   =  1020
   Integer, Parameter, Public :: TPrint =  1030

   Integer, Parameter ::   Month_January =  1
   Integer, Parameter ::  Month_February =  2
   Integer, Parameter ::     Month_March =  3
   Integer, Parameter ::     Month_April =  4
   Integer, Parameter ::       Month_May =  5
   Integer, Parameter ::      Month_June =  6
   Integer, Parameter ::      Month_July =  7
   Integer, Parameter ::    Month_August =  8
   Integer, Parameter :: Month_September =  9
   Integer, Parameter ::   Month_October = 10
   Integer, Parameter ::  Month_November = 11
   Integer, Parameter ::  Month_December = 12

   Character(Len=9), Dimension(12), Parameter, Public :: Month_Table = (/ &
         'January  ', 'February ',  'March    ', 'April    ', &
         'May      ', 'June     ',  'July     ', 'August   ', &
         'September', 'October  ',  'November ', 'December '  /)

   Character(Len=9), Dimension(0:6), Parameter :: DOW_Table = (/ &
         'Sunday   ', 'Monday   ',  'Tuesday  ', 'Wednesday', &
         'Thursday ', 'Friday   ',  'Saturday '               /)

   Integer, Dimension(12), Save, Target :: days_in_month_non_leap_year = &
         (/ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 /)

   Integer, Dimension(12), Save, Target :: days_in_month_leap_year = &
         (/ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 /)

   ! Days in (1582/October) == 21
   Integer, Dimension(12), Save, Target :: days_in_month_1582 = &
         (/ 31, 28, 31, 30, 31, 30, 31, 31, 30, 21, 30, 31 /)

   ! The PRZM year (e.g., 61) is effectively, years since 1900.
   ! Calendar year = iybase + (przm-2-digit-year)
   Integer, Parameter, Public :: iybase = 1900


Contains


   Pure Function xxJd(yyyy, mm, dd) Result(Ival)
      ! yyyy, mm, dd -> Julian Day. See [Latham] date_to_jd0,
      ! page 93 (with modifications).
      ! Example Jd(1970, 01, 01) = 2440588

      Implicit None
      Integer, Intent(In) :: yyyy, mm, dd
      Integer             :: Ival

      Real :: xx, rval, rday, rmonth, ryear

      ryear = yyyy
      rmonth = mm
      rday = dd

      If (yyyy == 1582) Then   ! 15 Oct 1582
         If (mm == Month_October) Then
            If ((4 < dd) .And. (dd < 15)) rday = 15
         End If
      End If

      xx = 12.0*(ryear+4800.0) + rmonth - 3.0
      rval = (2.0*Modulo(xx,12.0) + 7.0 + 365.0*xx) / 12.0
      rval = Floor(rval) + rday + Floor(xx/48.0) - 32083.0

      If (rval > 2299170.0) Then  ! Jd 2299170 == 1582/Oct/24
         rval = rval + Floor(xx/4800.0) - Floor(xx/1200.0) + 38.0
      End If

      Ival = Ceiling(rval)
   End Function xxJd


   Pure Function Jd(yyyy, mm, dd) Result(Ival)
      ! yyyy, mm, dd -> Julian Day. See [Meeus] pages 60-61.
      ! Example Jd(1970, 01, 01) = 2440588

      Implicit None
      Integer, Intent(In) :: yyyy
      Integer, Intent(In) :: mm
      Integer, Intent(In) :: dd
      Integer             :: Ival

      Integer :: jyear, jmonth, jday, aa, bb
      Logical :: is_Gregorian_date
      Real    :: rval

      jday = dd
      If (mm > Month_February) Then
         jyear = yyyy
         jmonth = mm
      Else
         ! i.e., if the date is in January or February, it is considered
         ! to be in the 13th or 14th month of the preceding year.
         jyear = yyyy - 1
         jmonth = mm + 12
      End If

      ! Determine if the given date occurs in the Julian or Gregorian calendar.
      ! Last Julian date ...: Thursday 1582-October-4 (Julian calendar)
      ! First Gregorian date: Friday 1582-October-15 (Gregorian calendar)
      is_Gregorian_date = .False.
      Select Case(yyyy)
      Case(-4712:1581)     ! Julian calendar
         is_Gregorian_date = .False.
      Case(1582)           ! Special case of year = 1582
         Select Case(mm)
         Case(Month_January : Month_September)
            is_Gregorian_date = .False.   ! still Julian calendar
         Case(Month_October)
            Select Case(dd)
            Case(:4)       ! Julian calendar ends 1582-October-4
               is_Gregorian_date = .False.
            Case(15:)      ! Gregorian calendar starts
               is_Gregorian_date = .True.
            Case Default   ! invalid day: 1582-October 5-14 did not exist
               jday = 15
               is_Gregorian_date = .True.
            End Select
         Case(Month_November, Month_December)
            is_Gregorian_date = .True.    ! Gregorian calendar
         Case Default
            ! month out of range
         End Select
      Case(1583:)          ! Gregorian calendar
         is_Gregorian_date = .True.
      Case Default
         ! year < -4712 is out of range for Julian day computation.
         is_Gregorian_date = .False.
      End Select

      If (is_Gregorian_date) Then
         aa = Floor(jyear/100.0)
         bb = 2 - aa + Floor(aa/4.0)
      Else
         bb = 0
      End If
      rval = Floor(365.25*(jyear+4716)) + Floor(30.6001*(jmonth+1)) &
            + jday + bb - 1524.5
      Ival = Ceiling(rval)
   End Function Jd


   Subroutine Jd_to_ymd(Jd, yyyy, mm, dd)
      ! Jd -> yyyy-mm-dd
      ! Example:  Call Jd_to_ymd(2440588, yyyy, mm, dd) returns 1970 1 1 .

      Implicit None
      Integer, Intent(In)  :: Jd    ! Julian day
      Integer, Intent(Out) :: yyyy, mm, dd

      Real    :: zz, zf, rday
      Integer :: ka, kb, kc, kd, ke, alpha, kz

      zz = Jd + 0.5
      kz = Floor(zz)
      zf = zz - kz
      If (kz < 2299161) Then
         ! Jd is a date in the Julian Calendar.
         ! Jd 2299161 == Fri Oct 15 1582 -- First day of the Gregorian calendar
         ka = kz
      Else
         alpha = Floor((kz-1867216.25)/36524.25)
         ka = kz + 1 + alpha - Floor(alpha/4.0)
      End If
      kb = ka + 1524
      kc = Floor((kb-122.1)/365.25)
      kd = Floor(365.25*kc)
      ke = Floor((kb-kd)/30.6001)

      rday = kb - kd - Floor(30.6001*ke) + zf
      dd = Floor(rday)

      If (ke < 14) Then
         mm = ke - 1
      Else
         mm = ke - 13
      End If

      If (mm > 2) Then
         yyyy = kc - 4716
      Else
         yyyy = kc - 4715
      End If
   End Subroutine Jd_to_ymd


   Pure Elemental Function iDoY(yyyy, mm, dd) Result(Ival)
      ! yyyy-mm-dd -> Day of the year (DoY).
      ! Example: iDoY(1984, 4, 22) = 113

      Implicit None
      Integer, Intent(In) :: yyyy, mm, dd
      Integer             :: Ival

      Ival = 1 + Delta_Days(yyyy, mm, dd, yyyy, 01, 01)
   End Function iDoY


   Pure Function Day_Of_Week(yyyy, mm, dd) Result(Ival)
      ! Day_Of_Week(yyyy, mm, dd) gives the weekday number
      !    0 = Sunday,
      !    1 = Monday,
      !      :
      !    6 = Saturday.
      !
      ! Example: Day_Of_Week(1970, 1, 1) = 4 = Thursday

      Implicit None
      Integer, Intent(In) :: yyyy, mm, dd
      Integer             :: Ival

      Ival = Mod(Jd(yyyy,mm,dd)+1.5, 7.0)
   End Function Day_Of_Week


   Pure Function IsLeapYear(Iyear) Result(qLeap)
      ! Determine if (astronomical) year Iyear is a leap year.

      Implicit None
      Integer, Intent(In) :: Iyear
      Logical             :: qLeap

      If (Iyear > 1583) Then
         ! Gregorian year
         qLeap = (((Mod(Iyear,4) == 0) .And. (Mod(Iyear,100) /= 0)) .Or. &
               (Mod(Iyear,400) == 0))
      Else
         ! Julian year
         qLeap = (Mod(Iyear,4) == 0)
      End If
   End Function IsLeapYear


   Function Number_of_Days_in_Month(Iyear) Result(pArray)

      ! Returns a pointer to an array.
      ! Usage:
      !        Integer, Dimension(:), Pointer :: Days_in_Month
      !        Days_in_Month => Number_of_Days_in_Month(Iyear=1960)

      Implicit None
      Integer,                Intent(In) :: Iyear
      Integer,  Dimension(:), Pointer    :: pArray

      If (IsLeapYear(Iyear)) Then
         pArray => days_in_month_leap_year
      Else
         pArray => days_in_month_non_leap_year
      End If

   End Function Number_of_Days_in_Month


   Subroutine i_to_ISO(ISOd, iYear, doy, iMonth, iMday, Julian_Day)

      ! Given
      ! 1. year and day_of_the_year (doy), or
      ! 2. year, month number, and day of the month, or
      ! 3. Julian day
      ! Return ISOd : character string of the form 'yyyy-mm-dd'
      !
      ! Examples:
      ! iYear=1961, doy= 11 : 1961-01-11 ( 11 days after 1961-01-00)
      ! iYear=1961, doy=366 : 1962-01-01 (366 days after 1961-01-00)
      ! iYear=1961, iMonth=01, iMday=01) : 1961-01-01
      ! Julian_Day= 2437301 : 1961-01-01

      Implicit None
      Character(Len=*), Intent(Out) :: ISOd     ! Len >= 10
      Integer, Optional, Intent(In) :: iYear
      Integer, Optional, Intent(In) :: doy      ! day of the year
      Integer, Optional, Intent(In) :: iMonth
      Integer, Optional, Intent(In) :: iMday    ! day of the month
      Integer, Optional, Intent(In) :: Julian_Day

      Integer :: jmm, jdd, jyyyy
      Integer :: Jd_of_DoY ! The Julian day of the day of the year

      9110 Format (i4.4, '-', i2.2, '-', i2.2)
      If (Present(iYear) .And. Present(doy)) Then
         Jd_of_DoY = Jd(iYear,01,01) + doy - 1
         Call Jd_to_ymd(Jd_of_DoY, jyyyy, jmm, jdd)
         Write (ISOd, 9110) jyyyy, jmm, jdd

      Else If (Present(iYear) .And. Present(iMonth) .and. Present(iMday)) Then
         Write (ISOd, 9110) iYear, iMonth, iMday

      Else If (Present(Julian_Day)) Then
         Call Jd_to_ymd(Julian_Day, jyyyy, jmm, jdd)
         Write (ISOd, 9110) jyyyy, jmm, jdd

      Else
         ISOd = '**NoDate**'
      End If

   End Subroutine i_to_ISO


   Subroutine Calend(yyyy, doy, mm, dd, Year_of_doy)
      ! yyyy, DoY -> mm, dd
      ! Examples:
      ! yyyy=1984, Doy=113 -> mm=4, dd=22
      ! yyyy=1961, doy=366 : 1962-01-01 (366 days after 1961-01-01)
      !                      mm=1, dd=1, Year_of_doy = 1962

      Implicit None
      Integer, Intent(In)  :: yyyy
      Integer, Intent(In)  :: doy
      Integer, Intent(Out) :: mm
      Integer, Intent(Out) :: dd
      Integer, Optional, Intent(Out) :: Year_of_doy

      Integer :: Jd_of_DoY ! The Julian day of the day of the year
      Integer :: y4

      ! The Julian day of the date is equal to the
      ! Julian day(beginning of the year) + (number of days since the beginning of the year)
      Jd_of_DoY = Jd(yyyy,01,01) + doy - 1

      Call Jd_to_ymd(Jd_of_DoY, y4, mm, dd)
      If (Present(Year_of_doy)) Year_of_doy = y4
   End Subroutine calend


   Subroutine DaySub(Jd, yyyy, mm, dd, wd, ddd)
      ! Jd -> yyyy-mm-dd, Day_of_Week(wd=0..6), and the Day of the Year(ddd=1..365,366)
      !
      ! Example: Call DaySub(2440588, yyyy, mm, dd, wd, ddd) yields 1970 1 1 4 1.

      Implicit None
      Integer, Intent(In)  :: Jd
      Integer, Intent(Out) :: yyyy, mm, dd
      Integer, Intent(Out) :: wd
      Integer, Intent(Out) :: ddd

      Call Jd_to_ymd(Jd, yyyy, mm, dd)
      wd = Day_Of_Week(yyyy, mm, dd)
      ddd = iDoY(yyyy, mm, dd)
   End Subroutine DaySub


   Pure Function Delta_Days(yyyy1, mm1, dd1, yyyy2, mm2, dd2) Result(Ival)
      ! Delta_Days is returned as the number of days between two dates, i.e, Date_1 - Date_2;
      ! Delta_Days will be positive if Date_1 is more recent than Date_2.

      Implicit None
      Integer, Intent(In) :: yyyy1, mm1, dd1 ! Date_1
      Integer, Intent(In) :: yyyy2, mm2, dd2 ! Date_2
      Integer             :: Ival

      Ival = Jd(yyyy1,mm1,dd1) - Jd(yyyy2,mm2,dd2)
   End Function Delta_Days


   Function Unix_Date() Result(Thedate) ! Thedate == 'Sat Sep  5 10:12:26 1998'

      Implicit None
      Character(Len=24)       :: Thedate

      Character(Len=08)       :: xdate    ! yyyymmdd
      Character(Len=10)       :: xtime    ! hhmmss.sss
      Character(Len(TheDate)) :: DateModel
      Integer                 :: idow
      Integer, Dimension(8)   :: V

      !            123456789=123456789=1234
      !    xdate:  yyyymmdd
      !    xtime:  hhmmss.sss
      !DateModel: 'Sat Sep  5 10:12:26 1998'
      !            123456789=123456789=1234
      DateModel = 'DOW mmm dd HH:mm:ss yyyy'

      Call Date_and_time(Date=xdate, Time=xtime, Values=V)

      idow = Day_Of_Week(yyyy=V(1), mm=V(2), dd=V(3))
      DateModel(01:03) = DOW_Table  (idow)(1:3) ! Name of the day of the week
      DateModel(05:07) = Month_Table(V(2))(1:3) ! Name of the Month
      DateModel(09:10) = xdate(7:8) ! day of Month
      DateModel(12:13) = xtime(1:2) ! hour
      DateModel(15:16) = xtime(3:4) ! minutes
      DateModel(18:19) = xtime(5:6) ! seconds
      DateModel(21:24) = xdate(1:4) ! year

      Thedate = DateModel
   End Function Unix_Date


   Function ISO_Date() Result(Thedate) ! Thedate == '1998-08-27 15:35:46'

      Implicit None
      Character(Len=19)       :: Thedate

      Character(Len=08)       :: xdate    ! yyyymmdd
      Character(Len=10)       :: xtime    ! hhmmss.sss
      Character(Len(TheDate)) :: DateModel

      !            123456789=123456789=
      !    xdate:  yyyymmdd
      !    xtime:  hhmmss.sss
      !DateModel: '1998-08-27 15:35:46'
      !            123456789=123456789=
      DateModel = 'yyyy-mm-dd hh:mm:ss'

      Call Date_and_time(Date=xdate, Time=xtime)
      DateModel(01:04) = xdate(1:4) ! year
      DateModel(06:07) = xdate(5:6) ! Month
      DateModel(09:10) = xdate(7:8) ! day of Month
      DateModel(12:13) = xtime(1:2) ! hour
      DateModel(15:16) = xtime(3:4) ! minutes
      DateModel(18:19) = xtime(5:6) ! seconds

      Thedate = DateModel
   End Function ISO_Date


   Subroutine xTiming(T, Tcode, Uout, Id)

      Implicit None
      Type(Timing_Type),          Intent(InOut) :: T
      Integer,                    Intent(In)    :: Tcode
      Integer,          Optional, Intent(In)    :: Uout
      Character(Len=*), Optional, Intent(In)    :: Id

      Character(Len=80) :: q0tmp
      Integer :: Jout, n

      If (Present(Id)) Then
         T%Id = Id
      End If

      Select Case(Tcode)
         Case(TBegin)
            Call CPU_Time(T%time_beg)
            T%ybegin_date = Unix_Date()

         Case(TEnd)
            Call CPU_Time(T%time_end)
            T%yend_date = Unix_Date()

         Case(TPrint)
            Call Elapsed_Time(T%time_end-T%time_beg, q0tmp)

            If (Present(Uout)) Then
               Jout = Uout
            Else
               Jout = 6
            End If

            Write (Jout, '(///)')
            n = Len_Trim(T%Id)
            If (n > 0) Then
               Write (Jout, '(a)') T%Id(1:n)
            End If

            Write (Jout, '(a)') Repeat('__', 20)
            Write (Jout, '(1x,a,a)') '## Started  on ....: ', Trim(T%ybegin_date)
            Write (Jout, '(1x,a,a)') '## Finished on ....: ', Trim(T%yend_date)
            Write (Jout, '(1x,a,a)') '## Elapsed cpu time: ', Trim(q0tmp)

         Case Default
      End Select

   End Subroutine xTiming


   Subroutine Elapsed_Time(DeltaSeconds, TheString)

      ! <A NAME="Elapsed_Time">
      ! subroutine duplicated in
      !     <A HREF="e:\5\Fortran\f90Lib\genutils.f90#Elapsed_Time">
      !
      ! Example:
      !     Real :: time_beg, time_end
      !     Call CPU_Time(time_beg)
      !     Call CPU_Time(time_end)
      !     Call Elapsed_Time(time_end-time_beg, q0tmp)
      !        e.g., q0tmp = '2:20:35.45'
      !
      ! ________________________________________
      ! ## Started  on ....: Mon Jan 07 15:27:12 2002
      ! ## Finished on ....: Mon Jan 07 15:30:33 2002
      ! ## Elapsed cpu time: 0:03:04.89

      Implicit None
      Real,             Intent(In)  :: DeltaSeconds
      Character(Len=*), Intent(Out) :: TheString

      Integer :: h, m, si
      Real :: sf

      h = DeltaSeconds / 3600.0
      m = (DeltaSeconds-h*3600.0) / 60.0
      si = DeltaSeconds - h*3600.0 - m*60.0
      sf = DeltaSeconds - Int(DeltaSeconds)
0030  Format (i4, ":", i2.2, ":", i2.2, f3.2)

      Write (TheString,0030) h, m, si, sf
      TheString = Adjustl(TheString)

   End Subroutine Elapsed_Time


End Module Date_Module


