$(document).ready(function() {

    var tab_pool = ["tab_Chemical", "tab_Avian", "tab_Mammal", "tab_LargeFish", "tab_MediumFish", "tab_SmallFish", "tab_Filterfeeders", "tab_Invertebrates", "tab_Zooplankton", "tab_Phytoplankton", "tab_Sediment", "tab_Constants"];
    var uptab_pool = ["Chemical", "Avian", "Mammal", "LargeFish", "MediumFish", "SmallFish", "Filterfeeders", "Invertebrates", "Zooplankton", "Phytoplankton", "Sediment", "Constants"];
    var visible = $(".tab:visible").attr('class').split(" ")[1];
    var curr_ind = $.inArray(visible, tab_pool);
    $(".submit").hide();
    $(".back").hide();

    $('li.Chemical').click(function(){
        curr_ind = 0;
        $('li.Chemical').addClass('tabSel').removeClass('tabUnsel');
        $('li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Chemical').show();
        $(".back").hide();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Avian').click(function(){
        curr_ind = 1;
        $('li.Avian').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Avian').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Mammal').click(function(){
        curr_ind = 2;
        $('li.Mammal').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Mammal').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.LargeFish').click(function(){
        curr_ind = 3;
        $('li.LargeFish').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_LargeFish').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.MediumFish').click(function(){
        curr_ind = 4;
        $('li.MediumFish').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_MediumFish').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.SmallFish').click(function(){
        curr_ind = 5;
        $('li.SmallFish').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_SmallFish').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Filterfeeders').click(function(){
        curr_ind = 6;
        $('li.Filterfeeders').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Filterfeeders').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Invertebrates').click(function(){
        curr_ind = 7;
        $('li.Invertebrates').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Zooplankton, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Invertebrates').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Zooplankton').click(function(){
        curr_ind = 8;
        $('li.Zooplankton').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Phytoplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Zooplankton').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Phytoplankton').click(function(){
        curr_ind = 9;
        $('li.Phytoplankton').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Sediment, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Phytoplankton').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Sediment').click(function(){
        curr_ind = 10;
        $('li.Sediment').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Constants').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Sediment').show();
        $(".back").show();
        $(".submit").hide();
        $(".next").show();
    });

    $('li.Constants').click(function(){
        curr_ind = 11;
        $('li.Constants').addClass('tabSel').removeClass('tabUnsel');
        $('li.Chemical, li.Avian, li.Mammal, li.LargeFish, li.MediumFish, li.SmallFish, li.Filterfeeders, li.Invertebrates, li.Zooplankton, li.Phytoplankton, li.Sediment').addClass('tabUnsel').removeClass('tabSel');
        $(".tab:visible").hide();
        $('.tab_Constants').show();
        $(".back").show();
        $(".submit").show();
        $(".next").hide();
    });

    $('.next').click(function () {
        var tab = $(".tab:visible");
        
        if (curr_ind < 11) {      
            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
            curr_ind = curr_ind + 1;
            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
            $(".submit").hide();
            $(".back").show();
            }
        
        if (curr_ind == 11) {
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

    $('#id_phyto_k1').closest('tr').addClass('method_options').hide();
    $('#id_phyto_k2').closest('tr').addClass('method_options').hide();
    $('#id_phyto_kd').closest('tr').addClass('method_options').hide();
    $('#id_phyto_ke').closest('tr').addClass('method_options').hide();
    $('#id_phyto_km').closest('tr').addClass('method_options').hide();
    $('#id_zoo_k1').closest('tr').addClass('method_options').hide();
    $('#id_zoo_k2').closest('tr').addClass('method_options').hide();
    $('#id_zoo_kd').closest('tr').addClass('method_options').hide();
    $('#id_zoo_ke').closest('tr').addClass('method_options').hide();
    $('#id_zoo_km').closest('tr').addClass('method_options').hide();
    $('#id_beninv_k1').closest('tr').addClass('method_options').hide();
    $('#id_beninv_k2').closest('tr').addClass('method_options').hide();
    $('#id_beninv_kd').closest('tr').addClass('method_options').hide();
    $('#id_beninv_ke').closest('tr').addClass('method_options').hide();
    $('#id_beninv_km').closest('tr').addClass('method_options').hide();
    $('#id_ff_k1').closest('tr').addClass('method_options').hide();
    $('#id_ff_k2').closest('tr').addClass('method_options').hide();
    $('#id_ff_kd').closest('tr').addClass('method_options').hide();
    $('#id_ff_ke').closest('tr').addClass('method_options').hide();
    $('#id_ff_km').closest('tr').addClass('method_options').hide();
    $('#id_sfish_k1').closest('tr').addClass('method_options').hide();
    $('#id_sfish_k2').closest('tr').addClass('method_options').hide();
    $('#id_sfish_kd').closest('tr').addClass('method_options').hide();
    $('#id_sfish_ke').closest('tr').addClass('method_options').hide();
    $('#id_sfish_km').closest('tr').addClass('method_options').hide();
    $('#id_mfish_k1').closest('tr').addClass('method_options').hide();
    $('#id_mfish_k2').closest('tr').addClass('method_options').hide();
    $('#id_mfish_kd').closest('tr').addClass('method_options').hide();
    $('#id_mfish_ke').closest('tr').addClass('method_options').hide();
    $('#id_mfish_km').closest('tr').addClass('method_options').hide();
    $('#id_lfish_k1').closest('tr').addClass('method_options').hide();
    $('#id_lfish_k2').closest('tr').addClass('method_options').hide();
    $('#id_lfish_kd').closest('tr').addClass('method_options').hide();
    $('#id_lfish_ke').closest('tr').addClass('method_options').hide();
    $('#id_lfish_km').closest('tr').addClass('method_options').hide();
    // $('#id_bw_quail').closest('tr').addClass('method_options2').hide();
    $('#id_bw_duck').closest('tr').addClass('method_options3').hide();
    $('#id_bwb_other').closest('tr').addClass('method_options4').hide();
    // $('#id_bw_rat').closest('tr').hide();
    $('#id_bwm_other').closest('tr').hide();
    
    $('#id_m_species').change(function() {
        if ($(this).val() == "350"){
            $('#id_bw_rat').closest('tr').show();
            $('#id_bwm_other').closest('tr').hide();
        }
        else{
           $('#id_bw_rat').closest('tr').hide();
           $('#id_bwm_other').closest('tr').show();
       }
   });
    $('#id_b_species').change(function() { 
       
        if ($(this).val() == "178"){
            $('#id_bw_quail').closest('tr').show();
            $('#id_bw_duck').closest('tr').hide();
            $('#id_bwb_other').closest('tr').hide();
        }
        else if ($(this).val() == "1580"){
            $('#id_bw_duck').closest('tr').show();
            $('#id_bw_quail').closest('tr').hide();
            $('#id_bwb_other').closest('tr').hide();
        }
        else{
           $('#id_bwb_other').closest('tr').show();
           $('#id_bw_duck').closest('tr').hide();
           $('#id_bw_quail').closest('tr').hide();
       }
   });
    $('#id_rate_c').change(function() { 
       $('tr[class^="method_options"]').hide();  
       if ($(this).val() == "b"){
        $('tr[class^="method_options"]').show();
    }
    else if ($(this).val() == "a"){
        $('tr[class^="method_options"]').hide();
    }    
    });

});