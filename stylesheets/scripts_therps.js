$(document).ready(function() {

    var tab_pool = ["tab_Chemical", "tab_Avian", "tab_Herptile"];
    var uptab_pool = ["Chemical", "Avian", "Herptile"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').css({'color': '#FFA500'});
        $('li.Avian, li.Herptile').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_Chemical').show();
        $(".back").hide();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Avian').click(function(){
        curr_ind = 1;
        $('li.Avian').css({'color': '#FFA500'});
        $('li.Chemical, li.Herptile').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_Avian').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Herptile').click(function(){
        curr_ind = 2;
        $('li.Herptile').css({'color': '#FFA500'});
        $('li.Avian, li.Chemical').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_Herptile').show();
        $(".back").show();
        $(".submit").show();
        $(".next").hide();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        
        if (curr_ind < 2) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#FFA500'});
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
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind - 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#FFA500'});
            $(".submit").hide();
            $(".next").show();
           
        }
        if (curr_ind == 0) {
            $(".back").hide();
        }
    });

    $('#id_Species_of_the_tested_bird_avian_ld50').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_bw_avian_ld50').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_bw_avian_ld50').val(1580);
        }
        else{
            $('#id_bw_avian_ld50').val(7);
       }
   });

    $('#id_Species_of_the_tested_bird_avian_lc50').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_bw_avian_lc50').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_bw_avian_lc50').val(1580);
        }
        else{
            $('#id_bw_avian_lc50').val(7);
       }
   });

    $('#id_Species_of_the_tested_bird_avian_NOAEC').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_bw_avian_NOAEC').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_bw_avian_NOAEC').val(1580);
        }
        else{
            $('#id_bw_avian_NOAEC').val(7);
       }
   });

    $('#id_Species_of_the_tested_bird_avian_NOAEL').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_bw_avian_NOAEL').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_bw_avian_NOAEL').val(1580);
        }
        else{
            $('#id_bw_avian_NOAEL').val(7);
       }
   });

});
