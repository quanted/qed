subroutine PRCHEM
! PRCHEM records the properties of chemicals (input data) in the output file
! defined by Fortran LUN RPTLUN.
! Created August 1979 by L.A. Burns
! Revised 25-DEC-1985 (LAB)
! Revised 10/20/88 (LAB)--run-time formats for implementation-dependent cursor
! Revised 4/12/90 to improve database print control at print of RFLAT
! Converted to Fortran90 2/20/96 et seq.
! Revised to handle arbitrary (>99) number of chemicals April 2001
! Revised 2004-05-21 to document metabolic study temperatures (QTBTW, QTBTS)
! Revised 2004-06-16 to suppress printing of non-zero Q10 when associated
!   rate constant is zero
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
! Local variables
real :: Q10Dummy(2) ! for conditional suppression of Q10 printing
integer :: I,J,K,EOF,LFIRST,LLAST,I1,I2,ITAB,IMBED
integer, parameter :: Zero = 0
logical :: IONS
! IONS is used to test for the existence of ionic species.
! I, J, and K are loop counters--I for output cycles,
! J for ionic species, and K for compounds.
! LFIRST and LLAST are loop boundaries for the print sequence.
character(len=1), dimension(2) :: CCHAR = (/'1',' '/)
! CCHAR is a control character to improve the response on SHO CHEM
character(len=2), dimension(6) :: IOUT=(/'+1','+2','+3','-1','-2','-3'/)
integer :: Number_of_Blanks ! used with KOUT_ChemLoop to space outputs
character(len=132) :: PhotoFormat ! run-time format for photolysis table
! IOUT holds table title elements for ions.
character(len=7), dimension(4,4) :: NAME1 = reshape &
   ((/' KAH:  ',' KBH:  ',' KBACW:',' K1O2: ',' EAH:  ',' EBH:  ',' QTBAW:',&
   ' EK1O2:',' KNH:  ',' KRED: ',' KBACS:',' KOX:  ',' ENH:  ',' ERED: ',&
   ' QTBAS:',' EOX:  '/), (/4,4/))
! NAMEs of variables for output records
character(len=78), dimension(4) :: OUTLIN, MSSAGE = (/&
   ' *** Reactivity of dissolved species: SET via "entry(I,J,KK)"',&
   ' *** Reactivity of solids-sorbed species:     "entry(I,J,KK)"',&
   ' *** Reactivity of "DOC"-complexed species:   "entry(I,J,KK)"',&
   ' *** Reactivity of biosorbed species:         "entry(I,J,KK)"'/)
! MSSAGE holds lines of output messages
! OUTLIN is internal file for output processing
! internal file for checking output length requirments for study chemicals
character(len=9) :: KOUT_Chem_Loop

! Set loop boundaries depending on number of chemicals and whether
! PRCHEM has been called by a simulation or a database inspection
if (BATCH == 0) then ! set up for simulation output
   LFIRST = 1
   LLAST = KCHEM
else                 ! interactive database SHOW
   LFIRST = MCHEMG
   LLAST = MCHEMG
endif
Chemicals: do K = LFIRST, LLAST ! loop on multiple chemicals
! instantiate internal file for determining required output width
write (KOUT_Chem_Loop, fmt='(I0)') K
if (SPFLGG(1,K) == 0) SPFLGG(1,K) = 1 ! a neutral molecule must exist
IONS = .false.
do I = 2, 7       ! test for existence of ionic species
   if (SPFLGG(I,K) == 1) then
      IONS = .true.
      exit
   end if
end do
! molecular weight is required for checking loadings, etc.
! If it has not been specified, set error flag and notify user
if (MWTG(K) .LessThanOrEqual. 0.0) then
   IFLAG = 8 ! to force the RUN to abort on return to GHOST
   write (stderr,fmt='(A,I2,A,1PG8.1/1X,A/A)')&
   ' Molecular weight of Chemical in ADB #',K,' = ',MWTG(K),trim(CHEMNA(K)),&
   ' Molecular weight must be specified to RUN an analysis.'
end if
Ionic_species: do J = 1, 7    ! begin loop on chemical species
if (SPFLGG(J,K) /= 1) cycle Ionic_species
Ask_user: if (BATCH /= 0 .and. IONS) then
   write (stdout,fmt='(/A)',advance='NO')&
      ' Do you want to inspect the input data for'
   if (J == 1) then
      write (stdout,fmt='(A,I0,A)')&
         ' the neutral species (SPFLG(1,',MCHEMG,'))?'
   else
      write (stdout,fmt='(A,I1,A,I0,A)') &
         ' the '//IOUT(J-1)//' ion (SPFLG(',J,',',MCHEMG,'))?'
   endif
   Query: do
      write (stdout,fmt='(A)',advance='NO')&
         ' Please enter Yes, No, or Quit-> '
      call INREC (EOF,stdin)
      if (EOF == 1) exit Chemicals
      START = IMBED(INPUT,Zero)
      if(START == -999) exit Query  ! treat null input as yes...
      if(INPUT(START:START)=='Q'.or.INPUT(START:START)=='q') exit Chemicals
      if(INPUT(START:START)=='Y'.or.INPUT(START:START)=='y') exit Query
      if(INPUT(START:START)=='N'.or.INPUT(START:START)=='n')cycle Ionic_species
      write (stdout,fmt='(A)') ' Response not understood.'
   end do Query
end if Ask_user
! Page header--name of chemical and ecosystem
write (RPTLUN,5060) CCHAR(BATCH+1),VERSN,MODEG,K,trim(CHEMNA(K))
write (RPTLUN,5070)
Neutral: if (J == 1) then  ! Print data specific to neutral molecule
                           ! =======================================
   write (RPTLUN,5080) K
   5080 format &
   (' Table 1.',I0,'.1  Chemical input data for',' neutral molecule (Sp.#1).')
   write (RPTLUN,fmt='(A,I0,A)') &
      ' *** Chemical-specific data: SET via "entry(',K,')"'
   write (OUTLIN(1),5100) MWTG(K),VAPRG(K),HENRYG(K),KOWG(K)
   5100 format(' MWT:  ',1PE9.2,' VAPR: ',E9.2,' HENRY:',E9.2,' KOW:  ', E9.2)
   write (OUTLIN(2),5110) MPG(K),EVPRG(K),EHENG(K),KOCG(K)
   5110 format(' MP:   ',1PE9.2,' EVPR: ',E9.2,' EHEN: ',E9.2,' KOC:  ',E9.2)
   write (OUTLIN(3),5120) SOLG(1,K),KPBG(1,K),KPSG(1,K)
   5120 format(' SOL:  ',1PE9.2,' KPB:  ',E9.2,' KPS:  ',E9.2,:,' pK?:  ',E9.2)
   write (OUTLIN(4),5130) ESOLG(1,K),KPDOCG(1,K)
   5130 format(' ESOL: ',1PE9.2,' KPDOC:',E9.2,:,' KIEC: ',E9.2,' EpK:  ',E9.2)
   do I1 = 1, 4
      do I = 9, 57, 16
         if (OUTLIN(I1)(I:I) == '0') OUTLIN(I1)(I-1:I+7) = '         '
         if (OUTLIN(I1)(I+4:I+7) == 'E+00') OUTLIN(I1)(I+4:I+7) = '    '
      end do
   end do
   OUTLIN(3)(49:64) = ' '
   OUTLIN(4)(33:64) = ' '
   do I=1,2
      write (RPTLUN,fmt='(A)') trim(OUTLIN(I))
   end do
   write (OUTLIN(1), fmt="(' AerMet (half-life, days): ',1pE9.2,&
                          &' AnaerM (half-life, days): ',E9.2)") &
                             AerMet(K),AnaerM(K)
   do I2 = 29, 65, 36 ! blank out missing values
      if (OUTLIN(1)(I2:I2) == '0') OUTLIN(1)(I2-1:I2+7)= '         '
      if (OUTLIN(1)(I2+4:I2+7) == 'E+00') OUTLIN(1)(I2+4:I2+7) = '    '
   end do
   write (RPTLUN,fmt='(A)') trim(OUTLIN(1))
   write (RPTLUN,5150) J,K
   do I=3,4
     write (RPTLUN,fmt='(A)') trim(OUTLIN(I))
   end do
else Neutral ! Print data specific to ions
             ! ===========================
   write (RPTLUN,5160) K,J,IOUT(J-1),J
   5160  format (' Table 1.',I0,'.',I1,'.  Chemical input data for ',A2,&
      ' ion (Species #',I1,').')
   write (RPTLUN,5150) J,K,J-1,K
   write (OUTLIN(1),5120) SOLG(J,K),KPBG(J,K),KPSG(J,K),PKG(J-1,K)
   write (OUTLIN(2),5130) ESOLG(J,K),KPDOCG(J,K),KIECG(J-1,K),EPKG(J-1,K)
   do I1 = 1, 2
      do I = 9, 57, 16
         if (OUTLIN(I1)(I:I) == '0') OUTLIN(I1)(I-1:I+7) = '         '
         if (OUTLIN(I1)(I+4:I+7) == 'E+00') OUTLIN(I1)(I+4:I+7) = '    '
      end do
   end do
   OUTLIN(1)(52:52) = 'b'
   if (J > 4) OUTLIN(1)(52:52) = 'a'
   write (RPTLUN,fmt='(A/A)') trim(OUTLIN(1)),trim(OUTLIN(2))
end if Neutral

! Print data common to all species
! ================================
do I = 1, 4
   write (MSSAGE(I)(54:),5170) I,J,K
   write (RPTLUN,fmt='(A)') trim(MSSAGE(I))
   if (I < 4) then
      write (OUTLIN(1),5190) NAME1(1,1),KAHG(I,J,K),NAME1(1,2),&
      EAHG(I,J,K),NAME1(1,3),KNHG(I,J,K),NAME1(1,4),ENHG(I,J,K)
      write (OUTLIN(2),5190) NAME1(2,1),KBHG(I,J,K),NAME1(2,2),&
      EBHG(I,J,K),NAME1(2,3),KREDG(I,J,K),NAME1(2,4),EREDG(I,J,K)
   end if
   ! dummy variable to suppress printing of non-zero Q10 when the asociated
   ! rate constant is zero
   if (KBACWG(I,J,K) .EQ. 0.0) then
      Q10Dummy(1)=0.0
   else
      Q10Dummy(1) = QTBAWG(I,J,K)
   end if
   if (KBACSG(I,J,K) .eq. 0.0) then
      Q10Dummy(2)=0.0
   else
      Q10Dummy(2)=QTBASG(I,J,K)
   end if
   write (OUTLIN(3),5190) NAME1(3,1),KBACWG(I,J,K),NAME1(3,2),Q10Dummy(1),&
      NAME1(3,3),KBACSG(I,J,K),NAME1(3,4),Q10Dummy(2)
   do I1 = 1, 3
      do I2 = 9, 57, 16
         if (OUTLIN(I1)(I2:I2) == '0') OUTLIN(I1)(I2-1:I2+7)= '         '
         if (OUTLIN(I1)(I2+4:I2+7) == 'E+00') OUTLIN(I1)(I2+4:I2+7) = '    '
      end do
   end do
   if (I < 4) then
      do I2=1,3
         write (RPTLUN,fmt='(A)') trim(OUTLIN(I2))
      end do
      write(RPTLUN,fmt='(A,F5.1,20X,A,F5.1)')&
           ' QTBTW:',QTBTWG(I,J,K), ' QTBTS:',QTBTSG(I,J,K)
   else
      write (RPTLUN,fmt='(A)') trim(OUTLIN(3))
      write(RPTLUN,fmt='(A,F5.1,20X,A,F5.1)')&
           ' QTBTW:',QTBTWG(I,J,K), ' QTBTS:',QTBTSG(I,J,K)
   endif
end do

Interactive: if (BATCH /= 0) then
   write (stdout,fmt='(/A)')&
      ' Do you want to inspect the photolytic process data?'
   Photolysis_query: do
      write (stdout,fmt='(A)',advance='NO')&
         ' Please enter Yes, No, or Quit-> '
      call INREC (EOF,stdin)
      if (EOF == 1) exit Chemicals
      START = IMBED(INPUT,Zero)
      if(START == -999) exit Photolysis_query ! treat null input as yes
      if(INPUT(START:START)=='Q'.or.INPUT(START:START)=='q')&
         exit Chemicals
      if(INPUT(START:START)=='Y'.or.INPUT(START:START)=='y')&
         exit Photolysis_query
      if(INPUT(START:START)=='N'.or.INPUT(START:START)=='n')&
         cycle Ionic_species
      write (stdout,fmt='(/A)')&
         ' Response not understood; please try again.'
   end do Photolysis_query
   ! Page header--name of chemical and ecosystem
   write (RPTLUN,5060) CCHAR(BATCH+1),VERSN,MODEG,K,trim(CHEMNA(K))
   write (RPTLUN,5070)
   if (J == 1) then
      write (RPTLUN,5080) K
   else
      write (RPTLUN,5160) K,J,IOUT(J-1),J
   endif
end if Interactive
write (RPTLUN,fmt='(/A,I1,A,I0,A)')&
   ' Photochemical process data;  Ion-specific data: "entry(',J,',',K,')"'
write (OUTLIN(1),5220) J,K,KDPG(J,K),J,K,RFLATG(J,K),J,K,LAMAXG(J,K)
5220 format (' KDP(',I1,',',I0,'):',1PE9.2,' RFLAT(',I1,',',I0,'):',&
   0PF6.1,'   ',' LAMAX(',I1,',',I0,'):',F6.1,'   ')
! If KDP is zero, RFLAT and LAMAX are extraneous information and need not
! be printed. In a show command, however, the user may need to see them,
! so printing is only suppressed in the output reports.
if (OUTLIN(1)(13:13) == '0' .and. BATCH == 0) then
   do I = 13, 57, 22
      OUTLIN(1)(I-1:I+7) = '         '
   end do
endif
if (OUTLIN(1)(13:13) == '0') OUTLIN(1)(12:20) = '         '
write (RPTLUN,fmt='(A)') trim(OUTLIN(1))
do I = 1, 3
   write (MSSAGE(I)(54:),5170) I,J,K
   write (RPTLUN,fmt='(A)') trim(MSSAGE(I))
   write (OUTLIN(1),5190) NAME1(4,1),K1O2G(I,J,K),NAME1(4,2),&
      EK1O2G(I,J,K),NAME1(4,3),KOXG(I,J,K),NAME1(4,4),EOXG(I,J,K)
   do I1 = 9, 57, 16
      if (OUTLIN(1)(I1:I1) == '0') OUTLIN(1)(I1-1:I1+7) = '         '
      if (OUTLIN(1)(I1+4:I1+7) == 'E+00') OUTLIN(1)(I1+4:I1+7) = '    '
   end do
   write (RPTLUN,fmt='(A)') trim(OUTLIN(1))
end do
write (OUTLIN(1),5230) (I,J,K,QYield(I,J,K),I=1,3)
       5230 format (3(' QYield(',I1,',',I1,',',I0,')',1PE9.2))

I1 = len_trim(KOUT_Chem_Loop)
! variable I1 is the field size used for the chemical number
do I = 15+I1, 59+3*I1, 22+I1
   if (OUTLIN(1)(I:I) == '0') OUTLIN(1)(I-1:I+7) = '         '
   if (OUTLIN(1)(I+4:I+7) == 'E+00') OUTLIN(1)(I+4:I+7) = '    '
end do
write (RPTLUN,fmt='(A)') trim(OUTLIN(1))

! Calculate datum for first line of photolysis data output
Number_of_Blanks = 9-len_trim(KOUT_Chem_Loop)
! Create run-time format for photolysis table
write(PhotoFormat,fmt='(A,I0,A)') "(' Light ABSORption (n,',I1,',',I0,'):',",&
      Number_of_Blanks,"X,'(1)',1PE10.3,'   (2)',E10.3)"
write (OUTLIN(1),fmt=PhotoFormat) J,K,(ABSORG(I,J,K),I=1,2)
do I = 39, 55, 16
   if (OUTLIN(1)(I:I) == '0') OUTLIN(1)(I-1:I+8) = '          '
end do
write (RPTLUN,fmt='(A)') trim(OUTLIN(1))
do ITAB = 3, 43, 4
   write (OUTLIN(1),5250) (I,ABSORG(I,J,K),I=ITAB,ITAB+3)
   5250 format (' (',I2,')',1PE10.3,3('  (',I2,')',E10.3))
   do I = 7, 55, 16
      if (OUTLIN(1)(I:I) == '0') OUTLIN(1)(I-1:I+8) = '          '
   end do
   do I = 3, 51, 16
      if (OUTLIN(1)(I-1:I) == '( ') OUTLIN(1)(I-1:I) = ' ('
   end do
   write (RPTLUN,fmt='(A)') trim(OUTLIN(1))
end do
end do Ionic_species
end do Chemicals
return
5060 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Chemical: ',I0,') ',A)
5070 format (1X,77('-'))
5150 format (' *** Ion-specific data: "entry(',I1,',',I0,')"',:,&
   ' or, for KIEC & pK, (',I1,',',I0,')')
5170 format (I1,',',I1,',',I0,')')
5190 format (4(A7,1PE9.2))
end subroutine PRCHEM
