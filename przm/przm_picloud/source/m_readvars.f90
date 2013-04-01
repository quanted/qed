module m_readvars
	! this module contains global variables for przm.
	! Apr 13 10:40:12 EDT 2006 
	

   Use General_Vars
   Implicit None
   public
   
   ! flit_num - value determines which formulation of the curve numbers (CN) will
   !            be used.
   ! cn_beta - CN formulation as in przm 3.12 beta the Cn formulation has not
   ! 	changed between przm 3.12 beta and 3.12.2 (inclusive). See release_notes
   ! 	por przm 3.12.2
   ! cn_chow - CN formulation from Chow.
   ! references and code in file: cnfuns.90
   Integer, Parameter :: cn_beta = 0
   Integer, Parameter :: cn_chow = 1
   Integer, Public :: flit_num = cn_beta ! default value

end module m_readvars
