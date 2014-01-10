$( document ).ready(function() {

	$('#resetbutton').click(
		function(){
			var values = [];
      		var selected = $("input:checkbox").each(
     		 function(){
          		values.push( $(this).is(':checked'));
     		});
			this.form.reset();
			for (i=0;i<selected.length;i++) {
				$(selected[i]).prop('checked', values[i]);
			}
	});

	$('#clearbutton').click(
		function(){
		$(this.form).find(':input').each(function() {
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
