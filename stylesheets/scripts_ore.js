$( document ).ready(function() {
	// Call function to setup tabbed nav
    uberNavTabs(
        ['ToxInp', 'CropTargetSel', 'OccHandler'],
        {   "isSubTabs":false	}
    );

	// Inital setup
	$('.tab_tox_st').show();
	$('.tab_tox_it, .tab_tox_lt, .tab_CropTargetSel').hide();
	$('#id_expDurationType_0').prop("checked",true);

	// Checkboxes
	var selectedArray = ["id_expDurationType_0"]  // default with Short-term selected
	$("input[name='expDurationType']").click(function() {
		var selection = $(this).attr('id');
		console.log(selection);
		arrayIndex = $.inArray(selection, selectedArray);
		if ( arrayIndex == -1) {
			selectedArray.splice(0, 0, selection);  // add selection to array
			switch(selection) {
				case 'id_expDurationType_0':
					$('.tab_tox_st').show();
					break;
				case 'id_expDurationType_1':
					$('.tab_tox_it').show();
					break;
				case 'id_expDurationType_2':
					$('.tab_tox_lt').show();
					break;
			}
		} else {
			selectedArray.splice(arrayIndex, 1);  // remove selection from array
			switch(selection) {
				case 'id_expDurationType_0':
					$('.tab_tox_st').hide();
					break;
				case 'id_expDurationType_1':
					$('.tab_tox_it').hide();
					break;
				case 'id_expDurationType_2':
					$('.tab_tox_lt').hide();
					break;
			}
		}

	});

});