$(document).ready(function() {

    var tab_pool = ["tab_Chemical", "tab_Applications", "tab_CropLand", "tab_WaterBody"];
    var uptab_pool = ["Chemical", "Applications", "CropLand", "WaterBody"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        $('li.Applications, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .back, .submit').hide();
        $('.tab_Chemical, .tab_Chemical0, .next').show();
    });

    $('li.Applications').click(function(){
        curr_ind = 1;
        $('li.Applications').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .submit').hide();
        $('.tab_Applications, .back, .next').show();
    });

    $('li.CropLand').click(function(){
        curr_ind = 2;
        $('li.CropLand').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Applications, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .submit').hide();
        $('.tab_CropLand, .back, .next').show();
    });

    $('li.WaterBody').click(function(){
        curr_ind = 3;
        $('li.WaterBody').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Applications, li.CropLand').addClass('tabUnsel').removeClass('tabSel');
        $('.tab:visible, .next').hide();
        $('.tab_WaterBody, .tab_WaterBodyWCparms, .tab_WaterBodyBparms, .back, .submit').show();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        if (curr_ind < 3) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
            $(".submit").hide();
            $(".back").show();
            }
        if (curr_ind == 3) {
            $('.submit, .tab_WaterBodyWCparms, .tab_WaterBodyBparms').show();
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
        }
    });

    // Temporary Fixes
    $('#id_water_body_type_check, #id_app_date_type, #upfile1, #upfile2').prop('disabled', true);
    // 
    $('#id_noa').val('1').prop('disabled', true);
    $('.tab_Applications').append(
        '<tr><td><input id="id_day_a_0" type="text" name="day_a_0" value="1" size="2" /></td><td><input id="id_mon_a_0" type="text" name="mon_a_0" value="6" size="2" /></td><td><input id="id_year_a_0" type="text" name="year_a_0" size="4" /></td><td><input id="id_rate_a_0" type="text" name="rate_a_0" value="1.12" size="5" /></td><td><select id="id_cam_a_0" name="cam_a_0"><option value="1">Ground</option><option value="2">Foliar</option><option value="4">Incorporate</option><option value="8">@ Depth</option><option value="7">T-Band</option></select></td><td><input id="id_depth_a_0" type="text" name="depth_a_0" value="4" size="5" /></td><td><input id="id_eff_a_0" type="text" name="eff_a_0" value="0.95" size="4" /></td><td><input id="id_drift_a_0" type="text" name="drift_a_0" value="0.05" size="5" /></td></tr>'
    );
    $("input[id^='id_depth']").prop('readonly', true).css({ 'background-color':'#EBEBE4', 'color':'#EBEBE4' });
    $('#id_year_a_0').prop('disabled', true);
    // 

});