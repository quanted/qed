$( document ).ready(function() {

	$('#backbutton').click(function() {
		$(this).hide();
		$('.webiceSel').show();
		$("#wiTaxatemp, .wiSSDtemp").hide();
		$('.model_header').replaceWith('<h2 class="model_header">Web-ICE v3.2.1</h2>');
		$('#primaryType').html('');
	});
	function pageLoadTaxa() {
		$('#wiTaxatemp').show();
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/ice.js', function() {
			importSurrogate('Surrogate');
			importPredicted('Predicted');
			document.getElementById('file').value = fileFamily;
			// popHeader();
		});
		$('#contbutton, #backbutton').show();
		$('.webiceSel').hide();
	}
	function pageLoadSSD() {
		$('.wiSSDtemp').show();
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/iceSSD.js', function() {
			initPage();
		});
		$('#backbutton').show();
		$('.webiceSel').hide();
	}
	$('#asTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Aquatic Species - Taxa Selection Page');
	});
	$('#agTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Aquatic Genus - Taxa Selection Page');
	});
	$('#afTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Aquatic Family - Taxa Selection Page');
	});
	$('#wsTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Wildlife Species - Taxa Selection Page');
	});
	$('#wfTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Wildlife Family - Taxa Selection Page');
	});
	$('#lsTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Algae Species - Taxa Selection Page');
	});
	$('#lgTaxa').click(function() {
		pageLoadTaxa();
		$('.model_header').append(': Algae Genus - Taxa Selection Page');
	});

	$('#asSSD').click(function() {
		pageLoadSSD();
		$('.model_header').append(': Species Sensitivity Distributions - Aquatic Species');
	});
	$('#awSSD').click(function() {
		pageLoadSSD();
		$('.model_header').append(': Species Sensitivity Distributions - Wildlife Species');
	});

});