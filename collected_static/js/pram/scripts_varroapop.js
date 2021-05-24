$(document).ready(function() {
    // Call function to setup tabbed nav

    listen_varroapop_events();
    initialize_varroapop();
    uberNavTabs(
        ["Colony", "Mites", "Chemical", "Resources"],
        {   "isSubTabs":false   }
    );

});


function initialize_varroapop(){

    //Split Resources tab into two tables
    var $mainTable = $('.tab_Resources');
    var splitBy = 17;
    var rows = $mainTable.find("tr").slice(splitBy);
    var $secondTable = $("<table id='secondTable' class='input_table tab tab_Resources tab_Consumption ' style='display:none'><tbody></tbody></table>").insertAfter($mainTable);
    $secondTable.find("tbody").append(rows);
    $mainTable.find ( "tr" ).slice( splitBy ).remove();

};

function listen_varroapop_events() {

    $('#id_RQEnableReQueen').change(function () {

        if ($(this).val() == "false") {
            $('#id_RQScheduled').attr('disabled', 'disabled');

        }
        else if ($(this).val() == "true") {
            $('#id_RQScheduled').removeAttr('disabled');

        }
    }).trigger('change');

    $('#id_RQScheduled').change(function () {

        if ($(this).val() == "false") {
            $('#id_RQReQueenDate_month').attr('disabled', 'disabled');
            $('#id_RQReQueenDate_day').attr('disabled', 'disabled');
            $('#id_RQReQueenDate_year').attr('disabled', 'disabled');
            $('#id_RQonce').attr('disabled', 'disabled');


        }
        else if ($(this).val() == "true") {
            $('#id_RQReQueenDate_month').removeAttr('disabled');
            $('#id_RQReQueenDate_day').removeAttr('disabled');
            $('#id_RQReQueenDate_year').removeAttr('disabled');
            $('#id_RQonce').removeAttr('disabled');
        }
    }).trigger('change');

    $('#id_enable_mites').change(function () {

        if ($(this).val() == "false") {
            $('.tab_Mites :input').not($(this)).attr('disabled', 'disabled');
        }
        else if ($(this).val() == "true") {
            $('.tab_Mites :input').not($('.mite_imm, .mite_treat')).removeAttr('disabled');
            $('#id_ImmEnabled').trigger('change');
            $('#id_VTEnable').trigger('change');
        }
    }).trigger('change');


    $('#id_ImmEnabled').change(function () {

        if ($(this).val() == "false") {
            $('.mite_imm').attr('disabled', 'disabled');
            $('.mite_imm').closest('tr').hide();
        }
        else if ($(this).val() == "true") {
            $('.mite_imm').removeAttr('disabled');
            $('.mite_imm').closest('tr').show();
        }
    }).trigger('change');

    $('#id_VTEnable').change(function () {

        if ($(this).val() == "false") {
            $('.mite_treat').attr('disabled', 'disabled');
            $('.mite_treat').closest('tr').hide();
        }
        else if ($(this).val() == "true") {
            $('.mite_treat').removeAttr('disabled');
            $('.mite_treat').closest('tr').show();
        }
    }).trigger('change');


    $('#id_application_type').change(function () {

        if ($(this).val() == "Foliar spray") {
            $('.foliar').closest('tr').show();
            $('.soil').closest('tr').hide();
            $('.seed').closest('tr').hide();
            $('.foliar').removeAttr('disabled');
            $('.soil').attr('disabled', 'disabled');
            $('.seed').attr('disabled', 'disabled');
            $('#id_FoliarEnabled').val('true');
            $('#id_SoilEnabled').val('false');
            $('#id_SeedEnabled').val('false');
        }
        else if ($(this).val() == "Soil") {
            $('.foliar').closest('tr').hide();
            $('.soil').closest('tr').show();
            $('.seed').closest('tr').hide();
            $('.foliar').attr('disabled', 'disabled');
            $('.soil').removeAttr('disabled');
            $('.seed').attr('disabled', 'disabled');
            $('#id_FoliarEnabled').val('false');
            $('#id_SoilEnabled').val('true');
            $('#id_SeedEnabled').val('false');
        }
        else {
            $('.foliar').closest('tr').hide();
            $('.soil').closest('tr').hide();
            $('.seed').closest('tr').show();
            $('.foliar').attr('disabled', 'disabled');
            $('.soil').attr('disabled', 'disabled');
            $('.seed').removeAttr('disabled');
            $('#id_FoliarEnabled').val('false');
            $('#id_SoilEnabled').val('false');
            $('#id_SeedEnabled').val('true');
        }
    }).trigger('change');


    $('#id_enable_pesticides').change(function () {

        if ($(this).val() == "false") {
            $('.tab_Chemical :input').not($(this)).attr('disabled', 'disabled');
            $('#id_FoliarEnabled').val('false');
            $('#id_SoilEnabled').val('false');
            $('#id_SeedEnabled').val('false');
        }
        else if ($(this).val() == "true") {
            $('.tab_Chemical :input').removeAttr('disabled');
            $('#id_application_type').trigger('change');
        }
    }).trigger('change');


    $('#id_SupPollenEnable').change(function () {

        if ($(this).val() == "false") {
            $('.sup_pol').attr('disabled', 'disabled');
            $('.sup_pol').closest('tr').hide();
        }
        else if ($(this).val() == "true") {
            $('.sup_pol').removeAttr('disabled');
            $('.sup_pol').closest('tr').show();
        }
    }).trigger('change');


    $('#id_SupNectarEnable').change(function () {

        if ($(this).val() == "false") {
            $('.sup_nec').attr('disabled', 'disabled');
            $('.sup_nec').closest('tr').hide();
        }
        else if ($(this).val() == "true") {
            $('.sup_nec').removeAttr('disabled');
            $('.sup_nec').closest('tr').show();
        }
    }).trigger('change');

    //$(window).bind('beforeunload', function () {
    //    $(":reset").click();
    //});

    $('#main_form').submit(function () {
        $('#main_form :disabled').removeAttr('disabled');

        if ($('#id_enable_mites').val() == "false"){
            $('#id_ICWorkerAdultInfest').val(0);
            $('#id_ICWorkerBroodInfest').val(0);
            $('#id_ICDroneAdultInfest').val(0);
            $('#id_ICDroneBroodInfest').val(0);
            $('#id_ImmEnabled').val("false");
            $('#id_VTEnable').val("false");
        }
    });
}


//$(window).bind("pageshow", function(event) {
//    if (event.originalEvent.persisted) {
//        listen_varroapop_events();
//        initialize_varroapop();
//    }
//});
