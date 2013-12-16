$(document).ready(function() {
  // Only 1 Soil Ref Temp Allowed
  var soilRefTemp = $('#id_soilHalfLife_ref').val();
  $('#id_soilHalfLife_ref_1, #id_soilHalfLife_ref_2').val(soilRefTemp).prop('readonly', true).css({ 'background-color':'#EBEBE4', 'color':'#888' });
  $('#id_soilHalfLife_ref').change(function() {
    soilRefTemp = $('#id_soilHalfLife_ref').val();
    $('#id_soilHalfLife_ref_1, #id_soilHalfLife_ref_2').val(soilRefTemp);
  });
  // Degradates
  $('#id_deg_check').change(function() { 
    if ($("#id_deg_check").val() == '1'){
      $(".tab_Chemical1, .tab_Chemical_MCF1").show();
      $('.tab_Chemical2, .tab_Chemical_MCF2').hide();
    }
    if ($("#id_deg_check").val() == '2'){
      $(".tab_Chemical1, .tab_Chemical_MCF1, .tab_Chemical2, .tab_Chemical_MCF2").show();
    } 
    if ($("#id_deg_check").val() == '0'){
      $(".tab_Chemical1, .tab_Chemical_MCF1, .tab_Chemical2, .tab_Chemical_MCF2").hide();
    }
  });
  // Format Form
  $(".tab_Chemical th, .tab_Chemical0 th, .tab_Chemical1 th, .tab_Chemical2 th, .tab_Chemical_MCF1 th, .tab_Chemical_MCF2 th, .tab_CropLand th, .tab_Runoff th, .tab_WaterBody th").css({width:"53.3%"});
  // Format Form (Application Tab)
  $("label[for='id_water_body_type_check'], label[for='id_fieldSize'], label[for='id_hydlength'], label[for='id_app_date_type'], label[for='id_noa'], label[for='id_specifyYears']").closest('th').attr({colspan:"5"});
  $("input[id='id_water_body_type_check'], input[id='id_fieldSize'], input[id='id_hydlength'], select[id='id_app_date_type'], select[id='id_noa'], select[id='id_specifyYears']").closest('td').attr({colspan:"3"});
  $("select[id='id_specifyYears']").prop('disabled', true);
});