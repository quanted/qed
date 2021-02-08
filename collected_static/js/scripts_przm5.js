$(document).ready(function() {
  // Call function to setup tabbed nav
  uberNavTabs(
      ["Chemical", "Applications", "CropLand", "Runoff", "WaterBody"],
      {   "isSubTabs":true,
          "Chemical":".tab_Chemical0" }
  );

	var USLE_day = [16,1,16,1,16,1,16,1,16,1,10,16,1,16,1,16,1,16,1,16,1,10,16,1,16,1];
	var USLE_mon = [2,3,3,4,4,5,5,6,6,7,7,7,8,8,9,9,10,10,11,11,12,12,12,1,1,2];
	var USLE_c = [0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011];
	var USLE_n = [0.188,0.190,0.191,0.527,0.558,0.569,0.572,0.574,0.575,0.634,0.796,0.750,0.602,0.302,0.176,0.176,0.177,0.178,0.505,0.560,0.634,0.803,0.767,0.632,0.318,0.186];
	var USLE_cn = [89,89,89,89,89,89,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94];

  var i = 0;
  var total = $('#id_nott').val();
  while (i < total) {
          $('.tab_nott').append(
          	'<tr><td><input name="jm_'+i+' " type="text" size="5" value="'+(i+1)+'"/></td><td><input type="text" size="5" name="day_t_'+i+'" id="id_day_t_'+i+'" value="'+USLE_day[i]+'"/></td><td><input type="text" size="5" name="mon_t_'+i+'" id="id_mon_t_'+i+'" value="'+USLE_mon[i]+'"/></td><td><input type="text" size="5" name="cn_t_'+i+'" id="id_cn_t_'+i+'" value="'+USLE_cn[i]+'"/></td><td><input type="text" size="5" name="c_t_'+i+'" id="id_c_t_'+i+'" value="'+USLE_c[i]+'"/></td><td><input type="text" size="5" name="n_t_'+i+'" id="id_n_t_'+i+'" value="'+USLE_n[i]+'"/></td><td class="year_not"><input type="text" size="5" name="year_t_'+i+'" id="id_year_t_'+i+'" value="1972" /></td>');
      i = i + 1;
  }
  $('</table>').appendTo('.tab_nott');
  $(".year_not").hide();

    var i_a = 0;
    var total_a = $('#id_noa').val();
    while (i_a < total_a) {
            $('.tab_noa').append(
              '<tr><td class="rela"><input type="text" size="5" name="rela_a_'+i_a+'" id="id_rela_a_'+i_a+'" value='+i_a+'></td><td class="abs"><input type="text" size="5" name="day_a_'+i_a+'" id="id_day_a_'+i_a+'" value="1"/></td><td class="abs"><input type="text" size="5" name="mon_a_'+i_a+'" id="id_mon_a_'+i_a+'" value="6" /></td><td><input type="text" size="5" name="rate_a_'+i_a+'" id="id_rate_a_'+i_a+'" value="1.12"/></td><td><select name="cam_a_'+i_a+'" id="id_cam_a_'+i_a+'"><option value="" disabled="disabled">Please select a name</option><option value="1">Ground</option><option value="2" selected="selected">Foliar</option><option value="4">Incorporate</option><option value="8">@Depth</option><option value="7">T-Band</option></select></td><td><input type="text" size="5" name="depth_a_'+i_a+'" id="id_depth_a_'+i_a+'" value="4" readonly="readonly"/></td><td><input type="text" size="5" name="eff_a_'+i_a+'" id="id_eff_a_'+i_a+'" value="0.95"/></td><td><input type="text" size="5" name="drift_a_'+i_a+'" id="id_drift_a_'+i_a+'" value="0.05"/></td>');
        i_a = i_a + 1;
    }
  $('</table>').appendTo('.tab_noa');
    $(".rela").hide();

  var thick_h = [10,22,40,77,22, '', ''];
  var rho_h = [1.575, 1.575, 1.475, 1.725, 1.75, '', ''];
  var max_h = [0.295, 0.295, 0.347, 0.224, 0.214, '', ''];
  var min_h = [0.17, 0.17, 0.242, 0.139, 0.089, '', ''];
  var oc_h = [0.725, 0.725, 0.058, 0.058, 0.058, '', ''];
  var n_h = [100, 11, 8, 77, 11, '', ''];
  var sand_h = [0.10, 0.11, 0.12, 0.13, 0.14, '', ''];
  var clay_h = [0.15, 0.16, 0.17, 0.18, 0.19, '', ''];

  var i_h = 0;
  var total_h = $('#id_noh').val();
  while (i_h < total_h) {
          $('.tab_noh').append(
            '<tr><td><input type="text" size="5" name="thick_h_'+i_h+'" id="id_thick_h_'+i_h+'" value="'+thick_h[i_h]+'"/></td><td><input type="text" size="5" name="rho_h_'+i_h+'" id="id_rho_h_'+i_h+'" value="'+rho_h[i_h]+'"/></td><td><input type="text" size="5" name="max_h_'+i_h+'" id="id_max_h_'+i_h+'" value="'+max_h[i_h]+'"/></td><td><input type="text" size="5" name="min_h_'+i_h+'" id="id_min_h_'+i_h+'" value="'+min_h[i_h]+'"/></td><td><input type="text" size="5" name="oc_h_'+i_h+'" id="id_oc_h_'+i_h+'" value="'+oc_h[i_h]+'"/></td><td><input type="text" size="5" name="n_h_'+i_h+'" id="id_n_h_'+i_h+'" value="'+n_h[i_h]+'"/></td><td class="tempflag"><input type="text" size="5" name="sand_h_'+i_h+'" id="id_sand_h_'+i_h+'" value="'+sand_h[i_h]+'"/></td><td class="tempflag"><input type="text" size="5" name="clay_h_'+i_h+'" id="id_clay_h_'+i_h+'" value="'+clay_h[i_h]+'"/></td>');
      i_h = i_h + 1;
  }
  $('</table>').appendTo('.tab_noh');
  $(".tempflag").hide();

  $('#id_noh').change(function () {
    var total_h = $(this).val();
    while (i_h < total_h) {
            $('.tab_noh').append(
              '<tr><td><input type="text" size="5" name="thick_h_'+i_h+'" id="id_thick_h_'+i_h+'" value="'+thick_h[i_h]+'" /></td><td><input type="text" size="5" name="rho_h_'+i_h+'" id="id_rho_h_'+i_h+'" value="'+rho_h[i_h]+'"/></td><td><input type="text" size="5" name="max_h_'+i_h+'" id="id_max_h_'+i_h+'" value="'+max_h[i_h]+'"/></td><td><input type="text" size="5" name="min_h_'+i_h+'" id="id_min_h_'+i_h+'" value="'+min_h[i_h]+'"/></td><td><input type="text" size="5" name="oc_h_'+i_h+'" id="id_oc_h_'+i_h+'" value="'+oc_h[i_h]+'"/></td><td><input type="text" size="5" name="n_h_'+i_h+'" id="id_n_h_'+i_h+'" value="'+n_h[i_h]+'"/></td><td class="tempflag"><input type="text" size="5" name="sand_h_'+i_h+'" id="id_sand_h_'+i_h+'" value="'+sand_h[i_h]+'"/></td><td class="tempflag"><input type="text" size="5" name="clay_h_'+i_h+'" id="id_clay_h_'+i_h+'" value="'+clay_h[i_h]+'"/></td>');
        i_h = i_h + 1;
    }
    while (i_h > total_h) {
      $(".tab_noh tr:last").remove();
      i_h=i_h-1;
    }
    $('</table>').appendTo('.tab_noh');
    $(".tempflag").hide();
  });

  $('#id_tempflag_check').change(function () {
    if($(this).is(":checked")) {
      $(".tempflag").show();
    }
    else{
      $(".tempflag").hide();
    }
  });

  $('#id_app_date_type').change(function () {
    var app_date_type = $(this).val();
    if (app_date_type == 0)
    {
      $(".rela").hide();
      $(".abs").show();
    }
    else
    {
      $(".rela").show();
      $(".abs").hide();
    }
  });

  $('#id_nott').change(function () {
    var total = $(this).val();
  while (i < total) {
          $('.tab_nott').append(
            '<tr><td><input name="jm_'+i+'" type="text" size="5" value="'+(i+1)+'"/></td><td><input type="text" size="5" name="day_t_'+i+'" id="id_day_t_'+i+'" value="'+USLE_day[i]+'"/></td><td><input type="text" size="5" name="mon_t_'+i+'" id="id_mon_t_'+i+'" value="'+USLE_mon[i]+'"/></td><td><input type="text" size="5" name="cn_t_'+i+'" id="id_cn_t_'+i+'" value="'+USLE_cn[i]+'"/></td><td><input type="text" size="5" name="c_t_'+i+'" id="id_c_t_'+i+'" value="'+USLE_c[i]+'"/></td><td><input type="text" size="5" name="n_t_'+i+'" id="id_n_t_'+i+'" value="'+USLE_n[i]+'"/></td><td class="year_not"><input type="text" size="5" name="year_t_'+i+'" id="id_year_t_'+i+'" value="1972"/></td>');
      i = i + 1;
  }
    while (i > total) {
      $(".tab_nott tr:last").remove();
      i=i-1;
    }
    $('</table>').appendTo('.tab_nott');
    $(".year_not").hide();
  });

  $('#id_sp_year').change(function () {
    if($(this).is(":checked")) {
      $(".year_not").show();
    }
    else{
      $(".year_not").hide();
    }
  });

  // PRZM5 specific changes
  $("#id_pond_res_custom").prop('disabled', true);

  // Save input page html to browser Local Storage to be retrieved on output page
  $("input[value='Submit']").click(function() {
      var html_input = $("form").html();
      localStorage.html_input=html_input;
      var html_new = $("form").serialize();
      localStorage.html_new=html_new;
  });

});