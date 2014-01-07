$(document).ready(function() {

    var tab_pool = ["tab_Chemical", "tab_CropLand", "tab_WaterBody"];
    var uptab_pool = ["Chemical", "CropLand", "WaterBody"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        $('li.CropLand, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Chemical').show();
        $(".back").hide();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.CropLand').click(function(){
        curr_ind = 1;
        $('li.CropLand').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.WaterBody').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_CropLand').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.WaterBody').click(function(){
        curr_ind = 2;
        $('li.WaterBody').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.CropLand').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_WaterBody').show();
        $(".back").show();
        $(".submit").show();
        $(".next").hide();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        if (curr_ind < 2) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
            $(".submit").hide();
            $(".back").show();
            }
        if (curr_ind == 2) {
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

});