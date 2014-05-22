$(document).ready(function() {
    // Call function to setup tabbed nav
    uberNavTabs(
        ["Chemical", "Avian", "Herptile"],
        {   "isSubTabs":false  }
    );

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