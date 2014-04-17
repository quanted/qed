$(document).ready(function() {

    $('#id_der_pod_sor_cm').change(function () {
    if ($('#id_der_pod_sor_cm').val() == "Route-specific") {
        $('#id_der_abs_cm').val(1.0)
        }
    });
// Start Dynamic for Outdoor Aerosol Space Sprays// 
    $('#id_at_g_oa').closest('tr').hide();
    $('#id_at_ml_oa').closest('tr').hide();
    $('#id_den_oa').closest('tr').hide();

    $('#id_lab_oa').change(function () {
        $('#id_at_oz_oa').closest('tr').hide();
        $('#id_at_g_oa').closest('tr').hide();
        $('#id_at_ml_oa').closest('tr').hide();
        $('#id_den_oa').closest('tr').hide();
        
        if ($('#id_lab_oa').val() == "oz") {
            $('#id_at_oz_oa').closest('tr').show();
        } 
        else if ($('#id_lab_oa').val() == "g") {
            $('#id_at_g_oa').closest('tr').show();
        }
        else if ($('#id_lab_oa').val() == "ml") {
            $('#id_at_ml_oa').closest('tr').show();
            $('#id_den_oa').closest('tr').show();
        }
    });
// End Dynamic for Outdoor Aerosol Space Sprays// 

    var curr_ind = 0;
    $(".submit").hide();
    $(".back").hide();
    $('.next').click(function () {
        var tab = $(".tab:visible");
        if (curr_ind < 6) {      
            var tab_pool = ["tab_scenario"];
            var uptab_pool = ["scenario"];
            var vis_list = [".scenario"];
            $('input[name="scenario_cm"]:checked').each(function () {
                selec_temp = $(this).val()
                tab_pool.push(selec_temp);
                uptab_pool.push(selec_temp.slice(4));
                vis_list.push("."+selec_temp.slice(4));
            });

            $('.uutab').hide();
            $(vis_list.join(', ')).show();

            $(".tab:visible").hide();
            $("."+ uptab_pool[curr_ind]).css({'color': '#333333'});
            curr_ind = curr_ind + 1;

            $("." + tab_pool[curr_ind]).show();
            $("."+ uptab_pool[curr_ind]).css({'color': '#A31E39'});
            $(".submit").hide();
            $(".back").show();
            }
        if (curr_ind == tab_pool.length-1) {
            $(".submit").show();
            $(".next").hide();
        }
    });

    $('.back').click(function () {
        if (curr_ind > 0) {
            var tab_pool = ["tab_scenario"];
            var uptab_pool = ["scenario"];
            var vis_list = [".scenario"];
            $('input[name="scenario_cm"]:checked').each(function () {
                selec_temp = $(this).val()
                tab_pool.push(selec_temp);
                uptab_pool.push(selec_temp.slice(4));
                vis_list.push("."+selec_temp.slice(4));
            });
            
            // console.log(vis_list)
            $('.uutab').hide();
            $(vis_list.join(', ')).show();

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