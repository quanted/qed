$( document ).ready(function() {
	$.getScript('/static/stylesheets/webice/scripts/iceCalc.js', function() {
		popHeader();
		begin();
	});
});