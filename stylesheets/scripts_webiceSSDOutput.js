$( document ).ready(function() {
	$.getScript('/stylesheets/webice/scripts/ssdCalc.js', function() {
		begin();
	});
	$.getScript('/stylesheets/webice/scripts/tablesort.js', function() {
		setClicks('ssdResults');
	});
	setTimeout('reCompute()',1000);
});