$( document ).ready(function() {

	$.getScript('http://localhost:8081/stylesheets/webice/scripts/iceCalc.js', function() {
		popHeader();
		begin();
	});
});