$(document).ready(function () {
    listen_agdrift_events();
    initialize_agdrift_aerial();
});

// $(document).on(function () {
//     //initialize_agdrift_aerial();
// });

function initialize_agdrift_aerial(){
    //setup user interface page; initially 'aerial tier 1 - aquatic' but user selections in
    //subsequent page invocations (e.g., when returning after viewing modeling results page

    $('#id_application_method').trigger("change");
    $('#id_ecosystem_type').trigger("change");
    //ecosystem type conditionally triggers aquatic_body or
    // terrestrial_field type in listen_agdrift_events()
    $('#id_calculation_input').trigger("change");


    // $('#id_boom_height').closest('tr').hide();
    // $('#id_airblast_type').closest('tr').hide();
    // $('#id_drop_size_ground').closest('tr').hide();
//    $('#id_drop_size_aerial').closest('tr').hide();
//    $('#id_aquatic_body_type').closest('tr').hide();
//     $('#id_terrestrial_field_type').closest('tr').hide();
//    $('#id_epa_pond_width').closest('tr').hide();
//    $('#id_epa_pond_depth').closest('tr').hide();
//     $('#id_epa_wetland_width').closest('tr').hide();
//     $('#id_epa_wetland_depth').closest('tr').hide();
//     $('#id_user_pond_width').closest('tr').hide();
//     $('#id_user_pond_depth').closest('tr').hide();
//     $('#id_user_wetland_width').closest('tr').hide();
//     $('#id_user_wetland_depth').closest('tr').hide();
//     $('#id_user_terrestrial_width').closest('tr').hide();
//    $('#id_downwind_distance').closest('tr').hide();
//     $('#id_user_frac_applied').closest('tr').hide();
//     $('#id_user_avg_dep_gha').closest('tr').hide();
//     $('#id_user_avg_dep_mgcm2').closest('tr').hide();
//     $('#id_user_avg_dep_lbac').closest('tr').hide();
//     $('#id_user_avg_conc_ngl').closest('tr').hide();

    // $("#id_assessment_type option[value='Terrestrial Assessment']").prop('disabled',true);
    // $("#id_calculation_input option[value='Fraction']").prop('disabled',true);
    // $("#id_calculation_input option[value*='Initial Average']").prop('disabled',true);
    // $("#id_airblast_type option[value='Normal']").prop('disabled',true);
    // $("#id_airblast_type option[value='Dense']").prop('disabled',true);
    // $("#id_airblast_type option[value='Sparse']").prop('disabled',true);
};

function listen_agdrift_events() {

    $('#id_application_method').change(function () {

        if ($(this).val() == "tier_1_ground") {
            $('#id_drop_size_aerial').closest('tr').hide();
            $('#id_drop_size_ground').closest('tr').show();
            $('#id_boom_height').closest('tr').show();
            $('#id_airblast_type').closest('tr').hide(); //orchard_type
        }
        else if ($(this).val() == "tier_1_aerial") {
            $('#id_boom_height').closest('tr').hide();
            $('#id_drop_size_ground').closest('tr').hide();
            $('#id_airblast_type').closest('tr').hide();
            $('#id_drop_size_aerial').closest('tr').show();
        }
        else if ($(this).val() == "tier_1_airblast") {
            $('#id_drop_size_aerial').closest('tr').hide();
            $('#id_drop_size_ground').closest('tr').hide();
            $('#id_boom_height').closest('tr').hide();
            $('#id_airblast_type').closest('tr').show();
        }
    });
    $('#id_ecosystem_type').change(function () {

        if ($(this).val() == "aquatic_assessment") {
            $('#id_aquatic_body_type').closest('tr').show();
            $('#id_epa_pond_width').closest('tr').show();
            $('#id_epa_pond_depth').closest('tr').show();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
            $('#id_terrestrial_field_type').closest('tr').hide();
            $('#id_user_terrestrial_width').closest('tr').hide();
            // update calculation input combo box choices
            $("#id_calculation_input").children("option[value^=" + "'initial_concentration_ngL'" + "]").show();
            $('#id_aquatic_body_type').trigger("change");
        }
        else {
            if ($(this).val() == "terrestrial_assessment") {
                $('#id_aquatic_body_type').closest('tr').hide();
                $('#id_terrestrial_field_type').closest('tr').show();
                $('#id_epa_pond_width').closest('tr').hide();
                $('#id_epa_pond_depth').closest('tr').hide();
                $('#id_epa_wetland_width').closest('tr').hide();
                $('#id_epa_wetland_depth').closest('tr').hide();
                $('#id_user_pond_width').closest('tr').hide();
                $('#id_user_pond_depth').closest('tr').hide();
                $('#id_user_wetland_width').closest('tr').hide();
                $('#id_user_wetland_depth').closest('tr').hide();
                $('#id_user_terrestrial_width').closest('tr').hide();
                // update calculation input combo box choices
                $("#id_calculation_input").children("option[value^=" + "'initial_concentration_ngL'" + "]").hide();
                //$("#id_calculation_input").children("option[value^=InitialAverageConcentrationnng_L]").hide();
                $('#id_terrestrial_field_type').trigger("change");
            }
        }
    });
    $('#id_aquatic_body_type').change(function () {

        if ($(this).val() == "epa_defined_pond") {
            $('#id_epa_pond_width').closest('tr').show();
            $('#id_epa_pond_depth').closest('tr').show();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
            $('#id_user_terrestrial_width').closest('tr').hide();
        }
        else if ($(this).val() == "epa_defined_wetland") {
            $('#id_epa_pond_width').closest('tr').hide();
            $('#id_epa_pond_depth').closest('tr').hide();
            $('#id_epa_wetland_width').closest('tr').show();
            $('#id_epa_wetland_depth').closest('tr').show();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
            $('#id_user_terrestrial_width').closest('tr').hide();
        }
        else if ($(this).val() == "user_defined_pond") {
            $('#id_epa_pond_width').closest('tr').hide();
            $('#id_epa_pond_depth').closest('tr').hide();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').show();
            $('#id_user_pond_depth').closest('tr').show();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
            $('#id_user_terrestrial_width').closest('tr').hide();
        }
        else if ($(this).val() == "user_defined_wetland") {
            $('#id_epa_pond_width').closest('tr').hide();
            $('#id_epa_pond_depth').closest('tr').hide();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').show();
            $('#id_user_wetland_depth').closest('tr').show();
            $('#id_user_terrestrial_width').closest('tr').hide();
        }
    });
    $('#id_terrestrial_field_type').change(function () {

        if ($(this).val() == "epa_defined_terrestrial") {
            $('#id_user_terrestrial_width').closest('tr').hide();
            $('#id_epa_pond_width').closest('tr').hide();
            $('#id_epa_pond_depth').closest('tr').hide();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
        }
        else if ($(this).val() == "user_defined_terrestrial") {
            $('#id_user_terrestrial_width').closest('tr').show();
            $('#id_epa_pond_width').closest('tr').hide();
            $('#id_epa_pond_depth').closest('tr').hide();
            $('#id_epa_wetland_width').closest('tr').hide();
            $('#id_epa_wetland_depth').closest('tr').hide();
            $('#id_user_pond_width').closest('tr').hide();
            $('#id_user_pond_depth').closest('tr').hide();
            $('#id_user_wetland_width').closest('tr').hide();
            $('#id_user_wetland_depth').closest('tr').hide();
        }
    });
    $('#id_calculation_input').change(function () {
        if ($(this).val() == "distance_to_point_or_area_ft") {
            $('#id_downwind_distance').closest('tr').show();
            $('#id_user_frac_applied').closest('tr').hide();
            $('#id_user_avg_dep_gha').closest('tr').hide();
            $('#id_user_avg_dep_lbac').closest('tr').hide();
            $('#id_user_avg_conc_ngl').closest('tr').hide();
            $('#id_user_avg_dep_mgcm2').closest('tr').hide();
           }
        else if ($(this).val() == "fraction_of_applied") {
            $('#id_downwind_distance').closest('tr').hide();
            $('#id_user_frac_applied').closest('tr').show();
            $('#id_user_avg_dep_gha').closest('tr').hide();
            $('#id_user_avg_dep_mgcm2').closest('tr').hide();
            $('#id_user_avg_dep_lbac').closest('tr').hide();
            $('#id_user_avg_conc_ngl').closest('tr').hide();
        }
        else if ($(this).val() == "initial_deposition_gha") {
            $('#id_downwind_distance').closest('tr').hide();
            $('#id_user_frac_applied').closest('tr').hide();
            $('#id_user_avg_dep_gha').closest('tr').show();
            $('#id_user_avg_dep_mgcm2').closest('tr').hide();
            $('#id_user_avg_dep_lbac').closest('tr').hide();
            $('#id_user_avg_conc_ngl').closest('tr').hide();
        }
        else if ($(this).val() == "initial_deposition_lbac") {
            $('#id_downwind_distance').closest('tr').hide();
            $('#id_user_frac_applied').closest('tr').hide();
            $('#id_user_avg_dep_gha').closest('tr').hide();
            $('#id_user_avg_dep_mgcm2').closest('tr').hide();
            $('#id_user_avg_dep_lbac').closest('tr').show();
            $('#id_user_avg_conc_ngl').closest('tr').hide();
        }
        else if ($(this).val() == "initial_concentration_ngL") {
            $('#id_downwind_distance').closest('tr').hide();
            $('#id_user_frac_applied').closest('tr').hide();
            $('#id_user_avg_dep_gha').closest('tr').hide();
            $('#id_user_avg_dep_mgcm2').closest('tr').hide();
            $('#id_user_avg_dep_lbac').closest('tr').hide();
            $('#id_user_avg_conc_ngl').closest('tr').show();
        }
        else if ($(this).val() == "initial_deposition_mgcm2") {
            $('#id_downwind_distance').closest('tr').hide();
            $('#id_user_frac_applied').closest('tr').hide();
            $('#id_user_avg_dep_gha').closest('tr').hide();
            $('#id_user_avg_dep_mgcm2').closest('tr').show();
            $('#id_user_avg_dep_lbac').closest('tr').hide();
            $('#id_user_avg_conc_ngl').closest('tr').hide();
        }
    });
    $(window).bind('beforeunload', function () {
        $(":reset").click();
    });
}