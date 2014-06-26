subroutine CKPULS
! Created 29 August 1983 (L.A. Burns) to eliminate bad values, sort, and print
! pulse load vectors.
! Revised 05 May 1984 (LAB) -- command language revisions.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised Feb-08-1999 to use floating point comparisons
! Revised Jun-15-2001 to currect OBOB in "Tester" loop
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Floating_Point_Comparisons
Implicit None
! Local variables for this subroutine
real :: TEST, XTEMP
integer :: I, IA, IB, IC, ITEMP(4), J, NTEST
! NTEST counts passage of active locations while wringing out
! null sets during call from SHOW command.
logical :: Needs_sorting
Needs_sorting = .false.
! In mode 1, print dummy output table and return
if (MODEG == 1) then
   ! Fail-safe reset of NPULSE to prevent negative values
   if (NPULSE < 1) NPULSE = 0
   if (RPTFIL .or. BATCH==1) call PRPULS
   return
end if
! In RUN mode, test the dataset and kill bad entries
Run_mode: if (BATCH == 0) then
   NDAYS(2) = 29 ! Allow for leap day
   Bad_values: do I = 1, MAXMAS ! Process entire data set for bad values
      TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
      if (TEST .Equals. 0.0) cycle Bad_values ! Skip unused locations
      ! test source segment number
      if (ISEGG(I) < 1 .or. ISEGG(I) > KOUNT) then ! Bad value of ISEGG
         write (stderr,fmt='(A,I5)')& ! write message and then zero
            ' Warning: a pulse was specified for segment ',ISEGG(I),'.'
         write (stderr,5000)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
         cycle Bad_values
      end if
      ! ISEGG is O.K., test ICHEMG
      if (ICHEMG(I) < 0 .or. ICHEMG(I) > KCHEM) then ! Bad value of ICHEMG
         write (stderr,fmt='(A,I5,A)')& ! write message and then zero
            ' Warning: a pulse was specified for chemical ',ICHEMG(I),'.'
         write (stderr,5000)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
         cycle Bad_values
      end if
      ! Next test IMASSG:
      if (IMASSG(I) .LessThanOrEqual. 0.0) then ! Negative or zero IMASSG
         write (stderr,fmt='(A,1PG9.2,A)')&
            ' Warning: a pulse load of ',IMASSG(I),' was requested.'
         write (stderr,5000)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
         cycle Bad_values
      end if
      ! Months and days not used in operational MODE 2, so
      if (MODEG == 2) then ! Fail-safe set zeros in mode 2
         IMONG(I) = 0
         IDAYG(I) = 0
         cycle Bad_values
      end if
      ! Test month
      if (IMONG(I) < 1 .or. IMONG(I) > 12) then ! No such month
         write (stderr,fmt='(A,I5,A)')&
            ' Warning: a pulse was specified for month ',IMONG(I),'.'
         write (stderr,5000)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
         cycle Bad_values
      end if
      ! Test day
      if (IDAYG(I) < 1 .or. IDAYG(I) > NDAYS(IMONG(I))) then ! Bad day
         write (stderr,fmt='(A,I5,A,I5,A)')&
            ' Warning: a pulse was specified on day ',IDAYG(I),&
            ' of month ',IMONG(I),'.'
         write (stderr,5000)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
         cycle Bad_values
      end if
   end do Bad_values
end if Run_mode

! When in SHOW mode, all entries have been retained for further processing
NPULSE = 0 ! Counter for the number of valid pulses
! The full test is used here (rather, for example, than simply
! testing ISEGG for .NE. 0) to allow for the SHOW command:
do I = 1, MAXMAS
   TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
   if (TEST .NotEqual. 0.0) NPULSE = NPULSE+1
end do
if (NPULSE == 0) then ! If no pulses remain, simply print dummy table
   if (RPTFIL .or. BATCH==1) call PRPULS
   return
end if

! If only one pulse remains, make sure it is in position 1 and then print
One_pulse: if (NPULSE == 1) then
   Find_it: do I = 1, MAXMAS
      ! The full test is used here (rather, for example, than simply
      ! testing ISEGG(I) == 0) to allow for the SHOW command
      TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
      if (TEST .Equals. 0.0) cycle Find_it
      ! The vector location of the single pulse is "I" --
      ! move it to position 1 if necessary, and then print
      if (I>1) then
         ISEGG(1) = ISEGG(I)
         ICHEMG(1) = ICHEMG(I)
         IMONG(1) = IMONG(I)
         IDAYG(1) = IDAYG(I)
         IMASSG(1) = IMASSG(I)
         call Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
      end if
      if (RPTFIL .or. BATCH==1) call PRPULS
      return
   end do Find_it
end if One_pulse

! At least 2 non-zero pulses, therefore sort and compress vector
! as needed: Branch to appropriate sector for sorting, depending
! on operation (type of call and value of MODEG):
Show_mode: if (BATCH > 0) then ! show mode; wring out null sets only
   Wringer: do
      NTEST = 0
      Tester: do I = 1, MAXMAS
         TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
         if (TEST .NotEqual. 0.0) then
            NTEST = NTEST+1
            ! When all active pulses have been processed, print and return
            if (NTEST >= NPULSE) then
               if (NPULSE < 1) NPULSE = 0 ! fail-safe
               if (RPTFIL .or. BATCH==1) call PRPULS
               return
            end if
            cycle Tester
         end if
         ! The Ith item is zero: drop all remaining items by one location
         ! and shift the zero to location MAXMAS:
         do J = I, MAXMAS-1
            IMASSG(J) = IMASSG(J+1)
            IMONG(J) = IMONG(J+1)
            IDAYG(J) = IDAYG(J+1)
            ICHEMG(J) = ICHEMG(J+1)
            ISEGG(J) = ISEGG(J+1)
         end do
         IMASSG(MAXMAS) = 0.0
         IMONG(MAXMAS) = 0
         IDAYG(MAXMAS) = 0
         ICHEMG(MAXMAS) = 0
         ISEGG(MAXMAS) = 0
         ! Because the (I+1) item may also have been zero, the test must
         cycle Wringer ! now be redone
      end do Tester
   end do Wringer
end if Show_mode

Mode_select: select case (MODEG)
case (2) Mode_select
! Sorting may be required
do I = 1, MAXMAS ! load dummy values of ICHEM to force empties to bottom
   if (ICHEMG(I) == 0) ICHEMG(I) = 9999
end do
! Begin with bubble sort to determine if sorting is needed
Big_bubble: do I = 1, MAXMAS-1
   Little_bubble: do J = I+1, MAXMAS
      if (ICHEMG(I) > ICHEMG(J)) then ! chemicals out of order
         Needs_sorting = .true.
         exit Big_bubble
      else if (ICHEMG(I) < ICHEMG(J)) then   ! chemicals in order
         cycle Little_bubble                 ! so check the next pairing
      else if (ISEGG(I) > ISEGG(J)) then ! chemicals equal, test segments
         Needs_sorting = .true.
         exit Big_bubble
      end if
   end do Little_bubble
end do Big_bubble

if (Needs_sorting) then ! Sorting required
   Binary_Insertion_Sort: do I = 2, MAXMAS
      IA = 1
      IB = I
      Finder_loop: do
         if (IA > IB) exit Finder_loop
         IC = (IA+IB)/2
         if (ICHEMG(IC) < ICHEMG(I)) then
            IA = IC + 1
         else if (ICHEMG(IC) > ICHEMG(I)) then
            IB = IC -1
         else if (ISEGG(IC) > ISEGG(I)) then
            IB = IC-1
         else
            IA = IC+1
         end if
      end do Finder_loop
      ! Insert value in new location (unless insertion point is to the
      IC = IA      ! right of the current element)
      if (IC >= I) cycle Binary_insertion_sort
      XTEMP = IMASSG(I)
      ITEMP(1) = ICHEMG(I)
      ITEMP(2) = ISEGG(I)
      do J = I, IC+1, -1
         IMASSG(J) = IMASSG(J-1)
         ICHEMG(J) = ICHEMG(J-1)
         ISEGG(J) = ISEGG(J-1)
      end do
      IMASSG(IC) = XTEMP
      ICHEMG(IC) = ITEMP(1)
      ISEGG(IC) = ITEMP(2)
   end do Binary_insertion_sort
end if

case (3) Mode_select ! Sort and compress for MODE 3
! Load dummy values to dump unused locations to bottom
do I = 1, MAXMAS
   if (IMONG(I) == 0) IMONG(I) = 9999
end do
Big_bubbler: do I = 1, MAXMAS-1        ! Begin with bubble search
   Little_bubbler: do J = I+1, MAXMAS  ! to see if already sorted
      if (IMONG(I) > IMONG(J)) then
         Needs_sorting = .true.
         exit Big_bubbler
      else if (IMONG(I) < IMONG(J)) then
         cycle Little_bubbler
      else if (IDAYG(I) > IDAYG(J)) then
         Needs_sorting = .true.
         exit Big_bubbler
      else if (IDAYG(I) < IDAYG(J)) then
         cycle Little_bubbler
      else if (ICHEMG(I) > ICHEMG(J)) then
         Needs_sorting = .true.
         exit Big_bubbler
      else if (ICHEMG(I) < ICHEMG(J)) then
         cycle Little_bubbler
      else if (ISEGG(I) > ISEGG(J)) then
         Needs_sorting = .true.
         exit Big_bubbler
      end if
   end do Little_bubbler
end do Big_bubbler
if (Needs_sorting) then ! Binary insertion sorter
   Binary_insertion_sorter: do I = 2, MAXMAS
   IA = 1
   IB = I
   Locator_loop: do
      if (IA > IB) exit Locator_loop
      IC = (IA+IB)/2
      if (IMONG(IC)<IMONG(I)) then
         IA = IC+1
         cycle Locator_loop
      else if (IMONG(IC)>IMONG(I)) then
         IB = IC-1
         cycle Locator_loop
      else if (IDAYG(IC)<IDAYG(I)) then
         IA = IC+1
         cycle Locator_loop
      else if (IDAYG(IC)>IDAYG(I)) then
         IB = IC-1
         cycle Locator_loop
      else if (ICHEMG(IC)<ICHEMG(I)) then
         IA = IC+1
         cycle Locator_loop
      else if (ICHEMG(IC)>ICHEMG(I)) then
         IB = IC-1
         cycle Locator_loop
      else if (ISEGG(IC)<ISEGG(I)) then
         IA = IC+1
         cycle Locator_loop
      else
         IB = IC-1
      end if
   end do Locator_loop
   IC = IA     ! Insert value
   if (IC >= I) cycle Binary_insertion_sorter
   XTEMP = IMASSG(I)
   ITEMP(1) = IMONG(I)
   ITEMP(2) = IDAYG(I)
   ITEMP(3) = ICHEMG(I)
   ITEMP(4) = ISEGG(I)
   do J = I, IC+1, -1
      IMASSG(J) = IMASSG(J-1)
      IMONG(J) = IMONG(J-1)
      IDAYG(J) = IDAYG(J-1)
      ICHEMG(J) = ICHEMG(J-1)
      ISEGG(J) = ISEGG(J-1)
   end do
   IMASSG(IC) = XTEMP
   IMONG(IC) = ITEMP(1)
   IDAYG(IC) = ITEMP(2)
   ICHEMG(IC) = ITEMP(3)
   ISEGG(IC) = ITEMP(4)
   end do Binary_insertion_sorter
end if
case default Mode_select ! Corrupted value
   write (stderr,fmt='(A,I5/A)')& ! write error message and abort
      ' System failure in subroutine CKPULS: MODE is ',&
        MODEG,' RUN aborted.'
   IFLAG = 8
   return
end select Mode_select

! Print pulse vectors
do I = 1, MAXMAS        ! Remove dummy values of ICHEMG and IMONG
   if (ICHEMG(I) == 9999) ICHEMG(I) = 0
   if (IMONG(I)  == 9999) IMONG(I)  = 0
end do
! Compress vectors to combine redundant specifications (i.e., if
! 2 or more pulses are specified for a particular date, chemical,
! and segment, the entries are combined into a single unit):
select case (MODEG)
case (2)
   Mode_2_compression: do I = 1, MAXMAS-1
      if (I >= (NPULSE)) exit Mode_2_compression
      Mode_2_Inner_loop: do
         if (ICHEMG(I) /= ICHEMG(I+1)) cycle Mode_2_compression
         ! Same chemical, segments should differ
         if (ISEGG(I) /= ISEGG(I+1)) cycle Mode_2_compression
         ! Same chemical and segment--combine entries and compress vector
         IMASSG(I) = IMASSG(I)+IMASSG(I+1)
         do J = I+1, NPULSE-1
            ICHEMG(J) = ICHEMG(J+1)
            ISEGG(J) =  ISEGG(J+1)
            IMASSG(J) = IMASSG(J+1)
         end do
         ICHEMG(NPULSE) = 0
         ISEGG(NPULSE) = 0
         IMASSG(NPULSE) = 0.0
         NPULSE = NPULSE-1
         ! Outer loop will increment beyond current value and miss a third
         ! entry with identical data, hence here must restart inner loop with
         ! current value of counter
      end do Mode_2_Inner_loop
   end do Mode_2_compression

case (3) ! MODEG 3 compression check
   Mode_3_compression: do I = 1, MAXMAS-1
      if (I >= (NPULSE)) exit Mode_3_compression
      Mode_3_inner_loop: do
         if (IMONG(I) /= IMONG(I+1)) cycle Mode_3_compression
         ! Same month, check day:
         if (IDAYG(I) /= IDAYG(I+1))  cycle Mode_3_compression
         ! Same month and day, check chemical:
         if (ICHEMG(I) /= ICHEMG(I+1)) cycle Mode_3_compression
         ! Same date and chemical, check segment
         if (ISEGG(I) /= ISEGG(I+1)) cycle Mode_3_compression
         ! Redundant entry, compress vector
         IMASSG(I) = IMASSG(I)+IMASSG(I+1)
         Move_pointers: do J = I+1, NPULSE-1
            IMONG(J) = IMONG(J+1)
            IDAYG(J) = IDAYG(J+1)
            ICHEMG(J) = ICHEMG(J+1)
            ISEGG(J) = ISEGG(J+1)
            IMASSG(J) = IMASSG(J+1)
         end do Move_pointers
         IMONG(NPULSE) = 0 ! zero the slot
         IDAYG(NPULSE) = 0
         ICHEMG(NPULSE) = 0
         ISEGG(NPULSE) = 0
         IMASSG(NPULSE) = 0.0
         NPULSE = NPULSE-1
      end do Mode_3_Inner_loop
   end do Mode_3_compression
end select

if (NPULSE < 1) NPULSE = 0 ! Fail-safe reset of NPULSE
if (BATCH==1 .or. RPTFIL) call PRPULS
return
5000  format (' This entry has been deleted from the pulse load vectors.')
contains
subroutine Kill_entry (ICHEMG,ISEGG,IMONG,IDAYG,IMASSG)
   integer, dimension (:) :: ICHEMG,ISEGG,IMONG,IDAYG
   real,    dimension (:) :: IMASSG
   ! Bad value: clean out entry in vector so all unused portions
   ! contain zeros following a RUN.
   ICHEMG(I) = 0
   ISEGG(I)  = 0
   IMONG(I)  = 0
   IDAYG(I)  = 0
   IMASSG(I) = 0.0
end subroutine Kill_entry
end Subroutine CKPULS
