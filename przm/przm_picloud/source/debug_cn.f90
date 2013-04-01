module debug
	implicit None
	private
	public :: dump_CN
	Include "PPARM.INC"
	Include "CHYDR.INC"
	Include "CCROP.INC"

	integer, parameter, public :: u99966 = 99966
	integer, parameter, public :: uu_debug = u99966
contains

!------------------------------------------------
	subroutine dump_CN (IJ, T)
	integer, intent(IN), optional :: IJ
	Character(len=*), Intent(In), Optional :: T
	Character(Len=08)  :: xdate
	Character(Len=10)  :: xtime
	iNTEGER :: II, JJ, KK, j, k, uu, nn, I
	character(len=200) :: tcopy
	
	end subroutine dump_CN
end module debug

