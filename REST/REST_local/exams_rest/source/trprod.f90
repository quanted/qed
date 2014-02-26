subroutine TRPROD(K)
! TRPROD converts the input description of product chemistry into
! a matrix of first-order (/hr) transformation coefficients
! "YIELDL." YIELDL has dimensions /hour so that multiplication of
! chemical concentrations by YIELDL gives the rate of generation
! (mg/L/hr) of the daughter product.
! Revised 03-MAY-1985 (LAB) -- command language
! Revisions 10/22/88--run-time implementation of machine dependencies
! Converted to Fortran 90 and error checking improved 3/12/96
! Revised 2004-05-17 to include biolysis study temperatures
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
! Several variables moved to subroutines : DTEMP, TKEL, TEMP2,
! and integer J, II, KK
! J counts segment loops, II and KK index the ALPHA matrix
integer :: IFORM,ION,I1,I2,I3,N1
! IFORM decodes the RFORMG entries to 1, 2, 3, or 4 for processing
! ION is decoder and counter for ionic species (1 ... 7)
integer, intent(in) :: K
! The chemical given by "K" (passed via call list) denotes the
! chemical currently being processed in FIRORD; it is producing
! transformation products whose behavior is also being simulated.

Products: do N1 = 1, NTRAN ! Pass through all the product chemistry data
IFORM = 0 ! initialize on each pathway evaluation
if (CHPARG(N1) /= K) cycle Products ! if parent chemical not current chemical
! The current chemical produces a transformation product; make
! sure that the daughter is in the current simulation set:
if (TPRODG(N1) < 1 .or. TPRODG(N1) > KCHEM) then
  ! The transformation product is not in the current
  ! simulation set--so write a warning and go on:
  call Print_Header (stdout,N1,CHEMNA(CHPARG(N1)))
  write (stdout,fmt='(1X,A,I5,A,/,A)')&
  'in that the transformation product (TPROD) is chemical number',TPRODG(N1),&
  ',', ' which is not part of the current simulation. This entry was ignored.'
  cycle Products
end if
! Check on process specified:
if (NPROCG(N1) < 1 .or. NPROCG(N1) > 9) then
  call Print_Header (stdout,N1,CHEMNA(CHPARG(N1)))! Process number incorrect
  write (stdout,fmt='(A,I5,A,/,A,/,A)')&
  ' in that the process is numbered ',NPROCG(N1), '.',&
  ' Valid process numbers are 1 -- 9 inclusive. This entry was ignored.',&
  ' Type HELP NPROC for more information.'
cycle Products
!
end if
! Check on the designation of molecular species:
if (RFORMG(N1) < 1 .or. RFORMG(N1) > 32) then
   call Print_Header(stdout,N1,CHEMNA(CHPARG(N1))) ! error in reactive form
   write (stdout,fmt='(A,I5,A,/,A,/,A)')&
   ' in that the reactive chemical form is given as ', RFORMG(N1), '.',&
   ' This pathway was ignored.',&
   ' Valid values of RFORM can be seen by typing "HELP RFORM."'
   cycle Products
end if
! Transfer indices to simplify following code:
I1 = CHPARG(N1)
I2 = TPRODG(N1)
I3 = RFORMG(N1)
! Integer vectors are O.K.; proceed with computations:
! Calculate matrix indices for rate constants:
! If RFORMG specified as single form (not, e.g., all dissolved species), then
Single_species: if (.not. (I3 > 28)) then
   ION = int((float(I3)+3.0)/4.0) ! Calculate the number of the ion specified
   ! Check to be sure that such an ion exists:
   Species_problem: if (SPFLGG(ION,K) == 0) then! Problem: ion does not exist,
      call Print_Header(stdout,N1,CHEMNA(CHPARG(N1)))                   ! so write warning and ignore entry
      write (stdout,fmt='(A,/,A,/,A)')&
         ' in that the reactive form (RFORMG) specifies an ionic species',&
         ' that is not part of the molecular structure.',&
         ' This entry was ignored.'
      cycle Products ! skip to next entry
   end if Species_problem
   ! Calculate the form (dissolved (1), sediment-sorbed (2),
   ! DOC-complexed (3), or biosorbed (4)) implied by RFORMG
   IFORM = 4-(4*ION-I3) ! for transfer to computational procedures
   !
end if Single_species

! Biosorbed chemicals can only be scheduled for transformation by
! biological processes; at this point check for this error. If it is a
! single species, the form has been computed above, else it may be 32...
Biochemical_problem: if (IFORM == 4 .or. I3 == 32) then
   ! Reaction of biological form, check for biochemical reaction:
   Not_biological: if (.not. (NPROCG(N1) == 7 .or. NPROCG(N1) == 8)) then
      ! Error: biosorbed chemical species scheduled for non-biological
      call Print_Header(stdout,N1,CHEMNA(CHPARG(N1)))  ! transformation. Write warning and ignore entry.
      write (stdout,fmt='(A,/,A)')&
        ' in that a non-biological reaction is specified',&
        ' from a biosorbed chemical species. This pathway was ignored.'
      cycle Products ! Skip to next Pathway entry
   end if Not_biological
end if Biochemical_problem

! Should the process yield be zero, write warning
Yield_problem1: if ( (YIELDG(N1) .Equals. 0.0) & !   yield=0
               .and. (EAYLDG(N1) .Equals. 0.0))& ! + eayld=0
      then
      call Print_Header(stdout,N1,CHEMNA(CHPARG(N1)))
      write (stdout,fmt='(A,/,A)')&
      ' in that the transformation pathway specifies zero yield.',&
      ' This pathway was executed, but no reaction products will be observed.'
end if Yield_problem1

! Should the process yield be negative, report problem and skip entry
Yield_problem2: if (YIELDG(N1) .LessThan. 0.0) then
   ! yield is negative (or, worse yet, the log of A is negative)...
   call Print_Header(stdout,N1,CHEMNA(CHPARG(N1)))
   cases: if (EAYLDG(N1) .Equals. 0.0) then ! eayld = 0
     write (stdout,fmt='(A)')&
       ' in that the transformation pathway specifies negative yield.'
   else; write (stdout,fmt='(A)')&
       ' in that the Briggsian log of the pre-exponential factor is negative.'
   end if cases
   write (stdout,fmt='(A)') ' This pathway was ignored.'
   cycle Products ! Skip to next Pathway entry
end if Yield_problem2

Reaction_class: Select case (NPROCG(N1))
case (1:3) Reaction_class ! hydrolysis products
   call HYDPR(IFORM,ION,I1,I2,I3,K,N1,stdout)
case (4:6) Reaction_class ! photochemical products
  call PHOPR(IFORM,ION,I1,I2,I3,K,N1,stdout)
case (7:8) Reaction_class ! biotransformation products
  call BIOPR(IFORM,ION,I1,I2,I3,K,N1,stdout)
case (9) Reaction_class ! reduction products
  call REDPR(IFORM,ION,I1,I2,I3,K,N1,stdout)
case default Reaction_class ! Fail-safe sector -- code malfunction
   call Print_Header(stdout,N1,CHEMNA(CHPARG(N1)))
   write (stdout,fmt='(A)') &
   " This entry has caused a code malfunction in TRPROD."
end select Reaction_class
end do Products ! End of loop through product chemistry data

! If this is the last chemical in the simulation, make a final sweep
! of the product chemistry to warn user should there be some parent chemicals
! specified that are not currently being simulated, to check for partial
! data entries, etc.
Check_for_errors: if (K == KCHEM) then
   Check_parents: do N1 = 1, NTRAN
      if (CHPARG(N1) < 0 .or. CHPARG(N1) > KCHEM) then
        write (stdout,fmt='(/,A,/,A,I5,A,I5,A,/,A)')&
        ' WARNING: The product chemistry dataset includes a parent chemical',&
        ' that is not under consideration (at Pathway',N1,', CHPAR =',&
        CHPARG(N1),').',' This entry was ignored.'
      end if
   end do Check_parents
   Other_errors: do N1 = 1, NTRAN
      if (CHPARG(N1) == 0) then
        if (  (EAYLDG(N1) .NotEqual. 0.0)  .or. & ! Enthalpy /= 0
              (YIELDG(N1) .NotEqual. 0.0)  .or. & ! Yield /= 0
               NPROCG(N1) /= 0             .or. & ! process
               RFORMG(N1) /= 0             .or. & ! reactive form
               TPRODG(N1) /= 0                  & ! product I.D.
           ) write(stdout,fmt='(/,A,/,A,I5,A)')&
          '  WARNING: The product chemistry dataset includes an incomplete',&
          '  specification at Pathway ',N1,'. This entry was ignored.'
      end if
   end do Other_errors
end if Check_for_errors
return
end subroutine TRPROD

subroutine HYDPR(IFORM,ION,I1,I2,I3,K,N1,ttyout)
use Floating_Point_Comparisons
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real (kind (0D0)) :: DTEMP
real :: TEMP2, TKEL
integer :: II, J, KK
integer :: IFORM,ION,I1,I2,I3,K,N1,ttyout
! This subroutine computes hydrolysis transformation products
real :: HPLUS, HYDRX, KAHL, KNHL, KBHL ! Hydrolysis parameters
DTEMP = 0.0D+00 ! initialize on each pathway evaluation
Process: select case (NPROCG(N1)) ! Branch to proper hydrolysis subsection
case (1) Process!-specific acid hydrolysis
  Forms1: select case (RFORMG(N1))
  case (1:28) Forms1!-single reactive form
    Segments1: do J = 1, KOUNT
      TKEL = TCELG(J,NDAT)+273.15
      HPLUS = 10.**(-PHG(J,NDAT))
      KAHL = KAHG(IFORM,ION,I1)
      if (EAHG(IFORM,ION,I1) .NotEqual. 0.0) KAHL =&
         10.**(KAHG(IFORM,ION,I1)-(EAHG(IFORM,ION,I1)/(R_Factor*TKEL)))
      TEMP2 = YIELDG(N1) ! Compute yield factor
      if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
         10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
      DTEMP = &        ! Add this path to total transformation yield
              TEMP2*KAHL*(MWTG(I2)/MWTG(I1))*HPLUS*ALPHA(I3,J,K)
      YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      ! Correction for molecular weights converts input units (Mole
      ! product produced per Mole parent compound reacted) to
      ! weight/weight factor, i.e., mg produced per mg reacted.
    end do Segments1
  case (29:) Forms1!-sector for multiple forms (e.g., all dissolved forms)
    IFORM = RFORMG(N1)-28
    Segments11: do J = 1, KOUNT
      II = -3
      TKEL = TCELG(J,NDAT)+273.15
      HPLUS = 10.**(-PHG(J,NDAT))
      Species1: do ION = 1, 7
        II = II + 1
        if (SPFLGG(ION,I1) == 0) cycle Species1 ! Skip non-existent species
        KAHL = KAHG(IFORM,ION,I1)
        if (EAHG(IFORM,ION,I1) .NotEqual. 0.0) KAHL =&
          10.**(KAHG(IFORM,ION,I1)-(EAHG(IFORM,ION,I1)/(R_Factor*TKEL)))
        TEMP2 = YIELDG(N1)
        if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
          10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
        KK = 3*ION+II+IFORM-1
        DTEMP = TEMP2*KAHL*(MWTG(I2)/MWTG(I1))*HPLUS*ALPHA(KK,J,K)
        YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      end do Species1
    end do Segments11
  end select Forms1
case (2) Process!-neutral hydrolysis
  Forms2: select case (RFORMG(N1))
  case (1:28) Forms2!-single reactive form
    Segments2: do J = 1, KOUNT ! Loop on segments
      TKEL = TCELG(J,NDAT)+273.15
      KNHL = KNHG(IFORM,ION,I1)
      if (ENHG(IFORM,ION,I1) .NotEqual. 0.0) KNHL =&
        10.**(KNHG(IFORM,ION,I1)-(ENHG(IFORM,ION,I1)/(R_Factor*TKEL)))
      TEMP2 = YIELDG(N1) ! Compute yield factor
      if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
        10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
      DTEMP = &       ! Add this path to total transformation yield
              TEMP2*KNHL*(MWTG(I2)/MWTG(I1))*ALPHA(I3,J,K)
      YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      ! Correction for molecular weights converts input units (Mole
      ! product C produced per Mole parent compound reacted) to
      ! weight/weight factor C i.e., mg produced per mg reacted.
    end do Segments2
  case (29:) Forms2!-multiple reactive forms (e.g., all dissolved forms)
    IFORM = RFORMG(N1)-28
    Segments22: do J = 1, KOUNT ! Loop on segments
      II = -3
      TKEL = TCELG(J,NDAT)+273.15
      Species2: do ION = 1, 7
        II = II+1
        if (SPFLGG(ION,I1) == 0) cycle Species2
        KNHL = KNHG(IFORM,ION,I1)
        if (ENHG(IFORM,ION,I1) .NotEqual. 0.0) KNHL =&
          10.**(KNHG(IFORM,ION,I1)-(ENHG(IFORM,ION,I1)/(R_Factor*TKEL)))
        TEMP2 = YIELDG(N1)
        if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
        10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
        KK = 3*ION+II+IFORM-1
        DTEMP = TEMP2*KNHL*(MWTG(I2)/MWTG(I1))*ALPHA(KK,J,K)
        YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      end do Species2
    end do Segments22
  end select Forms2
case (3) Process!-specific base hydrolysis:
  Forms3: select case (RFORMG(N1))
  case (1:28) Forms3!-single reactive form
    Segments3: do J = 1, KOUNT ! Loop on segments
      TKEL = TCELG(J,NDAT)+273.15
      HYDRX = 10.**(-POHG(J,NDAT))
      KBHL = KBHG(IFORM,ION,I1)
      if (EBHG(IFORM,ION,I1) .NotEqual. 0.0) KBHL =&
        10.**(KBHG(IFORM,ION,I1)-(EBHG(IFORM,ION,I1)/(R_Factor*TKEL)))
      TEMP2 = YIELDG(N1) ! Compute yield factor
      if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
        10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
      DTEMP = &       ! Add this path to total transformation yield
              TEMP2*KBHL*(MWTG(I2)/MWTG(I1))*HYDRX*ALPHA(I3,J,K)
      YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      ! Correction for molecular weights converts input units (Mole
      ! product produced per Mole parent compound reacted) to
      ! weight/weight factor i.e., mg produced per mg reacted.
    end do Segments3
  case (29:) Forms3!-multiple reactive forms (e.g., all dissolved forms)
    IFORM = RFORMG(N1)-28
    Segments33: do  J = 1, KOUNT ! Loop on segments
      II = -3
      TKEL = TCELG(J,NDAT)+273.15
      HYDRX = 10.**(-POHG(J,NDAT))
      Species3: do ION = 1, 7
        II = II+1
        if (SPFLGG(ION,I1) == 0) cycle Species3
        KBHL = KBHG(IFORM,ION,I1)
        if (EBHG(IFORM,ION,I1) .NotEqual. 0.0) KBHL =&
          10.**(KBHG(IFORM,ION,I1)-(EBHG(IFORM,ION,I1)/(R_Factor*TKEL)))
        TEMP2 = YIELDG(N1)
        if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
          10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
        KK = 3*ION+II+IFORM-1
        DTEMP = TEMP2*KBHL*(MWTG(I2)/MWTG(I1))*HYDRX*ALPHA(KK,J,K)
        YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      end do Species3
    end do Segments33
  end select Forms3
case default Process! Fail-safe sector; code malfunction
   ! print name of chemical and Pathway number
   call Print_Header(TTYOUT,N1,CHEMNA(CHPARG(N1)))
   write (TTYOUT,fmt='(A)')&
      ' which has caused a code malfunction in HYDPR.'
end select process
end Subroutine HYDPR

subroutine PHOPR(IFORM,ION,I1,I2,I3,K,N1,ttyout)
use Floating_Point_Comparisons
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real (kind (0D0)) :: DTEMP
integer II, J, KK
integer :: IFORM,ION,I1,I2,I3,K,N1,ttyout
real :: KOXL, K1O2L, TEMP2, TKEL
DTEMP = 0.0D+00 ! initialize on each pathway evaluation
Process: select case (NPROCG(N1))
case (4) Process!-direct photolysis
   Forms4: select case (RFORMG(N1))
   case (1:28) Forms4!-single reactive form
      Segments4: do J = 1, KOUNT ! Loop on segments
         TKEL = TCELG(J,NDAT)+273.15
         TEMP2 = YIELDG(N1) ! Compute yield factor
         if (EAYLDG(N1) .NotEqual. 0.0) &
            TEMP2 = 10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         DTEMP = TEMP2*KDPL(ION,J)*(MWTG(I2)/MWTG(I1))*& ! Add this path to
            QYield(IFORM,ION,I1)*ALPHA(I3,J,K) ! the total yield
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         ! Correction for molecular weights converts input units (Mole
         ! product produced per Mole parent compound reacted) to
         ! weight/weight factor i.e., mg produced per mg reacted.
      end do Segments4
   case (29:) Forms4!-sector for multiple forms (e.g., all dissolved forms)
      IFORM = RFORMG(N1)-28
      Segments44: do J = 1, KOUNT
         TKEL = TCELG(J,NDAT)+273.15
         II = -3
         Species4: do ION = 1, 7
            II = II+1
            if (SPFLGG(ION,I1) == 0) cycle Species4
            TEMP2 = YIELDG(N1)
            if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 = 10.**(YIELDG(N1)-&
               (EAYLDG(N1)/(R_Factor*TKEL)))
            KK = 3*ION+II+IFORM-1
            DTEMP = TEMP2*KDPL(ION,J)*(MWTG(I2)/MWTG(I1))*&
               QYield(IFORM,ION,I1)*ALPHA(KK,J,K)
            YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
        end do Species4
      end do Segments44
   end select Forms4
case (5) Process!-singlet oxygen
   Forms5: select case (RFORMG(N1))
   case (1:28) Forms5!-single reactive species
      Segments5: do J = 1, KOUNT ! Loop on segments
         TKEL = TCELG(J,NDAT)+273.15
         K1O2L = K1O2G(IFORM,ION,I1)
         if (EK1O2G(IFORM,ION,I1) .NotEqual. 0.0) K1O2L = 10.**&
            (K1O2G(IFORM,ION,I1)-(EK1O2G(IFORM,ION,I1)/(R_Factor*TKEL)))
         TEMP2 = YIELDG(N1) ! Compute yield factor
         if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 = 10.**&
            (YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         DTEMP = TEMP2*K1O2L*(MWTG(I2)/MWTG(I1))*S1O2L(J)*ALPHA(I3,J,K)
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         ! Correction for molecular weights converts input units (Mole
         ! product produced per Mole parent compound reacted) to
         ! weight/weight factor i.e., mg produced per mg reacted.
      end do Segments5
   case (29:) Forms5!-sector for multiple forms (e.g., all dissolved forms)
      IFORM = RFORMG(N1)-28
      Segments55: do J = 1, KOUNT
         II = -3
         TKEL = TCELG(J,NDAT)+273.15
         Species5: do ION = 1, 7
            II = II+1
            if (SPFLGG(ION,I1) == 0) cycle Species5
            K1O2L = K1O2G(IFORM,ION,I1)
            if (EK1O2G(IFORM,ION,I1) .NotEqual. 0.0) K1O2L = 10.**&
            (K1O2G(IFORM,ION,I1)-(EK1O2G(IFORM,ION,I1)/(R_Factor*TKEL)))
            TEMP2 = YIELDG(N1)
            if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =10.**&
               (YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
            KK = 3*ION+II+IFORM-1
            DTEMP = TEMP2*K1O2L*(MWTG(I2)/MWTG(I1))*S1O2L(J)*ALPHA(KK,J,K)
            YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         end do Species5
      end do Segments55
   end select Forms5
case (6) Process!-free-radical oxidants
   Forms6: select case (RFORMG(N1))
   case (1:28) Forms6!-single reactive form
      Segments6: do J = 1, KOUNT ! Loop on segments
         TKEL = TCELG(J,NDAT)+273.15
         KOXL = KOXG(IFORM,ION,I1)
         if (EOXG(IFORM,ION,I1) .NotEqual. 0.0) KOXL = 10.**&
            (KOXG(IFORM,ION,I1)-(EOXG(IFORM,ION,I1)/(R_Factor*TKEL)))
         TEMP2 = YIELDG(N1) ! Compute yield factor
         if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 = 10.**&
            (YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         DTEMP = TEMP2*KOXL*(MWTG(I2)/MWTG(I1))*OXRADL(J)*ALPHA(I3,J,K)
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         ! Correction for molecular weights converts input units (Mole
         ! product produced per Mole parent compound reacted) to
         ! weight/weight factor i.e., mg produced per mg reacted.
      end do Segments6
   case (29:) Forms6!-sector for multiple forms (e.g., all dissolved forms)
      IFORM = RFORMG(N1)-28
      Segments66: do J = 1, KOUNT
         II = -3
         TKEL = TCELG(J,NDAT)+273.15
         Species6: do ION = 1, 7
            II = II+1
            if (SPFLGG(ION,I1) == 0) cycle Species6
            KOXL = KOXG(IFORM,ION,I1)
            if (EOXG(IFORM,ION,I1) .NotEqual. 0.0) KOXL = 10.**&
               (KOXG(IFORM,ION,I1)-(EOXG(IFORM,ION,I1)/(R_Factor*TKEL)))
            TEMP2 = YIELDG(N1)
            if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
              10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
            KK = 3*ION+II+IFORM-1
            DTEMP = TEMP2*KOXL*(MWTG(I2)/MWTG(I1))*OXRADL(J)*ALPHA(KK,J,K)
            YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         end do Species6
      end do Segments66
   end select Forms6
case default Process! Fail-safe sector--code malfunction
   call Print_Header(TTYOUT,N1,CHEMNA(CHPARG(N1)))
   write (TTYOUT,fmt='(A)')&
      ' which has caused a code malfunction in PHOPR.'
end select Process
end subroutine PHOPR

subroutine BIOPR(IFORM,ION,I1,I2,I3,K,N1,ttyout)
use Floating_Point_Comparisons
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real (kind (0D0)) :: DTEMP
integer :: II, J, KK
integer :: IFORM,ION,I1,I2,I3,K,N1,ttyout
real :: ACBACL, KBACWLocal, KBACSLocal, TEMP2, TKEL
DTEMP = 0.0D+00 ! initialize on each pathway evaluation
Process: select case (NPROCG(N1))
case (7) Process!-bacterial biolysis in water column:
   Forms7: select case (RFORMG(N1))
   case (1:28) Forms7!-single reactive form
      Segments7: do J = 1, KOUNT
         if (TYPEG(J) == 'B') cycle Segments7 ! Skip benthic segments
         ACBACL = BACPLG(J,NDAT)
         KBACWLocal = KBACWL(IFORM,ION,I1)
         if (QTBAWG(IFORM,ION,I1) .NotEqual. 0.0) KBACWLocal = &
            KBACWL(IFORM,ION,I1)*&
            QTBAWG(IFORM,ION,I1)**((TCELG(J,NDAT)-QTBTWG(IFORM,ION,I1))/10.0)
         TEMP2 = YIELDG(N1) ! Compute yield factor
         if (EAYLDG(N1) .NotEqual. 0.0) then
            TKEL = TCELG(J,NDAT)+273.15
            TEMP2 = 10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         endif
         DTEMP = &       ! Add this path to total transformation yield
                 TEMP2*KBACWLocal*(MWTG(I2)/MWTG(I1))*ACBACL*ALPHA(I3,J,K)
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         ! Correction for molecular weights converts input units (Mole
         ! product produced per Mole parent compound reacted) to
         ! weight/weight factor i.e., mg produced per mg reacted.
      end do Segments7
   case (29:) Forms7!-sector for multiple forms (e.g., all dissolved forms)
      IFORM = RFORMG(N1)-28
      Segments77: do J = 1, KOUNT
         II = -3
         if (TYPEG(J) == 'B') cycle Segments77 ! Skip benthic segments
         ACBACL = BACPLG(J,NDAT)
         Species7: do ION = 1, 7
            II = II+1
            if (SPFLGG(ION,I1) == 0) cycle Species7
            KBACWLocal = KBACWL(IFORM,ION,I1)
            if (QTBAWG(IFORM,ION,I1) .NotEqual. 0.0) KBACWLocal = &
               KBACWL(IFORM,ION,I1)*QTBAWG(IFORM,ION,I1)**&
                    ((TCELG(J,NDAT)-QTBTWG(IFORM,ION,I1))/10.0)
            TEMP2 = YIELDG(N1)
            if (EAYLDG(N1) .NotEqual. 0.0) then
               TKEL = TCELG(J,NDAT)+273.15
               TEMP2 = 10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
            endif
            KK = 3*ION+II+IFORM-1
            DTEMP = TEMP2*KBACWLocal*(MWTG(I2)/MWTG(I1))*ACBACL*ALPHA(KK,J,K)
            YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         end do Species7
      end do Segments77
   end select Forms7
case (8) Process!-bacterial biolysis in bottom sediments
   Forms8: select case (RFORMG(N1))
   case (1:28) Forms8!-single reactive form
      Segments8: do J = 1, KOUNT ! Loop on segments
         if (TYPEG(J) /= 'B') cycle Segments8 ! Skip water column segments
         ACBACL = (BNBACG(J,NDAT)*SEDMSL(J))/(WATVOL(J)*100.)
         KBACSLocal = KBACSL(IFORM,ION,I1)
         if (QTBASG(IFORM,ION,I1) .NotEqual. 0.0) KBACSLocal = &
            KBACSL(IFORM,ION,I1)*&
            QTBASG(IFORM,ION,I1)**((TCELG(J,NDAT)-QTBTSG(IFORM,ION,I1))/10.0)
         TEMP2 = YIELDG(N1) ! Compute yield factor
         if (EAYLDG(N1) .NotEqual. 0.0) then
            TKEL = TCELG(J,NDAT)+273.15
            TEMP2 = 10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         endif
         DTEMP = &        ! Add this path to total transformation yield
                 TEMP2*KBACSLocal*(MWTG(I2)/MWTG(I1))*ACBACL*ALPHA(I3,J,K)
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         ! Correction for molecular weights converts input units (Mole
         ! product produced per Mole parent compound reacted) to
         ! weight/weight factor i.e., mg produced per mg reacted.
      end do Segments8
   case (29:) Forms8!-sector for multiple forms (e.g., all dissolved forms)
      IFORM = RFORMG(N1)-28
      Segments88: do J = 1, KOUNT
         II = -3
         if (TYPEG(J) /= 'B') cycle Segments88 ! Skip water column segments
         ACBACL = (BNBACG(J,NDAT)*SEDMSL(J))/(WATVOL(J)*100.)
         Species8: do ION = 1, 7
            II = II+1
            if (SPFLGG(ION,I1) == 0) cycle Species8
            KBACSLocal = KBACSL(IFORM,ION,I1)
            if (QTBASG(IFORM,ION,I1) .NotEqual. 0.0) KBACSLocal = &
              KBACSL(IFORM,ION,I1)*QTBASG(IFORM,ION,I1)**&
                    ((TCELG(J,NDAT)-QTBTSG(IFORM,ION,I1))/10.0)
            TEMP2 = YIELDG(N1)
            if (EAYLDG(N1) .NotEqual. 0.0) then
               TKEL = TCELG(J,NDAT)+273.15
               TEMP2 = 10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
            endif
            KK = 3*ION+II+IFORM-1
            DTEMP = TEMP2*KBACSLocal*(MWTG(I2)/MWTG(I1))*ACBACL*ALPHA(KK,J,K)
            YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
         end do Species8
      end do Segments88
   end select Forms8
case default Process  ! Fail-safe sector -- code malfunction
   call Print_Header(TTYOUT,N1,CHEMNA(CHPARG(N1)))
   write (TTYOUT,fmt='(A)')&
      ' which has caused a code malfunction in BIOPR.'
end select Process
End Subroutine BIOPR

subroutine REDPR(IFORM,ION,I1,I2,I3,K,N1,ttyout) ! reduction products
use Floating_Point_Comparisons
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real (kind (0D0)) :: DTEMP
real :: TEMP2, TKEL, KREDL
integer :: II, J, KK
integer :: IFORM,ION,I1,I2,I3,K,N1,ttyout
DTEMP = 0.0D+00 ! initialize on each pathway evaluation
Forms1: select case (RFORMG(N1))
case (1:28) Forms1!-single reactive form
   Segments1: do J = 1, KOUNT
      TKEL = TCELG(J,NDAT)+273.15
      KREDL = KREDG(IFORM,ION,I1)
      if (EREDG(IFORM,ION,I1) .NotEqual. 0.0) KREDL = &
        10.**(KREDG(IFORM,ION,I1)-(EREDG(IFORM,ION,I1)/(R_Factor*TKEL)))
      TEMP2 = YIELDG(N1) ! Compute yield factor
      if (EAYLDG(N1) .NotEqual. 0.0) TEMP2 =&
        10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
      DTEMP = &       ! Add this path to total transformation yield
              TEMP2*KREDL*(MWTG(I2)/MWTG(I1))*REDAGG(J,NDAT)*ALPHA(I3,J,K)
      YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      ! Correction for molecular weights converts input units (Mole
      ! product produced per Mole parent compound reacted) to
      ! weight/weight factor i.e., mg produced per mg reacted.
   end do Segments1
   !
case (29:) Forms1!-multiple reactive forms (e.g., all dissolved forms)
   IFORM = RFORMG(N1)-28
   Segments11: do J = 1, KOUNT
      II = -3
      TKEL = TCELG(J,NDAT)+273.15
      Species1: do ION = 1, 7
         II = II+1
         if (SPFLGG(ION,I1) == 0) cycle Species1 ! skip non-existent species
         KREDL = KREDG(IFORM,ION,I1)
         if (EREDG(IFORM,ION,I1) .NotEqual. 0.0) KREDL =&
           10.**(KREDG(IFORM,ION,I1)-(EREDG(IFORM,ION,I1)/(R_Factor*TKEL)))
         TEMP2 = YIELDG(N1)
         if (EAYLDG(N1) .NotEqual. 0.0) TEMP2=&
           10.**(YIELDG(N1)-(EAYLDG(N1)/(R_Factor*TKEL)))
         KK = 3*ION+II+IFORM-1
         DTEMP = TEMP2*KREDL*(MWTG(I2)/MWTG(I1))*REDAGG(J,NDAT)*ALPHA(KK,J,K)
         YIELDL(I2,I1,J) = YIELDL(I2,I1,J)+DTEMP
      end do Species1
   end do Segments11
case default Forms1 !--fail-safe: bad reactive form slipped through;
                    ! this shouldn't happen, but just in case...
   call Print_Header(TTYOUT,N1,CHEMNA(CHPARG(N1)))
   write (TTYOUT,fmt='(A,I5,A)')&
     ' in that the reactive form (', RFORMG(N1), ') is invalid; entry skipped'
end select Forms1
end subroutine REDPR


subroutine Print_Header(ttyout,path_number,name_of_chemical)
! print the name of the chemical being processed
Implicit None
integer :: ttyout, path_number
character(*) :: name_of_chemical
write (ttyout,fmt='(/A/1X,A/A,I5,A)')&
   ' WARNING: The product chemistry specifications for',&
   trim(name_of_chemical),&
   ' include an invalid entry at pathway',&
   path_number,',' ! the current pathway number
end subroutine Print_Header
