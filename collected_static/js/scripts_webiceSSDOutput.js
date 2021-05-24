$( document ).ready(function() {
	// function scrollBarInit() {
	// 	// Scrollbar Setup
	// 	console.log('Fired');
	// 	var scrollDivWidth = $('#ssdResults').outerWidth(true);
	// 	$('.scroll-div1, .scroll-div2').css({ width: scrollDivWidth });
	// 	console.log(scrollDivWidth);
	// 	$(".ssdResultsContainerTopScroll").scroll(function(){
	// 		$(".ssdResultsContainer")
	// 			.scrollLeft($(".ssdResultsContainerTopScroll").scrollLeft());
	// 	});
	// 	$(".ssdResultsContainer").scroll(function(){
	// 		$(".ssdResultsContainerTopScroll")
	// 			.scrollLeft($(".ssdResultsContainer").scrollLeft());
	// 	});
	// }
	$.getScript('/static/stylesheets/webice/scripts/ssdCalc.js', function() {
		begin();
	});
	$.getScript('/static/stylesheets/webice/scripts/tablesort.js', function() {
		setClicks('ssdResults');
	});
	setTimeout('reCompute()',1000);
});