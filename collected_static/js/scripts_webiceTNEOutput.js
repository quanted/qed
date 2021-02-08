$( document ).ready(function() {
	$.getScript('/static/stylesheets/webice/scripts/tneCalc.js', function() {
		begin();
	});
	$.getScript('/static/stylesheets/webice/scripts/tablesort.js', function() {
		setClicks('tneResults');
	});
});