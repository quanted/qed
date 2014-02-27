module solute_capacity
!  Written by Dirk F. Young (Virginia, USA).

contains
subroutine solute_holding_capacity (index)
   use variables, ONLY:  area, depth_0, porosity,bulk_density,FROC1,FROC2,SUSED,DOC1,DOC2,PLMAS,BNMAS,benthic_depth, koc
   
    use nonInputVariables, ONLY: num_records,daily_depth,theta,capacity_1,capacity_2,fw1,fw2, v1,v2
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !Calculates the Solute Holding capacity parameter as a vector the size of the simulation 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   
   implicit none

    integer,intent(in) :: index  
    
!   real(8), intent(out),dimension(num_records) :: theta
!   real(8), intent(out),dimension(num_records) :: capacity_1
!   real(8), intent(out)                        :: capacity_2
!   real(8), intent(out),dimension(num_records) :: fw1
!   real(8), intent(out)                        :: fw2

   real(8):: VOL1,VOL2
   real(8):: KOW, KPDOC1,KPDOC2,XKPB

   real(8):: m_sed_1, m_sed_2
   real(8):: m_bio_1, m_bio_2
   real(8):: m_doc_1, m_doc_2

   real(8):: kd_sed_1, kd_sed_2
   real(8):: kd_bio
   real(8):: kd_doc_1, kd_doc_2


   v1   = daily_depth*area
   vol2 = benthic_depth*area !total benthic volume
   

  
!Default EXAMS conditions for partitioning
    KOW = KOC(index)/.35           !DEFAULT EXAMS CONDITION ON Kow  p.35
    KPDOC1= KOW*.074        !DEFAULT RELATION IN EXAMS (LITTORAL)
    KPDOC2 = KOC(index)            !DEFAULT RELATION IN EXAMS (BENTHIC) p.16 of EXAMS 2.98 (or is it Kow*.46 ?)
    XKPB = 0.436*KOW**.907  !DEFAULT RELATION IN EXAMS

!aqueous volumes in each region

    v2 = vol2*porosity  !with EXAMS parameters   v2  = VOL2*BULKD*(1.-100./PCTWA)


! mass in littoral region
    vol1 = depth_0*area              !initial volume corresponding with susspended matter reference
    m_sed_1 = SUSED*VOL1*.001        !SEDIMENT MASS LITTORAL
    m_bio_1 = PLMAS*VOL1*.001        !BIOLOGICAL MASS LITTORAL
    m_doc_1 = DOC1*VOL1*.001         !DOC MASS LITTORAL

! partitioning coefficients of individual media 
    kd_sed_1 = KOC(index)*FROC1*.001       !Kd of sediment in littoral [m3/kg]
    kd_sed_2 = KOC(index)*FROC2*.001       !Kd of sediment in benthic                       
    kd_bio   = XKPB/1000.           !Kd of biological organisms
    kd_doc_1 = KPDOC1/1000.         !Kd of DOC in littoral region
    kd_doc_2 = KPDOC2/1000.        !Kd of DOC in benthic region

! mass in benthic region

    m_sed_2 = bulk_density*VOL2*1000.   ! as defined by EXAMS parameters m_sed_2 = BULKD/PCTWA*VOL2*100000.
    m_bio_2 = BNMAS*AREA*.001
    m_doc_2 = DOC2*v2*.001
    
    


!solute holding capacity in region 1
    capacity_1 = kd_sed_1 * m_sed_1 + kd_bio * m_bio_1 + kd_doc_1 * m_doc_1 + v1



    !solute holding capacity in region 2
    capacity_2 = kd_sed_2 * m_sed_2 + kd_bio * m_bio_2 + kd_doc_2 * m_doc_2 + v2

    fw1=v1/capacity_1
    fw2=v2/capacity_2

    theta = capacity_2/capacity_1
    

end subroutine solute_holding_capacity
end module solute_capacity