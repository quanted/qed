$(document).ready(function() {
    // Call function to setup tabbed nav
    uberNavTabs(
        ["Chemical", "Avian", "Mammal"],
        {"isSubTabs": false}
    );
    listen_trex_events();
    initialize_trex();
    num_apps_table();

});

function num_apps_table() {

    var i = 2;
    var total = $('#id_num_apps').val();
    $('tr[id*="noa_header"]').show();

    while (i <= total) {
        if (i == 1) {
            $('.tab_Application').append('<tr class="tab_noa1"><td>' + i + '</td><td><input type="text" size="5" name="rate' + i + '" id="id_rate-' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day-' + i + '"  value="0" /></td></tr>');
        }

        else {
            $('.tab_Application').append('<tr class="tab_noa1"><td>' + i + '</td><td><input type="text" size="5" name="rate' + i + '" id="id_rate-' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day-' + i + '" value="' + 3 * (i - 1) + '"/></td></tr>');
        }
        i = i + 1;
    }
    while (i - 1 > total) {
        $(".tab_Application tr:last").remove();
        i = i - 1;
    }
    $('</table>').appendTo('.tab_Application');
    $('#id_num_apps').change(function () {
        var total = $(this).val();
        $('tr[id*="noa_header"]').show();

        while (i <= total) {
            if (i == 1) {
                $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate-' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day-' + i + '"  value="0" /></td></tr>');
            }

            else {
                $('.tab_Application').append('<tr class="tab_noa1"><td><input name="jm' + i + '" type="text" size="5" value="' + i + '"/></td><td><input type="text" size="5" name="rate' + i + '" id="id_rate-' + i + '" value="4"/></td><td><input type="text" size="5" name="day' + i + '" id="id_day-' + i + '" value="' + 3 * (i - 1) + '"/></td></tr>');
            }
            i = i + 1;
        }
        while (i - 1 > total) {
            $(".tab_Application tr:last").remove();
            i = i - 1;
        }
        $('</table>').appendTo('.tab_Application');
    });
}
function listen_trex_events() {
    $('.submit').click(function (e) {
        e.preventDefault();
        var app_rates = [];
        var day_outs = [];
        var unNeededFields = ['id_seed_crop_v'];

        $('[id^="id_rate-"]').each(function () {
            var rate = this.value;
            app_rates.push(rate);
            unNeededFields.push(this.id);
        });
        $('#id_app_rates').val(app_rates);

        $('[id^="id_day-"]').each(function () {
            var day_out = this.value;
            day_outs.push(day_out);
            unNeededFields.push(this.id);
        });
        $('#id_day_out').val(day_outs);

        rmFormFields(unNeededFields);

        $('.inputs_form').submit();
    });


    $('#id_noaec_bird').change(function () {
        $('#id_noael_bird').val($(this).val() / 20);
    }).trigger('change');


    $('#id_noaec_mamm').change(function () {
        $('#id_noael_mamm').val($(this).val() / 20);
    }).trigger('change');


    $('#id_application_type').change(function () {
        if ($(this).val() == 'Seed Treatment') {
            $('#id_seed_treatment_formulation_name').closest('tr').show();
            $('#id_max_seed_rate').closest('tr').show();
            $('#id_density').closest('tr').show();
            $('#id_seed_crop_v').closest('tr').show();
            $('#id_bandwidth').closest('tr').hide();
            $('#id_row_spacing').closest('tr').hide();
            $('#id_foliar_diss_hlife').closest('tr').hide();
            $('#id_percent_incorp').closest('tr').hide();
            $('.tab_Application').show();
            $('#rate_head').text('Rate (fl oz/cwt)');
            $('#id_num_apps').val(1);
            $("#id_num_apps").attr('disabled', 'disabled');
            while (i - 1 > 1) {
                $(".tab_Application tr:last").remove();
                i = i - 1
            }

            $('#id_max_seed_rate').val($('#id_seed_crop_v').val());
            $('#id_seed_crop_v_v').val($('#id_seed_crop_v :selected').text());

            $('#id_seed_crop_v').change(function () {
                $('#id_max_seed_rate').val($(this).val());
                $('#id_seed_crop_v_v').val($('#id_seed_crop_v :selected').text());
            });
        }
        else if ($(this).val() == 'Row/Band/In-furrow-Granular') {
            $('.tab_Application').show();
            $('#rate_head').text('Rate (lb ai/acre)');
            $("#id_num_apps").removeAttr('disabled');
            $('.seed').remove();
            $('#id_seed_treatment_formulation_name').closest('tr').hide();
            $('#id_max_seed_rate').closest('tr').hide();
            $('#id_density').closest('tr').hide();
            $('#id_seed_crop_v').closest('tr').hide();
            $('#id_foliar_diss_hlife').closest('tr').show();
            $('#id_percent_incorp').closest('tr').show();
            $('#id_bandwidth').closest('tr').show();
            $('#id_row_spacing').closest('tr').show();
        }
        else if ($(this).val() == 'Row/Band/In-furrow-Liquid') {
            $('.tab_Application').show();
            $('#rate_head').text('Rate (lb ai/acre)');
            $("#id_num_apps").removeAttr('disabled');
            $('.seed').remove();
            $('#id_seed_treatment_formulation_name').closest('tr').hide();
            $('#id_max_seed_rate').closest('tr').hide();
            $('#id_density').closest('tr').hide();
            $('#id_seed_crop_v').closest('tr').hide();
            $('#id_foliar_diss_hlife').closest('tr').show();
            $('#id_percent_incorp').closest('tr').show();
            $('#id_bandwidth').closest('tr').show();
            $('#id_row_spacing').closest('tr').show();
        }
        else {
            $('.tab_Application').show();
            $('#rate_head').text('Rate (lb ai/acre)');
            $("#id_num_apps").removeAttr('disabled');
            $('.seed').remove();
            $('#id_seed_treatment_formulation_name').closest('tr').hide();
            $('#id_max_seed_rate').closest('tr').hide();
            $('#id_density').closest('tr').hide();
            $('#id_seed_crop_v').closest('tr').hide();
            $('#id_bandwidth').closest('tr').hide();
            $('#id_foliar_diss_hlife').closest('tr').show();
            $('#id_percent_incorp').closest('tr').show();
            $('#id_row_spacing').closest('tr').hide();
        }
    }).trigger('change');


    $('#id_species_of_the_tested_bird_avian_ld50').change(function () {
        if ($(this).val() == "Bobwhite quail") {
            $('#id_tw_bird_ld50').val(178);
        }
        else if ($(this).val() == "Mallard duck") {
            $('#id_tw_bird_ld50').val(1580);
        }
        else {
            $('#id_tw_bird_ld50').val(7);
        }
    }).trigger('change');

    $('#id_species_of_the_tested_bird_avian_lc50').change(function () {
        if ($(this).val() == "Bobwhite quail") {
            $('#id_tw_bird_lc50').val(178);
        }
        else if ($(this).val() == "Mallard duck") {
            $('#id_tw_bird_lc50').val(1580);
        }
        else {
            $('#id_tw_bird_lc50').val(7);
        }
    }).trigger('change');

    $('#id_species_of_the_tested_bird_avian_noaec').change(function () {
        if ($(this).val() == "Bobwhite quail") {
            $('#id_tw_bird_noaec').val(178);
        }
        else if ($(this).val() == "Mallard duck") {
            $('#id_tw_bird_noaec').val(1580);
        }
        else {
            $('#id_tw_bird_noaec').val(7);
        }
    }).trigger('change');

    $('#id_species_of_the_tested_bird_avian_noael').change(function () {
        if ($(this).val() == "Bobwhite quail") {
            $('#id_tw_bird_noael').val(178);
        }
        else if ($(this).val() == "Mallard duck") {
            $('#id_tw_bird_noael').val(1580);
        }
        else {
            $('#id_tw_bird_noael').val(7);
        }
    }).trigger('change');


    $('#main_form').submit(function () {
        $('#main_form :disabled').removeAttr('disabled');
    });

};

function rmFormFields(fields) {
    for (i=0; i < fields.length; i++) {
        $('#' + fields[i]).remove();
    }
};

function initialize_trex(){

    $('#id_noael_bird').val($('#id_noaec_bird').val() / 20);
    $('#id_noael_mamm').val($('#id_noaec_mamm').val() / 20);


    $('#id_seed_treatment_formulation_name').closest('tr').hide();
    $('#id_max_seed_rate').closest('tr').hide();
    $('#id_seed_crop_v').closest('tr').hide();
    $('#id_bandwidth').closest('tr').hide();
    $('#id_row_spacing').closest('tr').hide();
    $('#id_density').closest('tr').hide();

};
