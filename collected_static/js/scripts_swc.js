$(document).ready(function() {
  
	var tab_pool = ["tab_Chemical", "tab_Applications", "tab_CropLand", "tab_Runoff", "tab_WaterBody"];
    var uptab_pool = ["Chemical", "Applications", "CropLand", "Runoff", "WaterBody"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".back, .submit, #metaDataToggle, #metaDataText").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        $('li.Applications, li.CropLand, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
        $('.tab_Chemical, .tab_Chemical0, .next').show();
    });

    $('li.Applications').click(function(){
        curr_ind = 1;
        $('li.Applications').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.CropLand, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
        $('.tab_Applications, .back, .next').show();
    });

    $('li.CropLand').click(function(){
        curr_ind = 2;
        $('li.CropLand').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Applications, li.Runoff, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
        $('.tab_CropLand, .back, .next').show();
    });

	$('li.Runoff').click(function(){
        curr_ind = 3;
        $('li.Runoff').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Applications, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
        $('.tab_Runoff, .back, .next').show();
    });    

    $('li.WaterBody').click(function(){
        curr_ind = 4;
        $('li.WaterBody').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Applications, li.CropLand, li.Runoff').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .next').hide();
        $('.tab_WaterBody, .tab_WaterBodyWCparms, .tab_WaterBodyBparms, .back, .submit, #metaDataToggle, #metaDataText').show();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        if (curr_ind < 4) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
            $(".submit, #metaDataToggle, #metaDataText").hide();
            $(".back").show();
            }
        if (curr_ind == 4) {
            $('.submit, .tab_WaterBodyWCparms, .tab_WaterBodyBparms, #metaDataToggle, #metaDataText').show();
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
            $(".submit, #metaDataToggle, #metaDataText").hide();
            $(".next").show();
        }
        if (curr_ind == 0) {
            $(".back, #metaDataToggle, #metaDataText").hide();
            $('.tab_Chemical0').show();
        }
    });


    // Temp Disable SimType selection:
    $('#id_SimTypeFlag').prop('readonly', true);

    // Inital & Maximum Water Body Depth
    $("input[name$='_Custom']").closest('tr').hide();
    $("input[name$='_Pond'], input[name$='_Reservoir']").prop('readonly', true);
    $('#id_SimTypeFlag').change(function() {
        // Simtype selection        
        if ($(this).val() == '0') {
            $("input[name$='_Pond'], input[name$='_Reservoir']").closest('tr').show();
            $("input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '4') {
            $("input[name$='_Reservoir']").closest('tr').show();
            $("input[name$='_Pond'], input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '5') {
            $("input[name$='_Pond']").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Custom']").closest('tr').hide();
        }
        if ($(this).val() == '1' || $(this).val() == '2' || $(this).val() == '3') {
            $("input[name$='_Custom']").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Pond'], #id_resAvgBox_Custom").closest('tr').hide();
        }
        if ($(this).val() == '6') {
            $("input[name$='_Custom'], #id_resAvgBox_Custom").closest('tr').show();
            $("input[name$='_Reservoir'], input[name$='_Pond']").closest('tr').hide();
        }
    });

    // Temporary Fixes
    $('#id_water_body_type_check, #id_app_date_type, #upfile1, #upfile2').prop('disabled', true);
    $('#id_year_a_0').prop('disabled', true);
    $('#id_water_body_type_check').closest('tr').hide();
    // 
    // Save input page html to browser Local Storage to be retrieved on output page
    // $("input[value='Submit']").click(function() {
    //     var html_input = $("form").html();
    //     localStorage.html_input=html_input;
    //     var html_new = $("form").serialize();
    //     localStorage.html_new=html_new;
    // });

});
