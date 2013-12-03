$(document).ready(function() {

    var tab_pool = ["tab_Chemical", "tab_Applications", "tab_CropLand", "tab_Runoff", "tab_WaterBody"];
    var uptab_pool = ["Chemical", "Applications", "CropLand", "Runoff", "WaterBody"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        $('li.Applications, li.CropLand, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Chemical, .tab_Chemical0').show();
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
        $(".submit").show();
        $(".next").hide();
    });

    $('li.Runoff').click(function(){
        curr_ind = 3;
        $('li.Runoff').addClass('tabSel').removeClass('tabUnsel');
        $('li.Applications, li.Chemical, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Runoff').show();
        $(".back").show();
        $(".submit").show();
        $(".next").hide();
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
        }
    });

  $("label[for='id_n_chem_1']").hide();
  
  var soilRefTemp = $('#id_s_ref').val();
  $('#id_s_ref_1, #id_s_ref_2').val(soilRefTemp).prop('disabled', true);
  $('#id_s_ref').change(function() {
    soilRefTemp = $('#id_s_ref').val();
    $('#id_s_ref_1, #id_s_ref_2').val(soilRefTemp);
  });

  $('#id_n_chem_0, #id_n_chem_1').change(function() { 
    if ($("input#id_n_chem_0").is(':checked')){
      $("label[for='id_n_chem_1'], .tab_Chemical1, .tab_MCF1").show();
    } else {
      $("input#id_n_chem_1").prop('checked', false);
      $("label[for='id_n_chem_1'], .tab_Chemical1, .tab_MCF1").hide();
    }
    if ($("input#id_n_chem_1").is(':checked')){
      $('.tab_Chemical2, .tab_MCF2').show();
    } else {
      $('.tab_Chemical2, .tab_MCF2').hide();
    }
  });

  $("label[for='id_dates'], label[for='id_app_n'], label[for='id_specifyYears_0']").closest('th').attr({colspan:"5"});
  $("select[id='id_dates'], select[id='id_app_n'], label[for='id_specifyYears_0']").closest('td').attr({colspan:"3"});
  $("label[for='id_specifyYears_0']").closest('ul').find("li").attr({display:"inline"});

  var i_a = 0;
  $('#id_app_n').change(function () {
    if ($('#id_specifyYears_1').checked) {
      // $("input[id^='id_year']").prop('disabled', true);
      alert('No is checked');
    }
    else if ($("#id_specifyYears_1").prop( "checked" )) {
      // $("input[id^='id_year']").prop('disabled', true);
      alert('No is checked');
    }
    else if ($("#id_specifyYears_1").is( ":checked" )) {
      // $("input[id^='id_year']").prop('disabled', true);
      alert('No is checked');
    } else {
      alert('Yes is checked');
    }
    var total_a = $(this).val();
    while (i_a < total_a) {
      var i = i_a + 1;
      $('.tab_Applications').append(
        '<tr><td><input id="id_day_'+i+'" type="text" name="day_'+i+'" value="1" size="2" /></td><td><input id="id_month_'+i+'" type="text" name="month_'+i+'" value="1" size="2" /></td><td><input id="id_year_'+i+'" type="text" name="year_'+i+'" value="1" size="4" /></td><td><input id="id_app_'+i+'" type="text" name="app_'+i+'" value="1" size="5" /></td><td><select id="id_apptype_'+i+'"><option value="1">Ground</option><option value="2">Foliar</option><option value="3">Incorporate</option><option value="4">@ Depth</option><option value="5">T-Band</option></select></td><td><input id="id_depth_'+i+'" type="text" name="depth_'+i+'" size="5" /></td><td><input id="id_eff_'+i+'" type="text" name="eff_'+i+'" value="1" size="4" /></td><td><input id="id_driftT_'+i+'" type="text" name="driftT_'+i+'" value="1" size="5" /></td></tr>'
      );
    i_a = i_a + 1;
    };
    $("input[id^='id_depth']").prop('disabled', true);
    // Specify Years?
    while (i_a > total_a) {
      $(".tab_Applications tr:last").remove();
      i_a=i_a-1;
    }
  });

  function useDepth() {
    var app_nChk = $(this);
    var apptypeChk = $(this).val();
    if (apptypeChk == '1') {
      $(app_nChk).parent().next().children().prop('disabled', true);
    } else if (apptypeChk == '2') {
      $(app_nChk).parent().next().children().prop('disabled', true);
    } else {
      $(app_nChk).parent().next().children().prop('disabled', false); 
    }
  }

  $("tbody").on("change", "select[id^='id_apptype']", useDepth );

});
   //  $('#id_avian_NOAEL').val($('#id_avian_NOAEC').val()/20);
   //  $('#id_avian_NOAEC').change(function() { 
   //      $('#id_avian_NOAEL').val($(this).val()/20);
   //  })

   //  $('#id_mammalian_NOAEL').val($('#id_mammalian_NOAEC').val()/20);
   //  $('#id_mammalian_NOAEC').change(function() { 
   //      $('#id_mammalian_NOAEL').val($(this).val()/20);
   //  });
   //  $('#id_seed_treatment_formulation_name').closest('tr').hide();
   //  $('#id_maximum_seedling_rate_per_use').closest('tr').hide();
   //  $('#id_seed_crop').closest('tr').hide();
   //  $('#id_bandwidth').closest('tr').hide();
   //  $('#id_row_sp').closest('tr').hide();
   //  $('#id_density_of_product').closest('tr').hide();

   //  $('#id_Application_type').change(function() { 
   //      if ($(this).val() == 'Seed Treatment'){
   //          $('#id_seed_treatment_formulation_name').closest('tr').show(); 
   //          $('#id_maximum_seedling_rate_per_use').closest('tr').show();
   //          $('#id_density_of_product').closest('tr').show();
   //          $('#id_seed_crop').closest('tr').show();
   //          $('#id_bandwidth').closest('tr').hide();
   //          $('#id_row_sp').closest('tr').hide();
   //          $('#id_Foliar_dissipation_half_life').closest('tr').hide();
   //          $('#id_percent_incorporated').closest('tr').hide();
   //          $('.tab_Application').show()
   //          $('#rate_head').text('Rate (fl oz/cwt)')
   //          $('#id_noa').val(1)
   //          $("#id_noa").prop("disabled", true);
   //          while (i-1 > 1) {
   //              $(".tab_Application tr:last").remove();
   //              i=i-1
   //          }

   //          $('#id_maximum_seedling_rate_per_use').val($('#id_seed_crop').val())
   //          $('#id_seed_crop_v').val($('#id_seed_crop :selected').text())

   //          $('#id_seed_crop').change(function () {
   //              $('#id_maximum_seedling_rate_per_use').val($(this).val())
   //              $('#id_seed_crop_v').val($('#id_seed_crop :selected').text())
   //          })
   //      }
   //      else if ($(this).val() == 'Row/Band/In-furrow-Granular'){
   //          $('.tab_Application').show()
   //          $('#rate_head').text('Rate (lb ai/acre)')
   //          $("#id_noa").prop("disabled", false);
   //          $('.seed').remove()
   //          $('#id_seed_treatment_formulation_name').closest('tr').hide(); 
   //          $('#id_maximum_seedling_rate_per_use').closest('tr').hide();
   //          $('#id_density_of_product').closest('tr').hide();
   //          $('#id_seed_crop').closest('tr').hide();
   //          $('#id_Foliar_dissipation_half_life').closest('tr').show();
   //          $('#id_percent_incorporated').closest('tr').show();
   //          $('#id_bandwidth').closest('tr').show();
   //          $('#id_row_sp').closest('tr').show();
   //      }
   //       else if ($(this).val() == 'Row/Band/In-furrow-Liquid'){
   //          $('.tab_Application').show()
   //          $('#rate_head').text('Rate (lb ai/acre)')
   //          $("#id_noa").prop("disabled", false);
   //          $('.seed').remove()
   //          $('#id_seed_treatment_formulation_name').closest('tr').hide(); 
   //          $('#id_maximum_seedling_rate_per_use').closest('tr').hide();
   //          $('#id_density_of_product').closest('tr').hide();
   //          $('#id_seed_crop').closest('tr').hide();
   //          $('#id_Foliar_dissipation_half_life').closest('tr').show();
   //          $('#id_percent_incorporated').closest('tr').show();
   //          $('#id_bandwidth').closest('tr').show();
   //          $('#id_row_sp').closest('tr').show();
   //      }
   //      else{
   //          $('.tab_Application').show()
   //          $('#rate_head').text('Rate (lb ai/acre)')
   //          $("#id_noa").prop("disabled", false);
   //          $('.seed').remove()
   //          $('#id_seed_treatment_formulation_name').closest('tr').hide(); 
   //          $('#id_maximum_seedling_rate_per_use').closest('tr').hide();
   //          $('#id_density_of_product').closest('tr').hide();
   //          $('#id_seed_crop').closest('tr').hide();
   //          $('#id_bandwidth').closest('tr').hide();
   //          $('#id_Foliar_dissipation_half_life').closest('tr').show();
   //          $('#id_percent_incorporated').closest('tr').show();
   //          $('#id_row_sp').closest('tr').hide();
   //     }
   //  });    

   //  var i = 2

   //      var total = $('#id_noa').val()
   //      $('tr[id*="noa_header"]').show()

   //      while (i <= total) {
   //          if (i==1){
   //              $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day' + i + '"  value="0" /></td></tr>');
   //          }

   //          else {
   //              $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day' + i + '" value="' + 3*(i-1) + '"/></td></tr>');
   //          }
   //          i = i + 1;
   //      }
   //      while (i-1 > total) {
   //          $(".tab_Application tr:last").remove();
   //          i=i-1
   //      }
   //      $('</table>').appendTo('.tab_Application');


   //  $('#id_noa').change(function () {
   //  	var total = $(this).val()
   //  	$('tr[id*="noa_header"]').show()

   //  	while (i <= total) {
   //  		if (i==1){
   //  			$('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day' + i + '"  value="0" /></td></tr>');
   //  		}

   //  		else {
   //  			$('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day' + i + '" value="' + 3*(i-1) + '"/></td></tr>');
   //  		}
   //  		i = i + 1;
   //  	}
   //  	while (i-1 > total) {
   //  		$(".tab_Application tr:last").remove();
   //  		i=i-1
   //  	}
   //  	$('</table>').appendTo('.tab_Application');
   //  })

   //  $('#id_Species_of_the_tested_bird_avian_ld50').change(function() { 
   //      if ($(this).val() == "Bobwhite quail"){
   //          $('#id_bw_avian_ld50').val(178);
   //      }
   //      else if ($(this).val() == "Mallard duck"){
   //          $('#id_bw_avian_ld50').val(1580);
   //      }
   //      else{
   //          $('#id_bw_avian_ld50').val(7);
   //     }
   // });

   //  $('#id_Species_of_the_tested_bird_avian_lc50').change(function() { 
   //      if ($(this).val() == "Bobwhite quail"){
   //          $('#id_bw_avian_lc50').val(178);
   //      }
   //      else if ($(this).val() == "Mallard duck"){
   //          $('#id_bw_avian_lc50').val(1580);
   //      }
   //      else{
   //          $('#id_bw_avian_lc50').val(7);
   //     }
   // });

   //  $('#id_Species_of_the_tested_bird_avian_NOAEC').change(function() { 
   //      if ($(this).val() == "Bobwhite quail"){
   //          $('#id_bw_avian_NOAEC').val(178);
   //      }
   //      else if ($(this).val() == "Mallard duck"){
   //          $('#id_bw_avian_NOAEC').val(1580);
   //      }
   //      else{
   //          $('#id_bw_avian_NOAEC').val(7);
   //     }
   // });

   //  $('#id_Species_of_the_tested_bird_avian_NOAEL').change(function() { 
   //      if ($(this).val() == "Bobwhite quail"){
   //          $('#id_bw_avian_NOAEL').val(178);
   //      }
   //      else if ($(this).val() == "Mallard duck"){
   //          $('#id_bw_avian_NOAEL').val(1580);
   //      }
   //      else{
   //          $('#id_bw_avian_NOAEL').val(7);
   //     }
   // });

// });
