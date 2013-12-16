$( document ).ready(function() {

	$('#backbutton').click(function() {
		$(this).hide();
		$('.webiceSel').show();
		$("#wiTaxatemp, #wiSSDtemp").hide();
		$('#PageName').replaceWith('<h1 id="PageName"> </h1>');
		$('#fileType').replaceWith('<div id="fileType"> </div>');
		$('#primaryType').html('');
	});
	function pageLoadTaxa() {
		$('#wiTaxatemp').show();
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/ice.js', function() {
			document.getElementById('file').value = fileFamily;
			popHeader();
			importSurrogate('Surrogate');
			importPredicted('Predicted');
		});
		$('#contbutton, #backbutton').show();
		$('.webiceSel').hide();
	}
	function pageLoadSSD() {
		$('#wiForm').attr("action","webice_SSD_output.html");
		$('#wiSSDtemp').show();
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/iceSSD.js', function() {
			initPage();
		});
		$('#backbutton').show();
		$('.webiceSel').hide();
	}
	function pageLoadTNE() {
		$('#wiForm').attr({action:"webice_TNE_output.html", onsubmit:"return checkTox();"});
		$('#ICEContent').show();
		$.getScript('http://localhost:8081/stylesheets/webice/scripts/iceTNE.js', function() {
			tneInitData();
			popHeader();
			document.getElementById('AllGroups').checked = true;
		});
		$('#backbutton').show();
		$('.webiceSel').hide();
	}
	$('#asTaxa, #agTaxa, #afTaxa, #wsTaxa, #wfTaxa, #lsTaxa, #lgTaxa').click(function() {
		pageLoadTaxa();
	});
	$('#asSSD, #wsSSD').click(function() {
		pageLoadSSD();
	});
	$('#tneAs, #tneWs').click(function() {
		pageLoadTNE();
	});

});