Module Step_data  ! File Stepdata.f90
Implicit None
Save
Real (kind (0D0)) :: ALPHA(12), BETA(12), EPS, G(13), X, H, HOLD,&
   SIG(13),V(12),W(12),PSI(12),h_standard
Integer :: KOLD,ICRASH,K,NFE,NS
Logical :: START,PHASE1,NORND
End Module Step_data
