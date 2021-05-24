$(document).ready(function() {
    // Call function to setup tabbed nav
    uberNavTabs(
        ["Chemical", "Avian", "Herptile"],
        {   "isSubTabs":false  }
    );

    $('#id_species_of_the_tested_bird_avian_ld50').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_tw_bird_ld50').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_tw_bird_ld50').val(1580);
        }
        else{
            $('#id_tw_bird_ld50').val(7);
       }
   }).trigger("change");

    $('#id_species_of_the_tested_bird_avian_lc50').change(function() { 
        if ($(this).val() == "Bobwhite quail"){
            $('#id_tw_bird_lc50').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_tw_bird_lc50').val(1580);
        }
        else{
            $('#id_tw_bird_lc50').val(7);
       }
   });

    $('#id_species_of_the_tested_bird_avian_noaec').change(function() {
        if ($(this).val() == "Bobwhite quail"){
            $('#id_tw_bird_noaec').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_tw_bird_noaec').val(1580);
        }
        else{
            $('#id_tw_bird_noaec').val(7);
       }
   });

    $('#id_species_of_the_tested_bird_avian_noael').change(function() {
        if ($(this).val() == "Bobwhite quail"){
            $('#id_tw_bird_noael').val(178);
        }
        else if ($(this).val() == "Mallard duck"){
            $('#id_tw_bird_noael').val(1580);
        }
        else{
            $('#id_tw_bird_noael').val(7);
       }
   });

    $('#main_form').submit(function () {
        $('#main_form :disabled').removeAttr('disabled');
    });

});