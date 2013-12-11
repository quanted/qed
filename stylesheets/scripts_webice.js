$( document ).ready(function() {
	// var iceScriptsPath = pathDoamin + '/stylesheets/webice/scripts/ice.js';
	// $('.webice a').click(function() {
	// 	$.getScript(iceScriptsPath);
	// });
	
	$('#asTaxa').click(function() {
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/ice.js', function() {
			importSurrogate('Surrogate');
			importPredicted('Predicted');
			document.getElementById('file').value = fileFamily;
			// popHeader();
		});
		$('.asTaxaSel').show();
		$('.webiceSel').hide();
		$('.model_header').children().append(': Aquatic Species - Taxa Selection Page');
		// e.preventDefault();
	});
	
});