var chemspecDefaults = {
    "pKa_decimals": 2,
    "pKa_pH_lower": 0,
    "pKa_pH_upper": 14,
    "pKa_pH_increment": 0.2,
    "pH_microspecies": 7.0,
    "isoelectricPoint_pH_increment": 0.5,
    "tautomer_maxNoOfStructures": 100,
    "tautomer_pH": 7.0,
    "stereoisomers_maxNoOfStructures": 100
};

// ordered list of inputs:
var chemspec_params = ["pKa_decimals", "pKa_pH_lower", "pKa_pH_upper", "pKa_pH_increment",
                        "pH_microspecies", "isoelectricPoint_pH_increment", "tautomer_maxNoOfStructures",
                        "tautomer_pH", "stereoisomers_maxNoOfStructures"]


$(document).ready(function() {

    if ( typeof uberNavTabs == 'function' ) {
        uberNavTabs(
            ["Chemical", "Speciation"],
            {   "isSubTabs":true,
            	"Chemical": [".tab_chemicalButtons"] }
        );
    }

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    	// $('#chemEditLookup').hide();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    	// $('#chemEditDraw').hide();
    });

    $('#resetbutton').parent('li').show(); // only workflow with defaults button

    //default button
    $('#resetbutton').click(function(){
        //load default values to fields 
        for (key in chemspecDefaults) {
            if (chemspecDefaults.hasOwnProperty(key)) {
                $('input[name=' + key + ']').val(chemspecDefaults[key]);
            }
        }
        //check first table (calculate ionization constants parameters)
        var defaultChkbox = $('input[name=get_pka]');
        $(defaultChkbox).prop('checked', true);
        enableTable(defaultChkbox);
    });

    //disable all input fields until checked:
    $('input').not('input[type="checkbox"], input[type="button"]').prop('readonly', true);

    enableTable($('input[type="checkbox"]'));

    $('input[type="checkbox"]').change(function() {
        enableTable(this);
    });

    //mouseover speciation table - highlight its textbox:
    $('table.tab_Speciation').hover(
        function() {
            //mouseenter
            $(this).removeClass('darken');
            $(this).find('input[type=checkbox]').addClass('brightBorders');
        },
        function() {
            //mouseleave
            var checked = $(this).find('input[type=checkbox]').is(':checked');
            if (!checked) {
                $(this).addClass('darken'); 
            }
            $(this).find('input[type=checkbox]').removeClass('brightBorders');
        }   
    );

});


//Enables or disables table depending
//on its checkbox state
function enableTable(chkbox) {

    $(chkbox).each(function() {

        var table = $(this).closest('table');

        if ($(this).is(":checked")) {
            table.find('input[type=number], input[type=text]').prop('readonly', false);
            table.removeClass('darken');
        }
        else {
            table.find('input[type=number], input[type=text]').prop('readonly', true);
            table.addClass('darken');
        }

        //Submit only enabled if a checkbox is selected:
        if ($('input[type="checkbox"]').is(":checked")) {
            // $('input[type="submit"]').prop('disabled', false).addClass('brightBorders');
            $('input[type="submit"]').addClass('brightBorders');
        }
        else {
            // $('input[type="submit"]').prop('disabled', true).removeClass('brightBorders');
            $('input[type="submit"]').removeClass('brightBorders');
        }

    });

}