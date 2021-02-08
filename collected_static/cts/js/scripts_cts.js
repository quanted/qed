$(document).ready(function() {
    // Call function to setup tabbed nav
    // uberNavTabs(
    //     ["Chemical", "Speciation", "ChemCalcs", "Transform"],
    //     {   "isSubTabs":true,
    //     	"Chemical": [".tab_chemicalButtons"] }
    // );

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    	// $('#chemEditLookup').hide();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    	// $('#chemEditDraw').hide();
    });

    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $("#id_all").click(function() {
        // for (var i=0;1<noOfInput_ChemCalcs;i++) {
        //     if ($(".tab_ChemCalcs input").prop( "checked" )) {

        //     }
        // }
        // if ($(".tab_ChemCalcs input").prop( "checked" )) {
        //     console.log($(".tab_ChemCalcs input").attr('id'));
        // }
        switch(isAllChecked_ChemCalcs) {
            case 1:
                isAllChecked_ChemCalcs = 0;
                $(".tab_ChemCalcs input").prop( "checked", true );
                console.log('Set checked');
                break;
            case 0:
                $(".tab_ChemCalcs input").prop( "checked", false );
                isAllChecked_ChemCalcs = 1;
                console.log('Set unchecked');
                break;
            default:
                console.log('JavaScript Error');
        }
    });
});