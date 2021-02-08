var pchempropsDefaults = ["chemaxon", "ion_con", "kow_no_ph", "kow_wph"]; //checkbox names

$(document).ready(function() {

    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $("#id_all").change(function() {
        switch(isAllChecked_ChemCalcs) {
            case 1:
                isAllChecked_ChemCalcs = 0;
                $(".chemprop input:checkbox").prop( "checked", true );
                console.log('Set checked');
                break;
            case 0:
                $(".chemprop input:checkbox").prop( "checked", false );
                isAllChecked_ChemCalcs = 1;
                console.log('Set unchecked');
                break;
            default:
                console.log('JavaScript Error');
        }
    });

    //default button
    $('#resetbutton').click(function(){
        //check chemaxon and its avaiable properties
        for (i in pchempropsDefaults) {
            var chkbox = $('input[type=checkbox][name=' + pchempropsDefaults[i] + ']');
            $(chkbox).prop('checked', true);
        }
        $('.chemaxon').fadeTo(0, 1); //highlight chemaxon column
        $('#id_kow_ph').val(7.0);
    });

    //submit button logic:
    $('.submit.input_button').prop('disabled', true); //initialize submit as disabled


    // Triggered if any checkbox is clicked on pchem table:
    $('input[type=checkbox]').change(function() {

        submitButtonLogic(); //tie submitLogic() to any checkbox changes
        pchempropTableLogic();

        var workflow_url = window.location.href;

        // abandon if not in gentrans workflow to begin with:
        // if (workflow_url.indexOf("gentrans") < 0) { return; }

        var is_checked = this.checked;
        var is_TEST = false;

        if (this.id.indexOf("test") > -1) { is_TEST = true; }

        if (is_checked && is_TEST) {
            // warn user that TEST takes awhile:
            // TODO: maybe do a fancier popup near the TEST checkbox, not an obtrusive alert message!!!
            alert("Note: The TEST calculator can take several minutes to run");
        }

    });

    //Initialize all checkboxes to be unchecked:
    $("input:checkbox").prop('checked', false);

    //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    //Make them slightly transparent, then darken a column that's selected.
    $('.ChemCalcs_available').fadeTo(0, 0.75);  
    $('.ChemCalcs_unavailable').fadeTo(0, 0.75);

    pchempropTableLogic();

    $('#btn-pchem-cleardata').on('click', clearPchemData);

});


function submitButtonLogic() {
    // Enable submit only when a calculator is 
    // checked AND an available property:

    var calc_checkbox = $('input[type=checkbox].calc_checkbox');

    // disable submit if no calculator is checked (and not gentrans/batch)
    // if ($(calc_checkbox).is(':not(:checked)') && window.location.href.indexOf('gentrans') < 0) {
    if ($(calc_checkbox).is(':not(:checked)' && window.location.href.indexOf('gentrans/batch') < 0)) {
        $('.submit.input_button').prop('disabled', true).removeClass('brightBorders');
    }

    // if (window.location.href.indexOf('pchemprop') > -1) {
    if (window.location.href.indexOf('gentrans/batch') < 0) {
        // loop through calculators' checkboxes
        $(calc_checkbox).each(function() {
            if ($(this).is(':checked')) {
                var calcName = $(this).attr('name');
                var availableProps = $('td.ChemCalcs_available.' + calcName);
                //enable submit if checked calculator has checked properties
                if ($(availableProps).parent().find('input[type=checkbox]').is(':checked')) {
                    $('.submit.input_button').prop('disabled', false).addClass('brightBorders');
                }
            }
        });
    }
}


function pchempropTableLogic() {
    // Highlight column of selected calculator:
    $('input.calc_checkbox').change(function() {
        var colClass = $(this).attr('name');
        if ($(this).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        else { $('td.' + colClass).fadeTo(0, 0.75); }
    });
}


function clearPchemData() {
    // Clears all data on pchemprop table:
    $('#pchemprop_table td').not('td.colorKey').html('');
}