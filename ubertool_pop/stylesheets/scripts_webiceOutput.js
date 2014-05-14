$( document ).ready(function() {
	$.getScript('/stylesheets/webice/scripts/iceCalc.js', function() {
		popHeader();
		begin();
	});
});