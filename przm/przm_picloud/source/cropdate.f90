Module m_Crop_Dates

   Use Date_Module
   Use m_debug
   Implicit None
   Include 'PPARM.INC'
   Include 'CCROP.INC'
   Include 'CMISC.INC'
   Private

   ! e_Bogus - No value
   Integer, Parameter, Public :: e_Bogus = -Huge(0)

   ! Julian day (J.D., JD) -- See module Date_Module (datemod.f90)

   ! The derived type t_Event contains information specific to the
   ! cropping period.
   ! Jd_begin - starting Julian Day of the cropping period, e.g.,
   !     Jd(yyyy=1961, mm=01, dd=01) =  2437301  1961-01-01
   !
   ! jd_end - ending Julian Day of the cropping period, e.g.,
   !     Jd(yyyy=1990, mm=12, dd=31) =  2448257  1990-12-31
   !
   ! jd_emergence, jd_maturation, jd_harvest - Julian day of the event.
   !
   ! CropPeriod - cropping period associated with the event type
   !              (Record 11). (1 <= CropPeriod <= ncpds)
   !
   ! Crop_Number - crop number of the cropping period
   !              (Record 9, variable ICNCN) (Record 11, INCROP)
   Type, Public :: t_Event
      Integer :: jd_begin = e_Bogus
      Integer :: jd_end = e_Bogus
      Integer :: jd_emergence = e_Bogus
      Integer :: jd_maturation = e_Bogus
      Integer :: jd_harvest = e_Bogus
      Integer :: CropPeriod = e_Bogus
      Integer :: Crop_Number = e_Bogus
   End Type t_Event

   ! Crop_Period contains all the significant events of the simulation.
   ! nEvents = Dimension of Crop_Period == ncpds
   ! Cropping periods:  InCrop(1:NCPDS)
   Type(t_Event), Dimension(:), Allocatable, Public, Save :: Crop_Period
   Integer, Save, Public :: nEvents = 0 ! eventually, Ubound(Crop_Period,1)

   ! "32" is hardwired in przm. We will make it a parameter.
   ! Plan for the future: allocate the arrays to the appropriate
   ! size.

   ! Use a leap year (Year_for_doy) to compute a day of the year (DoY)
   ! that works for both non-leap and leap years. Year_for_doy is an
   ! arbitrary leap year.
   Integer, Parameter, Public :: Year_for_doy = 1804
   Integer, Parameter, Public :: n32 = 32
   Type, Public :: t_Crop_Info
      Integer :: Crop_Number = e_Bogus
      Real :: Max_Interception_Storage = 0.0
      Real :: Max_Rooting_depth = 0.0
      Real :: Max_Areal_canopy_coverage = 0.0
      Integer :: nUSELEC = e_Bogus
      Integer, Dimension(:), Pointer :: doy => Null()
      Real, Dimension(:), Pointer :: USLE_C => Null()
      Real, Dimension(:), Pointer :: Manning_N => Null()
      Integer, Dimension(:), Pointer :: CN1 => Null()
      Integer, Dimension(:), Pointer :: CN2 => Null()
      Integer, Dimension(:), Pointer :: CN3 => Null()
   End Type t_Crop_Info

   ! Crop Info:  ICNCN(1:NDC)
   ! Number_of_Crops == NDC
   Type(t_Crop_Info), Dimension(:), Allocatable, Public, Save :: Crop_Info
   Integer, Save, Public :: Number_of_Crops = 0 ! eventually, Ubound(Crop_Info,1)

   ! Julian Day of the start and end dates of the simulation
   Integer, Save, Public :: Jd_Begin_Simul = 0
   Integer, Save, Public :: Jd_End_Simul = 0

   Public :: Events_Sort      ! Sort Crop_Info array
   Public :: Events_Print     ! Print Crop_Info (debug)
   Public :: Find_Crop_Number ! Determine the crop number active in a Julian Day
   Public :: Normalize_DoY    ! Normalize Day-of-Year
   !Public :: make_doy_table

Contains

   Subroutine Events_Sort ()

      ! Sort events array.

      Implicit None
      Integer :: i
      Integer, Dimension(:), Allocatable :: pList

      Allocate(pList(Nevents))
      pList = (/ (i, i = 1, nEvents) /)

      ! Sort events in chronological order
      Call SortHeap(nEvents, IsLess_Events, pList)
      Crop_Period = Crop_Period(pList)  ! Rearrange list.
      Deallocate(pList)

   End Subroutine Events_Sort


   Subroutine Events_Print (Ztitle)

      ! Sort events array.

      Implicit None
      Character(Len=*), Intent(In) :: Ztitle

      Integer :: i
      Character(Len=10) :: d_emergence, d_maturation, d_harvest, &
            d_begin, d_end

      Write (u0debug, 9140) Trim(Ztitle)
9140  Format (//, '*** ', a, ' ***')

      Do i = 1, nEvents

         Call i_to_ISO(d_begin, Julian_Day=Crop_Period(i)%Jd_begin)
         Call i_to_ISO(d_end, Julian_Day=Crop_Period(i)%jd_end)
         Call i_to_ISO(d_emergence, Julian_Day=Crop_Period(i)%jd_emergence)
         Call i_to_ISO(d_maturation, Julian_Day=Crop_Period(i)%jd_maturation)
         Call i_to_ISO(d_harvest, Julian_Day=Crop_Period(i)%jd_harvest)

         Write (u0debug, 9320) i, d_begin, d_end
9320     Format (/, 1x, 'Cropping period ', i0, ' starts on ', a, &
               ' and ends on ', a)

9340     Format (1x, 3x, a, a)
         Write (u0debug, 9340) 'Emergence ..: ', d_emergence
         Write (u0debug, 9340) 'Maturation .: ', d_maturation
         Write (u0debug, 9340) 'Harvest ....: ', d_harvest

9360     Format (1x, 3x, a, i0)
         Write (u0debug, 9360) 'CropPeriod .: ', Crop_Period(i)%CropPeriod
         Write (u0debug, 9360) 'Crop_Number : ', Crop_Period(i)%Crop_Number

      End Do

   End Subroutine Events_Print


   Subroutine SortHeap(nList, IsLess, pList)

      ! sorts into ascending order using the heap sort algorithm;
      ! outputs the array "pList" such that Crop_Period(pList) is in
      ! ascending order.
      !
      ! In input, pList must be initialized,
      !     pList(j) = j,  for j = 1, 2, ..., nList.
      !
      ! notes:
      ! * nList < 50,         straight insertion sort; order: nList^2
      ! * 50 < nList < 1000,  shell sort; order: nList^{3/2}
      ! * 1000 < nList,       heap sort;  order: nList log2(nList)
      !                       quick sort; order: nList log2(nList)

      Implicit None
      Integer,               Intent(In)    :: nList
      Integer, Dimension(:), Intent(InOut) :: pList

      Interface
         Function IsLess(Np1, Np2)
            Implicit None
            Integer, Intent(In) :: Np1, Np2
            Logical             :: IsLess
         End Function IsLess
      End Interface

      Integer :: ii, ir, i2, kk, phold

      kk = nList/2 + 1
      ir = nList

      ! the index kk will be decremented from its initial value down to 1 during the
      ! "hiring" (heap creation) phase.  once it reaches 1, the index *ir* will
      ! be decremented from its initial value down to 1 during the
      ! "retirement-and-promotion" (heap selection) phase.

      Do                            ! still in hiring phase
         If (kk > 1) Then
            kk = kk - 1
            phold = pList(kk)
         Else                       ! "retirement-and-promotion" (heap selection)
            phold = pList(ir)       ! clear a space at end of array
            pList(ir) = pList(1)    ! retire the top of the heap into it
            ir = ir - 1             ! decrease the size of the corporation
            If (ir == 1) Then       ! done with the last promotion
               pList(1) = phold     ! the least competent worker of all
               Return
            End If
         End If

         ! whether we are in the hiring phase or promotion phase, we here set up to sift
         ! down element phold to its proper level.

         ii = kk
         i2 = 2*kk
         Do While (i2 <= ir)
            If (i2 < ir) Then       ! then compare to better underling
               If (IsLess(pList(i2),pList(i2+1))) i2 = i2 + 1
            End If
            If (IsLess(phold,pList(i2))) Then  ! demote phold
               pList(ii) = pList(i2)
               ii = i2
               i2 = 2 * i2
            Else        ! this is phold's level.  set i2 to terminate the sift-down
               i2 = ir + 1
            End If
         End Do
         pList(ii) = phold          ! put phold into its slot
      End Do

   End Subroutine SortHeap


   Function IsLess_Events(Np1, Np2)

      ! IsLess_Events: Truth of "Crop_Period(Np1) < Crop_Period(Np2)"
      ! Compare by:
      ! #1. by Julian Day,
      ! #2. by initial order (to make IsLess_Events well defined).
      Implicit None
      Integer, Intent(In) :: Np1, Np2
      Logical             :: IsLess_Events

      If (Crop_Period(Np1)%Jd_begin /= Crop_Period(Np2)%Jd_begin) Then
         IsLess_Events = (Crop_Period(Np1)%Jd_begin < Crop_Period(Np2)%Jd_begin)
      Else
         IsLess_Events = (Np1 < Np2)
      End If

   End Function IsLess_Events


   Subroutine Find_Crop_Number (Julian_Day, In_Cropping_Period, &
         jNCP, jNCROP, jPos)

      ! Find the crop active in the given Julian Day.
      !
      ! In_Cropping_Period : Truth of "Julian_Day falls within a cropping period"
      ! In_Cropping_Period == .True.
      !        jNCP : Number of Current Cropping Period
      !        jNCROP : Number of Current Crop
      ! In_Cropping_Period == .False. then Julian_Day falls outside
      !     the range of all cropping periods.
      !     If (Julian_Day falls before Crop_Period(1))
      !        Use the crop associated with the first Cropping Period
      !     Else
      !        Use the crop associated with the previous (Jpos-1) Cropping Period
      !
      ! jPos : Position on the array where Julian_Day lies.
      !        See description of "npos" below

      Implicit None
      Integer, Intent(In)  :: Julian_Day
      Logical, Intent(Out) :: In_Cropping_Period
      Integer, Intent(Out) :: jNCP, jNCROP
      Integer, Optional, Intent(Out) :: jPos

      Logical :: xFound
      Integer :: low, high, middle, npos, zpos

      ! Crop_Period js sorted. Use a binary search to find the date.
      ! Average number of comparisons = Log_2(Nevents)
      !
      ! Xfound - Truth of "Julian_Day found in Crop_Period"
      !
      ! npos = position in Crop_Period where Julian_Day lies:
      ! npos range: (0 <= npos <= Nevents+1)
      !     If (1 <= npos <= Nevents)  (Xfound == .True.)
      !        Julian_Day <= Crop_Period(npos)%Jd_begin
      !
      !     If (npos < 1)  (Xfound == .False.)
      !        Julian_Day occurs before the first entry of Crop_Period;
      !        No cropping period js active.
      !
      !     If (npos > Nevents)  (Xfound == .False.)
      !        Julian_Day occurs after the last entry of Crop_Period;
      !        No cropping period js active.

      low = 1
      high = Nevents
      Xfound = .False.
      npos = 0
      In_Cropping_Period = .False.

      Do
         If (low > high) Exit
         middle = (low+high)/2
         If (Julian_Day == Crop_Period(middle)%Jd_begin) Then
            npos = middle
            Xfound = .True.
            Exit
         Else If (Julian_Day < Crop_Period(middle)%Jd_begin) Then
            high = middle - 1
         Else
            low = middle + 1
         End If
      End Do

      If (.Not. Xfound) npos = low
      If (Present(jPos)) jPos = npos

      If (Xfound) Then
         ! Date found implies we are at the boundary
         ! of a cropping period. This is the easy case.
         In_Cropping_Period = .True.
         jNCP = Crop_Period(npos)%CropPeriod
         jNCROP = Crop_Period(npos)%Crop_Number
      Else If (npos <= 1) Then
         ! Date falls before jd_begin of Crop_Period(1) :
         ! Not in a cropping period.
         In_Cropping_Period = .False.
         jNCP = Crop_Period(1)%CropPeriod
         jNCROP = Crop_Period(1)%Crop_Number
      Else
         ! (2 <= npos <= Nevents+1) implies (1 <= zpos <= Nevents).
         zpos = npos - 1
         ! We already know
         !     Crop_Period(zpos)%Jd_begin /= Julian_Day, and
         !     Crop_Period(zpos)%Jd_begin < Julian_Day.
         ! This is a sanity check.
         In_Cropping_Period = &
               (Crop_Period(zpos)%Jd_begin <= Julian_Day) .And. &
               (Julian_Day <= Crop_Period(zpos)%jd_end)
         jNCP = Crop_Period(zpos)%CropPeriod
         jNCROP = Crop_Period(zpos)%Crop_Number
      End If

   End Subroutine Find_Crop_Number



   Elemental Function Normalize_DoY(IYear, DoY) Result (Ival)

      ! Given a DoY and a year, Normalize_DoY returns:
      ! * if IYear is a leap year, DoY.
      ! * if IYear is a nonleap year, the value "leap_DoY"
      !   (table below) for the corresponding date.
      !
      ! Statement of the problem:
      ! PRZM record 9b specifies dates of the form day-month, e.g.,
      ! 1504 denotes 15-April. The dates are translated to day of
      ! the year (DoY). The problem is that the DoY (for a date after
      ! Feb-28) changes depending on the year (leap or non-leap).
      ! I.e.,
      !
      !      Month-day     nonleap_DoY        leap_DoY
      !      ---------     -----------        --------
      !       Jan-01            1                 1
      !         :               :                 :
      !       Feb-27           58                58
      !       Feb-28           59                59
      !       Feb-29                             60
      !       Mar-01           60                61
      !       Mar-02           61                62
      !         :               :                 :
      !       Dec-31          365               366
      !
      ! Normalize_DoY returns the same value for a Month-day combination,
      ! regardless of the year. Examples:
      !     Let
      !        1961: arbitrary nonleap year
      !        1964: arbitrary leap year
      !
      !     DoY   IYear    Normalize_DoY
      !     ---   -----    -------------
      !       1    1961         1
      !       1    1964         1
      !      60    1961        61   ! DoY 60 in a nonleap year corresponds
      !                             ! to Mar-01, which is DoY 61 in a leap year.
      !      60    1964        60   ! 1964 is a leap year.
      !     365    1961       366
      !     366    1964       366
      !
      ! No error checking is performed.
      !
      ! Restrictions:
      ! * Year 1582 : year of the Gregorian Calendrical reform.

      Implicit None
      Integer, Intent(In) :: IYear  ! year of the DoY

      ! 1 <= DoY <= 365 for nonleap IYear
      ! 1 <= DoY <= 366 for leap IYear
      Integer, Intent(In) :: DoY    ! day of the year
      Integer             :: Ival   ! Normalized DoY

      ! Day-of-the-Year(Feb-28) == 59 on a non-leap year.
      Integer, Parameter :: DoY_Feb_28 = 59

      Ival = DoY
      If (.Not. IsLeapYear(IYear)) Then
         ! IYear is not a leap year: increase DoY if the
         ! date falls after Feb-28.
         If (DoY > DoY_Feb_28) Ival = DoY + 1
      End If

   End Function Normalize_DoY



   Subroutine make_doy_table()

      ! make_doy_table ! m_debug

      Implicit None
      Integer :: imonth, iday
      Integer :: leap_DoY, nonleap_DoY
      Integer, Parameter :: yleap = 1804
      Integer, Parameter :: ynonleap = yleap + 1

      Integer, Dimension(:), Pointer :: Days_in_Month
      Days_in_Month => Number_of_Days_in_Month(Iyear=ynonleap)

      Write (802, 9220)
9220  Format (4x, '! Month-dd       nonleap_DoY     leap_DoY  ')
      Do imonth = 1, 12
         Do iday = 1, Days_in_Month(imonth)
            ! Month_Table
            leap_DoY = iDoY(yyyy=yleap, mm=imonth, dd=iday)
            nonleap_DoY = iDoY(yyyy=ynonleap, mm=imonth, dd=iday)
            Write (802, 9240) Month_Table(imonth)(1:3), iday, nonleap_DoY, leap_DoY
9240        Format (4x, '! ', a, '-', i2.2, 7x, i6, 3x, i6)
         End Do
      End Do

   End Subroutine make_doy_table

End Module m_Crop_Dates
