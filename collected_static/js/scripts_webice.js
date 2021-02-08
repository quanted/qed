$( document ).ready(function() {

	$('#backbutton').click(function() {
		$(this).hide();
		$('.webiceSel').show();
		$("#wiTaxatemp, #wiSSDtemp, #ICEContent").hide();
		$('#PageName').replaceWith('<h1 id="PageName"> </h1>');
		$('#fileType').replaceWith('<div id="fileType"> </div>');
		$("input[type='hidden']").attr({name:'', id:''});
		$('#primaryType').html('');
	});
	function pageLoadTaxa() {
		$('div#wiTaxatemp').show();
		$("div#wiTaxatemp h1").attr({id:'PageName'});
		$("div#wiTaxatemp div").attr({id:'fileType'});
		$("div#wiTaxatemp td").first().attr({id:'SurrogateCell'}).next().attr({id:'PredictedCell'});
		$("td#SurrogateCell > select").attr({id:'Surrogate', name:'Surrogate'});
		$("td#PredictedCell > select").attr({id:'Predicted', name:'Predicted'});
		$('tr#sortRow select').attr({id:'sortBy'});
		$("#wiTaxatemp input[type='hidden']").attr({name:'file', id:'file'});
		$.getScript('/static/stylesheets/webice/scripts/ice.js', function() {
			document.getElementById('file').value = fileFamily;
			popHeader();
			importSurrogate('Surrogate');
			importPredicted('Predicted');
		});
		$('#contbutton, #backbutton').show();
		$('.webiceSel').hide();
	}
	function pageLoadSSD() {
		$('#wiForm').attr({action:"webice_SSD_output.html"});
		$('#wiSSDtemp').show();
		$("div#wiSSDtemp h1").attr({id:'PageName'});
		$("div#wiSSDtemp td").first().attr({id:'SurrogateCell'}).next().attr({id:'PredictedCell'});
		$("td#SurrogateCell > select").attr({id:'Surrogate', name:'Surrogate'});
		$("td#PredictedCell > select").attr({id:'Predicted', name:'Predicted'});
		$('tr#SurrogateHeaderRow td:nth-child(3) select').attr({id:'sortBy'});
		$("div#wiSSDtemp table:eq(1)").attr({id:'DataTable'});
		$('#DataTable').find('tr').attr({id:'DataRow'});
		$('#wiForm').attr({action:"webiceSSD_out.html"});
		$("#wiSSDtemp input[type='hidden']").first().attr({name:'file', id:'file1'}).next().attr({name:'type1', id:'type1'}).next().attr({name:'type2', id:'type2'});
		$("#SubmitTable").attr({value:'Calculate SSD'});
		$.getScript('/static/stylesheets/webice/scripts/iceSSD.js', function() {
			initPage();
		});
		$('#backbutton').show();
		$('.webiceSel').hide();
	}
	function pageLoadTNE() {
		$('#wiForm').attr({action:"webice_TNE_output.html"});
		$('#ICEContent').show();
		$("div#ICEContent h1").attr({id:'PageName'});
		$("div#ICEContent td:eq(2)").attr({id:'SurrogateCell'});
		$("div#ICEContent table:eq(2)").attr({id:'DataTable'});
		$('#DataTable').find('tr').attr({id:'DataRow'});
		$('#wiForm').attr({action:"webiceTNE_out.html"});
		$("#ICEContent input[type='hidden']").first().attr({name:'file', id:'file1'}).next().attr({name:'type1', id:'type1'}).next().attr({name:'type2', id:'type2'});
		$.getScript('/static/stylesheets/webice/scripts/iceTNE.js', function() {
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


	// $("input[type='submit']").click(function(e) {
	// 	e.preventDefault();
	// 	alert('Form submit clicked');
	// 	$(document).ajaxStart(function(){
	// 		alert('Ajax Started (Loading....)');
	// 	});
	// 	$.ajax({
	// 		url: "/webice_output.html",
	// 		data: "Surrogate=Amphipod+%28Allorchestes+compressa%29&Predicted=Daphnid+%28Daphnia+magna%29&file=as&Algae=&group=&species=&Surrogate=",
	// 		cache: false,
	// 		success: function(url){
	// 			alert('Ajax submit completed!');
	// 			document.open();
	// 			document.write(url);
	// 			document.close();
	// 			$("body").html(url);
	// 		},
	// 		error: function(){
	// 			alert('Ajax Failed!');
	// 		}
	// 	});

	// });

});