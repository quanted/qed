$( document ).ready(function() {
	$.getScript('/stylesheets/webice/scripts/tneCalc.js', function() {
		begin();
	});
	$.getScript('/stylesheets/webice/scripts/tablesort.js', function() {
		setClicks('tneResults');
	});
});