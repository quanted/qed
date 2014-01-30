$(document).ready(function() {

  var tab_pool = ["tab_Chemical", "tab_Applications", "tab_CropLand", "tab_Runoff", "tab_WaterBody"];
  var uptab_pool = ["Chemical", "Applications", "CropLand", "Runoff", "WaterBody"];
  var visible = $(".tab:visible").attr('class').split(" ")[1];
  var curr_ind = $.inArray(visible, tab_pool);
  $(".submit").hide();
  $(".back").hide();

  $('li.Chemical').click(function(){
    var degCheck = $("#id_deg_check").val()
    curr_ind = 0;
    $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
    $('li.Applications, li.CropLand, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
    $(".tab:visible").hide();
    $('.tab_Chemical, .tab_Chemical0').show();
    if (degCheck == '1') {
      $('.tab_Chemical1, .tab_Chemical_MCF1').show();
    }
    if (degCheck == '2') {
      $('.tab_Chemical1, .tab_Chemical_MCF1, .tab_Chemical2, .tab_Chemical_MCF2').show();
    }
    $(".back").hide();
    $(".submit").hide();
    $(".next").show();
  });

  $('li.Applications').click(function(){
    curr_ind = 1;
    $('li.Applications').addClass('tabSel').removeClass('tabUnsel');
    $('li.Chemical, li.CropLand, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
    $(".tab:visible").hide();
    $('.tab_Applications').show();
    $(".back").show();
    $(".submit").hide();
    $(".next").show();
  });

  $('li.CropLand').click(function(){
    curr_ind = 2;
    $('li.CropLand').addClass('tabSel').removeClass('tabUnsel');
    $('li.Applications, li.Chemical, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
    $(".tab:visible").hide();
    $('.tab_CropLand').show();
    $(".back").show();
    $(".submit").hide();
    $(".next").show();
  });

  $('li.Runoff').click(function(){
    curr_ind = 3;
    $('li.Runoff').addClass('tabSel').removeClass('tabUnsel');
    $('li.Applications, li.Chemical, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
    $(".tab:visible").hide();
    $('.tab_Runoff').show();
    $(".back").show();
    $(".submit").hide();
    $(".next").show();
  });

  $('li.WaterBody').click(function(){
    curr_ind = 4;
    $('li.WaterBody').addClass('tabSel').removeClass('tabUnsel');
    $('li.Applications, li.Chemical, li.CropLand, li.Runoff').addClass('tabUnsel').removeClass('tabSel');
    $(".tab:visible").hide();
    $('.tab_WaterBody').show();
    $(".back").show();
    $(".submit").show();
    $(".next").hide();
  });

  $('.next').click(function () {
    var tab = $(".tab:visible");
    if (curr_ind < 4) {      
        $(".tab:visible").hide();
        $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
        curr_ind = curr_ind + 1;
        $("." + tab_pool[curr_ind]).show();
        $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
        $(".submit").hide();
        $(".back").show();
        }
    if (curr_ind == 4) {
        $(".submit").show();
        $(".next").hide();
    }
  });

  $('.back').click(function () {
    if (curr_ind > 0) {
        $(".tab:visible").hide();
        $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
        curr_ind = curr_ind - 1;
        $("." + tab_pool[curr_ind]).show();
        $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
        $(".submit").hide();
        $(".next").show();
    }
    if (curr_ind == 0) {
      $(".back").hide();
      $('.tab_Chemical0').show();
      var degCheck = $("#id_deg_check").val()
      if (degCheck == '1') {
        $('.tab_Chemical1, .tab_Chemical_MCF1').show();
      }
      if (degCheck == '2') {
        $('.tab_Chemical1, .tab_Chemical_MCF1, .tab_Chemical2, .tab_Chemical_MCF2').show();
      }
    }
  });

  // Number of Applications
  var i_a = 0;
  $('#id_noa').change(function () {
    var total_a = $(this).val();
    while (i_a < total_a) {
      $('.tab_Applications').append(
        '<tr><td><input id="id_day_a_'+i_a+'" type="text" name="day_a_'+i_a+'" value="1" size="2" /></td><td><input id="id_mon_a_'+i_a+'" type="text" name="mon_a_'+i_a+'" value="6" size="2" /></td><td><input id="id_year_a_'+i_a+'" type="text" name="year_a_'+i_a+'" size="4" /></td><td><input id="id_rate_a_'+i_a+'" type="text" name="rate_a_'+i_a+'" value="1.12" size="5" /></td><td><select id="id_cam_a_'+i_a+'" name="cam_a_'+i_a+'"><option value="1">Ground</option><option value="2">Foliar</option><option value="4">Incorporate</option><option value="8">@ Depth</option><option value="7">T-Band</option></select></td><td><input id="id_depth_a_'+i_a+'" type="text" name="depth_a_'+i_a+'" value="4" size="5" /></td><td><input id="id_eff_a_'+i_a+'" type="text" name="eff_a_'+i_a+'" value="0.95" size="4" /></td><td><input id="id_drift_a_'+i_a+'" type="text" name="drift_a_'+i_a+'" value="0.05" size="5" /></td></tr>'
      );
    i_a = i_a + 1;
    };
    $("input[id^='id_depth']").prop('readonly', true).css({ 'background-color':'#EBEBE4', 'color':'#EBEBE4' });
    // Specify Years?
    if ($('#id_specifyYears').val() == '0') {
      $("input[id^='id_year']").prop('disabled', true);
    } else {
      $("input[id^='id_year']").prop('disabled', false);
    }
    while (i_a > total_a) {
      $(".tab_Applications tr:last").remove();
      i_a=i_a-1;
    }
  });
  // Specify Years?
  $("#id_specifyYears").change(function() {
    if ($('#id_specifyYears').val() == '0') {
      $("input[id^='id_year']").prop('disabled', true);
    } else {
      $("input[id^='id_year']").prop('disabled', false);
    }
  });
  // Use Depth?
  function useDepth() {
    var app_nChk = $(this);
    var apptypeChk = $(this).val();
    if (apptypeChk == '1') {
      $(app_nChk).parent().next().children().prop('readonly', true).css({ 'background-color':'#EBEBE4', 'color':'#EBEBE4' });
    } else if (apptypeChk == '2') {
      $(app_nChk).parent().next().children().prop('readonly', true).css({ 'background-color':'#EBEBE4', 'color':'#EBEBE4' });
    } else {
      $(app_nChk).parent().next().children().prop('readonly', false).css({ 'background-color':'#FFFFFF', 'color':'#000' }); 
    }
  }
  $("tbody").on("change", "select[id^='id_cam_a']", useDepth );

});