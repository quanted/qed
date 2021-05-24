$( document ).ready(function() {

	// BlockUI on Form Submit
	$("button").click(function (e) {
		e.preventDefault();
		// var form_valid = $("form").valid();
		var form_valid;

		if (typeof form_valid == 'undefined'){
			$.blockUI({
			  css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
			  message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static_qed/images/loader.gif" style="margin-top:-16px">',
			  fadeIn:  500
			});
			setTimeout(function() {$('form').submit();}, 500);
		}

		// if (typeof form_valid !== 'undefined' && form_valid !== false){
		else {
			e.preventDefault();
			// ES Mapper check
			if (model == "es_mapping") {
				var html_input = $("form").html();
				localStorage.html_input=html_input;

				var html_new = $("form").serialize();

				localStorage.html_new=html_new;
				console.log(localStorage);
			}
			$.blockUI({
			  css:{ "top":""+wintop+"", "left":""+winleft+"", "padding": "30px 20px", "width": "400px", "height": "60px", "border": "0 none", "border-radius": "4px", "-webkit-border-radius": "4px", "-moz-border-radius": "4px", "box-shadow": "3px 3px 15px #333", "-webkit-box-shadow": "3px 3px 15px #333", "-moz-box-shadow": "3px 3px 15px #333" },
			  message: '<h2 class="popup_header">Processing Model Submission...</h2><br/><img src="/static_qed/images/loader.gif" style="margin-top:-16px">',
			  fadeIn:  500
			});
			setTimeout(function() {$('form').submit();}, 500);
		}
	});

	$('#resetbutton').click(
		function(){
			// Store Checkbox values
			var valuesCheckbox = [];
			var selectedCheckbox = $("input:checkbox").each(
				function(){
					valuesCheckbox.push( $(this).is(':checked'));
			});

			// Create array of hidden tabs
			var hiddenTabs = [];
			var fill_hiddenTabs = $(".tab:hidden").each(
				function(){
					hiddenTabs.push(this);
			});

			// Store radio button values
			var valuesRadio = [];
			var selectedRadio = $(hiddenTabs).find("input:radio").each(
				function(){
					valuesRadio.push( $(this).is(':checked'));
			});

			// Store TextArea values
			var valuesTextArea = [];
			var selectedTextArea = $(hiddenTabs).find("textarea").each(
				function(){
					valuesTextArea.push( $(this).val());
			});

			// Store Text values
			var valuesText = [];
			var selectedText = $(hiddenTabs).find("input:text").each(
				function(){
					valuesText.push( $(this).val());
			});

			// Reset Form (default values)
			this.form.reset();

			// Re-Fill inputs with previous user input values
			for (i=0;i<selectedCheckbox.length;i++) {
				$(selectedCheckbox[i]).prop('checked', valuesCheckbox[i]);
			}
			for (i=0;i<selectedRadio.length;i++) {
				$(selectedRadio[i]).prop('checked', valuesRadio[i]);
			}
			for (i=0;i<selectedTextArea.length;i++) {
				$(selectedTextArea[i]).prop('value', valuesTextArea[i]);
			}
			for (i=0;i<selectedText.length;i++) {
				$(selectedText[i]).prop('value', valuesText[i]);
			}
	});

	$('#clearbutton').click(
		function(){
		$("table[class^='tab']:visible").find(':input').each(function() {
			switch(this.type) {
				case 'text':
				case 'textarea':
					$(this).val('');
					break;
				case 'radio':
					this.checked = false;
			}
		});
	});

	// Save Metadata
	$('#metaDataTxtArea').prop('disabled', true);
	$('#metaDataToggle').change(function() {
		if ($('#metaDataToggle').prop( "checked" )) {
			$('#metaDataTxtArea').prop('disabled', false);
			$('#metaDataDiv').slideDown();
		} else {
			$('#metaDataDiv').slideUp();
			$('#metaDataTxtArea').prop('disabled', true);
		}
	});

});

// Tabbed Nav
function uberNavTabs( modelTabs, subTabs ) {
	var tab_pool = [], liTabArray = [], noOfTabs = modelTabs.length;
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
	$(".back, .submit, #metaDataToggle, #metaDataText").hide();

	// Click handler
	$('.input_nav ul li').click(function() {
		// Check if "li" element has class (ignores the input buttons)
		if ($(this).attr('class')) {
			var testClass = $(this).attr("class").split(' ')[0];


			curr_ind = $.inArray(testClass, modelTabs);


			// Remove current tab from array;
			var liTabArrayMinusCurr = liTabArray.slice(0);
			liTabArrayMinusCurr.splice(curr_ind,1);


			if (curr_ind == 0) {

				
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
				$(tab_pool[curr_ind]+", .back, .next").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}

			if ( curr_ind == (modelTabs.length-1) ) {


				$(liTabArray[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
				$(liTabArrayMinusCurr.join(',')).addClass('tabUnsel').removeClass('tabSel');
				$('.tab:visible, .next, #metaDataToggle, #metaDataText').hide();
				$(tab_pool[curr_ind]+", .back, .submit").show();
				// Check if this tab has subTabs
				if ( subTabs.isSubTabs && subTabs.hasOwnProperty(testClass) ) {
					$(subTabs[testClass].toString()).show();
				}
			}
		}
	});

	$('.next').click(function () {
		var tab = $(".tab:visible");
		if (curr_ind < (modelTabs.length-1)) {
			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind + 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".back").show();
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
		if (curr_ind > 0) {
			$(".tab:visible").hide();
			$("."+ uptab_pool[curr_ind]).addClass('tabUnsel').removeClass('tabSel');
			curr_ind = curr_ind - 1;
			$(tab_pool[curr_ind]).show();
			$("."+ uptab_pool[curr_ind]).addClass('tabSel').removeClass('tabUnsel');
			$(".submit, #metaDataToggle, #metaDataText").hide();
			$(".next").show();
			// Check if this tab has subTabs
			if ( subTabs.isSubTabs ) {
				var subTabsText = tab_pool[curr_ind].replace(".tab_","");

				if ( subTabs.hasOwnProperty(subTabsText) ) {
					$(subTabs[subTabsText].toString()).show();
				}
			}
		}
		if (curr_ind == 0) {
			$(".back, #metaDataToggle, #metaDataText").hide();
		}
	});

	// Error Handling, show tab with error
	var isError = $('form').find('.errorlist');
	if (isError.length > 0) {
		var tableWithError = $(isError).closest('table');
		var tableWithErrorClass = tableWithError.attr('class').split(' ')[2].slice(4);
		if (modelTabs.includes(tableWithErrorClass)) {
			$('.' + tableWithErrorClass).trigger('click');
		}
	}
}