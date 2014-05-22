$(document).ready(function() {
	// Log-in
	$('#l_menu a, .logreg').click(function(e) {
		e.preventDefault();
		var destination = $(this).attr('href');
		setTimeout(function() { window.location.href = destination; }, 500);
		$('#topheader_pic_main, #topheader_p_main').animate({
			height:'120px'
		}, 500);
		$('#topheader_p_main p, .logreg').fadeOut(500);
	});
});