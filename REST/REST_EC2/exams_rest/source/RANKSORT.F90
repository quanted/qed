Subroutine RankSort(N,Array,Date)
! Created 2002-05-03 (L.A. Burns)
! rank and sort (from largest to smallest) a real array for Weibull plots,
! using the HeapSort algorithm, with a companion array of associated dates
Implicit none
Integer, intent(in) :: N ! the size of the input array
Real :: Array(N), Isorter ! Array is the input array to be sorted
Character (len=10) :: Date(N)   ! for Exams' ISO 8601 dates, e.g., 2000-05-05
Character (len=10) :: DateSaver
Integer :: i, ir, j, k
if (N<2) return ! fail-safe; nothing to do
k=N/2+1
ir=N
Sorter: do
   Heap: if (k>1) then     ! still in heap creation phase
      k = k-1
      Isorter = Array(k)
      DateSaver = Date(k)
   else                    ! in heap selection phase
      Isorter = Array(ir)
      DateSaver = Date(ir)
      Array(ir) = Array(1)
      Date(ir) = Date(1)
      ir = ir-1
      if (ir==1) then
         Array(1) = Isorter
         Date(1)  = DateSaver
         return
      end if
   end if Heap
                           ! set up the sifting phase
   i=k
   j=k+k
   Sifter: do while (j<=ir)
      if (j<ir) then
         if (Array(j)>Array(j+1)) j=j+1
      end if
      if (Isorter>Array(j)) then
         Array(i) = Array(j)
         Date(i)  = Date(j)
         i=j; j=j+j
      else
         j=ir+1
      end if
   end do Sifter
   Array(i) = Isorter
   Date(i) = DateSaver
end do Sorter
end Subroutine RankSort
