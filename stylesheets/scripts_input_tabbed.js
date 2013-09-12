$( document ).ready(function() {

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

});