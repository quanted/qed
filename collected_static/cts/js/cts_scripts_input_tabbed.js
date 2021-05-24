$( document ).ready(function() {

	// if errors on one tab but not another, go to tab
	// that has errors displayed
	var error_list = $('ul.errorlist');
	if ($(error_list).length > 0) {
		var closest_table = $(error_list).closest('table.input_table');
		if ($(closest_table).hasClass('tab_Speciation')) {
			// display tab_Speciation tab:
			$('.tab_Chemical').hide();
			$('.tab_Speciation').show();
			//highlight appropriate tab:
			$('li.Chemical').removeClass('tabSel').addClass('tabUnsel');
			$('li.Speciation').removeClass('tabUnsel').addClass('tabSel');
			//display proper buttons:
			$('.next, #metaDataToggle, #metaDataText').hide();
			$(".back, .submit, #resetbutton").show();
		}
	}


	//++++++++++ From scripts_inputs.js in ubertool_eco ++++++++++++
	//BlockUI on Form Submit
	$("input[value='Submit']").click(function (e) {

		e.preventDefault();

		// If submit button doesn't have brightBorders (model ready for submission),
		// then display alert that inputs must be selected before submitting model.
		var submitReady = $('input.brightBorders');
		if (submitReady.length < 1) {
			// Display alert to select inputs before submitting model:
			alert("User must select model inputs before submitting..");
			return;
		}

		// implement field validation for checked tables:
		var tables_to_validate = $('table input:checkbox:checked').closest('table');
		var input_fields = $(tables_to_validate).find('input').not('input:checkbox');

		$('input').not('checkbox').removeAttr('data-parsley-group'); // remove from all fields
		$(input_fields).attr('data-parsley-group', 'validate'); // add group name to inputs

		$('#form').parsley().validate("validate"); // todo: figure out why it's still validating the whole form
		var valid = $('#form').parsley().isValid();

        if (valid) {
        	$.blockUI({
			  css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "200px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
			  message: '<div id="pchem_wait"><h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static_qed/cts/images/loader.gif" style="margin-top:-16px"></div>',
			  fadeIn:  500
			});
			setTimeout(function() {$('#form').submit();}, 500);
        }
        else {
        	return;
        }
		
	});

	$('#clearbutton').click(function(){
		// $("table[class^='tab']:visible").find(':input').each(function() {

		//Needs to only clear the selected tab
		//tab classes: [Chemical, Speciation] and [tabSel, tabUnsel]
		//divs have classes: tab_Chemical or tab_Speciation

		$('input:visible, textarea:visible').not('#id_kow_ph').each(function () {
			switch(this.type) {
				case 'text':
					$(this).val('');
					break;
				case 'textarea':
					$(this).val('');
					break;
				case 'radio':
					this.checked = false;
					break;
				case 'number':
					$(this).val('');
					break;
				case 'checkbox':
					//need .change() to trigger chkbox change event...
					$(this).prop('checked', false).change(); 
					break;
			}
		});

		// Handles Chemical Editor tab defaults:
		if ($('li.Chemical').hasClass('tabSel')) {
			marvinSketcherInstance.clear(); //clear marvinjs sketch
		}

	});


	//Highlight errors on form 
	$('.errorlist').each(function() {
		var parentCell = $(this).parent();
		var input = $(parentCell).find('textarea, input');
		if (input.length == 0) {
			//if .errorList element is a sibling of element with error:
			input = $(parentCell).siblings('textarea, input:not([type=checkbox])');
		}
		$(input).addClass('formError');
	});

	//Remove formError class when focused on textbox:



	// Single user ("normal") and batch mode templates:
	$('#run_type').change(function () {
		var run_type = $(this).val();
		if (run_type === "batch") {
			// load batch divs, hide single mode chemical editor:
			console.log("batch mode boyzzz");
			$('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
			$("#batchChemEdit").show();
		}
		else {
			// load normal chemical editor divs
		}
	});


});

// Tabbed Nav
function uberNavTabs( modelTabs, subTabs ) {
	var tab_pool = [], liTabArray = [], noOfTabs = modelTabs.length
	// Create 'tab_' & 'li.' arrays
	for (var i=0;i<noOfTabs;i++) {
		var addTabText = ".tab_"+modelTabs[i];
		tab_pool.push(addTabText);
		var addTabText_li = 'li.'+modelTabs[i];
		liTabArray.push(addTabText_li);
	}

	// Setup tab defaults
	var uptab_pool = modelTabs;
	var curr_ind = 0;
	$(".back, .submit, #metaDataToggle, #metaDataText, #resetbutton").hide();
	
	// $('.tabUnsel').hide();

	// Click handler
	$('.input_nav ul li').not('#clearbutton').click(function() {

		// don't validate fields if hitting "clear" button
		// var test = $(this);

		var form = $('#form');
    	form.parsley().validate(); // validate form

		// validate fields before tabbing
		if (!form.parsley().isValid()) { return; } // return if form not valid

		// Checking that chemical info has been obtained before moving on:
		var isInputsPage = window.location.href.indexOf('input') > 0;  // only perform Results table check if on inputs endpoint
		if (isInputsPage && !inputChemIsValid()) {
			alert("Enter or draw a chemical, then click to get chemical information before going to next page.");
			return;
		}


		// Check if "li" element has class (ignores the input buttons)
		if ($(this).attr('class')) {
			var testClass = $(this).attr("class").split(' ')[0];

			curr_ind = $.inArray(testClass, modelTabs);

			// Remove current tab from array;
			var liTabArrayMinusCurr = liTabArray.slice(0);
			liTabArrayMinusCurr.splice(curr_ind,1);

			if (curr_ind == 0) {

				// chemical editor tab doesn't need defaults button:
				$('#resetbutton').hide();
				
				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .back, .submit, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .next").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}


			}

			if ( curr_ind > 0 && curr_ind < (modelTabs.length-1) ) {

				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .submit, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .back, .next, #resetbutton").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}

			}

			if ( curr_ind == (modelTabs.length-1) ) {

				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .next, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .back, .submit, #resetbutton").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}
		}
	});

	$('.next').click(function () {

        if (!validFields()) { return; }

        // Checking that chemical info has been obtained before moving on:
       	var isInputsPage = window.location.href.indexOf('input') > 0;  // only perform Results table check if on inputs endpoint
		if (isInputsPage && !inputChemIsValid()) {
			// Returns before going to next tab.
			// Note: li tab nav click is triggered, so Results check is performed.
			return;
		}

		window.scroll(0,0); //scroll to top

		var tab = $(".tab:visible");
		if (curr_ind < (modelTabs.length-1)) {

			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind + 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".back, #resetbutton").show();
			// Check if this tab has subTabs
			if ( subTabs.isSubTabs && curr_ind > 1 ) {
				var subTabsText = tab_pool[curr_ind].replace(".tab_","");

				if ( subTabs.hasOwnProperty(subTabsText) ) {
					$(subTabs[subTabsText].toString()).show();
				}
			}
		}
		if (curr_ind == (modelTabs.length-1)) {
			
			$('.submit, #metaDataToggle, #metaDataText').show();
			$(".next").hide();
			
		}
	});

	$('.back').click(function () {

		if (!validFields()) { return; }

		window.scroll(0, 0); //scroll to top

		if (curr_ind > 0) {
			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind - 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".next, #resetbutton").show();
			// Check if this tab has subTabs
			if ( subTabs.isSubTabs ) {
				var subTabsText = tab_pool[curr_ind].replace(".tab_","");

				if ( subTabs.hasOwnProperty(subTabsText) ) {
					$(subTabs[subTabsText].toString()).show();
				}
			}
		}
		if (curr_ind == 0) {
			$(".back, #metaDataToggle, #metaDataText, #resetbutton").hide();
		}
	});

    // if submit is enabled, make it glow for the slow
    $('input[type=submit]').change(function() {
        if ($(this).prop('disabled', false)) {
            $(this).addClass('brightBorders');
        }
        else {
            $(this).removeClass('brightBorders');
        }
    });

}


function validFields() {
	// validate fields w/ parsely
    var form = $('#form');
    form.parsley().validate(); // validate form
    return form.parsley().isValid(); // check if form is valid
}



function inputChemIsValid() {
	// Makes sure Results table has values before going to next inputs section
	var textAreaText = $('textarea#chemical').val();
	if (textAreaText.length < 1) {
		// Displays error message about submitting a chemical before
		// going to the next set of model inputs:
		return false;
	}
	return true;
}