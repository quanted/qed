var pchempropsDefaults = ["chemaxon", "ion_con", "kow_no_ph", "kow_wph"]; //checkbox names

var pchemPopupMap = {
  'melting_point': 'mp',
  'boiling_point': 'bp',
  'water_sol': 'ws',
  'vapor_press': 'vp',
  'mol_diss': 'mdw',
  'mol_diss_air': 'mda',
  'ion_con': 'ic',
  'henrys_law_con': 'hlc',
  'kow_no_ph': 'kow',
  'koc': 'koc',
  'log_bcf': 'bcf',
  'log_baf': 'baf', 
  'kow_wph': 'd_ow',
  'water_sol_ph': 'wsph'
};

$(document).ready(function() {

    var hasBeenTipped = false;  // bool for whether tooltips have been initialized

    if ( typeof uberNavTabs == 'function' ) {
        uberNavTabs(
            ["Chemical", "ChemCalcs"],
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

    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $("#pchem-select-all").change(function() {
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
        submitButtonLogic();
    });

    //default button
    $('#resetbutton').click(function(){
        //check chemaxon and its avaiable properties
        for (i in pchempropsDefaults) {
            var chkbox = $('input[type=checkbox][name=' + pchempropsDefaults[i] + ']');
            $(chkbox).prop('checked', true);
        }
        $('.chemaxon').fadeTo(0, 1); //highlight chemaxon column
        $('#id_kow_ph').val(7.4);
    });

    //submit button logic:
    // $('.submit.input_button').prop('readonly', true); //initialize submit as disabled


    // Triggered if any checkbox is clicked on pchem table:
    $('input[type=checkbox]').not('#pchem-select-all').change(function() {
        var checkbox = $(this);
        submitButtonLogic(); //tie submitLogic() to any checkbox changes
        pchempropTableLogic(checkbox);
        // Brings up warning that TEST is slow (no longer needed for TESTWS, 08/08/18)
        // NOTE: This is now being used for OPERA as TESTWS is much faster.
        var is_checked = this.checked;
        var is_opera = false;
        if (this.id.indexOf("opera") > -1) { is_opera = true; }
        if (is_checked && is_opera) {
            // Warns user that opera takes awhile:
            alert("Note: The OPERA calculator can take several minutes to run");
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

    tipPchemTable();  // adds popups when document loads

    // // Makes p-chem table cell clickable instead of just checkbox:
    // $('th.calc-header, th.chemprop, th#pchem-select-all').on("click", function() {
    //     // Toggles checkbox values for p-chem table:
    //     var checkedVal = $(this).children('input[type=checkbox]').prop("checked");
    //     $(this).chi-ldren('input[type=checkbox]').prop("checked", !checkedVal);
    //     pchempropTableLogic();
    // });

});


function submitButtonLogic() {
    // Enable submit only when a calculator is 
    // checked AND an available property:

    var calc_checkbox = $('input[type=checkbox].calc_checkbox');

    // disable submit if no calculator is checked (and not gentrans/batch)
    // if ($(calc_checkbox).is(':not(:checked)') && window.location.href.indexOf('gentrans') < 0) {
    if ($(calc_checkbox).is(':not(:checked)' && window.location.href.indexOf('gentrans/batch') < 0)) {
        // $('.submit.input_button').prop('disabled', true).removeClass('brightBorders');
        $('.submit.input_button').removeClass('brightBorders');
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
                    // $('.submit.input_button').prop('disabled', false).addClass('brightBorders');
                    $('.submit.input_button').addClass('brightBorders');
                }
            }
        });
    }
}


function pchempropTableLogic(checkbox) {

    if (!$(checkbox).hasClass('calc_checkbox')) {
        return;
    }


    // Highlight column of selected calculator:
    // $('input.calc_checkbox').change(function() {
        // var colClass = $(this).attr('name');
        var colClass = $(checkbox).attr('name');
        // if ($(this).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        if ($(checkbox).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        else { $('td.' + colClass).fadeTo(0, 0.75); }
    // });
}


function clearPchemData() {
    // Clears all data on pchemprop table:
    $('#pchemprop_table td').not('td.colorKey').html('');
}



function tipPchemTable() {
  /*
  Uses qtip2 JS library to create popups (tooltips)
  for pchem table definitions.
  */

  // NOTE: This worked!
  $('th.chemprop').each(function() {

    var propName = $(this).children('input').attr('name');  // get pchem name (in CTS format)
    var propLabel = $(this).children('span');  // gets pchem label inside table cell

    // Loops pchem popup map (top of this file) to match cts p-chem props
    // with the p-chem definitions (some cts props will have the same definition):
    for (var ctsProp in pchemPopupMap) {
      
      if (propName == ctsProp) {
        // append popup to this pchem name in table
        var pchemKey = pchemPopupMap[ctsProp];
        var tippedProp = $('div#' + pchemKey);

        // Removes 'display: none' from tooltip div:
        // $(tooltip).css('display', 'inline');

        // Adds qtip2 popup to p-chem property label (and not the checkbox):
        $(propLabel).qtip({
          content: {
            text: $(tippedProp)
          },
            style: {
            classes: 'qtip-light'
          },
          position: {
            my: 'bottom left',  // set bottom-left of popup div..
            at: 'center right',  // at center right of label..
            target: 'mouse'  // triggered by mouse.
          }
        });

        // Adds 'none' back after qtip popup is built, so it doesn't show up initially in pchem table
        // Note: this tooltip div gets converted to a qtip div (i.e., removed from <th> elements in cts_pchem.html)
        // $(tooltip).css('display', 'none');
      
      }

    }

  });
}