//+++++++++++++++++++++++++++++++++++++++++
//Selection logic for the Reaction Pathway
//Simulator in the gentrans workflow
//
//TODO: refactor this atrocity!!!!!
//+++++++++++++++++++++++++++++++++++++++++

$(document).ready(function() {

    var gentrans_tables = '#oecd_selection, #ftt_selection, #health_selection, ' +
                            '#cts_reaction_sys, #respiration_tbl'; // tables to hide/show

    var unaviable_options = 'select[name=ftt_selection] option[value=2], ' + 
        'select[name=ftt_selection] option[value=3], select[name=pop_limit], ' +
        '#id_aerobic_biodegrad, #id_anaerobic_biodegrad';

    if (typeof uberNavTabs == 'function') {
        uberNavTabs(
            ["Chemical", "ReactionPathSim"],
            {   "isSubTabs":true,
            	"Chemical": [".tab_chemicalButtons"] }
        );
    }

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    });

    $('input[type=radio], input[type=checkbox]').prop('checked', false); // clear data

    $(gentrans_tables).hide();

    $(unaviable_options).prop('disabled', true); // these options are currently not available

    // disable checkboxes and submit button
    // $('#cts_reaction_libs input[type="checkbox"], input.submit').prop('disabled', true);
    $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

    brightenBorder($('#cts_reaction_paths')); // brighten first table for user input


    if ($('table#cts_biotrans_libs').length > 0) {
        $('input.submit').addClass('brightBorders');
    }


    $("input[name='reaction_paths']").change(function() {

        $(gentrans_tables).hide();

        if ($(this).val() == "0") {
            //If "Reaction System" is selected
            $('#cts_reaction_sys').show();
            clearReactionLib();
            brightenBorder($('#cts_reaction_sys'));
        }

        else if ($(this).val() == "1") {
            $('#oecd_selection').show();
            clearReactionLib();
            brightenBorder($('#oecd_selection'));
        }

        else if ($(this).val() == "2") {
            // only show Reaction Library if user selected checked
            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $("input[name='reaction_system']").change(function() {

        $(gentrans_tables).hide();

        if ($(this).val() == "0") {
            //If "Environmental" is selected..
            $('#cts_reaction_sys, #respiration_tbl').show();
            clearReactionLib();
            brightenBorder($('#respiration_tbl'));
        }

        else if ($(this).val() == "1") {
            //Show Reaction Library with "Mammalian" selected
            $('#cts_reaction_sys').show();
            //Set what's checkable in Reaction Libraries table
            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $('select[name="respiration"]').change(function() {

        $(gentrans_tables).hide();
        $('#cts_reaction_sys, #respiration_tbl').show();

        if ($(this).val() == "0") {
            clearReactionLib();
            brightenBorder($(this).closest('table'));
        }

        else if ($(this).val() == "1") {
            // set Reaction Libraries ...
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        else if ($(this).val() == "2") {
            //Set Reaction Libraries table...
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $("input[name='oecd_selection']").change(function() {

        //FTT content columns
        $('#labAbioTrans_picks').hide();
        $('#transWaterSoil_picks').hide();
        $('#transChemSpec_picks').hide();

        $(gentrans_tables).hide();

        if ($(this).val() == "0") {
            //If FTT is selected
            $('#oecd_selection').show();
            $('#ftt_selection').show();
            clearReactionLib();
            brightenBorder($('#ftt_selection'));
        }
        else if ($(this).val() == "1") {
            //If "Health Effects" is selected
            $('#oecd_selection').show();
            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $('select[name="ftt_selection"]').change(function() {

        var value = $(this).val();

        $(gentrans_tables).hide();

        $('#oecd_selection').show();
        $('#ftt_selection').show();

        if ($(this).val() == "0") {
            clearReactionLib();
            brightenBorder($(this).closest('table'));
        }

        else if ($(this).val() == "1") {
            //If  Laboratory Abiotic Transformation Guidelines is selected
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }
        else {
            clearReactionLib();
        }

        clearHiddenInputs();

    });

    // Enable submit only if a reaction library is selected
    $('#cts_reaction_libs input:checkbox').on("change", function() {

        // Mammalian metabolism should not run with any other reaction library..
        // if (this.
        var mamm_meta_checked = $('#id_mamm_metabolism:checked').length > 0;
        var areduct_checked = $('#id_abiotic_reduction:checked').length > 0;
        var ahydro_checked = $('#id_abiotic_hydrolysis:checked').length > 0;
        if (mamm_meta_checked && (areduct_checked || ahydro_checked)) {
            $('#id_mamm_metabolism').prop({'checked': false});  // uncheck, disable if mamm meta checked
            // if (areduct_checked || areduct_checked) {
                alert("Mammalian metabolism should not run with additional reaction libraries");
            // }
        }

        if ($('#cts_reaction_libs input:checkbox:checked').length > 0) {
            // $('input.submit').prop('disabled', false).addClass('brightBorders');
            $('input.submit').addClass('brightBorders');
        }
        else {
            // $('input.submit').prop('disabled', true).removeClass('brightBorders');
            $('input.submit').removeClass('brightBorders');
        }
    });

});


function brightenBorder(element) {
    // remove border from previous, add to current
    $('table').removeClass('brightBorders'); // remove all 
    $(element).addClass('brightBorders'); // add to specified element
}


function clearReactionLib() {
    $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
    $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
    $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
}


function clearHiddenInputs() {
    // clear all radios and selects that are hidden:
    var hidden_inputs = $('div.tab_ReactionPathSim :input:hidden');
    for (index in hidden_inputs) {
        if (hidden_inputs.hasOwnProperty(index)) {
            var input = hidden_inputs[index];
            if (input.type == "radio") {
                $(input).prop('checked', false);
            }
            else if (input.type == "select-one") {
                $(input).val("0"); 
            }
        }
    }
}