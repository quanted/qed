$(document).ready(function() {

    var tab_pool = ["tab_chem", "tab_ad", "tab_c1", "tab_c2"];
    var uptab_pool = ["chem", "ad", "c1", "c2"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.chem').click(function(){
        curr_ind = 0;
        $('li.chem').css({'color': '#A31E39'});
        $('li.ad, li.c1, li.c2').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_chem').show();
        $(".back").hide();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.ad').click(function(){
        curr_ind = 1;
        $('li.ad').css({'color': '#A31E39'});
        $('li.chem, li.c1, li.c2').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_ad').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.c1').click(function(){
        curr_ind = 2;
        $('li.c1').css({'color': '#A31E39'});
        $('li.chem, li.ad, li.c2').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_c1').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.c2').click(function(){
        curr_ind = 3;
        $('li.c2').css({'color': '#A31E39'});
        $('li.chem, li.ad, li.c1').css({'color': '#333333'});
        $(".tab:visible").hide();
        $('.tab_c2').show();
        $(".back").show();
        $(".submit").show();
        $(".next").hide();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        if (curr_ind < 3) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            $(".submit").hide();
            $(".back").show();
            }
        if (curr_ind == 3) {
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
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            $(".submit").hide();
            $(".next").show();
        }
        if (curr_ind == 0) {
            $(".back").hide();
        }
    });
});